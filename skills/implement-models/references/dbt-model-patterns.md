# dbt Model Patterns

## Layer-by-Layer Generation

### Staging (stg_)

- **Purpose:** Rename, cast, basic cleaning. Light transformation only.
- **Materialization:** `view` or `ephemeral`
- **Rule:** One model per source table. No joins, no business logic.
- **Naming:** `stg_<source>__<table>` (double underscore separating source from table)
- **Source reference:** `{{ source('<source_name>', '<table_name>') }}`

### Intermediate (int_)

- **Purpose:** Business logic joins, enrichments, deduplication, pivots.
- **Materialization:** `table` or `incremental`
- **Naming:** `int_<entity>__<verb>` (e.g., `int_orders__pivoted`)
- **Use when:** Transformation is reused by multiple marts, or logic is complex enough to warrant isolation.

### Marts (fct_, dim_, or wide table)

- **Purpose:** Consumer-facing models. Final output matching the modeling recommendation.
- **Materialization:** `table` or `incremental`. Contract enforcement enabled.
- **Naming by modeling approach:**

| Approach | Naming Pattern | Key Characteristics |
|----------|---------------|---------------------|
| Kimball star schema | `fct_<process>`, `dim_<entity>` | Fact tables at atomic grain, denormalized dimensions, surrogate keys |
| OBT / wide table | `<entity>_wide` or `obt_<entity>` | Pre-joined, denormalized, best as serving layer on top of Kimball core |
| Entity-centric | `<entity>` | Domain-organized, one model per business entity |

## Modeling Approach Patterns

### Kimball Star Schema (default)

Fact tables: one row per business event at atomic grain. Types: transaction, periodic snapshot, accumulating snapshot, factless.

Dimension tables: wide, denormalized. Include surrogate keys, role-playing dimensions, degenerate dimensions (stored on fact), junk dimensions (low-cardinality flags combined).

SCD handling: Type 1 (overwrite), Type 2 (add row with effective dating), or daily snapshot approach.

### OBT / Wide Table

Best as downstream mart layer on Kimball core (Brooklyn Data hybrid pattern). Consolidates fact + dimensions into single wide table.

Works well with: BigQuery, Databricks with Liquid Clustering, BI tools without relationship support.

Avoid as standalone architecture: dimension change cascades, SCD awkwardness, governance drift, PII blast radius, 6x storage overhead.

### Layering Strategy

| Scenario | Recommended Layers |
|----------|-------------------|
| Multiple consumers, different quality tiers, raw data preservation needed | Medallion: Bronze → Silver → Gold |
| Single consumer, straightforward transformations | Simpler: staging → marts |
| Clean sources, minimal transformation | Two-layer or single-layer |

Start with the simplest architecture. Add layers only when concrete needs emerge.

## Incremental Model Configuration

```yaml
{{ config(
    materialized='incremental',
    unique_key='id',
    incremental_strategy='merge',  # or delete+insert, append, microbatch
    on_schema_change='append_new_columns'
) }}
```

Key considerations:
- In CI, incremental models run full-refresh (clean schema) — different SQL path from production
- Use `dbt clone` to seed CI schema for accurate incremental testing
- Partition pruning is critical for merge strategy on large tables
