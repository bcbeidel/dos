---
name: "Data Catalog Selection"
description: "Open-source catalogs (DataHub, OpenMetadata) match commercial feature sets but impose significant operational burden; platform-native catalogs (Unity Catalog, Horizon) complement but do not replace standalone catalogs in multi-platform stacks; metadata quality requires product-level operational commitment or catalogs decay within months"
type: context
related:
  - docs/context/data-lineage-implementation.md
  - docs/context/iceberg-catalog-interoperability.md
  - docs/research/2026-03-22-data-catalog-lineage.research.md
---

## Key Insight

The catalog decision is engineering capacity vs. licensing budget, not features vs. no-features. Open-source catalogs (DataHub, OpenMetadata) match commercial tools on core cataloging, lineage, and search. The difference is operational burden: DataHub requires four infrastructure components and 4-8 weeks to deploy; OpenMetadata needs two components and 2-4 weeks. Commercial tools like Atlan deploy in 4-6 weeks with zero infrastructure management. Platform-native catalogs (Unity Catalog, Snowflake Horizon) govern data within their ecosystems but do not replace standalone catalogs for multi-platform stacks.

## Open-Source Catalogs

**DataHub** uses a distributed, event-driven architecture: relational database, Elasticsearch, graph database (JanusGraph/Neo4j), and Kafka. Every metadata change becomes an immutable Kafka event enabling near-real-time enrichment and indexing. This architecture excels at scale and data mesh implementations but requires Kubernetes expertise for production. Its SQL parser (sqlglot-based) generates column-level lineage with 97-99% accuracy across 20+ SQL dialects.

- Strengths: Real-time metadata streaming, schema-aware lineage, data mesh governance support.
- Weaknesses: Complex four-component deployment, high resource requirements, steep learning curve.

**OpenMetadata** uses a simpler stack: MySQL/PostgreSQL plus Elasticsearch, no Kafka or graph database. It provides 84+ connectors, built-in data quality/profiling, and a visual lineage editor. Version 1.8 introduced data contracts; version 1.12 added semantic search with vector embeddings.

- Strengths: Simplest deployment among OSS catalogs, comprehensive out-of-box features, modern UI.
- Weaknesses: No event-driven architecture, stability concerns under high concurrency.

## Platform-Native Catalogs

**Unity Catalog** implements the Iceberg REST Catalog API for multi-engine access and supports Catalog Federation (connecting to AWS Glue, Hive Metastore, Snowflake Horizon). Best within the Databricks ecosystem; the OSS version lacks full governance features of managed Databricks.

**Snowflake Horizon** provides metadata search, classification, lineage, access controls, and quality monitoring natively within Snowflake. Catalog-Linked Databases extend governance to external Iceberg objects. Governance remains Snowflake-centric.

Both complement but do not replace standalone catalogs in heterogeneous environments.

## Metadata Quality and Decay

Manual-entry catalogs become untrusted within the first year. Automated metadata harvesting is necessary but not sufficient. Three automation layers prevent staleness:

1. **Technical metadata harvesting** -- incremental schema scans detect new columns, type changes, dropped tables.
2. **Usage-based curation** -- query log analysis identifies popular assets, frequent users, and natural owners.
3. **Quality signal integration** -- test results, freshness metrics, and anomaly detections surfaced directly in catalog entries.

Distributed ownership (domain teams own their metadata) is the only model that scales. Centralized stewardship cannot keep pace.

## Health Metrics

- Search click-through rate >35% (below indicates poor metadata quality)
- Time-to-first-answer <5 minutes
- >80% domain ownership coverage
- >60% of top assets have at least one quality check

## Selection Guidance

| Scenario | Recommended Catalog |
|----------|-------------------|
| Cloud-native, moderate engineering capacity | OpenMetadata |
| Data mesh, real-time metadata, AI-forward | DataHub |
| Databricks-centric stack | Unity Catalog |
| Snowflake-centric stack | Snowflake Horizon |
| Modern stack, fastest deployment, budget available | Atlan |

## Takeaway

Treat the catalog as a product with SLAs, user feedback loops, and continuous improvement cycles. The most common failure modes are attempting to catalog everything simultaneously ("boil the ocean") and treating the catalog as a one-time documentation project ("static wiki"). Start with 3-5 high-impact domains and expand incrementally. Quality-signal-integrated catalogs reduce incident MTTR by 30-50%, providing concrete ROI justification.
