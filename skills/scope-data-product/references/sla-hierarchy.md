# SLA Hierarchy and Error Budgets

## SLI / SLO / SLA Hierarchy

Define the indicator first, set the objective, then negotiate the agreement.

| Concept | Definition | Example |
|---------|-----------|---------|
| **SLI** (Service Level Indicator) | The measured metric | Freshness of orders table measured every hour |
| **SLO** (Service Level Objective) | Internal target, typically stricter than SLA | 99.5% of tables refreshed within 2 hours |
| **SLA** (Service Level Agreement) | Contractual commitment with consequences | Dashboard data will be no more than 4 hours stale |
| **Error Budget** | Acceptable violation rate | 99.5% compliance ~ 3.6 hours/month of violations |

## Five SLA Dimensions

Start with timeliness and completeness — they provide the highest signal-to-investment ratio.

| Dimension | What to Measure | Typical SLI |
|-----------|----------------|-------------|
| **Timeliness** | Data arrives within agreed windows | Max age of latest record in destination |
| **Completeness** | Expected records are present | Row count vs expected; null rate on required fields |
| **Accuracy** | Values are correct | Distribution checks, cross-system reconciliation |
| **Consistency** | Data agrees across systems | Source-destination reconciliation |
| **Availability** | Data is accessible when needed | Uptime of query endpoints and dashboards |

## Error Budget Calculation

A 99.5% freshness SLA allows ~3.6 hours of cumulative staleness per month.

| Budget Remaining | Action |
|:----------------:|--------|
| > 50% | Ship new features confidently |
| 25-50% | Review budget consumption, slow risky changes |
| < 25% | Freeze new features, focus on reliability |

Error budgets make the feature-vs-reliability tradeoff explicit and data-driven.

## Tiered SLA Structures

Not all data deserves an SLA. Over-SLA-ing creates the same noise as over-alerting.

| Tier | Example | Freshness | Completeness |
|------|---------|-----------|-------------|
| **Tier 1** (customer-facing) | Payment transactions | 15 min | 99.9% |
| **Tier 2** (operational) | Daily sales reporting | 2 hours | 99% |
| **Tier 3** (analytical) | Trend analysis | 24 hours | 95% |

The cost of maintaining SLAs scales with strictness — 99.9% requires significantly more investment than 99%.

## Decision Rules

1. Define freshness and completeness SLAs before the first production deploy.
2. Use error budgets to make SLA conversations concrete — "99.5% compliance" is actionable; "data should be fresh" is not.
3. Start with Tier 1 SLAs for customer-facing data products. Expand as measurement matures.
4. Document SLAs with measurement queries, not prose descriptions.
5. Alert on SLO violation, not SLA breach. By the time the SLA is breached, the error budget is gone.
