---
name: Cross-Cloud Data Sharing
description: "Delta Sharing and Snowflake replication enable cross-cloud/cross-region data access but with fundamentally different architectures -- Delta Sharing shares in place (no duplication) while Snowflake requires physical replication; both introduce egress costs and sovereignty constraints that make multi-cloud architectures 2-3x more expensive than single-cloud"
type: context
related:
  - docs/research/2026-03-22-platform-security-access-control.research.md
  - docs/context/production-platform-comparison.md
  - docs/context/private-networking-data-platforms.md
  - docs/context/finops-governance.md
---

## Key Insight

Cross-cloud data sharing avoids expensive data duplication in theory, but organizations systematically underestimate the cloud infrastructure costs (egress, compute, storage) that make multi-cloud deployments 2-3x more expensive than single-cloud. The decision to go multi-cloud requires a realistic total cost model, not just platform feature comparison.

## Delta Sharing (Databricks)

Delta Sharing enables live data sharing across platforms, clouds, and regions without replication. Two modes:

- **Databricks-to-Databricks**: Uses Unity Catalog with governed access controls and audit logging. Only works within the same environment type -- commercial-to-commercial or GovCloud-to-GovCloud. Cross-environment sharing (commercial-to-GovCloud) is not supported.
- **Open sharing**: Token-based security for non-Databricks consumers. Configurable token lifetime, networking controls, and on-demand revocation.

For intra-cloud sharing, private endpoints and storage firewalls ensure no public access. For cross-cloud sharing, Delta Sharing uses NAT gateway egress IPs and supports existing private connections (site-to-site VPNs, dedicated links).

Unity Catalog + Delta Sharing together enable centralized policy enforcement regardless of where data physically resides. Lakehouse Federation adds cross-platform query without data movement.

## Snowflake Cross-Region Sharing

Snowflake cross-region sharing works through **data replication** -- data is physically copied to target regions. The process: enable replication for the source account, create a replication group containing databases and shares, replicate to target regions.

All replicated data is encrypted at rest and in transit using Snowflake-controlled internal data paths. Global data masking and row-level security apply uniformly across regions.

The fundamental difference from Delta Sharing: Snowflake replication creates physical copies, incurring ongoing storage and replication compute costs. Delta Sharing shares in place.

## Cost Realities

Cross-cloud architectures incur costs that single-cloud deployments avoid:

- **Egress charges**: $0.01-0.02/GB intra-continent, $0.05-0.09/GB inter-continent
- **Delta Sharing**: No data replication, but cross-cloud queries incur compute costs on both sides plus network egress for result transfer
- **Snowflake replication**: Full data copy with ongoing storage and replication compute costs

Organizations budget for platform licensing but underestimate these infrastructure costs.

## Multi-Cloud Security Patterns

Five pillars govern secure multi-cloud data access:

1. **Federated identity** -- centralize in one IdP (Entra ID, Okta), federate to all platforms via SAML/OIDC
2. **Policy-as-code** -- define access policies in Terraform/Pulumi, apply consistently across clouds
3. **Data locality awareness** -- map data residency requirements to regions before configuring cross-cloud access
4. **Egress cost modeling** -- include realistic transfer costs in architecture decisions
5. **Unified audit** -- aggregate logs from all platforms into a central SIEM for cross-cloud correlation

## Data Sovereignty

Organizations must confirm no legal or regulatory restrictions exist before replicating data across geographic regions or countries. This applies to both Snowflake replication (physical copy crosses borders) and Delta Sharing (queries may transfer result sets across regions). Data residency requirements constrain which cross-cloud patterns are legally permissible.

## Takeaway

Default to single-cloud when possible. Cross-cloud data sharing is a capability, not a recommendation. When multi-cloud is architecturally required, Delta Sharing's share-in-place model is cheaper than Snowflake's replication model for read-heavy workloads, but neither eliminates the cost premium of multi-cloud operations. Budget realistically.
