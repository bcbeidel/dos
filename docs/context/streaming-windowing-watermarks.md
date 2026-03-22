---
name: Windowing and Watermarking Patterns
description: "Tumbling, sliding, and session window types with lifecycle mechanics; watermarking as a precision-vs-latency tradeoff; Flink's three-tier late data strategy vs Spark's probabilistic drop; practical watermark sizing guidance"
type: context
related:
  - docs/research/2026-03-22-stream-processing.research.md
  - docs/context/stream-processing-comparison.md
  - docs/context/streaming-observability-backpressure.md
  - docs/context/data-freshness-slas.md
---

## Key Insight

Watermarking is a precision-vs-latency tradeoff with no universal default. Larger delays capture more late data but increase result latency. The correct value depends on source-specific out-of-orderness characteristics -- measure actual late arrival distributions before configuring. Start with 2-3x the observed p99 out-of-orderness and adjust.

## Window Types

**Tumbling windows** -- fixed-size, non-overlapping, contiguous time intervals. Each event belongs to exactly one window. Simplest to implement, lowest state overhead. All engines support natively. Use case: minute-by-minute counts, hourly aggregation.

**Sliding (hopping) windows** -- fixed-size intervals that advance at a slide interval shorter than window size, creating overlap. A 10-minute window with 5-minute slide puts each event in two windows. Higher state cost: `window_size / slide_interval` windows overlap at any moment. Use case: moving averages.

**Session windows** -- activity-based windows defined by an inactivity timeout. Window starts on first event, extends with each subsequent event, closes after the timeout period with no events. Most complex: variable-size output, highest state overhead, hardest to parallelize. Flink and Spark micro-batch support them natively. Spark RTM does not support session windows.

## Window Lifecycle

Every window operation has three phases: **creation** (boundary established by first event or time alignment), **accumulation** (events assigned, state updated), and **trigger/eviction** (results emitted, state cleaned up per watermarks). Incorrect watermark configuration causes either premature eviction (incomplete results) or unbounded state growth (windows never close, eventual OOM).

## Watermarking in Spark

`withWatermark("event_time", "10 minutes")` declares events arriving more than 10 minutes after the latest observed event time may be dropped. The watermark controls state cleanup -- once the watermark passes a window's end time plus the delay, state for that window is purged. Without watermarks, state grows unboundedly.

For multiple input streams, two global watermark policies:
- **Min policy** (default) -- uses the slowest stream's watermark; safer but delays results
- **Max policy** -- uses the fastest stream's watermark; faster results but may drop data from slower streams

Late records outside the threshold "might still be processed but this isn't guaranteed." Watermarks guarantee what WILL be processed, not a hard cutoff for what WILL NOT.

## Watermarking in Flink

More granular than Spark. Watermark generators can be periodic (framework-timed via `onPeriodicEmit()`) or punctuated (reactive to marker events). Two built-in strategies cover most cases:

- **BoundedOutOfOrderness** -- watermark lags behind max observed timestamp by configured duration
- **MonotonousTimestamps** -- assumes strictly ascending timestamps (zero lag)

For multi-source pipelines, watermarks propagate using the minimum across all input partitions. An idle source stalls the entire pipeline's watermark progress -- use `withIdleness(Duration)` to mark inactive partitions as idle. Watermark alignment via `withWatermarkAlignment()` prevents fast sources from racing ahead.

## Flink's Three-Tier Late Data Strategy

Flink's side output mechanism is a critical architectural advantage over Spark's probabilistic drop:

1. **Within watermark** -- processed normally in the window
2. **Within allowed lateness** -- updates the window result
3. **Beyond allowed lateness** -- routed to a side output stream for separate handling

This means no late data is silently lost. Late records can be written to a dead letter topic, processed in a separate pipeline, or used for accuracy monitoring.

## Practical Guidance

Start with a watermark delay of 2-3x the observed p99 out-of-orderness, then adjust. Monitor the gap between watermark time and wall-clock time -- a growing gap means the pipeline is falling behind. Track the count of late-arriving records dropped by the watermark to detect whether the configured delay is sufficient. Mobile/IoT sources typically need minutes of delay; well-ordered Kafka partitions may need near-zero.
