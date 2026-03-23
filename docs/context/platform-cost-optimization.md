---
name: Platform Cost Optimization
description: "Platform-specific compute billing mechanics and tuning levers for Databricks, Snowflake, BigQuery, and ClickHouse — Photon's 2x DBU breakeven, Snowflake's 60-second minimum billing trap, BigQuery on-demand vs Editions crossover, ClickHouse scale-to-zero advantage"
type: context
related:
  - docs/research/2026-03-22-cost-optimization-finops.research.md
  - docs/context/production-platform-comparison.md
  - docs/context/query-storage-cost-optimization.md
  - docs/context/finops-governance.md
---

## Key Insight

Each platform has a structural billing mechanic that, if ignored, inflates costs by 2-20x. Databricks Photon costs 2x more in DBUs and must deliver 2x speedup to break even. Snowflake's 60-second minimum per warehouse resume inflates short-query costs by up to 20x. BigQuery Editions' 50-slot allocation granularity and 60-second minimums require a 1.5x multiplier on theoretical costs. Knowing these mechanics matters more than generic "right-sizing" advice.

## Databricks

Databricks bills in DBUs, an abstracted compute unit priced by workload type. The most important lever: separate human from machine compute. Interactive (all-purpose) clusters cost 2-3x more per DBU than job clusters. Production pipelines should always run on job compute.

**Photon** increases DBU consumption by 2x-2.9x (AWS: 2.9x, Azure/GCP: 2.5x). It delivers 2x-4x speedup on complex joins and aggregations but provides zero benefit for simple DML, VACUUM/OPTIMIZE, single-machine tasks, and development clusters. Per-workload evaluation is required — blanket enablement wastes money.

**Serverless vs classic:** Serverless DBU rates run $0.70-0.95 vs $0.40-0.55 for classic. A two-hour ETL costs ~$60 serverless vs ~$16 on a tuned classic cluster. Serverless wins for short, infrequent workloads (under 30 minutes). Classic wins when cluster utilization stays high.

**Spot instances** offer 60-90% discounts. Use on-demand for driver nodes, spot for workers on fault-tolerant batch jobs. Not appropriate for streaming or SLA-bound pipelines.

## Snowflake

Credits scale linearly with warehouse size (X-Small = 1 credit/hour, 6X-Large = 512). Per-second billing applies, but each warehouse resume triggers a **60-second minimum charge**. A dashboard running 10 three-second queries with auto-suspend between each pays for 600 seconds instead of 30.

**Auto-suspend tuning:** BI dashboards need 10+ minutes (preserves SSD cache). ETL pipelines need 1 minute or immediate. Setting auto-suspend below the natural query gap causes continuous suspend/resume cycles, each hitting the 60-second floor.

**Sizing:** Doubling warehouse size doubles cost but does not always halve execution time — only queries with sufficient parallelism benefit. Start at XS/S and scale up only when consistently exceeding 60% resource utilization.

**Three cache layers** reduce credit consumption: result cache (free, 24-hour TTL), metadata cache (partition pruning), and warehouse cache (SSD, lost on suspend). Resource monitors enforce credit limits; `STATEMENT_TIMEOUT_IN_SECONDS` kills runaway queries.

## BigQuery

Two pricing models with different cost drivers. **On-demand** ($6.25/TiB scanned) is best for sporadic ad-hoc work. **Editions** (slot-based: Standard $0.04, Enterprise $0.06, Enterprise Plus $0.10 per slot-hour) saves 40-60% for sustained ETL above 50 TiB/day. Decision rule: if Editions cost exceeds 75% of on-demand equivalent, stay on on-demand.

Editions autoscales in 50-slot increments with 60-second minimums per allocation. Apply a **1.5x multiplier** to theoretical slot-hour costs for real-world estimates.

Standard Edition lacks materialized views, BI Engine, and BigQuery ML. Verify tier feature coverage before committing.

## ClickHouse

Compute bills per minute at $0.22-0.39/unit/hour. Basic tier can scale to zero — no compute charges during inactivity. Storage bills on compressed data ($25.30/TB/month); 5-10x compression means 1 TB raw data costs $2.53-5.06/month in storage.

ClickHouse Cloud introduced egress fees in January 2025. This is a vendor lock-in mechanism that increases the cost of migrating away.

## Takeaway

Vendor cost optimization guides recommend their own features and omit scenarios where competitors are cheaper. The most actionable cost insights come from independent practitioners and competitor analyses. Always benchmark actual workloads before committing to premium tiers (Photon, Editions, serverless).
