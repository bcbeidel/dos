---
name: Schema Evolution
description: How to handle schema changes in data pipelines; compatibility rules, expand-and-contract pattern, tool-specific gaps in dbt/dlt/Delta Lake
type: context
related:
  - docs/research/2026-03-21-pipeline-design-architecture.research.md
  - docs/context/incremental-loading-patterns.md
  - docs/context/data-contract-structure.md
  - docs/context/data-contract-enforcement-versioning.md
  - docs/context/schema-drift-risk.md
  - docs/context/data-contracts.md
---

## Key Takeaway

Plan for schema evolution before the first production deploy. The expand-and-contract pattern is theoretically sound but has practical gaps: dbt cannot track nested column changes or backfill new columns, and Delta Lake schema updates terminate active streams. Choose your contract strictness early and accept that nested column evolution is a known blind spot across tools.

## Change Compatibility

| Change Type | Forward-Compatible | Backward-Compatible |
|---|---|---|
| Add optional column | Yes | Yes |
| Add required column | Yes | No |
| Drop optional column | Yes | Yes |
| Drop required column | No | Yes |
| Rename column | No | No |
| Widen type (int to long) | No | Yes |
| Narrow type (long to int) | Yes | No |
| Swap type (double to enum) | No | No |

**Non-breaking changes:** Adding optional fields with defaults, adding new enum values tolerated by consumers, extending nested structures with optional attributes.

**Breaking changes:** Removing required fields, tightening nullability, changing data types incompatibly, renaming fields without aliases.

## Expand-and-Contract Pattern

The standard zero-downtime migration approach in five steps:

1. **Expand:** Add new fields as nullable/optional with defaults. Keep old fields.
2. **Backfill:** Populate new fields for historical data. Run idempotent backfills.
3. **Dual-read/write:** Producers write both old and new fields during transition window.
4. **Cutover:** Migrate consumers to new fields. Turn off dual-writes at 100% adoption.
5. **Contract:** Deprecate and remove old fields after a safe window.

**Practical problems:** Requires minimum three production deployments per field rename. The "contract" phase commonly stalls, leaving deprecated fields indefinitely -- a frequent source of schema bloat. Reverting a contraction step cannot be done without data loss or backup restoration.

## Tool-Specific Behavior

### dbt (`on_schema_change`)

Four modes: `ignore` (default -- new columns silently dropped, removed columns cause failures), `fail` (error on any divergence), `append_new_columns` (adds new, keeps removed), `sync_all_columns` (adds new, removes old, handles type changes).

**Critical gaps:**
- Does not track nested column changes
- None of the modes backfill new columns in existing rows
- For backfill, you must run manual updates or trigger `--full-refresh`
- On BigQuery, `sync_all_columns` type changes require a full table scan

### dlt

Auto-detects new columns and creates variant columns for type changes using the naming convention `column_name__v_datatype` (e.g., `inventory_nr__v_text` when an integer column receives string data). Flattens nested dictionaries and unpacks nested lists into sub-tables.

Four contract modes controlling strictness:
- **evolve** (default): No constraints on schema changes
- **freeze:** Raises exception on non-conforming data
- **discard_row:** Drops rows that don't match schema
- **discard_value:** Drops non-conforming values, loads row without them

Contracts apply separately to tables (new table creation), columns (new column addition), and data_type (type changes including nullability, precision, scale).

### Delta Lake

Supports ADD, RENAME, DROP COLUMN operations plus automatic evolution via `MERGE WITH SCHEMA EVOLUTION` or `.option("mergeSchema", "true")`.

**Critical behaviors:**
- Schema updates conflict with all concurrent write operations
- Schema updates terminate any active streams reading from the table
- DROP COLUMN is metadata-only -- physical purge requires REORG TABLE + VACUUM
- Adding nested columns supported only for structs, not arrays or maps
- Databricks recommends per-write `WITH SCHEMA EVOLUTION` syntax over Spark-level configuration

### CDC Pipelines

Debezium publishes DDL changes to dedicated Kafka topics (MySQL, SQL Server). PostgreSQL lacks DDL support in logical decoding -- schema changes appear only in data change events. The **outbox pattern** isolates downstream consumers: write to both application tables and a dedicated outbox table, CDC captures only from outbox. Internal schema changes stay invisible to consumers, but requires application modification.

## Decision Rules

1. Choose contract strictness at project start. Default to dlt's `evolve` for development, tighten to `freeze` or `discard_row` for production.
2. Treat all renames as breaking changes regardless of tooling. Use expand-and-contract.
3. Add fields as optional with defaults. Never flip nullability in one shot.
4. Version schemas visibly -- include a version field in messages, store schemas in a repo with changelogs.
5. Monitor for schema drift: contract checks and schema diffs on new batches. Quarantine unexpected data in a DLQ or bronze quarantine layer.
