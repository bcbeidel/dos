---
name: "dbt Adapter Dialect Gaps"
description: "dbt's 38 cross-database macros cover date/string/cast but have zero coverage for JSON, regex, and array flattening; ClickHouse is the cross-platform outlier with no merge, no Python models, and broken ephemeral models; contract enforcement diverges between DuckDB (full) and Snowflake (metadata-only)"
type: context
related:
  - docs/context/dlt-destination-type-mapping.md
  - docs/context/cross-platform-portability-strategy.md
  - docs/research/2026-03-22-cross-platform-adapter-compatibility.research.md
---

## Key Insight

dbt's cross-database macros solve basic SQL dialect differences but leave the three hardest problems uncovered: JSON path extraction, regex, and array flattening. ClickHouse breaks assumptions that hold across the other three platforms (DuckDB, Snowflake, Databricks). Contract enforcement gives false confidence when moving from DuckDB dev to production.

## What the 38 Cross-Database Macros Cover

dbt provides macros across eight categories: data types (8), strings (7), date/time (5), casting (3), sets (2), arrays (3), aggregates (3), and other (2). These normalize `dateadd`, `datediff`, `concat`, `safe_cast`, `listagg`, and similar operations across all target platforms.

## What They Do Not Cover

**JSON path extraction** has four incompatible syntaxes that cannot share function signatures:
- Snowflake: `doc:path` or `GET_PATH(doc, 'path')`
- DuckDB: `doc -> 'key'`
- Databricks: `doc.key` or `get_json_object()`
- ClickHouse: `JSONExtractString(doc, 'key')`

**Regex** is similarly fragmented: `REGEXP_LIKE` (Snowflake), `RLIKE` (Spark/Databricks), `regexp_matches` (DuckDB), `match()` (ClickHouse), with behavioral differences like auto-anchoring.

**Array flattening** uses four different constructs: `LATERAL FLATTEN` (Snowflake), `UNNEST` (DuckDB), `EXPLODE` (Spark/Databricks), `arrayJoin` (ClickHouse).

Any pipeline working with semi-structured data must write custom dispatch macros for each adapter.

## ClickHouse Is the Outlier

ClickHouse breaks multiple assumptions that hold across the other three platforms:

- **No merge incremental strategy.** The default creates a full table copy and swaps, which is expensive. `delete+insert` with lightweight deletes is the only viable incremental approach.
- **No standard UPDATE/DELETE.** Uses `ALTER TABLE DELETE` (heavy mutation) or lightweight deletes (v22.8+, opt-in).
- **CTEs do not work with INSERT.** Ephemeral models fail when included in table model SELECT.
- **No Python model support.** SQL models with dispatch shims are the only portable path.
- **`ReplicatedMergeTree` deduplication** can prevent re-insertion after `delete+insert`, creating silent data loss.

## Incremental Strategy Matrix

| Strategy | DuckDB | Snowflake | Databricks | ClickHouse |
|---|---|---|---|---|
| append | Yes | Yes | Yes | Yes |
| merge | Yes (>=1.4.0) | Yes (default) | Yes (Delta only) | **No** |
| delete+insert | Yes (default) | Yes | Yes (DBR 12.2+) | Yes |
| microbatch | Yes | Yes | Yes | Yes |

Snowflake's merge fails with "nondeterministic merge" when `unique_key` has duplicates -- use `delete+insert` instead.

## Contract Enforcement Divergence

| Constraint | DuckDB | Snowflake | Databricks | ClickHouse |
|---|---|---|---|---|
| not_null | Enforced | Enforced | Enforced (post-build) | Exact type only |
| primary_key | Enforced | **Metadata only** | **Metadata only** | Not supported |
| unique | Enforced | **Metadata only** | Not supported | Not supported |
| foreign_key | Enforced | **Metadata only** | Not supported | Not supported |
| check | Enforced | Not supported | Enforced (post-build) | Not supported |

A contract that passes in DuckDB local dev will silently allow invalid data in Snowflake or Databricks production. Teams relying on contracts for enforcement must add explicit dbt tests for constraints the production warehouse does not enforce.

## Takeaway

For covered operations, use cross-database macros. For JSON, regex, and arrays, write adapter-specific macros using the `dispatch()` pattern with `{adapter}__` prefix convention. Treat ClickHouse as architecturally distinct -- it needs separate incremental strategy, separate macro implementations, and testing against its specific limitations.
