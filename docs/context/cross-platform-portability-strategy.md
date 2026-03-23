---
name: "Cross-Platform Portability Strategy"
description: "Portability across DuckDB, Snowflake, Databricks, and ClickHouse requires a layered approach: cross-database macros for basics, dispatch shims for JSON/regex/arrays, dlt abstraction for ingestion, lowest-common-denominator SQL for everything else; SQLGlot is a migration tool not a runtime layer; Python models are non-portable by design"
type: context
related:
  - docs/context/dbt-adapter-dialect-gaps.md
  - docs/context/dlt-destination-type-mapping.md
  - docs/research/2026-03-22-cross-platform-adapter-compatibility.research.md
---

## Key Insight

No single tool or approach solves cross-platform portability. It requires a layered strategy ranked by reliability: cross-database macros, dispatch shims, dlt abstraction, lowest-common-denominator SQL. SQLGlot has significant error rates and belongs only in migration workflows. Python models are fundamentally non-portable.

## The Portability Stack

| Layer | Tool/Pattern | Reliability | What It Covers |
|---|---|---|---|
| 1 | dbt cross-database macros (38 built-in) | HIGH | Date, string, cast, array, aggregates |
| 2 | Custom dispatch shims (`{adapter}__` macros) | HIGH | JSON, regex, array flattening, QUALIFY |
| 3 | dlt canonical type system | MODERATE | Ingestion type mapping (ClickHouse loses fidelity) |
| 4 | Lowest-common-denominator SQL | HIGH | Everything else |
| 5 | SQLGlot transpilation | **LOW** | Migration assistance only |
| 6 | Python models | **NONE** | Non-portable by design |

Each layer handles what the layers above cannot. Skip a layer and you hit portability gaps.

## Layer 1: Cross-Database Macros

dbt's 38 macros normalize the most common dialect differences. Use `{{ dbt.dateadd() }}` instead of native `dateadd`/`date_add`. Use `{{ dbt.safe_cast() }}` instead of `TRY_CAST`/`SAFE_CAST`. These work reliably across all four platforms.

## Layer 2: Dispatch Shims

For operations with no built-in macro, dbt's `adapter.dispatch()` lets you write platform-specific implementations:

1. Define a default macro: `default__extract_json_value`
2. Add adapter-specific overrides: `clickhouse__extract_json_value`, `snowflake__extract_json_value`
3. Configure search order in `dbt_project.yml`

The three operations that always need dispatch shims are JSON path extraction, regex matching, and array flattening. These have incompatible syntax across every platform -- there is no way to write one SQL expression that works everywhere.

## Layer 3: dlt Abstraction

dlt's canonical type system handles ingestion portability. Define a schema once, deploy to any destination. Caveats: ClickHouse degrades json/time/binary to String, Databricks requires Parquet for several types, and merge strategy support varies (ClickHouse lacks upsert). See the dlt destination type mapping context for full details.

## Layer 4: Lowest-Common-Denominator SQL

For everything not covered by macros or dispatch, write SQL that works everywhere:

**Safe to use:** Standard CTEs, JOINs, GROUP BY, basic window functions (ROW_NUMBER, RANK, LAG/LEAD), CASE expressions, subqueries.

**Avoid:** QUALIFY (standalone Spark lacks it), LATERAL FLATTEN (Snowflake-only), VARIANT syntax, spatial extensions, platform-specific date literals, MERGE (ClickHouse lacks it).

## Layer 5: SQLGlot -- Migration Only

SQLGlot parses SQL in one dialect and generates another across 31 dialects. The CrackSQL paper (SIGMOD 2025) documents significant translation error rates on complex constructs, with data type mapping as a primary failure mode. SQLGlot is a parser, not a catalog-aware tool, so it cannot resolve column types or validate semantic correctness.

Use it to accelerate migrations (bulk-translate SQL files with human review). Do not use it as a runtime transpilation layer.

## Layer 6: Python Models Are a Lock-in Decision

Each platform uses a different DataFrame API:
- Snowflake: Snowpark
- Databricks: PySpark
- DuckDB: DuckDB Relations
- ClickHouse: **No Python model support at all**

A Python model written for one platform cannot run on another without rewriting. If your pipeline uses Python models, you are accepting single-platform lock-in. SQL models with cross-database macros and dispatch shims are the only portable path.

## Practical Implications

1. **Default to SQL models.** Python models are a last resort when SQL cannot express the logic.
2. **Build a project-level macro library** for JSON, regex, and array operations with dispatch implementations for each target platform.
3. **Do not rely on dbt contracts for cross-platform data quality.** DuckDB enforces all constraints; Snowflake marks most as metadata-only. Add explicit dbt tests for constraints production does not enforce.
4. **Test incremental models on the actual production adapter.** ClickHouse's lack of merge and its CTE/INSERT limitations will not surface in DuckDB testing.
5. **Treat SQLGlot as a code review assistant,** not a production dependency.

## Takeaway

Portability is achievable for SQL-based pipelines using the first four layers. The cost is maintaining dispatch shims for semi-structured data operations. Python models and SQLGlot runtime transpilation are not viable portability strategies. ClickHouse requires the most adapter-specific work due to its fundamental differences in mutation, incremental strategy, and type support.
