---
name: Incremental Loading Patterns
description: Five incremental loading strategies (full refresh, append, merge, delete+insert, microbatch), selection criteria, silent failure modes, and idempotency requirements
type: context
related:
  - docs/research/2026-03-21-pipeline-design-architecture.research.md
  - docs/context/medallion-architecture.md
  - docs/context/query-storage-cost-optimization.md
---

## Key Takeaway

Match your incremental strategy to source data characteristics, not tool defaults. The core tradeoff is "simpler systems and higher load costs vs. more complex systems and lower load costs." Full refresh is correct more often than engineers assume. Silent failures (missed gaps, duplicate accumulation) are the dominant risk -- monitor incremental correctness actively.

## The Five Patterns

**Full Refresh.** Rebuild the entire table every run. Use when: dataset is small (under a few GB), source lacks reliable change tracking, simplicity matters more than efficiency. Implementation is trivial: `CREATE OR REPLACE` over a `SELECT`.

**Append.** Insert new records without touching existing data. Use for: immutable event data (logs, clicks, transactions). Does not check for duplicates -- repeated source records create duplicate rows. Cheapest incremental strategy.

**Merge/Upsert.** Insert new records, update existing ones by key. Use for: stateful records (user profiles, inventory). Warning: "can be expensive for large tables because it scans the entire destination table." Delta Lake requires that only a single source row matches a given target row -- multiple matches cause failures. Always use partition pruning (e.g., 7-day window) to avoid full-table scans.

**Delete+Insert.** Delete matching records, then insert replacements within a single transaction. Use for: atomicity when unique_key is not truly unique, or when merge is unsupported. May be less efficient for large datasets but provides clean idempotency.

**Microbatch.** Split time-series data into independent, bounded time periods (default: one day). Each batch is idempotent and can execute concurrently, retry individually, and backfill via `--event-time-start/end` flags. Use for: large time-series datasets where you need efficient incremental processing with built-in backfill support.

## Selection Framework

| Source Characteristic | Recommended Pattern |
|---|---|
| Small dataset, no change tracking | Full refresh |
| Immutable events (logs, clicks) | Append |
| Stateful records with updates | Merge/Upsert |
| Need atomicity, non-unique keys | Delete+Insert |
| Large time-series data | Microbatch |

**Stateless data** (recorded events) maps to append. **Stateful data** (user profiles, dimensions) requires merge or SCD2. Late-arriving records need lookback windows -- "trading a little extra compute for a lot more reliability."

## Tool Support

**dbt:** Supports all five strategies (append, delete+insert, merge, insert_overwrite, microbatch) across major platforms. Platform support varies for insert_overwrite and microbatch.

**dlt:** Three write dispositions (replace, append, merge) with four merge strategies: delete-insert (default, atomic), upsert (database-native, lower overhead), SCD2 (historical tracking), insert-only (maximum performance for immutable data). Supports hard deletes via Boolean column hint.

**Delta Lake MERGE:** Supports WHEN MATCHED (update/delete), WHEN NOT MATCHED (insert), and WHEN NOT MATCHED BY SOURCE (cleanup). Native SCD Type 1 and Type 2 via Lakeflow Spark APIs.

## Silent Failure Modes

These are under-documented and represent the biggest risk with incremental loading:

- **Missed gaps:** Timestamp-based cursors check only the latest value, missing gaps in the middle or beginning of tables
- **Duplicate accumulation:** Late-arriving data (e.g., offline-synced mobile sessions) creates duplicates without explicit output-range filtering
- **Full-table scans:** MERGE operations without partition pruning scan entire destination tables, degrading performance silently
- **Non-replayable sources:** API rate limits, deleted records, or ephemeral streams make source data unavailable for re-extraction

## Idempotency Rules

Every pipeline must be idempotent -- running it multiple times produces the same result as running once. Three strategies:

1. **DELETE+INSERT:** Remove existing data for a time period, insert fresh data within transaction boundaries
2. **MERGE/UPSERT:** Update existing records or insert new ones based on key
3. **Immutable append with deduplication:** Append with processing timestamps, deduplicate at read time using window functions

Every pipeline should accept a date parameter and process exactly that date's data. Design for backfill from day one: parameterized date ranges, partition-aware processing, pre/post validation (row counts, checksums).
