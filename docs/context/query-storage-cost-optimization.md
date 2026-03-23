---
name: Query & Storage Cost Optimization
description: "Cross-platform techniques for reducing compute and storage costs — partition pruning as the single biggest lever, incremental materialization for 80-95% savings, full-scan anti-patterns, storage tiering for up to 90% reduction, and the seven hidden costs that inflate bills by 60-80%"
type: context
related:
  - docs/research/2026-03-22-cost-optimization-finops.research.md
  - docs/context/platform-cost-optimization.md
  - docs/context/finops-governance.md
  - docs/context/incremental-loading-patterns.md
---

## Key Insight

Partition pruning is the single most impactful cost optimization across all platforms. A query filtering to one day of a year-partitioned table scans ~0.3% of the data. After pruning, incremental materialization is the second-largest lever, reducing per-run compute by 80-95% on large tables. Storage tiering is third, cutting cold data costs by up to 90%. Everything else is noise until these three are addressed.

## Partition Pruning

Each platform implements pruning differently but the principle is universal: partition on frequently filtered columns (typically date/timestamp) so queries skip irrelevant data.

- **Snowflake:** Automatic micro-partitioning with min/max metadata pruning. No explicit partition definition needed.
- **BigQuery:** Requires explicit partitioning on ingestion-time, date/timestamp, or integer-range columns. Clustering on high-cardinality filter columns adds further pruning.
- **Databricks:** Delta Lake data skipping with Z-ordering for multi-column optimization and dynamic file pruning for joins.
- **ClickHouse:** Primary key ordering determines data layout and pruning efficiency.

Critical BigQuery nuance: `LIMIT` clauses do not reduce scanned data on non-clustered tables. You pay for the full table scan regardless. Use the free table preview feature for data exploration.

## Incremental Materialization

dbt incremental models process only new or changed records, avoiding full-table reprocessing. For large tables with 5-10% change rates, this delivers 80-95% compute savings per run. Databricks extends this with Delta Change Data Feed, processing only changed rows.

The trade-off: incremental models add complexity (late-arriving data, schema changes, deduplication) and occasionally require full refreshes for drift correction.

## Full-Scan Anti-Patterns

Common patterns that trigger expensive full scans:
- `SELECT *` when only a few columns are needed
- Missing `WHERE` clauses on partitioned columns, bypassing pruning
- `LIMIT` on non-clustered BigQuery tables (scans full table regardless)
- Cross-joins and Cartesian products (often accidental)
- Exploration queries that should use free preview features instead

A single inefficient dashboard query at a Fortune 100 company cost $800/day.

## Materialized Views

Pre-computing expensive aggregations avoids redundant computation. BigQuery materialized views auto-refresh and support query rewriting. Snowflake materialized views consume credits for maintenance but save on repeated queries. The cost-benefit depends on query frequency — views that refresh more often than they are queried waste resources.

## Storage Optimization

**Compression:** Columnar formats (Parquet, ORC) reduce storage 60-80% vs raw CSV/JSON. ClickHouse achieves 5-10x compression with codec-per-column, making storage nearly negligible relative to compute.

**Tiering:** Cloud object storage tiers have dramatic price differences — hot (~$23/TB/month), infrequent access (~$12.50), cold/archive (~$1-4). Lifecycle policies should automatically move data unused for months to lower tiers. ByteDance achieved 73% cost reduction through intelligent tiering on a 12 EB data lake.

**Retention:** Storing data indefinitely "just in case" is expensive. One organization accumulated 5 PB of stale data costing $1.38M/year with no regulatory requirement. Effective retention needs: regulatory minimum analysis, access frequency auditing, automated lifecycle rules, and deletion governance.

**BigQuery specifics:** Long-term storage pricing (50% reduction after 90 days of no modifications) is automatic. Reducing time travel from 7 to 2 days and setting table expirations on temporary datasets prevents accumulation.

## The Seven Hidden Costs

Beyond compute and storage, teams routinely encounter: egress fees ($180K/year for cross-region replication), query inefficiency ($800/day from one bad dashboard), zombie pipelines (47 unused pipelines costing $28K/month), uncapped auto-scaling ($42K from an infinite loop in 8 hours), unnecessary cross-region replication ($138K/month), over-retention ($1.38M/year), and vendor lock-in preventing price negotiation. Companies routinely overspend by 60-80% from costs they do not know to monitor.

## Takeaway

Address optimizations in order of impact: partition pruning first, incremental materialization second, storage tiering third. Only then pursue materialized views, query rewriting, and fine-grained tuning. The biggest cost savings come from not scanning data in the first place.
