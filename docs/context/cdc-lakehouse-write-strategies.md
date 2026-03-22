---
name: CDC Lakehouse Write Strategies
description: "CDC into Delta Lake uses MERGE INTO (copy-on-write, read-optimized but write-amplified); Iceberg uses merge-on-read with delete files (write-optimized but requires compaction); Iceberg V3 deletion vectors reduce overhead; strategy choice depends on read-heavy vs write-heavy workload profile"
type: context
related:
  - docs/research/2026-03-22-cdc-event-driven-ingestion.research.md
  - docs/context/cdc-mechanisms-tooling.md
  - docs/context/kafka-event-streaming-patterns.md
  - docs/context/open-table-formats.md
  - docs/context/iceberg-cross-platform-compatibility.md
  - docs/context/incremental-loading-patterns.md
---

## Key Insight

Delta Lake and Iceberg use fundamentally different strategies for applying CDC changes. Delta Lake's MERGE INTO is copy-on-write (expensive writes, cheap reads). Iceberg's merge-on-read uses delete files (cheap writes, reads degrade without compaction). Neither is universally superior -- the choice depends on the workload's read/write ratio.

## Delta Lake: MERGE INTO (Copy-on-Write)

Delta Lake applies CDC changes via MERGE INTO:

1. Identify target files containing matching rows (using data-skipping statistics and partition pruning)
2. Read those files and join against the incoming CDC batch
3. Rewrite matched files with the merged result
4. Commit the new file set atomically via the transaction log

This is write-amplified by nature: updating 10 rows scattered across 10 Parquet files means rewriting all 10 files. But reads are fast because data is pre-merged -- queries never need to reconcile separate delete records at read time.

Delta Lake 3.0 improved MERGE performance by up to 56%. The degree of write amplification is workload-dependent: if CDC updates concentrate in recent partitions (common for time-series data), partitioning by date restricts the merge surface to a small number of files. For entity tables where updates touch any partition, amplification remains significant.

**Streaming CDC pattern:** Spark Structured Streaming with `foreachBatch` applies MERGE against incoming CDC micro-batches. Partition by date and restrict the merge condition to recent partitions. High-frequency micro-batch MERGE creates many small files -- periodic OPTIMIZE (compaction) and ZORDER (clustering) are required.

**Databricks AUTO CDC:** The `APPLY CHANGES INTO` API automatically merges CDC events, handling out-of-order data and SCD2 semantics without manual MERGE statements.

## Iceberg: Merge-on-Read with Compaction

Iceberg takes the opposite approach. Instead of rewriting data files on every update, it writes small delete files that mark which rows in existing data files are invalidated. At read time, the engine merges delete files with data files to produce correct results.

Write latency stays low. The cost shifts to reads: queries must scan both data files and delete files, filtering out invalidated rows. Without compaction, read performance degrades non-linearly as delete files accumulate.

**Compaction is not optional.** For CDC tables: compact at least daily, with `delete-file-threshold` set to trigger earlier when delete files pile up (50 is a common threshold). Pair with `rewrite_manifests`, `expire_snapshots`, and `remove_orphan_files` for complete maintenance. Teams adopting Iceberg for CDC must budget for compaction infrastructure and monitoring as a first-class operational concern.

**Iceberg V3 deletion vectors (2025):** Replace positional delete files with an efficient binary format stored as Puffin files. Deletion vectors consolidate references to a single vector per data file, reducing metadata overhead and improving read performance. They narrow the gap but do not eliminate the compaction requirement.

**Two ingestion patterns:**
1. **Direct materialization:** Flink CDC writes directly to final Iceberg tables, handling merge logic internally. Simpler to operate.
2. **Raw changelog + ETL:** Append all CDC events to a bronze table, then MERGE INTO a final mirror table. Preserves complete history and enables replay, but requires two tables and a merge pipeline.

## Strategy Comparison

| Aspect | Delta Lake (MERGE INTO) | Iceberg (Merge-on-Read) |
|--------|------------------------|------------------------|
| Write cost | High (file rewrite) | Low (small delete files) |
| Read cost | Low (pre-merged) | Higher (merge at read) |
| Compaction | OPTIMIZE for small files | Critical for delete files |
| Streaming | foreachBatch + MERGE | Flink CDC direct write |
| V3 improvements | -- | Deletion vectors reduce overhead |

## Takeaway

Read-heavy analytics workloads with moderate CDC frequency favor Delta Lake's pre-merged approach. Write-heavy CDC workloads with high change rates favor Iceberg's merge-on-read with scheduled compaction. Iceberg V3 narrows the gap but compaction remains a hard operational requirement. Match the write strategy to the target format's strengths -- do not force one format's pattern onto the other.
