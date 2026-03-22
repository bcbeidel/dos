---
name: CI/CD Pipeline Design
description: Three-tier validation pipeline (pre-commit, PR validation, production deployment) for dbt+dlt projects, including slim CI mechanics, manifest management, and known blind spots
type: context
related:
  - docs/research/2026-03-22-development-workflow.research.md
  - docs/context/local-duckdb-development.md
  - docs/context/pre-commit-dbt-hooks.md
  - docs/context/pipeline-orchestration-comparison.md
  - docs/context/data-lineage-implementation.md
---

## Key Insight

The emerging best practice is three-tier validation: pre-commit hooks catch issues in seconds, PR CI validates modified models with slim builds in minutes, and production deployment runs merge-triggered or scheduled full builds. Each tier has a distinct purpose and different tradeoffs. Skipping a tier creates a gap that the other tiers cannot fill.

## Tier 1: Pre-commit (Local, Seconds)

Runs on every commit via the pre-commit framework. Goal: catch obvious issues before code reaches CI.

- **Ruff** for Python linting/formatting (dlt pipelines, macros)
- **SQLFluff** for SQL linting — use Jinja templater locally (fast), dbt templater in CI only (accurate but 10x slower)
- **dbt-checkpoint** (successor to pre-commit-dbt) for model governance: tests exist, properties documented, naming conventions followed

Performance caveat: SQLFluff with dbt templater is ~20s per file vs ~2s with Jinja templater. Parallelism (`--processes > 1`) is broken with dbt templater — causes hangs and crashes. Use `--processes 1` or switch to Jinja templater for pre-commit.

## Tier 2: PR Validation (CI, Minutes)

Runs on PR creation and push. Goal: validate modified models build correctly.

1. `dbt parse` — syntax validation
2. `dbt clone` — seed CI schema with production incrementals (prevents false full-refresh path)
3. `dbt build --select state:modified+ --defer --state ./` — slim CI, only modified models and downstream
4. `dbt run --empty` — schema-only validation without warehouse compute (dbt 1.8+)
5. SQLFluff lint with dbt templater — full accuracy

Operational patterns:
- Exclude draft PRs: `if: ${{ !github.event.pull_request.draft }}`
- Dynamic PR schemas: `PR_NUM_<pr_number>` for isolation
- Concurrency control to avoid redundant runs

**Manifest artifact management** (dbt Core only): persist `manifest.json` to S3/GCS after production runs, fetch at CI start for state comparison. This adds infrastructure and a failure mode (stale/missing manifest).

```yaml
# Upload after production run
- run: aws s3 cp target/manifest.json s3://bucket/manifest.json
# Download at CI start
- run: aws s3 cp s3://bucket/manifest.json ./manifest.json
```

## Tier 3: Production Deployment (Merge-triggered or Scheduled)

Runs on merge to main or on schedule. Goal: deploy validated changes to production.

- Full `dbt build` or source-freshness-aware selective build: `dbt run --select source_status:fresher+ --state ./ --exclude config.materialized:view tag:static`
- Persist manifest artifact for future state comparisons
- Clean up old PR schemas

## Slim CI Blind Spots

These are documented limitations that cause false confidence:

**False negatives for var()/env_var() changes.** dbt cannot detect that a model should be rebuilt when a variable value changes. CI passes while production breaks.

**Incremental models run full-refresh in CI.** In a clean PR schema, incremental models don't exist yet. `is_incremental` evaluates to false, so CI tests the full-refresh path — entirely different SQL from the production incremental path. Fix: use `dbt clone` to seed the CI schema first.

**State artifact staleness.** If the production manifest is stale or missing, state:modified+ comparisons are wrong. The pipeline that persists the manifest is itself a failure mode.

## Takeaway

The three tiers form a funnel: fast-and-loose locally, accurate-and-thorough in CI, reliable-and-complete in production. The biggest operational risk is not missing a tier — it is trusting slim CI results without understanding its blind spots around incremental models and variable changes.
