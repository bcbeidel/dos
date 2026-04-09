# Profiling Metrics Reference

Profile data before writing quality rules. Rules without profiling are assumptions.

## Three Profiling Types

### 1. Structure Profiling

Examines metadata and format — "What shape is the data?"

| Metric | What It Reveals |
|--------|----------------|
| Column names | Naming conventions (snake_case, camelCase, mixed) |
| Data types | Type consistency, implicit type coercion risks |
| Field lengths | Min/max string lengths, fixed vs variable |
| Constraints | NOT NULL, UNIQUE, CHECK constraints present in source |
| Naming consistency | Whether the source follows a consistent convention |

### 2. Content Profiling

Examines actual values — distributions, completeness, validity.

| Metric | Calculation | Quality Dimension |
|--------|-------------|-------------------|
| Null count | `COUNT(*) - COUNT(column)` | Completeness |
| Null rate | `NULL count / total rows` | Completeness |
| Distinct count | `COUNT(DISTINCT column)` | Cardinality |
| Uniqueness ratio | `Distinct count / total rows` | Uniqueness |
| Value frequency | `COUNT per distinct value` | Distribution |
| Min / Max | `MIN(column)`, `MAX(column)` | Validity (range) |
| Mean / Median | `AVG(column)`, `PERCENTILE_CONT(0.5)` | Central tendency |
| Standard deviation | `STDDEV(column)` | Distribution shape |
| Percentiles (25th, 50th, 75th) | `PERCENTILE_CONT(0.25/0.5/0.75)` | Distribution spread |
| Pattern frequency | `Regex match count / total` | Validity (format) |

**Cardinality analysis:**
- Cardinality = row count → candidate primary key
- Very low cardinality (e.g., 3 values in 10M rows) → categorical field
- Unexpected cardinality change between runs → data issue signal

### 3. Relationship Profiling

Examines connections across columns and tables.

| Metric | What It Reveals |
|--------|----------------|
| Key candidates | Columns with uniqueness ratio = 1.0 |
| Foreign key candidates | Columns whose values are a subset of another column's distinct values |
| Referential integrity | % of FK values that exist in the referenced table |
| Orphan records | FK values with no matching parent record |
| Cross-column dependencies | Functional dependencies between columns |

## Profiling → Quality Dimension Mapping

| Profiling Output | Quality Dimension | Baseline Derivation |
|-----------------|-------------------|-------------------|
| Null rate per column | Completeness | `1 - null_rate` = completeness score |
| Uniqueness ratio on key candidates | Uniqueness | Direct measure |
| Values within expected ranges/patterns | Validity | `in_range_count / total` |
| Cross-field consistency checks | Consistency | `consistent_count / total` |
| Referential integrity rate | Integrity | `matched_fk / total_fk` |
| Freshness of latest timestamp | Timeliness | `now - max(updated_at)` |

## Sampling & Representativeness

Profiling results are only as good as the data profiled. A biased sample produces misleading baselines.

### When to suspect a non-representative sample

| Signal | Risk |
|--------|------|
| Row count is a round number (500, 1000, 5000) | Likely a `--limit` flag — source ordering may cluster edge cases |
| Sample is <1% of total population | Distribution metrics may not reflect population proportions |
| Source API returns deterministic order (alphabetical, by ID, by date) | First-page samples over-represent one segment |
| All enrichment/derived fields are null | Sample may hit un-enriched records (geographic or temporal bias) |

### Sampling strategies for paginated APIs

| Strategy | When to Use |
|----------|------------|
| First page only | Quick schema check — **not for distribution baselines** |
| First + middle + last page | Minimum viable representative sample |
| Stratified by parameter (geography, type, date range) | API has categorical distribution; each category needs representation |
| Full extraction with `--limit` on processing | Large APIs where full extraction is feasible but analysis is expensive |

**Minimum sample size:** 100 records for baseline profiling. Below 100, flag the profile as insufficient for distribution metrics.

### Recording sampling provenance

Every profile should record:
- **Sample size** — how many rows were profiled
- **Total population** — how many rows exist in the source (if known)
- **Sampling method** — full scan, first N rows, stratified pages, random
- **Warnings** — any caveats about representativeness

The profiling script accepts `--sample-of N` to record total population and automatically flags suspicious sample sizes (round numbers, small fractions).

## Re-Profiling Cadence

| Schema Stability | Recommended Cadence |
|:----------------:|-------------------|
| High drift (score 1-2) | Monthly |
| Moderate (score 3) | Quarterly |
| Stable (score 4-5) | Semi-annually |

Profiling is continuous, not one-time. Initial profiling establishes baselines; ongoing profiling detects drift; periodic re-profiling updates baselines as data legitimately evolves.
