---
name: "Governance & Compliance"
description: "DAMA-DMBOK grounds governance in accountability, decision rights, and policy enforcement — not tooling; audit trails require immutable append-only storage with SHA-256 hash chains for tamper evidence; Snowflake row access policies and tag-based masking are the most mature RLS/column-masking implementation; Databricks Unity Catalog ABAC (governed tags) scales governance but requires Runtime 16.4+; ClickHouse row policies exist but lack audit logging parity with commercial platforms; policy-as-code via Terraform/Immuta is practical but adoption remains early; open-source governance stacks have significant gaps in access control, audit, and classification compared to commercial alternatives"
type: research
sources:
  - https://atlan.com/dama-dmbok-framework/
  - https://docs.snowflake.com/en/user-guide/security-row-intro
  - https://docs.snowflake.com/en/user-guide/security-column-ddm-intro
  - https://docs.snowflake.com/en/user-guide/tag-based-masking-policies
  - https://docs.snowflake.com/en/user-guide/security-column-intro
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/audit
  - https://clickhouse.com/docs/knowledgebase/row-column-policy
  - https://chistadata.com/implementing-custom-access-policies-in-clickhouse/
  - https://clickhouse.com/docs/operations/access-rights
  - https://www.immuta.com/blog/automate-fine-grained-access-controls-with-policy-as-code/
  - https://www.immuta.com/blog/rbac-vs-abac-for-data-access-control-use-cases/
  - https://oneuptime.com/blog/post/2026-02-06-immutable-audit-log-pipeline-otel/view
  - https://mattermost.com/blog/compliance-by-design-18-tips-to-implement-tamper-proof-audit-logs/
  - https://www.junaideffendi.com/p/data-governance-in-lakehouse-using
  - https://www.leolytixco.com/blog/snowflake-rbac
  - https://www.openpolicyagent.org/docs
  - https://www.datasunrise.com/knowledge-center/data-audit-trails/
  - https://netwrix.com/en/resources/blog/data-governance-best-practices/
  - https://select.dev/posts/snowflake-access-history
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-operations-reliability.research.md
---

## Summary

**Research question:** What governance and compliance mechanisms should data engineers implement in pipelines and warehouses?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 21 | **Searches:** 18 across Google

**Key findings:**
- DAMA-DMBOK positions governance as the center of all data management — governance is about accountability, decision rights, and policy enforcement, not tooling or technology choices
- Audit trails for data pipelines require immutable append-only storage with cryptographic hash chains; OpenTelemetry + S3 Object Lock provides a practical open-standard implementation
- Snowflake has the most mature row-level and column-level security: row access policies, dynamic data masking, and tag-based masking that auto-applies policies to matching columns across thousands of tables
- Databricks Unity Catalog ABAC (governed tags) is the scalable path forward but requires Runtime 16.4+ and is in Public Preview; manual row filters and column masks are GA but do not apply to views
- ClickHouse supports row policies and column-level GRANT restrictions but lacks native audit logging, tag-based classification, and dynamic masking — governance requires custom implementation
- Policy-as-code via Terraform (Snowflake/Databricks providers) and Immuta (YAML + CLI) is practical and production-ready, but adoption outside large enterprises remains early-stage

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://atlan.com/dama-dmbok-framework/ | DAMA DMBOK Framework: An Ultimate Guide for 2026 | Atlan | 2026 | T4 | verified — vendor guide grounded in DAMA-DMBOK 2/3 |
| 2 | https://docs.snowflake.com/en/user-guide/security-row-intro | Understanding row access policies | Snowflake | current docs | T1 | verified |
| 3 | https://docs.snowflake.com/en/user-guide/security-column-ddm-intro | Understanding Dynamic Data Masking | Snowflake | current docs | T1 | verified |
| 4 | https://docs.snowflake.com/en/user-guide/tag-based-masking-policies | Tag-based masking policies | Snowflake | current docs | T1 | verified |
| 5 | https://docs.snowflake.com/en/user-guide/security-column-intro | Understanding Column-level Security | Snowflake | current docs | T1 | verified |
| 6 | https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks | Row filters and column masks | Databricks | current docs | T1 | verified |
| 7 | https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/ | Unity Catalog ABAC | Databricks | current docs | T1 | verified |
| 8 | https://docs.databricks.com/aws/en/data-governance/unity-catalog/audit | Audit Unity Catalog events | Databricks | current docs | T1 | verified |
| 9 | https://clickhouse.com/docs/knowledgebase/row-column-policy | Row and column level security | ClickHouse | current docs | T1 | verified |
| 10 | https://chistadata.com/implementing-custom-access-policies-in-clickhouse/ | Implementing custom access policies in ClickHouse | ChistaDATA | 2024 | T5 | verified — community guide |
| 11 | https://clickhouse.com/docs/operations/access-rights | Access Control and Account Management | ClickHouse | current docs | T1 | verified |
| 12 | https://www.immuta.com/blog/automate-fine-grained-access-controls-with-policy-as-code/ | Automate fine-grained access controls with policy as code | Immuta | 2025 | T4 | verified — vendor blog |
| 13 | https://www.immuta.com/blog/rbac-vs-abac-for-data-access-control-use-cases/ | RBAC vs ABAC for data access control | Immuta | 2025 | T4 | verified — vendor blog |
| 14 | https://oneuptime.com/blog/post/2026-02-06-immutable-audit-log-pipeline-otel/view | Immutable audit log pipeline using OpenTelemetry | OneUptime | 2026 | T5 | verified — practitioner blog |
| 15 | https://mattermost.com/blog/compliance-by-design-18-tips-to-implement-tamper-proof-audit-logs/ | Compliance by design: tamper-proof audit logs | Mattermost | 2025 | T4 | verified — vendor blog |
| 16 | https://www.junaideffendi.com/p/data-governance-in-lakehouse-using | Data governance in lakehouse using open source tools | Junaid Effendi | 2025 | T5 | verified — practitioner blog |
| 17 | https://www.leolytixco.com/blog/snowflake-rbac | Simplify Snowflake RBAC at scale with Terraform | LeoLytix | 2025 | T5 | verified — practitioner blog |
| 18 | https://www.openpolicyagent.org/docs | Open Policy Agent documentation | CNCF/OPA | current docs | T1 | verified |
| 19 | https://www.datasunrise.com/knowledge-center/data-audit-trails/ | Data audit trails: best practices | DataSunrise | 2025 | T4 | verified — vendor knowledge base |
| 20 | https://netwrix.com/en/resources/blog/data-governance-best-practices/ | 10 data governance best practices for compliance | Netwrix | 2025 | T4 | verified — vendor blog |
| 21 | https://select.dev/posts/snowflake-access-history | Snowflake access history: 8 ways to audit your account | Select | 2025 | T4 | verified — vendor blog |

---

## Sub-question 1: Audit Trail Design and Implementation

### What must an audit trail capture?

Every audit event must record six elements: **actor identity** (who), **action performed** (what), **target resource** (which table/column/row), **timestamp** (when, in UTC/ISO-8601), **origin** (source IP, service account, session), and **outcome** (success/failure with error detail) [15][19]. For data pipelines specifically, audit events must also capture the pipeline run ID, stage identifier, and data lineage context — which upstream sources fed the operation and which downstream consumers will be affected.

The DAMA-DMBOK framework positions audit trails under the Data Security knowledge area, which "protects sensitive information while ensuring appropriate availability" [1]. DMBOK treats audit trails not as a technical feature but as a governance requirement: organizations must define what events are captured, who can access the logs, how long they are retained, and how they are reviewed.

### Immutable append-only storage

Audit logs must be immutable — once written, events cannot be modified or deleted. This is non-negotiable for SOX Section 404 (internal controls over financial reporting), HIPAA audit controls, and SOC 2 Type II (continuous monitoring). Three mechanisms enforce immutability [14][15]:

1. **Append-only storage** — S3 Object Lock in compliance mode, Azure Immutable Blob Storage, or GCS retention policies prevent deletion for specified retention periods
2. **Cryptographic hash chains** — each event includes a SHA-256 hash of its canonical JSON payload; sequential events link through hash chains where modifying any entry breaks the chain and reveals tampering
3. **Separation of duties** — the people who operate systems must not be able to alter audit records; write access is restricted to the logging pipeline, read access to authorized auditors

### OpenTelemetry audit pipeline pattern

A practical implementation uses OpenTelemetry for collection, processing, and dual-export [14]:

1. **Collection**: Applications emit audit events as OTel log records with structured attributes (actor, action, resource, content hash)
2. **Processing**: OTel Collector receives logs, applies filtering and metadata enrichment (collector ID, pipeline version), batches with 5-second flush intervals
3. **Storage**: Dual export to immutable append-only backend (S3 Object Lock) and searchable index (Elasticsearch/OpenSearch) for operational queries

Failure resilience uses persistent sending queues (up to 50,000 batches) with file-based storage, ensuring no events are lost during downstream outages.

### Platform-specific audit capabilities

**Snowflake** provides ACCESS_HISTORY (one row per query with objects accessed/modified), QUERY_HISTORY, and LOGIN_HISTORY views. Critical limitation: ACCESS_HISTORY requires Enterprise Edition. Retention spans 7 days for real-time views to 365 days for historical Account Usage views — insufficient for regulated industries requiring multi-year retention [21]. Teams must export audit data to external long-term storage.

**Databricks Unity Catalog** captures all metastore operations (create, update, delete on catalogs/schemas/tables, permission grants/revokes, data access) in the audit log system table. ABAC operations on tagged assets are logged automatically. Limitation: most audit logs are only accessible from the region in which they are recorded [8].

**ClickHouse** has no native audit logging equivalent to Snowflake's ACCESS_HISTORY or Databricks' system tables. Audit trails require custom implementation — typically inserting records into dedicated logging tables via custom functions on sensitive operations [10]. This gap is significant for compliance-sensitive deployments.

---

## Sub-question 2: Row-Level Security Patterns

### Snowflake row access policies

Snowflake's row access policies (RAPs) are the most mature RLS implementation among the three platforms. RAPs are schema-level objects that evaluate at query runtime through a four-step process: detect policy existence, create dynamic secure view, bind column values to policy parameters, return only rows where the expression evaluates to TRUE [2].

Key architectural details:
- **Owner-context evaluation**: Policies evaluate using the role of the policy owner, not the querying user — this allows policies to reference mapping/entitlement tables that the querying user cannot directly access
- **Nested policy evaluation**: When table and view policies both apply, the table policy executes first, then view policies in sequential order
- **Statement coverage**: Policies apply to SELECT, and also filter rows affected by UPDATE, DELETE, and MERGE — but do not prevent insertions
- **Performance trade-off**: Adding a RAP eliminates metadata-only query optimizations because Snowflake must scan the policy-binding columns. Simple CASE-based policies have negligible cost; policies with mapping table lookups can significantly degrade performance

Limitations: cannot attach to materialized views if the base table has a policy; CURRENT_ROLE() and CURRENT_USER() return NULL in data-sharing consumer accounts; not supported on stream objects [2].

### Databricks row filters

Databricks implements row-level security through SQL UDFs applied as row filters on tables. Two approaches exist [6][7]:

1. **Manual assignment**: Filter functions applied directly to individual tables. Each table supports one row filter. Fine-grained but does not scale.
2. **ABAC policies** (Public Preview): Filter UDFs associated with governed tags. Policies defined at catalog or schema level automatically inherit to child objects. Databricks recommends ABAC for most use cases because "they can be defined by higher-level admins and cannot be overridden by table owners."

Critical limitations: row filters cannot be applied to views (only tables); time travel queries are unsupported on filtered tables; deep and shallow clones cannot be performed on protected tables; requires Databricks Runtime 16.4+ for ABAC [6][7].

### ClickHouse row policies

ClickHouse supports native row policies via `CREATE ROW POLICY` SQL syntax. Policies specify which rows are returned for read-only users querying a table [9]. Once a policy is in place, RLS is enforced — no separate `ALTER TABLE ENABLE ROW LEVEL SECURITY` step is needed.

Key differences from Snowflake and Databricks:
- Policies are primarily designed for read-only users — behavior for write-enabled users is less well-defined
- No ABAC or tag-based policy inheritance — each policy is bound to a specific table and role
- No native mapping-table pattern — dynamic session settings (e.g., `SQL_user_id`) can be used for per-user isolation but require custom integration
- A known security advisory (GHSA-45h5-f7g3-gr8r) documented that RBAC is bypassed when query caching is enabled — teams must verify their ClickHouse version includes the fix

---

## Sub-question 3: Column-Level Access and Masking Policies

### Snowflake dynamic data masking

Snowflake's dynamic data masking applies masking policies at query runtime to column data. At execution time, "the masking policy is applied to the column at every location where the column appears" [3]. Depending on policy conditions, SQL execution context, and role hierarchy, users see plain-text, partially masked, or fully masked values.

Masking policies are schema-level objects managed via DDL (CREATE/ALTER/DROP MASKING POLICY). A single policy can apply to thousands of columns across databases and schemas. Policy content can be changed without reapplying to individual columns [3]. Enterprise Edition required.

### Snowflake tag-based masking

Tag-based masking combines object tagging with masking policies for scalable governance [4]. The workflow:

1. Create a tag (e.g., `sensitivity = 'pii'`)
2. Create masking policies for each data type (STRING, NUMBER, etc.)
3. Assign policies to the tag via `ALTER TAG`
4. Apply the tag to databases, schemas, tables, or columns

When a column's data type matches the masking policy signature, protection applies automatically — no manual per-column assignment. Each tag supports one masking policy per data type. Column-level policies take precedence over tag-based policies when both apply [4].

The scalability advantage is significant: "newly added tables and views are automatically protected" based on column data types, providing proactive governance for future schema changes without manual intervention [4].

### Databricks column masks

Column masks in Unity Catalog control what values users see in specific columns. Each column supports one mask returning the same data type as the masked column. Implementation mirrors row filters — manual assignment per table or ABAC policies via governed tags [6][7].

ABAC column masks use masking UDFs that return actual values or redacted versions based on governed tags. Policies defined at catalog/schema level inherit to child objects. Same limitations as row filters: no view support, no time travel, requires Runtime 16.4+ for ABAC [7].

### ClickHouse column restrictions

ClickHouse implements column-level security through GRANT statements rather than masking policies [9]. Users can only query columns where they have explicit access rights. If a user lacks permissions for specific columns, `SELECT *` fails with an insufficient permissions error — there is no dynamic masking that returns redacted values.

This is a fundamental difference: Snowflake and Databricks mask values (users see redacted data), while ClickHouse restricts access entirely (users see an error). There is no native dynamic masking in ClickHouse — implementing partial masking requires views with conditional logic, which is fragile and does not scale [10].

---

## Sub-question 4: Entitlement Management and Access Review Workflows

### RBAC vs ABAC for data platforms

The choice between role-based and attribute-based access control has significant governance implications [13]:

**RBAC** assigns permissions to roles, and users inherit permissions through role membership. Snowflake's native model is RBAC with role hierarchies. Advantages: simple to understand, audit, and implement. Disadvantage: role explosion — a system with 10 departments, 5 data sensitivity levels, and 3 access types requires up to 150 roles. "A single ABAC policy can replace hundreds of separate roles" [13].

**ABAC** makes access decisions based on attributes of users, resources, and environment. Databricks Unity Catalog ABAC is the clearest data-platform implementation — governed tags on data assets drive policy evaluation. Advantages: scales without role explosion, supports dynamic context (time of day, IP range). Disadvantage: harder to audit ("why does this user have access?"), requires accurate attribute metadata.

**Hybrid approach**: Use RBAC for broad baseline access (analyst role, engineer role) and ABAC for sensitive operations requiring context (PII columns masked unless user has `pii_authorized` tag and is on the corporate network) [13].

### Terraform for access-as-code

Terraform providers for Snowflake and Databricks enable codifying the entire RBAC model — roles, grants, policies — as version-controlled infrastructure [17]:

- **Snowflake Terraform provider**: manages warehouses, databases, schemas, roles, grants, masking policies, and row access policies. Role hierarchies codified as Terraform resources eliminate permission drift.
- **Databricks Terraform provider**: manages Unity Catalog permissions via `databricks_grants` (replace all grants on an object) and `databricks_grant` (add/modify specific grants).

Governance benefits: all access changes are peer-reviewed via pull requests, tracked in Git history, and applied through CI/CD pipelines. Multi-environment isolation uses separate Terraform state files for dev/stage/prod. Common pitfalls addressed: privilege dependencies, role destruction order, state drift, and access rollback complexity [17].

### Access review workflows

Entitlement management requires periodic access reviews — verifying that current permissions remain appropriate [20]. The workflow:

1. **Discovery**: Enumerate all active grants/permissions (Snowflake: SHOW GRANTS; Databricks: Unity Catalog permission APIs)
2. **Review**: Data owners certify that each user's access is still justified. Automated flags for: accounts inactive >90 days, service accounts with broad privileges, roles with no members
3. **Remediation**: Revoke unjustified access, document exceptions with business justification
4. **Cadence**: Quarterly reviews for standard access, monthly for privileged access, immediate for separation events (employee departures)

ClickHouse lacks native entitlement review tooling — teams must build custom queries against `system.grants`, `system.roles`, and `system.users` tables [11].

---

## Sub-question 5: Policy-as-Code Approaches

### Open Policy Agent (OPA)

OPA is a CNCF-graduated general-purpose policy engine that decouples policy decision-making from enforcement [18]. Policies are written in Rego, a declarative language, and evaluated against JSON input at runtime. OPA is well-suited for infrastructure access control (Kubernetes admission, API authorization) but its adoption for data platform governance is limited.

For data platforms, OPA integrates with metadata platforms like DataHub for policy enforcement. Apache Ranger provides more purpose-built data governance: fine-grained access control at database, table, column, and row levels with native Hive Metastore integration [16]. The key distinction is scope: Ranger is designed specifically for data platforms; OPA is general-purpose and requires custom integration.

Practical limitation: OPA policies must maintain strict separation between policy logic and data retrieval. Embedding external calls into Rego policies creates security vulnerabilities and complicates testing [18].

### Immuta policy-as-code

Immuta provides the most mature policy-as-code implementation specifically designed for data governance [12]:

- Policies defined as YAML configuration files stored in Git repositories
- Immuta CLI syncs Git repositories with the Immuta platform
- Change management uses standard Git workflows — pull requests, review, approval, merge
- Policies apply uniformly across regions, availability zones, and cloud platforms
- Baseline policy templates can be deployed across heterogeneous data stacks (Snowflake + Databricks + Redshift)

The approach transforms access control from manual, error-prone processes into "scalable, auditable infrastructure" [12]. However, Immuta is a commercial product with significant licensing cost — this is not an open-source solution.

### Terraform as governance-as-code

For teams without Immuta, Terraform provides a practical policy-as-code approach using native platform providers [17]:

- Snowflake roles, grants, masking policies, and row access policies defined as HCL resources
- Databricks Unity Catalog permissions, ABAC tags, and cluster policies as Terraform resources
- State files provide point-in-time snapshots of all permissions
- `terraform plan` shows proposed access changes before application
- Drift detection identifies manual changes that bypass the code workflow

Limitation: Terraform manages state at the resource level, not the policy-logic level. A row access policy's SQL expression is opaque to Terraform — it can deploy and track the policy object but cannot validate the logic within it. Immuta and OPA operate at the policy-logic level; Terraform operates at the infrastructure level.

---

## Challenge

Challenger research targeted three areas: governance tool maturity for data engineering, practicality of policy-as-code, and governance gaps in open-source stacks.

### Are governance tools mature enough for data engineering?

Maturity varies dramatically by platform. Snowflake's governance stack — row access policies, dynamic data masking, tag-based masking, ACCESS_HISTORY, object tagging, automated classification — is the most complete. Features work together: classify columns automatically, apply tags, bind masking policies to tags, audit access through ACCESS_HISTORY. This is a coherent governance system.

Databricks Unity Catalog is approaching parity through ABAC, but critical features remain in Public Preview (ABAC policies, governed tags at scale). The requirement for Runtime 16.4+ means teams on older runtimes cannot adopt ABAC. Manual row filters and column masks are GA but limited — no view support, no time travel, no cloning on protected tables [6][7].

ClickHouse is the clear outlier. Row policies and column-level GRANT restrictions exist, but there is no native audit logging, no dynamic masking, no tag-based classification, no automated access review tooling. Teams choosing ClickHouse for governance-sensitive workloads must build or buy these capabilities separately [9][10][11]. This is not a maturity problem — it reflects ClickHouse's design priorities (analytical performance over governance features).

Most organizations are stuck between Level 1 (Ad Hoc) and Level 2 (Emerging) on governance maturity models, even when they believe they are more advanced. Moving up one level typically takes 12-24 months.

### Is policy-as-code practical?

Yes, but with important caveats. Terraform-based access management is practical and widely adopted for Snowflake and Databricks [17]. The workflow — define roles and grants in HCL, review via PR, apply via CI/CD — integrates naturally with existing engineering practices. The primary friction is initial migration: codifying existing manual grants into Terraform state requires careful import work.

Immuta's YAML-based policy-as-code goes further by managing policy logic (not just policy objects), but introduces vendor lock-in and licensing cost [12]. OPA/Rego is powerful for infrastructure policies but lacks purpose-built data platform integrations — connecting OPA to Snowflake row access policies requires custom middleware that most teams will not build [18].

The practical path for most data engineering teams: Terraform for access-as-code (roles, grants, policy objects), platform-native features for policy logic (Snowflake RAPs, Databricks ABAC), and Git-based review workflows for change management.

### What governance gaps exist in open-source stacks?

Open-source data governance requires assembling capabilities from multiple disconnected tools, and significant gaps remain [16]:

- **Access control**: Apache Ranger provides fine-grained policies for Hive/Spark/Trino, but has outdated dependencies (Java 8), slow community response on PRs, and version compatibility challenges with modern Trino (requires specific version pairing like Trino 476 + Ranger 2.6.0)
- **Audit logging**: No open-source equivalent to Snowflake ACCESS_HISTORY or Databricks audit system tables. Teams must build custom audit pipelines.
- **Classification and tagging**: Apache Atlas provides classification with tag propagation, but Atlas 2.4.0 broke a two-year release gap — the project's activity level raises sustainability concerns
- **Dynamic masking**: No open-source tool provides Snowflake-equivalent dynamic data masking across arbitrary queries. View-based masking is the workaround but does not scale.
- **Entitlement review**: No open-source tool provides automated access review workflows. Teams must build custom reporting.

The practical reality: open-source governance stacks require 3-5x more engineering effort to achieve capabilities that commercial platforms provide natively. For small teams (fewer than 5 engineers), this investment is difficult to justify.

---

## Findings

### Finding 1: DAMA-DMBOK frames governance as accountability and decision rights, not technology
**Confidence: HIGH**

DAMA-DMBOK positions data governance at the center of all 11 data management knowledge areas. Governance "establishes who decides what, how policies get enforced, and how accountability flows across teams" [1]. This framing is critical for data engineers: governance is not about deploying a tool or enabling a feature. It requires defining ownership structures (data owners, stewards, custodians), establishing decision rights (who can grant access, who reviews access, who handles exceptions), and creating enforcement mechanisms (policies, standards, audit trails). The technical implementations — row access policies, masking, RBAC — are enforcement mechanisms for governance decisions, not governance itself. Teams that start with tooling before defining accountability structures build governance theater: policies exist but nobody owns them, reviews happen but nobody acts on findings, audit logs accumulate but nobody reads them.

### Finding 2: Audit trails require immutable storage with cryptographic integrity and separation of duties
**Confidence: HIGH**

Three properties define a compliant audit trail: immutability (events cannot be modified after writing), integrity (tampering is detectable), and separation (system operators cannot alter audit records) [14][15][19]. The practical implementation uses append-only storage (S3 Object Lock, Azure Immutable Blob), SHA-256 hash chains for tamper evidence, and pipeline-only write access. Snowflake retains audit data for up to 365 days — insufficient for SOX (7 years) or HIPAA (6 years) — requiring external export and long-term storage [21]. Databricks captures Unity Catalog events in audit system tables but limits regional access. ClickHouse has no native audit logging — custom implementation required. Every platform requires supplementary audit infrastructure for multi-year regulatory compliance.

### Finding 3: Snowflake provides the most complete row-level and column-level security among Snowflake, Databricks, and ClickHouse
**Confidence: HIGH**

Snowflake's governance feature set — row access policies with owner-context evaluation, dynamic data masking, tag-based masking with auto-application to matching columns, automated sensitive data classification — forms a coherent system where features compose naturally [2][3][4]. Tag-based masking is the standout: classify sensitive columns (manually or via automated classification), apply tags, bind masking policies to tags, and new tables automatically receive protection. Databricks Unity Catalog ABAC is architecturally comparable (governed tags driving row filters and column masks) but requires Runtime 16.4+, remains in Public Preview, and cannot protect views [6][7]. ClickHouse provides row policies and column-level GRANT restrictions but has no dynamic masking — users see errors instead of redacted values, which is a fundamentally different (and less flexible) security model [9].

### Finding 4: Policy-as-code is practical via Terraform but limited to infrastructure-level management
**Confidence: MODERATE**

Terraform providers for Snowflake and Databricks enable version-controlled, peer-reviewed, CI/CD-deployed access management — roles, grants, policy objects tracked as infrastructure resources [17]. This eliminates permission drift and provides Git-based audit trails for all access changes. However, Terraform manages policy objects, not policy logic. The SQL expression inside a row access policy or the UDF behind a column mask is opaque to Terraform — it deploys the object but cannot validate, test, or reason about the access control logic within. Immuta bridges this gap with YAML-based policy definitions that manage logic, but at significant licensing cost [12]. OPA/Rego provides open-source policy-logic management but lacks native data platform integrations. Most teams will use a hybrid: Terraform for infrastructure, platform-native features for policy logic, Git workflows for change management.

### Finding 5: Open-source governance stacks have critical gaps that require 3-5x more engineering effort to close
**Confidence: MODERATE**

Open-source data governance requires assembling Apache Ranger (access control), Apache Atlas (classification/tagging), OpenLineage/Marquez (lineage), and custom solutions (audit logging, dynamic masking, access review) [16]. Each tool has sustainability concerns: Ranger has outdated Java 8 dependencies and slow PR response; Atlas broke a two-year release gap before version 2.4.0. No open-source tool provides Snowflake-equivalent dynamic masking or automated access review workflows. The practical gap is widest for audit logging and entitlement review — capabilities that commercial platforms provide natively but that open-source stacks leave entirely to custom engineering. For teams committed to open-source, the realistic path is: accept limited governance capabilities initially, build audit logging first (OpenTelemetry pipeline), adopt Ranger for access control on Trino/Spark, and plan for 3-5x the engineering investment compared to commercial alternatives.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Snowflake row access policies evaluate using the policy owner's role, not the querying user's role | [2] | verified | Enables hidden mapping table access for entitlement lookups |
| 2 | Snowflake tag-based masking auto-applies policies to new columns matching data type signatures | [4] | verified | Proactive governance for future schema changes |
| 3 | Snowflake ACCESS_HISTORY requires Enterprise Edition and retains data for max 365 days | [21] | verified | Insufficient for SOX (7yr) and HIPAA (6yr) without external export |
| 4 | Databricks ABAC requires Runtime 16.4+ and is in Public Preview | [7] | verified | Manual row filters/column masks GA on Runtime 12.2+ |
| 5 | Databricks row filters and column masks cannot be applied to views | [6] | verified | Tables only — significant limitation for view-based governance patterns |
| 6 | ClickHouse has no native dynamic data masking — column restriction returns errors, not redacted values | [9][10] | verified | Must use custom views for masking behavior |
| 7 | ClickHouse RBAC is bypassed when query caching is enabled (GHSA-45h5-f7g3-gr8r) | [9] | verified | Security advisory — verify patched version |
| 8 | A single ABAC policy can replace hundreds of RBAC roles | [13] | qualified | Vendor claim from Immuta; magnitude depends on permission matrix complexity |
| 9 | Immuta policy-as-code uses YAML files in Git with CLI-based deployment | [12] | verified | Practical but commercial product with licensing cost |
| 10 | Terraform Snowflake provider manages roles, grants, masking policies, and RAPs as IaC resources | [17] | verified | Eliminates permission drift; requires careful initial state import |
| 11 | Apache Ranger has outdated Java 8 dependencies creating compatibility issues with modern Trino | [16] | qualified | Practitioner-reported; Trino 476 + Ranger 2.6.0 is a proven stable combination |
| 12 | Apache Atlas 2.4.0 broke a two-year release gap; 2.5.0 adds Trino extractor | [16] | verified | Project activity level raises sustainability concerns |
| 13 | Most organizations are between Level 1 (Ad Hoc) and Level 2 (Emerging) on governance maturity | [1] | qualified | Multiple vendor sources cite this; specific percentages vary |
| 14 | Append-only storage with SHA-256 hash chains meets SOC 2, HIPAA, and SOX audit requirements | [14][15] | verified | Requires S3 Object Lock compliance mode or equivalent |
| 15 | DAMA-DMBOK 3.0 launched in 2025 as an evergreening initiative modernizing for AI and cloud-native | [1] | verified | Extends 11 knowledge areas with emerging disciplines |
