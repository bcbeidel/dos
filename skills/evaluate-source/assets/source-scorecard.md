---
name: {{name}}
artifact_type: source-evaluation
version: 1.0.0
owner: {{owner}}
status: draft
last_modified: {{date}}
---

# Source Evaluation: {{name}}

## Source Metadata

| Field | Value |
|-------|-------|
| **Source Name** | {{name}} |
| **Source Type** | {{transactional DB / event stream / SaaS API / file-based}} |
| **Owner** | {{team or individual who owns the source system}} |
| **Data Format** | {{JSON / CSV / Parquet / database tables / API responses}} |
| **Location** | {{connection string, API base URL, S3 path, etc.}} |
| **Business Purpose** | {{what decision will be made with this data}} |

## Source Classification

**Classification:** {{transactional DB / event stream / SaaS API / file-based}}

**Rationale:** {{why this classification was chosen — primary access mechanism, update pattern}}

## Six-Dimension Assessment

| Dimension | Score (1-5) | Evidence |
|-----------|:-----------:|----------|
| **Connectivity** | {{score}} | {{how the source exposes data: JDBC, REST, stream, file, webhook}} |
| **Volume** | {{score}} | {{data size at rest and change rate — use 95th percentile, not averages}} |
| **Freshness** | {{score}} | {{update frequency, reliable timestamp availability}} |
| **Schema Stability** | {{score}} | {{change frequency and notification process over past 6-12 months}} |
| **Data Quality** | {{score}} | {{baseline across DAMA dimensions from profiling}} |
| **Access Complexity** | {{score}} | {{auth mechanism, rate limits, IP restrictions, token refresh}} |

**Scoring Guide:** 1 = significant risk/complexity, 5 = minimal risk/straightforward. See [six-dimension-framework](../references/six-dimension-framework.md) for detailed criteria.

**Composite Score:** {{average or weighted average}} / 5

## Authentication & Credential Management

### Authentication Mechanism

| Field | Value |
|-------|-------|
| **Mechanism** | {{OAuth M2M / API key / service account / key-pair / JDBC credentials}} |
| **Token Lifetime** | {{e.g., 1h for OAuth, indefinite for API key}} |
| **Rotation Cadence** | {{e.g., automatic 1h / manual quarterly / never}} |

### Credential Management Assessment

| Criterion | Status |
|-----------|--------|
| Secrets stored in a secrets manager (not code/config files) | {{yes / no}} |
| Rotation automated or scheduled | {{yes / no / N/A}} |
| No shared credentials across environments | {{yes / no}} |
| No static PATs in production | {{yes / no}} |

**Anti-patterns detected:** {{list any: static PATs, shared credentials, secrets in code, no rotation}}

## Datasets

A single source may contain multiple datasets (e.g., tables in a database, endpoints in an API). List all datasets relevant to downstream data products. Each dataset gets its own profiling subsection below.

| Dataset | Description | Estimated Rows | Update Frequency |
|---------|-------------|:--------------:|-----------------|
| {{dataset_name}} | {{what this dataset contains}} | {{count}} | {{frequency}} |

## Data Profiling Results

**Profiling date:** {{date}}
**Sample size:** {{row count and sampling method if not full dataset}}

Repeat the profiling sections below for each dataset in this source. For sources with a single dataset, use one section.

### Dataset: {{dataset_name}}

#### Structure Profiling

| Column | Inferred Type | Nullable | Field Length | Naming Convention |
|--------|---------------|:--------:|-------------|-------------------|
| {{column_name}} | {{type}} | {{yes/no}} | {{min-max}} | {{snake_case / camelCase / mixed}} |

#### Content Profiling

| Column | Null Count | Null Rate | Distinct Count | Uniqueness Ratio | Min | Max |
|--------|:----------:|:---------:|:--------------:|:----------------:|-----|-----|
| {{column_name}} | {{count}} | {{pct}} | {{count}} | {{ratio}} | {{min}} | {{max}} |

#### Numeric Distribution

For numeric columns only. Skewness indicates distribution shape: 0 = symmetric, positive = right-skewed (long tail of high values), negative = left-skewed.

| Column | Mean | Std Dev | P25 | Median | P75 | IQR | Skewness |
|--------|-----:|--------:|----:|-------:|----:|----:|---------:|
| {{column_name}} | {{mean}} | {{stddev}} | {{p25}} | {{median}} | {{p75}} | {{iqr}} | {{skewness}} |

**Distribution notes:** {{any notable patterns, outliers, or skew}}

#### Relationship Profiling

| Relationship | Type | Status |
|-------------|------|--------|
| {{column → target_table.column}} | {{PK candidate / FK candidate / unique constraint}} | {{valid / orphans detected / not assessed}} |

**Key candidates:** {{columns that could serve as primary keys based on uniqueness ratio}}
**Referential integrity:** {{assessment if multi-table source}}

#### Quality Dimension Baselines

| Quality Dimension | Baseline Value | Derived From |
|-------------------|---------------|--------------|
| Completeness | {{pct non-null across required fields}} | Content profiling |
| Uniqueness | {{pct unique on key candidates}} | Content profiling |
| Validity | {{pct within expected ranges/patterns}} | Content profiling |
| Consistency | {{cross-field consistency rate}} | Relationship profiling |

## Ingestion Recommendation

| Field | Recommendation |
|-------|---------------|
| **Approach** | {{full load / incremental (cursor-based) / incremental (merge) / CDC (log-based)}} |
| **Rationale** | {{based on classification and dimension scores}} |
| **Tool** | {{dlt (polling/extraction) / Debezium (CDC) / platform-native CDC}} |
| **Incremental Key** | {{column used for cursor or merge key, if applicable}} |
| **Initial Load Strategy** | {{full backfill then switch to incremental}} |

**Important:** dlt is a polling/extraction tool, not CDC. If log-based change capture is needed for high-frequency transactional sources, use Debezium or platform-native CDC.

## Re-Profiling Cadence

| Schema Stability Score | Recommended Cadence |
|:----------------------:|-------------------|
| 1-2 (high drift) | Monthly |
| 3 (moderate) | Quarterly |
| 4-5 (stable) | Semi-annually |

**Recommended cadence for this source:** {{cadence based on schema stability score}}
**Next profiling date:** {{date}}

## Next Steps

Based on this evaluation, the recommended next skills are:

1. **`/dos:scope-data-product`** — Define what the data product needs to be, driven by consumption intent. The source evaluation pre-populates known facts about source classification, profiling baselines, and ingestion approach.
2. **`/dos:design-pipeline`** — If the pipeline architecture is the immediate concern, this skill consumes the source classification and ingestion recommendation directly.

## Changelog

| Date | Version | Change | Author |
|------|---------|--------|--------|
| {{date}} | 1.0.0 | Initial evaluation | {{author}} |
