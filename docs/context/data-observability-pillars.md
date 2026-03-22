---
name: Data Observability Pillars
description: "Data observability and pipeline monitoring are distinct disciplines -- observability infers data health from outputs (freshness, volume, distribution, schema, lineage) while monitoring watches execution metrics (throughput, latency, error rate); teams need both but routinely conflate them"
type: context
related:
  - docs/research/2026-03-22-operations-reliability.research.md
  - docs/context/data-freshness-slas.md
  - docs/context/ci-cd-pipeline-design.md
---

## Key Takeaway

Pipeline monitoring answers "Did the pipeline run?" Data observability answers "Is the output data trustworthy?" A pipeline can succeed while producing stale, incomplete, or incorrectly distributed data. Teams that invest only in monitoring will catch execution failures but miss data quality degradation -- the more common and more damaging failure mode.

## Observability vs Monitoring

These are distinct disciplines that teams routinely conflate.

**Pipeline monitoring** watches known metrics against known thresholds: throughput (records per unit time at each stage), latency (end-to-end time from source event to downstream availability), error rate (failures per total executions by stage and type), and resource utilization. Orchestrators handle this natively.

**Data observability** infers internal system state from external outputs, answering open-ended questions: "Why did row counts drop 40% on Tuesday? Why is this column's distribution bimodal when it was normal last week?"

## Five Pillars of Data Observability

Monte Carlo's framework, widely adopted across the industry:

1. **Freshness** -- Is data arriving on time? Time since the most recent valid data arrived in each destination table.
2. **Volume** -- Did the expected number of rows arrive? Detects partial loads, dropped partitions, silent upstream failures.
3. **Distribution** -- Are values within expected ranges? Catches data corruption, unit changes, upstream business logic shifts.
4. **Schema** -- Have columns or types changed? Detects breaking changes from upstream sources before they propagate.
5. **Lineage** -- What upstream changes impact this table? Enables blast radius analysis during incidents.

None of these are covered by pipeline monitoring. All five require dedicated tooling -- dbt tests, Dagster asset checks, or platforms like Monte Carlo.

## Dashboard Design

Separate operational health from data health into two views:

- **Operational dashboard:** Pipeline execution status, resource utilization, task durations, retry counts. Answers "Is the system running?"
- **Data dashboard:** Freshness trends, volume anomalies, schema changes, test results. Answers "Is the output trustworthy?"

ML-powered monitors (Monte Carlo's approach) learn expected patterns and surface anomalies without manual threshold configuration. Useful when data arrives at irregular but predictable intervals.

## Distributed Tracing for Batch Workloads

OpenTelemetry tracing applies to batch data pipelines, not just request/response systems. The pattern: generate a trace ID at pipeline start, propagate it through each stage via metadata or environment variables, emit structured logs with the trace ID as a correlation key. W3C TraceContext provides the standard propagation format. This enables tracing a single pipeline run across dlt extraction, dbt transformation, and orchestrator scheduling using the same tooling as microservices.

## Decision Rules

1. Instrument pipeline monitoring first (orchestrator-native), then layer data observability on top.
2. Start with freshness and volume -- highest signal-to-investment ratio. Add distribution, schema, and lineage as the system matures.
3. Separate operational and data dashboards. Do not mix them.
4. Propagate trace IDs across pipeline stages for cross-process correlation.
