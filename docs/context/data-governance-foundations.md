---
name: Data Governance Foundations
description: "DAMA-DMBOK frames governance as accountability, decision rights, and policy enforcement -- not tooling; most organizations stall between Level 1 (Ad Hoc) and Level 2 (Emerging); governance that starts with tools before defining ownership builds governance theater"
type: context
related:
  - docs/research/2026-03-22-governance-compliance.research.md
  - docs/context/audit-trail-design.md
  - docs/context/row-column-security-comparison.md
  - docs/context/access-control-models.md
---

## Key Insight

Governance is about accountability, decision rights, and policy enforcement -- not tooling. DAMA-DMBOK positions data governance at the center of all 11 data management knowledge areas. Teams that deploy row access policies, masking, and RBAC before defining who owns what, who decides what, and how decisions are enforced build governance theater: policies exist but nobody owns them, reviews happen but nobody acts on findings, audit logs accumulate but nobody reads them.

## DAMA-DMBOK Framework

DAMA-DMBOK (Data Management Body of Knowledge) defines governance as the exercise of authority, control, and shared decision-making over the management of data assets. The framework establishes three pillars:

**Ownership structures** -- Data owners (business accountability), data stewards (day-to-day management), and data custodians (technical implementation). Without these roles explicitly assigned, policies have no enforcement path.

**Decision rights** -- Who can grant access, who reviews access, who handles exceptions. These must be documented and agreed upon before any technical controls are implemented.

**Enforcement mechanisms** -- Policies, standards, procedures, and audit trails that translate governance decisions into observable outcomes. Row access policies, masking, and RBAC are all enforcement mechanisms, not governance itself.

DAMA-DMBOK 3.0 (launched 2025) extends the 11 knowledge areas with emerging disciplines for AI and cloud-native architectures, but the core principle is unchanged: governance is organizational, not technical.

## Governance Maturity

Most organizations are stuck between Level 1 (Ad Hoc) and Level 2 (Emerging) on governance maturity models, even when they believe they are more advanced. Moving up one level typically takes 12-24 months.

The maturity gap manifests concretely: teams have Snowflake row access policies deployed but no documented data owner who reviews whether those policies are correct. Or Terraform manages RBAC grants, but nobody runs quarterly access reviews to verify permissions remain appropriate. The technical controls exist; the governance process does not.

## Open-Source Governance Gaps

Open-source governance stacks require assembling Apache Ranger (access control), Apache Atlas (classification/tagging), OpenLineage/Marquez (lineage), and custom solutions for audit logging, dynamic masking, and access review. Each component has sustainability concerns:

- Apache Ranger has outdated Java 8 dependencies and slow community PR response
- Apache Atlas broke a two-year release gap before version 2.4.0
- No open-source tool provides Snowflake-equivalent dynamic masking or automated access review workflows

The practical gap: open-source governance stacks require 3-5x more engineering effort than commercial alternatives. For teams with fewer than 5 engineers, this investment is difficult to justify.

## Takeaway

Define ownership, decision rights, and review processes before selecting tools. The technical implementation (which platform features, which access model) follows from governance decisions, not the reverse. Start by answering: who owns each data domain, who can grant access, who reviews access quarterly, and who is accountable when a policy fails.
