# Cross-Platform SQL & Platform Detection

## Platform Detection

Before generating models, detect the target platform from `dbt_project.yml` or `profiles.yml`. Each platform has constraints that affect code generation.

## The 38 Cross-Database Macros

dbt provides macros across 8 categories (date, string, cast, array, aggregate, set, type, other). Use these instead of native SQL:

```sql
-- Use this:
{{ dbt.dateadd("day", 7, "created_at") }}
-- Not this:
dateadd(day, 7, created_at)  -- Snowflake-only syntax
```

## Zero Coverage Areas

Three operations have **incompatible syntax across every platform** and require custom dispatch shims:

| Operation | Snowflake | DuckDB | Databricks | ClickHouse |
|-----------|-----------|--------|------------|------------|
| JSON path | `doc:path` | `doc -> 'key'` | `doc.key` | `JSONExtractString()` |
| Regex | `REGEXP_LIKE` | `regexp_matches` | `RLIKE` | `match()` |
| Array flatten | `LATERAL FLATTEN` | `UNNEST` | `EXPLODE` | `arrayJoin` |

**If the contract schema includes JSON types:** require dispatch shim implementations before generating models. Do not proceed without them — the generated SQL will not be portable.

## ClickHouse Incompatibilities

ClickHouse is architecturally distinct. Flag these before generating code:

| Feature | Other Platforms | ClickHouse |
|---------|----------------|------------|
| Incremental merge | Supported | **Not supported** — use `delete+insert` with lightweight deletes |
| Python models | Supported | **Not supported** — SQL only |
| CTEs with INSERT | Works | **Fails** — ephemeral models break when included in table model SELECT |
| UPDATE/DELETE | Standard | `ALTER TABLE DELETE` (heavy) or lightweight deletes (v22.8+) |
| ReplicatedMergeTree | N/A | Deduplication prevents re-insertion after `delete+insert` — silent data loss risk |

**Recommendation for ClickHouse:** Append-only patterns with materialized views for pre-aggregation.

## Incremental Strategy by Platform

| Strategy | DuckDB | Snowflake | Databricks | ClickHouse |
|----------|--------|-----------|------------|------------|
| append | Yes | Yes | Yes | Yes |
| merge | Yes (>=1.4.0) | Yes (default) | Yes (Delta) | **No** |
| delete+insert | Yes (default) | Yes | Yes (DBR 12.2+) | Yes |
| microbatch | Yes | Yes | Yes | Yes |

Snowflake merge fails with "nondeterministic merge" when `unique_key` has duplicates.

## Semi-Structured Data Handling

If the contract schema includes JSON, regex, or array operations, build a dispatch macro library:

```sql
-- macros/extract_json_value.sql
{% macro extract_json_value(column, path) %}
  {{ return(adapter.dispatch('extract_json_value')(column, path)) }}
{% endmacro %}

{% macro snowflake__extract_json_value(column, path) %}
  {{ column }}:{{ path }}
{% endmacro %}

{% macro duckdb__extract_json_value(column, path) %}
  {{ column }} -> '{{ path }}'
{% endmacro %}
```

## Portability Rules

1. **Default to SQL models.** Python models lock you to one platform.
2. **Use cross-database macros** for date, string, cast operations.
3. **Write dispatch shims** for JSON, regex, and array operations.
4. **Safe SQL everywhere:** CTEs, JOINs, GROUP BY, basic window functions (ROW_NUMBER, RANK, LAG/LEAD), CASE, subqueries.
5. **Avoid:** QUALIFY (Spark lacks it), platform-specific syntax, MERGE on ClickHouse.
