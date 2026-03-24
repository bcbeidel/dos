# Layering Strategy

Medallion (Bronze/Silver/Gold) is a useful organizing pattern, not a universal default. Practitioners have documented 37-90% cost reductions by departing from standard three-layer approaches.

## The Medallion Pattern

| Layer | Responsibility |
|---|---|
| **Bronze** | Raw source data as single source of truth. Store as string/VARIANT/binary to absorb schema changes. Never write directly to Silver from ingestion. |
| **Silver** | Validate, deduplicate, normalize. At least one non-aggregated, validated representation per record. |
| **Gold** | Business-domain aligned. Aggregations, joins, business-specific modeling. Multiple Gold layers can serve different business units. |

## When Medallion Works Well

- Multiple source systems feeding a shared analytical platform
- Data quality needs to improve incrementally across well-defined stages
- Team is using Databricks (first-class support via Delta Live Tables, Auto Loader)
- Auditing and reprocessing from raw data are important requirements

## When to Consider Alternatives

- **2-layer (skip Bronze or collapse Bronze/Silver)** -- Clean sources with stable schemas
- **OneBigTable / Direct Lake** -- Source data is already clean, minimal transformation needed. 60-70% cost reductions documented.
- **Domain-partitioned** -- Organize by business domain rather than quality tier. Each domain owns its own pipeline.
- **Late transformation** -- Keep data in neutral format, transform only at consumption time.

**Structural risks of medallion:** Consumer responsibility inversion, excessive copy costs per layer, Bronze fragility as a dumping ground, no operational data reuse from batch processing.

## Platform Differences

| Platform | Medallion Support | Key Mechanisms |
|---|---|---|
| **Databricks** | First-class | Delta Live Tables, Auto Loader, Unity Catalog |
| **Snowflake** | Pattern works, no explicit tooling | Snowpipe/Streaming for ingestion, Tasks/Streams for CDC, SQL ELT |
| **ClickHouse** | Supported via MergeTree family | MergeTree for Bronze, Incremental MVs for Silver, Refreshable MVs for Gold |

## Decision Rule

Start with the simplest architecture that meets your requirements. If you have clean, low-volume, single-domain data, a two-layer or single-layer approach is likely sufficient. Add layers only when you have concrete needs for raw data preservation, incremental quality improvement, or multi-consumer reuse at different quality tiers.
