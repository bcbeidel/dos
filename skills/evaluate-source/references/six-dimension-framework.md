# Six-Dimension Source Assessment Framework

Evaluate every source across these six dimensions before writing pipeline code. Each dimension scores 1-5 where 1 = significant risk/complexity and 5 = minimal risk/straightforward.

## Scoring Criteria

### 1. Connectivity

How the source exposes its data. Determines ingestion pattern and tooling.

| Score | Criteria |
|:-----:|----------|
| 5 | Direct database access (JDBC/ODBC), standard protocols, no network restrictions |
| 4 | Well-documented REST API with stable endpoints, or managed file drop (S3) |
| 3 | API with pagination quirks or moderate rate limits; VPN required |
| 2 | Webhook-only (push model), undocumented API, or IP allowlisting required |
| 1 | Multiple auth hops, custom protocols, screen scraping, or no programmatic access |

### 2. Volume

Data size at rest and change rate. Use 95th percentile, not averages — averages mask burst behavior.

| Score | Criteria |
|:-----:|----------|
| 5 | < 1 GB total, < 10K rows/day change rate |
| 4 | 1-10 GB total, < 100K rows/day change rate |
| 3 | 10-100 GB total, < 1M rows/day change rate |
| 2 | 100 GB - 1 TB total, > 1M rows/day change rate |
| 1 | > 1 TB total, or > 10M rows/day change rate, or unpredictable bursts |

### 3. Freshness

Update frequency and reliable timestamp availability. Drives batch vs. micro-batch vs. streaming.

| Score | Criteria |
|:-----:|----------|
| 5 | Daily or less frequent updates, reliable `updated_at` timestamp |
| 4 | Hourly updates, reliable timestamps |
| 3 | Sub-hourly updates, timestamps present but with known gaps or clock skew |
| 2 | Near-real-time updates needed, no reliable timestamp — must use log position or offset |
| 1 | Real-time required, no reliable change tracking mechanism |

### 4. Schema Stability

Change frequency and notification process. Schema drift causes 7.8% of all data quality incidents with 27% compounding per percentage-point increase in drift rate.

| Score | Criteria |
|:-----:|----------|
| 5 | Schema unchanged 12+ months, version-controlled, changes announced in advance |
| 4 | 1-2 changes/year, documented, consumers notified |
| 3 | 3-6 changes/year, partially documented, inconsistent notification |
| 2 | Monthly changes, undocumented, no notification process |
| 1 | Frequent unannounced changes (SaaS APIs), no schema versioning |

**High-risk indicator:** SaaS APIs are the most schema-volatile source type. A 3% monthly change rate does not produce a 3% incident rate — it compounds at 27% per point.

### 5. Data Quality

Baseline quality across DAMA dimensions from profiling results.

| Score | Criteria |
|:-----:|----------|
| 5 | > 99% completeness, consistent types, validated referential integrity |
| 4 | > 95% completeness, minor type inconsistencies, key integrity holds |
| 3 | 90-95% completeness, some nulls in critical fields, occasional duplicates |
| 2 | < 90% completeness, type mismatches, duplicate records, orphaned references |
| 1 | Pervasive quality issues: missing data, inconsistent formats, no key integrity |

### 6. Access Complexity

Authentication, authorization, and operational overhead. Access problems are the most common onboarding blocker.

| Score | Criteria |
|:-----:|----------|
| 5 | Service account with read access, no rate limits, standard auth |
| 4 | OAuth M2M or API key, reasonable rate limits (> 1000 req/min) |
| 3 | OAuth with token refresh, moderate rate limits, or per-endpoint auth differences |
| 2 | IP allowlisting + VPN + multi-step auth, or strict rate limits (< 100 req/min) |
| 1 | Manual approval workflows, complex token chains, undocumented auth, or no API auth available |

## Composite Score

Average the six dimensions for an overall risk profile:

| Range | Interpretation |
|:-----:|---------------|
| 4.0 - 5.0 | Low risk — straightforward onboarding |
| 3.0 - 3.9 | Moderate risk — plan for specific mitigations |
| 2.0 - 2.9 | High risk — defensive pipeline design required |
| 1.0 - 1.9 | Very high risk — evaluate whether the source is viable |

## Minimum Viable Assessment

For any new source, validate at minimum:
1. Access connectivity works (dimension 1 + 6)
2. Data profiling establishes quality baseline (dimension 5)
3. Schema stability assessed over past 6-12 months (dimension 4)
