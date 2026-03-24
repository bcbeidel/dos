# dbt Testing Patterns

## Generic Test Mapping from Quality Dimensions

| Quality Dimension | dbt Generic Test | Configuration |
|------------------|-----------------|---------------|
| Completeness | `not_null` | Apply to required columns from contract |
| Uniqueness | `unique` | Apply to primary key columns |
| Validity (categorical) | `accepted_values` | `values: [list]` from contract constraints |
| Referential integrity | `relationships` | `to: ref('dim_table')`, `field: 'id'` |

```yaml
columns:
  - name: order_id
    tests:
      - not_null
      - unique
  - name: status
    tests:
      - accepted_values:
          values: ['pending', 'shipped', 'delivered', 'cancelled']
  - name: customer_id
    tests:
      - relationships:
          to: ref('dim_customers')
          field: customer_id
```

## dbt-expectations Tests for Distribution/Range Checks

Use the Metaplane fork (original calogica package is unmaintained since December 2024).

| Check Type | Test | Example |
|-----------|------|---------|
| Range | `expect_column_values_to_be_between` | `min_value: 0, max_value: 10000` |
| Distribution | `expect_column_mean_to_be_between` | `min_value: 45, max_value: 55` |
| Row count | `expect_table_row_count_to_be_between` | `min_value: 1000` |
| Recency | `expect_row_values_to_have_recent_data` | `datepart: day, interval: 1` |
| Pattern | `expect_column_values_to_match_regex` | `regex: '^\d{3}-\d{2}-\d{4}$'` |

## Severity and Failure Handling

```yaml
tests:
  - not_null:
      config:
        severity: warn        # warn or error
        error_if: ">100"      # fail if >100 failures
        warn_if: ">10"        # warn if >10 failures
        store_failures: true   # persist failures to schema
```

Treat every suppressed test as tech debt requiring business justification. Alert fatigue from accumulated tests is the dominant risk.

## dbt Unit Tests (v1.8+)

Test SQL transformation logic with mock data. Run in dev/CI only — never in production (static inputs waste compute).

```yaml
unit_tests:
  - name: test_order_total_calculation
    model: int_orders__enriched
    given:
      - input: ref('stg_orders')
        rows:
          - {order_id: 1, quantity: 3, unit_price: 10.00}
      - input: ref('stg_taxes')
        rows:
          - {order_id: 1, tax_rate: 0.08}
    expect:
      rows:
        - {order_id: 1, total: 32.40}
```

Use for: complex joins, conditional logic, edge cases (nulls, zero quantities, negative values).

## Three-Tier Validation Strategy

| Tier | Environment | Tools | Purpose |
|------|------------|-------|---------|
| 1 | Local dev | Pandera + pytest, dbt unit tests | Fast feedback (<60s), no warehouse |
| 2 | CI pipeline | dbt data tests + dbt-expectations | Transformation validation (<10 min) |
| 3 | Production | Soda / Great Expectations, dbt source freshness | Continuous monitoring, anomaly detection |

Small teams (1-3 engineers): start with dbt tests in CI/production. Add Pandera only for Python-heavy pipelines. Defer Soda/GE until dedicated capacity exists.
