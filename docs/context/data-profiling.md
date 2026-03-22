---
name: Data Profiling
description: "Data profiling (structure, content, relationship analysis) is the measurement foundation for data quality -- you cannot score quality without first understanding shape, distribution, completeness, and cardinality; profiling must be continuous, not one-time"
type: context
related:
  - docs/research/2026-03-22-quality-engineering.research.md
  - docs/context/data-quality-dimensions.md
  - docs/context/anomaly-drift-detection.md
  - docs/context/data-quality-scoring.md
---

## Key Takeaway

Data profiling must precede any quality measurement because you cannot score what you have not characterized. Without knowing a column's distribution, cardinality, and null rate, quality rules are guesses rather than informed assertions. Profiling is not a one-time activity -- initial profiling establishes baselines, ongoing profiling detects drift, and periodic re-profiling updates baselines as data legitimately evolves.

## Three Types of Profiling

**Structure profiling** examines metadata and format: column names, data types, field lengths, constraints, and naming consistency. This answers "What shape is the data?" -- the most basic question before any quality assessment.

**Content profiling** examines actual values: null/missing value rates, value distributions (frequency histograms), outlier detection, format pattern analysis, and range validation. Key metrics include completeness (percentage of non-null values), uniqueness (distinct values / total values), and cardinality (count of distinct values per column). Descriptive statistics -- min, max, mean, median, mode, standard deviation, percentiles (25th, 50th, 75th) -- characterize numeric distributions.

**Relationship profiling** examines connections across columns and tables: primary/foreign key integrity, cross-column dependencies, orphaned records, circular references, and referential consistency. Critical for data spanning multiple tables or systems.

## Core Profiling Metrics

Profiling outputs map directly to quality dimensions:

| Metric | Calculation | Quality Dimension |
|--------|-------------|-------------------|
| Null rate | NULL count / total rows | Completeness |
| Distinct count | COUNT(DISTINCT column) | Cardinality |
| Uniqueness ratio | Distinct count / total rows | Uniqueness |
| Value frequency | COUNT per distinct value | Distribution |
| Min/max range | MIN(column), MAX(column) | Validity |
| Standard deviation | STDDEV(column) | Distribution shape |
| Pattern frequency | Regex match count / total | Validity |

Cardinality analysis deserves specific attention: a column with cardinality equal to row count is a candidate primary key; very low cardinality (e.g., 3 values in 10M rows) indicates a categorical field; cardinality that changes unexpectedly between profiling runs signals a data issue.

## Continuous Profiling Workflow

The four-step cycle: (1) profile to understand current state, (2) define quality rules based on profiles, (3) monitor against those rules, (4) re-profile periodically to update baselines. Tools range from enterprise platforms (Ataccama, Talend) to open-source options (YData Profiling, Soda Core).

## Decision Rules

1. Profile data before writing quality rules. Rules without profiling are assumptions.
2. Run all three profiling types -- structure, content, and relationship -- on initial ingestion.
3. Schedule ongoing content profiling to detect drift between baseline updates.
4. Use cardinality analysis to validate key candidates and detect categorical field corruption.
5. Re-profile periodically to update baselines as data legitimately evolves.
