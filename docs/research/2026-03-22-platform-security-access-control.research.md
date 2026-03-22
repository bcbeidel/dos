---
name: "Platform Security & Access Control"
description: "Private networking (PrivateLink) is available across Databricks, Snowflake, and ClickHouse but architectures differ — Databricks requires two VPCs (transit + compute), Snowflake supports privatelink-only enforcement, ClickHouse restricts to Scale/Enterprise plans; RBAC is the universal baseline but insufficient alone — Snowflake's three-tier role hierarchy (access/functional/service) prevents role explosion while Unity Catalog ABAC (governed tags, Runtime 16.4+) enables dynamic policy enforcement; service principals with OAuth M2M and short-lived tokens are the production default — PATs and passwords are anti-patterns; secrets management requires centralized vaults with automated rotation (Vault dynamic secrets generate per-session database credentials with 1h default TTL); audit logging maturity varies — Snowflake ACCESS_HISTORY (Enterprise+) tracks column-level access with 365-day retention while ClickHouse lacks unified audit logging; cross-cloud data sharing via Delta Sharing and Snowflake replication avoids data duplication but introduces egress and sovereignty constraints"
type: research
sources:
  - https://docs.databricks.com/aws/en/security/network/concepts/privatelink-concepts
  - https://docs.snowflake.com/en/user-guide/admin-security-privatelink
  - https://clickhouse.com/docs/manage/security/aws-privatelink
  - https://docs.snowflake.com/en/user-guide/security-access-control-overview
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/privileges
  - https://select.dev/posts/snowflake-rbac-best-practices
  - https://clickhouse.com/docs/operations/access-rights
  - https://docs.databricks.com/aws/en/admin/users-groups/service-principals
  - https://docs.snowflake.com/en/user-guide/key-pair-auth
  - https://docs.databricks.com/aws/en/dev-tools/auth/oauth-m2m
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
  - https://developer.hashicorp.com/vault/tutorials/db-credentials/database-secrets
  - https://docs.databricks.com/aws/en/admin/system-tables/audit-logs
  - https://docs.snowflake.com/en/user-guide/access-history
  - https://docs.snowflake.com/en/user-guide/secure-data-sharing-across-regions-platforms
  - https://docs.databricks.com/aws/en/delta-sharing/
  - https://www.databricks.com/blog/governing-cybersecurity-data-across-multiple-clouds-and-regions-using-unity-catalog-delta
  - https://docs.snowflake.com/en/user-guide/security-disable-public-access-privatelink
  - https://www.osohq.com/learn/rbac-vs-abac-vs-pbac
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-governance-compliance.research.md
  - docs/research/2026-03-22-privacy-engineering.research.md
  - docs/research/2026-03-22-cost-optimization-finops.research.md
---

## Summary

**Research question:** What network, identity, and secrets management patterns govern secure data platform deployments?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 20 | **Searches:** 18 across Google

**Key findings:**
- Private networking (PrivateLink/Private Service Connect) is available across Databricks, Snowflake, and ClickHouse Cloud, but architectures differ significantly — Databricks requires two VPCs (transit + compute plane), Snowflake supports privatelink-only enforcement to block all public access, and ClickHouse restricts PrivateLink to Scale/Enterprise plans with inbound-only connectivity
- RBAC is the universal baseline but insufficient alone at scale — Snowflake's three-tier role architecture (access roles, functional roles, service roles) prevents role explosion, while Databricks Unity Catalog ABAC with governed tags enables dynamic policy enforcement but requires Runtime 16.4+
- Service principals with OAuth M2M and short-lived tokens are the production default for automated workloads — PATs and password-based authentication are anti-patterns that create credential sprawl and lifecycle management debt
- Secrets management requires centralized vaults with automated rotation — Vault dynamic secrets generate per-session database credentials with configurable TTL (1h default, 24h max), eliminating static credential risk entirely
- Audit logging maturity varies dramatically across platforms — Snowflake ACCESS_HISTORY (Enterprise Edition required) tracks column-level data access with 365-day retention, Databricks system tables provide workspace-level audit, while ClickHouse lacks a unified compliance-focused audit structure
- Cross-cloud data sharing via Delta Sharing and Snowflake replication avoids expensive data duplication but introduces egress costs and data sovereignty constraints that must be addressed architecturally

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://docs.databricks.com/aws/en/security/network/concepts/privatelink-concepts | Private Link concepts | Databricks | current docs | T1 | verified |
| 2 | https://docs.snowflake.com/en/user-guide/admin-security-privatelink | AWS PrivateLink and Snowflake | Snowflake | current docs | T1 | verified |
| 3 | https://clickhouse.com/docs/manage/security/aws-privatelink | AWS PrivateLink | ClickHouse | current docs | T1 | verified |
| 4 | https://docs.snowflake.com/en/user-guide/security-access-control-overview | Overview of Access Control | Snowflake | current docs | T1 | verified |
| 5 | https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/ | Unity Catalog ABAC | Databricks | current docs | T1 | verified |
| 6 | https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/privileges | Unity Catalog privileges and securable objects | Databricks | current docs | T1 | verified |
| 7 | https://select.dev/posts/snowflake-rbac-best-practices | Top 7 Snowflake RBAC Best Practices | Select | 2024 | T4 | verified — practitioner guide |
| 8 | https://clickhouse.com/docs/operations/access-rights | Access Control and Account Management | ClickHouse | current docs | T1 | verified |
| 9 | https://docs.databricks.com/aws/en/admin/users-groups/service-principals | Service principals | Databricks | current docs | T1 | verified |
| 10 | https://docs.snowflake.com/en/user-guide/key-pair-auth | Key-pair authentication and key-pair rotation | Snowflake | current docs | T1 | verified |
| 11 | https://docs.databricks.com/aws/en/dev-tools/auth/oauth-m2m | Authorize service principal access with OAuth | Databricks | current docs | T1 | verified |
| 12 | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | Secrets Management Cheat Sheet | OWASP | current | T2 | verified — industry standard |
| 13 | https://developer.hashicorp.com/vault/tutorials/db-credentials/database-secrets | Dynamic secrets for database credential management | HashiCorp | current docs | T1 | verified |
| 14 | https://docs.databricks.com/aws/en/admin/system-tables/audit-logs | Audit log system table reference | Databricks | current docs | T1 | verified |
| 15 | https://docs.snowflake.com/en/user-guide/access-history | Access History | Snowflake | current docs | T1 | verified |
| 16 | https://docs.snowflake.com/en/user-guide/secure-data-sharing-across-regions-platforms | Share data securely across regions and cloud platforms | Snowflake | current docs | T1 | verified |
| 17 | https://docs.databricks.com/aws/en/delta-sharing/ | What is Delta Sharing? | Databricks | current docs | T1 | verified |
| 18 | https://www.databricks.com/blog/governing-cybersecurity-data-across-multiple-clouds-and-regions-using-unity-catalog-delta | Governing data across clouds and regions | Databricks | 2024 | T4 | verified — vendor blog |
| 19 | https://docs.snowflake.com/en/user-guide/security-disable-public-access-privatelink | Enforcement of privatelink-only access | Snowflake | current docs | T1 | verified |
| 20 | https://www.osohq.com/learn/rbac-vs-abac-vs-pbac | RBAC vs ABAC vs PBAC | Oso | 2025 | T4 | verified — security vendor guide |

---

## Sub-question 1: Private Networking for Data Platforms

### Databricks private connectivity architecture

Databricks supports three types of Private Link connectivity, each securing a different traffic path [1]:

1. **Inbound (front-end)** — Secures user connections to workspaces via VPC interface endpoints, protecting access to the web application, REST API, and Databricks Connect API
2. **Outbound (serverless)** — Secures connections from serverless compute to customer resources using Network Connectivity Configurations (NCCs), which are account-level regional constructs managing private endpoint creation at scale
3. **Classic (back-end)** — Secures cluster-to-control-plane communication, addressing regulatory mandates requiring all internal cloud traffic to remain on a private network

The architecture requires two distinct VPCs. The **transit VPC** functions as a central hub containing inbound VPC endpoints for client access. The **compute plane VPC** hosts the workspace and classic VPC endpoints, requiring at least two subnets in separate Availability Zones plus an additional subnet for VPC endpoints [1].

Scale limits apply: maximum 10 NCCs per region per account, up to 50 workspaces per NCC, S3 endpoints limited to 30 per region, and VPC resource endpoints limited to 100 per region. Network ACLs must allow `0.0.0.0/0` for subnet-level traffic control. Legacy Hive Metastore connectivity (port 3306) does not traverse Private Link [1].

### Snowflake PrivateLink architecture

Snowflake PrivateLink establishes direct, secure connectivity between customer AWS VPCs and the Snowflake VPC without traversing the public internet. Business Critical edition or higher is required [2].

Configuration requires a four-step process: generate a federated token via AWS STS, extract the AWS account ID, authorize via `SYSTEM$AUTHORIZE_PRIVATELINK`, then create VPC endpoints and DNS records. Federated tokens expire after 12 hours. Cross-region connectivity is supported — a Snowflake account in one region can connect to a VPC in another — but cross-region is not supported for PaaS services like S3 or KMS [2].

Snowflake's key differentiator is **privatelink-only enforcement**: organizations can optionally block all public access to Snowflake by implementing network policies with CIDR blocks restricting connections to private IP ranges only. This ensures every connection traverses PrivateLink, providing a hard guarantee that no traffic flows over the public internet [19].

### ClickHouse Cloud private networking

ClickHouse Cloud supports AWS PrivateLink, Azure Private Link, and GCP Private Service Connect, but only on **Scale and Enterprise plans** — lower tiers have no private networking option [3].

PrivateLink is unidirectional: consumer VPCs can connect to ClickHouse Cloud, but ClickHouse Cloud cannot connect back to customer VPCs via PrivateLink. For outbound connectivity (e.g., MySQL/PostgreSQL table functions accessing customer databases), security groups must allow ClickHouse's static IP addresses — PrivateLink cannot facilitate this direction [3].

Cross-region PrivateLink is supported across 34+ AWS regions, though AWS cross-region data transfer charges apply. Configuration requires four steps: obtain service endpoint details, create AWS VPC endpoint (ports 443, 8443, 9440, 3306), register endpoint ID in ClickHouse allow-list, and configure private DNS [3].

### Platform comparison

| Capability | Databricks | Snowflake | ClickHouse Cloud |
|---|---|---|---|
| PrivateLink support | AWS, Azure, GCP | AWS, Azure | AWS, Azure, GCP |
| Minimum plan | All plans with customer-managed VPC | Business Critical | Scale/Enterprise |
| Direction | Bidirectional (inbound + outbound) | Inbound | Inbound only |
| Cross-region | Supported | Supported (not for PaaS) | Supported (34+ regions) |
| Public access blocking | Via network configuration | Native privatelink-only enforcement | Via IP allow-lists |

---

## Sub-question 2: RBAC vs ABAC Design Patterns and Platform Implementations

### RBAC vs ABAC fundamentals

RBAC (Role-Based Access Control) grants permissions based on predefined roles — the "who does what" layer. ABAC (Attribute-Based Access Control) evaluates attributes of the user, resource, and environment to make dynamic access decisions — the "under what conditions" layer [20].

RBAC is simpler to implement and audit but leads to **role explosion** when systems span multiple teams, geographies, or tenants — dozens or hundreds of roles are required to capture nuanced access conditions. ABAC offers fine-grained, context-sensitive control but is more complex to manage and harder to audit. The emerging best practice is a hybrid approach: RBAC for coarse-grained baseline permissions, ABAC for fine-grained dynamic controls [20].

### Snowflake RBAC hierarchy

Snowflake combines three access control models: Discretionary Access Control (DAC), where each object has an owner who grants access; Role-Based Access Control (RBAC), where privileges are assigned to roles and roles to users; and User-Based Access Control (UBAC) for direct privilege assignment when secondary roles are enabled [4].

The system-defined role hierarchy has five built-in roles [4]:
- **ACCOUNTADMIN** — top-level role encompassing SYSADMIN and SECURITYADMIN capabilities
- **SECURITYADMIN** — manages grants globally, oversees users/roles, inherits USERADMIN
- **SYSADMIN** — creates warehouses, databases, and other objects
- **USERADMIN** — dedicated to user and role creation only
- **PUBLIC** — pseudo-role automatically granted to every user and role

The production best practice is a three-tier custom role architecture [7]:

1. **Access roles** — low-level building blocks controlling database/schema/object access (e.g., `DB_ANALYTICS_READ`, `DB_ANALYTICS_READWRITE`). Never granted directly to users.
2. **Functional roles** — business-aligned roles composed of access roles, granted to human users (e.g., `DATA_ANALYST`, `DATA_ENGINEER`). Single point of change for permission updates.
3. **Service roles** — identical to functional roles but for service accounts and automated tools (e.g., `SVC_DBT`, `SVC_AIRBYTE`).

Critical anti-patterns to avoid: granting access roles directly to users (bypasses the functional layer), granting functional roles to other functional roles (creates unmaintainable hierarchies), and skipping `FUTURE GRANTS` (causes manual toil whenever new objects are created) [7].

### Unity Catalog privilege model (Databricks)

Unity Catalog uses a standard RBAC privilege model where privileges are granted on securable objects (catalogs, schemas, tables, volumes, functions) to principals (users, groups, service principals). Privileges include `SELECT`, `MODIFY`, `CREATE`, `USAGE`, and `MANAGE` [6].

Unity Catalog ABAC complements the privilege model with tag-based dynamic policy enforcement [5]. ABAC uses three components:

1. **Governed tags** — defined at the account level using tag policies, representing attributes like data sensitivity or classification. Tags are assigned to tables, schemas, or catalogs.
2. **Policies** — created at catalog, schema, or table level with inheritance (catalog-level policies cascade to all child objects)
3. **User-defined functions** — row filters and column masks that evaluate access based on governed tags

ABAC requires **Databricks Runtime 16.4 or above** or serverless compute [5]. Key limitations: only one row filter or column mask can apply per user-table combination (multiple conflicting policies block access entirely); time travel and cloning are blocked unless users are explicitly excluded; ABAC does not apply directly to views; and Delta Sharing requires both sharing permissions and ABAC policy exemption [5].

### ClickHouse access control

ClickHouse implements RBAC with five entities: user accounts, roles, row policies, settings profiles, and quotas [8]. Two configuration methods exist — SQL-driven (recommended) and file-based (`users.xml`) — but the same entity cannot be managed by both methods simultaneously.

ClickHouse RBAC has notable limitations compared to commercial platforms [8]:
- Privileges granted to non-existent databases/tables remain valid indefinitely
- No lifetime settings for privileges (no automatic expiration)
- Row policies only function with read-only access — modification capability defeats row-level restrictions
- Deleted table privileges persist and require explicit `REVOKE` statements
- No ABAC equivalent — all access control is role-based

---

## Sub-question 3: Service Principal Design and Least-Privilege Patterns

### Databricks service principals

Service principals are specialized identities designed for automation and programmatic access [9]. They differ from user accounts in purpose: user accounts are for interactive access tied to individuals; service principals are for programmatic, automation-focused identities that persist independently of the employee lifecycle. This structural separation prevents job failures when users depart or group memberships change.

Service principals are managed at two levels [9]:
- **Account-level** — account admins add service principals to accounts and assign admin roles
- **Workspace-level** — workspace admins add service principals to specific workspaces and control scope

Common deployment patterns include CI/CD pipeline automation, scheduled ETL jobs, cross-system data integrations, and infrastructure-as-code provisioning (Terraform, ARM templates) [9].

Authentication uses **OAuth M2M** (machine-to-machine) as the recommended approach [11]. Each OAuth access token is valid for one hour and can be generated at account level (for both account-level and workspace-level APIs) or workspace level (for single-workspace APIs). Scopes enforce least privilege — applications should request only the scopes they need. PATs (Personal Access Tokens) are still supported but considered a legacy pattern — any token lasting months is a liability.

### Snowflake service account authentication

Snowflake enforces authentication method restrictions based on user type [10]. Users marked as `TYPE=SERVICE` can only authenticate via key-pair or OAuth — never password + MFA. This prevents the common anti-pattern of service accounts using shared passwords.

Key-pair authentication requires a minimum 2048-bit RSA key pair (RSA or ECDSA algorithms supported) [10]. Snowflake supports dual active keys through `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` parameters, enabling zero-downtime key rotation:
1. Generate a new key pair
2. Assign the new public key to the unused parameter slot
3. Update client configuration with the new private key
4. Remove the old public key once migration is complete

Private keys should be encrypted with passphrases complying with PCI DSS standards and stored in enterprise-grade secret managers (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) — never in files or plaintext environment variables [10]. Network policies should restrict service account connections to authorized IP addresses.

### Least-privilege implementation patterns

Across all platforms, the principle of least privilege follows a consistent pattern:

1. **One service principal per workload** — do not share credentials across applications, pipelines, or environments
2. **Minimum required permissions** — grant only `CAN USE` or `CAN QUERY` for read workloads; `SELECT` only for analytics; `INSERT`/`UPDATE` only for ETL write targets
3. **Environment isolation** — use different workspaces/accounts to separate development, staging, and production
4. **Short-lived credentials** — OAuth tokens (1h TTL) or Vault dynamic secrets (configurable TTL) over static PATs or passwords
5. **Credential rotation** — rotate when personnel change, on a fixed schedule (30-90 days for static credentials), or continuously via dynamic secrets

---

## Sub-question 4: Secrets Management and Rotation Strategies

### Secrets management architecture

OWASP defines four lifecycle phases for secrets: creation (cryptographically robust generation with minimum required privileges), rotation (regular cycling to limit compromised credential utility), revocation (immediate disabling when no longer needed or potentially compromised), and expiration (time-based automatic invalidation) [12].

Core requirements from OWASP [12]:
- **Never store secrets in plaintext** — encrypt at rest using AES-256-GCM or ChaCha20-Poly1305
- **Centralize management** — use dedicated solutions (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, HashiCorp Vault) rather than scattered configuration files
- **Enforce transport security** — TLS for all secret transmission
- **Implement detection** — pre-commit hooks, CI/CD scanning, and signature matching to catch accidental exposure
- **Separate environments** — use distinct vaults/instances for production and development

### HashiCorp Vault dynamic secrets

Vault's database secrets engine generates credentials dynamically upon request rather than using static, long-lived credentials [13]. The mechanism:

1. Administrator configures a database connection with root credentials and defines roles with SQL templates
2. Application requests credentials through a role-based endpoint
3. Vault connects to the database, creates a new user with a random password and defined permissions
4. Vault returns credentials with a unique `lease_id` for tracking
5. Credentials automatically expire after the configured TTL (default 1h, max 24h)

Each credential set is unique and short-lived. If an application is compromised, only that application's credentials require revocation — not a global credential rotation. The `lease_id` enables audit trail correlation between Vault access logs and database activity [13].

Dynamic secrets are the ideal pattern for data platform deployments: ETL jobs receive per-execution database credentials that expire when the job completes. No static passwords exist to leak, share, or forget to rotate.

### Cloud-native secrets managers

**AWS Secrets Manager** supports automatic rotation of RDS, Redshift, and DocumentDB secrets via Lambda rotation functions. Custom Lambda functions can rotate other credential types. Rotation policies run automatically and audit logs capture every access and rotation event.

**Azure Key Vault** provides secret versioning (updating a secret with the same name creates a new version) and event-driven rotation via Azure Functions triggered by Key Vault events. Separate Key Vaults for different security domains limit blast radius.

**GCP Secret Manager** uses a notification-driven rotation model where Cloud Scheduler triggers rotation via pub/sub messages.

### Rotation frequency guidance

Rotation frequency depends on the secret type and risk profile:
- **Dynamic database credentials** — per-session (minutes to hours via Vault)
- **Service principal OAuth tokens** — automatically expire after 1 hour (Databricks M2M)
- **API keys and static credentials** — 30-90 day rotation schedule
- **RSA key pairs** — 90-day rotation with dual-key zero-downtime pattern (Snowflake)
- **TLS certificates** — before expiration, with automated renewal via ACME or cert-manager

---

## Sub-question 5: Audit Logging for Security and Compliance

### Databricks audit logging

Databricks audit logs are stored in the `system.access.audit` system table (Public Preview) [14]. Key schema fields:

- **Temporal**: `event_time` (UTC timestamp), `event_date`
- **Identity**: `user_identity` (struct with email), `identity_metadata` (tracks `run_by` and `run_as` for delegated actions)
- **Request tracking**: `request_id`, `session_id`, `source_ip_address`, `user_agent`
- **Action details**: `action_name`, `request_params` (key-value map), `response` (status codes and error messages)
- **Classification**: `audit_level` distinguishes workspace and account-level events

Most audit logs are only available in the region of the workspace. Account-level events record `workspace_id` as `0`. Detections can be applied as Databricks SQL Alerts running on a recurring schedule, sending notifications via email, webhook, PagerDuty, or Slack [14].

### Snowflake audit logging

Snowflake provides audit capabilities through the ACCOUNT_USAGE schema, with ACCESS_HISTORY as the most granular view [15]. ACCESS_HISTORY tracks:

- **direct_objects_accessed** — objects explicitly named in queries
- **base_objects_accessed** — original source tables underlying views and other abstractions
- **objects_modified** — targets of write operations (INSERT, UPDATE, DELETE, COPY)
- **policies_referenced** — row access and masking policies enforced during queries
- **object_modified_by_ddl** — DDL operations on databases, schemas, tables, views, columns

ACCESS_HISTORY requires **Enterprise Edition or higher** and tracks parent/root query IDs to trace relationships between queries and nested stored procedure calls [15]. Retention is 365 days for ACCOUNT_USAGE views. For organizations in highly regulated industries requiring multi-year audit trails, this one-year cap requires external archival strategies.

LOGIN_HISTORY logs all authentication attempts. QUERY_HISTORY captures all executed queries with performance metrics. Together, these views enable comprehensive compliance auditing: who accessed what data, when, from where, and what operations they performed.

### ClickHouse audit logging gaps

ClickHouse emits access-related information through system logs and system tables — role-based access control checks, failed authentication attempts, user and role modifications, and privilege enforcement outcomes [8]. However, these events are **not unified into a compliance-focused audit structure**. There is no equivalent to Snowflake's ACCESS_HISTORY or Databricks' system tables. Organizations requiring SOC 2 or HIPAA compliance with ClickHouse must implement external audit logging (e.g., DataSunrise, custom log aggregation) to achieve parity with commercial platforms.

### Audit logging comparison

| Capability | Databricks | Snowflake | ClickHouse |
|---|---|---|---|
| Unified audit table | `system.access.audit` (Preview) | ACCOUNT_USAGE views | None (fragmented logs) |
| Column-level access tracking | Via Unity Catalog lineage | ACCESS_HISTORY | Not available |
| Retention | Region-specific | 365 days | Log-dependent |
| Required edition | All plans | Enterprise+ (ACCESS_HISTORY) | N/A |
| Real-time alerting | DBSQL Alerts on system tables | Via external SIEM integration | Via external tools only |

---

## Sub-question 6: Cross-Cloud and Cross-Region Access Patterns

### Delta Sharing (Databricks)

Delta Sharing enables secure sharing of live data across platforms, clouds, and regions without data replication [17]. Two sharing modes exist:

- **Databricks-to-Databricks** — uses Unity Catalog integration with governed access controls and audit logging. Only supported within the same environment type (commercial-to-commercial, GovCloud-to-GovCloud) — cross-environment sharing is not supported [17].
- **Open sharing** — token-based security for non-Databricks consumers, with configurable token lifetime, networking controls, and on-demand access revocation.

For intra-cloud sharing, private endpoints, storage firewalls, and network gateways ensure no public access. For cross-cloud sharing, Delta Sharing leverages NAT gateway egress IPs and supports existing cross-cloud private connections (site-to-site VPNs, dedicated links) [17].

Unity Catalog and Delta Sharing together enable multi-cloud, multi-region governance: centralized policy enforcement regardless of where data physically resides, with Lakehouse Federation enabling cross-platform query without data movement [18].

### Snowflake cross-region sharing

Snowflake supports cross-region data sharing through replication [16]. The process involves enabling replication for the source account, creating a replication group containing databases and shares, and replicating to target regions. All replicated data is encrypted at rest and in transit using Snowflake-controlled internal data paths — not public internet routes [16].

Global data masking policies and row-level security apply uniformly across regions, ensuring consistent governance regardless of which cloud region accesses the data. RBAC applies identically across standard and hybrid tables.

Critical consideration: organizations must confirm no legal or regulatory restrictions exist before replicating data to accounts in different geographic regions or countries. Unlike Delta Sharing, Snowflake cross-region sharing requires data replication — the data is physically copied, incurring storage and egress costs [16].

### Multi-cloud security patterns

Three pillars govern multi-cloud data security: Identity and Access Management (IAM), Policy Enforcement, and Encryption. Organizations implementing zero-trust security validate all access requests based on least-privilege controls regardless of network location.

Practical multi-cloud access patterns:
1. **Federated identity** — centralize identity in one IdP (Entra ID, Okta) and federate to all platforms via SAML/OIDC
2. **Policy-as-code** — define access policies in Terraform/Pulumi and apply consistently across clouds
3. **Data locality awareness** — map data residency requirements to regions before configuring cross-cloud access
4. **Egress cost modeling** — cross-cloud data transfer incurs significant egress charges (typically $0.01-0.02/GB intra-continent, $0.05-0.09/GB inter-continent)
5. **Unified audit** — aggregate audit logs from all platforms into a central SIEM for cross-cloud correlation

---

## Challenge

Challenger research targeted the practical complexity of private networking, the RBAC vs ABAC maturity gap, service principal lifecycle risks, secrets management operational burden, audit logging sufficiency, and cross-cloud cost assumptions. Six findings were challenged.

### Private networking is necessary but not sufficient for data security

PrivateLink eliminates public internet exposure, which addresses network-level attacks and satisfies compliance requirements. But PrivateLink does not protect against authorized user misuse, credential compromise, or application-layer vulnerabilities. Teams that deploy PrivateLink and consider networking "done" create a false sense of security. Network isolation is one layer in a defense-in-depth strategy that must include identity, access control, encryption, audit logging, and secrets management. The Snowflake breaches of 2024 (Ticketmaster, AT&T) occurred via compromised credentials, not network-level attacks — PrivateLink would not have prevented them.

### ABAC sounds powerful but operational complexity is real

Unity Catalog ABAC with governed tags is architecturally elegant — define policies once, apply dynamically via tags. In practice, ABAC introduces operational complexity that RBAC does not have [5]. Only one row filter or column mask can apply per user-table combination; conflicting policies silently block access. Time travel and cloning are disabled by default. Views do not inherit ABAC policies directly. Runtime 16.4+ is required, meaning older clusters cannot access ABAC-secured tables. Teams must weigh the governance benefits against the operational overhead. For organizations with fewer than 50 data assets, RBAC with explicit grants is simpler and more auditable.

### Service principal lifecycle management is the actual hard problem

Creating a service principal is trivial. Managing its lifecycle — rotating credentials, auditing usage, decommissioning when workloads retire, preventing privilege accumulation over time — is the operational challenge that organizations underestimate [9]. Service principals accumulate permissions through incremental "just add this grant" requests and rarely lose permissions through cleanup. The result is privilege creep that violates least privilege within months of deployment. Automated access reviews (quarterly minimum) and just-in-time access provisioning are necessary countermeasures, but neither is built into Databricks or Snowflake natively.

### Vault dynamic secrets are ideal but operationally demanding

Dynamic database credentials eliminate static credential risk entirely [13]. But operating Vault at production scale requires its own infrastructure: HA deployment, storage backend management, seal/unseal procedures, disaster recovery, and operational expertise. HCP Vault Secrets (SaaS) reduces this burden but introduces vendor dependency and may not satisfy data residency requirements. For teams without dedicated platform engineering capacity, AWS Secrets Manager or Azure Key Vault with automated rotation provides 80% of the security benefit at 20% of the operational cost.

### Snowflake's 365-day audit retention is insufficient for regulated industries

ACCOUNT_USAGE views retain data for 365 days [15]. SOC 2 requires audit trail retention for the audit period (typically 12 months — barely covered). HIPAA requires 6 years. PCI DSS requires 1 year minimum with 3 months immediately available. Financial services regulations often require 7 years. Organizations in regulated industries must implement external audit log archival from day one — not as an afterthought when the first compliance audit reveals gaps. Snowflake does not provide native long-term audit archival; teams must stream logs to external storage (S3, Azure Blob) via scheduled tasks.

### Cross-cloud data sharing cost models are systematically underestimated

Delta Sharing avoids data replication, but cross-cloud queries still incur compute costs on both sides and network egress for result transfer [17][18]. Snowflake cross-region sharing requires full data replication with ongoing storage and replication compute costs [16]. In both cases, organizations budget for the platform licensing but underestimate the cloud infrastructure costs (egress, storage, compute) that make cross-cloud architectures 2-3x more expensive than single-cloud deployments. The architectural decision to go multi-cloud must include a realistic total cost model, not just platform feature comparison.

---

## Findings

### Finding 1: Private networking requires platform-specific architecture with significant configuration differences
**Confidence: HIGH**

PrivateLink/Private Service Connect is universally available across Databricks, Snowflake, and ClickHouse Cloud, but the architectures are not equivalent. Databricks requires a two-VPC topology (transit + compute plane) with scale limits (10 NCCs per region, 50 workspaces per NCC). Snowflake provides the strongest isolation guarantee with native privatelink-only enforcement that blocks all public access. ClickHouse restricts private networking to Scale/Enterprise plans with inbound-only connectivity — outbound connections to customer databases must use static IP allow-lists. All three support cross-region connectivity. Teams must design networking per platform, not assume a uniform approach.

### Finding 2: RBAC is the necessary baseline; ABAC is valuable at scale but operationally complex
**Confidence: HIGH**

RBAC works for all three platforms and should be the starting point. Snowflake's three-tier role hierarchy (access/functional/service roles) is the most prescriptive and scalable RBAC pattern, preventing role explosion through compositional design. Unity Catalog ABAC adds dynamic policy enforcement via governed tags but requires Runtime 16.4+, introduces restrictions on time travel and cloning, and limits row filter/column mask combinations. ClickHouse RBAC works but lacks ABAC, privilege expiration, and audit logging parity. The practical threshold for investing in ABAC is when RBAC role count exceeds manageable levels (typically 50+ roles) or when data classification drives access decisions across many assets.

### Finding 3: Service principals with OAuth M2M and short-lived tokens are the production authentication standard
**Confidence: HIGH**

Service principals should be the exclusive identity type for automated workloads — never personal user accounts. Databricks OAuth M2M tokens expire after 1 hour and support scope-based least privilege. Snowflake `TYPE=SERVICE` users enforce key-pair or OAuth only (password authentication is blocked), with dual-key rotation enabling zero-downtime credential cycling. PATs, long-lived tokens, and password-based service accounts are anti-patterns that create credential sprawl, prevent rotation, and couple pipeline reliability to individual employee lifecycle events. One service principal per workload, minimum required permissions, and environment isolation are non-negotiable production patterns.

### Finding 4: Centralized secrets management with automated rotation is essential, but operational complexity varies by solution
**Confidence: HIGH**

OWASP mandates centralized secrets management with automated rotation, detection, and incident response capabilities. Vault dynamic secrets provide the strongest security posture by generating per-session database credentials that expire automatically — no static passwords exist to compromise. But Vault requires significant operational investment (HA deployment, seal management, DR). Cloud-native alternatives (AWS Secrets Manager, Azure Key Vault) offer managed rotation for their respective platform databases with lower operational overhead. The minimum viable secrets strategy: centralize all credentials in a secrets manager, enable automated rotation on a 30-90 day schedule for static secrets, implement pre-commit detection for accidental exposure, and audit all access.

### Finding 5: Audit logging maturity is a key differentiator between platforms and requires external archival for compliance
**Confidence: HIGH**

Snowflake ACCESS_HISTORY provides the most granular audit capability — column-level data access tracking with policy enforcement visibility — but requires Enterprise Edition and has a 365-day retention limit that is insufficient for HIPAA (6 years), financial regulations (7 years), and some SOC 2 implementations. Databricks system tables (`system.access.audit`) provide workspace-level audit with alerting capabilities but are in Public Preview. ClickHouse lacks unified audit logging entirely — events are scattered across system logs without a compliance-focused structure. All platforms require external audit log archival for regulated industries. Organizations should stream audit logs to durable storage (S3, Azure Blob, GCS) and a SIEM from day one.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Databricks PrivateLink requires two VPCs: transit (inbound endpoints) and compute plane (workspace + classic endpoints) | [1] | verified | At least two subnets in separate AZs required for compute plane |
| 2 | Snowflake supports privatelink-only enforcement to block all public access | [19] | verified | Network policies restrict connections to private IP ranges |
| 3 | ClickHouse Cloud PrivateLink is restricted to Scale and Enterprise plans | [3] | verified | Lower tiers have no private networking option |
| 4 | ClickHouse PrivateLink is inbound-only — outbound connections require static IP allow-lists | [3] | verified | Cannot use PrivateLink for ClickHouse-to-customer-database connections |
| 5 | Snowflake ACCESS_HISTORY requires Enterprise Edition and has 365-day retention | [15] | verified | Insufficient for HIPAA (6yr), financial regulations (7yr) |
| 6 | Unity Catalog ABAC requires Databricks Runtime 16.4+ or serverless compute | [5] | verified | Older clusters cannot access ABAC-secured tables |
| 7 | Snowflake `TYPE=SERVICE` users can only authenticate via key-pair or OAuth, never password | [10] | verified | Prevents shared-password anti-pattern for service accounts |
| 8 | Vault dynamic database credentials default to 1h TTL with 24h maximum | [13] | verified | Each credential set is unique with a trackable lease_id |
| 9 | Databricks OAuth M2M access tokens are valid for one hour | [11] | verified | Can be generated at account or workspace level |
| 10 | Snowflake key-pair rotation supports dual active keys for zero-downtime rotation | [10] | verified | RSA_PUBLIC_KEY and RSA_PUBLIC_KEY_2 parameters |
| 11 | OWASP requires secrets encrypted at rest with AES-256-GCM or ChaCha20-Poly1305 | [12] | verified | Industry-standard guidance applicable to all data platforms |
| 12 | Databricks-to-Databricks Delta Sharing only works within the same environment type | [17] | verified | Commercial-to-commercial, GovCloud-to-GovCloud; no cross-environment |
| 13 | Snowflake cross-region sharing requires data replication (physical copy) unlike Delta Sharing | [16] | verified | Incurs storage and egress costs; Delta Sharing shares in place |
| 14 | ClickHouse RBAC has no privilege expiration — grants to non-existent objects persist indefinitely | [8] | verified | Explicit REVOKE required; no automatic cleanup |
| 15 | Only one ABAC row filter or column mask can apply per user-table combination in Unity Catalog | [5] | verified | Multiple conflicting policies block access entirely |
