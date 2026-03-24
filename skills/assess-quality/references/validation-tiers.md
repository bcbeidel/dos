# Validation Tiers

The data testing pyramid has three layers that map to three execution environments. Each layer catches different failure modes at different cost levels. No single tool covers all three tiers well -- that is a feature of the architecture, not a problem to solve.

## Data Testing Pyramid

**Base -- Schema and contract tests.** Fast, cheap, run on every execution. Validate column existence, data types, not-null constraints, primary key uniqueness. Structural failures cascade to every downstream consumer, so catching them first provides the highest ROI.

**Middle -- Data validation tests.** Check actual values: range bounds, referential integrity, freshness, volume anomaly detection (row count within +/-20% of previous run). More expensive but catches quality problems before downstream propagation.

**Top -- Regression and anomaly detection.** Compare current output against historical baselines: distribution drift, aggregate metric shifts, temporal trend breaks. Most resource-intensive but catches subtle degradation that rule-based tests miss.

## Three-Tier Execution Strategy

### Tier 1: Local Development (pre-commit / pre-push)
- Pandera schema validation on sample data loaded into DuckDB
- pytest test suite covering transformation functions, business logic, edge cases
- dbt unit tests (v1.8+) for SQL logic validation with mock data
- Execution time target: under 60 seconds

### Tier 2: CI Pipeline (pull request)
- dbt build with `--select state:modified+` against DuckDB or CI warehouse
- Full dbt data test suite (generic + singular + dbt-expectations via Metaplane fork)
- Pandera integration tests against larger sample datasets
- Execution time target: under 10 minutes

### Tier 3: Production (post-deployment)
- Soda scans with anomaly detection (requires Soda Cloud for alerting)
- Great Expectations checkpoints on critical assets with Data Docs
- dbt source freshness checks wired into orchestrator as pre-build step
- Volume and distribution monitoring with historical baselines

## Tool Selection by Tier

| Tier | Primary Tool | Secondary Tool | Rationale |
|------|-------------|---------------|-----------|
| Local dev | Pandera + pytest | dbt unit tests | Fast feedback, Python-native, no warehouse needed |
| CI | dbt data tests | dbt-expectations | Integrated with DAG, catches transformation issues |
| Production | Soda / Great Expectations | dbt source freshness | Continuous monitoring, anomaly detection |

## Scaling Down for Small Teams

Teams of 1-3 data engineers cannot maintain three validation toolchains. The pragmatic path:

1. **Start with dbt tests in CI and production.** Already in the stack, covers the middle tier.
2. **Add Pandera only for Python-heavy pipelines** (dlt extractors, custom transformations, ML features).
3. **Defer Soda/GE** until dedicated platform engineering capacity exists. dbt source freshness + store_failures provides basic production monitoring.

The three-tier strategy is a target architecture, not a minimum viable setup. Collapsing tiers is preferable to maintaining toolchains the team cannot invest in.

## Decision Rules

1. Catch structural issues locally in seconds, value issues in CI in minutes, drift in production continuously.
2. Start with dbt tests -- they are already in the stack.
3. Add Pandera for Python-centric pipelines; defer Soda/GE until capacity exists.
4. Use the Metaplane fork of dbt-expectations (calogica package is unmaintained since December 2024).
5. Do not over-invest in one tier while ignoring others.
