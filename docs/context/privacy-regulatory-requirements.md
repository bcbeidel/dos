---
name: Privacy Regulatory Requirements for Data Pipelines
description: "GDPR and CCPA requirements that constrain pipeline architecture — right to erasure, data minimization, retention enforcement, consent models, and why privacy enforcement belongs in the pipeline layer"
type: context
related:
  - docs/research/2026-03-22-privacy-engineering.research.md
  - docs/context/right-to-erasure-implementation.md
  - docs/context/data-masking-tokenization.md
  - docs/context/medallion-architecture.md
---

## Key Takeaway

GDPR uses opt-in consent; CCPA uses opt-out. This difference forces architecturally distinct consent management. Privacy enforcement belongs in the pipeline layer because it is the only layer that consistently touches every dataset and every transformation regardless of destination. Automated PII scanners achieve 81-96% F1 scores but no system guarantees 100% recall — human review remains essential in regulated environments.

## GDPR Requirements Affecting Pipelines

1. **Lawful basis for processing** (Article 6) — Every pipeline stage processing personal data must have a documented legal basis. Opt-in consent is the default; legitimate interest requires a balancing test and documented assessment.

2. **Right to erasure** (Article 17) — Data subjects can request deletion. Controllers must respond within one month (extendable by two months for complex requests). Erasure must propagate to all systems where data resides, including backups. Exceptions exist for legal compliance, public interest, and established legal claims.

3. **Data minimization** (Article 5(1)(c)) — Processing must be "adequate, relevant and limited to what is necessary." Pipelines must not collect or propagate fields not required for the stated purpose.

4. **Storage limitation** (Article 5(1)(e)) — Personal data kept only as long as necessary. Requires automated retention enforcement with defined TTLs per data category.

5. **Data Protection Impact Assessment** (Article 35) — Required for high-risk processing. Must be completed before pipeline deployment, not after.

6. **Third-party notification** (Article 19) — When data has been disclosed to other controllers, the organization must notify each recipient of erasure requests.

## CCPA/CPRA Requirements

CCPA uses an opt-out model, creating architecturally distinct requirements from GDPR:

1. **Right to delete** — Consumers can request deletion. Identity verification required before processing. The California Delete Act (effective January 1, 2026) introduces the DROP system — data brokers must access it every 45 days to retrieve and process deletion requests.

2. **Right to opt out of sale/sharing** — Requires "Do Not Sell or Share My Personal Information" link. Pipeline architecture must support per-user opt-out flags that prevent data from flowing to third-party destinations.

3. **Automated decision-making** — Enhanced requirements effective January 1, 2026 cover profiling and automated decisions, requiring opt-out mechanisms and impact assessments.

## Dual-Jurisdiction Architecture

Organizations serving both EU and California residents need pipelines supporting both consent models simultaneously. Consent Management Platforms must handle opt-in collection for GDPR and opt-out mechanisms for CCPA while maintaining user preference synchronization.

## PII Detection and Classification

Detection uses three complementary methods: **pattern matching (regex)** for structured PII (SSNs, credit cards, emails) with high false positive rates; **Named Entity Recognition (NER)** for free text, achieving ~96% F1 with BERT-based models but dropping to 81% for zero-shot models; and **ML-based contextual detection** combining column names, sampling, and context (Presidio achieves ~30% F-score improvement when customized).

No automated system guarantees 100% recall. Use F-beta with beta=2 (recall weighted 2x over precision) because missing PII carries regulatory risk while over-flagging creates only operational overhead.

**Classification tiers:** Public (no restrictions), Internal (business-sensitive), Confidential (regulated PII), Restricted (special category — health, financial, government identifiers, biometric).

## Pipeline-Layer Enforcement

The scan-classify-mask pattern at ingestion:

1. **Scan** — Identify PII at ingestion using schema-aware parsing and classifiers. Tools: AWS Macie, Google Sensitive Data Protection (100+ classifiers), Microsoft Presidio, open-source PiiCatcher.
2. **Classify** — Assign sensitivity tier and regulatory category. Attach classification metadata to column-level lineage.
3. **Mask/Protect** — Apply protection based on classification: mask, redact, tokenize, or drop fields downstream systems do not need.

The pipeline layer is the optimal enforcement point because "when privacy is enforced uniformly in the pipeline, rules don't vary by downstream system, governance becomes simpler, compliance becomes more predictable."

## Retention Enforcement

Retention requirements vary by regulation: GDPR (only as long as necessary), HIPAA (6-year minimum), SOX (7-year), PCI DSS (only as long as business need exists). Implementation options: table-level TTL properties (Databricks Auto-TTL, currently Private Preview), scheduled retention jobs (DELETE + VACUUM), or platform-native lifecycle policies (S3 lifecycle rules).

## Decision Rules

1. Document the lawful basis for every pipeline stage processing personal data before deployment.
2. Implement the scan-classify-mask pattern at ingestion — downstream systems should never see PII they do not need.
3. Use automated PII scanners as first-line defense but complement with human review and domain-specific tuning.
4. Build deletion request control tables and scheduled propagation jobs from day one — retrofitting is far more expensive.
5. For dual-jurisdiction, default to GDPR's stricter opt-in model and layer CCPA's opt-out on top.
