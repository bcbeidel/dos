---
name: Data Quality Scoring
description: "Composite quality scores use weighted dimension aggregation -- score each dimension as a percentage, assign business-driven weights, compute weighted average; scores without action thresholds and defined owners become vanity metrics; Elementary's dbt-native approach demonstrates practical implementation"
type: context
related:
  - docs/research/2026-03-22-quality-engineering.research.md
  - docs/context/data-quality-dimensions.md
  - docs/context/data-profiling.md
  - docs/context/data-quality-slas.md
---

## Key Takeaway

A quality score of 94.2% is meaningless without three things: (1) a defined threshold below which action is required, (2) a defined action to take when the threshold is breached, and (3) a defined owner responsible for taking that action. Without these operational bindings, quality dashboards become the data equivalent of unread email -- technically present, practically ignored. Composite scores serve leadership communication and trend tracking; dimension-level scores serve engineering investigation and remediation. Both are necessary.

## Composite Score Calculation

Weighted dimension aggregation in five steps:

1. **Define dimensions**: Select 4-7 dimensions relevant to the use case (e.g., completeness, accuracy, validity, freshness)
2. **Score each dimension**: Convert measurement results to percentages (e.g., 97% completeness, 92% validity)
3. **Assign weights**: Domain experts assign importance weights that sum to 1.0 (e.g., completeness=0.3, accuracy=0.3, validity=0.2, freshness=0.2)
4. **Compute weighted average**: Quality Score = sum(dimension_score * weight) for all dimensions
5. **Standardize**: Normalize scores before aggregation so different measurement scales integrate equally

Weight assignment is a business decision, not an engineering one. Accuracy may matter more than completeness for financial data, or vice versa for marketing data.

## Elementary's dbt-Native Scoring

Elementary Data implements two scoring methods within the dbt ecosystem:

**Test fail rate**: Each test gets a binary score -- passed=1.0, warning=0.5, failed=0.0 -- averaged across tests within a dimension. Example: 3 passing + 1 warning = (3*1.0 + 1*0.5) / 4 = 87.5%.

**Failed row count**: Dimension scores measure the proportion of affected rows. Formula: (total_rows - failed_rows) / total_rows, averaged across tests. Example: 3 passing tests (1,000 rows each) + 1 test with 100 failures = (3*1.0 + 1*0.9) / 4 = 97.5%.

The failed row count method provides finer granularity -- a test that fails on 1 row out of 1M scores 99.9999% rather than 0.0. Elementary maps common dbt tests to quality dimensions automatically: `not_null` to completeness, `unique` to uniqueness, `accepted_values` to accuracy, `relationships` to consistency.

## Action Thresholds

Three-tier classification is the minimum viable approach:

- **Green (90-100%)**: No action required, data is fit for use
- **Yellow (70-89%)**: Investigation required, data may be degraded
- **Red (below 70%)**: Remediation required, data is unfit for use

Thresholds must be calibrated per use case -- a financial reporting table may require 99.5% completeness at the green threshold, while an internal analytics table may tolerate 95%.

## The Aggregation Tension

Composite scores hide more than they reveal. A score of 92% could mean all dimensions are at 92% (healthy) or that completeness is at 100% while accuracy is at 70% (dangerous). Weighted aggregation partially addresses this -- higher-weighted dimensions pull the composite down more when they degrade. But the fundamental tension between summary metrics and actionable detail remains. The resolution: composite score on the dashboard, dimension drill-down on click.

## Decision Rules

1. Do not ship a quality score without defined action thresholds and an assigned owner.
2. Use business-driven weights, not equal weights. Stakeholders must participate in weight assignment.
3. Prefer Elementary's failed row count method over test fail rate for finer granularity.
4. Display composite scores for communication; expose dimension-level scores for investigation.
5. Calibrate thresholds per data product -- no single threshold set fits all use cases.
