# Quality Dimension Selection

Data quality is "fitness for use" — the same dataset can be high quality for one use case and poor for another. A 5% null rate in email is acceptable for aggregate analytics but catastrophic for a marketing campaign.

## The Six-Dimension Consensus

Industry-standard starting vocabulary adopted by IBM, DAMA, and dbt Labs:

| Dimension | Definition | Measurement Approach |
|-----------|-----------|---------------------|
| **Accuracy** | How closely data represents reality | Validation against trusted references, statistical sampling, cross-system reconciliation |
| **Completeness** | Whether all required records and fields are present | Null rate (NULL count / total rows), volume vs expected row counts |
| **Consistency** | Whether data agrees across systems and within itself | Cross-system comparison, referential integrity checks |
| **Timeliness** | Whether data is available when needed | Delta between event occurrence and data availability |
| **Validity** | Whether data conforms to formats, types, business rules | Regex pattern matching, range checks, accepted-value validation |
| **Uniqueness** | Whether data is free of unintended duplicates | Duplicate row detection, primary key violation rate |

## Dimension Selection Process

Select 4-10 dimensions based on use case. Do not adopt all dimensions from any framework wholesale.

1. **Identify the data product and its consumers**
2. **Determine which quality properties matter most** to those consumers
3. **Select dimensions** that map to those properties
4. **Define measurement methods and thresholds** per dimension
5. **Revisit selection** as use cases evolve

## Starting Recommendations

| Data Product Type | Start With | Add If Needed |
|-------------------|-----------|---------------|
| Financial reporting | Accuracy, Completeness, Timeliness | Consistency (cross-system reconciliation) |
| Operational dashboards | Timeliness, Completeness | Validity (format/range checks) |
| ML feature stores | Accuracy, Completeness, Uniqueness | Consistency (feature drift) |
| Customer-facing data | Accuracy, Validity, Uniqueness | Timeliness (freshness SLAs) |
| General analytics | Completeness, Validity, Timeliness | Accuracy (if decisions depend on precision) |

## Mapping Profiling Baselines to Dimensions

| Profiling Result | Quality Dimension | Derivation |
|-----------------|-------------------|------------|
| Null rates | Completeness | NULL count / total rows per required field |
| Uniqueness ratios on key candidates | Uniqueness | Distinct count / total rows on key columns |
| Values within ranges/patterns | Validity | % within expected ranges or matching patterns |
| Cross-field consistency | Consistency | % of records passing cross-field checks |

## Decision Rules

1. Define quality context before measurement — who uses this data, for what, with what tolerance.
2. Start with the six-dimension consensus as vocabulary, then extend with domain-specific dimensions.
3. Quality rules and thresholds must be defined per data product and per consumer.
4. Table-level quality scores without consumer context are technically measurable but operationally meaningless.
