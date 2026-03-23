---
name: Pipeline Orchestration Comparison
description: "Airflow (task-centric), Dagster (asset-centric), and Prefect (flow-centric) represent three fundamentally different paradigms -- selection depends on team size, dbt depth, pricing model, cross-pipeline dependency needs, and local dev experience; all three have significant production trade-offs"
type: context
related:
  - docs/research/2026-03-22-pipeline-orchestration.research.md
  - docs/context/ci-cd-pipeline-design.md
  - docs/context/local-duckdb-development.md
---

## Key Insight

Airflow, Dagster, and Prefect are not three versions of the same tool at different maturity levels. They embody different philosophies: Airflow asks "what tasks should run and when?", Dagster asks "what data should exist and is it fresh?", Prefect asks "what Python code should execute and how?" The right choice depends on which question matches your team's mental model, not feature checklists.

## Paradigm Comparison

| Dimension | Airflow 3.x | Dagster | Prefect v3 |
|---|---|---|---|
| **Core model** | DAG/task-centric (+ @asset in 3.0) | Asset-centric (software-defined assets) | Flow/task-centric (decorators) |
| **Dynamic tasks** | Dynamic task mapping (degrades at 100k+) | Dynamic partitions + graph composition | Native Python loops/conditionals |
| **Backfills** | Scheduler-managed (3.0+) | Partition-aware, asset-level | No guaranteed catch-up for missed runs |
| **Data lineage** | Asset dependencies (event signals only) | Native column-level lineage | No native lineage |
| **Local dev** | Scheduler + DB + webserver required | Single command (`dagster dev`) | `prefect server start` or Cloud |
| **Partitioning** | Asset partitions (3.0+) | First-class partition definitions | No native partitioning |
| **Cross-pipeline deps** | Asset-based triggers between DAGs | Native asset graph across code locations | No native cross-flow mechanism |
| **SLA monitoring** | Task-level (limited, reworked in 3.1) | Asset freshness policies (warn/fail thresholds) | Proactive triggers + metric automations |

## dbt Integration Depth

**Dagster** provides the deepest integration. Each dbt model becomes a Dagster asset with automatic lineage. dbt sources link to upstream assets (Fivetran, Sling, custom). dbt tests become asset checks. Incremental models support partition-aware CLI variables.

**Airflow + Cosmos** is the most mature by adoption (21M+ monthly downloads). Cosmos converts dbt models into Airflow tasks with automatic dependency wiring from the dbt manifest. Supports multiple execution modes (standard, virtualenv, Docker, K8s, ECS). Caveat: large projects may trigger DagBag import timeouts.

**Prefect** is improving but least mature. v0.7.0+ maps dbt nodes as Prefect tasks, but task runs do not persist results or support caching. The architecture "significantly differs" between versions, signaling ongoing instability.

## Production Trade-offs

Every tool has structural pain that teams will encounter at scale, not edge cases.

**Airflow:** Infrastructure overhead (scheduler + database + webserver + workers). Airflow 3.0 has early-release instability with migration edge cases and plugin compatibility issues -- 3.1+ is the safer upgrade target. Assets are event signals, not software-defined assets with lineage and freshness. Dynamic task mapping hits scheduler timeouts at 100k+ mapped tasks.

**Dagster:** Credit-based pricing can surprise. At $0.03/credit, 8 ops materializing every 5 minutes generates ~$2,464/month on the Solo tier. Kubernetes pod startup times can reach 10 minutes at 100% CPU utilization. The multiprocess executor adds 5+ seconds per op overhead. IO manager abstractions obscure debugging. Rapid API changes reduce LLM code generation quality.

**Prefect:** No native data lineage or cross-flow dependencies. No native partitioning. dbt integration lacks result persistence and caching. No guaranteed catch-up for missed runs. Cross-pipeline coordination requires custom instrumentation.

## Decision Framework

| If you need... | Choose | Why |
|---|---|---|
| Existing Airflow investment, large ops team | Airflow | Ecosystem lock-in, 30M+ monthly downloads, largest community |
| Deep dbt integration, data product thinking | Dagster | First-class asset-dbt mapping, lineage, freshness policies |
| Rapid prototyping, Python-heavy ML workflows | Prefect | Minimal ceremony, runtime graph construction, low ops burden |
| Cross-pipeline SLA enforcement | Dagster | Asset freshness policies with warn/fail thresholds across code locations |
| High-frequency pipelines on a budget | Prefect | Per-user pricing, zero marginal execution cost |
| Multi-language future | Airflow | Task Execution Interface targets multi-language SDKs |

## Migration Paths

Dagster provides "Airlift" for gradual Airflow-to-Dagster migration -- most Dagster users were Airflow users. No official migration tools exist for Airflow-to-Prefect or Prefect-to-Dagster; both require rewrites. Prefect-to-Dagster also requires a conceptual shift from flow-centric to asset-centric thinking.

## Bottom Line

Default to Dagster if you are building a new data platform with dbt at the center and need cross-pipeline dependencies or SLA enforcement. Choose Airflow if you have existing investment or need the broadest ecosystem. Choose Prefect for lightweight Python orchestration where speed-to-production matters more than lineage or partitioning. All three have real production pain -- understand the trade-offs before committing.
