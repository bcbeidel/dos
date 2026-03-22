---
name: Local DuckDB Development Loop
description: How the DuckDB + dlt + dbt local stack works, what it enables, and the three divergence risks that undermine local-to-production confidence
type: context
related:
  - docs/research/2026-03-22-development-workflow.research.md
  - docs/context/ci-cd-pipeline-design.md
  - docs/context/secrets-environment-management.md
---

## Key Insight

DuckDB eliminates cloud dependencies for development — the entire ingestion-to-transformation loop runs in seconds locally. But three divergence risks (SQL dialect gaps, concurrency model, scale characteristics) mean local success does not guarantee production success. DuckDB is for rapid iteration and unit testing, not for proving production readiness.

## How the Local Stack Works

dlt loads data into a local DuckDB file. dbt-duckdb transforms it. No credentials, no cloud account, no Docker required. The recommended project structure separates ingestion (`dlt_pipeline/`), transformation (`dbt_project/` with staging, intermediate, marts), and optionally dashboards — orchestrated by a single shell script or Makefile.

Minimal dbt profile for local DuckDB:

```yaml
default:
  outputs:
    dev:
      type: duckdb
      path: data/project.duckdb
      threads: 4
  target: dev
```

dlt configuration for local DuckDB:

```python
dlt.destinations.duckdb("files/data.db")
# or pipeline-relative:
dlt.destinations.duckdb(":pipeline:")
```

dbt-duckdb supports table, view, incremental (append, delete+insert, merge, microbatch), snapshot, and external materializations. External sources can read directly from S3 Parquet/CSV/JSON via the `httpfs` extension. Parquet is the recommended dlt file format for DuckDB (faster, multithreaded loading with 20 threads by default).

## Three Divergence Risks

**1. SQL dialect gaps (HIGH).** DuckDB lacks Snowflake's VARIANT/OBJECT types and platform-specific functions (IFF, TRY_TO_*, PARSE_JSON). DuckDB uses STRUCT and explicit typing where Snowflake uses flexible VARIANT. It supports LATERAL joins and UNNEST (functional equivalents to LATERAL FLATTEN but with different syntax). Models using semi-structured data require syntax adaptation between environments. Code that compiles locally may produce silently different results in production due to type coercion differences.

**2. Concurrency model (MODERATE).** DuckDB is single-writer at the process level — one write process at a time, with MVCC and optimistic concurrency within a process. Production warehouses handle concurrent writes natively. Cross-process concurrency bugs are invisible in local dev.

**3. Scale characteristics (MODERATE).** DuckDB handles ~500MB comfortably. Beyond that, performance diverges significantly from cloud warehouses. Local dev gives false confidence about query performance at scale.

## DuckDB Gotchas

- Case-insensitive identifiers: loading `{"Column": 1, "column": 2}` creates collisions.
- Do not name datasets identically to database names — this confuses DuckDB's binder regarding catalog/schema references.
- `dbt clone` creates views on DuckDB instead of zero-copy clones (another local-vs-prod divergence).
- `dbt --defer` resolves ref() calls against a production manifest when referenced models don't exist locally — useful for testing one model without building all upstream.
- `dbt run --empty` (1.8+) validates SQL and schema with zero data, but if pointed at a production schema, it replaces tables with empty ones.

## Mitigation Strategy

Use DuckDB for rapid iteration and unit testing. Run integration tests against the production warehouse in CI. Write adapter-portable SQL where possible. Isolate platform-specific logic in macros with cross-database dispatch.
