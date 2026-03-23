---
name: Streaming Observability and Backpressure
description: "Five baseline streaming metrics (consumer lag, throughput, e2e latency, checkpoint duration, state size); Flink backpressure diagnostics via busyTimeMsPerSecond (bottleneck is NOT the backpressured operator); Spark batch duration as backpressure proxy; Kafka lag patterns; two-tier alerting strategy"
type: context
related:
  - docs/research/2026-03-22-stream-processing.research.md
  - docs/context/stream-processing-comparison.md
  - docs/context/streaming-windowing-watermarks.md
  - docs/context/data-observability-pillars.md
  - docs/context/data-freshness-slas.md
  - docs/context/retry-failure-patterns.md
---

## Key Insight

Backpressure is the single most critical operational signal for streaming pipelines. In Flink, the bottleneck operator is NOT the one showing the backpressure flag -- backpressure propagates upstream. Find the first operator in the chain that is NOT backpressured but has `busyTimeMsPerSecond > 900` (90% utilization). In Spark, the signal is batch processing duration exceeding the trigger interval.

## Five Baseline Metrics

1. **Consumer lag** -- offset gap between latest produced and latest consumed record. Growing lag means the pipeline cannot keep up with input volume.
2. **Throughput** -- records/second and bytes/second at each operator. Compare against 7-day rolling baselines to detect degradation.
3. **End-to-end latency** -- time from source event timestamp to sink write. The most user-visible metric.
4. **Checkpoint duration** -- a leading indicator. Increasing checkpoint times predict failures before they occur.
5. **State size** -- should remain stable for well-designed jobs. Unbounded growth indicates missing watermarks or incorrect key design.

## Flink Backpressure Diagnostics

Flink exposes three per-subtask metrics that sum to ~1000ms: `backPressuredTimeMsPerSecond`, `idleTimeMsPerSecond`, and `busyTimeMsPerSecond`. The Web UI color-codes: blue (idle), red (busy), black (backpressured).

The diagnostic pattern: walk the operator chain from sink to source. The bottleneck is the first operator that is NOT backpressured but has high busyTime. Common causes: slow external lookups, heavy serialization, insufficient sink parallelism.

Flink's credit-based flow control propagates backpressure automatically. Downstream tasks grant credits (one per network buffer) to upstream tasks. When downstream buffers fill, credits stop, upstream output buffers saturate, and pressure propagates toward the source. This is inherent and requires no configuration.

## Spark Streaming Monitoring

`StreamingQueryProgress` exposes batch-level metrics: `inputRowsPerSecond`, `processedRowsPerSecond`, `batchDuration`, and `stateOperator` metrics (row count, memory used). The primary backpressure signal: batch processing duration exceeding the trigger interval. A 30-second trigger taking 45 seconds means the pipeline is falling behind.

RTM adds latency metrics: `processingLatencyMs`, `sourceQueuingLatencyMs`, and `e2eLatencyMs` with p50/p99 breakdowns.

## Kafka Consumer Lag Patterns

Lag patterns tell a diagnostic story:
- **Linear growth** -- sustained throughput mismatch; scale the consumer
- **Spike then recovery** -- transient burst; no action unless SLA breached
- **Exponential growth** -- cascading failure; immediate intervention required
- **Lag exceeding topic retention** -- data loss; records purged before consumption

Monitor `records-lag-max`, `records-lag-avg`, and `fetch-rate`. Convert lag from offsets to time units for end-to-end latency visibility.

## Two-Tier Alerting Strategy

**Critical alerts (page on-call):**
- Job not running for > 2 minutes
- Checkpoint failures in the last 10 minutes
- Consumer lag growing continuously for > 5 minutes

**Warning alerts (Slack notification):**
- Checkpoint duration trending upward over 30 minutes
- `busyTimeMsPerSecond > 900` for 10+ minutes
- State size growing over 1-hour window
- Throughput below 50% of 7-day average for 15+ minutes

Use `deriv()` and `avg_over_time()` in PromQL to detect trends rather than spikes. Implement Alertmanager inhibition rules to suppress downstream alerts when root-cause alerts fire.
