---
name: Data Quality Dimensions
description: "Data quality is context-dependent ('fitness for use'), not absolute; the six-dimension consensus (accuracy, completeness, consistency, timeliness, validity, uniqueness) is a communication starting point, not a specification to adopt wholesale; dimension selection is a design decision driven by use case"
type: context
related:
  - docs/research/2026-03-22-quality-engineering.research.md
  - docs/context/data-profiling.md
  - docs/context/data-quality-scoring.md
  - docs/context/data-quality-slas.md
  - docs/context/data-freshness-slas.md
---

## Key Takeaway

Data quality is not a binary property. The same dataset can be high quality for one use case and poor for another. A 5% null rate in an email column is acceptable for aggregate analytics but catastrophic for a marketing email campaign. Quality assessment must start with defining who uses the data, for what purpose, and with what tolerance. Table-level quality scores without consumer context are technically measurable but operationally meaningless. Define quality contracts per data product and per consumer -- not per table.

## The Six-Dimension Consensus

The industry has converged on six core dimensions, adopted by IBM, DAMA, and dbt Labs:

1. **Accuracy** -- How closely data represents reality. Validated against trusted reference sources, statistical sampling, or cross-system reconciliation.
2. **Completeness** -- Whether all required records and fields are present. Measured by null rate (NULL count / total rows) and volume against expected row counts.
3. **Consistency** -- Whether data agrees across systems and within itself. Measured by cross-system comparison and referential integrity checks.
4. **Timeliness** -- Whether data is available when needed. Measured by the delta between event occurrence and data availability.
5. **Validity** -- Whether data conforms to defined formats, types, and business rules. Measured by regex pattern matching, range checks, and accepted-value validation.
6. **Uniqueness** -- Whether data is free of unintended duplicates. Measured by duplicate row detection and primary key violation rate.

## The Proliferation Problem

Six dimensions is a useful starting vocabulary, but the real landscape is broader. Wang & Strong's foundational 1996 paper defined 15 dimensions across four categories (intrinsic, contextual, representational, accessibility). DAMA NL's 2020 research identified 60 standardized dimensions and found 127 distinct definitions across literature. Different organizations adopt different subsets -- Collibra replaces timeliness with integrity; PricewaterhouseCoopers substitutes uniqueness with integrity; the US Department of Interior uses 11 dimensions.

The 127-dimension count sounds like fragmentation beyond usefulness, but many are synonyms, overlapping concepts, or context-specific variants. The proliferation actually validates the "fitness for use" principle: dimensions proliferate because quality requirements are context-dependent.

## Dimension Selection as a Design Decision

Select 4-10 dimensions based on specific use cases, data characteristics, and stakeholder needs. The process:

1. Identify the data product and its consumers
2. Determine which quality properties matter most to those consumers
3. Select dimensions that map to those properties
4. Define measurement methods and thresholds per dimension
5. Revisit selection as use cases evolve

The six-dimension consensus works as a communication tool and starting taxonomy. Treating it as exhaustive misses context-specific dimensions like usefulness (is the data actually consumed?) and freshness (distinct from timeliness -- how recently was data updated?).

## Decision Rules

1. Define quality context before measurement -- who uses this data, for what, with what tolerance.
2. Start with the six-dimension consensus as vocabulary, then extend with domain-specific dimensions.
3. Do not adopt all dimensions from any framework wholesale. Dimension selection is a design decision.
4. Quality rules, thresholds, and SLAs must be defined per data product and per consumer.
