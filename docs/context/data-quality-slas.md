---
name: Data Quality SLAs
description: "Data quality SLAs must follow the SLI/SLO/SLA hierarchy from SRE with error budgets driving prioritization; tiered SLA structures (customer-facing, operational, analytical) prevent over-SLA-ing; not all data deserves an SLA -- over-SLA-ing creates the same noise problem as over-alerting"
type: context
related:
  - docs/research/2026-03-22-quality-engineering.research.md
  - docs/context/data-quality-dimensions.md
  - docs/context/data-quality-scoring.md
  - docs/context/data-freshness-slas.md
---

## Key Takeaway

The SRE-derived framework -- SLIs measure, SLOs target, SLAs commit, error budgets prioritize -- provides the most practical structure for data quality commitments. Error budgets resolve the feature-vs-reliability tension by making the trade-off quantitative: when the budget is healthy, ship features; when it is depleted, fix quality. Not all data deserves an SLA. Over-SLA-ing creates the same noise problem as over-alerting. Start with Tier 1 (customer-facing) data products and expand as measurement infrastructure matures.

## Error Budgets for Data Quality

Error budgets define the acceptable amount of quality degradation over a measurement window. A 99.5% freshness SLA allows approximately 3.6 hours of cumulative staleness per month. Budget consumption drives engineering prioritization:

- **Budget > 50% remaining**: Ship new features confidently
- **Budget 25-50% remaining**: Review what is consuming the budget, slow risky changes
- **Budget < 25% remaining**: Freeze new features, focus on reliability

This framework makes the trade-off between building new pipelines and maintaining existing ones explicit and data-driven rather than political.

## Tiered SLA Structures

Different data products warrant different SLA commitments:

- **Tier 1 (customer-facing)**: Strictest SLAs, smallest error budgets, fastest response times. Example: payment transaction data with 99.9% completeness, 15-minute freshness.
- **Tier 2 (operational)**: Moderate SLAs aligned with business cadence. Example: daily sales reporting with 99% completeness, 2-hour freshness.
- **Tier 3 (analytical)**: Relaxed SLAs, larger error budgets. Example: trend analysis data with 95% completeness, 24-hour freshness.

The cost of maintaining SLAs scales with strictness -- a 99.9% SLA requires significantly more engineering investment than 99%.

## Implementation Roadmap

1. **Identify high-value targets**: Executive dashboards, core ML models, customer-facing data products.
2. **Define SLIs and SLOs through engineer-stakeholder collaboration**: Engineers propose technically feasible SLIs; stakeholders define acceptable SLO ranges. This must be a conversation, not a unilateral engineering decision.
3. **Document the SLA**: Include clear definitions, actual measurement queries (not prose descriptions), and consequence definitions. Ambiguous SLAs are worse than no SLAs.
4. **Implement SLI tracking**: Centralize measurement with error budget visibility. Monitoring frequency must align with SLA granularity -- check every 30 minutes for a 1-hour SLA.
5. **Establish alerting**: Alert on SLO violation, not just SLA breach. By the time an SLA is breached, the error budget is already consumed.
6. **Monitor error budget consumption**: Track burn rate over time to guide quarterly reviews and team prioritization.

## Relationship to Freshness SLAs

Data freshness SLAs (see related context) are one specific type of data quality SLA focused on timeliness. Quality SLAs are broader -- they cover completeness, accuracy, consistency, and validity in addition to timeliness. The SLI/SLO/SLA hierarchy and error budget mechanics are the same across all quality dimensions.

## Decision Rules

1. Start with Tier 1 SLAs for customer-facing data products. Expand coverage as measurement matures.
2. Use error budgets to make the feature-vs-reliability trade-off explicit.
3. Document SLAs with measurement queries, not prose descriptions.
4. Alert on SLO violation, not SLA breach. SLA breach means the error budget is already gone.
5. Align monitoring frequency with SLA granularity.
