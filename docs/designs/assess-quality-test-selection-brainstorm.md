---
name: assess-quality dbt Test Selection Reference
description: Brainstorm design for a new reference file that maps quality rule types to correct dbt test implementations, fixing wrong test suggestions (#31) and missing run-over-run patterns (#15).
type: design
status: draft
related:
  - skills/assess-quality/SKILL.md
  - skills/assess-quality/references/quality-dimensions.md
  - skills/assess-quality/references/validation-tiers.md
  - skills/implement-models/references/dbt-testing-patterns.md
  - docs/context/data-validation-tool-comparison.md
  - docs/context/tiered-validation-strategy.md
  - docs/context/anomaly-drift-detection.md
  - docs/context/data-quality-dimensions.md
---

# assess-quality: dbt Test Selection Reference

## Problem

The assess-quality skill categorizes quality rules by **dimension** (validity, consistency, completeness) but not by **implementation type**. This causes two documented failures:

1. **Wrong test selection (#31).** A string format/pattern rule (`station LIKE 'GHCND:%'`) was mapped to `dbt_utils.not_accepted_values` because the skill saw "validity" and picked a validity-associated test. The correct test is `dbt_utils.expression_is_true`. The dimension is right; the test is wrong because "validity" spans multiple implementation types (enum membership, numeric range, string pattern, cross-column expression).

2. **Missing stateful patterns (#15).** Run-over-run consistency checks (e.g., null rate stability within +/-5% of baseline) were defined in the quality config but have no implementation path. dbt generic tests are stateless -- they evaluate the current dataset only. The skill needs to acknowledge this and provide concrete singular test patterns.

**Root cause:** The skill maps dimension to test. It should map **rule type** to test. One new reference file with a rule-type-to-dbt-test mapping table fixes both issues.

## Rule Type Taxonomy

Every quality rule observed in issues, references, context files, and the quality-config template falls into one of these implementation types. The taxonomy is organized by what the test *does*, not which dimension it serves.

### Stateless Rule Types (dbt generic tests)

These evaluate the current dataset without needing historical state.

| Rule Type | Description | Examples |
|-----------|-------------|----------|
| **not-null** | Column must not contain NULL values | Required fields from contract |
| **unique** | Column values must be unique (no duplicates) | Primary keys, natural keys |
| **unique-combination** | Combination of columns must be unique | Composite keys |
| **enum-membership** | Value must be one of a defined set | `status IN ('active', 'inactive')` |
| **not-in-set** | Value must not be one of a defined set | `status NOT IN ('')` |
| **numeric-range** | Value must be within min/max bounds | `0 <= amount <= 10000` |
| **string-pattern** | Value must match a regex or LIKE pattern | `station LIKE 'GHCND:%'`, email regex |
| **string-length** | Value must have length within bounds | `LEN(zip_code) = 5` |
| **expression** | Arbitrary SQL expression must evaluate true per row | Cross-column constraints, computed validations |
| **referential-integrity** | Foreign key must exist in referenced table | `customer_id` exists in `dim_customers` |
| **row-count-range** | Table row count must be within bounds | `1000 <= row_count <= 50000` |
| **recency** | Table must contain recent data | Max timestamp within last N hours/days |
| **aggregate-bound** | Aggregate metric (mean, sum, stddev) within bounds | `45 <= AVG(age) <= 55` |
| **type-conformance** | Values must parse as expected type | All values in a string column are valid dates |
| **freshness** | Source data must be within freshness threshold | `loaded_at` within last 12 hours |

### Stateful Rule Types (require historical comparison)

These compare current state against a baseline or previous run. dbt generic tests cannot express them natively.

| Rule Type | Description | Examples |
|-----------|-------------|----------|
| **metric-stability** | A metric must be within +/-N% of a stored baseline | Null rate within 5% of previous run |
| **volume-stability** | Row count must be within +/-N% of previous run | Row count within 20% of yesterday |
| **distribution-drift** | Value distribution must not shift beyond threshold | KS test p > 0.05 vs reference distribution |
| **schema-stability** | Column set and types must not change unexpectedly | New columns, dropped columns, type changes |

## Rule Type to dbt Test Mapping

This is the core decision table the new reference file should contain. It maps each rule type to its correct dbt implementation.

### Stateless Rules

| Rule Type | dbt Test | Package | Configuration |
|-----------|----------|---------|---------------|
| not-null | `not_null` | built-in | bare test, no arguments |
| unique | `unique` | built-in | bare test, no arguments |
| unique-combination | `dbt_utils.unique_combination_of_columns` | dbt-utils | `combination_of_columns: [col_a, col_b]` |
| enum-membership | `accepted_values` | built-in | `values: ['a', 'b', 'c']` |
| not-in-set | `dbt_utils.not_accepted_values` | dbt-utils | `values: ['']` |
| numeric-range | `dbt_utils.accepted_range` | dbt-utils | `min_value: 0, max_value: 10000` |
| string-pattern | `dbt_expectations.expect_column_values_to_match_regex` | dbt-expectations (Metaplane) | `regex: '^\d{3}-\d{2}-\d{4}$'` |
| string-pattern (LIKE) | `dbt_utils.expression_is_true` | dbt-utils | `expression: "column LIKE 'PREFIX%'"` |
| string-length | `dbt_expectations.expect_column_value_lengths_to_be_between` | dbt-expectations (Metaplane) | `min_value: 5, max_value: 5` |
| expression | `dbt_utils.expression_is_true` | dbt-utils | `expression: "end_date >= start_date"` |
| referential-integrity | `relationships` | built-in | `to: ref('dim_table'), field: 'id'` |
| row-count-range | `dbt_expectations.expect_table_row_count_to_be_between` | dbt-expectations (Metaplane) | `min_value: 1000, max_value: 50000` |
| recency | `dbt_expectations.expect_row_values_to_have_recent_data` | dbt-expectations (Metaplane) | `datepart: day, interval: 1` |
| aggregate-bound | `dbt_expectations.expect_column_mean_to_be_between` | dbt-expectations (Metaplane) | `min_value: 45, max_value: 55` |
| type-conformance | `dbt_expectations.expect_column_values_to_match_regex` | dbt-expectations (Metaplane) | Use type-specific regex (date, integer, etc.) |
| freshness | `dbt source freshness` | built-in | `warn_after`, `error_after` in source YAML (not a data test) |

**The #31 fix in one line:** When the quality rule is a string format/pattern check, map to `dbt_expectations.expect_column_values_to_match_regex` (for regex) or `dbt_utils.expression_is_true` (for LIKE patterns). Never map to `accepted_values` or `not_accepted_values` -- those are for enum membership and set exclusion, not pattern matching.

### Stateful Rules

Stateful rules cannot use dbt generic tests. They require one of these implementation strategies:

| Rule Type | Implementation Strategy | Complexity | Dependency |
|-----------|------------------------|:----------:|------------|
| metric-stability | Singular test with baseline seed/table | Medium | Baseline storage |
| volume-stability | Singular test with previous row count | Medium | Baseline storage |
| distribution-drift | External script or dbt-expectations distribution tests | High | Statistical library or dbt-expectations |
| schema-stability | `dbt build --select state:modified+` (CI) or Elementary | Low | Manifest artifact or Elementary package |

## Stateful Test Implementation Patterns

This section addresses #15 directly. Run-over-run checks require storing previous state and comparing against it.

### Pattern 1: Singular Test with Baseline Seed (Recommended Starting Point)

Store baselines in a seed CSV. Write a singular test that queries current metrics and compares against the seed.

**Baseline seed (`seeds/quality_baselines.csv`):**

```csv
model_name,column_name,metric_name,baseline_value,tolerance_pct,last_updated
fct_orders,customer_id,null_rate,0.02,5.0,2026-04-01
fct_orders,amount,null_rate,0.001,5.0,2026-04-01
```

**Singular test (`tests/assert_metric_stability.sql`):**

```sql
-- Returns rows that violate stability thresholds (failing = non-empty result)
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
        c.model_name,
        c.column_name,
        c.metric_name,
        c.current_value,
        b.baseline_value,
        b.tolerance_pct,
        abs(c.current_value - b.baseline_value) / nullif(b.baseline_value, 0) * 100
            as deviation_pct
    from current_metrics c
    join baselines b
        on c.model_name = b.model_name
        and c.column_name = b.column_name
        and c.metric_name = b.metric_name
    where abs(c.current_value - b.baseline_value) / nullif(b.baseline_value, 0) * 100
        > b.tolerance_pct
)

select * from violations
```

**Tradeoffs:** Simple, no package dependencies, version-controlled baselines. Manual baseline updates. Requires one singular test per metric or a parametrized macro.

### Pattern 2: Snapshot-Based Baseline (Automated Updates)

Use dbt snapshots to automatically capture metrics each run, then compare current against the most recent snapshot.

**Metrics model (`models/quality/quality_metrics_current.sql`):**

```sql
{{ config(materialized='table') }}

select
    'fct_orders' as model_name,
    'customer_id' as column_name,
    'null_rate' as metric_name,
    count(case when customer_id is null then 1 end)::float
        / nullif(count(*), 0) as metric_value,
    current_timestamp as measured_at
from {{ ref('fct_orders') }}
```

**Snapshot (`snapshots/quality_metrics_snapshot.sql`):**

```sql
{% snapshot quality_metrics_snapshot %}
{{ config(
    target_schema='snapshots',
    unique_key="model_name || '|' || column_name || '|' || metric_name",
    strategy='timestamp',
    updated_at='measured_at'
) }}
select * from {{ ref('quality_metrics_current') }}
{% endsnapshot %}
```

**Singular test (`tests/assert_metric_stability_vs_snapshot.sql`):**

```sql
with current_metrics as (
    select * from {{ ref('quality_metrics_current') }}
),

previous_metrics as (
    select *
    from {{ ref('quality_metrics_snapshot') }}
    where dbt_valid_to is not null  -- most recently superseded record
    qualify row_number() over (
        partition by model_name, column_name, metric_name
        order by dbt_valid_to desc
    ) = 1
),

violations as (
    select
        c.model_name,
        c.column_name,
        c.metric_name,
        c.metric_value as current_value,
        p.metric_value as previous_value,
        abs(c.metric_value - p.metric_value) / nullif(p.metric_value, 0) * 100
            as deviation_pct
    from current_metrics c
    join previous_metrics p
        on c.model_name = p.model_name
        and c.column_name = p.column_name
        and c.metric_name = p.metric_name
    where abs(c.metric_value - p.metric_value) / nullif(p.metric_value, 0) * 100
        > 5.0  -- configurable tolerance
)

select * from violations
```

**Tradeoffs:** Baselines update automatically. Full history in the snapshot table. More moving parts (metrics model + snapshot + singular test). Snapshot table grows over time.

### Pattern 3: Elementary Package (If Already in Stack)

Elementary's `elementary.volume_anomalies` and `elementary.column_anomalies` tests provide run-over-run detection using a training period of historical results stored in `elementary_test_results`.

```yaml
models:
  - name: fct_orders
    data_tests:
      - elementary.volume_anomalies:
          timestamp_column: created_at
          training_period:
            period: day
            count: 14
      - elementary.column_anomalies:
          column_name: customer_id
          timestamp_column: created_at
```

**Tradeoffs:** Lowest implementation effort if Elementary is already adopted. Full package dependency otherwise. Training period requires 14+ days of historical data before anomalies are detected. Opaque algorithm -- hard to tune thresholds precisely.

### Recommended Approach

- **Start with Pattern 1 (seed-based baselines)** for teams new to run-over-run checks. Simple, explicit, debuggable.
- **Graduate to Pattern 2 (snapshots)** when manual baseline updates become painful or when you need automated baseline drift tracking.
- **Use Pattern 3 (Elementary)** only if the package is already in the project. Do not add Elementary solely for run-over-run checks.

## Integration into SKILL.md

### Where the Reference Is Used

The new reference `dbt-test-selection.md` should be integrated at **two points** in the SKILL.md workflow:

1. **Step 4 (Define Measurement Methods and Thresholds).** After the user defines a measurement method for each dimension, the skill classifies it into a rule type using the taxonomy. This is where the skill determines *what kind of test* each rule needs, preventing the #31 misclassification.

2. **Step 8 (Recommend Validation Tooling by Tier).** When recommending dbt tests in Tier 2/3, the skill references the mapping table to suggest specific tests. For stateful rules, the skill explicitly calls out the implementation gap and recommends a singular test pattern.

### Proposed SKILL.md Changes

**In the Reference Materials section, add:**

```markdown
- [dbt-test-selection.md](references/dbt-test-selection.md) -- Rule type classification and dbt test mapping for implementation guidance
```

**In Step 4, add after the threshold calibration guidance:**

```markdown
**Rule type classification:** For each measurement method, classify the underlying
rule type using [dbt-test-selection.md](references/dbt-test-selection.md). The rule
type determines which dbt test implements the check. Do not map directly from
dimension to test -- a single dimension (e.g., validity) spans multiple rule types
(enum membership, numeric range, string pattern, expression) that require different
dbt tests.

For stateful rules (run-over-run comparisons, metric stability checks), flag
explicitly that these require singular tests with baseline storage. Reference the
implementation patterns in dbt-test-selection.md and note the pattern in the quality
config output.
```

**In Step 8, add after the scaling guidance:**

```markdown
**Test selection by rule type:** When recommending specific dbt tests, use the
rule-type-to-test mapping in [dbt-test-selection.md](references/dbt-test-selection.md)
rather than mapping from dimension name alone. This prevents mismatches where a
validity rule is mapped to `accepted_values` when it actually requires
`expression_is_true` or a regex test.
```

## Changes to quality-config-template.md

The template should add a `Rule Type` column to the Quality Dimensions table. This makes the rule type explicit in the output artifact so that implement-models can select the correct dbt test downstream.

### Current Template (Quality Dimensions Table)

```markdown
| Dimension | Measurement Method | Threshold (Green) | Threshold (Yellow) | Threshold (Red) |
```

### Proposed Template (Quality Dimensions Table)

```markdown
| Dimension | Rule Type | Measurement Method | Threshold (Green) | Threshold (Yellow) | Threshold (Red) |
```

Where `Rule Type` uses the taxonomy from `dbt-test-selection.md` (e.g., `not-null`, `string-pattern`, `numeric-range`, `metric-stability`).

This is a minimal change. The rule type column costs nothing for the human reader (it is a natural description of the check) and provides the implementation type that implement-models needs to select the correct dbt test.

### Note on the Template Row for "Consistency"

The current consistency row says: "Cross-system comparison and referential integrity checks." This conflates two different rule types:

- Cross-system comparison (referential-integrity rule type) maps to `relationships`
- Run-over-run stability (metric-stability rule type) maps to a singular test

The template should not prescribe a single measurement method for consistency. The rule type column disambiguates.

## Reference File Specification

### File: `skills/assess-quality/references/dbt-test-selection.md`

**Constraints from project conventions:**
- Under 200 lines
- Decision tables, no explanatory prose
- No runtime dependencies on docs/context/

**Proposed structure:**

```
# dbt Test Selection

## Rule Type Taxonomy
[Table: rule_type | description | example]

## Stateless Rule Mapping
[Table: rule_type | dbt_test | package | config_example]

## Stateful Rule Mapping
[Table: rule_type | implementation_strategy | complexity | pattern_reference]

## Stateful Implementation Patterns
[Pattern 1: Seed-based singular test - SQL template]
[Pattern 2: Snapshot-based singular test - SQL template]
[Pattern 3: Elementary package - YAML example]

## Decision Rules
1. Classify by rule type, not dimension.
2. Use built-in tests when available, dbt-utils second, dbt-expectations third.
3. Stateful rules always require singular tests or packages -- never generic tests.
4. Use Metaplane fork for dbt-expectations (calogica unmaintained since Dec 2024).
5. When a rule includes LIKE or regex, it is string-pattern, not enum-membership.
```

**Estimated length:** 120-150 lines. Well within the 200-line limit.

## Relationship to implement-models

The `implement-models` skill already has `references/dbt-testing-patterns.md` which contains a "Generic Test Mapping from Quality Dimensions" table. That table maps dimensions to tests (the same dimension-level mapping that causes #31). After the new assess-quality reference exists:

- `assess-quality` classifies rules into rule types and records them in the quality config
- `implement-models` reads the rule type from the quality config and uses its own `dbt-testing-patterns.md` to generate the correct YAML

The implement-models reference may benefit from a similar rule-type table, but that is a downstream change. The assess-quality reference is the fix for the classification step.

## Edge Cases and Open Questions

### 1. LIKE vs Regex Decision

When the user specifies a string pattern, should the skill default to LIKE-based `expression_is_true` or regex-based `expect_column_values_to_match_regex`?

**Proposed heuristic:** If the user provides a LIKE pattern, use `expression_is_true`. If the user provides a regex or describes a complex format (e.g., "SSN format XXX-XX-XXXX"), use `expect_column_values_to_match_regex`. If ambiguous, ask.

### 2. Cross-Platform Regex Differences

Regex syntax differs across platforms (DuckDB: `regexp_matches`, Snowflake: `REGEXP_LIKE`, Databricks: `RLIKE`, ClickHouse: `match()`). The `dbt_expectations.expect_column_values_to_match_regex` test abstracts this, but `expression_is_true` with raw SQL does not.

**Proposed approach:** Prefer `dbt_expectations.expect_column_values_to_match_regex` for regex patterns (it handles cross-platform dispatch). Use `expression_is_true` for LIKE patterns (LIKE is standard SQL, portable across all platforms).

### 3. Baseline Zero Problem

When a metric baseline is 0 (e.g., 0% null rate on a required field), percentage-based deviation is undefined (division by zero). A single null record would represent infinite percentage change.

**Proposed approach:** For zero baselines, use absolute threshold instead of percentage. If baseline null rate = 0, alert on any null count > 0 (which is just `not_null`). Document this edge case in the reference.

### 4. First-Run Bootstrapping

Stateful tests have no baseline on the first run. The seed-based pattern (Pattern 1) handles this by requiring explicit baseline seeding. The snapshot pattern (Pattern 2) produces no violations on first run (no previous snapshot to compare against) which is correct but may mask issues.

**Proposed approach:** Document that first-run behavior differs by pattern. Pattern 1 requires seeding before first run. Pattern 2 silently passes first run. Neither is wrong; the user should know.

### 5. Should implement-models Also Get a Rule Type Table?

The `implement-models` reference `dbt-testing-patterns.md` currently maps dimensions to tests. If the quality config now includes rule types, implement-models could read the rule type directly and skip its own mapping. But implement-models must also work without a quality config (graceful degradation).

**Proposed approach:** Keep the dimension-to-test mapping in implement-models as a fallback. When a quality config with rule types exists, use the rule type. When no quality config exists, fall back to dimension-based mapping. This is a follow-up change, not part of this reference file.

### 6. Freshness as a Rule Type vs Source Configuration

Freshness checks are not dbt data tests -- they use `dbt source freshness`, which is a separate command. The reference should list freshness as a rule type but note that it is configured in source YAML (`warn_after`, `error_after`), not in model schema YAML, and is not run by `dbt build`.

## Summary of Deliverables

| Deliverable | Location | Action |
|-------------|----------|--------|
| New reference file | `skills/assess-quality/references/dbt-test-selection.md` | Create |
| SKILL.md update | `skills/assess-quality/SKILL.md` | Edit Steps 4 and 8 + Reference Materials |
| Template update | `skills/assess-quality/assets/quality-config-template.md` | Add Rule Type column |
| designs/_index.md | `docs/designs/_index.md` | Add this document |

## Changelog

| Date | Change |
|------|--------|
| 2026-04-08 | Initial brainstorm document |
