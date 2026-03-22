---
name: Audit Trail Design
description: "Compliant audit trails require immutable append-only storage, SHA-256 hash chains for tamper evidence, and separation of duties; OpenTelemetry + S3 Object Lock is a practical implementation; Snowflake/Databricks native audit retention is insufficient for SOX (7yr) and HIPAA (6yr)"
type: context
related:
  - docs/research/2026-03-22-governance-compliance.research.md
  - docs/context/data-governance-foundations.md
  - docs/context/row-column-security-comparison.md
---

## Key Insight

Three properties define a compliant audit trail: immutability (events cannot be modified after writing), integrity (tampering is detectable), and separation of duties (system operators cannot alter audit records). Every data platform -- Snowflake, Databricks, ClickHouse -- has native audit retention gaps that require external supplementary infrastructure for multi-year regulatory compliance.

## What Audit Events Must Capture

Every audit event records six elements:

1. **Actor identity** -- who (user, service account)
2. **Action performed** -- what (SELECT, UPDATE, GRANT)
3. **Target resource** -- which table, column, or row
4. **Timestamp** -- when (UTC, ISO-8601)
5. **Origin** -- source IP, service account, session
6. **Outcome** -- success or failure with error detail

For data pipelines, events must also capture pipeline run ID, stage identifier, and data lineage context -- which upstream sources fed the operation and which downstream consumers are affected.

## Immutable Storage Mechanisms

Three mechanisms enforce immutability for SOX Section 404, HIPAA audit controls, and SOC 2 Type II:

**Append-only storage** -- S3 Object Lock in compliance mode, Azure Immutable Blob Storage, or GCS retention policies prevent deletion for specified retention periods.

**Cryptographic hash chains** -- Each event includes a SHA-256 hash of its canonical JSON payload. Sequential events link through hash chains where modifying any entry breaks the chain and reveals tampering.

**Separation of duties** -- Write access is restricted to the logging pipeline only. Read access goes to authorized auditors. The people operating systems must not be able to alter their own audit records.

## OpenTelemetry Audit Pipeline Pattern

A practical implementation:

1. **Collection**: Applications emit audit events as OTel log records with structured attributes (actor, action, resource, content hash)
2. **Processing**: OTel Collector receives logs, applies filtering and metadata enrichment, batches with 5-second flush intervals
3. **Storage**: Dual export to immutable backend (S3 Object Lock) and searchable index (Elasticsearch/OpenSearch) for operational queries

Failure resilience uses persistent sending queues (up to 50,000 batches) with file-based storage, ensuring no events are lost during downstream outages.

## Platform Audit Retention Gaps

| Platform | Native Audit | Max Retention | Gap |
|---|---|---|---|
| Snowflake | ACCESS_HISTORY, QUERY_HISTORY, LOGIN_HISTORY | 365 days (Account Usage views) | Insufficient for SOX (7yr), HIPAA (6yr). Enterprise Edition required for ACCESS_HISTORY. |
| Databricks | Unity Catalog audit system tables | Varies | Regional access limitation -- logs only accessible from the region where recorded. |
| ClickHouse | None | N/A | No native audit logging. Must build custom audit pipelines entirely. |

Every platform requires external export and long-term storage for regulated workloads.

## Takeaway

Build audit infrastructure before deploying governance policies. The audit trail is what proves governance is actually working. Use the OpenTelemetry pipeline pattern for collection, S3 Object Lock for immutable storage, and plan for multi-year retention from day one. Do not rely on platform-native audit retention for regulatory compliance.
