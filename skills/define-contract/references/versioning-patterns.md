# Versioning Patterns

Contract versioning follows semantic versioning with the expand-contract pattern for breaking changes. SemVer covers structural changes but not behavioral changes -- a shift in data distribution or freshness can equally break downstream consumers.

## Semantic Versioning Rules

| Bump | When | Examples |
|------|------|----------|
| **MAJOR** | Breaking changes | Remove column, change type incompatibly, tighten nullability, rename field |
| **MINOR** | Backward-compatible additions | Add optional column with default, add new quality check, add new enum value |
| **PATCH** | Non-functional changes | Documentation updates, metadata corrections, comment changes |

Extend SemVer with behavioral dimensions: SLA changes and quality metric shifts should also trigger version bumps (SLA tightening = MINOR, SLA relaxation = MAJOR from consumer perspective).

## Breaking vs Additive Change Classification

| Change Type | Breaking? | Forward-Compatible | Backward-Compatible |
|---|---|---|---|
| Add optional column | No | Yes | Yes |
| Add required column | Yes | Yes | No |
| Drop optional column | Depends | Yes | Yes |
| Drop required column | Yes | No | Yes |
| Rename column | Yes | No | No |
| Widen type (int -> long) | No | No | Yes |
| Narrow type (long -> int) | Yes | Yes | No |
| Swap type (double -> enum) | Yes | No | No |

**Non-breaking:** Adding optional fields with defaults, adding new tolerated enum values, extending nested structures with optional attributes.

**Breaking:** Removing required fields, tightening nullability, changing data types incompatibly, renaming fields without aliases.

## Expand-Contract Pattern

The standard zero-downtime migration for unavoidable breaking changes:

| Phase | Action | Consumer Impact |
|-------|--------|-----------------|
| **1. Expand** | Add new elements alongside existing ones. Producers write both old and new fields. | None -- old consumers unaffected |
| **2. Migrate** | Update consumers to use new elements. Both versions active. Monitor adoption. | Consumers migrate at their own pace |
| **3. Contract** | Remove old elements once all consumers have migrated. Deprecation date enforced. | Old consumers must have migrated |

**dbt implementation:** Create model `v2`, set `latest_version`, define `deprecation_date` on `v1`. Consumers migrate from `ref('model', v=1)` to `ref('model')`. Recommended cadence: version bumps once or twice a year.

**Practical problems:** Requires minimum three production deployments per field rename. The "contract" phase commonly stalls, leaving deprecated fields indefinitely -- a frequent source of schema bloat.

## Compatibility Modes

| Mode | Direction | Upgrade Order | Best For |
|------|-----------|---------------|----------|
| **BACKWARD** (default) | New schema reads old data | Consumers first | Data warehousing, topic rewind |
| **FORWARD** | Old schema reads new data | Producers first | Streaming with slow consumer upgrades |
| **FULL** | Both directions | Either | Most restrictive: only add/remove optional fields with defaults |
| **TRANSITIVE** variants | Checked against all previous versions | Varies | BACKWARD_TRANSITIVE essential for data warehousing |

## Decision Rules

1. Default to BACKWARD compatibility for batch/warehouse contracts.
2. Treat all renames as breaking changes regardless of tooling. Use expand-contract.
3. Add fields as optional with defaults. Never flip nullability in one shot.
4. Version schemas visibly -- include a version field in contracts, store in a repo with changelogs.
