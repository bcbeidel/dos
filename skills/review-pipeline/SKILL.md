---
name: review-pipeline
description: Audit an existing data pipeline against best practices across observability, validation, CI/CD, SLA compliance, and retry handling. Produces an append-only review checklist with findings, severity ratings, and prioritized recommendations.
---

# dos:review-pipeline

Audit an existing data pipeline against best practices. Walk through pipeline inventory, five assessment dimensions (observability, validation, CI/CD, SLAs, retry/failure handling), and artifact-vs-implementation gap detection — producing a persistent review checklist with prioritized findings and recommendations.

## Preamble

Before starting, establish context:

1. **Which data product?** Ask the user for the data product name (e.g., `orders`, `customer-360`). This determines the artifact path: `docs/data-products/<name>/`.

2. **Check for existing artifacts.** Look for specification artifacts that enrich the review:
   - `docs/data-products/<name>/scope.md`
   - `docs/data-products/<name>/contract.md`
   - `docs/data-products/<name>/quality-config.md`
   - `docs/data-products/<name>/pipeline-architecture.md`

   For each, report as "available" or "not found." If artifacts exist, load them — they provide context for gap detection in Step 6. If no artifacts exist, proceed by auditing the pipeline directly. This skill works without any upstream artifacts.

3. **Check for existing reviews.** Look for prior reviews in `docs/data-products/<name>/reviews/`. If previous reviews exist, summarize them and ask what's changed since the last review.

4. **Gather pipeline context.** If artifacts don't fully describe the pipeline, ask the user about their setup: orchestrator, transformation tool (dbt version), extraction tool (dlt or other), validation tools, monitoring infrastructure.

## Workflow

### Step 1: Pipeline Inventory

Document the current pipeline stack. Ask about or detect:

- Orchestrator (Airflow, Dagster, Prefect, cron, or none)
- Extraction tool (dlt, Fivetran, custom scripts)
- Transformation tool (dbt, SQLMesh) and version
- Validation tools (dbt tests, Soda, Great Expectations, Pandera)
- Monitoring tools (Datadog, Grafana, orchestrator-native, Monte Carlo)

If pipeline architecture artifact exists, cross-reference against it.

If no pipeline code is found in the project (no dbt models, no dlt pipelines), note this and adjust the review scope to assess the specification artifacts and readiness for implementation rather than auditing running code. Suggest `/dos:implement-source` and `/dos:implement-models` as next steps.

### Step 2: Observability Assessment

Assess whether the five baseline data observability metrics are covered. Refer to [observability-pillars.md](references/observability-pillars.md) for assessment criteria per metric and the observability-vs-monitoring distinction.

For each metric (freshness, volume, distribution, schema, lineage), determine:
- Is it implemented?
- What tool or method is used?
- What is the coverage (which tables/columns)?

Distinguish observability (infer data health from outputs) from monitoring (watch execution metrics). Both are needed. Instrument pipeline monitoring first (orchestrator-native), then layer data observability on top.

Start assessment with freshness and volume — highest signal-to-investment ratio.

### Step 3: Validation Assessment

Assess whether the three-tier validation strategy is in place. Refer to [validation-audit.md](references/validation-audit.md) for gap detection criteria at each tier.

For each tier (local dev, CI pipeline, production):
- Is it implemented?
- What tools are used?
- What's missing compared to expected coverage?

Small teams: collapsing tiers is acceptable. Note which tiers are collapsed and whether the coverage is adequate.

### Step 4: CI/CD Assessment

Assess which CI/CD tiers exist (pre-commit, PR validation, production deployment). Refer to [validation-audit.md](references/validation-audit.md) for CI/CD tier assessment and the three slim CI blind spots.

Flag each blind spot explicitly:
1. **var()/env_var() changes** — not detected by `state:modified+`. CI passes, production breaks.
2. **Incremental full-refresh in CI** — clean schema means `is_incremental` is false. Different SQL path from production.
3. **Manifest staleness** — stale or missing manifest makes `state:modified+` comparisons wrong.

For each, assess: exposed, mitigated, or N/A.

### Step 5: SLA Compliance Assessment

Assess enforcement across three layers. Refer to [sla-checklist.md](references/sla-checklist.md) for the enforcement assessment checklist and SLA quantification criteria.

Key questions:
- **CI-time:** Are breaking changes detected via state comparison?
- **Build-time:** Are dbt contracts enforced? Are constraints actually enforced by the production warehouse (not just metadata)?
- **Runtime:** Are quality checks and freshness monitoring in place?
- Are SLAs quantified with error budgets, or aspirational?
- Is `dbt source freshness` wired separately from `dbt build`? If not, there is no freshness monitoring.

### Step 6: Retry & Failure Handling Assessment

Assess retry strategy and failure handling. Refer to [retry-patterns.md](references/retry-patterns.md) for failure classification criteria and retry strategy assessment.

Key questions:
- Has every known failure mode been classified as terminal or transient?
- Does the retry strategy use exponential backoff with jitter (not fixed-interval)?
- Is there a dead letter queue for records that exhaust retries?
- **dlt-specific:** Is tenacity or equivalent retry configured? dlt has no default retry.

### Step 7: Artifact-vs-Implementation Gap Detection

If specification artifacts exist (contract, quality config, pipeline architecture), compare what they specify against what the pipeline actually does. Flag discrepancies:

- Contract specifies a column but the dbt model doesn't include it
- Quality config defines a threshold but no corresponding test exists
- Pipeline architecture specifies incremental loading but the model uses full refresh
- Contract enforcement enabled in spec but not in model config

If no artifacts exist, note: "No specification artifacts available for comparison. Consider running upstream skills to create them."

### Step 8: Generate Review Checklist

Produce the review checklist using the template from [review-checklist.md](assets/review-checklist.md).

Save to `docs/data-products/<name>/reviews/<date>-review.md` where `<date>` is today's date in YYYY-MM-DD format. Reviews are append-only — never overwrite existing reviews.

Populate:
- All assessment sections from the workflow above
- Findings summary table with severity (critical / warning / info) and category
- Recommendations prioritized by severity (critical first)
- Changelog with single entry recording the review

### Step 9: Next Steps

End the review with recommendations for addressing findings. As the terminal skill in the chain, next steps loop back to upstream skills based on what was found:

- **Observability or architecture gaps** → `/dos:design-pipeline`
- **Contract-vs-implementation gaps or missing contracts** → `/dos:define-contract`
- **Validation tier gaps or quality dimension issues** → `/dos:assess-quality`
- **dbt model structure, testing, or contract enforcement issues** → `/dos:implement-models`
- **Extraction, freshness wiring, or source configuration issues** → `/dos:implement-source`

Suggest re-running `/dos:review-pipeline` after addressing findings to verify improvements.
