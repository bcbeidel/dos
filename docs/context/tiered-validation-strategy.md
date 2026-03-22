---
name: Tiered Validation Strategy
description: "Three-tier data validation strategy mapping the data testing pyramid to execution environments -- local dev (Pandera + pytest), CI (dbt tests), production (Soda/GE monitoring); no single tool covers all tiers; teams under 5 engineers should collapse tiers"
type: context
related:
  - docs/research/2026-03-22-validation-frameworks.research.md
  - docs/context/data-validation-tool-comparison.md
  - docs/context/ci-cd-pipeline-design.md
  - docs/context/data-observability-pillars.md
  - docs/context/data-freshness-slas.md
---

## Key Insight

The data testing pyramid has three layers (schema/contract, value validation, regression/anomaly) that map to three execution environments (local dev, CI, production). Each layer catches different failure modes at different cost levels. No single tool covers all three tiers well -- that is a feature of the architecture, not a problem to solve. Teams under 5 engineers should collapse tiers rather than maintain three separate toolchains.

## The Data Testing Pyramid

**Base: Schema and contract tests.** Fast, cheap, run on every pipeline execution. Validate column existence, data types, not-null constraints, primary key uniqueness. Structural failures cascade to every downstream consumer, so catching them first provides the highest ROI.

**Middle: Data validation tests.** Check actual values -- range bounds, referential integrity, freshness, volume anomaly detection (row count within +/-20% of previous run). More expensive but catches quality problems before downstream propagation.

**Top: Regression and anomaly detection.** Compare current output against historical baselines -- distribution drift, aggregate metric shifts, temporal trend breaks. Most resource-intensive but catches subtle degradation that rule-based tests miss.

## Three-Tier Execution Strategy

### Tier 1: Local Development (pre-commit / pre-push)

- Pandera schema validation on sample data loaded into DuckDB
- pytest test suite covering transformation functions, business logic, edge cases
- dbt unit tests (v1.8+) for SQL logic validation with mock data
- SQLFluff / Ruff for code quality
- Execution time target: under 60 seconds

### Tier 2: CI Pipeline (pull request)

- dbt build with `--select state:modified+` against DuckDB or a CI warehouse
- Full dbt data test suite (generic + singular + dbt-expectations via Metaplane fork)
- Pandera integration tests against larger sample datasets
- Data diffing between PR branch and production (Datafold or equivalent)
- Execution time target: under 10 minutes

### Tier 3: Production (post-deployment)

- Soda scans on production data sources with anomaly detection (requires Soda Cloud)
- Great Expectations checkpoints on critical data assets with Data Docs
- dbt source freshness checks wired into orchestrator as pre-build step
- Volume and distribution monitoring with historical baselines
- Data quality agreements enforcing SLAs with stakeholder-approved thresholds

## Tool Selection by Tier

| Tier | Primary Tool | Secondary Tool | Rationale |
|---|---|---|---|
| Local dev | Pandera + pytest | dbt unit tests | Fast feedback, Python-native, no warehouse needed |
| CI | dbt data tests | dbt-expectations | Integrated with DAG, catches transformation issues |
| Production | Soda / Great Expectations | dbt source freshness | Continuous monitoring, anomaly detection, Data Docs |

## Scaling Down for Small Teams

The three-tier strategy assumes capacity for three validation toolchains. For teams of 1-3 data engineers, this is unrealistic. The pragmatic path:

1. **Start with dbt tests in CI and production.** They are already in the stack and cover the middle tier of the pyramid.
2. **Add Pandera only for Python-heavy pipelines** (dlt extractors, custom transformations, ML feature engineering).
3. **Defer Soda/Great Expectations** until dedicated platform engineering capacity exists. dbt source freshness + store_failures provides basic production monitoring.

The three-tier strategy is a target architecture, not a minimum viable setup. Collapsing tiers is preferable to maintaining toolchains the team cannot invest in.

## Takeaway

Defense in depth means catching different failure types at the cheapest appropriate layer. Structural issues should fail in seconds locally, value issues in minutes during CI, and drift/anomaly issues continuously in production. The critical mistake is over-investing in one tier while ignoring others -- a team with 500 dbt tests but no local validation still ships broken code to CI on every push.
