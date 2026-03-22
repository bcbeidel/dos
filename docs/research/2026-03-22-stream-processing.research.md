---
name: "Stream Processing"
description: "Spark Structured Streaming is micro-batch by default with RTM (Spark 4.1) now offering millisecond latency on Databricks but with significant sink/state limitations; Flink is the superior choice for complex stateful event-time processing with true per-record streaming, credit-based backpressure, and exactly-once via Chandy-Lamport checkpointing; Databricks DLT abstracts streaming complexity through declarative SQL/Python with expectations-based quality enforcement but locks you into the Databricks platform; watermarking is a precision-vs-latency tradeoff with no universal default; session windows are the hardest to implement correctly and RTM does not support them; Flink 2.0 disaggregated state (ForSt) reduces checkpoint duration by up to 94% and recovery time by 49x; testing streaming pipelines requires four layers (unit, operator harness, integration with MiniCluster/embedded, end-to-end); backpressure is the #1 operational signal — in Flink find the first non-backpressured busy operator, in Spark watch for increasing batch durations"
type: research
sources:
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
  - https://docs.databricks.com/aws/en/structured-streaming/checkpoints
  - https://docs.databricks.com/aws/en/structured-streaming/triggers
  - https://docs.databricks.com/aws/en/structured-streaming/watermarks
  - https://docs.databricks.com/aws/en/structured-streaming/real-time
  - https://docs.databricks.com/aws/en/structured-streaming/delta-lake
  - https://docs.databricks.com/aws/en/data-engineering/tables-views
  - https://nightlies.apache.org/flink/flink-docs-master/docs/concepts/stateful-stream-processing/
  - https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/event-time/generating_watermarks/
  - https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/testing/
  - https://nightlies.apache.org/flink/flink-docs-master/docs/ops/monitoring/back_pressure/
  - https://flink.apache.org/2025/03/24/apache-flink-2.0.0-a-new-era-of-real-time-data-processing/
  - https://www.decodable.co/blog/comparing-apache-flink-and-spark-for-modern-stream-data-processing
  - https://streamkap.com/resources-and-guides/backpressure-stream-processing
  - https://streamkap.com/resources-and-guides/flink-job-monitoring-metrics
  - https://www.singdata.com/trending/spark-structured-streaming-exactly-once-guarantees/
  - https://moderndata101.substack.com/p/understand-the-new-spark
  - https://quix.io/blog/windowing-stream-processing-guide
  - https://www.databricks.com/blog/introducing-real-time-mode-apache-sparktm-structured-streaming
  - https://www.decodable.co/blog/understanding-apache-flink-event-time-and-watermarks
  - https://oneuptime.com/blog/post/2026-01-24-streaming-late-data/view
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-21-pipeline-design-architecture.research.md
  - docs/research/2026-03-22-pipeline-orchestration.research.md
  - docs/research/2026-03-22-operations-reliability.research.md
---

## Summary

**Research question:** How should streaming data pipelines be designed and operated, and what are the tradeoffs between Spark Structured Streaming, Databricks DLT, and Apache Flink?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 21 | **Searches:** 18 across Google

**Key findings:**
- Spark Structured Streaming is micro-batch by default — each trigger processes accumulated data as a static DataFrame, introducing latency equal to the batch interval (minimum ~1 second); Spark 4.1 RTM on Databricks reduces this to single-digit millisecond p99 but only supports Kafka sources/sinks and has no session window or stream-stream join support
- Apache Flink is purpose-built for true per-record streaming with sub-millisecond latency, native stateful processing (ValueState, ListState, MapState), credit-based backpressure propagation, and exactly-once semantics via Chandy-Lamport distributed snapshots
- Databricks Delta Live Tables abstracts streaming pipeline complexity through declarative SQL/Python definitions with expectations-based data quality enforcement, but locks teams into the Databricks platform and provides less control over processing semantics than raw Spark or Flink
- Watermarking is a precision-vs-latency tradeoff — larger watermark delays capture more late data but increase result latency; there is no universal default because the right value depends on source-specific out-of-orderness characteristics
- Flink 2.0 disaggregated state management (ForSt) reduces checkpoint duration by up to 94% and recovery time by 49x by decoupling state storage from compute via remote DFS, a fundamental architectural shift for cloud-native streaming
- Backpressure is the most critical operational signal — in Flink, the bottleneck is the first non-backpressured operator with high busyTimeMsPerSecond; in Spark, increasing batch processing durations that exceed the trigger interval indicate the pipeline cannot keep up

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html | Structured Streaming Programming Guide | Apache Spark | Spark 4.1.1 | T1 | verified |
| 2 | https://docs.databricks.com/aws/en/structured-streaming/checkpoints | Structured Streaming checkpoints | Databricks | current docs | T1 | verified |
| 3 | https://docs.databricks.com/aws/en/structured-streaming/triggers | Configure Structured Streaming trigger intervals | Databricks | current docs | T1 | verified |
| 4 | https://docs.databricks.com/aws/en/structured-streaming/watermarks | Apply watermarks to control data processing thresholds | Databricks | current docs | T1 | verified |
| 5 | https://docs.databricks.com/aws/en/structured-streaming/real-time | Real-time mode in Structured Streaming | Databricks | current docs | T1 | verified |
| 6 | https://docs.databricks.com/aws/en/structured-streaming/delta-lake | Delta table streaming reads and writes | Databricks | current docs | T1 | verified |
| 7 | https://docs.databricks.com/aws/en/data-engineering/tables-views | Tables and views in Databricks | Databricks | current docs | T1 | verified |
| 8 | https://nightlies.apache.org/flink/flink-docs-master/docs/concepts/stateful-stream-processing/ | Stateful Stream Processing | Apache Flink | current docs | T1 | verified |
| 9 | https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/event-time/generating_watermarks/ | Generating Watermarks | Apache Flink | current docs | T1 | verified |
| 10 | https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/testing/ | Testing | Apache Flink | current docs | T1 | verified |
| 11 | https://nightlies.apache.org/flink/flink-docs-master/docs/ops/monitoring/back_pressure/ | Monitoring Back Pressure | Apache Flink | current docs | T1 | verified |
| 12 | https://flink.apache.org/2025/03/24/apache-flink-2.0.0-a-new-era-of-real-time-data-processing/ | Apache Flink 2.0.0: A new Era | Apache Flink | 2025-03 | T1 | verified |
| 13 | https://www.decodable.co/blog/comparing-apache-flink-and-spark-for-modern-stream-data-processing | Comparing Flink and Spark for Stream Processing | Decodable | 2025 | T4 | verified — vendor blog |
| 14 | https://streamkap.com/resources-and-guides/backpressure-stream-processing | Backpressure in Stream Processing | Streamkap | 2025 | T4 | verified — vendor blog |
| 15 | https://streamkap.com/resources-and-guides/flink-job-monitoring-metrics | Flink Job Monitoring: Key Metrics and Alerting | Streamkap | 2025 | T4 | verified — vendor blog |
| 16 | https://www.singdata.com/trending/spark-structured-streaming-exactly-once-guarantees/ | Spark Structured Streaming Exactly-Once Guarantees | SingData | 2025 | T5 | verified — practitioner blog |
| 17 | https://moderndata101.substack.com/p/understand-the-new-spark | Spark Streaming Feature that Changes Everything | ModernData101 | 2025 | T5 | verified — practitioner blog |
| 18 | https://quix.io/blog/windowing-stream-processing-guide | A guide to windowing in stream processing | Quix | 2025 | T4 | verified — vendor blog |
| 19 | https://www.databricks.com/blog/introducing-real-time-mode-apache-sparktm-structured-streaming | Introducing Real-Time Mode in Spark Structured Streaming | Databricks | 2025 | T4 | verified — vendor blog |
| 20 | https://www.decodable.co/blog/understanding-apache-flink-event-time-and-watermarks | Understanding Flink Event Time and Watermarks | Decodable | 2025 | T4 | verified — vendor blog |
| 21 | https://oneuptime.com/blog/post/2026-01-24-streaming-late-data/view | How to Fix Late Data Handling in Streaming | OneUptime | 2026-01 | T5 | verified — practitioner blog |

---

## Sub-question 1: Spark Structured Streaming — Sources, Sinks, Triggers, and Checkpointing

### Sources and sinks

Spark Structured Streaming supports four built-in source types: **Kafka** (the primary production source), **File** (reading from directories as new files appear), **Socket** (text data over TCP, testing only), and **Rate/Rate-per-micro-batch** (synthetic data generation for testing and benchmarking) [1]. Delta Lake tables serve as both source and sink with exactly-once guarantees, supporting `readStream` for continuous ingestion with configurable rate limiting via `maxFilesPerTrigger` (default 1000) and `maxBytesPerTrigger` [6].

Supported sinks include: **File** (Parquet, JSON, CSV to directories), **Kafka** (for event publishing), **Foreach/ForeachBatch** (arbitrary write logic — but `foreachBatch` provides only at-least-once delivery, not exactly-once [16]), **Console** (debugging), and **Memory** (debugging). Delta Lake as a sink guarantees exactly-once processing even with concurrent operations [6].

Three output modes control what results are written: **Append** (only new rows, default), **Complete** (entire result table rewritten each trigger, for aggregations), and **Update** (only changed rows emitted). Not all combinations of operations and output modes are valid — for example, aggregations without watermarks only support Complete mode [1].

### Trigger types

Spark 4.1 supports five trigger types [3]:

1. **Default** (no trigger specified) — processes micro-batches as fast as possible, equivalent to `processingTime='0 seconds'`
2. **ProcessingTime** — periodic micro-batches at fixed intervals (e.g., `processingTime='30 seconds'`); balances throughput and resource utilization
3. **AvailableNow** — processes all available data in multiple batches then terminates; replaces deprecated `Trigger.Once` as of Spark 3.4
4. **Continuous** (experimental since Spark 2.3) — true continuous processing with at-least-once semantics and ~1ms latency; never recommended for production by Databricks [3]
5. **RealTime** (Spark 4.1, Databricks only) — millisecond-latency continuous processing with pipeline scheduling and streaming shuffle; GA on Databricks Runtime 16.4+ [5]

The critical distinction: triggers can be changed between restarts for a given query without breaking checkpoint compatibility, except when switching between fundamentally different execution modes [2].

### Checkpointing and fault tolerance

Checkpoints store four components: **source offsets** (position in each source), **commits** (which micro-batches completed), **state** (for stateful operations like aggregations and joins), and **metadata** (query ID and configuration) [2]. Each streaming query requires a unique checkpoint location — sharing locations between queries is prohibited.

Checkpoint compatibility rules determine what changes survive restart. Allowed: adding/removing filters, adjusting rate limits, changing trigger intervals. Breaking: changing number/type of input sources, modifying stateful operation schemas, switching output sink types [2]. When checkpoint compatibility breaks, the query must start fresh from a new location, which means reprocessing all historical data.

Exactly-once end-to-end semantics require three components working together: **replayable sources** (Kafka, Delta, HDFS — can replay from saved offsets), **deterministic processing** (same input produces same output), and **idempotent sinks** (writing the same data twice produces no change) [16]. If any component is missing, the guarantee degrades to at-least-once.

---

## Sub-question 2: Databricks Delta Live Tables for Streaming

### Declarative pipeline definition

Delta Live Tables (DLT) abstracts streaming pipeline complexity into declarative SQL or Python definitions where developers specify *what* transformations to perform, and DLT manages *how* — including cluster orchestration, autoscaling, monitoring, and error recovery [7]. A DLT pipeline is a DAG of dataset definitions linking sources to target tables.

Two primary dataset types exist:

- **Streaming tables** — Delta tables with streaming semantics that process data incrementally and append-only; defined against continuously growing sources; only process data added since the last pipeline run [7]
- **Materialized views** — batch-semantic Delta tables that precompute and store query results; refreshed (recomputed) on each pipeline run rather than incrementally appended [7]

### Pipeline execution modes

DLT pipelines run in two modes [7]:

1. **Continuous** — the pipeline runs continuously, processing newly arrived data with latency of seconds to minutes; highest cost but lowest latency
2. **Triggered** (scheduled) — the pipeline runs periodically (every 10 minutes, hourly, daily); lower cost but higher latency

Streaming tables in continuous mode connect directly to sources like Kafka, Kinesis, or Event Hubs for low-latency ingestion. Auto Loader integration enables incremental file ingestion from cloud storage into Bronze-layer streaming tables [6].

### Data quality expectations

DLT's expectations are declarative data quality constraints applied to each record passing through the pipeline. Three enforcement actions are available:

1. **Expect** — log the violation but keep the record (quality reporting without data loss)
2. **Expect or drop** — silently discard records that violate the constraint
3. **Expect or fail** — halt the pipeline on first violation (strictest enforcement)

Expectations are defined inline with table definitions in SQL (`CONSTRAINT name EXPECT (condition)`) or Python (`@dlt.expect("name", "condition")`). Quality metrics (pass/fail counts per expectation) are tracked automatically and visible in the DLT UI. This is a significant operational advantage over raw Structured Streaming, where data quality checks must be implemented manually.

### DLT tradeoffs

The abstraction comes with real constraints. DLT is Databricks-only — there is no open-source equivalent or portable API. Debugging is harder because the framework manages cluster lifecycle and execution; developers cannot easily reproduce issues locally. Schema evolution in streaming context is limited: if the source schema changes after a streaming read begins, the query fails and must be restarted [6]. Enhanced autoscaling for DLT streaming workloads is GA but optimized for spiky workloads, which means steady-state streaming may overprovision.

---

## Sub-question 3: Flink Stateful Processing, Event Time, and Exactly-Once Semantics

### Stateful stream processing

Flink treats state as a first-class primitive. Every operator can maintain state that persists across events, partitioned by key and co-located with the processing task [8]. The state is stored in an embedded key/value store, distributed strictly together with the streams that the operators read. State primitives include `ValueState<T>` (single value per key), `ListState<T>` (list of values), `MapState<K,V>` (key-value map), and `ReducingState<T>` (aggregated value).

Flink's state partitioning guarantees that records with the same key are always handled by the same task, enforcing single-writer semantics without requiring distributed locks. This is architecturally different from Spark, where state management is "limited" and "experimental" according to Decodable's comparison [13].

### Event time and watermarks

Flink distinguishes between **event time** (timestamp embedded in the event, indicating when it actually occurred) and **processing time** (wall-clock time when the record is processed). Event time is essential for correct results when events arrive out of order or with variable delay [9].

Watermarks are special records injected into the stream that declare "all events with timestamps up to W have been observed." The `WatermarkStrategy` interface combines timestamp extraction with watermark generation [9]. Two built-in strategies cover most cases:

- **BoundedOutOfOrderness** — watermark lags behind the maximum observed timestamp by a configured duration; handles out-of-order arrival within known bounds
- **MonotonousTimestamps** — assumes strictly ascending timestamps; zero lag (equivalent to BoundedOutOfOrderness with Duration.ZERO)

For multi-source pipelines, watermarks propagate using the **minimum** across all input partitions. An idle source (producing no events) can stall the entire pipeline's watermark progress. The `withIdleness(Duration)` configuration marks inactive partitions as idle, preventing watermark blockage [9]. Watermark alignment via `withWatermarkAlignment()` prevents fast sources from racing ahead, pausing sources whose watermarks are too far in the future [9].

### Exactly-once via Chandy-Lamport checkpointing

Flink achieves exactly-once through distributed snapshots inspired by the Chandy-Lamport algorithm [8]. Checkpoint barriers are injected into the data stream and flow with records. When all operators have received a barrier, a consistent snapshot is created. Two modes exist:

- **Aligned checkpointing** — operators wait for barriers from all inputs before snapping state; provides exactly-once but can introduce latency when inputs have skewed throughput
- **Unaligned checkpointing** — barriers can overtake in-flight records (which become part of the checkpoint state); reduces checkpoint latency at the cost of larger checkpoint sizes

State backends determine where state is stored between checkpoints. **HashMapStateBackend** stores state in the JVM heap — fast but limited by available memory. **EmbeddedRocksDBStateBackend** (RocksDB) stores state on disk with in-memory caching — handles multi-terabyte state and supports incremental checkpointing (only changed data since last checkpoint), dramatically reducing checkpoint time for large state [12].

Savepoints are manually triggered snapshots in a canonical, version-stable format for operational use (upgrades, migrations, A/B testing). They are larger and slower than checkpoints because they prioritize portability over speed [8].

### Flink 2.0 disaggregated state (ForSt)

Flink 2.0 (released March 2025) introduces ForSt ("For Streaming"), a purpose-built state backend that decouples storage from compute [12]. State is stored on a remote distributed file system (DFS) with local disks as cache. Benchmark results:

- **Up to 94% reduction** in checkpoint duration
- **Up to 49x faster recovery** after failures or rescaling
- **Up to 50% cost savings** in cloud deployments
- Stateful queries with heavy I/O achieved 75-120% throughput compared to local state stores despite remote storage

Breaking changes in Flink 2.0 include: DataSet API removed, Java 8 no longer supported (minimum Java 11), SourceFunction/SinkFunction removed, per-job deployment mode eliminated, and state compatibility between 1.x and 2.x is NOT guaranteed [12]. The new DataStream V2 API is experimental and not recommended for production.

---

## Sub-question 4: Late Data Handling and Watermarking Strategies

### The precision-vs-latency tradeoff

Watermark configuration is fundamentally a tradeoff between two competing objectives [4]:

- **Larger watermark delay** — captures more late data (higher precision) but increases time before results are emitted (higher latency)
- **Smaller watermark delay** — emits results faster (lower latency) but drops more late-arriving records (lower precision)

There is no universal default. The correct watermark delay depends on the source's out-of-orderness characteristics, which vary by use case. A mobile app may have events arriving minutes late due to network connectivity. A Kafka topic with in-order partitions may have near-zero out-of-orderness. Measure actual late arrival distributions before configuring watermarks.

### Spark watermarking

In Spark Structured Streaming, `withWatermark("event_time", "10 minutes")` declares that events arriving more than 10 minutes after the latest observed event time may be dropped [4]. The watermark controls state cleanup — once the watermark passes a window's end time plus the delay, state for that window is purged. Without watermarks, state grows unboundedly, eventually causing OOM failures.

For multiple input streams, Spark supports two global watermark policies [4]:
- **Min policy** (default) — uses the slowest stream's watermark; safer but delays results
- **Max policy** — uses the fastest stream's watermark; faster results but may drop data from slower streams

Late-arriving records outside the watermark threshold "might still be processed but this isn't guaranteed" [4]. This is an important nuance: watermarks are a guarantee about what WILL be processed, not a hard cutoff for what WILL NOT be processed.

### Flink watermarking

Flink's watermark system is more granular. Watermark generators can be periodic (emitting at framework-defined intervals via `onPeriodicEmit()`) or punctuated (emitting reactively when special marker events appear in the stream) [9]. The `WatermarkStrategy` interface provides a clean separation between timestamp assignment and watermark generation.

Flink's side output mechanism for late data is a critical architectural advantage: records arriving after the watermark can be redirected to a side output stream for separate processing rather than being silently dropped [21]. This enables a three-tier late data strategy:
1. Records within watermark — processed normally in the window
2. Records within allowed lateness — update the window result
3. Records beyond allowed lateness — routed to side output for separate handling

### Practical watermarking guidance

Start with a watermark delay of 2-3x the observed p99 out-of-orderness, then adjust based on the impact of dropped records vs. result latency. Monitor the gap between watermark time and wall-clock time — a growing gap indicates the pipeline is falling behind. Track the count of late-arriving records dropped by the watermark to detect whether the configured delay is sufficient [21].

---

## Sub-question 5: Windowing Patterns

### Tumbling windows

Fixed-size, non-overlapping, contiguous time intervals. Each event belongs to exactly one window. Use case: minute-by-minute website traffic counts, hourly revenue aggregation [18].

Properties: simplest to implement, lowest state overhead (one window active at a time per key), deterministic assignment. All three engines (Spark, Flink, DLT) support tumbling windows natively.

### Sliding (hopping) windows

Fixed-size intervals that advance at a specified slide interval shorter than the window size, creating overlap. A 10-minute window with 5-minute slide means each event appears in two windows [18].

Properties: higher state cost than tumbling (multiple active windows per key), produces more output records, useful for smoothing trends. The slide interval determines how many concurrent windows exist: `window_size / slide_interval` windows overlap at any moment. Use case: 5-minute moving average of sensor readings updated every 30 seconds.

### Session windows

Activity-based windows defined by an inactivity timeout. A window starts when the first event arrives and extends with each subsequent event. The window closes when no event arrives within the timeout period [18].

Properties: most complex to implement, variable-size output, highest state overhead (must track per-key session boundaries), hardest to parallelize. Session windows are the most operationally demanding window type. Flink supports session windows natively. Spark supports session windows in micro-batch mode but **RTM does not support session windows** [5]. DLT supports session windows through Spark's implementation.

### Window lifecycle

Every window operation has three phases: **creation** (window boundary established by first event or time alignment), **accumulation** (events assigned to windows, state updated), and **trigger/eviction** (results emitted and state cleaned up, governed by watermarks). Incorrect watermark configuration causes either premature eviction (results emitted before all events arrive) or unbounded state growth (windows never close) [4].

---

## Sub-question 6: Micro-batch vs. Continuous Streaming Tradeoffs

### Architecture comparison

| Dimension | Spark Micro-batch | Spark RTM (4.1) | Flink |
|-----------|------------------|-----------------|-------|
| Processing model | Accumulated data as static DataFrame | Continuous flow with pipeline scheduling | True per-record streaming |
| Latency floor | ~1 second (trigger interval) | Single-digit ms p99 [5] | Sub-millisecond |
| Exactly-once | Yes (replayable source + idempotent sink) | Not explicitly documented [5] | Yes (Chandy-Lamport checkpointing) |
| State management | Limited, experimental arbitrary state [13] | transformWithState (single-value iterator) [5] | Native first-class (Value/List/Map/Reducing state) |
| Backpressure | Implicit (batch accumulation) | Not documented | Credit-based flow control [14] |
| Session windows | Yes | No [5] | Yes |
| Stream-stream joins | Yes | No [5] | Yes |
| Recovery granularity | Coarse (restart application) [13] | Coarse | Fine (restart individual tasks) [13] |

### When micro-batch is sufficient

Micro-batch is the correct choice when: latency requirements are in the seconds-to-minutes range, the team has existing Spark expertise, the pipeline is primarily ETL (extract-transform-load) with simple aggregations, and the operational complexity of running a separate Flink cluster is not justified. Spark's micro-batch model simplifies debugging (each batch is a standard DataFrame), checkpointing (one checkpoint per batch boundary), and resource management (batch-to-batch scaling).

### When true streaming is required

Flink is the correct choice when: sub-second latency is required, complex stateful processing is needed (CEP, session analysis, pattern detection), event-time semantics with sophisticated late data handling are critical, or the pipeline has many stateful operators that benefit from fine-grained recovery. Flink handles backpressure "inherently and automatically without explicit configuration" [13], while Spark requires manual tuning that demands "deep Spark expertise" [13].

### Spark RTM positioning

Spark RTM (Spark 4.1, Databricks-only) bridges the gap with millisecond latency but has significant restrictions: only Kafka and Event Hubs sources, only Kafka sinks and foreachWriter, no session windows, no stream-stream joins, no forEachBatch, update output mode only, requires dedicated non-autoscaling clusters, and DBR 16.4+ [5]. RTM is best suited for simple stateless transformations from Kafka to Kafka where the team already runs on Databricks. For complex streaming, Flink remains the better engine.

---

## Sub-question 7: Testing Strategies for Streaming Pipelines

### Four-layer testing model

Production streaming pipelines need four layers of testing, progressing from fast and isolated to slow and integrated:

**Layer 1: Unit tests** — test business logic functions in isolation without any streaming infrastructure. Pure functions that transform records should be tested with standard unit testing frameworks. This layer runs in milliseconds and catches logic errors early [10].

**Layer 2: Operator harness tests** — Flink provides specialized test harnesses (`OneInputStreamOperatorTestHarness`, `KeyedOneInputStreamOperatorTestHarness`, `TwoInputStreamOperatorTestHarness`) that enable testing stateful operators with controlled time progression, watermark injection, and state inspection without a running cluster [10]. For Spark, the equivalent is testing with in-memory sources (`MemoryStream`) and sinks in a local SparkSession.

**Layer 3: Integration tests with embedded cluster** — Flink's `MiniClusterWithClientResource` runs a local embedded cluster for end-to-end pipeline testing [10]. Spark's equivalent is a local-mode SparkSession. These tests exercise the full pipeline including serialization, partitioning, and state management but run in a single JVM.

**Layer 4: End-to-end tests** — full pipeline deployed against test instances of Kafka, databases, and storage systems. These tests validate connector configurations, schema compatibility, and integration with external systems. Use generated data that emulates production characteristics (volume, key distribution, out-of-orderness).

### Best practices

- **Make sources and sinks pluggable** — inject test sources/sinks in tests rather than copying production code [10]
- **Test with parallelism > 1** — parallel execution surfaces bugs that only appear when data is distributed across tasks [10]
- **Test checkpointing and recovery** — enable checkpointing in integration tests, trigger failures via test-only functions, and verify state recovery produces correct results [10]
- **Test watermark behavior** — inject events with controlled timestamps and verify window results match expectations for on-time, late, and very-late events
- **Test backpressure behavior** — introduce artificial delays in sinks to verify the pipeline degrades gracefully under load

### DLT testing limitations

DLT lacks a local testing story. Pipelines must be deployed to a Databricks workspace to execute. Unit testing individual transformation logic is possible by extracting pure functions, but testing the full DLT pipeline (including expectations, streaming tables, and materialized views) requires a running Databricks environment. This increases feedback loop time from milliseconds (Flink harness) to minutes (DLT pipeline deployment).

---

## Sub-question 8: Observability — Lag, Throughput, and Backpressure Monitoring

### Critical streaming metrics

Five metrics form the baseline for streaming pipeline observability [15]:

1. **Consumer lag** — the offset gap between the latest produced record and the latest consumed record; a growing lag indicates the pipeline cannot keep up with input volume
2. **Throughput** — records/second and bytes/second at each operator; compare against 7-day rolling baselines to detect degradation
3. **End-to-end latency** — time from source event timestamp to sink write; the most user-visible metric
4. **Checkpoint duration** — leading indicator of problems; increasing checkpoint times predict failures before they occur [15]
5. **State size** — should remain stable for well-designed jobs; unbounded growth indicates missing watermarks or incorrect key design

### Flink backpressure monitoring

Flink exposes three per-subtask metrics that sum to ~1000ms: `backPressuredTimeMsPerSecond`, `idleTimeMsPerSecond`, and `busyTimeMsPerSecond` [11]. The Flink Web UI color-codes tasks: blue (idle), red (busy), black (backpressured).

The key diagnostic pattern: **the bottleneck operator is NOT the one showing the backpressure flag**. Backpressure propagates upstream. Find the first operator in the chain that is NOT backpressured but has `busyTimeMsPerSecond > 900` (90% utilization) — that is the bottleneck [11][15]. Common bottleneck causes: slow external lookups, heavy serialization, insufficient parallelism at the sink.

Flink's credit-based flow control propagates backpressure automatically: downstream tasks grant credits (one per network buffer) to upstream tasks. When downstream buffers fill, credits stop, upstream output buffers saturate, and the pressure propagates toward the source [14].

### Spark streaming monitoring

Spark Structured Streaming exposes `StreamingQueryProgress` with batch-level metrics: `inputRowsPerSecond`, `processedRowsPerSecond`, `batchDuration`, and `stateOperator` metrics (number of rows, memory used). The primary backpressure signal is **batch processing duration exceeding the trigger interval** — when a 30-second trigger takes 45 seconds to process, the pipeline is falling behind.

RTM adds additional latency metrics: `processingLatencyMs` (read to write within a stage), `sourceQueuingLatencyMs` (time in the message bus before reading), and `e2eLatencyMs` (complete journey) with p50/p99 breakdowns [5].

### Alerting strategies

Based on Streamkap's monitoring guide [15], production Flink deployments should implement two alert tiers:

**Critical alerts (page on-call):**
- Job not running for > 2 minutes
- Checkpoint failures in the last 10 minutes
- Consumer lag growing continuously for > 5 minutes

**Warning alerts (Slack notification):**
- Checkpoint duration trending upward over 30 minutes
- `busyTimeMsPerSecond > 900` for 10+ minutes (backpressure)
- State size growing over 1-hour window
- Throughput below 50% of 7-day average for 15+ minutes

Use `deriv()` and `avg_over_time()` in PromQL to detect trends rather than spikes, and implement Alertmanager inhibition rules to suppress downstream alerts when root-cause alerts fire [15].

### Kafka consumer lag patterns

Lag patterns tell a diagnostic story [14]:
- **Linear growth** — sustained throughput mismatch; need to scale the consumer
- **Spike then recovery** — transient burst; no action needed unless SLA breached
- **Exponential growth** — cascading failure; immediate intervention required
- **Lag exceeding topic retention** — data loss; records purged before consumption

Monitor `records-lag-max`, `records-lag-avg`, and `fetch-rate`. Convert lag from offsets to time units for end-to-end latency visibility.

---

## Challenge

Challenger research targeted the marketing claims around Spark RTM vs Flink positioning, the practical limitations of DLT for streaming, and the universality of watermarking recommendations. Six findings were challenged.

### Spark RTM does NOT eliminate the case for Flink

Databricks positions RTM as making Flink unnecessary for Spark shops: "ultra-low latency streaming on Spark APIs without a second engine" [19]. The latency numbers are real — single-digit millisecond p99 for stateless workloads [5]. But RTM has significant restrictions that make it unsuitable for complex streaming: no session windows, no stream-stream joins, no forEachBatch, only Kafka/Event Hubs sources, only update output mode, requires dedicated non-autoscaling clusters, and `transformWithState` returns single values instead of all values per key [5]. Flink's stateful processing capabilities — native CEP, flexible windowing, fine-grained recovery, credit-based backpressure — remain unmatched for complex event processing workloads. RTM is best understood as Spark competing with Flink on simple streaming use cases, not as a replacement for Flink's full capabilities.

### DLT expectations are useful but not sufficient for data quality

DLT expectations provide inline data quality constraints that are genuinely valuable for catching obvious issues (nulls, out-of-range values, type violations). But expectations operate on individual records — they cannot detect distributional anomalies (sudden changes in value distributions), volumetric anomalies (unexpected drops in record counts), or cross-table consistency issues. Teams using DLT for streaming still need supplementary data quality tooling for statistical checks and cross-dataset validation. The DLT UI surfaces expectation pass/fail rates, which is useful for monitoring but not a substitute for full data observability.

### Watermark defaults are dangerous

Several tutorials and blog posts suggest starting with a watermark delay of "10 minutes" or "1 hour" without context. These defaults are dangerous because they embed assumptions about source behavior that may not hold. A 10-minute watermark on a Kafka topic with <1 second out-of-orderness wastes 10 minutes of latency. A 10-minute watermark on a mobile app source with 30-minute network delays silently drops 20+ minutes of data. The correct approach is to measure actual out-of-orderness distributions from production data before setting watermark delays, then monitor dropped-record counts to validate the configuration [4][9].

### Flink 2.0 state incompatibility is a real migration risk

Flink 2.0 does NOT guarantee state compatibility with Flink 1.x [12]. This means existing Flink 1.x jobs cannot be upgraded to 2.0 with state continuity — they must be drained, migrated, and restarted with fresh state. For stateful jobs with large state (hundreds of GB to TB), this is a multi-hour production event with data reprocessing implications. The performance gains from ForSt are real (94% checkpoint duration reduction, 49x faster recovery) but the migration path is disruptive. Teams should plan 2.0 migration as a major operational event, not a routine upgrade.

### Exactly-once is achievable but not automatic in any engine

All three engines can achieve exactly-once end-to-end semantics, but none do so automatically. Spark requires replayable sources AND idempotent sinks — and `foreachBatch` (the most flexible sink API) only provides at-least-once [16]. Flink requires careful checkpoint configuration and external system integration (2-phase commit for Kafka sinks). DLT provides exactly-once within Delta Lake but the guarantee extends only as far as the Delta table — downstream consumers must handle their own deduplication. The claim "exactly-once" should always be qualified with the scope of the guarantee.

### Backpressure handling is Flink's architectural advantage

Flink handles backpressure automatically through credit-based flow control at the network level [14]. Spark's micro-batch model handles backpressure implicitly (batches accumulate), but this is not true flow control — it simply delays processing. RTM's backpressure behavior is not documented [5]. The practical difference: in Flink, a slow sink causes automatic producer throttling with no data loss. In Spark micro-batch, a slow sink causes batch durations to increase until they exceed the trigger interval, at which point latency degrades continuously. This is a fundamental architectural difference, not a tuning matter.

---

## Findings

### Finding 1: Flink is the superior choice for complex stateful streaming with event-time semantics
**Confidence: HIGH**

Flink's architecture — true per-record processing, native state primitives (ValueState, ListState, MapState), event-time watermarks with idle source handling and alignment, credit-based backpressure, fine-grained recovery, and Chandy-Lamport exactly-once checkpointing — makes it the strongest engine for complex streaming workloads requiring sub-second latency, sophisticated windowing (including session windows), and stateful pattern detection. Spark's state management is "limited" and "experimental" by comparison [13]. The operational cost of running a Flink cluster is justified when the use case demands these capabilities. For simple ETL-style streaming, Spark micro-batch is simpler and sufficient.

### Finding 2: Spark RTM narrows the latency gap but does not close the capability gap
**Confidence: HIGH**

Spark 4.1 RTM achieves single-digit millisecond p99 latency for stateless workloads on Databricks [5], making "Flink for low latency" a less universal recommendation. However, RTM restricts sources (Kafka/Event Hubs only), sinks (Kafka/foreachWriter only), output modes (update only), and excludes session windows, stream-stream joins, and forEachBatch [5]. It requires Databricks Runtime 16.4+, dedicated non-autoscaling clusters, and manual enablement. RTM is best suited for teams already on Databricks who need millisecond latency for simple Kafka-to-Kafka transformations. For anything more complex, Flink remains the better engine.

### Finding 3: Watermarking must be configured based on measured source behavior, not defaults
**Confidence: HIGH**

Watermark delay is a precision-vs-latency tradeoff with no universal default [4][9]. Too small and late data is silently dropped. Too large and results are delayed unnecessarily. The correct approach: measure the p99 out-of-orderness from production data, set the watermark delay to 2-3x that value, and monitor dropped-record counts. Flink's side output mechanism for late data is architecturally superior to Spark's "might be processed" soft guarantee [9]. For multi-source pipelines, idle source detection (`withIdleness`) and watermark alignment (`withWatermarkAlignment`) are essential to prevent watermark stalls [9].

### Finding 4: Backpressure is the most critical operational signal for streaming pipelines
**Confidence: HIGH**

Backpressure detection and resolution is the single most important operational capability for streaming pipelines. In Flink, the bottleneck is found by locating the first non-backpressured operator with `busyTimeMsPerSecond > 900` [11][15]. In Spark micro-batch, the signal is batch processing duration exceeding the trigger interval. Flink's credit-based flow control propagates backpressure automatically without data loss [14]. Kafka's decoupled architecture surfaces backpressure as consumer lag rather than direct flow control [14]. Monitor consumer lag patterns: linear growth means sustained mismatch, spike-and-recovery means transient burst, exponential growth means cascading failure requiring immediate intervention.

### Finding 5: DLT provides the fastest path to production streaming on Databricks at the cost of portability and control
**Confidence: MODERATE**

DLT's declarative model — streaming tables, materialized views, expectations, autoscaling, built-in monitoring — reduces the engineering effort to deploy streaming pipelines on Databricks. Expectations provide inline data quality constraints that are operationally useful for catching record-level issues. However, DLT locks teams into Databricks (no open-source equivalent), provides less control over processing semantics than raw Structured Streaming or Flink, lacks a local testing story (pipelines must deploy to a workspace), and expectations cannot detect distributional or volumetric anomalies. Teams choosing DLT should understand they are trading control and portability for operational simplicity.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Spark Structured Streaming micro-batch latency floor is ~1 second (trigger interval) | [1][13] | verified | Confirmed by Spark docs and independent comparison |
| 2 | Spark RTM achieves single-digit millisecond p99 e2e latency for stateless workloads | [5] | verified | Databricks docs; confirmed by StreamingQueryProgress metrics showing P99: 4ms |
| 3 | RTM does not support session windows or stream-stream joins | [5] | verified | Explicit in Databricks documentation limitations section |
| 4 | Flink exactly-once uses Chandy-Lamport distributed snapshots with barrier alignment | [8] | verified | Core Flink documentation; algorithm well-established in distributed systems literature |
| 5 | Flink 2.0 ForSt reduces checkpoint duration by up to 94% and recovery by 49x | [12] | verified | Official Flink 2.0 release announcement; benchmarked on Nexmark |
| 6 | Flink 2.0 does NOT guarantee state compatibility with Flink 1.x | [12] | verified | Explicit in release notes: DataSet API removed, state migration not guaranteed |
| 7 | Spark foreachBatch provides only at-least-once delivery, not exactly-once | [16] | verified | Confirmed by Spark documentation and practitioner analysis |
| 8 | DLT expectations enforce record-level quality constraints (expect, expect-or-drop, expect-or-fail) | [7] | verified | Databricks documentation; three enforcement modes confirmed |
| 9 | Flink backpressure bottleneck is the first non-backpressured operator with high busyTimeMsPerSecond | [11][15] | verified | Official Flink monitoring docs and practitioner guide |
| 10 | Watermark in Spark is a guarantee about what WILL be processed, not a hard cutoff for what will NOT | [4] | verified | Databricks docs: late records "might still be processed but this isn't guaranteed" |
| 11 | Flink credit-based flow control grants one credit per available network buffer | [14] | verified | Documented Flink network stack mechanism |
| 12 | Spark RTM requires Databricks Runtime 16.4+, dedicated non-autoscaling clusters | [5] | verified | Explicit prerequisites in Databricks documentation |
| 13 | Flink's withIdleness prevents idle sources from stalling global watermark progress | [9] | verified | Official Flink watermark generation documentation |
| 14 | Checkpoint duration is a leading indicator of streaming pipeline problems | [15] | verified | Increasing checkpoint times predict failures before they occur |
| 15 | Consumer lag exceeding Kafka topic retention causes permanent data loss | [14] | verified | Records purged before consumption cannot be recovered |
