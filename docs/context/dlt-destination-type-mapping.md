---
name: "dlt Destination Type Mapping"
description: "dlt's canonical type system maps to native types per destination but ClickHouse degrades json/time/binary to String; Databricks requires Parquet for json/decimal/binary; nested data behavior at max_table_nesting=0 diverges silently across all four platforms"
type: context
related:
  - docs/context/dbt-adapter-dialect-gaps.md
  - docs/context/cross-platform-portability-strategy.md
  - docs/research/2026-03-22-cross-platform-adapter-compatibility.research.md
---

## Key Insight

dlt provides a canonical type system for write-once-deploy-anywhere ingestion, but type fidelity varies significantly by destination. ClickHouse loses the most fidelity (json, time, binary all become String). Databricks requires Parquet format for several types. These differences are silent -- no error is raised, data just arrives in a degraded form.

## Type Mapping Matrix

| dlt Type | DuckDB | Snowflake | Databricks | ClickHouse |
|---|---|---|---|---|
| text | TEXT | VARCHAR | STRING | String |
| double | DOUBLE | FLOAT | DOUBLE | Float64 |
| bool | BOOLEAN | BOOLEAN | BOOLEAN | Bool |
| timestamp | TIMESTAMP / TIMESTAMPTZ | TIMESTAMP_NTZ / TIMESTAMP_TZ | TIMESTAMP | DateTime64 |
| date | DATE | DATE | DATE | Date |
| time | TIME | TIME | TIME | **String** |
| bigint | BIGINT | NUMBER | BIGINT | Int64 |
| binary | BLOB | BINARY | BINARY | **String** (base64) |
| json | JSON (native) | VARIANT | Not via JSONL | **String** |
| decimal | DECIMAL | DECIMAL(38,9) | Not via JSONL | Decimal (rounding risk) |

**Critical divergences:**
- ClickHouse: `json`, `time`, `binary` all degrade to String with no native querying support.
- Databricks: `json`, `decimal`, `date`, `binary` cannot be loaded via JSONL -- Parquet is required.
- Snowflake: JSON stored inside VARIANT becomes string when loaded via Parquet.

## File Format Requirements

| Destination | Preferred Loader | Preferred Staging |
|---|---|---|
| DuckDB | insert-values | N/A |
| Snowflake | JSONL | JSONL |
| Databricks | Parquet | Parquet |
| ClickHouse | JSONL | JSONL |

Databricks' Parquet requirement is the reason several types fail via JSONL. This is a format-level constraint, not a platform limitation.

## Merge Strategy Support

| Strategy | DuckDB | Snowflake | Databricks | ClickHouse |
|---|---|---|---|---|
| delete-insert | Yes | Yes | Yes | Yes |
| upsert | Yes | Yes | Yes | **No** |
| scd2 | Yes | Yes | Yes | Yes |

ClickHouse lacks upsert but offers `ReplacingMergeTree` as a native alternative. Deduplication happens asynchronously during background merges, not at insert time.

## Nested Data Divergence

dlt flattens nested JSON into child tables by default, using `_dlt_id`, `_dlt_parent_id`, `_dlt_list_idx`, and `_dlt_root_id` columns for lineage. The `max_table_nesting` setting controls depth.

At `max_table_nesting=0` (store as JSON column, no child tables), behavior diverges silently:
- **DuckDB:** Native JSON column, queryable with JSON functions.
- **Snowflake:** VARIANT column, queryable -- but becomes string if loaded via Parquet.
- **Databricks:** JSON not supported via JSONL format at all.
- **ClickHouse:** String column with no JSON querying capability.

## Schema Evolution Behavior

When a column's data type changes, dlt does not alter the column in place. It creates a new column with a version suffix (e.g., `inventory_nr__v_text`). On ClickHouse, sorting and partition keys are immutable after table creation, which means schema evolution cannot touch key columns.

## Additional Platform Quirks

- **ClickHouse is case-sensitive** for identifiers. All other destinations are case-insensitive.
- **ClickHouse lacks multiple datasets per database.** dlt emulates datasets by prefixing table names with the dataset name using a `___` separator and creating a sentinel table.
- **ClickHouse float rounding errors** are documented and can cause test failures on exact comparisons.

## Takeaway

dlt's canonical type system works well for basic types (text, double, bool, bigint, timestamp, date) across all four platforms. For json, time, binary, and decimal, expect degraded fidelity on ClickHouse and format-dependent behavior on Databricks. Test nested data handling explicitly on each target platform rather than assuming DuckDB local behavior transfers.
