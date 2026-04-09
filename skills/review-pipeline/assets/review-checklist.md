---
name: {{data_product}}
artifact_type: pipeline-review
version: 1.0.0
owner: {{owner}}
status: active
last_modified: {{date}}
review_date: {{date}}
data_product: {{data_product}}
---

# Pipeline Review: {{data_product}}

**Review date:** {{date}}
**Reviewer:** {{reviewer}}

## Pipeline Inventory

| Component | Tool / Service | Version | Notes |
|-----------|---------------|---------|-------|
| **Orchestrator** | {{e.g., Airflow, Dagster, Prefect, cron}} | {{version}} | {{deployment model}} |
| **Extraction** | {{e.g., dlt, Fivetran, custom}} | {{version}} | {{source count}} |
| **Transformation** | {{e.g., dbt, SQLMesh}} | {{version}} | {{model count}} |
| **Validation** | {{e.g., dbt tests, Soda, Great Expectations}} | {{version}} | {{test count}} |
| **Monitoring** | {{e.g., Datadog, Grafana, native}} | {{version}} | {{coverage}} |

## Observability Assessment

Assess the five baseline data observability metrics. Start with freshness and volume (highest signal-to-investment ratio).

| Metric | Implemented? | Tool / Method | Coverage | Notes |
|--------|:------------:|---------------|----------|-------|
| **Freshness** | {{yes / partial / no}} | {{e.g., dbt source freshness, Dagster policies}} | {{tables covered}} | {{thresholds set?}} |
| **Volume** | {{yes / partial / no}} | {{e.g., row count checks, dbt-expectations}} | {{tables covered}} | {{baseline established?}} |
| **Distribution** | {{yes / partial / no}} | {{e.g., statistical tests, anomaly detection}} | {{columns covered}} | {{method: rule-based / statistical / ML}} |
| **Schema** | {{yes / partial / no}} | {{e.g., contract enforcement, schema registry}} | {{models covered}} | {{drift detection?}} |
| **Lineage** | {{yes / partial / no}} | {{e.g., dbt docs, DataHub, manual}} | {{coverage}} | {{cross-system?}} |

**Observability vs monitoring distinction:** Observability infers data health from outputs. Monitoring watches execution metrics. Both are needed.

- Pipeline monitoring in place? {{yes / no — instrument orchestrator-native metrics first}}
- Data observability layered on top? {{yes / no — layer after monitoring is established}}

## Validation Assessment

Assess the three-tier validation strategy. Identify gaps.

| Tier | Environment | Expected Tools | Present? | Gap Description |
|------|------------|----------------|:--------:|-----------------|
| 1 | Local dev | Pandera + pytest, dbt unit tests | {{yes / partial / no}} | {{what's missing}} |
| 2 | CI pipeline | dbt data tests + dbt-expectations | {{yes / partial / no}} | {{what's missing}} |
| 3 | Production | Soda / Great Expectations, dbt source freshness | {{yes / partial / no}} | {{what's missing}} |

## CI/CD Assessment

Assess which CI/CD tiers exist.

| Tier | Present? | Implementation | Notes |
|------|:--------:|---------------|-------|
| **Pre-commit** | {{yes / no}} | {{e.g., SQLFluff, Ruff, dbt-checkpoint}} | {{hooks configured?}} |
| **PR validation (slim CI)** | {{yes / no}} | {{e.g., dbt build --select state:modified+}} | {{see blind spots below}} |
| **Production deployment** | {{yes / no}} | {{e.g., merge-triggered dbt build}} | {{manifest persisted?}} |

### Slim CI Blind Spots

| Blind Spot | Status | Mitigation |
|-----------|--------|------------|
| var()/env_var() changes not detected | {{exposed / mitigated / N/A}} | {{how mitigated, if at all}} |
| Incremental models run full-refresh in CI | {{exposed / mitigated / N/A}} | {{e.g., dbt clone to seed CI schema}} |
| State artifact (manifest.json) staleness | {{exposed / mitigated / N/A}} | {{manifest pipeline reliability}} |

## SLA Compliance Assessment

Assess enforcement across three layers.

| Layer | Assessment Question | Status | Evidence |
|-------|-------------------|--------|----------|
| **CI-time** | Are breaking changes detected via `state:modified+`? | {{yes / no}} | {{tool and config}} |
| **Build-time** | Are dbt contracts enforced (`contract: { enforced: true }`)? | {{yes / no}} | {{model count with contracts}} |
| **Build-time** | Are constraints actually enforced by production warehouse (not metadata-only)? | {{yes / no / partial}} | {{platform: DuckDB=full, Snowflake=metadata}} |
| **Runtime** | Are quality checks running in production? | {{yes / no}} | {{tool and frequency}} |
| **Runtime** | Is `dbt source freshness` wired separately from `dbt build`? | {{yes / no}} | {{if source YAML defines freshness thresholds but production job lacks `dbt source freshness`: **critical** — freshness SLI defined but never measured}} |

**SLA quantification:**
- Are SLAs defined with error budgets? {{yes — e.g., "99.5% compliance ≈ 3.6h/month violation" / no — aspirational only}}
- Freshness SLA compliance % tracked? {{yes / no}}
- Staleness ratio tracked? {{yes / no}}

## Retry & Failure Handling Assessment

| Criterion | Status | Details |
|-----------|--------|---------|
| Failure modes classified (terminal vs transient)? | {{yes / partial / no}} | {{list unclassified modes}} |
| Retry strategy uses exponential backoff with jitter? | {{yes / no — fixed-interval is an anti-pattern}} | {{implementation}} |
| Dead letter queue for exhausted retries? | {{yes / no}} | {{where records go}} |
| dlt retry configured (tenacity or equivalent)? | {{yes / no / N/A}} | {{dlt has no default retry}} |
| Alert fatigue mitigated (dedup, grouping, suppression)? | {{yes / partial / no}} | {{approach}} |

## Artifact-vs-Implementation Gaps

Compare what specification artifacts declare against what the pipeline actually does.

| Artifact | Specification | Implementation | Gap? | Severity |
|----------|--------------|----------------|:----:|----------|
| {{e.g., contract.md}} | {{e.g., column "status" is not_null}} | {{e.g., no not_null test on status}} | {{yes / no}} | {{critical / warning / info}} |

{{If no artifacts exist, note: "No specification artifacts available for comparison. Recommend running upstream skills to create them."}}

## Findings Summary

| # | Finding | Severity | Category | Recommendation |
|---|---------|----------|----------|----------------|
| 1 | {{finding description}} | {{critical / warning / info}} | {{observability / validation / ci-cd / sla / retry / gap}} | {{specific action}} |

## Recommendations

Prioritized by severity (critical first):

1. {{Most urgent recommendation with specific action}}
2. {{Next recommendation}}

## Next Steps

Based on the findings above, consider re-running these upstream skills:

- **`/dos:design-pipeline`** — if observability or architecture gaps were found
- **`/dos:define-contract`** — if contract-vs-implementation gaps were found or contracts are missing
- **`/dos:assess-quality`** — if validation tier gaps or quality dimension coverage issues were found
- **`/dos:implement-models`** — if dbt model structure, testing, or contract enforcement issues were found
- **`/dos:implement-source`** — if extraction, freshness wiring, or source configuration issues were found

Re-run `/dos:review-pipeline` after addressing findings to verify improvements.

## Changelog

| Date | Version | Change | Author |
|------|---------|--------|--------|
| {{date}} | 1.0.0 | Initial review | {{reviewer}} |
