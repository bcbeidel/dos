---
name: {{name}}
artifact_type: quality-config
version: 1.0.0
owner: {{owner}}
status: draft
last_modified: {{date}}
---

# Quality Configuration: {{name}}

## Data Product Context

| Field | Value |
|-------|-------|
| **Data Product** | {{name}} |
| **Owner** | {{owner}} |
| **Primary Consumers** | {{list consumers and their use cases}} |
| **Quality Context** | {{what "fit for use" means for this product}} |

## Quality Dimensions

Selected dimensions with measurement methods and thresholds. Dimensions are chosen based on consumer needs and data characteristics -- not adopted wholesale from a framework.

| Dimension | Rule Type | Measurement Method | Threshold (Green) | Threshold (Yellow) | Threshold (Red) |
|-----------|-----------|-------------------|:-----------------:|:------------------:|:---------------:|
| **Completeness** | not-null | `(total_rows - null_count) / total_rows` for required fields | >= {{pct}}% | >= {{pct}}% | < {{pct}}% |
| **Accuracy** | {{expression / aggregate-bound}} | Cross-reference against {{trusted source}} or statistical sampling | >= {{pct}}% | >= {{pct}}% | < {{pct}}% |
| **Validity** | {{enum-membership / string-pattern / numeric-range / expression}} | {{measurement per rule type}} | >= {{pct}}% | >= {{pct}}% | < {{pct}}% |
| **Uniqueness** | {{unique / unique-combination}} | Duplicate row detection and primary key violation rate | >= {{pct}}% | >= {{pct}}% | < {{pct}}% |
| **Consistency** | {{referential-integrity / metric-stability}} | {{referential checks or run-over-run comparison}} | >= {{pct}}% | >= {{pct}}% | < {{pct}}% |
| **Timeliness** | {{recency / freshness}} | Delta between event occurrence and data availability | <= {{minutes}} min | <= {{minutes}} min | > {{minutes}} min |

**Note:** Select 4-10 dimensions relevant to this data product. Remove rows that do not apply. Add domain-specific dimensions as needed. Rule types use the taxonomy from `dbt-test-selection.md` -- downstream skills use the rule type to select the correct dbt test implementation.

## Scoring Method

**Method:** {{test fail rate / failed row count}}

**Recommended:** Failed row count provides finer granularity. A test failing on 1 row out of 1M scores 99.9999% rather than 0.0.

- **Test fail rate:** Each test gets a binary score -- passed=1.0, warning=0.5, failed=0.0, averaged across tests within a dimension.
- **Failed row count:** Dimension scores measure the proportion of affected rows: `(total_rows - failed_rows) / total_rows`, averaged across tests.

## Dimension Weights

Weights are business-driven. Stakeholders must participate in assignment. Weights sum to 1.0.

| Dimension | Weight | Justification |
|-----------|:------:|---------------|
| {{dimension}} | {{weight}} | {{why this weight for this consumer}} |
| {{dimension}} | {{weight}} | {{why this weight for this consumer}} |
| {{dimension}} | {{weight}} | {{why this weight for this consumer}} |
| {{dimension}} | {{weight}} | {{why this weight for this consumer}} |

**Composite Score Formula:**

```
Quality Score = SUM(dimension_score * weight) for all dimensions
```

Normalize dimension scores to percentages before aggregation so different measurement scales integrate equally.

## Action Thresholds

Composite score thresholds with assigned owners and required actions.

| Threshold | Score Range | Action Required | Owner |
|-----------|:----------:|-----------------|-------|
| **Green** | {{90-100%}} | No action required. Data is fit for use. | {{owner}} |
| **Yellow** | {{70-89%}} | Investigation required. Data may be degraded. Identify root cause within {{SLA}}. | {{owner}} |
| **Red** | {{below 70%}} | Remediation required. Data is unfit for use. Block downstream consumption until resolved. | {{owner}} |

**Per-dimension overrides:** Critical dimensions may have stricter thresholds than the composite. List any overrides below.

| Dimension | Override Threshold | Action | Owner |
|-----------|:-----------------:|--------|-------|
| {{dimension}} | Red below {{pct}}% | {{action}} | {{owner}} |

## Validation Tooling by Tier

| Tier | Environment | Tools | Tests Run |
|------|------------|-------|-----------|
| **Tier 1** | Local development | Pandera + pytest, dbt unit tests | Schema validation on sample data, transformation logic, edge cases |
| **Tier 2** | CI pipeline | dbt data tests + dbt-expectations (Metaplane fork) | Full test suite against CI warehouse, data diffing on PR |
| **Tier 3** | Production | Soda / Great Expectations, dbt source freshness | Continuous monitoring, anomaly detection, freshness checks |

**Scaling guidance:** Teams under 5 engineers should start with dbt tests in CI and production, add Pandera for Python-heavy pipelines, and defer Soda/GE until dedicated platform capacity exists.

## Anomaly Detection Approach

**Current maturity:** {{rule-based only / statistical / hybrid}}

| Layer | Method | Applied To | Threshold |
|-------|--------|-----------|-----------|
| **Rule-based** | Known constraint checks | {{fields/metrics}} | {{thresholds}} |
| **Statistical** | {{z-score / IQR / SPC control charts}} | {{fields/metrics}} | {{e.g., |z| > 3, Tukey's fences}} |
| **Distribution drift** | {{KS test / Wasserstein Distance / PSI}} | {{fields/metrics}} | {{e.g., p < 0.05, distance > threshold}} |

**Method selection:**
- Point anomalies on normal distributions: z-score
- Point anomalies on skewed distributions: IQR
- Time-series monitoring (row counts, null rates): SPC control charts
- Distribution drift on small datasets (<1K rows): KS test
- Distribution drift on large datasets (100K+ rows): Wasserstein Distance

**Maturity progression:** Rules-only (start here) -> statistical methods -> ML-based detection (only at scale with 100K+ observations).

## SLA Configuration

When a scope document exists, these values should match the SLA dimensions defined in `docs/data-products/<name>/scope.md`. The scope document is the authoritative SLA agreement; this section tracks the operational measurement infrastructure.

| SLA Dimension | SLI (Measured Metric) | SLO (Internal Target) | SLA (Commitment) | Error Budget |
|---------------|----------------------|----------------------|-------------------|-------------|
| Timeliness | {{metric}} | {{target}} | {{commitment}} | {{budget}} |
| Completeness | {{metric}} | {{target}} | {{commitment}} | {{budget}} |

**Error budget consumption rules:**
- Budget > 50% remaining: Ship new features confidently
- Budget 25-50% remaining: Review consumption, slow risky changes
- Budget < 25% remaining: Freeze new features, focus on reliability

**Tier:** {{Tier 1 (customer-facing) / Tier 2 (operational) / Tier 3 (analytical)}}

## Next Steps

1. **`/dos:implement-models`** -- Implement the dbt models with quality tests embedded based on this configuration. The quality config drives which generic and singular tests are applied per model.
2. **`/dos:define-contract`** -- If a data contract does not yet exist, define one. The quality config provides the measurement side; the contract provides the commitment side.

## Changelog

| Date | Version | Change | Author |
|------|---------|--------|--------|
| {{date}} | 1.0.0 | Initial quality configuration | {{author}} |
