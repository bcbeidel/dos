# Validation & CI/CD Audit

## Three-Tier Validation Strategy

| Tier | Environment | Expected Tools | What to Check |
|------|------------|----------------|---------------|
| 1 | Local dev | Pandera + pytest, dbt unit tests, SQLFluff/Ruff | Tests run in <60s? Python logic covered? SQL linting configured? |
| 2 | CI pipeline | dbt data tests + dbt-expectations (Metaplane fork) | `state:modified+` selector used? Data diffing enabled? <10 min execution? |
| 3 | Production | Soda / Great Expectations, dbt source freshness | Continuous monitoring? Anomaly detection? Source freshness as pre-build step? |

**Gap detection:** For each tier, check: (a) is it implemented? (b) what tool(s)? (c) what's missing compared to the expected coverage?

Small teams (1-3 engineers): collapsing tiers is acceptable. dbt tests in CI/production is the minimum viable setup.

## CI/CD Tier Assessment

| Tier | Purpose | Key Check |
|------|---------|-----------|
| **Pre-commit** | Catch obvious issues in seconds | SQLFluff, Ruff, dbt-checkpoint hooks configured? |
| **PR validation (slim CI)** | Validate modified models in minutes | `dbt build --select state:modified+` running? See blind spots below. |
| **Production deployment** | Deploy validated changes | Merge-triggered or scheduled `dbt build`? Manifest persisted? |

## Three Slim CI Blind Spots

These cause false confidence — CI passes but production breaks:

### 1. var()/env_var() Changes Not Detected

dbt cannot detect that a model should be rebuilt when a variable value changes. `state:modified+` only tracks file changes, not configuration changes. CI passes while production breaks on the new variable value.

**Mitigation:** Add integration tests for critical variable-dependent models. Document which models depend on runtime variables.

### 2. Incremental Models Run Full-Refresh in CI

In a clean CI schema, incremental models don't exist yet. `is_incremental` evaluates to false, so CI tests the full-refresh path — entirely different SQL from production.

**Mitigation:** Use `dbt clone` to seed the CI schema with production incremental tables before running tests.

### 3. State Artifact (manifest.json) Staleness

If the production manifest is stale or missing, `state:modified+` comparisons are wrong. The pipeline that persists the manifest is itself a failure mode.

**Mitigation:** Verify manifest freshness as part of CI setup. Alert if manifest is >24h old.
