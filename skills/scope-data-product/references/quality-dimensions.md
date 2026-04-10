# Quality Dimensions

Data quality is context-dependent ("fitness for use"), not absolute. The same dataset can be high quality for one use case and poor for another. A 5% null rate in an email column is acceptable for aggregate analytics but catastrophic for a marketing email campaign.

## Six-Dimension Consensus

The industry has converged on six core dimensions (IBM, DAMA, dbt Labs):

1. **Accuracy** -- How closely data represents reality. Validated against trusted reference sources, statistical sampling, or cross-system reconciliation.
2. **Completeness** -- Whether all required records and fields are present. Measured by null rate (NULL count / total rows) and volume against expected row counts.
3. **Consistency** -- Whether data agrees across systems and within itself. Measured by cross-system comparison and referential integrity checks.
4. **Timeliness** -- Whether data is available when needed. Measured by the delta between event occurrence and data availability.
5. **Validity** -- Whether data conforms to defined formats, types, and business rules. Measured by regex pattern matching, range checks, and accepted-value validation.
6. **Uniqueness** -- Whether data is free of unintended duplicates. Measured by duplicate row detection and primary key violation rate.

## Dimension Selection as a Design Decision

The six-dimension consensus is a communication starting point, not a specification to adopt wholesale. Wang & Strong (1996) defined 15 dimensions; DAMA NL (2020) identified 60 standardized and 127 distinct definitions across literature. Dimensions proliferate because quality requirements are context-dependent.

**Select 4-10 dimensions** based on:

1. Identify the data product and its consumers
2. Determine which quality properties matter most to those consumers
3. Select dimensions that map to those properties
4. Define measurement methods and thresholds per dimension
5. Revisit selection as use cases evolve

Consider domain-specific dimensions beyond the six: usefulness (is the data actually consumed?), freshness (distinct from timeliness -- how recently was data updated?).

## Decision Rules

1. Define quality context before measurement -- who uses this data, for what, with what tolerance.
2. Start with the six-dimension consensus as vocabulary, then extend with domain-specific dimensions.
3. Do not adopt all dimensions from any framework wholesale. Dimension selection is a design decision.
4. Quality rules, thresholds, and SLAs must be defined per data product and per consumer.
