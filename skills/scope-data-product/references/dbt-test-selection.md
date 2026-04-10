# dbt Test Selection

## Rule Type Taxonomy

Every quality rule falls into a rule type based on what the test *does*, not which dimension it serves. A single dimension (e.g., validity) spans multiple rule types requiring different dbt tests.

### Stateless Rule Types

| Rule Type | Description | Example |
|-----------|-------------|---------|
| not-null | Column must not contain NULL | Required fields from contract |
| unique | Column values must be unique | Primary keys, natural keys |
| unique-combination | Combination of columns must be unique | Composite keys |
| enum-membership | Value must be in a defined set | `status IN ('active', 'inactive')` |
| not-in-set | Value must not be in a forbidden set | `status NOT IN ('')` |
| numeric-range | Value must be within min/max bounds | `0 <= amount <= 10000` |
| string-pattern | Value must match a LIKE or regex pattern | `station LIKE 'GHCND:%'` |
| string-length | Value length must be within bounds | `LEN(zip_code) = 5` |
| expression | Arbitrary SQL expression must be true per row | `end_date >= start_date` |
| referential-integrity | Foreign key must exist in referenced table | `customer_id` in `dim_customers` |
| row-count-range | Table row count within bounds | `1000 <= count <= 50000` |
| recency | Table must contain recent data | Max timestamp within last N hours |
| aggregate-bound | Aggregate metric within bounds | `45 <= AVG(age) <= 55` |
| type-conformance | Values must parse as expected type | String column contains valid dates |
| freshness | Source data within freshness threshold | `loaded_at` within last 12 hours |

### Stateful Rule Types

| Rule Type | Description | Example |
|-----------|-------------|---------|
| metric-stability | Metric within +/-N% of stored baseline | Null rate within 5% of previous run |
| volume-stability | Row count within +/-N% of previous run | Row count within 20% of yesterday |
| distribution-drift | Value distribution must not shift beyond threshold | KS test p > 0.05 vs reference |
| schema-stability | Column set and types must not change unexpectedly | New/dropped columns, type changes |

## Stateless Rule Mapping

| Rule Type | dbt Test | Package | Config |
|-----------|----------|---------|--------|
| not-null | `not_null` | built-in | bare test |
| unique | `unique` | built-in | bare test |
| unique-combination | `dbt_utils.unique_combination_of_columns` | dbt-utils | `combination_of_columns: [col_a, col_b]` |
| enum-membership | `accepted_values` | built-in | `values: ['a', 'b', 'c']` |
| not-in-set | `dbt_utils.not_accepted_values` | dbt-utils | `values: ['']` |
| numeric-range | `dbt_utils.accepted_range` | dbt-utils | `min_value: 0, max_value: 10000` |
| string-pattern (LIKE) | `dbt_utils.expression_is_true` | dbt-utils | `expression: "LIKE 'PREFIX%'"` (column-level) |
| string-pattern (regex) | `dbt_expectations.expect_column_values_to_match_regex` | dbt-expectations | `regex: '^\d{5}$'` |
| string-length | `dbt_expectations.expect_column_value_lengths_to_be_between` | dbt-expectations | `min_value: 5, max_value: 5` |
| expression | `dbt_utils.expression_is_true` | dbt-utils | `expression: "end_date >= start_date"` (model-level) |
| referential-integrity | `relationships` | built-in | `to: ref('dim_table'), field: 'id'` |
| row-count-range | `dbt_expectations.expect_table_row_count_to_be_between` | dbt-expectations | `min_value: 1000, max_value: 50000` |
| recency | `dbt_expectations.expect_row_values_to_have_recent_data` | dbt-expectations | `datepart: day, interval: 1` |
| aggregate-bound | `dbt_expectations.expect_column_mean_to_be_between` | dbt-expectations | `min_value: 45, max_value: 55` |
| type-conformance | `dbt_expectations.expect_column_values_to_match_regex` | dbt-expectations | Use type-specific regex |
| freshness | `dbt source freshness` | built-in | `warn_after`, `error_after` in source YAML |

### LIKE vs Regex Selection

| Constraint | Test | Rationale |
|-----------|------|-----------|
| SQL LIKE pattern (`%`, `_` wildcards) | `dbt_utils.expression_is_true` | LIKE is standard SQL, portable |
| Regex pattern (character classes, quantifiers) | `dbt_expectations.expect_column_values_to_match_regex` | Handles cross-platform regex dispatch |
| Ambiguous | Ask the user | Do not guess |

## Stateful Rule Mapping

Stateful rules compare current state against a baseline. dbt generic tests cannot express them — use singular tests or packages.

| Rule Type | Strategy | Complexity | Dependency |
|-----------|----------|:----------:|------------|
| metric-stability | Singular test with baseline seed or snapshot | Medium | Baseline storage |
| volume-stability | Singular test with previous row count | Medium | Baseline storage |
| distribution-drift | dbt-expectations cross-table tests or external script | High | Reference distribution |
| schema-stability | `dbt build --select state:modified+` (CI) or Elementary | Low | Manifest artifact |

### Pattern 1: Seed-Based Baselines (Recommended Start)

**Baseline seed (`seeds/quality_baselines.csv`):**

```csv
model_name,column_name,metric_name,baseline_value,tolerance_pct,last_updated
fct_orders,customer_id,null_rate,0.02,5.0,2026-04-01
```

**Singular test (`tests/assert_metric_stability.sql`):**

```sql
with current_metrics as (
    select
        'fct_orders' as model_name,
        'customer_id' as column_name,
        'null_rate' as metric_name,
        count(case when customer_id is null then 1 end)::float
            / nullif(count(*), 0) as current_value
    from {{ ref('fct_orders') }}
),

baselines as (
    select * from {{ ref('quality_baselines') }}
),

violations as (
    select
        c.model_name, c.column_name, c.metric_name,
        c.current_value, b.baseline_value, b.tolerance_pct,
        abs(c.current_value - b.baseline_value)
            / nullif(b.baseline_value, 0) * 100 as deviation_pct
    from current_metrics c
    join baselines b using (model_name, column_name, metric_name)
    where abs(c.current_value - b.baseline_value)
        / nullif(b.baseline_value, 0) * 100 > b.tolerance_pct
)

select * from violations
```

**Zero-baseline edge case:** When baseline is 0 (e.g., 0% null rate), use absolute threshold instead of percentage. A 0% null rate baseline with any nulls is just `not_null`.

### Pattern 2: Snapshot-Based Baselines (Automated Updates)

Use a dbt snapshot on a metrics model to capture values each run. Compare current vs most recent superseded snapshot record. Baselines update automatically. See the [research document](../../docs/research/2026-04-08-dbt-test-selection-patterns.research.md) for full SQL.

### Team Size Recommendation

| Team Size | Recommended Pattern | Rationale |
|-----------|-------------------|-----------|
| 1-3 engineers | Pattern 1 (seed-based) | No extra packages, explicit thresholds |
| 3-5 engineers | Pattern 2 (snapshot-based) | Automated baselines, less maintenance |
| 5+ engineers | Elementary package | Statistical detection, adapts to variance |

## Decision Rules

1. Classify by rule type, not by quality dimension.
2. Use built-in tests when available, dbt-utils second, dbt-expectations third.
3. Stateful rules always require singular tests or packages — never generic tests.
4. Use the Metaplane fork of dbt-expectations (calogica is unmaintained since Dec 2024).
5. When a rule includes LIKE or regex, it is `string-pattern`, not `enum-membership`.
