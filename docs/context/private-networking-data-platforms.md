---
name: Private Networking for Data Platforms
description: "PrivateLink/Private Service Connect is available across Databricks, Snowflake, and ClickHouse but architectures differ significantly — Databricks requires two VPCs, Snowflake supports privatelink-only enforcement to block all public access, ClickHouse restricts to Scale/Enterprise plans with inbound-only connectivity; private networking is necessary but not sufficient for security"
type: context
related:
  - docs/research/2026-03-22-platform-security-access-control.research.md
  - docs/context/production-platform-comparison.md
  - docs/context/cross-cloud-data-sharing.md
---

## Key Insight

PrivateLink eliminates public internet exposure but does not prevent credential compromise or authorized user misuse. The 2024 Snowflake breaches (Ticketmaster, AT&T) occurred via compromised credentials -- PrivateLink would not have stopped them. Network isolation is one layer in defense-in-depth, not a complete security solution.

## Platform Architectures

### Databricks

Databricks supports three Private Link connectivity types:

1. **Inbound (front-end)** -- secures user connections to workspaces (web app, REST API, Databricks Connect)
2. **Outbound (serverless)** -- secures serverless compute connections to customer resources via Network Connectivity Configurations (NCCs), which are account-level regional constructs
3. **Classic (back-end)** -- secures cluster-to-control-plane communication for regulatory mandates

The architecture requires two VPCs: a **transit VPC** (hub with inbound endpoints) and a **compute plane VPC** (workspace + classic endpoints, minimum two subnets across separate Availability Zones). Scale limits apply: 10 NCCs per region per account, 50 workspaces per NCC, 30 S3 endpoints per region, 100 VPC resource endpoints per region. Legacy Hive Metastore (port 3306) does not traverse Private Link.

### Snowflake

Snowflake PrivateLink requires Business Critical edition or higher. Configuration involves generating a federated token via AWS STS, extracting the AWS account ID, authorizing via `SYSTEM$AUTHORIZE_PRIVATELINK`, then creating VPC endpoints and DNS records. Federated tokens expire after 12 hours. Cross-region connectivity is supported but not for PaaS services (S3, KMS).

Snowflake's key differentiator: **privatelink-only enforcement**. Network policies can restrict all connections to private IP ranges, providing a hard guarantee that no traffic traverses the public internet. No other platform offers this as a native toggle.

### ClickHouse Cloud

PrivateLink is available only on **Scale and Enterprise plans** -- lower tiers have no private networking. Connectivity is **inbound-only**: consumer VPCs can reach ClickHouse Cloud, but ClickHouse Cloud cannot connect back via PrivateLink. Outbound connections to customer databases (MySQL/PostgreSQL table functions) require static IP allow-lists. Cross-region is supported across 34+ AWS regions with standard AWS transfer charges.

## Comparison

| Capability | Databricks | Snowflake | ClickHouse Cloud |
|---|---|---|---|
| Minimum plan | All (with customer-managed VPC) | Business Critical | Scale/Enterprise |
| Direction | Bidirectional | Inbound | Inbound only |
| Cross-region | Supported | Supported (not PaaS) | Supported (34+ regions) |
| Public access blocking | Via network config | Native privatelink-only | Via IP allow-lists |

## Takeaway

Design networking per platform -- do not assume a uniform approach. Snowflake offers the strongest isolation guarantee via native privatelink-only enforcement. Databricks requires the most architectural planning (two-VPC topology with scale limits). ClickHouse has the most restrictive availability (plan-gated, inbound-only). In all cases, pair network isolation with strong identity, access control, secrets management, and audit logging.
