---
name: Source System Evaluation
description: "Six-dimension assessment framework for evaluating new data sources before pipeline construction -- connectivity, volume, freshness, schema stability, data quality, and access complexity; source classification (transactional, event stream, SaaS API, file-based) constrains ingestion approach"
type: context
related:
  - docs/research/2026-03-22-data-discovery.research.md
  - docs/context/incremental-loading-patterns.md
  - docs/context/schema-drift-risk.md
  - docs/context/data-contracts.md
  - docs/context/data-source-onboarding.md
---

## Key Takeaway

Evaluate every source system across six dimensions before writing pipeline code. These dimensions are not a one-time checklist -- they define the constraints that determine ingestion approach, error handling, monitoring configuration, and maintenance burden. Teams that skip this assessment consistently discover the same problems at higher cost: access failures during deployment, quality issues during stakeholder review, schema changes during the first production incident.

## The Six Evaluation Dimensions

**1. Connectivity** -- How does the source expose its data? Direct database access (JDBC/ODBC), REST API, event stream (Kafka/Kinesis), file drop (SFTP/S3), or webhook. Connectivity determines the fundamental ingestion pattern and tooling. Each access method has different failure modes, retry semantics, and throughput ceilings.

**2. Volume** -- Data size at rest and change rate over time. Volume determines whether full loads are feasible or incremental loading is required. Use the 95th percentile rather than averages for capacity planning -- averages mask burst behavior.

**3. Freshness** -- How frequently does the source update, and how stale can data be before it loses value? Freshness drives the choice between batch (hours/daily), micro-batch (minutes), and streaming (seconds). The source must expose a reliable timestamp field (e.g., `updated_at`) to support incremental extraction.

**4. Schema stability** -- How frequently does the source schema change, and are changes announced? Schema drift causes 7.8% of all data quality incidents, and incidents increase 27% per percentage-point rise in drift rate. Sources with high volatility (particularly SaaS APIs) require schema validation at ingestion time.

**5. Data quality** -- Baseline quality across DAMA-DMBOK dimensions: accuracy, completeness, consistency, timeliness, validity, uniqueness. A source with known quality issues requires defensive pipeline design -- validation gates, quarantine tables, and reconciliation checks.

**6. Access complexity** -- Authentication, authorization, and operational overhead. Ranges from simple (service account with read access) to highly complex (OAuth2 token refresh, IP allowlisting, VPN tunnels, per-endpoint rate limits). Access problems are the most common onboarding blocker.

## Source Classification Constrains Ingestion Approach

Source type determines available ingestion methods -- this is not a free choice.

| Source Type | Examples | Key Constraints | Typical Ingestion |
|---|---|---|---|
| Transactional DB | PostgreSQL, MySQL, Oracle | Extraction load on source; need reliable timestamps for incremental | Full load, incremental, or CDC |
| Event stream | Kafka, Kinesis, Pub/Sub | Retention period; schema registry; partition strategy | Streaming consumers |
| SaaS API | Salesforce, Stripe, HubSpot | Rate limits, pagination, vendor-controlled auth; most volatile type | API extraction (managed connectors preferred) |
| File-based | CSV/JSON via SFTP, S3 | No query interface; format consistency; silent delivery gaps | Polling or event-driven detection |

## Ingestion Approach Decision

| Question | Full Load | Incremental | CDC |
|---|---|---|---|
| Change frequency? | Rare | Moderate, regular | High frequency |
| Must track hard deletes? | No | No | Yes |
| Freshness requirement? | Hours/daily | Hours/daily | Minutes/real-time |
| Source system impact? | Query load | Query load | Log-based (lower impact) |

Most production environments use a hybrid: full loads for small dimensions, incremental for regular fact tables, CDC for high-value transactional data. CDC's critical advantage is reading the transaction log rather than running queries, reducing CPU/IO pressure on the source.

## Minimum Viable Assessment

For any new source, validate at minimum: (1) access connectivity works, (2) data profiling establishes quality baseline, and (3) schema stability is assessed over the past 6-12 months. Everything else can be refined iteratively.
