# dlt Pipeline Patterns

## CDC Boundary

dlt is a polling/extraction tool, NOT CDC. It does not read transaction logs.

| Need | Tool | Mechanism |
|------|------|-----------|
| Log-based change capture (sub-second, captures deletes) | Debezium on Kafka Connect | Reads WAL/binlog |
| API extraction, file-based sources | dlt | Polling with cursor-based state |
| Database polling (incremental) | dlt | Timestamp/cursor-based merge |

If the source evaluation recommends CDC, do not use dlt. Guide the user to Debezium or platform-native CDC.

## Write Dispositions

| Disposition | Behavior | Use When | Risk |
|-------------|----------|----------|------|
| `replace` | Truncate + load | Full refresh, small datasets | **Truncates before loading** — empty/partial tables on failure. Recommend staging with atomic swap where supported. |
| `append` | Insert only | Immutable events (logs, clicks) | Duplicate accumulation if source replays events. No dedup. |
| `merge` | Upsert by key | Stateful records with updates | Full-table scan without partition pruning. ClickHouse lacks upsert — use `delete-insert` strategy instead. |

## Merge Strategies

| Strategy | Behavior | Platform Support |
|----------|----------|-----------------|
| `delete-insert` | Delete matching rows, insert replacements (default) | All platforms |
| `upsert` | Database-native upsert, lower overhead | DuckDB, Snowflake, Databricks — **not ClickHouse** |
| `scd2` | Historical tracking with valid_from/valid_to | All platforms |
| `insert-only` | Maximum performance for immutable data | All platforms |

Hard deletes supported via Boolean column hint (`x-delete`).

## Incremental Loading Configuration

```python
@dlt.resource(write_disposition="merge", merge_key="id")
def my_resource():
    # Cursor-based incremental
    yield dlt.sources.incremental("updated_at", initial_value="2024-01-01")
```

- **Cursor field**: Column used for change detection (e.g., `updated_at`)
- **Merge key**: Column(s) for identifying existing records (e.g., `id`)
- **Initial value**: Starting point for first run

## Known Pitfalls

### Bug #2782: Config/secrets confusion
`dlt.config.get()` reads from `secrets.toml` instead of `config.toml`. Test config/secrets separation explicitly — values may silently load from the wrong file.

### Silent env var failures
Double-underscore nesting errors in env var names produce no warning. dlt silently falls back to TOML values. Example: `SOURCES__MY_SOURCE__API_KEY` must match the exact nesting structure.

### Silent destination fallback
Misnamed destinations silently fall back to shorthand type string. A typo in `destination="snowflke"` does not error — it creates an unexpected destination configuration.

### Nested data divergence at max_table_nesting=0

| Platform | Behavior |
|----------|----------|
| DuckDB | Native JSON column, queryable |
| Snowflake | VARIANT column — becomes string via Parquet |
| Databricks | JSON not supported via JSONL at all |
| ClickHouse | String column, no JSON querying |

Test nested data handling on each target platform. DuckDB local behavior does not transfer.

## Type Fidelity Warnings

| dlt Type | Degrades On | Result |
|----------|-------------|--------|
| `json` | ClickHouse | String (no native querying) |
| `time` | ClickHouse | String |
| `binary` | ClickHouse | String (base64) |
| `json`, `decimal` | Databricks via JSONL | Not supported — use Parquet |

## Schema Evolution

dlt does not alter columns in place on type change. It creates a versioned column (e.g., `inventory_nr__v_text`). On ClickHouse, sorting and partition keys are immutable after table creation.

## Cost-Aware Retry Configuration

| Retry Type | Behavior | Cost Impact |
|------------|----------|-------------|
| Full-state retry (`max_retries` on job) | Replays all API calls from scratch | Multiplies total API cost per retry |
| Checkpoint retry (dlt incremental cursor) | Resumes from last successful cursor | Only replays failed segment |
| Idempotent retry (request-level) | Re-requests same data | Depends on API billing model |

Cost calculation:

```
retry_cost = api_calls_per_run × overage_price_per_call
```

Decision rule:
- If `retry_cost > $10`: present cost tradeoff to user before recommending `max_retries > 0`
- If source is not quota-billed: standard retry guidance applies
- Prefer checkpoint retry over full-state retry for any quota-billed API

Cross-reference: See `extraction-boundary-rules.md` for the full cost-of-retry decision table.
