---
name: Platform Tooling Compatibility
description: dbt adapter maturity and dlt destination support across ClickHouse, BigQuery, Redshift, Athena, Databricks, and Snowflake — incremental strategies, merge capabilities, and known gaps
type: context
related:
  - docs/research/2026-03-22-production-platform-landscape.research.md
  - docs/context/production-platform-comparison.md
---

## Key Insight

dbt adapter maturity varies significantly across platforms and is a real constraint on platform choice. The four first-party adapters (BigQuery, Redshift, Databricks, Snowflake) are materially more capable than dbt-clickhouse (no merge, no dbt Cloud) or dbt-athena (community-maintained, merge requires Iceberg). dlt has broad destination coverage but nested data handling is consistently lossy across all platforms.

## dbt Adapter Maturity

**First-party (dbt Labs maintained):** dbt-snowflake, dbt-bigquery, dbt-redshift, dbt-databricks. All support dbt Cloud and the Fusion Engine. Full incremental strategy support including microbatch. dbt-snowflake is the most complete with no significant limitations.

**Vendor-maintained:** dbt-clickhouse (ClickHouse Inc). No dbt Cloud support. No Fusion Engine. No merge incremental strategy — only append and delete+insert (default). insert_overwrite is experimental. No catalog integrations. This is the most consequential gap for teams standardizing on dbt.

**Community Trusted:** dbt-athena. Supported in dbt Cloud. Merge requires Iceberg tables and engine v3. No microbatch support. insert_overwrite is the default. 100-partition limit on insert_overwrite. Snapshot materialization cannot drop columns.

## Incremental Strategy Matrix

| Strategy | Snowflake | BigQuery | Redshift | Databricks | Athena | ClickHouse |
|---|---|---|---|---|---|---|
| append | Yes | Yes | Yes | Yes | Yes | Yes |
| merge | Yes | Yes | Yes | Yes | Iceberg only | **No** |
| delete+insert | Yes | Yes | Yes | Yes | Yes | Yes (default) |
| insert_overwrite | Yes | Yes | Yes | Yes | Yes (default) | Experimental |
| microbatch | Yes | Yes | Yes | Yes | **No** | Yes |

Microbatch underlying mechanisms differ: Snowflake/Redshift use delete+insert; BigQuery uses insert_overwrite; Databricks uses replace_where.

## dlt Destination Support

All six platforms are supported dlt destinations with append, replace, and merge write dispositions. The differences appear in merge strategies and data handling.

**Full merge strategies** (delete-insert, upsert, scd2, insert-only): BigQuery, Snowflake, Databricks.

**Partial merge:** Redshift (delete-insert, scd2 — no upsert). Athena (delete-insert only, Iceberg required). ClickHouse (basic merge with primary_key only — no delete-insert, upsert, or scd2).

**Staging:** All platforms support cloud storage staging. Athena requires filesystem staging (mandatory). Snowflake and BigQuery support atomic swap and clone operations for replace disposition.

## Known Gaps by Platform

**ClickHouse:** Complex types stored as text. No `time` datatype. Float/double rounding errors (use decimal). Merge requires explicit primary_key but supports only basic merge — no advanced strategies. Default engine is ReplicatedMergeTree.

**BigQuery:** Cannot load JSON columns from Parquet (format conflict). INT64 partitioning capped at 10,000 partitions. Nested fields stored as JSON, not native RECORD, unless autodetect enabled. Aggressive type coercion.

**Snowflake:** JSON loads as string in VARIANT with Parquet. DECFLOAT limited to text formats only.

**Databricks:** JSONL cannot handle decimal, json, date, or binary types. Delta Live Tables naming conflicts in notebooks.

**Redshift:** Cannot load VARBYTE from JSON or TIME from JSON/Parquet. No upsert merge strategy.

**Athena:** No JSON field support (stored as string). Merge requires Iceberg tables. Staging is mandatory. Timestamp precision: milliseconds for standard tables, microseconds for Iceberg.

## Nested Data: Universal Weakness

Nested data is the consistent pain point across dlt destinations. Most platforms store nested structures as text or JSON strings rather than native nested types. Plan for flattening or post-load transformation of nested structures regardless of destination choice.

## Bottom Line

If standardizing on dbt, the adapter gap matters: dbt-clickhouse's lack of merge and dbt Cloud support makes it the weakest link. For dlt, all six platforms work for basic ingestion, but merge strategy coverage and nested data handling vary enough to affect pipeline design decisions. Snowflake and Databricks offer the most complete tooling support across both dbt and dlt.
