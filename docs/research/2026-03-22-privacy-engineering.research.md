---
name: "Privacy Engineering for Data Pipelines"
description: "Right-to-erasure is achievable in Delta Lake and Iceberg but requires multi-step physical deletion (DELETE + REORG/VACUUM or compaction) propagated through every medallion layer — logical deletes alone do not satisfy GDPR; dynamic data masking adds 2-10% CPU overhead and is bypassable via aggregate queries, WHERE clauses, and ORDER BY — it protects casual exposure but not determined adversaries; automated PII scanners achieve 81-96% F1 scores depending on model sophistication but no system guarantees 100% recall, making human review essential for regulated environments; pseudonymized data remains personal data under GDPR while anonymized data does not — this distinction drives architecture choices; NIST withdrew FF3 format-preserving encryption in 2025, leaving FF1 as the sole approved FPE standard; privacy enforcement belongs in the pipeline layer because it is the only layer that consistently touches every dataset regardless of destination"
type: research
sources:
  - https://docs.databricks.com/aws/en/security/privacy/gdpr-delta
  - https://www.databricks.com/blog/handling-right-be-forgotten-gdpr-and-ccpa-using-delta-live-tables-dlt
  - https://olake.io/blog/iceberg-delta-lake-delete-methods-comparison
  - https://aws.amazon.com/blogs/big-data/accelerate-data-lake-operations-with-apache-iceberg-v3-deletion-vectors-and-row-lineage/
  - https://dev.to/jakkie_koekemoer/dynamic-data-masking-use-cases-limitations-and-what-to-do-instead-4laj
  - https://www.immuta.com/blog/tokenization-vs-data-masking/
  - https://aws.amazon.com/what-is/data-masking/
  - https://www.protecto.ai/blog/best-ner-models-for-pii-identification
  - https://microsoft.github.io/presidio/evaluation/
  - https://www.databahn.ai/blog/privacy-by-design-in-the-pipeline-embedding-data-protection-at-scale
  - https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/
  - https://gdpr-info.eu/art-17-gdpr/
  - https://docs.cloud.google.com/architecture/de-identification-re-identification-pii-using-cloud-dlp
  - https://mostly.ai/blog/pseudonymization-vs-anonymization-ensure-gdpr-compliance-and-maximize-data-utility
  - https://www.confluent.io/blog/real-time-pii-detection-via-ml/
  - https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-38g.pdf
  - https://datasumi.medium.com/ensuring-your-data-lake-is-gdpr-compliant-a-strategic-and-technical-imperative-4ba79e9d94c0
  - https://www.strac.io/blog/top-10-data-scanning-tools
  - https://atlan.com/know/data-governance/automated-pii-classification/
  - https://www.progress.com/blogs/what-is-dynamic-data-masking
  - https://medium.com/@cralle/auto-ttl-in-databricks-automated-data-retention-done-properly-5ea511b45c1d
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-21-pipeline-design-architecture.research.md
  - docs/research/2026-03-22-open-table-formats.research.md
---

## Summary

**Research question:** What technical patterns and regulatory requirements govern privacy engineering for data pipelines?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 21 | **Searches:** 14 across Google

**Key findings:**
- Right-to-erasure is achievable in Delta Lake and Iceberg but requires multi-step physical deletion (DELETE + REORG TABLE APPLY PURGE + VACUUM in Delta, or DELETE + compaction in Iceberg) propagated through every medallion layer — logical deletes and deletion vectors alone do not satisfy GDPR
- Dynamic data masking adds 2-10% CPU overhead per query and is bypassable via aggregate functions, WHERE clauses, ORDER BY, and binary search attacks — it protects casual exposure but not determined adversaries with query access
- Automated PII scanners achieve 81-96% F1 scores depending on model sophistication (GLiNER 81%, BERT-based 96%), but no system guarantees 100% recall — human review remains essential in regulated environments
- Pseudonymized data remains personal data under GDPR (subject to full regulation); anonymized data does not — this distinction fundamentally drives pipeline architecture choices around reversibility
- NIST withdrew FF3 format-preserving encryption entirely in February 2025 due to the Beyne attack; FF1 is the sole remaining approved FPE standard
- Privacy enforcement belongs in the pipeline layer because it is the only layer that consistently touches every dataset and every transformation regardless of destination

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://docs.databricks.com/aws/en/security/privacy/gdpr-delta | Prepare your data for GDPR compliance | Databricks | current docs | T1 | verified |
| 2 | https://www.databricks.com/blog/handling-right-be-forgotten-gdpr-and-ccpa-using-delta-live-tables-dlt | Handling Right to be Forgotten using DLT | Databricks | 2024 | T4 | verified — vendor blog |
| 3 | https://olake.io/blog/iceberg-delta-lake-delete-methods-comparison | Comparing Delete Methods in Iceberg & Delta Lake | OLake | 2025 | T5 | verified — practitioner comparison |
| 4 | https://aws.amazon.com/blogs/big-data/accelerate-data-lake-operations-with-apache-iceberg-v3-deletion-vectors-and-row-lineage/ | Iceberg V3 deletion vectors and row lineage | AWS | 2025 | T2 | verified — cloud provider blog |
| 5 | https://dev.to/jakkie_koekemoer/dynamic-data-masking-use-cases-limitations-and-what-to-do-instead-4laj | Dynamic Data Masking: Limitations and Alternatives | Jakkie Koekemoer | 2025 | T5 | verified — practitioner blog |
| 6 | https://www.immuta.com/blog/tokenization-vs-data-masking/ | Tokenization vs Data Masking | Immuta | 2025 | T4 | verified — vendor blog |
| 7 | https://aws.amazon.com/what-is/data-masking/ | What is Data Masking? | AWS | current docs | T1 | verified |
| 8 | https://www.protecto.ai/blog/best-ner-models-for-pii-identification | Comparing Best NER Models for PII Identification | Protecto | 2025 | T4 | verified — vendor blog with benchmarks |
| 9 | https://microsoft.github.io/presidio/evaluation/ | PII detection evaluation | Microsoft Presidio | current docs | T1 | verified |
| 10 | https://www.databahn.ai/blog/privacy-by-design-in-the-pipeline-embedding-data-protection-at-scale | Privacy by Design in the Pipeline | DataBahn | 2025 | T4 | verified — vendor blog |
| 11 | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/ | Right to erasure | UK ICO | current guidance | T1 | verified — regulatory authority |
| 12 | https://gdpr-info.eu/art-17-gdpr/ | Art. 17 GDPR – Right to erasure | GDPR-info.eu | current text | T1 | verified — regulation text |
| 13 | https://docs.cloud.google.com/architecture/de-identification-re-identification-pii-using-cloud-dlp | De-identification and re-identification using Sensitive Data Protection | Google Cloud | current docs | T1 | verified |
| 14 | https://mostly.ai/blog/pseudonymization-vs-anonymization-ensure-gdpr-compliance-and-maximize-data-utility | Pseudonymization vs Anonymization | MOSTLY AI | 2025 | T4 | verified — vendor blog |
| 15 | https://www.confluent.io/blog/real-time-pii-detection-via-ml/ | Automatic Detect PII in Real Time with ML | Confluent | 2023 | T4 | verified — vendor blog |
| 16 | https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-38g.pdf | NIST SP 800-38G Format-Preserving Encryption | NIST | 2016 (FF3 withdrawn 2025) | T1 | verified — government standard |
| 17 | https://datasumi.medium.com/ensuring-your-data-lake-is-gdpr-compliant-a-strategic-and-technical-imperative-4ba79e9d94c0 | Ensuring Your Data Lake is GDPR Compliant | Datasumi | 2024 | T5 | verified — practitioner blog |
| 18 | https://www.strac.io/blog/top-10-data-scanning-tools | Top PII Data Scanning Tools | Strac | 2026 | T4 | verified — vendor comparison |
| 19 | https://atlan.com/know/data-governance/automated-pii-classification/ | Automated PII Classification | Atlan | 2025 | T4 | verified — vendor blog |
| 20 | https://www.progress.com/blogs/what-is-dynamic-data-masking | Dynamic Data Masking: Benefits, Challenges & Best Practices | Progress | 2025 | T4 | verified — vendor blog |
| 21 | https://medium.com/@cralle/auto-ttl-in-databricks-automated-data-retention-done-properly-5ea511b45c1d | Auto-TTL in Databricks | Christian Hansen | 2026 | T5 | verified — practitioner blog |

---

## Sub-question 1: PII and Sensitive Data Identification and Classification

### Detection approaches: regex, NLP, and ML

PII detection uses three complementary methods with increasing sophistication and cost [8][9][18]:

1. **Pattern matching (regex)** — Fast and deterministic. Catches structured PII with known formats: SSNs, credit card numbers, email addresses, phone numbers. Limitations: high false positive rate on generic numeric fields (e.g., order IDs matching SSN patterns), zero capability for unstructured text or context-dependent PII.

2. **Named Entity Recognition (NER)** — NLP models trained to identify entities (names, locations, organizations) in free text. spaCy, Flair, and transformer-based models (BERT, DeBERTa) provide varying accuracy. NER models tend toward high recall with low precision (too many false alarms) or vice versa — striking the right balance is critical in regulated industries [8].

3. **ML-based contextual detection** — Combines column name analysis, data sampling, and contextual signals. Microsoft Presidio uses regex + NER + context-aware detection, achieving approximately 30% F-score improvement when customized versus vanilla configuration [9]. Confluent built real-time PII detection UDFs for ksqlDB using NLP models that inspect Kafka messages in-stream and redact before data reaches the broker [15].

### NER model accuracy benchmarks

Model accuracy varies significantly by architecture and training data [8]:

| Model | F1-Score | Precision/Recall | Key Characteristic |
|-------|----------|-------------------|--------------------|
| ab-ai/pii_model (BERT) | ~96% | 95-97% | High accuracy, pattern-focused, ~110M params |
| Roblox PII Classifier | 94.3% | 98% recall, 1% FP rate | Chat-context specific, detects obfuscation |
| GLiNER (zero-shot) | 81-83% | Balanced | 60+ entity types, flexible but lower accuracy |
| HydroX AI (DeBERTa-v3) | Not published | High precision | Direct masking output, up to 1024 tokens |

Critical limitation: no automated system guarantees 100% recall or 100% precision [9]. Microsoft Presidio's documentation states this explicitly. In PII detection, recall is typically prioritized over precision — missing PII (false negative) carries regulatory risk, while flagging non-PII (false positive) merely creates review work. The recommended evaluation metric is F-beta with beta=2, weighting recall twice as heavily as precision [9].

### Classification taxonomy design

Data classification follows a sensitivity-tiered approach aligned with regulatory frameworks [18][19]:

- **Public** — No restrictions. Aggregated statistics, published reports.
- **Internal** — Business-sensitive but not regulated. Internal metrics, operational logs.
- **Confidential** — Regulated PII subject to GDPR/CCPA. Names, emails, addresses, phone numbers, dates of birth.
- **Restricted** — Special category data requiring strongest controls. Health records (PHI), financial account numbers, government identifiers (SSN, passport), biometric data, religious beliefs, ethnic origin.

NIST SP 800-122 defines PII as "any information about an individual maintained by an agency" and categorizes by linkability — directly identifiable (name, SSN) versus indirectly identifiable (date of birth + ZIP code + gender). ISO 27701 Clause 6.5.2 requires organizations to classify, label, and handle PII according to legal requirements, value, and sensitivity to unauthorized disclosure [19].

### Automated scan-classify-mask pipeline pattern

The production pattern for PII management is a three-stage pipeline [10][18][19]:

1. **Scan** — Identify PII at ingestion using schema-aware parsing and lightweight classifiers. Tools: AWS Macie, Google Sensitive Data Protection (100+ built-in classifiers), Microsoft Presidio, open-source PiiCatcher (regex + spaCy NER).
2. **Classify** — Assign sensitivity tier and regulatory category. Attach classification metadata to column-level lineage for downstream propagation.
3. **Mask/Protect** — Apply appropriate protection based on classification: mask, redact, tokenize, or drop fields that downstream systems do not need.

The pipeline layer is the optimal enforcement point because it "consistently touches every dataset and every transformation regardless of where that data eventually resides" [10]. When privacy rules apply at the pipeline level, every downstream consumer inherits the privacy posture.

---

## Sub-question 2: Data Masking, Tokenization, Pseudonymization, and Encryption

### Static vs. dynamic masking

**Static data masking (SDM)** permanently transforms sensitive data before distribution, creating sanitized copies of production data [7][20]. Use cases: non-production environments (dev, test, QA), data sharing with third parties, training datasets. The masked copy contains no reversible path to original values. Drawback: copies become stale as production data changes.

**Dynamic data masking (DDM)** applies masking rules in real-time at query time based on user roles and permissions [5][7][20]. Authorized users see original data; others receive masked views. The actual stored data is never altered. Drawback: adds 2-10% CPU overhead per query and is vulnerable to inference attacks.

DDM security weaknesses are well-documented and significant [5]:

- **WHERE clause bypass** — Queries execute against real unmasked data before output filtering. A WHERE clause like `WHERE salary > 100000` reveals information despite masked display.
- **Aggregate function exposure** — SUM, AVG, COUNT return actual values regardless of masking.
- **Pattern extraction** — String data leaks character-by-character through LIKE queries (~6,000 iterations for a 24-character email).
- **ORDER BY disclosure** — Sorting reveals relative rankings despite masked values.
- **Binary search attack** — ~20 queries can pinpoint numeric values within a million-dollar range to exact precision.

Microsoft and Oracle both document these limitations explicitly. Microsoft states: "DDM doesn't aim to prevent database users from connecting directly...and running exhaustive queries that expose pieces of the sensitive data" [5].

DDM is appropriate for production dashboards with controlled interfaces, customer support tools, and read-only reporting. It is inappropriate for development environments, any scenario where users compose arbitrary SQL, or as a sole compliance mechanism [5].

### Tokenization

Tokenization replaces sensitive values with randomly generated tokens while the original data resides in a separate secure vault [6][7]. The token has no mathematical relationship to the original value — unlike encryption, it cannot be reversed without access to the vault. Key characteristics:

- **Reversible** through de-tokenization (vault lookup), not through computation
- **Performance cost** on analytical queries — operations like LIKE searches, JOINs, and mathematical calculations require decrypting entire columns before execution [6]
- **Primary use case** — Extremely sensitive data with zero analytical value: credit card numbers (PCI DSS compliance), SSNs, account numbers
- **Not suitable for** — Analytical workloads, ML training, BI dashboards where data utility matters [6]

### Pseudonymization vs. anonymization

This distinction is architecturally consequential because it determines GDPR applicability [14]:

**Pseudonymization** (GDPR Article 4(5)) replaces identifying information while maintaining the ability to re-identify with additional information kept separately. Pseudonymized data **remains personal data under GDPR** — subject to full regulatory obligations including right to erasure, consent management, and breach notification. Methods: tokenization, deterministic encryption, key-coding, hashing with salt.

**Anonymization** permanently destroys the pathway back to individuals. Anonymized data **falls outside GDPR scope entirely**. Even the person who performed anonymization cannot reverse it. Methods: k-anonymity, differential privacy, generalization, aggregation.

The trade-off is utility versus regulatory burden [14]. Pseudonymization preserves analytical value — researchers can track patient outcomes, marketers can analyze customer journeys, developers can test with realistic data structures. Anonymization sacrifices individual-level analysis but eliminates GDPR compliance overhead. Most production data pipelines use pseudonymization because downstream analytics require individual-level granularity.

### Format-preserving encryption (FPE)

FPE encrypts data while maintaining the original format, length, and character set [16]. A 16-digit credit card number encrypts to another 16-digit number. Useful for legacy systems that validate input formats.

NIST SP 800-38G defined two FPE modes: FF1 and FF3 [16]. **Critical 2025 update:** NIST withdrew FF3 entirely in February 2025 due to the Beyne attack that affected both FF3 and FF3-1. FF1 remains the sole approved standard, with an increased minimum domain size in the latest revision.

FF1 uses 10 rounds of Feistel network encryption (vs. 8 for the now-withdrawn FF3), providing stronger security at the cost of lower throughput. FPE adds computational overhead from cycle-walking when the output space does not perfectly align with the cipher domain.

Google Cloud's Sensitive Data Protection offers FPE-FFX mode that preserves input text length and character set but notes it "lacks authentication and an initialization vector" — making it less secure than deterministic encryption but maintaining backward compatibility with legacy systems [13].

### Encryption at rest and in transit

Encryption requirements form the baseline of any privacy-compliant pipeline:

- **At rest** — AES-256 is the universal standard. All major cloud providers encrypt stored data by default (S3, GCS, ADLS). Key management via AWS KMS, Google Cloud KMS, or Azure Key Vault. Key rotation recommended annually minimum, quarterly for highly sensitive data.
- **In transit** — TLS 1.2 minimum, TLS 1.3 preferred for enhanced security and performance. Perfect Forward Secrecy (PFS) prevents retrospective decryption if long-term keys are compromised.
- **In use** — Emerging area. Confidential computing (Intel SGX, AMD SEV) protects data during processing. Not yet standard for data pipelines.

GDPR Article 32 requires "appropriate technical and organizational measures" including encryption. HIPAA maps encryption at rest to the Access Controls standard and in transit to Transmission Security. Encrypting one state but not the other creates exploitable gaps.

---

## Sub-question 3: GDPR and CCPA Compliance Requirements Affecting Pipeline Architecture

### GDPR requirements with pipeline implications

GDPR imposes several requirements that directly constrain pipeline architecture [11][12]:

1. **Lawful basis for processing** (Article 6) — Every pipeline stage that processes personal data must have a documented legal basis. Opt-in consent is required by default; legitimate interest requires a balancing test and documented assessment.

2. **Right to erasure** (Article 17) — Data subjects can request deletion of their personal data. Controllers must respond "without undue delay and at the latest within one month." Erasure must be propagated to all systems where data resides, including backup systems [11]. Exceptions exist for legal compliance, public interest, and established legal claims.

3. **Data minimization** (Article 5(1)(c)) — Organizations must limit processing to what is "adequate, relevant and limited to what is necessary." Pipelines must not collect or propagate fields that are not required for the stated processing purpose.

4. **Storage limitation** (Article 5(1)(e)) — Personal data must be kept only for as long as necessary. Requires automated retention enforcement with defined TTLs per data category.

5. **Data Protection Impact Assessment** (Article 35) — Required for high-risk processing. Must be completed before the pipeline is deployed, not after.

6. **Third-party notification** (Article 19) — When data has been disclosed to other controllers, the organization must notify each recipient of erasure requests "unless this proves impossible or involves disproportionate effort" [11].

### CCPA requirements with pipeline implications

CCPA (and its amendment CPRA) uses an opt-out model rather than GDPR's opt-in model, creating architecturally distinct requirements:

1. **Right to delete** — Consumers can request deletion. Businesses must verify requester identity before processing. The California Delete Act (effective January 1, 2026) introduces the DROP (Delete Request and Opt-Out Platform) system — data brokers must access DROP every 45 days to retrieve and process deletion requests.

2. **Right to opt out of sale/sharing** — Requires a "Do Not Sell or Share My Personal Information" link. Pipeline architecture must support per-user opt-out flags that prevent data from flowing to third-party destinations.

3. **Automated decision-making technology** — Enhanced CCPA requirements effective January 1, 2026, cover profiling and automated decisions, requiring opt-out mechanisms and impact assessments.

### Dual-jurisdiction pipeline architecture

Organizations serving both EU and California residents need pipelines that support both consent models simultaneously. Consent Management Platforms must support opt-in collection for GDPR and opt-out mechanisms for CCPA while maintaining user preference synchronization. API gateways can centralize consent enforcement, verifying consent status before routing requests to downstream processing.

---

## Sub-question 4: Right-to-Erasure Implementation in Data Warehouses

### Delta Lake deletion mechanics

Delta Lake implements erasure through a three-step process [1][2]:

**Step 1 — Logical delete:**
```sql
-- Single record
DELETE FROM bronze.users WHERE user_id = 5;

-- Bulk deletion via control table
MERGE INTO target
USING (SELECT user_id FROM gdpr_control_table) AS source
ON target.user_id = source.user_id
WHEN MATCHED THEN DELETE;
```

The MERGE method is recommended for processing batches of deletion requests from a control table that tracks incoming GDPR/CCPA requests [1].

**Step 2 — Physical purge (for tables with deletion vectors):**
```sql
REORG TABLE target APPLY (PURGE);
```

Deletion vectors mark rows as deleted in metadata without rewriting data files. This is efficient for writes but **does not satisfy GDPR** — the original data remains in the underlying Parquet files. REORG TABLE APPLY PURGE rewrites files to physically remove deleted rows [1].

**Step 3 — Remove historical versions:**
```sql
VACUUM target;
```

Delta Lake retains table history for 30 days by default (enabling time travel). VACUUM removes files no longer referenced by the current table version. The 30-day default aligns with GDPR's "without undue delay" standard [1].

### Propagation through medallion layers

Deletion must propagate through every layer — bronze, silver, and gold [1][2]:

- **Bronze (raw)** — Direct DELETE or MERGE against tables containing PII. Start here, driven by a scheduled job that queries the deletion request control table.
- **Silver/Gold via materialized views** — "Materialized views automatically handle deletions in sources. Hence, you do not have to do anything special" [1]. However, views must be refreshed and maintenance run to ensure deletions are fully processed.
- **Silver/Gold via streaming tables** — Problematic. Streaming tables can only process append queries. Deleting from a source table used for streaming breaks the stream. Workaround: add `skipChangeCommits` option to ignore non-append operations, then handle deletions separately [1].

### Apache Iceberg deletion mechanics

Iceberg V3 introduces deletion vectors stored as Roaring Bitmaps in Puffin sidecar files [3][4]:

- **Merge-on-Read (MoR)** — Deletions are recorded in sidecar files. Query engines filter deleted rows at read time. Write performance is excellent; read performance degrades as delete files accumulate.
- **Compaction** — Periodic compaction jobs merge delete files and rewrite data files to physically remove deleted rows. This is the equivalent of Delta Lake's REORG + VACUUM.
- **Performance** — Apple reported maintenance operations reduced from "approximately two hours" to "several minutes" after migrating to Iceberg with deletion vectors. Airbnb achieved 50% reduction in compute resources and 40% decrease in job elapsed time [3].

Both Delta Lake and Iceberg now use Roaring Bitmaps for deletion vectors [3]. The key architectural difference: Delta Lake offers both Copy-on-Write and Merge-on-Read strategies, while Iceberg V3 standardizes on Merge-on-Read with mandatory compaction.

### The append-only problem

Traditional data lakes built on immutable file systems (plain Parquet on S3/GCS) cannot easily delete a single row from a massive multi-row file — doing so requires rewriting the entire file [17]. This is why transactional table formats (Delta Lake, Iceberg) are prerequisites for GDPR compliance in data lakes. Without them, erasure at scale is operationally infeasible.

### Retention enforcement with Auto-TTL

Databricks introduced Auto-TTL as a Predictive Optimization capability — retention becomes a table-level property instead of a pipeline-level responsibility [21]. Predictive Optimization handles deletion of expired rows and manages physical storage cleanup automatically. This eliminates custom retention jobs and cron schedules. Currently in Private Preview.

---

## Sub-question 5: Privacy-by-Design Principles

### Data minimization in practice

Data minimization is not merely a policy statement — it requires architectural enforcement [10]:

1. **Early detection** — Identify PII, quasi-identifiers, and sensitive metadata at ingestion using schema-aware parsing or lightweight classifiers.
2. **Inline minimization** — Mask, redact, tokenize, or drop fields that downstream systems do not need. This happens during pipeline processing, not after storage.
3. **Sensitivity-based routing** — Direct high-sensitivity data to appropriate regions/storage layers. Produce different dataset versions: masked analytics views versus full-fidelity security views.
4. **Lineage preservation** — Attach metadata recording what was changed, when, and why. Downstream systems inherit this context.

The pipeline is the strongest enforcement point because "when privacy is enforced uniformly in the pipeline, rules don't vary by downstream system, governance becomes simpler, compliance becomes more predictable" [10].

### Retention enforcement

Automated retention requires mapping data categories to applicable regulations and assigning retention periods [21]:

- **GDPR** — Personal data kept only as long as necessary for processing purpose
- **HIPAA** — 6-year retention minimum for medical records
- **SOX** — 7-year retention for financial records
- **PCI DSS** — Cardholder data retained only as long as business need exists

Implementation approaches: table-level TTL properties (Databricks Auto-TTL), scheduled retention jobs that DELETE expired rows followed by VACUUM, or platform-native lifecycle policies (S3 lifecycle rules for object-level expiration). The choice depends on whether retention applies at row level (TTL) or object level (lifecycle policies).

### Google Cloud de-identification architecture

Google Cloud's Sensitive Data Protection provides a reference architecture for privacy-preserving pipelines [13]:

- **De-identification pipeline** — Dataflow streaming pipeline applies transformations (tokenization, masking, generalization, redaction) as data flows from Cloud Storage to BigQuery.
- **Two transformation types** — `recordTransformations` for structured tabular data (fast, column-targeted); `infoTypeTransformations` for unstructured free text (requires content inspection, higher cost).
- **Re-identification pipeline** — Separate pipeline reverses tokenization using the same encryption keys, restricted to security admins via IAM. Key rotation breaks tokenization integrity and requires re-tokenizing entire datasets.
- **Format-preserving encryption** — FPE-FFX mode preserves length and character set. Less secure than deterministic encryption but compatible with legacy systems expecting specific formats.

---

## Challenge

Challenger research targeted three claims frequently asserted without adequate qualification: that right-to-erasure is achievable in append-only data lakes, that dynamic masking is production-viable, and that automated PII scanners are reliable enough for compliance.

### Is right-to-erasure actually achievable in append-only data lakes?

Not in traditional append-only data lakes — and the framing of the question reveals the real issue. Plain Parquet on S3 or GCS is genuinely immutable at the row level; deleting one row requires rewriting an entire file [17]. This is why Delta Lake and Iceberg exist. With transactional table formats, erasure is achievable but requires a multi-step process that teams underestimate:

1. Logical delete (DELETE/MERGE) — marks rows but does not remove data from storage
2. Physical purge (REORG PURGE in Delta, compaction in Iceberg) — rewrites files to exclude deleted rows
3. History cleanup (VACUUM in Delta, snapshot expiration in Iceberg) — removes old file versions that still contain deleted data
4. Propagation — repeat steps 1-3 for every downstream table in every medallion layer

Teams that run only step 1 and declare compliance are wrong. The original data persists in Parquet files until steps 2-3 complete. Delta Lake's 30-day default VACUUM retention means deleted data can exist on storage for up to a month after the DELETE command [1]. This is defensible under GDPR's "without undue delay" standard but must be documented and justified. Streaming tables add further complexity — they cannot process deletes natively and require workarounds [1].

The honest answer: right-to-erasure is achievable with transactional table formats and disciplined multi-step deletion processes. It is not achievable with plain append-only storage, and it is not as simple as running a DELETE statement.

### Does dynamic masking introduce unacceptable latency?

The latency is acceptable; the security is not. DDM adds 2-10% CPU overhead per query [5][20] — this is within tolerance for most analytical workloads and barely noticeable for dashboards. Native DDM implementations at the database layer (Aerospike, Snowflake, BigQuery) minimize overhead further.

The real problem is that DDM provides a false sense of security. Users with direct query access can extract masked values through inference attacks [5]. Microsoft explicitly states DDM is not a security boundary. DDM is appropriate as a convenience layer preventing accidental exposure — support agents seeing masked SSNs, dashboard viewers seeing anonymized names. It is inappropriate as a compliance mechanism or as protection against any user who can write SQL.

The recommendation: use DDM for casual exposure prevention in controlled interfaces. Use static masking or tokenization for actual data protection. Never rely on DDM as your sole privacy control.

### Are automated PII scanners reliable enough?

Reliable enough for what? The best NER models achieve 94-96% F1 scores on curated test datasets [8]. In production, accuracy drops due to domain-specific terminology, multilingual content, implicit identifiers, and data format variability. Microsoft Presidio's documentation explicitly states: "No de-identification system is perfect" and that "false positive and false negative rates should be balanced" [9].

The precision-recall trade-off is inescapable. Tuning for high recall (catching all PII) increases false positives — flagging benign data as sensitive, creating noise and unnecessary masking. Tuning for high precision (reducing false alarms) increases false negatives — missing actual PII, creating compliance risk. The recommended approach uses F-beta with beta=2, weighting recall twice as heavily, because the cost of missing PII (regulatory fines, breach liability) exceeds the cost of over-flagging (operational overhead) [9].

Automated scanners are reliable enough to be the first line of defense — they should run continuously and flag candidates for review. They are not reliable enough to be the sole mechanism for compliance. Human review of scanner output, regular accuracy audits with labeled test sets, and domain-specific customization (custom regex patterns, fine-tuned NER models) are necessary complements.

---

## Findings

### Finding 1: Right-to-erasure requires multi-step physical deletion propagated through every medallion layer
**Confidence: HIGH**

GDPR Article 17 requires erasure "without undue delay" across all systems where personal data resides, including backups [11][12]. In Delta Lake, this means DELETE + REORG TABLE APPLY PURGE + VACUUM across bronze, silver, and gold layers [1]. In Iceberg, it means DELETE + compaction + snapshot expiration [3][4]. Deletion vectors (used by both formats) are a write optimization — they mark rows as deleted in metadata but leave original data in Parquet files until physical rewrite occurs. Materialized views propagate deletions automatically upon refresh; streaming tables cannot process deletes natively and require workarounds [1]. Teams must implement deletion request control tables, scheduled propagation jobs, and verification that physical files no longer contain deleted data. The 30-day default VACUUM retention in Delta Lake is defensible under GDPR's "undue delay" standard but must be documented.

### Finding 2: Dynamic data masking is a convenience layer, not a security boundary
**Confidence: HIGH**

DDM adds 2-10% CPU overhead per query — acceptable for most workloads [5][20]. However, DDM is bypassable through aggregate functions, WHERE clause inference, ORDER BY disclosure, LIKE pattern extraction, and binary search attacks [5]. Microsoft and Oracle document these limitations explicitly. DDM protects against casual exposure in controlled interfaces (dashboards, support tools) where users cannot compose arbitrary SQL. It does not protect against users with direct query access. Organizations should use DDM for UI-level privacy (preventing support agents from seeing raw SSNs) and static masking, tokenization, or column-level encryption for actual data protection. Relying on DDM as a sole compliance mechanism will not withstand regulatory scrutiny.

### Finding 3: Automated PII scanners require human oversight and domain-specific tuning
**Confidence: HIGH**

NER models for PII detection range from 81% to 96% F1 score depending on model sophistication [8]. BERT-based models achieve ~96% F1 with 95-97% precision/recall but are pattern-focused with limited context understanding. Zero-shot models (GLiNER) offer flexibility across 60+ entity types but drop to 81-83% F1. Microsoft Presidio achieves ~30% F-score improvement when customized versus vanilla configuration [9]. No automated system guarantees 100% recall — false negatives (missed PII) create regulatory risk. Production systems should prioritize recall over precision (F-beta with beta=2), run scanners continuously, and implement human review workflows for flagged content. Domain-specific customization — custom regex patterns for industry identifiers, fine-tuned NER models for specialized terminology — is necessary for regulated environments.

### Finding 4: Pseudonymization and anonymization have fundamentally different GDPR consequences
**Confidence: HIGH**

Pseudonymized data remains personal data under GDPR, subject to full regulatory obligations including right to erasure, consent management, and breach notification [14]. Anonymized data falls outside GDPR scope entirely. This distinction drives architecture decisions: pseudonymization (tokenization, deterministic encryption, key-coding) preserves analytical utility and individual-level tracking but carries full compliance burden. Anonymization (k-anonymity, differential privacy, aggregation) eliminates compliance overhead but destroys individual-level analysis capability. Most production data pipelines use pseudonymization because downstream analytics require individual-level granularity. Teams must understand that tokenized data is still personal data — the vault mapping tokens to originals is "additional information" under Article 4(5), and the entire system remains subject to GDPR.

### Finding 5: Privacy enforcement belongs in the pipeline layer, not downstream systems
**Confidence: MODERATE**

The data pipeline is the only layer that consistently touches every dataset and every transformation regardless of destination [10]. When privacy rules apply at the pipeline level, every downstream consumer inherits the privacy posture. The recommended pattern is scan-classify-mask at ingestion: identify PII using schema-aware parsing, assign sensitivity tiers, and apply appropriate protection (mask, redact, tokenize, drop) before data reaches downstream systems [10][19]. Google Cloud's reference architecture implements this as a Dataflow streaming pipeline applying de-identification transformations between Cloud Storage and BigQuery [13]. Confidence is moderate because enforcement at the pipeline layer requires comprehensive PII detection (which has known accuracy limitations per Finding 3), and some use cases legitimately require raw PII to flow to specific destinations (e.g., customer support systems, identity verification services).

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Delta Lake deletion vectors mark rows as deleted but do not physically remove data from Parquet files | [1] | verified | REORG TABLE APPLY PURGE required for physical deletion |
| 2 | Delta Lake VACUUM default retention is 30 days, aligning with GDPR "undue delay" | [1] | verified | Configurable; must be documented for compliance |
| 3 | Materialized views automatically propagate source deletions upon refresh | [1] | verified | No special handling needed, but refresh + maintenance required |
| 4 | Streaming tables cannot process deletes natively in Delta Lake | [1] | verified | Requires skipChangeCommits workaround |
| 5 | Dynamic data masking adds 2-10% CPU overhead per query | [5][20] | verified | Varies by masking algorithm complexity and native vs proxy implementation |
| 6 | DDM is bypassable via WHERE clauses, aggregates, ORDER BY, and binary search | [5] | verified | Microsoft and Oracle both document these limitations explicitly |
| 7 | Best NER models for PII achieve ~96% F1 score (BERT-based) | [8] | verified | On curated test data; production accuracy lower due to domain variability |
| 8 | Microsoft Presidio achieves ~30% F-score improvement when customized | [9] | qualified | Improvement over vanilla configuration; absolute scores not published |
| 9 | NIST withdrew FF3 format-preserving encryption in February 2025 | [16] | verified | Due to Beyne attack; FF1 remains sole approved FPE standard |
| 10 | Pseudonymized data remains personal data under GDPR; anonymized data does not | [14] | verified | Article 4(5) explicitly defines pseudonymization as still requiring compliance |
| 11 | GDPR right to erasure must be fulfilled within one month | [11][12] | verified | Extendable by two months for complex requests with notification |
| 12 | Iceberg V3 deletion vectors use Roaring Bitmaps in Puffin sidecar files | [3][4] | verified | Replaces deprecated position delete files from V2 |
| 13 | Apple reduced Iceberg maintenance operations from ~2 hours to minutes | [3] | qualified | Vendor case study; specific workload characteristics not detailed |
| 14 | Google Cloud DLP provides 100+ built-in PII classifiers | [13] | verified | Plus custom infoType creation; recordTransformations faster than infoTypeTransformations |
| 15 | Databricks Auto-TTL makes retention a table-level property with automatic enforcement | [21] | verified | Currently Private Preview; Predictive Optimization handles deletion + VACUUM |
