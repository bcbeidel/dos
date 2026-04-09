# SLA Compliance Checklist

## Three-Layer Enforcement Assessment

| Layer | Assessment Question | What to Look For |
|-------|-------------------|-----------------|
| **CI-time** | Are breaking changes detected before deploy? | `dbt build --select state:modified+` with contract enforcement |
| **Build-time** | Are dbt contracts enforced? | `contract: { enforced: true }` on mart models |
| **Build-time** | Are constraints *actually* enforced by the production warehouse? | DuckDB = full enforcement; Snowflake/Databricks = metadata-only for most constraints |
| **Runtime** | Are quality checks running in production? | dbt tests, Soda, or Great Expectations post-deployment |
| **Runtime** | Is `dbt source freshness` wired separately from `dbt build`? | If no: **there is no freshness monitoring** |

**False confidence warning:** A contract that passes locally on DuckDB can silently allow invalid data on Snowflake or Databricks. For every constraint the production warehouse does not enforce, verify that an explicit dbt test exists.

## SLA Quantification Criteria

| Criterion | Quantified (good) | Aspirational (gap) |
|-----------|-------------------|-------------------|
| Freshness | "99.5% compliance ≈ 3.6h/month violation allowed" | "Data should be fresh" |
| Completeness | "99% of expected rows within 2 hours" | "All data should arrive" |
| Error budget | "Budget < 25% → freeze features, focus on reliability" | No error budget defined |
| Monitoring frequency | "Check every 30 min for 1-hour SLA" | "We check periodically" |

**Assessment:** Are SLAs defined with error budgets, or are they aspirational? Aspirational SLAs provide no enforcement or prioritization signal.

## SLA Tiers

| Tier | Example | Typical Freshness | Typical Completeness |
|------|---------|-------------------|---------------------|
| Tier 1 (customer-facing) | Payment transactions | 15 min | 99.9% |
| Tier 2 (operational) | Daily sales reporting | 2 hours | 99% |
| Tier 3 (analytical) | Trend analysis | 24 hours | 95% |

Not all data deserves an SLA. Over-SLA-ing creates the same noise as over-alerting. Start with Tier 1.

## Freshness Wiring Detection

`dbt source freshness` is a separate command — `dbt build` and `dbt test` do not run it.

| Condition | Severity | Finding |
|-----------|----------|---------|
| Source YAML defines `freshness` AND production job includes `dbt source freshness` | Pass | Freshness monitoring is wired |
| Source YAML defines `freshness` BUT production job does NOT include `dbt source freshness` | **Critical** | Freshness SLI is defined but never measured in production |
| Source YAML does not define `freshness` | Info | No freshness thresholds configured — consider adding if timeliness SLA exists |

When critical: the fix is `dbt source freshness --select source:<source_name>` added as a task in the production job, typically before `dbt build`.

## Key Checks

1. Are SLAs defined with measurement queries (not prose)?
2. Alert on SLO violation, not SLA breach (by breach time, error budget is consumed).
3. Track freshness SLA compliance % and staleness ratio as operational KPIs.
4. Monitoring frequency matches SLA granularity.
