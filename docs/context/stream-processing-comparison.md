---
name: Stream Processing Tool Comparison
description: "Spark Structured Streaming (micro-batch default, RTM for millisecond latency on Databricks), Flink (true per-record streaming with first-class state and exactly-once via Chandy-Lamport), and Databricks DLT (declarative abstraction with expectations-based quality but full platform lock-in) -- architecture, tradeoffs, and selection criteria"
type: context
related:
  - docs/research/2026-03-22-stream-processing.research.md
  - docs/context/streaming-windowing-watermarks.md
  - docs/context/streaming-observability-backpressure.md
  - docs/context/pipeline-orchestration-comparison.md
  - docs/context/production-platform-comparison.md
---

## Key Decision

Use Spark micro-batch when latency requirements are seconds-to-minutes and the team has Spark expertise. Use Flink when sub-second latency, complex stateful processing, or sophisticated late data handling is required. Use DLT only when already committed to Databricks and the declarative abstraction outweighs the loss of control and portability.

## Architecture Comparison

| Dimension | Spark Micro-batch | Spark RTM (4.1) | Flink |
|-----------|------------------|-----------------|-------|
| Processing model | Accumulated data as static DataFrame | Continuous flow with pipeline scheduling | True per-record streaming |
| Latency floor | ~1 second (trigger interval) | Single-digit ms p99 | Sub-millisecond |
| Exactly-once | Yes (replayable source + idempotent sink) | Not explicitly documented | Yes (Chandy-Lamport checkpointing) |
| State management | Limited, experimental | transformWithState (single-value iterator) | Native first-class (Value/List/Map/Reducing) |
| Backpressure | Implicit (batch accumulation) | Not documented | Credit-based flow control |
| Session windows | Yes | No | Yes |
| Stream-stream joins | Yes | No | Yes |
| Recovery | Coarse (restart application) | Coarse | Fine (restart individual tasks) |

## Spark Structured Streaming

Micro-batch by default: each trigger processes accumulated data as a static DataFrame. Five trigger types exist -- Default (as fast as possible), ProcessingTime (fixed interval), AvailableNow (process all then terminate, replaces deprecated Once), Continuous (experimental, at-least-once only), and RTM (Spark 4.1, Databricks-only).

Sources: Kafka, File (directory monitoring), Socket (testing only), Rate (benchmarking). Sinks: File, Kafka, Foreach/ForeachBatch (at-least-once only for foreachBatch), Console, Memory. Delta Lake works as both source and sink with exactly-once guarantees.

Checkpoints store source offsets, commit records, state, and metadata. Checkpoint compatibility survives filter changes, rate limit adjustments, and trigger interval changes. It breaks on source type changes, stateful operation schema changes, or sink type changes -- requiring full reprocessing.

Exactly-once end-to-end requires all three: replayable sources, deterministic processing, and idempotent sinks. Missing any one degrades to at-least-once.

## Spark RTM

RTM bridges the latency gap but with significant restrictions: only Kafka/Event Hubs sources, only Kafka sinks and foreachWriter, no session windows, no stream-stream joins, no forEachBatch, update output mode only, requires dedicated non-autoscaling clusters, DBR 16.4+. Best suited for simple stateless Kafka-to-Kafka transformations on Databricks.

## Apache Flink

State is a first-class primitive. Every operator maintains state partitioned by key with single-writer semantics -- no distributed locks needed. State primitives: ValueState, ListState, MapState, ReducingState. Flink handles backpressure automatically via credit-based flow control.

Flink 2.0 (March 2025) introduced ForSt, a disaggregated state backend storing state on remote DFS with local cache: up to 94% checkpoint duration reduction, 49x faster recovery, 50% cloud cost savings. Breaking changes: DataSet API removed, Java 8 dropped, SourceFunction/SinkFunction removed, no state compatibility guarantee between 1.x and 2.x.

## Databricks Delta Live Tables

DLT abstracts streaming into declarative SQL/Python definitions. Two dataset types: streaming tables (append-only incremental processing) and materialized views (batch recomputation). Two execution modes: continuous (seconds-to-minutes latency) and triggered (scheduled).

Expectations enforce data quality: expect (log but keep), expect or drop (silently discard), expect or fail (halt pipeline). Quality metrics are tracked automatically.

DLT is Databricks-only with no portable API. No local testing story -- pipelines must deploy to a workspace. Schema changes after a streaming read begins cause failures requiring restart.

## Testing Streaming Pipelines

Four layers, fast to slow: (1) Unit tests on pure transformation functions. (2) Operator harness tests -- Flink test harnesses or Spark MemoryStream with controlled time/watermarks. (3) Integration tests with embedded cluster (Flink MiniCluster, Spark local mode). (4) End-to-end tests against real Kafka/databases. Key practices: make sources/sinks pluggable, test with parallelism > 1, test checkpoint recovery, test watermark behavior. DLT lacks layers 1-3 -- everything requires a running Databricks workspace.
