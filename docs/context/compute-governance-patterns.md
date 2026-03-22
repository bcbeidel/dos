---
name: Compute Governance Patterns
description: "Cluster policies, resource monitors, and compute type selection as cost governance levers — Databricks job/all-purpose/serverless economics, Snowflake warehouse sizing and auto-suspend traps, ClickHouse Keeper and scaling topology"
type: context
related:
  - docs/research/2026-03-22-data-platform-engineering.research.md
  - docs/context/platform-cost-optimization.md
  - docs/context/terraform-data-platform-iac.md
  - docs/context/finops-governance.md
---

## Key Insight

Cost controls must be defined at the platform level through policies and monitors, not at the individual workload level. Users who can create unrestricted clusters or warehouses will create unrestricted clusters or warehouses. Cluster policies (Databricks) and resource monitors (Snowflake) shift cost governance from manual oversight to code-enforced policy, making it auditable, version-controlled, and consistently enforced across environments via Terraform.

## Databricks: Three Compute Tiers

The cost difference between cluster types is the single largest optimization lever:

- **Job clusters** ($0.15/DBU): Start for a specific job, execute, terminate. 50-75% cheaper than all-purpose. 5-12 minute startup latency. Use for all scheduled production workloads.
- **All-purpose clusters** ($0.40-$0.55/DBU): Stay running for interactive work. Prone to idle time. Use only for collaborative development with aggressive auto-termination (30-60 min).
- **Serverless** ($0.70-$0.95/DBU): 15-30 second startup. Break-even vs classic at ~30 minutes execution time. Optimal for interactive SQL, short notebooks, bursty workloads. Classic wins for jobs exceeding 45 minutes, streaming, and custom library requirements.

**Cluster pools** reduce classic startup from 5-12 minutes to under 2 minutes by maintaining idle ready-to-use instances. No DBU charges for idle pool instances (cloud VM charges still apply).

## Databricks Cluster Policies

Policies enforce cost boundaries through JSON attribute definitions with six constraint types: fixed (locked value), range (numeric bounds), allowlist, blocklist, forbidden, and unlimited. A practical cost-control policy:

- Fix auto-termination to 30 minutes (hidden from users)
- Cap autoscaling max workers
- Set `dbus_per_hour` maximum (hard ceiling on per-cluster spend)
- Require spot instances for workers

Policies are managed via Terraform `databricks_cluster_policy` resources and enforced through CI/CD for cross-workspace consistency.

## Snowflake: Warehouse Sizing and Monitors

Larger warehouses are not necessarily faster for simple queries -- they add nodes that sit idle if the query cannot be parallelized. Start with the smallest size meeting latency requirements, scale up based on measured performance.

**Auto-suspend settings:** ETL warehouses at 60 seconds. Interactive/BI warehouses at 300-600 seconds (balances cache retention with cost). Never disable auto-suspend unless the warehouse runs continuous workloads. The 60-second minimum billing floor creates a cost trap: short queries arriving every 90 seconds trigger full 60-second resume charges each time.

**Multi-cluster warehouses** handle concurrency, not query speed. A single complex query runs at the same speed regardless of cluster count. Start with max 2-3 clusters, Standard scaling policy for performance, Economy policy for cost.

**Resource monitors** track credit consumption with threshold-based actions: one suspend, one suspend-immediate, up to five notify. Suspension is not instantaneous -- set thresholds below 100% for buffer. Monitors cover warehouse compute only, not serverless features, Snowpark, or AI services.

## ClickHouse: Scaling and Keeper

Self-hosted scaling follows a shard-and-replicate model. Standard production topology: 2 shards, 2 replicas each, 3-node ClickHouse Keeper cluster. Nodes need 2-3x free space for merge operations.

**ClickHouse Keeper** replaces ZooKeeper: C++ (no GC pauses), 4GB RAM sufficient per node (vs 8GB+ for ZooKeeper), no zxid overflow requiring restart every ~2B transactions, drop-in compatible protocol. Production-ready since April 2022.

**ClickHouse Cloud SharedMergeTree** eliminates manual shard/replica management using shared object storage. Supports hundreds of replicas per table and dynamic scaling without sharding. Not available for self-hosted.

## Takeaway

Layer all three Databricks compute types by workload. Enforce cluster policies and resource monitors through Terraform. Right-size Snowflake warehouses empirically, not by default. Understand that auto-scaling optimizes for performance, not cost -- upper bounds are mandatory.
