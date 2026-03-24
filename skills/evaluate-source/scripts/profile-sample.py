#!/usr/bin/env python3
"""Profile a sample data file and output structured markdown tables.

Accepts CSV, JSON (newline-delimited or array), or Parquet files.
Uses Python stdlib for CSV/JSON and DuckDB for Parquet and heavier computation.

Usage:
    python profile-sample.py <file_path> [--format csv|json|parquet]

Output:
    Markdown tables to stdout covering:
    - Summary statistics (row count, column count)
    - Column inventory (name, inferred type, nullable)
    - Content metrics per column (null count, null rate, distinct count,
      uniqueness ratio, min, max)
"""

import argparse
import csv
import io
import json
import sys
from pathlib import Path


def detect_format(path: Path) -> str:
    """Detect file format from extension."""
    suffix = path.suffix.lower()
    format_map = {
        ".csv": "csv",
        ".tsv": "csv",
        ".json": "json",
        ".jsonl": "json",
        ".ndjson": "json",
        ".parquet": "parquet",
        ".pq": "parquet",
    }
    fmt = format_map.get(suffix)
    if fmt is None:
        print(f"Error: Cannot detect format from extension '{suffix}'.", file=sys.stderr)
        print("Supported: .csv, .tsv, .json, .jsonl, .ndjson, .parquet", file=sys.stderr)
        sys.exit(1)
    return fmt


def load_csv(path: Path) -> list[dict]:
    """Load CSV file into list of dicts."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_json(path: Path) -> list[dict]:
    """Load JSON file (array or newline-delimited) into list of dicts."""
    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("["):
        return json.loads(text)
    # Newline-delimited JSON
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def load_with_duckdb(path: Path, fmt: str) -> list[dict]:
    """Load file using DuckDB for Parquet support and heavier computation."""
    try:
        import duckdb
    except ImportError:
        print("Error: DuckDB is required for Parquet files.", file=sys.stderr)
        print("Install with: pip install duckdb", file=sys.stderr)
        sys.exit(1)

    conn = duckdb.connect()
    if fmt == "parquet":
        query = f"SELECT * FROM read_parquet('{path}')"
    elif fmt == "csv":
        query = f"SELECT * FROM read_csv('{path}', auto_detect=true)"
    elif fmt == "json":
        query = f"SELECT * FROM read_json('{path}', auto_detect=true)"
    else:
        print(f"Error: Unsupported format '{fmt}' for DuckDB.", file=sys.stderr)
        sys.exit(1)

    result = conn.execute(query)
    columns = [desc[0] for desc in result.description]
    rows = result.fetchall()
    return [dict(zip(columns, row)) for row in rows]


def infer_type(values: list) -> str:
    """Infer the dominant type from a list of values."""
    type_counts: dict[str, int] = {}
    for v in values:
        if v is None or (isinstance(v, str) and v.strip() == ""):
            continue
        if isinstance(v, bool):
            t = "boolean"
        elif isinstance(v, int):
            t = "integer"
        elif isinstance(v, float):
            t = "float"
        elif isinstance(v, str):
            # Try to detect numeric strings
            try:
                int(v)
                t = "integer"
            except (ValueError, TypeError):
                try:
                    float(v)
                    t = "float"
                except (ValueError, TypeError):
                    t = "string"
        else:
            t = type(v).__name__
        type_counts[t] = type_counts.get(t, 0) + 1

    if not type_counts:
        return "unknown"
    return max(type_counts, key=lambda k: type_counts[k])


def compute_metrics(rows: list[dict], columns: list[str]) -> dict:
    """Compute profiling metrics for each column."""
    total = len(rows)
    metrics = {}

    for col in columns:
        values = [row.get(col) for row in rows]
        null_count = sum(
            1 for v in values if v is None or (isinstance(v, str) and v.strip() == "")
        )
        non_null = [
            v for v in values if v is not None and not (isinstance(v, str) and v.strip() == "")
        ]
        distinct_values = set()
        for v in non_null:
            if isinstance(v, (list, dict)):
                distinct_values.add(str(v))
            else:
                distinct_values.add(v)
        distinct_count = len(distinct_values)

        # Min/max for comparable types
        min_val = None
        max_val = None
        if non_null:
            try:
                comparable = sorted(non_null)
                min_val = comparable[0]
                max_val = comparable[-1]
            except TypeError:
                pass

        # Numeric distribution metrics
        numeric_stats = None
        col_type = infer_type(values)
        if col_type in ("integer", "float"):
            nums = []
            for v in non_null:
                try:
                    nums.append(float(v))
                except (ValueError, TypeError):
                    pass
            if nums:
                nums_sorted = sorted(nums)
                n = len(nums_sorted)
                mean = sum(nums_sorted) / n
                variance = sum((x - mean) ** 2 for x in nums_sorted) / n
                stddev = variance ** 0.5

                def percentile(data: list[float], p: float) -> float:
                    k = (len(data) - 1) * (p / 100)
                    f = int(k)
                    c = f + 1 if f + 1 < len(data) else f
                    d = k - f
                    return data[f] + d * (data[c] - data[f])

                p25 = percentile(nums_sorted, 25)
                p50 = percentile(nums_sorted, 50)
                p75 = percentile(nums_sorted, 75)
                iqr = p75 - p25

                # Skewness (Fisher-Pearson)
                skewness = None
                if n >= 3 and stddev > 0:
                    skewness = (
                        sum((x - mean) ** 3 for x in nums_sorted)
                        / (n * stddev ** 3)
                    )

                numeric_stats = {
                    "mean": mean,
                    "stddev": stddev,
                    "p25": p25,
                    "median": p50,
                    "p75": p75,
                    "iqr": iqr,
                    "skewness": skewness,
                }

        # Value frequencies for low-cardinality (categorical) columns
        # Categorical if: low uniqueness ratio AND not a unique identifier
        top_values = None
        uniqueness = distinct_count / total if total > 0 else 1
        is_categorical = (
            distinct_count > 0
            and uniqueness < 0.5
            and distinct_count <= 50
        )
        if is_categorical:
            freq: dict[str, int] = {}
            for v in non_null:
                key = str(v)
                freq[key] = freq.get(key, 0) + 1
            sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
            top_values = sorted_freq[:10]  # Top 10 values

        metrics[col] = {
            "inferred_type": col_type,
            "nullable": null_count > 0,
            "null_count": null_count,
            "null_rate": f"{null_count / total:.1%}" if total > 0 else "N/A",
            "distinct_count": distinct_count,
            "uniqueness_ratio": (
                f"{distinct_count / total:.3f}" if total > 0 else "N/A"
            ),
            "min": min_val,
            "max": max_val,
            "numeric_stats": numeric_stats,
            "is_categorical": is_categorical,
            "top_values": top_values,
        }

    return metrics


def format_value(v) -> str:
    """Format a value for markdown output."""
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.4g}"
    return str(v)


def print_report(rows: list[dict], columns: list[str], file_path: str) -> None:
    """Print the profiling report as markdown."""
    total = len(rows)
    metrics = compute_metrics(rows, columns)

    print(f"# Data Profile: `{file_path}`\n")

    # Summary
    print("## Summary\n")
    print(f"| Metric | Value |")
    print(f"|--------|-------|")
    print(f"| **Row count** | {total:,} |")
    print(f"| **Column count** | {len(columns)} |")
    print()

    # Column inventory
    print("## Column Inventory\n")
    print("| # | Column | Inferred Type | Nullable |")
    print("|--:|--------|---------------|:--------:|")
    for i, col in enumerate(columns, 1):
        m = metrics[col]
        nullable = "yes" if m["nullable"] else "no"
        print(f"| {i} | `{col}` | {m['inferred_type']} | {nullable} |")
    print()

    # Content metrics
    print("## Content Metrics\n")
    print(
        "| Column | Null Count | Null Rate | Distinct Count | Uniqueness Ratio | Min | Max |"
    )
    print(
        "|--------|:----------:|:---------:|:--------------:|:----------------:|-----|-----|"
    )
    for col in columns:
        m = metrics[col]
        print(
            f"| `{col}` | {m['null_count']} | {m['null_rate']} "
            f"| {m['distinct_count']} | {m['uniqueness_ratio']} "
            f"| {format_value(m['min'])} | {format_value(m['max'])} |"
        )
    print()

    # Numeric distribution
    numeric_cols = [c for c in columns if metrics[c]["numeric_stats"] is not None]
    if numeric_cols:
        print("## Numeric Distribution\n")
        print(
            "| Column | Mean | Std Dev | P25 | Median | P75 | IQR | Skewness |"
        )
        print(
            "|--------|-----:|--------:|----:|-------:|----:|----:|---------:|"
        )
        for col in numeric_cols:
            s = metrics[col]["numeric_stats"]
            skew = format_value(s["skewness"]) if s["skewness"] is not None else "N/A"
            print(
                f"| `{col}` | {format_value(s['mean'])} | {format_value(s['stddev'])} "
                f"| {format_value(s['p25'])} | {format_value(s['median'])} "
                f"| {format_value(s['p75'])} | {format_value(s['iqr'])} "
                f"| {skew} |"
            )
        print()

    # Categorical analysis
    cat_cols = [c for c in columns if metrics[c]["is_categorical"]]
    if cat_cols:
        print("## Categorical Analysis\n")
        print(
            "Low-cardinality columns (<50% uniqueness ratio). "
            "Top values by frequency:\n"
        )
        for col in cat_cols:
            m = metrics[col]
            print(f"### `{col}` — {m['distinct_count']} distinct values\n")
            print("| Value | Count | Frequency |")
            print("|-------|------:|----------:|")
            for val, count in m["top_values"]:
                freq_pct = f"{count / total:.1%}" if total > 0 else "N/A"
                print(f"| {val} | {count:,} | {freq_pct} |")
            print()

    # Key candidates
    print("## Key Candidates\n")
    candidates = [
        col
        for col in columns
        if metrics[col]["distinct_count"] == total and not metrics[col]["nullable"]
    ]
    if candidates:
        for col in candidates:
            print(f"- `{col}` — unique and non-null across all {total:,} rows")
    else:
        print("No columns are both unique and non-null across all rows.")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Profile a sample data file and output structured markdown tables.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Supported formats: CSV (.csv, .tsv), JSON (.json, .jsonl, .ndjson), "
            "Parquet (.parquet, .pq)\n\n"
            "Examples:\n"
            "  python profile-sample.py data.csv\n"
            "  python profile-sample.py events.jsonl\n"
            "  python profile-sample.py warehouse.parquet --format parquet\n"
        ),
    )
    parser.add_argument("file", help="Path to the data file to profile")
    parser.add_argument(
        "--format",
        choices=["csv", "json", "parquet"],
        help="File format (auto-detected from extension if omitted)",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    fmt = args.format or detect_format(path)

    # Use DuckDB for parquet; stdlib for csv/json
    if fmt == "parquet":
        rows = load_with_duckdb(path, fmt)
    elif fmt == "csv":
        rows = load_csv(path)
    elif fmt == "json":
        rows = load_json(path)
    else:
        print(f"Error: Unsupported format: {fmt}", file=sys.stderr)
        sys.exit(1)

    if not rows:
        print("Warning: File contains no data rows.", file=sys.stderr)
        sys.exit(0)

    columns = list(rows[0].keys())
    print_report(rows, columns, args.file)


if __name__ == "__main__":
    main()
