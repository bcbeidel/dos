# Contract Enforcement in dbt

## Enabling Contract Enforcement

On mart models, enable contract enforcement in the model config:

```yaml
{{ config(
    materialized='table',
    contract={enforced: true}
) }}
```

When enabled, dbt performs a preflight check verifying the model's SQL produces the expected columns and types. If the check fails, the model is not built.

**Requirement:** Every column must be explicitly defined in the schema YAML when contract enforcement is enabled. Python models are not supported.

## Column Definition from Contract Schema

Map ODCS contract properties to dbt schema YAML:

| Contract (ODCS) | dbt Schema YAML |
|-----------------|-----------------|
| Property name | `name` |
| Property type | `data_type` |
| Property description | `description` |
| Required (not nullable) | `constraints: [{type: not_null}]` |
| Primary key | `constraints: [{type: primary_key}]` |
| Unique | `constraints: [{type: unique}]` |
| Foreign key | `constraints: [{type: foreign_key, to: ..., to_columns: [...]}]` |

## False Confidence Warning

**DuckDB enforces all constraints at build time.** A model that passes locally with DuckDB contract enforcement may silently allow invalid data in production.

| Platform | Constraint Enforcement |
|----------|----------------------|
| DuckDB | **Full** — all constraints enforced |
| PostgreSQL | Full — all constraints enforced |
| Snowflake | **Metadata-only** — most constraints defined but not enforced |
| Databricks | **Metadata-only** — most constraints defined but not enforced |
| Redshift | Partial — some constraints enforced |
| BigQuery | Partial — not_null enforced, others metadata |

**Rule:** For every constraint the production warehouse does not enforce, add an explicit dbt data test. A contract passing locally can silently allow invalid data in production.

```yaml
# Snowflake: primary_key constraint is metadata-only
# Add explicit tests to enforce it
columns:
  - name: order_id
    data_type: integer
    constraints:
      - type: primary_key    # Metadata only on Snowflake
    tests:
      - not_null              # Explicit enforcement
      - unique                # Explicit enforcement
```

## Three-Layer Enforcement Strategy

| Layer | When | What | Tool |
|-------|------|------|------|
| CI-time | PR validation | Breaking change detection | `dbt build --select state:modified+` |
| Build-time | Model materialization | Schema validation (preflight) | `contract: {enforced: true}` |
| Runtime | Post-deployment | Data quality + SLA checks | dbt tests, Soda, Great Expectations |

All three layers are needed. Teams implementing only one layer have blind spots.
