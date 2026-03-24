# Scoring Methods

A quality score is meaningless without: (1) a defined threshold below which action is required, (2) a defined action to take, and (3) a defined owner responsible for taking it. Without these, quality dashboards become the data equivalent of unread email.

## Two Scoring Methods

**Test fail rate:** Each test gets a binary score -- passed=1.0, warning=0.5, failed=0.0 -- averaged across tests within a dimension. Example: 3 passing + 1 warning = (3*1.0 + 1*0.5) / 4 = 87.5%.

**Failed row count:** Dimension scores measure the proportion of affected rows. Formula: `(total_rows - failed_rows) / total_rows`, averaged across tests. Example: 3 passing tests (1,000 rows each) + 1 test with 100 failures = (3*1.0 + 1*0.9) / 4 = 97.5%.

**Recommended:** Failed row count provides finer granularity -- a test failing on 1 row out of 1M scores 99.9999% rather than 0.0.

## Weighted Aggregation (5-Step Process)

1. **Define dimensions** -- Select 4-7 dimensions relevant to the use case
2. **Score each dimension** -- Convert measurement results to percentages
3. **Assign weights** -- Domain experts assign importance weights summing to 1.0
4. **Compute weighted average** -- `Quality Score = SUM(dimension_score * weight)`
5. **Standardize** -- Normalize scores before aggregation so different measurement scales integrate equally

Weight assignment is a business decision, not an engineering one. Stakeholders must participate.

## Score Interpretation

- **Composite scores** serve leadership communication and trend tracking
- **Dimension-level scores** serve engineering investigation and remediation
- Both are necessary -- composite on the dashboard, dimension drill-down on click

A score of 92% could mean all dimensions are at 92% (healthy) or completeness at 100% while accuracy is at 70% (dangerous). Weighted aggregation partially addresses this.

## Action Thresholds

Three-tier classification (minimum viable):

| Threshold | Score Range | Action |
|-----------|:----------:|--------|
| **Green** | 90-100% | No action required, data is fit for use |
| **Yellow** | 70-89% | Investigation required, data may be degraded |
| **Red** | Below 70% | Remediation required, data is unfit for use |

Calibrate thresholds per data product -- no single threshold set fits all use cases.

## Decision Rules

1. Do not ship a quality score without defined action thresholds and an assigned owner.
2. Use business-driven weights, not equal weights. Stakeholders must participate.
3. Prefer failed row count over test fail rate for finer granularity.
4. Display composite scores for communication; expose dimension-level scores for investigation.
5. Calibrate thresholds per data product.
