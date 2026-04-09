---
name: "dbt Test Selection Patterns: Rule Type to Test Implementation Mapping"
description: "Comprehensive mapping from data quality rule types to correct dbt test implementations across dbt core, dbt_utils, dbt-expectations (Metaplane fork), and Elementary; expression_is_true is the correct test for string pattern rules (not not_accepted_values); run-over-run consistency checks require either Elementary anomaly detection tests, custom singular tests with a metrics log table, or dbt-expectations cross-table comparison tests -- dbt has no built-in stateful comparison mechanism"
type: research
sources:
  - https://docs.getdbt.com/docs/build/data-tests
  - https://docs.getdbt.com/reference/resource-properties/data-tests
  - https://docs.getdbt.com/reference/resource-configs/store_failures
  - https://docs.getdbt.com/reference/resource-configs/store_failures_as
  - https://docs.getdbt.com/best-practices/writing-custom-generic-tests
  - https://github.com/dbt-labs/dbt-utils
  - https://github.com/dbt-labs/dbt-utils/blob/main/macros/generic_tests/expression_is_true.sql
  - https://github.com/metaplane/dbt-expectations
  - https://hub.getdbt.com/metaplane/dbt_expectations/latest/
  - https://github.com/elementary-data/dbt-data-reliability
  - https://docs.elementary-data.com/data-tests/how-anomaly-detection-works
  - https://www.elementary-data.com/dbt-tests/volume-anomalies
  - https://www.elementary-data.com/dbt-tests/freshness-anomalies
  - https://www.elementary-data.com/dbt-tests/expression-is-true
  - https://github.com/dbt-labs/dbt-audit-helper
related:
  - docs/research/2026-03-22-validation-frameworks.research.md
  - docs/research/2026-03-22-quality-engineering.research.md
  - docs/context/data-validation-tool-comparison.md
  - docs/context/tiered-validation-strategy.md
  - skills/implement-models/references/dbt-testing-patterns.md
  - skills/assess-quality/references/validation-tiers.md
---

## Summary

**Research question:** What are the correct dbt test implementations for each type of data quality rule, including stateful/run-over-run patterns?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 15 | **Searches:** 12 across Google, GitHub, dbt docs

**Key findings:**

1. **Bug #31 root cause confirmed.** `dbt_utils.not_accepted_values` checks whether a column contains forbidden discrete values from a list. It is categorically wrong for string pattern matching (e.g., `LIKE 'GHCND:%'`). The correct test is `dbt_utils.expression_is_true` with the expression `LIKE 'GHCND:%'` applied at the column level, or `dbt_expectations.expect_column_values_to_match_like_pattern` for the declarative equivalent.

2. **Bug #15 root cause confirmed.** dbt has no built-in mechanism for stateful run-over-run comparison. The quality config skill defines run-over-run consistency checks but the implement-models skill has no pattern to generate them. Four implementation options exist, ranked by complexity and capability.

3. **Test selection is a function of rule semantics, not rule category.** The same "validity" dimension can require `accepted_values` (categorical), `expression_is_true` (pattern/range), or `expect_column_values_to_match_regex` (regex) depending on the constraint type. A mapping table keyed on rule semantics -- not quality dimension -- is required.

## Critical Distinction: expression_is_true Behavior

The `expression_is_true` macro has two modes depending on whether `column_name` is provided:

```sql
-- Without column_name (model-level test): standalone expression
WHERE NOT({{ expression }})

-- With column_name (column-level test): expression appended to column
WHERE NOT({{ column_name }} {{ expression }})
```

**When applied at the column level**, the expression is concatenated after the column name. So for a column `station_id`, an expression of `LIKE 'GHCND:%'` produces `WHERE NOT(station_id LIKE 'GHCND:%')`. This is the correct pattern for string prefix/pattern rules on a specific column.

**When applied at the model level** (without column_name), the expression must be a complete SQL boolean expression like `subtotal + tax = total`.

## Rule Type to Test Implementation Mapping

All YAML examples use dbt >= 1.10.5 syntax (`data_tests:` with `arguments:`/`config:` nesting). For older versions, flatten `arguments:` and `config:` keys to the top level under the test name.

### Completeness Rules

| Rule | Test | Package | Notes |
|------|------|---------|-------|
| Column must not contain nulls | `not_null` | dbt-core | Built-in generic test |
| At least one non-null value in column | `dbt_utils.at_least_one` | dbt-utils | Weaker than not_null; for optional-but-not-empty columns |
| All required fields present | `not_null` on each required column | dbt-core | Apply per-column from contract |
| Row count within expected range | `dbt_expectations.expect_table_row_count_to_be_between` | dbt-expectations | `min_value`, `max_value` |

```yaml
columns:
  - name: customer_id
    data_tests:
      - not_null
  - name: email
    data_tests:
      - dbt_utils.at_least_one
```

### Uniqueness Rules

| Rule | Test | Package | Notes |
|------|------|---------|-------|
| Single-column primary key | `unique` | dbt-core | Built-in generic test |
| Composite primary key | `dbt_utils.unique_combination_of_columns` | dbt-utils | Model-level test |
| Uniqueness proportion in range | `dbt_expectations.expect_column_proportion_of_unique_values_to_be_between` | dbt-expectations | For soft uniqueness checks |

```yaml
models:
  - name: fct_orders
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          arguments:
            combination_of_columns:
              - order_id
              - line_item_id
    columns:
      - name: order_id
        data_tests:
          - unique
```

### Validity Rules -- Categorical (Discrete Value Sets)

| Rule | Test | Package | Notes |
|------|------|---------|-------|
| Column value must be in allowed list | `accepted_values` | dbt-core | Built-in; non-null values only |
| Column value must NOT be in forbidden list | `dbt_utils.not_accepted_values` | dbt-utils | Inverse of accepted_values |
| Distinct values must exactly match set | `dbt_expectations.expect_column_distinct_values_to_equal_set` | dbt-expectations | Strict set equality |
| Distinct values must contain set | `dbt_expectations.expect_column_distinct_values_to_contain_set` | dbt-expectations | Subset check |

```yaml
columns:
  - name: status
    data_tests:
      - accepted_values:
          arguments:
            values: ['pending', 'shipped', 'delivered', 'cancelled']
  - name: error_code
    data_tests:
      - dbt_utils.not_accepted_values:
          arguments:
            values: ['DEPRECATED_001', 'DEPRECATED_002']
```

**When to use `not_accepted_values`:** Only when you have a short, known list of forbidden discrete values. It checks `column_value IN (list)`. It does NOT support pattern matching, wildcards, or LIKE expressions.

### Validity Rules -- String Patterns (LIKE, Regex)

| Rule | Test | Package | Notes |
|------|------|---------|-------|
| String matches SQL LIKE pattern | `dbt_utils.expression_is_true` | dbt-utils | Column-level: `expression: "LIKE 'pattern'"` |
| String matches SQL LIKE pattern (declarative) | `dbt_expectations.expect_column_values_to_match_like_pattern` | dbt-expectations | `like_pattern: 'pattern'` |
| String matches one of multiple LIKE patterns | `dbt_expectations.expect_column_values_to_match_like_pattern_list` | dbt-expectations | `like_pattern_list: [...]` |
| String matches regex | `dbt_expectations.expect_column_values_to_match_regex` | dbt-expectations | `regex: 'pattern'` |
| String does NOT match LIKE pattern | `dbt_expectations.expect_column_values_to_not_match_like_pattern` | dbt-expectations | Inverse |
| String length in range | `dbt_expectations.expect_column_value_lengths_to_be_between` | dbt-expectations | `min_value`, `max_value` |

```yaml
columns:
  - name: station_id
    data_tests:
      # Option A: dbt_utils (no additional package beyond dbt-utils)
      - dbt_utils.expression_is_true:
          arguments:
            expression: "LIKE 'GHCND:%'"
      # Option B: dbt-expectations (more declarative, clearer intent)
      - dbt_expectations.expect_column_values_to_match_like_pattern:
          arguments:
            like_pattern: "GHCND:%"
  - name: ssn_masked
    data_tests:
      - dbt_expectations.expect_column_values_to_match_regex:
          arguments:
            regex: '^\*{3}-\*{2}-\d{4}$'
```

**This is the bug #31 fix.** For a rule like "station_id must match pattern GHCND:*", the correct test is `expression_is_true` with `LIKE` or `expect_column_values_to_match_like_pattern` -- never `not_accepted_values`.

### Validity Rules -- Numeric Range

| Rule | Test | Package | Notes |
|------|------|---------|-------|
| Value within min/max range | `dbt_utils.accepted_range` | dbt-utils | `min_value`, `max_value` (inclusive by default) |
| Value within range (configurable strictness) | `dbt_expectations.expect_column_values_to_be_between` | dbt-expectations | `strictly: true` for exclusive bounds |
| Positive/non-negative constraint | `dbt_utils.expression_is_true` | dbt-utils | `expression: ">= 0"` at column level |
| Cross-column arithmetic | `dbt_utils.expression_is_true` | dbt-utils | Model-level: `expression: "subtotal + tax = total"` |

```yaml
columns:
  - name: temperature_celsius
    data_tests:
      - dbt_utils.accepted_range:
          arguments:
            min_value: -89.2
            max_value: 56.7
  - name: quantity
    data_tests:
      - dbt_utils.expression_is_true:
          arguments:
            expression: ">= 0"
models:
  - name: fct_orders
    data_tests:
      - dbt_utils.expression_is_true:
          arguments:
            expression: "subtotal + tax_amount = total_amount"
```

### Referential Integrity / Consistency Rules

| Rule | Test | Package | Notes |
|------|------|---------|-------|
| Foreign key exists in parent | `relationships` | dbt-core | `to: ref('parent'), field: 'id'` |
| Column values not constant | `dbt_utils.not_constant` | dbt-utils | Detects frozen/stuck columns |
| Values monotonically increasing | `dbt_expectations.expect_column_values_to_be_increasing` | dbt-expectations | For sequence columns |
| Two tables have equal row counts | `dbt_expectations.expect_table_row_count_to_equal_other_table` | dbt-expectations | Cross-table consistency |
| Aggregation matches other table | `dbt_expectations.expect_table_aggregation_to_equal_other_table` | dbt-expectations | Cross-table value check |
| Column pair A > B | `dbt_expectations.expect_column_pair_values_A_to_be_greater_than_B` | dbt-expectations | e.g., end_date > start_date |

```yaml
columns:
  - name: customer_id
    data_tests:
      - relationships:
          arguments:
            to: ref('dim_customers')
            field: customer_id
  - name: end_date
    data_tests:
      - dbt_expectations.expect_column_pair_values_A_to_be_greater_than_B:
          arguments:
            column_A: end_date
            column_B: start_date
```

### Timeliness / Freshness Rules

| Rule | Test | Package | Notes |
|------|------|---------|-------|
| Data updated within N time units | `dbt_utils.recency` | dbt-utils | `datepart`, `field`, `interval` |
| Recent rows exist (declarative) | `dbt_expectations.expect_row_values_to_have_recent_data` | dbt-expectations | `datepart`, `interval` |
| Recent rows per group | `dbt_expectations.expect_grouped_row_values_to_have_recent_data` | dbt-expectations | Per-partition freshness |
| Complete date coverage | `dbt_expectations.expect_row_values_to_have_data_for_every_n_datepart` | dbt-expectations | No gaps in time series |

```yaml
models:
  - name: fct_daily_weather
    data_tests:
      - dbt_utils.recency:
          arguments:
            datepart: day
            field: observation_date
            interval: 3
      - dbt_expectations.expect_row_values_to_have_data_for_every_n_datepart:
          arguments:
            date_col: observation_date
            date_part: day
            interval: 1
```

### Statistical / Distribution Rules

| Rule | Test | Package | Notes |
|------|------|---------|-------|
| Mean within range | `dbt_expectations.expect_column_mean_to_be_between` | dbt-expectations | `min_value`, `max_value` |
| Median within range | `dbt_expectations.expect_column_median_to_be_between` | dbt-expectations | |
| Std dev within range | `dbt_expectations.expect_column_stdev_to_be_between` | dbt-expectations | |
| Sum within range | `dbt_expectations.expect_column_sum_to_be_between` | dbt-expectations | |
| Min/max within range | `dbt_expectations.expect_column_min_to_be_between` / `max` | dbt-expectations | |
| Quantile values in range | `dbt_expectations.expect_column_quantile_values_to_be_between` | dbt-expectations | |
| Values within N std devs | `dbt_expectations.expect_column_values_to_be_within_n_stdevs` | dbt-expectations | Z-score outlier detection |
| Values within N moving std devs | `dbt_expectations.expect_column_values_to_be_within_n_moving_stdevs` | dbt-expectations | Time-windowed outlier detection |
| Distinct count in range | `dbt_expectations.expect_column_unique_value_count_to_be_between` | dbt-expectations | Cardinality check |

```yaml
columns:
  - name: order_total
    data_tests:
      - dbt_expectations.expect_column_mean_to_be_between:
          arguments:
            min_value: 45.00
            max_value: 150.00
      - dbt_expectations.expect_column_stdev_to_be_between:
          arguments:
            min_value: 10
            max_value: 80
      - dbt_expectations.expect_column_values_to_be_within_n_stdevs:
          arguments:
            sigma_threshold: 3
```

## Run-Over-Run Implementation Patterns

dbt is stateless by design -- each `dbt test` invocation queries the current state of the warehouse with no memory of previous runs. Implementing run-over-run consistency checks (e.g., "row count changed by no more than 20% vs last run") requires introducing state outside dbt's built-in test framework.

Four patterns exist, ordered from simplest to most capable.

### Pattern 1: Elementary Anomaly Detection (Recommended)

**Best for:** Teams that want statistical run-over-run monitoring without writing custom code.

Elementary's anomaly detection tests automatically collect metrics into an incremental `data_monitoring_metrics` table and compare current values against a historical training period using statistical methods (z-score based, configurable sensitivity).

```yaml
# packages.yml
packages:
  - package: elementary-data/elementary
    version: [">=0.16.0", "<0.17.0"]
```

```yaml
# schema.yml
models:
  - name: fct_daily_weather
    config:
      elementary:
        timestamp_column: "loaded_at"
    data_tests:
      # Row count anomaly detection (run-over-run volume)
      - elementary.volume_anomalies:
          timestamp_column: loaded_at
          time_bucket:
            period: day
            count: 1
          training_period:
            period: day
            count: 30
          detection_period:
            period: day
            count: 1
          anomaly_sensitivity: 3        # z-score threshold
          anomaly_direction: both       # detect spikes and drops
          tags: ["elementary"]
          config:
            severity: warn

      # Freshness anomaly detection
      - elementary.freshness_anomalies:
          timestamp_column: loaded_at
          tags: ["elementary"]
          config:
            severity: warn

      # Column-level metric anomalies (null rate, mean, etc.)
      - elementary.column_anomalies:
          column_name: temperature_celsius
          timestamp_column: loaded_at
          column_anomalies:
            - null_count
            - mean
            - min
            - max
          anomaly_sensitivity: 3
          tags: ["elementary"]

      # Per-dimension volume tracking
      - elementary.dimension_anomalies:
          timestamp_column: loaded_at
          dimensions:
            - station_type
            - country_code
          tags: ["elementary"]
```

**How it works:** On each `dbt test` run, Elementary collects the metric (e.g., row count) for the current time bucket, stores it in `data_monitoring_metrics`, then compares the detection period values against the training period to compute a z-score. Values outside the sensitivity threshold are flagged as anomalies.

**Tradeoffs:** Requires adding the Elementary package. Free OSS version provides anomaly detection; Elementary Cloud adds dashboards and alerting. No manual threshold maintenance -- statistical bounds adapt automatically.

### Pattern 2: Custom Singular Test with Metrics Log Table

**Best for:** Teams that need explicit threshold control (e.g., "exactly 20% tolerance") without adding the Elementary package.

This pattern uses: (a) a dbt model that logs metrics per run into an incremental table, (b) a singular test that queries the metrics table comparing current vs previous run.

**Step 1: Create a metrics logging model.**

```sql
-- models/meta/meta_run_metrics.sql
{{ config(
    materialized='incremental',
    unique_key='metric_id'
) }}

WITH current_metrics AS (
    SELECT
        '{{ invocation_id }}' AS invocation_id,
        CURRENT_TIMESTAMP AS measured_at,
        'fct_daily_weather' AS model_name,
        'row_count' AS metric_name,
        CAST(COUNT(*) AS DOUBLE) AS metric_value
    FROM {{ ref('fct_daily_weather') }}

    UNION ALL

    SELECT
        '{{ invocation_id }}',
        CURRENT_TIMESTAMP,
        'fct_daily_weather',
        'null_rate_station_id',
        CAST(SUM(CASE WHEN station_id IS NULL THEN 1 ELSE 0 END) AS DOUBLE)
            / CAST(COUNT(*) AS DOUBLE)
    FROM {{ ref('fct_daily_weather') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['invocation_id', 'model_name', 'metric_name']) }}
        AS metric_id,
    *
FROM current_metrics
```

**Step 2: Create a singular test comparing runs.**

```sql
-- tests/assert_row_count_within_tolerance.sql
-- Fails if row count changed by more than 20% vs previous run.

WITH ranked_metrics AS (
    SELECT
        metric_value,
        measured_at,
        ROW_NUMBER() OVER (ORDER BY measured_at DESC) AS run_rank
    FROM {{ ref('meta_run_metrics') }}
    WHERE model_name = 'fct_daily_weather'
      AND metric_name = 'row_count'
),

current_run AS (
    SELECT metric_value FROM ranked_metrics WHERE run_rank = 1
),

previous_run AS (
    SELECT metric_value FROM ranked_metrics WHERE run_rank = 2
)

SELECT
    current_run.metric_value AS current_count,
    previous_run.metric_value AS previous_count,
    ABS(current_run.metric_value - previous_run.metric_value)
        / NULLIF(previous_run.metric_value, 0) AS pct_change
FROM current_run
CROSS JOIN previous_run
WHERE ABS(current_run.metric_value - previous_run.metric_value)
    / NULLIF(previous_run.metric_value, 0) > 0.20
```

**Tradeoffs:** Full control over tolerance thresholds. No additional packages. Requires maintaining the metrics model and ensuring it runs before the test. Manual threshold maintenance (does not adapt to natural variance). First run has no baseline to compare against -- the singular test must handle the case where `previous_run` returns zero rows (use `HAVING COUNT(*) > 0` or similar guard).

### Pattern 3: dbt-expectations Cross-Table Comparison

**Best for:** Simple "current table vs reference table" comparisons where the reference is a seed, snapshot, or prior-run table.

```yaml
models:
  - name: fct_daily_weather
    data_tests:
      # Row count within percentage of reference table
      - dbt_expectations.expect_table_row_count_to_equal_other_table_times_factor:
          arguments:
            compare_model: ref('fct_daily_weather_snapshot')
            factor: 1
            tolerance_percent: 0.20

      # Aggregation matches reference
      - dbt_expectations.expect_table_aggregation_to_equal_other_table:
          arguments:
            expression: "sum(temperature_celsius)"
            compare_model: ref('fct_daily_weather_snapshot')
            compare_expression: "sum(temperature_celsius)"
            tolerance_percent: 0.05
```

**Tradeoffs:** Requires a reference table (snapshot, seed, or materialized prior-run copy). Does not automatically maintain history. Clean syntax for known-reference comparisons.

### Pattern 4: store_failures + External Comparison

**Best for:** Ad hoc investigation after failures, not primary monitoring.

```yaml
data_tests:
  - not_null:
      config:
        store_failures: true
        store_failures_as: table    # or 'view'
        schema: dbt_test__audit
```

When `store_failures` is enabled, dbt materializes failing rows into a table in the `dbt_test__audit` schema. These tables are overwritten on each run (not appended). An external process (orchestrator, BI tool, or custom script) can query these tables to track failure trends over time.

**Tradeoffs:** dbt overwrites failure tables each run -- no built-in history. Useful for debugging specific failures but requires an external system to capture state between runs. Not a run-over-run comparison mechanism by itself.

### Run-Over-Run Pattern Recommendation

| Team Size | Recommended Pattern | Rationale |
|-----------|-------------------|-----------|
| 1-3 engineers | Pattern 2 (custom singular test) | No extra packages, explicit thresholds, easy to understand |
| 3-5 engineers | Pattern 1 (Elementary) | Statistical detection adapts to natural variance, less threshold maintenance |
| 5+ engineers | Pattern 1 (Elementary) + Pattern 2 for custom metrics | Statistical baseline + business-specific tolerance checks |

For the assess-quality and implement-models skills specifically: when a quality config defines a "run-over-run consistency" check, the implement-models skill should generate Pattern 2 (custom singular test) as the default, with a comment noting that Elementary is the recommended upgrade path.

## Package Decision Matrix

| Package | When to Use | When NOT to Use |
|---------|-------------|-----------------|
| **dbt-core tests** | Completeness (not_null), uniqueness (unique), categorical validity (accepted_values), referential integrity (relationships) | Pattern matching, range checks, statistical checks, cross-table comparisons |
| **dbt-utils** | Pattern matching via expression_is_true, range checks (accepted_range), composite keys (unique_combination_of_columns), freshness (recency), cross-table equality | Statistical/distribution checks, anomaly detection |
| **dbt-expectations** (Metaplane) | Statistical checks (mean, stdev, quantile), regex/LIKE pattern matching, cross-table comparisons, row count bounds, date completeness | Simple not_null/unique checks (use dbt-core), run-over-run anomaly detection |
| **Elementary** | Run-over-run anomaly detection (volume, freshness, column metrics, dimension monitoring) | Simple rule-based checks (use dbt-core/utils), one-time assertions |

## Key Recommendations for Skill Updates

### For assess-quality skill

The quality config template should map rule types to test semantics, not just quality dimensions. When a quality dimension is "validity" and the measurement method involves a string pattern (LIKE, regex), the quality config should record the constraint type (pattern, range, categorical, cross-column) so downstream skills select the correct test.

### For implement-models skill

1. **Update the test mapping table** in `dbt-testing-patterns.md` to include validity sub-types (categorical, pattern, range, cross-column) with distinct test selections for each.

2. **Add run-over-run generation logic.** When the quality config includes a run-over-run consistency check, generate a Pattern 2 singular test (metrics log + comparison query). Include a comment referencing Elementary as the recommended production approach.

3. **Add pattern-matching test generation.** When a contract or quality config specifies a LIKE pattern or regex constraint, generate `dbt_utils.expression_is_true` (for LIKE) or `dbt_expectations.expect_column_values_to_match_regex` (for regex). Never generate `dbt_utils.not_accepted_values` for pattern rules.

## Changelog

| Date | Change |
|------|--------|
| 2026-04-08 | Initial research document |
