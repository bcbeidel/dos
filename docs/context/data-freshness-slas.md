---
name: Data Freshness SLAs
description: "Five SLA dimensions (timeliness, completeness, accuracy, consistency, availability) with error budgets; dbt source freshness is NOT run by dbt build (critical gap); Dagster freshness policies provide continuous evaluation; start with timeliness and completeness for highest signal"
type: context
related:
  - docs/research/2026-03-22-operations-reliability.research.md
  - docs/context/data-observability-pillars.md
  - docs/context/retry-failure-patterns.md
---

## Key Takeaway

Data SLAs are not aspirational -- they require explicit definition, instrumentation, and enforcement. The most common failure is not defining them at all, then discovering during an incident that no one agreed on what "fresh" means. Start with timeliness and completeness. Wire `dbt source freshness` into the orchestrator as a separate step -- it is not included in `dbt build`, and this gap catches teams during their first stale-data incident.

## Five SLA Dimensions

1. **Timeliness** -- Data arrives within agreed time windows. Measured by freshness thresholds on destination tables.
2. **Completeness** -- Expected records are present. Measured by volume checks and row count comparisons.
3. **Accuracy** -- Values are correct. Measured by distribution checks, cross-referencing, and domain-specific validation.
4. **Consistency** -- Data agrees across systems. Measured by reconciliation checks between source and destination.
5. **Availability** -- Data is accessible when needed. Measured by uptime of query endpoints and dashboards.

Most teams lack instrumentation for all five. Start with timeliness (freshness) and completeness (volume) -- they provide the highest signal-to-investment ratio. Accuracy and consistency require domain-specific validation that cannot be generalized.

## SLAs vs SLOs vs SLIs

- **SLIs** (Service Level Indicators) -- the measured metrics. Example: "Freshness of the orders table measured every hour."
- **SLOs** (Service Level Objectives) -- internal targets, typically stricter than SLAs. Example: "99.5% of tables refreshed within 2 hours."
- **SLAs** (Service Level Agreements) -- contractual commitments with consequences. Example: "Dashboard data will be no more than 4 hours stale."
- **Error budgets** -- acceptable violation rates. "99.5% compliance" allows approximately 3.6 hours of cumulative violation per month.

## dbt Source Freshness

dbt defines freshness at the source level using `warn_after` and `error_after` thresholds with a `loaded_at_field` column:

```yaml
sources:
  - name: raw
    tables:
      - name: orders
        loaded_at_field: _loaded_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

The `dbt source freshness` command evaluates sources against thresholds and returns nonzero on staleness.

**Critical operational gap:** `dbt source freshness` is NOT included in `dbt build`. This is by design -- freshness checking queries the source database, which may be a production OLTP system where additional queries have cost and performance implications. But teams who follow tutorials and run `dbt build` in their orchestrator believe they have freshness monitoring when they do not. Wire freshness as a pre-check step in the orchestrator and fail the pipeline before running transformations on stale data.

## Dagster Freshness Policies

Two policy types, evaluated continuously:

1. **time_window** -- `fail_window` and `warn_window` define staleness thresholds (e.g., fail if not materialized in 24h, warn at 12h).
2. **cron** -- `deadline` and `lower_bound_delta` define expected schedule (e.g., "must be materialized by 8am daily using data from the last 24h").

Policies surface in the Dagster UI as asset health indicators and can be batch-applied via `map_asset_specs()`. Not supported for `SourceAssets` or `CacheableAssetsDefinition`.

## Freshness Metrics

Two metrics to track over time:

1. **Freshness SLA compliance %** -- Percentage of measurement windows where data met the freshness threshold.
2. **Staleness ratio** -- Ratio of stale tables to total tables. Track trends to catch systemic degradation.

ML-based anomaly detection supplements threshold-based checks by learning expected arrival patterns -- useful when data arrives at irregular but predictable intervals (e.g., partner feeds that arrive between 2am-6am).

## Decision Rules

1. Define freshness and completeness SLAs before the first production deploy. Do not wait for the first incident.
2. Wire `dbt source freshness` as a separate orchestrator step before `dbt build`. Always.
3. Set `warn_after` and `error_after` thresholds that match downstream consumer expectations.
4. Use error budgets to make SLA conversations concrete. "99.5% compliance" is actionable; "data should be fresh" is not.
5. Track freshness SLA compliance % and staleness ratio as operational KPIs.
