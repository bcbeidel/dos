---
name: Medallion Architecture
description: When to use Bronze/Silver/Gold layering and when simpler alternatives are better; key criticisms and platform differences
type: context
related:
  - docs/research/2026-03-21-pipeline-design-architecture.research.md
---

## Key Takeaway

Medallion (Bronze/Silver/Gold) is a useful organizing pattern for data pipelines, not a universal default. Databricks calls it "a recommended best practice but not a requirement." Practitioners have documented 37-90% cost reductions by departing from standard three-layer approaches. Evaluate whether your workload actually needs three layers before committing to the complexity.

## The Pattern

Bronze preserves raw source data as the single source of truth. Store fields as string, VARIANT, or binary to absorb upstream schema changes. Never write directly to Silver from ingestion -- corrupt records and schema changes in sources will cause failures.

Silver validates, deduplicates, and normalizes. It should contain at least one non-aggregated, validated representation of each record.

Gold aligns with business domains. Multiple Gold layers can serve different business units (HR, finance, IT). This is where aggregations, joins, and business-specific modeling happen.

## When Medallion Works Well

- Multiple source systems feeding a shared analytical platform
- Data quality needs to improve incrementally across well-defined stages
- Team is using Databricks (first-class support via Delta Live Tables, Auto Loader)
- Auditing and reprocessing from raw data are important requirements

## When to Consider Alternatives

**Five structural flaws** identified by expert practitioners:

1. **Consumer responsibility inversion** -- consumers must rebuild data into usable form without owning the source models
2. **Excessive copy costs** -- each layer incurs loading, network transfers, disk writes, and compute
3. **Data quality restoration difficulty** -- Bronze creators lack domain expertise, leading to inconsistent standardization
4. **Bronze fragility** -- becomes a "dumping ground" vulnerable to upstream schema changes
5. **No operational data reuse** -- batch processing is too slow for operational use cases

**Deeper criticisms:** Quality and purpose are independent variables that medallion conflates. A refined dataset may be unsuitable for specific use cases, while raw data might serve data scientists better. The architecture assumes one engine (Spark) and one format (Parquet/Delta) handles all workloads.

## Alternatives

- **2-layer Mini-Medallion** -- skip Bronze or collapse Bronze/Silver. Works for clean sources with stable schemas.
- **OneBigTable / Direct Lake** -- eliminate layers entirely when source data is already clean and transformation is minimal. Documented 60-70% cost reductions.
- **Domain-partitioned** -- organize by business domain rather than quality tier. Each domain owns its own transformation pipeline.
- **Late transformation** -- keep data in neutral format, transform only at consumption time.

## Platform Differences

- **Databricks:** Delta Live Tables, Auto Loader, Structured Streaming. Medallion is first-class. Unity Catalog for governance across SQL, Python, notebooks.
- **Snowflake:** Snowpipe/Snowpipe Streaming for ingestion, Tasks/Streams for CDC, SQL ELT for transformation. No explicit medallion tooling but the pattern works.
- **ClickHouse:** MergeTree for Bronze (fast inserts), Incremental Materialized Views for Bronze-to-Silver on insert, Refreshable Materialized Views for Gold aggregations. ReplacingMergeTree for CDC is eventually consistent -- requires FINAL operator at query time, which adds overhead.

## Decision Rule

Start with the simplest architecture that meets your requirements. If you have clean, low-volume, single-domain data, a two-layer or single-layer approach is likely sufficient. Add layers only when you have concrete needs for raw data preservation, incremental quality improvement, or multi-consumer reuse at different quality tiers.
