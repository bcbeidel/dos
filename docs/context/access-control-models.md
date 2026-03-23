---
name: Access Control Models and Policy-as-Code
description: "RBAC vs ABAC tradeoffs for data platforms; Terraform for access-as-code is practical and widely adopted; Immuta provides policy-logic management but at licensing cost; OPA lacks native data platform integrations; hybrid RBAC+ABAC is the recommended approach"
type: context
related:
  - docs/research/2026-03-22-governance-compliance.research.md
  - docs/research/2026-03-22-platform-security-access-control.research.md
  - docs/context/data-governance-foundations.md
  - docs/context/row-column-security-comparison.md
  - docs/context/secrets-environment-management.md
  - docs/context/secrets-management-rotation.md
---

## Key Insight

Use RBAC for broad baseline access (analyst role, engineer role) and ABAC for sensitive operations requiring context (PII columns masked unless user has `pii_authorized` tag and is on the corporate network). Terraform is the practical path for codifying access as infrastructure. It manages policy objects but not policy logic -- a row access policy's SQL expression is opaque to Terraform, which deploys the object but cannot validate the logic within.

## RBAC vs ABAC

**RBAC** (Role-Based Access Control) assigns permissions to roles. Users inherit permissions through role membership. Snowflake's native model is RBAC with role hierarchies.

- Advantages: simple to understand, audit, and implement
- Disadvantage: role explosion. A system with 10 departments, 5 sensitivity levels, and 3 access types requires up to 150 roles.

**ABAC** (Attribute-Based Access Control) makes decisions based on attributes of users, resources, and environment. Databricks Unity Catalog ABAC is the clearest data-platform implementation -- governed tags on data assets drive policy evaluation.

- Advantages: scales without role explosion, supports dynamic context (time of day, IP range). A single ABAC policy can replace hundreds of separate roles.
- Disadvantage: harder to audit ("why does this user have access?"), requires accurate attribute metadata.

**Hybrid approach** (recommended): RBAC for coarse-grained baseline permissions, ABAC for fine-grained context-dependent restrictions on sensitive data. This gives you the auditability of RBAC and the scalability of ABAC where it matters most.

## Policy-as-Code Approaches

### Terraform (Practical, Widely Adopted)

Terraform providers for Snowflake and Databricks enable version-controlled, peer-reviewed, CI/CD-deployed access management:

- **Snowflake provider**: manages warehouses, databases, schemas, roles, grants, masking policies, and row access policies as HCL resources
- **Databricks provider**: manages Unity Catalog permissions via `databricks_grants` (replace all grants) and `databricks_grant` (add/modify specific grants)

Governance benefits: all access changes are peer-reviewed via pull requests, tracked in Git history, applied through CI/CD pipelines. `terraform plan` shows proposed access changes before application. Drift detection identifies manual changes that bypass the code workflow.

Primary friction: initial migration requires careful import of existing manual grants into Terraform state. Common pitfalls include privilege dependencies, role destruction order, state drift, and access rollback complexity.

**Limitation**: Terraform manages state at the resource level, not the policy-logic level. It deploys a row access policy object but cannot validate or test the SQL expression inside it.

### Immuta (Policy-Logic Management)

Immuta provides the most mature policy-as-code for data governance: YAML configuration files in Git, CLI-based deployment, standard PR workflows, uniform policies across regions and cloud platforms. Baseline policy templates deploy across heterogeneous stacks (Snowflake + Databricks + Redshift). However, Immuta is a commercial product with significant licensing cost -- not an open-source option.

### OPA (General-Purpose, Limited Data Platform Integration)

Open Policy Agent is a CNCF-graduated policy engine using Rego for declarative policies. Well-suited for infrastructure access control (Kubernetes admission, API authorization) but adoption for data platform governance is limited. Connecting OPA to Snowflake row access policies requires custom middleware that most teams will not build.

## Access Review Workflows

Entitlement management requires periodic access reviews:

1. **Discovery**: Enumerate all active grants (Snowflake: SHOW GRANTS; Databricks: Unity Catalog permission APIs; ClickHouse: custom queries against `system.grants`, `system.roles`, `system.users`)
2. **Review**: Data owners certify access is justified. Flag accounts inactive >90 days, service accounts with broad privileges, roles with no members.
3. **Remediation**: Revoke unjustified access, document exceptions.
4. **Cadence**: Quarterly for standard access, monthly for privileged access, immediate for separation events.

## Takeaway

The practical path for most data engineering teams: Terraform for access-as-code (roles, grants, policy objects), platform-native features for policy logic (Snowflake RAPs, Databricks ABAC), and Git-based review workflows for change management. Invest in access review processes, not just access deployment tooling.
