---
name: Production Platform Comparison
description: Comparative overview of ClickHouse, BigQuery, Redshift, Athena, Databricks, and Snowflake — architecture, compute models, SQL/ACID support, incremental patterns, lock-in, and selection criteria
type: context
related:
  - docs/research/2026-03-22-production-platform-landscape.research.md
  - docs/context/platform-tooling-compatibility.md
---

## Key Insight

Platform architecture determines pipeline design more than any other factor. The six platforms occupy three architectural tiers — fully serverless, provisioned-with-serverless-options, and self-managed — and this choice cascades into compute scaling, idle cost, operational burden, and incremental loading patterns.

## Architecture Tiers

**Fully serverless (zero infrastructure):** BigQuery and Athena. No clusters to manage, no idle cost. BigQuery uses dynamic slot allocation; Athena charges $5/TB scanned. Both auto-scale per query. Tradeoff: no compute tuning knobs, unpredictable performance during peak hours (Athena especially).

**Provisioned with serverless options:** Snowflake, Databricks, Redshift. Snowflake virtual warehouses auto-suspend/resume in seconds with multi-cluster auto-scaling (Enterprise). Databricks serverless SQL warehouses cold-start in 2-6 seconds but have significant feature restrictions (no Spark UI, no custom configs, regional limits). Redshift Serverless bills RPU-hours with no idle cost; provisioned uses dedicated RA3 nodes.

**Self-managed or cloud-provisioned:** ClickHouse. Always-on compute (Cloud offers some auto-pause). Highest operational burden but purpose-built for sub-second OLAP on event/time-series data with extreme ingestion throughput (~1B rows/second).

## SQL and Transaction Support

ClickHouse is the outlier. No production-ready multi-statement transactions (experimental behind flag). No native MERGE statement. SQL dialect diverges from ANSI, requiring 6+ settings for compliance. JOINs, UNION, CAST, GROUP BY, and NULL handling all behave non-standardly by default.

BigQuery, Snowflake, and Redshift provide full ACID transactions and native MERGE INTO with high ANSI SQL compliance. Databricks provides full ACID via Delta Lake with Spark SQL (ANSI mode available). Athena supports MERGE INTO on Iceberg tables only (engine v3, Trino-based); non-Iceberg tables have no transaction support.

## Incremental Loading Patterns

Standard platforms (BigQuery, Snowflake, Redshift, Databricks) use MERGE INTO for upserts. ClickHouse replaces MERGE with engine selection: ReplacingMergeTree for eventual deduplication (background merge timing is nondeterministic; FINAL keyword forces dedup at query time with overhead), CollapsingMergeTree for sign-based row versioning. Athena requires Iceberg tables for merge operations.

For streaming: ClickHouse has sub-second query latency on fresh data. BigQuery Storage Write API delivers seconds-latency ingestion. Snowpipe Streaming achieves 1-3 second latency. Databricks Structured Streaming offers seconds-latency. Athena has no native streaming — batch on S3 only.

## Lock-In Gradient

From lowest to highest lock-in:

- **Athena**: Iceberg on S3. Data fully portable. Query engine is the only lock-in vector.
- **Databricks**: Delta Lake on cloud storage. UniForm enables Iceberg reads. Multi-cloud available.
- **Snowflake**: Proprietary micro-partitions plus Iceberg tables (GA, V3 preview). Credit-based pricing creates operational lock-in. Multi-cloud available.
- **Redshift**: AWS-only. Proprietary format. Distribution/sort key designs are platform-specific. Spectrum provides S3 escape hatch.
- **BigQuery**: GCP-only. Proprietary Capacitor format. Nested STRUCT/ARRAY usage creates schema lock-in.
- **ClickHouse**: Proprietary columnar parts. SQL dialect and engine-specific pipeline logic (ReplacingMergeTree, CollapsingMergeTree, FINAL) create tight coupling.

Iceberg is the migration insurance policy. All six platforms support Iceberg in some form, and lakehouse convergence means long-term platform choice is less permanent than it was two years ago.

## Selection Guide

| If you need... | Choose | Why |
|---|---|---|
| Sub-second OLAP on event/time-series data | ClickHouse | Purpose-built columnar engine, extreme ingestion speed |
| Zero-ops on GCP | BigQuery | Fully serverless, deep GCP integration |
| AWS warehouse with predictable BI | Redshift | Mature MPP, AWS integration, Spectrum for S3 |
| Ad-hoc S3 exploration, pay-per-query | Athena | Zero idle cost, Iceberg-native, cheapest for sporadic use |
| Unified analytics + ML, open formats | Databricks | Spark + Delta + Unity Catalog, multi-cloud |
| Multi-team BI, data sharing, low ops | Snowflake | Concurrency, ease of use, marketplace, multi-cloud |

## Multi-Platform Architectures

Multi-platform deployments are realistic: DuckDB for local dev (adapter swap in dbt), a primary warehouse for production, ClickHouse for real-time serving, Athena for ad-hoc exploration. Iceberg provides the shared data layer making these combinations work.

## Bottom Line

Choose architecture first (serverless vs. provisioned vs. self-managed), then filter by cloud provider, SQL/ACID requirements, and operational capacity. ClickHouse requires fundamentally different pipeline patterns. The remaining five platforms are converging on SQL + open formats + managed compute — differentiation is shifting from capability to operational model.
