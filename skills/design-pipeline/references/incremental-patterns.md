# Incremental Loading Patterns

Match your incremental strategy to source data characteristics, not tool defaults. The core tradeoff: simpler systems with higher load costs vs. more complex systems with lower load costs. Full refresh is correct more often than engineers assume.

## The Five Patterns

**Full Refresh.** Rebuild the entire table every run. Use when: dataset is small (under a few GB), source lacks reliable change tracking, simplicity matters. Implementation: `CREATE OR REPLACE` over a `SELECT`.

**Append.** Insert new records without touching existing data. Use for: immutable event data (logs, clicks, transactions). Does not check for duplicates -- repeated source records create duplicate rows.

**Merge/Upsert.** Insert new records, update existing ones by key. Use for: stateful records (user profiles, inventory). Warning: scans entire destination table without partition pruning. Delta Lake requires single source row per target key.

**Delete+Insert.** Delete matching records, then insert replacements within a single transaction. Use for: atomicity when unique_key is not truly unique, or when merge is unsupported. Clean idempotency.

**Microbatch.** Split time-series data into independent, bounded time periods. Each batch is idempotent, can execute concurrently, retry individually, and backfill via date range flags. Use for: large time-series datasets.

## Selection Framework

| Source Characteristic | Recommended Pattern |
|---|---|
| Small dataset, no change tracking | Full refresh |
| Immutable events (logs, clicks) | Append |
| Stateful records with updates | Merge/Upsert |
| Need atomicity, non-unique keys | Delete+Insert |
| Large time-series data | Microbatch |

Stateless data (recorded events) maps to append. Stateful data (user profiles, dimensions) requires merge or SCD2. Late-arriving records need lookback windows.

## Silent Failure Modes

These are under-documented and represent the biggest risk with incremental loading:

| Failure Mode | Description | Affected Patterns |
|---|---|---|
| Missed gaps | Timestamp cursors check only the latest value, missing gaps in the middle | Append, Merge |
| Duplicate accumulation | Late-arriving data creates duplicates without output-range filtering | Append |
| Full-table scans | MERGE without partition pruning scans entire destination table | Merge/Upsert |
| Non-replayable sources | API rate limits, deleted records, or ephemeral streams make re-extraction impossible | All incremental |

## Idempotency Strategies

Every pipeline must produce the same result if re-executed. Three strategies:

| Strategy | Mechanism |
|---|---|
| DELETE+INSERT | Remove existing data for a time period, insert fresh data within transaction boundaries |
| MERGE/UPSERT | Update existing records or insert new ones based on key |
| Immutable append + dedup | Append with processing timestamps, deduplicate at read time using window functions |

**Backfill by design:** Every pipeline should accept a date parameter and process exactly that date's data. Parameterized date ranges, partition-aware processing, pre/post validation (row counts, checksums).

## Tool Support

**dbt:** All five strategies (append, delete+insert, merge, insert_overwrite, microbatch). Platform support varies for insert_overwrite and microbatch.

**dlt:** Three write dispositions (replace, append, merge) with four merge strategies: delete-insert (default, atomic), upsert (database-native), SCD2 (historical tracking), insert-only (immutable data).

**Delta Lake MERGE:** WHEN MATCHED (update/delete), WHEN NOT MATCHED (insert), WHEN NOT MATCHED BY SOURCE (cleanup). Native SCD Type 1 and Type 2 via Lakeflow Spark APIs.
