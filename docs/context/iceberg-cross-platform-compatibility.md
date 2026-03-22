---
name: "Iceberg Cross-Platform Compatibility"
description: "Platform support matrix, ClickHouse integration patterns, streaming write limitations, and mandatory maintenance for Iceberg in production"
type: context
related:
  - docs/context/open-table-formats.md
  - docs/context/iceberg-catalog-interoperability.md
  - docs/research/2026-03-22-open-table-formats.research.md
---

## Key Insight

Iceberg has production read/write support across every major analytical platform as of early 2026. The practical concerns are not whether engines support Iceberg, but how much slower it is than native formats, how to handle streaming write concurrency limits, and how to manage metadata overhead.

## Platform Support (Early 2026)

| Platform | Iceberg Read | Iceberg Write | Delta Lake Read | Delta Lake Write |
|----------|:---:|:---:|:---:|:---:|
| **Databricks** | Yes | Yes | Yes (native default) | Yes (native default) |
| **Snowflake** | Yes | Yes (GA Oct 2025) | Via UniForm only | No |
| **BigQuery** | Yes (managed) | Yes (BigLake) | Via UniForm only | No |
| **ClickHouse** | Yes | Yes (25.7+ beta) | Yes | Limited |
| **Trino** | Yes (v373+) | Yes (v373+) | Yes (v373+) | Yes (v373+) |
| **Spark** | Yes | Yes | Yes (default) | Yes (default) |
| **Flink** | Yes | Yes | Via connector | Limited |

Snowflake and BigQuery are Iceberg-first with no native Delta write support. Databricks supports both but defaults to Delta. Trino treats both formats equally.

## ClickHouse Integration

ClickHouse's native MergeTree is 2-3x faster than Iceberg queries and 100x+ faster for complex multi-column queries on S3. Iceberg write support shipped in beta across 25.7-25.10 (INSERT, CREATE TABLE, ALTER DELETE/UPDATE, distributed writes).

**Hot/cold tiering pattern (recommended):** Recent data goes into MergeTree tables (millisecond latency). Historical data stays in Iceberg on object storage. Cross-tier queries use UNION ALL views. Netflix processes 5 PB of logs daily at 10.6M events/sec using this pattern.

**Practical limitations:** No Iceberg v3 deletion vectors support. Type mismatches with unsigned integers and Nullable handling. Metadata can go stale when external writers update tables (configurable via `iceberg_metadata_staleness_ms`).

## Streaming Write Limitations

Iceberg is not a real-time store. The commit model serializes writes via optimistic concurrency, creating a practical ceiling of ~15 commits/min/table (Adobe production data). Fresh rows are invisible until Parquet upload completes and metadata swaps atomically.

**Mitigations:**
- **Centralized committer pattern:** Single-threaded service aggregates writes and commits at fixed intervals (e.g., every 5 seconds), avoiding metadata swap contention.
- **Fan-out to multiple tables** with UNION ALL views distributes commit pressure.
- **Recommended pipeline pattern:** Buffer in Kafka (Avro-serialized), micro-batch to Iceberg via Flink at 1-5 minute intervals, compact separately.

The Flink Dynamic Iceberg Sink (Iceberg 1.10.0+) enables multi-table routing with automatic schema evolution from Schema Registry and exactly-once semantics.

## Mandatory Maintenance

Iceberg metadata overhead is non-trivial and maintenance is not optional:

- **File size target:** 256-512 MB Parquet files. Files under 128 MB create excessive planning latency; over 1 GB reduces pruning effectiveness.
- **Compaction:** Reduces query costs by 30-40% on Athena/Trino. Must be scheduled separately from writes.
- **Snapshot expiration:** Recommended every 3-7 days. Without it, storage can bloat 5-200x from time travel retention.
- **Orphan file cleanup:** Prevents unreferenced data accumulation.
- **BigQuery managed Iceberg tables** handle compaction, clustering, and garbage collection automatically — the most operationally simple option at the cost of platform coupling.

## Performance Penalties

Iceberg queries are slower than native formats across engines: ClickHouse 2-3x (100x+ for complex queries), Snowflake ~20% penalty, general S3 latency from Parquet's metadata structure requiring multiple sequential HTTP range requests. These penalties are acceptable for interchange and historical data access. They are not acceptable for latency-sensitive hot-path queries.

## Takeaway

Iceberg works everywhere, but native formats remain faster. Design for tiered architecture: native format (MergeTree, Delta, BigQuery native) for performance-critical queries, Iceberg for cross-engine access and historical data. Budget for ongoing compaction, snapshot expiration, and file size management.
