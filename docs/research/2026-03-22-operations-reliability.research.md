---
name: "Operations & Reliability"
description: "Data observability is NOT pipeline monitoring — observability infers internal state from external outputs while monitoring watches known metrics; dbt source freshness is not run by dbt build (critical operational gap); dlt has no default retry (must use tenacity); alert fatigue is the #1 operational challenge with 60-80% reduction possible through dedup/grouping/suppression; Data Reliability Engineering (DRE) is emerging as SRE's parallel for data systems; Airflow SLAs removed in 3.0 and replaced by Deadline Alerts in 3.1"
type: research
sources:
  - https://docs.getdbt.com/reference/resource-properties/freshness
  - https://docs.getdbt.com/docs/deploy/source-freshness
  - https://dlthub.com/docs/running-in-production/running
  - https://docs.dagster.io/guides/observe/alerts/alert-policy-types
  - https://docs.dagster.io/guides/observe/alerts/creating-alerts
  - https://docs.dagster.io/guides/observe/asset-freshness-policies
  - https://docs.prefect.io/v3/how-to-guides/workflows/state-change-hooks
  - https://docs.prefect.io/v3/develop/write-tasks
  - https://www.prefect.io/blog/data-pipeline-monitoring-best-practices
  - https://www.montecarlodata.com/blog-what-is-data-observability/
  - https://www.montecarlodata.com/product/the-data-observability-solution/
  - https://www.bigeye.com/blog/data-reliability-engineering-versus-site-reliability-engineering
  - https://www.getdbt.com/blog/data-slas-best-practices
  - https://opeonikute.dev/posts/distributed-tracing-for-batch-workloads
  - https://risingwave.com/blog/5-crucial-pillars-of-data-observability-for-modern-data-management/
  - https://medium.com/@squadcast/alert-noise-reduction-a-complete-guide-to-improving-on-call-performance-2025-f9e1c26112d3
  - https://dev.to/andreparis/queue-based-exponential-backoff-a-resilient-retry-pattern-for-distributed-systems-37f3
  - https://www.superstream.ai/blog/kafka-dead-letter-queue
  - https://www.sparkcodehub.com/airflow/task-management/failure-handling
  - https://tacnode.io/post/what-is-stale-data
  - https://www.rudderstack.com/blog/data-pipeline-monitoring/
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-pipeline-orchestration.research.md
---

## Summary

**Research question:** What observability, reliability, and incident response patterns are needed to operate data pipelines in production?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 21 | **Searches:** 10 across Google

**Key findings:**
- Data observability and pipeline monitoring are distinct disciplines — observability infers internal state from external outputs (freshness, volume, distribution, schema, lineage), while monitoring watches known metrics (throughput, latency, error rate)
- dbt `dbt source freshness` is NOT run by `dbt build` — a critical operational gap that teams discover late and must wire into their orchestrator separately
- dlt has NO default retry behavior — must explicitly configure tenacity with Terminal vs Transient exception classification
- Alert fatigue is the #1 operational challenge; deduplication, grouping, and suppression can reduce alert noise by 60-80%
- Data Reliability Engineering (DRE) is emerging as a discipline parallel to SRE, applying error budgets, SLOs, and incident response patterns to data systems
- Airflow SLAs were removed in 3.0 and replaced by Deadline Alerts in 3.1 — teams upgrading will temporarily lose SLA functionality

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://docs.getdbt.com/reference/resource-properties/freshness | Source freshness | dbt Labs | current docs | T1 | verified |
| 2 | https://docs.getdbt.com/docs/deploy/source-freshness | Source freshness (deploy) | dbt Labs | current docs | T1 | verified |
| 3 | https://dlthub.com/docs/running-in-production/running | Running in production | dlt | current docs | T1 | verified |
| 4 | https://docs.dagster.io/guides/observe/alerts/alert-policy-types | Alert policy types | Dagster | current docs | T1 | verified |
| 5 | https://docs.dagster.io/guides/observe/alerts/creating-alerts | Creating alerts | Dagster | current docs | T1 | verified |
| 6 | https://docs.dagster.io/guides/observe/asset-freshness-policies | Asset freshness policies | Dagster | current docs | T1 | verified |
| 7 | https://docs.prefect.io/v3/how-to-guides/workflows/state-change-hooks | State change hooks | Prefect | current (v3) | T1 | verified |
| 8 | https://docs.prefect.io/v3/develop/write-tasks | Write tasks | Prefect | current (v3) | T1 | verified |
| 9 | https://www.prefect.io/blog/data-pipeline-monitoring-best-practices | Data pipeline monitoring best practices | Prefect | 2024 | T4 | verified — vendor blog |
| 10 | https://www.montecarlodata.com/blog-what-is-data-observability/ | What is data observability? | Monte Carlo | 2024 | T4 | verified — vendor blog (coined the term) |
| 11 | https://www.montecarlodata.com/product/the-data-observability-solution/ | The data observability solution | Monte Carlo | current | T4 | verified — vendor product page |
| 12 | https://www.bigeye.com/blog/data-reliability-engineering-versus-site-reliability-engineering | DRE vs SRE | Bigeye | 2024 | T4 | verified — vendor blog |
| 13 | https://www.getdbt.com/blog/data-slas-best-practices | Data SLAs best practices | dbt Labs | 2024 | T4 | verified — vendor blog |
| 14 | https://opeonikute.dev/posts/distributed-tracing-for-batch-workloads | Distributed tracing for batch workloads | Opeo Adeyemi | 2024 | T5 | verified — practitioner blog |
| 15 | https://risingwave.com/blog/5-crucial-pillars-of-data-observability-for-modern-data-management/ | 5 pillars of data observability | RisingWave | 2024 | T5 | verified — vendor blog |
| 16 | https://medium.com/@squadcast/alert-noise-reduction-a-complete-guide-to-improving-on-call-performance-2025-f9e1c26112d3 | Alert noise reduction | Squadcast | 2025 | T5 | verified — vendor blog |
| 17 | https://dev.to/andreparis/queue-based-exponential-backoff-a-resilient-retry-pattern-for-distributed-systems-37f3 | Exponential backoff patterns | Andre Paris | 2024 | T5 | verified — practitioner blog |
| 18 | https://www.superstream.ai/blog/kafka-dead-letter-queue | Kafka dead letter queue | Superstream | 2024 | T5 | verified — vendor blog |
| 19 | https://www.sparkcodehub.com/airflow/task-management/failure-handling | Airflow failure handling | SparkCodeHub | 2024 | T5 | verified — community tutorial |
| 20 | https://tacnode.io/post/what-is-stale-data | What is stale data | Tacnode | 2024 | T5 | verified — vendor blog |
| 21 | https://www.rudderstack.com/blog/data-pipeline-monitoring/ | Data pipeline monitoring | RudderStack | 2024 | T4 | verified — vendor blog |

---

## Sub-question 1: Observability Instrumentation (Metrics, Logs, Traces, Dashboards)

### Data observability vs pipeline monitoring

These are distinct disciplines that teams routinely conflate. Pipeline monitoring watches known metrics — throughput, latency, error rate, resource utilization — and fires alerts when thresholds breach. Data observability infers internal system state from external outputs, answering questions like "Is this data correct? Is it fresh? Has its shape changed?" [10].

Monte Carlo defines five pillars of data observability: **freshness** (is data arriving on time?), **distribution** (are values within expected ranges?), **volume** (did the expected number of rows arrive?), **schema** (have columns or types changed?), and **lineage** (what upstream changes impact this table?) [10][15]. Pipeline monitoring covers none of these — a pipeline can complete successfully while producing stale, malformed, or incomplete data.

### Core monitoring metrics

Four metrics form the baseline for pipeline monitoring [9][21]:

1. **Throughput** — records processed per unit time, measured at each pipeline stage
2. **Latency** — time from source event to downstream availability (end-to-end, not just task duration)
3. **Error rate** — failures per total executions, broken down by stage and error type
4. **Freshness** — time since the most recent valid data arrived in each destination table

### Distributed tracing for batch workloads

OpenTelemetry tracing can be applied to batch data pipelines, not just request/response systems. The key challenge is **cross-process trace propagation** — batch stages often run in separate processes or containers. W3C TraceContext provides a standard propagation format. Each pipeline stage creates a span; the trace ID follows data through extraction, transformation, and loading. This enables answering "Where did this pipeline run slow?" with the same tooling used for microservices [14].

Practical instrumentation approach: generate a UUID or trace ID at pipeline start, propagate it through each stage via metadata or environment variables, and emit structured logs with the trace ID as a correlation key. This enables tracing a single pipeline run across dlt extraction, dbt transformation, and orchestrator scheduling [9].

### Dashboard design

Effective data pipeline dashboards separate operational health (pipeline execution status, resource utilization, task durations) from data health (freshness, volume trends, schema changes, test results). The operational dashboard answers "Is the system running?" The data dashboard answers "Is the output trustworthy?" Monte Carlo's ML-powered monitors attempt to automate the data health layer by learning expected patterns and surfacing anomalies without manual threshold configuration [11].

---

## Sub-question 2: Alerting Patterns and On-Call Workflows

### Dagster alerting

Dagster provides six alert policy types with built-in noise reduction — alerts trigger only on state changes, not repeated failures [4]. Alert types cover: asset materialization failure, asset check failure, run failure, run timeout, schedule failure, and sensor failure. Notifications route to email, Slack, or PagerDuty via UI or CLI YAML configuration [5]. Dagster alerts are tightly coupled to the asset model, meaning alerts carry asset lineage context — when a downstream asset fails, the alert can surface which upstream asset caused the issue.

### Prefect state change hooks

Prefect provides five state change hooks: `on_completion`, `on_failure`, `on_cancellation`, `on_crashed`, `on_running` [7]. Critical limitation: hooks run in-process and are not guaranteed to execute if the process crashes. Hooks interact with retries — `on_failure` fires on each retry attempt, not just the final failure. For guaranteed alerting, Prefect recommends Cloud automations rather than in-process hooks.

### Alert fatigue and noise reduction

Alert fatigue is the #1 operational challenge for data teams running pipelines in production. The problem is straightforward: too many alerts, too little signal. Three techniques reduce noise by 60-80% [16]:

1. **Deduplication** — collapse repeated alerts for the same root cause into a single notification
2. **Grouping** — bundle related alerts (e.g., all assets downstream of a failed source) into a single incident
3. **Suppression** — silence alerts during known maintenance windows or planned deployments

Dagster's built-in approach of alerting only on state changes (not repeated failures) addresses deduplication natively. Prefect automations with proactive triggers address the inverse problem — alerting on absence of expected events (e.g., "this pipeline should have run by 8am but didn't").

### On-call workflows for data teams

DRE (Data Reliability Engineering) adapts SRE on-call patterns to data systems [12]. Key differences from traditional SRE on-call: data incidents are often not "the system is down" but "the data is wrong" — harder to detect, harder to triage, harder to define resolution. Runbooks for data incidents must include: which upstream sources feed the broken asset, who the downstream consumers are, what the blast radius is (lineage-derived), and what "fixed" means (re-materialization? manual correction? communication to stakeholders?).

---

## Sub-question 3: Retry Strategies and Failure Classification

### Failure classification: Terminal vs Transient

The foundation of any retry strategy is classifying failures into two categories [3][17]:

- **Transient failures** — temporary conditions that may resolve on retry: network timeouts, rate limits, database connection pool exhaustion, cloud API throttling. These should be retried.
- **Terminal failures** — permanent conditions that will never resolve on retry: authentication errors, schema mismatches, invalid SQL, missing required columns, permissions denied. These must not be retried — doing so wastes resources and delays incident detection.

dlt makes this distinction explicit: exceptions inherit from either `TerminalException` or `TransientException`. Terminal exceptions immediately halt the pipeline. Transient exceptions are retried according to configured policy [3].

### Exponential backoff with jitter

The standard retry formula is: `min(base * 2^attempt, max_delay) + jitter` [17]. The exponential component prevents overwhelming a recovering service. The jitter component (random addition) prevents thundering herd — multiple retries all hitting the service at the same backoff interval. Without jitter, synchronized retries can cause the exact load spike that caused the original failure.

Prefect supports custom backoff schedules via `retry_delay_seconds` accepting a list — e.g., `[1, 10, 100]` for three retries with increasing delays [8]. This is more explicit than a formula but less flexible for long retry chains.

### dlt: No default retry

dlt has **no default retry behavior** — this is surprising and under-documented [3]. Pipelines that fail on transient errors will fail immediately unless the developer explicitly configures retries using the tenacity library. The recommended pattern:

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, max=30),
    retry=retry_if_exception(lambda e: not isinstance(e, TerminalException))
)
def run_pipeline():
    pipeline.run(source())
```

dlt also has operational concerns around `replace` disposition: it truncates the destination table before loading. If the load fails mid-stream, the table is left empty or partially loaded. Teams should use staging with atomic swap where the destination supports it [3].

### Airflow retry configuration

Airflow provides task-level retry configuration: `retries` (count), `retry_delay` (timedelta between attempts), `retry_exponential_backoff` (boolean), and `max_retry_delay` (ceiling). Callbacks `on_retry_callback` and `on_failure_callback` enable custom alerting logic. Trigger rules (`all_success`, `all_failed`, `one_success`, `none_failed_min_one_success`) control how downstream tasks respond to upstream failures [19].

Critical Airflow 3.0 change: SLA monitoring was removed entirely. Airflow 3.1 introduced Deadline Alerts as the replacement. Teams upgrading from Airflow 2.x will lose SLA functionality during the transition window [19].

### Dead letter queues

For streaming or event-driven pipeline components, dead letter queues (DLQs) capture failed records that cannot be processed after retry exhaustion [18]. DLQ records must include contextual metadata: original payload, error message, timestamp, retry count, source topic/table. Four implementation approaches exist: producer-side DLQ, consumer-side DLQ, broker-managed DLQ (e.g., Kafka native), and application-level DLQ. The parking-lot pattern moves records from DLQ to a secondary topic after a configurable time for later investigation [18].

---

## Sub-question 4: Error Handling in dbt, dlt, and Orchestrators

### dbt error handling

dbt's primary error handling mechanism is **tests** — assertions about data that run after model materialization. Tests catch data quality issues (not null, unique, accepted values, relationships) but do not prevent bad data from being written. dbt's `on_schema_change` configuration for incremental models controls behavior when source schema changes: `ignore` (default, silent data loss risk), `fail`, `append_new_columns`, `sync_all_columns` [1].

dbt source freshness provides an additional error surface: `warn_after` and `error_after` thresholds define staleness tolerance. The `loaded_at_field` column is evaluated against these thresholds, and `dbt source freshness` returns a nonzero exit code when sources are stale [1][2]. The critical operational gap: **`dbt source freshness` is NOT included in `dbt build`**. Teams must explicitly add this as a separate step in their orchestration pipeline. Failing to do so means stale data flows through the entire transformation layer undetected.

### dlt error handling

dlt uses Python exception handling with the Terminal/Transient distinction described above [3]. Graceful shutdown handles SIGINT and SIGTERM signals — the pipeline completes the current item and saves state before exiting. This is essential for containerized deployments where pods receive SIGTERM during scaling events.

dlt's `replace` disposition creates a dangerous failure mode: the destination table is truncated before the new data loads. If loading fails after truncation, the table is empty until the next successful run. Mitigation: use staging tables with atomic swap where the destination supports it, or use `merge` disposition with deduplication keys [3].

### Orchestrator error handling patterns

Each orchestrator handles errors differently at the structural level:

- **Dagster**: Asset materialization is atomic — it succeeds or fails as a unit. Failed assets are visible in the asset graph with clear upstream/downstream impact. Re-materialization targets specific assets without re-running the entire pipeline. Asset checks provide pre- and post-materialization validation.
- **Airflow**: Task-level retries with configurable backoff. `trigger_rule` on downstream tasks determines whether to proceed despite upstream failures. `on_failure_callback` enables custom error handling logic per task. The `BranchPythonOperator` can route to error-handling paths.
- **Prefect**: Flow-level and task-level retries. State change hooks fire on each state transition. Transactions (v3) provide rollback semantics for multi-step operations — if step 3 fails, steps 1-2 can be rolled back. Limitation: hooks run in-process and are not guaranteed if the process crashes [7].

---

## Sub-question 5: Data Freshness Tracking and SLA Enforcement

### dbt source freshness

dbt defines freshness at the source level using `warn_after` and `error_after` thresholds with a `loaded_at_field` column [1]. Example:

```yaml
sources:
  - name: raw
    tables:
      - name: orders
        loaded_at_field: _loaded_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

The `dbt source freshness` command evaluates each configured source against its thresholds and returns nonzero on staleness [2]. This must be wired into the orchestrator as a separate step — typically as a pre-check before `dbt build`. If freshness fails, the pipeline should halt to avoid propagating stale data through the transformation layer.

### Dagster asset freshness policies

Dagster provides two freshness policy types [6]:

1. **time_window** — `fail_window` and `warn_window` define staleness thresholds (e.g., fail if not materialized in 24h, warn at 12h)
2. **cron** — `deadline` and `lower_bound_delta` define expected materialization schedule (e.g., "must be materialized by 8am daily using data from the last 24h")

Freshness policies are evaluated continuously and surface in the Dagster UI as asset health indicators. They can be batch-applied across assets using `map_asset_specs()`. Limitation: not supported for `SourceAssets` or `CacheableAssetsDefinition` [6].

### SLA dimensions and enforcement

dbt Labs identifies five SLA dimensions for data systems [13]:

1. **Timeliness** — data arrives within agreed time windows
2. **Completeness** — expected records are present (volume checks)
3. **Accuracy** — values are correct (distribution checks, cross-referencing)
4. **Consistency** — data agrees across systems (reconciliation checks)
5. **Availability** — data is accessible when needed (uptime)

SLAs vs SLOs vs SLIs: SLAs are contractual commitments with consequences. SLOs are internal targets (typically stricter than SLAs). SLIs are the measured metrics that determine compliance. Error budgets define acceptable violation rates — e.g., "99.5% of tables refreshed within 2 hours" allows ~3.6 hours of cumulative violation per month [13].

The cost of poor data quality is estimated at **$12M annually** for organizations, driven by engineering time spent investigating issues, business decisions made on bad data, and customer trust erosion [13].

### Freshness tracking metrics

Two key freshness metrics [20]:

1. **Freshness SLA compliance %** — percentage of measurement windows where data was fresh according to the defined threshold
2. **Staleness ratio** — ratio of stale tables to total tables, tracked over time to identify degradation trends

ML-based anomaly detection can supplement threshold-based freshness checks by learning expected arrival patterns and alerting on deviations — useful when data arrives at irregular but predictable intervals (e.g., partner feeds that arrive between 2am-6am depending on their batch processing) [20].

---

## Challenge

Challenger research targeted the conflation of observability and monitoring, tool-specific operational gaps, and the maturity of emerging DRE practices. Six findings were challenged.

### Data observability is NOT pipeline monitoring

Many sources — including some official documentation — use "observability" and "monitoring" interchangeably. They are not the same. Monitoring watches known metrics against known thresholds: "Did the pipeline run? Did it succeed? How long did it take?" Observability asks open-ended questions about system state: "Why did row counts drop 40% on Tuesday? Why is this column's distribution bimodal when it was normal last week?" [10]. Monte Carlo coined the "five pillars" framework specifically to distinguish data observability from pipeline monitoring. Teams that invest only in monitoring will catch execution failures but miss data quality degradation — the more common and more damaging failure mode.

### dbt source freshness gap is a design choice, not a bug

The fact that `dbt source freshness` is excluded from `dbt build` is intentional — freshness checking queries the source database, which may be a production OLTP system where additional queries have cost and performance implications [1][2]. The design forces teams to be explicit about when to check freshness. But the consequence is that teams who follow tutorials and run `dbt build` in their orchestrator believe they have freshness monitoring when they do not. This gap is discovered during the first stale-data incident, not during setup.

### dlt's lack of default retry is a deliberate trade-off

dlt's documentation frames the absence of default retry as letting developers "choose their retry strategy" [3]. In practice, most developers assume a production-grade data loading tool retries transient failures by default. The explicit tenacity configuration requirement means that the first network blip in production surfaces as a pipeline failure, not a retry. Teams adopting dlt must add retry configuration to their production deployment checklist — it is not optional, despite being treated as optional in documentation examples.

### Alert fatigue statistics need context

The "60-80% reduction through dedup, grouping, and suppression" claim comes from Squadcast, an incident management vendor [16]. The figure is plausible — industry reports consistently cite 70%+ of alerts as non-actionable — but the specific reduction depends on how noisy the baseline is. A well-instrumented system with thoughtful thresholds may only achieve 20-30% reduction. The techniques themselves (dedup, grouping, suppression) are proven; the magnitude of improvement is environment-specific.

### DRE is emerging but not yet established

Data Reliability Engineering is positioned by vendors (Bigeye, Monte Carlo) as a discipline parallel to SRE [12]. The analogy is useful: SRE applies engineering practices to operations (error budgets, SLOs, incident response); DRE applies the same practices to data systems. But DRE lacks SRE's institutional maturity — there is no canonical "DRE book" equivalent to Google's SRE handbook, no widely accepted certification, and job titles with "Data Reliability" remain rare outside large tech companies. The practices are sound; the framing as a distinct discipline is aspirational.

### Airflow SLA removal creates a real upgrade risk

Airflow 2.x had task-level SLA monitoring that fired alerts when tasks exceeded expected duration. This was removed entirely in Airflow 3.0 [19]. The replacement — Deadline Alerts — was not available until Airflow 3.1. Teams that upgraded to 3.0 between its GA release and the 3.1 release lost SLA functionality with no built-in alternative. This is not a theoretical risk — it is a documented gap in the upgrade path that affects teams with SLA-dependent workflows.

---

## Findings

### Finding 1: Data observability and pipeline monitoring are distinct disciplines requiring different tooling
**Confidence: HIGH**

Pipeline monitoring answers "Did the pipeline run successfully?" Data observability answers "Is the output data trustworthy?" The five pillars of data observability — freshness, volume, distribution, schema, lineage — are orthogonal to pipeline execution metrics like throughput, latency, and error rate. A pipeline can succeed while producing stale, incomplete, or incorrectly distributed data. Teams need both: pipeline monitoring for operational health (handled by orchestrators natively) and data observability for data health (requiring additional tooling — dbt tests, Dagster asset checks, or dedicated platforms like Monte Carlo). Conflating the two creates blind spots where execution succeeds but data quality degrades silently.

### Finding 2: Retry strategy must be grounded in failure classification
**Confidence: HIGH**

The Terminal vs Transient distinction is the foundation of production retry strategy. Retrying terminal failures (auth errors, schema mismatches, invalid SQL) wastes resources and delays incident detection. Failing to retry transient failures (network timeouts, rate limits, connection pool exhaustion) causes unnecessary pipeline failures. dlt makes this explicit with exception hierarchy; Airflow and Prefect rely on developer judgment to configure appropriate retry conditions. The standard exponential backoff formula — `min(base * 2^attempt, max_delay) + jitter` — prevents thundering herd on recovery. Critical gap: dlt has no default retry, meaning transient failures crash the pipeline unless tenacity is explicitly configured.

### Finding 3: dbt source freshness is a critical operational gap that teams must explicitly address
**Confidence: HIGH**

`dbt source freshness` is not included in `dbt build` — this is by design (to avoid querying production OLTP systems unnecessarily) but creates a significant operational gap. Teams that run `dbt build` in their orchestrator without a separate freshness check step believe they have freshness monitoring when they do not. The gap is discovered during the first stale-data incident. Mitigation: wire `dbt source freshness` as a pre-check step in the orchestrator, fail the pipeline on stale sources before running transformations, and configure warn/error thresholds that match downstream SLA commitments.

### Finding 4: Alert fatigue is the #1 operational challenge, addressable through structured noise reduction
**Confidence: HIGH**

Data teams in production consistently cite alert noise as the primary operational burden. Three proven techniques reduce noise: deduplication (collapse repeated alerts for the same root cause), grouping (bundle related alerts into a single incident), and suppression (silence alerts during maintenance windows). Dagster addresses deduplication natively by alerting only on state changes. The magnitude of noise reduction (60-80% is cited but environment-dependent) depends on baseline alert quality. Teams should implement alerting in layers: critical alerts page on-call (asset materialization failures affecting SLA-bound consumers), warnings go to Slack (freshness degradation, volume anomalies), and informational alerts go to dashboards only (schema changes, distribution shifts).

### Finding 5: Data SLAs require explicit definition across five dimensions with error budgets
**Confidence: MODERATE**

Five SLA dimensions — timeliness, completeness, accuracy, consistency, availability — provide a framework for defining data reliability commitments. Error budgets (e.g., "99.5% of tables refreshed within 2 hours") translate these commitments into measurable targets with acceptable violation rates. The $12M annual cost of poor data quality (dbt Labs estimate) provides business justification for SLA investment. However, most teams lack the instrumentation to measure compliance across all five dimensions. Starting with timeliness (freshness) and completeness (volume) provides the highest signal-to-investment ratio. Accuracy and consistency require domain-specific validation logic that cannot be generalized.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | `dbt source freshness` is NOT included in `dbt build` | [1][2] | verified | By design — avoids querying production OLTP systems |
| 2 | dlt has no default retry behavior | [3] | verified | Must explicitly configure tenacity library |
| 3 | Monte Carlo defines five pillars: freshness, volume, distribution, schema, lineage | [10][15] | verified | Widely adopted framework, confirmed by multiple sources |
| 4 | Alert dedup/grouping/suppression reduces noise by 60-80% | [16] | qualified | Vendor claim from Squadcast; magnitude is environment-dependent |
| 5 | Dagster alerts only fire on state changes (built-in noise reduction) | [4] | verified | Six alert policy types, all state-change triggered |
| 6 | Prefect state change hooks run in-process and are not guaranteed | [7] | verified | Official docs recommend Cloud automations for guaranteed delivery |
| 7 | Airflow SLAs removed in 3.0, replaced by Deadline Alerts in 3.1 | [19] | verified | Creates upgrade gap for SLA-dependent workflows |
| 8 | Exponential backoff formula: min(base * 2^attempt, max_delay) + jitter | [17] | verified | Standard pattern, jitter prevents thundering herd |
| 9 | dlt `replace` disposition truncates before loading (data loss risk) | [3] | verified | Mitigation: staging with atomic swap |
| 10 | DRE is emerging as a discipline parallel to SRE | [12] | qualified | Vendor-promoted framing; practices are sound but discipline lacks institutional maturity |
| 11 | Poor data quality costs organizations $12M annually | [13] | pending | dbt Labs blog claim; methodology not detailed, needs independent verification |
| 12 | OpenTelemetry W3C TraceContext enables cross-process trace propagation for batch workloads | [14] | verified | Practitioner-demonstrated pattern |
| 13 | Prefect retry_delay_seconds accepts a list for custom backoff | [8] | verified | Official docs, e.g., [1, 10, 100] for three retries |
| 14 | Kafka DLQ records should include contextual metadata | [18] | verified | Original payload, error message, timestamp, retry count, source topic |
| 15 | dbt freshness SLA compliance % is a trackable metric | [20] | verified | Percentage of windows where data met freshness threshold |
