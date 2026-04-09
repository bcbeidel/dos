#!/usr/bin/env python3
"""Profile a data file using DuckDB and output structured results.

DuckDB handles all file formats and statistics computation natively.
The script produces a structured profile dict, then renders it as
markdown (stdout) or JSON (--json flag).

Usage:
    python profile-sample.py <file_path> [--format csv|json|parquet]
    python profile-sample.py <file_path> --json
    python profile-sample.py <file_path> --json --output profile.json

Output:
    Default: Markdown tables to stdout
    --json:  JSON profile to stdout
    --output: JSON profile to file, markdown to stdout
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

try:
    import duckdb
except ImportError:
    print("Error: DuckDB required. Install with: pip install duckdb", file=sys.stderr)
    sys.exit(1)

FORMATS = {
    ".csv": "csv", ".tsv": "csv",
    ".json": "json", ".jsonl": "json", ".ndjson": "json",
    ".parquet": "parquet", ".pq": "parquet",
}

READERS = {
    "csv": "read_csv('{path}', auto_detect=true)",
    "json": "read_json('{path}', auto_detect=true)",
    "parquet": "read_parquet('{path}')",
}

# DuckDB types that get numeric distribution stats
NUMERIC_TYPES = {"TINYINT", "SMALLINT", "INTEGER", "BIGINT", "HUGEINT",
                 "FLOAT", "DOUBLE", "DECIMAL", "UTINYINT", "USMALLINT",
                 "UINTEGER", "UBIGINT"}

# Cardinality threshold for frequent-item analysis
CATEGORICAL_MAX_DISTINCT = 50
CATEGORICAL_MAX_UNIQUENESS = 0.5


def detect_format(path: Path) -> str:
    fmt = FORMATS.get(path.suffix.lower())
    if not fmt:
        print(f"Error: Unknown extension '{path.suffix}'", file=sys.stderr)
        sys.exit(1)
    return fmt


def profile(file_path: Path, fmt: str) -> dict:
    """Build a structured profile using DuckDB native functions."""
    con = duckdb.connect()
    reader = READERS[fmt].format(path=file_path)
    con.execute(f"CREATE TABLE source AS SELECT * FROM {reader}")

    row_count = con.execute("SELECT count(*) FROM source").fetchone()[0]
    if row_count == 0:
        return {"dataset": {"row_count": 0, "column_count": 0}, "columns": {}}

    # SUMMARIZE: one statement for base stats on every column
    summary = con.execute("SUMMARIZE source").fetchall()
    col_names = [desc[0] for desc in con.execute("SUMMARIZE source").description]
    summary_dicts = [dict(zip(col_names, row)) for row in summary]

    columns = {}
    for row in summary_dicts:
        name = row["column_name"]
        col_type = row["column_type"]
        count = int(row["count"])
        null_pct = float(row["null_percentage"])
        approx_unique = int(row["approx_unique"])

        entry = {
            "type": col_type,
            "count": count,
            "null_count": round(null_pct * count / 100),
            "null_pct": round(null_pct, 2),
            "approx_unique": approx_unique,
            "uniqueness_ratio": round(min(approx_unique / count, 1.0), 4) if count > 0 else None,
            "min": _safe_str(row["min"]),
            "max": _safe_str(row["max"]),
        }

        # Numeric columns: extended distribution stats
        base_type = col_type.split("(")[0].upper()
        if base_type in NUMERIC_TYPES and row["std"] is not None:
            ext = con.execute(f"""
                SELECT
                    round(skewness("{name}"), 4),
                    round(kurtosis("{name}"), 4)
                FROM source
            """).fetchone()
            q25 = _safe_float(row["q25"])
            q75 = _safe_float(row["q75"])
            entry.update({
                "mean": _safe_float(row["avg"]),
                "stddev": _safe_float(row["std"]),
                "q25": q25,
                "median": _safe_float(row["q50"]),
                "q75": q75,
                "iqr": round(q75 - q25, 4) if q25 is not None and q75 is not None else None,
                "skewness": _safe_float(ext[0]),
                "kurtosis": _safe_float(ext[1]),
            })

        # Low-cardinality columns: frequent items
        if (approx_unique <= CATEGORICAL_MAX_DISTINCT
                and count > 0
                and approx_unique / count < CATEGORICAL_MAX_UNIQUENESS):
            freq = con.execute(f"""
                SELECT "{name}" as value, count(*) as freq,
                       round(count(*) * 100.0 / {count}, 2) as pct
                FROM source WHERE "{name}" IS NOT NULL
                GROUP BY "{name}" ORDER BY freq DESC LIMIT 10
            """).fetchall()
            entry["frequent_items"] = [
                {"value": str(r[0]), "frequency": int(r[1]), "pct": float(r[2])}
                for r in freq
            ]

        columns[name] = entry

    # Key candidates: columns that are unique and fully non-null
    key_candidates = [
        name for name, col in columns.items()
        if col["null_pct"] == 0.0
        and col["uniqueness_ratio"] is not None
        and col["uniqueness_ratio"] >= 0.99
    ]

    return {
        "dataset": {"row_count": row_count, "column_count": len(columns)},
        "columns": columns,
        "key_candidates": key_candidates,
    }


def _safe_str(val) -> Optional[str]:
    if val is None:
        return None
    return str(val)


def _safe_float(val) -> Optional[float]:
    if val is None:
        return None
    try:
        return round(float(val), 4)
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Markdown renderer
# ---------------------------------------------------------------------------

def render_markdown(prof: dict, file_path: str) -> str:
    lines = []
    ds = prof["dataset"]
    cols = prof["columns"]

    lines.append(f"# Data Profile: `{file_path}`\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| **Row count** | {ds['row_count']:,} |")
    lines.append(f"| **Column count** | {ds['column_count']} |")

    sampling = ds.get("sampling", {})
    if sampling.get("total_population"):
        lines.append(f"| **Total population** | {sampling['total_population']:,} |")
        pct = round(ds['row_count'] * 100 / sampling['total_population'], 1)
        lines.append(f"| **Sample coverage** | {pct}% |")
    lines.append("")

    # Sampling warnings
    if sampling.get("warnings"):
        lines.append("> **Sampling caveat**")
        for w in sampling["warnings"]:
            lines.append(f"> {w}")
        lines.append("")

    # Column inventory
    lines.append("## Column Inventory\n")
    lines.append("| # | Column | Type | Nullable |")
    lines.append("|--:|--------|------|:--------:|")
    for i, (name, col) in enumerate(cols.items(), 1):
        nullable = "yes" if col["null_count"] > 0 else "no"
        lines.append(f"| {i} | `{name}` | {col['type']} | {nullable} |")
    lines.append("")

    # Content metrics
    lines.append("## Content Metrics\n")
    lines.append("| Column | Nulls | Null % | Distinct | Uniqueness | Min | Max |")
    lines.append("|--------|------:|-------:|---------:|-----------:|-----|-----|")
    for name, col in cols.items():
        lines.append(
            f"| `{name}` | {col['null_count']} | {col['null_pct']}% "
            f"| {col['approx_unique']} | {col['uniqueness_ratio']} "
            f"| {col['min'] or ''} | {col['max'] or ''} |"
        )
    lines.append("")

    # Numeric distribution
    num = {n: c for n, c in cols.items() if "mean" in c}
    if num:
        lines.append("## Numeric Distribution\n")
        lines.append("| Column | Mean | Std Dev | Q25 | Median | Q75 | IQR | Skew |")
        lines.append("|--------|-----:|--------:|----:|-------:|----:|----:|-----:|")
        for name, col in num.items():
            f = lambda v: f"{v:.4g}" if v is not None else "—"
            lines.append(
                f"| `{name}` | {f(col['mean'])} | {f(col['stddev'])} "
                f"| {f(col['q25'])} | {f(col['median'])} "
                f"| {f(col['q75'])} | {f(col['iqr'])} | {f(col['skewness'])} |"
            )
        lines.append("")

    # Categorical analysis
    cat = {n: c for n, c in cols.items() if "frequent_items" in c}
    if cat:
        lines.append("## Categorical Analysis\n")
        for name, col in cat.items():
            lines.append(f"### `{name}` — {col['approx_unique']} distinct values\n")
            lines.append("| Value | Count | % |")
            lines.append("|-------|------:|--:|")
            for item in col["frequent_items"]:
                lines.append(f"| {item['value']} | {item['frequency']:,} | {item['pct']}% |")
            lines.append("")

    # Key candidates
    lines.append("## Key Candidates\n")
    keys = prof.get("key_candidates", [])
    if keys:
        for name in keys:
            lines.append(f"- `{name}` — unique and non-null")
    else:
        lines.append("No columns are both unique and non-null across all rows.")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Sampling metadata
# ---------------------------------------------------------------------------

# Row counts that suggest a --limit flag was used during extraction
_ROUND_THRESHOLDS = {10, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500,
                     5000, 10000, 25000, 50000, 100000}


def _build_sampling_metadata(row_count: int, total_population: Optional[int]) -> dict:
    """Build sampling provenance metadata for the profile."""
    sampling = {
        "sample_size": row_count,
        "total_population": total_population,
        "is_complete": total_population is None or row_count >= total_population,
    }

    warnings = []

    # Detect suspiciously round row counts that suggest a --limit flag
    if row_count in _ROUND_THRESHOLDS:
        warnings.append(
            f"Row count ({row_count}) is a round number — may indicate a "
            f"--limit flag was used during extraction. If the source API "
            f"returns records in a deterministic order (e.g., alphabetical, "
            f"by ID), this sample may not be representative of the full "
            f"population. Distribution metrics should be treated as "
            f"illustrative of value ranges, not population proportions."
        )

    # Warn if explicitly a partial sample
    if total_population is not None and row_count < total_population:
        pct = round(row_count * 100 / total_population, 1)
        warnings.append(
            f"This profile covers {pct}% of the total population "
            f"({row_count:,} of {total_population:,} records). "
            f"Re-profile after the first full production load."
        )

    if warnings:
        sampling["warnings"] = warnings

    return sampling


# ---------------------------------------------------------------------------
# JSON encoder for dates and other non-serializable types
# ---------------------------------------------------------------------------

class ProfileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Profile a data file using DuckDB.",
        epilog="Formats: CSV (.csv/.tsv), JSON (.json/.jsonl/.ndjson), Parquet (.parquet/.pq)",
    )
    parser.add_argument("file", help="Path to the data file")
    parser.add_argument("--format", choices=["csv", "json", "parquet"],
                        help="File format (auto-detected from extension if omitted)")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON profile instead of markdown")
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="Write JSON profile to FILE (markdown still goes to stdout)")
    parser.add_argument("--sample-of", type=int, metavar="N",
                        help="Total population size (if this file is a sample, not the full dataset)")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    fmt = args.format or detect_format(path)
    result = profile(path, fmt)

    # Add sampling metadata
    row_count = result["dataset"]["row_count"]
    sampling = _build_sampling_metadata(row_count, args.sample_of)
    result["dataset"]["sampling"] = sampling

    if row_count == 0:
        print("Warning: File contains no data rows.", file=sys.stderr)
        sys.exit(0)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2, cls=ProfileEncoder)

    if args.json:
        print(json.dumps(result, indent=2, cls=ProfileEncoder))
    else:
        print(render_markdown(result, args.file))


if __name__ == "__main__":
    main()
