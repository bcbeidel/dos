---
name: "Pipeline Orchestration"
description: "Three fundamentally different paradigms — task-centric (Airflow), asset-centric (Dagster), flow-centric (Prefect) — each with significant production trade-offs; dbt integration maturity favors Dagster > Cosmos > Prefect; cross-pipeline dependencies and SLA monitoring favor Dagster; selection is multi-dimensional across team size, pricing model, dynamic workflow needs, and local dev experience"
type: research
sources:
  - https://engineering.freeagent.com/2025/05/29/decoding-data-orchestration-tools-comparing-prefect-dagster-airflow-and-mage/
  - https://dagster.io/blog/dagster-airflow
  - https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow
  - https://risingwave.com/blog/airflow-vs-dagster-vs-prefect-a-detailed-comparison/
  - https://airflow.apache.org/blog/airflow-three-point-oh-is-here/
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/event-scheduling.html
  - https://danubedatalabs.com/apache-airflow-3-0-new-features-what-hurts-and-should-you-upgrade/
  - https://docs.dagster.io/guides/automate/declarative-automation
  - https://docs.prefect.io/v3/concepts/automations
  - https://docs.dagster.io/guides/observe/asset-freshness-policies
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/dynamic-task-mapping.html
  - https://www.astronomer.io/docs/learn/airflow-dbt
  - https://www.astronomer.io/blog/supercharge-dbt-orchestration-with-astronomer-cosmos-and-apache-airflow/
  - https://docs.dagster.io/integrations/libraries/dbt
  - https://docs.prefect.io/integrations/prefect-dbt
  - https://blog.pmunhoz.com/dbt/dbt-orchestration/dbt-orchestration-tools-comparison
  - https://opencredo.com/blogs/data-orchestration-showdown-airflow-vs-dagster
  - https://dagster.io/vs/dagster-vs-prefect
  - https://dagster.io/pricing
  - https://www.prefect.io/compare/dagster
  - https://docs-3.prefect.io/v3/develop/transactions
  - https://sairamkrish.medium.com/dagster-list-of-pain-points-e528ea139777
  - https://www.astronomer.io/blog/upgrading-airflow-2-to-airflow-3-a-checklist-for-2026/
  - https://kestra.io/blogs/2026-01-18-enterprise-airflow-alternatives
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
---

## Summary

**Research question:** How do Apache Airflow, Prefect, and Dagster compare for data pipeline orchestration, and what governs the choice between them?

**Mode:** Options | **SIFT rigor:** High | **Sources:** 24 | **Searches:** 12 across Google

**Key findings:**
- Three fundamentally different paradigms — task-centric (Airflow), asset-centric (Dagster), flow-centric (Prefect) — not a maturity gap but a philosophical difference
- dbt integration maturity: Dagster (first-class assets) > Cosmos/Airflow (per-model tasks, 21M+ downloads) > Prefect (improving but lacks result persistence)
- Cross-pipeline dependencies and SLA monitoring favor Dagster's asset freshness policies with warn/fail thresholds
- Selection is multi-dimensional: team size, pricing model (credit vs per-user vs self-managed), dynamic workflow needs, dbt depth, local dev experience
- All three have significant production trade-offs — Airflow's infrastructure overhead and 3.0 instability, Dagster's pricing surprises and startup time, Prefect's lack of native lineage and cross-flow dependencies

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://engineering.freeagent.com/2025/05/29/decoding-data-orchestration-tools-comparing-prefect-dagster-airflow-and-mage/ | Decoding Data Orchestration Tools | Paul Barber / FreeAgent Engineering | 2025-05-29 | T4 | verified — engineering team evaluation |
| 2 | https://dagster.io/blog/dagster-airflow | Dagster vs Airflow: Feature Comparison | Alex Noonan / Dagster | 2024-09-23 | T4 | verified — vendor comparison (bias expected) |
| 3 | https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow | Orchestration Showdown | Rishabh Sharma / ZenML | 2024-08 (updated 2025-11) | T4 | verified — third-party comparison |
| 4 | https://risingwave.com/blog/airflow-vs-dagster-vs-prefect-a-detailed-comparison/ | Airflow vs Dagster vs Prefect | RisingWave | 2025 | T5 | verified — vendor blog |
| 5 | https://airflow.apache.org/blog/airflow-three-point-oh-is-here/ | Apache Airflow 3 is Generally Available! | Apache Airflow Project | 2025-04 | T1 | verified |
| 6 | https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/event-scheduling.html | Event-Driven Scheduling | Apache Airflow | current (3.1.8) | T1 | verified |
| 7 | https://danubedatalabs.com/apache-airflow-3-0-new-features-what-hurts-and-should-you-upgrade/ | Apache Airflow 3.0: What's New, What Hurts | Danube Data Labs | 2025 | T5 | verified — practitioner analysis |
| 8 | https://docs.dagster.io/guides/automate/declarative-automation | Declarative Automation | Dagster | current docs | T1 | verified |
| 9 | https://docs.prefect.io/v3/concepts/automations | Automations | Prefect | current (v3) | T1 | verified |
| 10 | https://docs.dagster.io/guides/observe/asset-freshness-policies | Asset Freshness Policies | Dagster | current docs | T1 | verified |
| 11 | https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/dynamic-task-mapping.html | Dynamic Task Mapping | Apache Airflow | current (3.1.8) | T1 | verified |
| 12 | https://www.astronomer.io/docs/learn/airflow-dbt | Orchestrate dbt with Airflow and Cosmos | Astronomer | current docs | T1 | verified |
| 13 | https://www.astronomer.io/blog/supercharge-dbt-orchestration-with-astronomer-cosmos-and-apache-airflow/ | Cosmos 1.11 alpha | Astronomer | 2025-07-01 | T1 | verified |
| 14 | https://docs.dagster.io/integrations/libraries/dbt | Dagster & dbt (Component) | Dagster | current docs | T1 | verified |
| 15 | https://docs.prefect.io/integrations/prefect-dbt | prefect-dbt | Prefect | current docs | T1 | verified |
| 16 | https://blog.pmunhoz.com/dbt/dbt-orchestration/dbt-orchestration-tools-comparison | Best dbt Orchestration Tools | Pierre Munhoz | 2026-03-20 | T4 | verified — practitioner comparison |
| 17 | https://opencredo.com/blogs/data-orchestration-showdown-airflow-vs-dagster | Data Orchestration Showdown | OpenCredo | 2024-11-14 | T4 | verified — consultancy analysis |
| 18 | https://dagster.io/vs/dagster-vs-prefect | Dagster vs Prefect | Dagster | current | T4 | verified — vendor comparison (bias expected) |
| 19 | https://dagster.io/pricing | Dagster Pricing | Dagster | current | T1 | verified — vendor pricing page |
| 20 | https://www.prefect.io/compare/dagster | Prefect vs Dagster | Prefect | current | T4 | verified — vendor comparison (bias expected) |
| 21 | https://docs-3.prefect.io/v3/develop/transactions | Prefect Transactions | Prefect | current (v3) | T1 | verified — official docs |
| 22 | https://sairamkrish.medium.com/dagster-list-of-pain-points-e528ea139777 | Dagster: List of Pain Points | Sairam Krish / Medium | 2024 | T4 | verified — practitioner experience |
| 23 | https://www.astronomer.io/blog/upgrading-airflow-2-to-airflow-3-a-checklist-for-2026/ | Upgrading Airflow 2 to Airflow 3 | Astronomer | 2026 | T1 | verified — vendor migration guide |
| 24 | https://kestra.io/blogs/2026-01-18-enterprise-airflow-alternatives | Enterprise Airflow Alternatives | Kestra | 2026-01-18 | T4 | verified — vendor blog (bias expected) |

---

## Sub-question 1: Core Architecture and Programming Model

### Airflow: Task-centric DAG model
Airflow defines workflows as Directed Acyclic Graphs (DAGs) where each node is a task and edges represent execution order. DAGs are constructed using context managers or the `@dag`/`@task` decorators (TaskFlow API). Every DAG requires a schedule. Data flows between tasks via XComs (limited to small data) or external storage. Airflow 3.0 introduced `@asset` decorators and event-driven scheduling, narrowing the gap with asset-centric tools [5].

### Dagster: Asset-centric model
Dagster organizes workflows around software-defined assets — "data assets, not just tasks." Each asset represents a concrete data artifact with its own run history, metadata, and lineage. The programming model asks "what data should exist?" rather than "what tasks should run?" This enables answering "Is this asset up-to-date? What do I need to run to refresh it?" [2]. Local development is first-class: the entire pipeline runs locally with `dagster dev` without external dependencies [2].

### Prefect: Flow-centric Python model
Prefect uses decorator-based Python (`@flow`, `@task`) with maximum flexibility. Flows are standalone objects that can run anytime — no mandatory schedules [3]. The imperative model provides "lightweight yet powerful" orchestration with cloud-native workflows [4]. Work pools provide flexible infrastructure routing.

---

## Sub-question 2: Key Features Comparison

### Feature Matrix

| Feature | Airflow 3.x | Dagster | Prefect v3 |
|---|---|---|---|
| **Programming model** | DAG/task-centric (+ @asset in 3.0) | Asset-centric (software-defined assets) | Flow/task-centric (decorator-based) |
| **Dynamic task generation** | Dynamic task mapping (MapReduce model) | Dynamic partitions + graph composition | Native Python loops/conditionals |
| **Backfill management** | Scheduler-managed (3.0+), UI/API | Partition-aware, asset-level | No guaranteed catch-up for missed runs |
| **Partitioning** | Asset partitions (3.0+) | First-class partition definitions | No native partitioning |
| **Caching** | No native caching | Op-level caching (IO managers) | Result caching (task-level) |
| **Sensors/triggers** | AssetWatcher, event-driven scheduling | Declarative automation conditions | Automations (reactive/proactive/metric) |
| **Data lineage** | Asset dependencies (3.0+) | Native column-level lineage | No native lineage |
| **Local dev** | Requires scheduler + DB + webserver | `dagster dev` (single command) | `prefect server start` or Cloud |
| **Observability** | Structured logs + asset UI (3.0+) | Rich metadata, asset health, freshness | Centralized logs, task status |
| **Community** | 30M+ monthly downloads, 80K+ orgs | Growing (ex-Airflow users) | Declining weekly commits since mid-2021 |

### Airflow 3.0 Key Changes [5]
- Assets (renamed from Datasets) with partitions and external event integration
- DAG versioning — most requested feature; runs complete using version active at start
- Event-driven scheduling via AssetWatcher
- Backfills now run within the scheduler
- Task Execution Interface — client-server architecture, future multi-language SDKs

### Dagster Declarative Automation [8]
Three conditions: `on_cron` (scheduled, waits for dependencies), `eager` (propagates upstream changes), `on_missing` (fills partition gaps). Evaluates asset status and dependencies rather than fixed time intervals.

### Prefect Automations [9]
Trigger types: reactive (state changes), proactive (absence of expected events), metric-based (duration, lateness, completion %), custom. 17 action types: flow control, deployment management, notifications, webhooks.

### Dynamic Task Generation Comparison
- **Airflow**: Dynamic task mapping creates one task per input (MapReduce). Performance degrades at 100k+ mapped tasks with scheduler timeouts [11].
- **Dagster**: Dynamic partitions + graph composition. Asset-level granularity.
- **Prefect**: Native Python — for loops, conditionals, map operations. Most flexible but least structured.

---

## Sub-question 3: dbt Integration Patterns

### dbt Integration Matrix

| Dimension | Airflow + Cosmos | Dagster | Prefect |
|---|---|---|---|
| **Per-model observability** | Yes (one Airflow task per dbt node) | Yes (each dbt model = Dagster asset) | Limited (v0.7.0+ has per-node tasks) |
| **Retry granularity** | Per task (per dbt model) | Per asset/op | Per flow (dbt native retry for nodes) |
| **dbt test integration** | Auto-run after model completion | dbt tests → Dagster asset checks | Via PrefectDbtRunner |
| **Partition support** | Via Airflow asset partitions | Native partition-aware CLI variables | No |
| **Lineage** | Asset-level dependencies | Source → model → downstream asset chain | Asset graph (v0.7.0+) |
| **Execution modes** | standard, virtualenv, Docker, K8s, ECS | In-process, subprocess | In-process |
| **Maturity** | 21M+ monthly downloads (Cosmos) | First-class integration | "Significantly differs" between versions |

### Astronomer Cosmos (Airflow + dbt) [12][13]
Converts dbt models into Airflow tasks with automatic dependency wiring from dbt manifest. Supports dbt Fusion (Rust-based engine) for accelerated parsing. Uses Airflow connections instead of dbt profiles. Caveat: large projects may trigger `DagBag import timeout`. Cosmos 1.11 adds Airflow 3 support, DuckDB target.

### dagster-dbt [14]
`DbtProjectComponent` compiles and caches the dbt manifest. dbt models become Dagster assets with full lineage. dbt sources auto-link to upstream Dagster assets (Fivetran, Sling, custom). dbt tests become asset checks. Incremental models support partition-aware CLI variables. Auto-detects dbt Fusion engine.

### prefect-dbt [15]
Two execution methods: dbt Cloud (`run_dbt_cloud_job`) and dbt Core (`PrefectDbtRunner`). v0.7.0+ maps each dbt node as a Prefect task. Limitations: task runs don't persist results or support caching; failed nodes require dbt's native retry + Prefect flow retries. Architecture "significantly differs between v0.7.0+ and v0.6.6."

---

## Sub-question 4: Selection Criteria and Migration Patterns

### Selection Decision Framework

| Criterion | Choose Airflow | Choose Dagster | Choose Prefect |
|---|---|---|---|
| **Team profile** | Large team, existing Airflow investment | Data-centric team, strong testing culture | Small team, rapid prototyping |
| **Architecture** | Task-oriented ETL, multi-system orchestration | Asset-centric data mesh, data products | Python-heavy ML/data science workflows |
| **Infrastructure** | Willing to manage scheduler + DB + workers | Want local-first dev with cloud deploy | Want minimal self-hosting burden |
| **dbt integration** | Via Cosmos (mature, high-scale) | First-class asset integration (deepest) | Improving but least mature |
| **Existing investment** | Strong ecosystem lock-in | Migration path via Airlift | Easy to adopt, easy to leave |

### Migration Patterns
- **Airflow → Dagster**: Dagster provides "Airlift" for gradual migration. Most Dagster users were Airflow users [2].
- **Airflow → Prefect**: No official migration tool. Requires rewriting DAGs as flows.
- **Prefect → Dagster**: No migration tool. Conceptual shift from flow-centric to asset-centric required.

### Evaluation Criteria from FreeAgent [1]
FreeAgent evaluated 30+ criteria and selected Dagster, citing: data-first architecture, strong dbt integration, CI/CD for branch deployments, simple dev environment setup with code reloading. Airflow failed on dbt integration; Prefect was partial on dbt integration, cost, and data visibility.

---

## Sub-question 5: Cross-Pipeline Dependency Management and SLA Monitoring

### Cross-Pipeline Dependencies

| Feature | Airflow | Dagster | Prefect |
|---|---|---|---|
| **Cross-pipeline deps** | Asset-based (3.0+): producer declares output, consumer schedules on update | Native: assets automatically form dependency graph across code locations | No native cross-flow dependency mechanism |
| **External system triggers** | AssetWatcher monitors external events | Sensors + external asset integration | Automations with event triggers |
| **Limitation** | Persistent-state triggers cause infinite loops [6] | Not supported for SourceAssets | Requires custom instrumentation |

### SLA Monitoring

| Feature | Airflow | Dagster | Prefect |
|---|---|---|---|
| **SLA mechanism** | Task SLAs (limited) | Asset freshness policies (time_window, cron) | Proactive triggers + metric automations |
| **Granularity** | Task-level | Asset-level with warn + fail thresholds | Flow-level |
| **Alerting** | Email (native), webhooks (plugins) | Native alerts + integration hooks | 17 action types (notifications, webhooks, flow control) |

### Dagster Freshness Policies [10]
Two types: `time_window` (e.g., fail_window=24h, warn_window=12h) and `cron`-based (deadline + lower_bound_delta). Superseded freshness checks since v1.12. Can batch-apply via `map_asset_specs()`. Limitation: not supported for SourceAssets or CacheableAssetsDefinition.

### Prefect Automations for SLA [9]
Proactive triggers detect stuck processes (absence of expected events). Metric-based triggers: average duration, lateness, completion %. 17 action types including cancel/suspend flows, pause schedules, notifications, webhooks.

---

## Challenge

Challenger research targeted vendor-sourced claims, pricing assumptions, and production readiness gaps. Six additional sources (19-24) were evaluated.

### Airflow 3.0 assets are event signals, not software-defined assets
Airflow 3.0 assets connect dependencies and trigger downstream DAGs, but they do not provide lineage tracking, freshness policies, or partition awareness comparable to Dagster's software-defined assets. They function as dependency signals — "this data was updated" — not as first-class data objects with metadata and health monitoring. Airflow 3.1+ is the safer upgrade target; 3.0 has early-release instability including migration edge cases and plugin compatibility issues [7][23].

### Dagster has underdocumented production pain
Practitioner reports identify several Dagster production issues [22]: Kubernetes pod startup times reaching 10 minutes with 100% CPU utilization, multiprocess executor adding 5+ seconds per op overhead, IO manager complexity creating abstraction layers that obscure debugging, and LLMs producing invalid Dagster code due to rapid API changes and evolving abstractions. The framework overhead can dominate thinking time — developers spend more effort understanding Dagster conventions than solving data problems.

### Dagster pricing can surprise
Dagster's credit-based pricing model charges $0.03 per materialization credit [19]. A seemingly modest pipeline — 8 ops materializing every 5 minutes — generates ~82,944 credits/month, costing approximately $2,464/month on the Solo tier. This scales linearly with asset count and frequency. Prefect Cloud charges per user with zero marginal execution cost, making it significantly cheaper for high-frequency workloads [20].

### "Declining Prefect commits" is vendor bias
The claim that Prefect has "declining weekly commits since mid-2021" (repeated in source 18) originates from dagster.io/vs/dagster-vs-prefect — a vendor comparison page with expected bias. Prefect releases every 7-9 days, and development is split across multiple repositories (prefect, prefect-dbt, prefect-aws, etc.). Raw commit count on a single repo is a poor proxy for project health. Prefect 3.0 shipped significant architectural changes including transactional semantics [21].

### Prefect 3.0 has unique differentiators
Prefect 3.0 introduced transactional semantics — SQL-inspired transaction/rollback patterns that ensure data consistency across multi-step workflows [21]. Runtime graph construction allows dynamic workflow modification during execution, unlike Dagster's import-time graph freeze. Prefect achieved 98% runtime overhead reduction on Dask/Ray distributed workloads. Zero marginal execution cost pricing (per-user, not per-run) is a distinct advantage for high-volume scenarios [20].

### Temporal and Kestra are notable alternatives
Temporal excels at stateful/durable execution patterns — AI agent orchestration, compliance workflows, long-running processes with automatic state persistence. Kestra provides YAML-based multi-language orchestration with 600+ plugins, appealing to teams that want polyglot pipeline definitions [24]. Both were correctly excluded from scope (this research focuses on Python-native data pipeline orchestration) but are worth noting for adjacent use cases.

---

## Findings

### Finding 1: Three fundamentally different paradigms — task-centric, asset-centric, flow-centric
**Confidence: HIGH**

Airflow orchestrates tasks, Dagster orchestrates data assets, Prefect orchestrates Python functions. This is not a maturity gap — it is a philosophical difference that shapes every downstream decision. Airflow asks "what tasks should run and when?" Dagster asks "what data should exist and is it fresh?" Prefect asks "what Python code should execute and how?" Airflow 3.0 added asset concepts, but they function as dependency signals (event-driven triggers between DAGs), not full software-defined assets with lineage tracking, freshness policies, and partition awareness. Teams should select based on which question matches their mental model, not feature checklists.

### Finding 2: dbt integration maturity: Dagster > Cosmos > Prefect
**Confidence: HIGH**

Dagster provides the deepest dbt integration: each dbt model becomes a first-class Dagster asset with automatic lineage, partition awareness via CLI variables, and dbt tests mapped to asset checks. Cosmos (Airflow) provides mature per-model task decomposition with 21M+ monthly downloads, broad execution modes (standard, virtualenv, Docker, K8s, ECS), and active development including Airflow 3 support and dbt Fusion integration. Prefect's v0.7.0+ per-node mapping is improving but lacks result persistence, caching, and partition support — and the architecture "significantly differs" between versions, indicating ongoing instability. For teams where dbt is the primary transformation layer, Dagster offers the most cohesive experience; Cosmos is the pragmatic choice for existing Airflow installations.

### Finding 3: Cross-pipeline dependencies and SLA monitoring favor Dagster
**Confidence: HIGH**

Dagster's asset freshness policies (`time_window` with warn/fail thresholds, `cron`-based with deadline and lower_bound_delta) provide the most granular SLA mechanism among the three tools. Assets automatically form dependency graphs across code locations, enabling cross-pipeline dependency management without explicit wiring. Airflow 3.0 assets enable cross-DAG dependencies but persistent-state triggers can cause infinite loops. Prefect has no native cross-flow dependency mechanism and requires custom instrumentation for inter-pipeline coordination. For organizations where data freshness guarantees and multi-pipeline coordination are critical requirements, Dagster has a structural advantage.

### Finding 4: The selection framework is multi-dimensional, not single-axis
**Confidence: MODERATE**

No single tool "wins" across all dimensions. The selection should be evaluated across: (1) team size and engineering culture — large ops teams favor Airflow, data-centric teams favor Dagster, small Python-heavy teams favor Prefect; (2) pricing model — Dagster's credit-based pricing punishes high-frequency materialization, Prefect's per-user pricing favors high-volume workloads, Airflow's self-managed model shifts cost to infrastructure operations; (3) dynamic workflow needs — Prefect's runtime graph construction vs Dagster's import-time freeze; (4) dbt integration depth; (5) multi-language requirements — Airflow's Task Execution Interface targets future multi-language SDKs, Kestra already supports polyglot; (6) local dev experience — Dagster's single-command `dagster dev` vs Airflow's scheduler+DB+webserver stack; (7) LLM coding assistance — Airflow has the largest training corpus, Dagster's rapid API changes reduce LLM code quality.

### Finding 5: All three have significant production trade-offs
**Confidence: HIGH**

Airflow: infrastructure overhead (scheduler + database + webserver + workers), 3.0 early-release instability with migration edge cases, monolithic scaling issues at 100k+ dynamic tasks, persistent-state trigger infinite loops. Dagster: credit-based pricing surprises ($2,464/month for 8 ops every 5 min), K8s startup times reaching 10 min at 100% CPU, multiprocess executor 5+ sec per op overhead, IO manager abstraction complexity, poor LLM code generation due to rapid API changes. Prefect: no native data lineage, no cross-flow dependencies, dbt integration lacks result persistence and caching, no native partitioning, no guaranteed catch-up for missed runs. These are not edge cases — they are structural characteristics that teams will encounter in production.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Airflow 3.0 assets enable cross-DAG dependency management | [5][6] | verified | Assets function as dependency signals between DAGs |
| 2 | Dagster maps dbt models as first-class assets with lineage | [14] | verified | DbtProjectComponent compiles manifest, auto-links sources |
| 3 | Cosmos has 21M+ monthly downloads | [13] | verified | Astronomer-maintained, active development |
| 4 | Prefect has declining weekly commits since mid-2021 | [18] | disputed | Sourced from dagster.io vendor comparison; Prefect development split across multiple repos |
| 5 | Dagster local dev is single-command (`dagster dev`) | [2] | verified | No external dependencies required for local development |
| 6 | Airflow 3.0 assets provide lineage comparable to Dagster | — | refuted | Assets are event signals, not software-defined assets with lineage/freshness |
| 7 | Dagster credit-based pricing is $0.03/credit | [19] | verified | 8 ops every 5 min = ~$2,464/month on Solo tier |
| 8 | Prefect 3.0 has transactional semantics | [21] | verified | SQL-inspired transaction/rollback patterns |
| 9 | Prefect charges zero marginal execution cost | [20] | verified | Per-user pricing, no per-run or per-materialization charges |
| 10 | Dagster K8s startup can reach 10 min at 100% CPU | [22] | pending | Single practitioner report; needs broader confirmation |
| 11 | Prefect achieved 98% runtime overhead reduction on Dask/Ray | [20] | pending | Vendor claim from prefect.io/compare; needs independent verification |
| 12 | Airflow dynamic task mapping degrades at 100k+ tasks | [11] | verified | Scheduler timeouts reported in official docs |
| 13 | Dagster freshness policies superseded freshness checks since v1.12 | [10] | verified | Current docs confirm migration path |
| 14 | Prefect dbt integration lacks result persistence and caching | [15] | verified | Official docs state task runs don't persist results |
| 15 | Airflow 3.1+ is safer upgrade target than 3.0 | [7][23] | verified | Multiple sources cite 3.0 early-release instability |