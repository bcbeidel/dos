---
name: Right-to-Erasure Implementation
description: "Multi-step physical deletion in Delta Lake and Iceberg — logical delete alone does not satisfy GDPR; propagation through medallion layers, streaming table workarounds, and the append-only problem"
type: context
related:
  - docs/research/2026-03-22-privacy-engineering.research.md
  - docs/context/privacy-regulatory-requirements.md
  - docs/context/data-masking-tokenization.md
  - docs/context/medallion-architecture.md
  - docs/context/open-table-formats.md
  - docs/context/iceberg-cross-platform-compatibility.md
---

## Key Takeaway

Running a DELETE statement is not GDPR-compliant erasure. Both Delta Lake and Iceberg use deletion vectors that mark rows as deleted in metadata but leave original data in Parquet files. Physical removal requires a multi-step process (DELETE + physical purge + history cleanup) propagated through every medallion layer. Plain append-only storage (Parquet on S3/GCS without a table format) cannot support right-to-erasure at scale — transactional table formats are prerequisites.

## The Append-Only Problem

Traditional data lakes built on immutable file systems cannot easily delete a single row from a multi-row Parquet file — doing so requires rewriting the entire file. This is why transactional table formats (Delta Lake, Iceberg) are prerequisites for GDPR compliance in data lakes. Without them, erasure at scale is operationally infeasible.

## Delta Lake: Three-Step Erasure

**Step 1 — Logical delete:**

```sql
-- Single record
DELETE FROM bronze.users WHERE user_id = 5;

-- Bulk deletion via control table (recommended)
MERGE INTO target
USING (SELECT user_id FROM gdpr_control_table) AS source
ON target.user_id = source.user_id
WHEN MATCHED THEN DELETE;
```

The MERGE approach is recommended for processing batches of deletion requests from a control table that tracks GDPR/CCPA requests.

**Step 2 — Physical purge (for tables with deletion vectors):**

```sql
REORG TABLE target APPLY (PURGE);
```

Deletion vectors mark rows as deleted in metadata without rewriting data files. This is efficient for writes but does not satisfy GDPR — the original data remains in Parquet files. REORG TABLE APPLY PURGE rewrites files to physically remove deleted rows.

**Step 3 — Remove historical versions:**

```sql
VACUUM target;
```

Delta Lake retains table history for 30 days by default (enabling time travel). VACUUM removes files no longer referenced by the current version. The 30-day default is defensible under GDPR's "without undue delay" standard but must be documented and justified.

## Apache Iceberg: Deletion Vectors and Compaction

Iceberg V3 introduces deletion vectors stored as Roaring Bitmaps in Puffin sidecar files:

- **Merge-on-Read (MoR)** — Deletions recorded in sidecar files. Query engines filter deleted rows at read time. Write performance is excellent; read performance degrades as delete files accumulate.
- **Compaction** — Periodic jobs merge delete files and rewrite data files to physically remove deleted rows. This is the equivalent of Delta Lake's REORG + VACUUM.

Both Delta Lake and Iceberg now use Roaring Bitmaps for deletion vectors. Key architectural difference: Delta Lake offers both Copy-on-Write and Merge-on-Read, while Iceberg V3 standardizes on Merge-on-Read with mandatory compaction.

Performance reference: Apple reported maintenance operations reduced from approximately two hours to several minutes after migrating to Iceberg with deletion vectors. Airbnb achieved 50% reduction in compute resources and 40% decrease in job elapsed time.

## Propagation Through Medallion Layers

Deletion must propagate through every layer — bronze, silver, and gold:

- **Bronze (raw)** — Direct DELETE or MERGE against tables containing PII. Start here, driven by a scheduled job querying the deletion request control table.
- **Silver/Gold via materialized views** — Materialized views automatically handle source deletions upon refresh. No special handling needed, but the refresh and maintenance must actually run.
- **Silver/Gold via streaming tables** — Streaming tables can only process append queries. Deleting from a source table used for streaming breaks the stream. Workaround: add `skipChangeCommits` option to ignore non-append operations, then handle deletions separately.

## Implementation Checklist

1. **Deletion request control table** — Central table tracking incoming GDPR/CCPA requests with user identifiers, request timestamps, and processing status.
2. **Scheduled propagation job** — Runs against the control table, executes DELETE/MERGE across all layers, then runs physical purge and history cleanup.
3. **Verification step** — Confirm physical files no longer contain deleted data after purge completes.
4. **Streaming table handling** — Identify any streaming tables consuming from affected sources and implement separate deletion logic with `skipChangeCommits`.
5. **Document retention windows** — The gap between logical delete and physical removal (up to 30 days for Delta Lake default VACUUM) must be documented for compliance.
6. **Auto-TTL consideration** — Databricks Auto-TTL (currently Private Preview) makes retention a table-level property with automatic enforcement, eliminating custom retention jobs.

## What Teams Get Wrong

Teams that run only a DELETE and declare compliance are wrong. The four-step process is: logical delete, physical purge, history cleanup, propagation to every downstream table. Skipping any step leaves personal data accessible in storage. The most common failure is step 4 — deleting from bronze but leaving derived data intact in silver and gold layers.
