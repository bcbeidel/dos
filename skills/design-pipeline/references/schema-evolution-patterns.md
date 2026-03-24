# Schema Evolution Patterns

Plan for schema evolution before the first production deploy. The expand-and-contract pattern is sound but has practical gaps: dbt cannot track nested column changes or backfill new columns, and Delta Lake schema updates terminate active streams.

## Change Compatibility

| Change Type | Forward-Compatible | Backward-Compatible | Breaking? |
|---|---|---|---|
| Add optional column | Yes | Yes | No |
| Add required column | Yes | No | Yes |
| Drop optional column | Yes | Yes | No |
| Drop required column | No | Yes | Yes |
| Rename column | No | No | Yes |
| Widen type (int to long) | No | Yes | Depends |
| Narrow type (long to int) | Yes | No | Yes |
| Swap type (double to enum) | No | No | Yes |

**Non-breaking:** Adding optional fields with defaults, adding new enum values tolerated by consumers, extending nested structures with optional attributes.

**Breaking:** Removing required fields, tightening nullability, changing data types incompatibly, renaming fields without aliases.

## Expand-and-Contract Pattern

Zero-downtime migration in five steps:

1. **Expand** -- Add new fields as nullable/optional with defaults. Keep old fields.
2. **Backfill** -- Populate new fields for historical data. Run idempotent backfills.
3. **Dual-read/write** -- Producers write both old and new fields during transition.
4. **Cutover** -- Migrate consumers to new fields. Turn off dual-writes at 100% adoption.
5. **Contract** -- Deprecate and remove old fields after a safe window.

**Practical risk:** Requires minimum three production deployments per field rename. The "contract" phase commonly stalls, leaving deprecated fields indefinitely.

## Tool-Specific Behavior

### dbt (`on_schema_change`)

| Mode | Behavior |
|---|---|
| `ignore` (default) | New columns silently dropped, removed columns cause failures |
| `fail` | Error on any schema divergence |
| `append_new_columns` | Adds new columns, keeps removed columns |
| `sync_all_columns` | Adds new, removes old, handles type changes |

**Gaps:** Does not track nested column changes. None of the modes backfill new columns in existing rows. Manual updates or `--full-refresh` required for backfill.

### dlt

Auto-detects new columns. Creates variant columns for type changes (`column_name__v_datatype`). Four contract modes: `evolve` (default, no constraints), `freeze` (exception on non-conforming), `discard_row` (drops non-matching rows), `discard_value` (drops non-matching values).

### Delta Lake

Supports ADD, RENAME, DROP COLUMN. Automatic evolution via `MERGE WITH SCHEMA EVOLUTION`. Schema updates conflict with concurrent writes and terminate active streams. DROP COLUMN is metadata-only -- physical purge requires REORG TABLE + VACUUM.

## Decision Rules

1. Choose contract strictness at project start. Default `evolve` for dev, tighten to `freeze` or `discard_row` for production.
2. Treat all renames as breaking changes. Use expand-and-contract.
3. Add fields as optional with defaults. Never flip nullability in one shot.
4. Version schemas visibly -- include version field in messages, store schemas with changelogs.
5. Monitor for schema drift: contract checks and schema diffs on new batches.
