# SLA and Error Budgets

The SRE-derived framework -- SLIs measure, SLOs target, SLAs commit, error budgets prioritize -- provides the most practical structure for data quality commitments. Not all data deserves an SLA. Over-SLA-ing creates the same noise problem as over-alerting.

## SLI / SLO / SLA Hierarchy

- **SLIs** (Service Level Indicators) -- the measured metrics. Example: "Freshness of the orders table measured every hour."
- **SLOs** (Service Level Objectives) -- internal targets, typically stricter than SLAs. Example: "99.5% of tables refreshed within 2 hours."
- **SLAs** (Service Level Agreements) -- contractual commitments with consequences. Example: "Dashboard data will be no more than 4 hours stale."

Alert on SLO violation, not SLA breach. By the time an SLA is breached, the error budget is already consumed.

## Error Budget Calculation

Error budgets define acceptable quality degradation over a measurement window. A 99.5% freshness SLA allows approximately 3.6 hours of cumulative staleness per month.

**Consumption rules:**
- **Budget > 50% remaining:** Ship new features confidently
- **Budget 25-50% remaining:** Review consumption, slow risky changes
- **Budget < 25% remaining:** Freeze new features, focus on reliability

This makes the trade-off between building new pipelines and maintaining existing ones explicit and data-driven.

## Tiered SLA Structures

| Tier | Scope | Example | Strictness |
|------|-------|---------|------------|
| **Tier 1** | Customer-facing | Payment data: 99.9% completeness, 15-min freshness | Strictest SLAs, smallest error budgets, fastest response |
| **Tier 2** | Operational | Daily sales reports: 99% completeness, 2-hour freshness | Moderate SLAs, business-cadence aligned |
| **Tier 3** | Analytical | Trend analysis: 95% completeness, 24-hour freshness | Relaxed SLAs, larger error budgets |

The cost of maintaining SLAs scales with strictness -- a 99.9% SLA requires significantly more engineering investment than 99%.

## Five SLA Dimensions

1. **Timeliness** -- Data arrives within agreed time windows
2. **Completeness** -- Expected records are present
3. **Accuracy** -- Values are correct
4. **Consistency** -- Data agrees across systems
5. **Availability** -- Data is accessible when needed

Start with timeliness and completeness -- they provide the highest signal-to-investment ratio.

## Decision Rules

1. Start with Tier 1 SLAs for customer-facing data products. Expand as measurement matures.
2. Use error budgets to make the feature-vs-reliability trade-off explicit.
3. Document SLAs with measurement queries, not prose descriptions.
4. Alert on SLO violation, not SLA breach.
5. Align monitoring frequency with SLA granularity.
6. Define freshness and completeness SLAs before the first production deploy.
