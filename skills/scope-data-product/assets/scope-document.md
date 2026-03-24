---
name: {{name}}
artifact_type: scope
version: 1.0.0
owner: {{owner}}
status: draft
last_modified: {{date}}
sources:
  - {{source-name}}
---

# Data Product Scope: {{name}}

## Consumers and Use Cases

| Consumer | Role | Primary Use Case | Decision Enabled |
|----------|------|-----------------|-----------------|
| {{consumer}} | {{role}} | {{what they do with the data}} | {{what decision changes with this data}} |

### Query Patterns

| Consumer | Dominant Pattern | Description |
|----------|-----------------|-------------|
| {{consumer}} | {{join-heavy / scan-heavy / entity-lookup / ad-hoc}} | {{typical queries and access patterns}} |

**Empirical evidence:** {{dashboards reviewed, SQL queries analyzed, query log findings (BigQuery INFORMATION_SCHEMA.JOBS, Snowflake QUERY_HISTORY)}}

## Source Inventory

Sources evaluated via `/dos:evaluate-source`. Each source may contribute multiple datasets.

| Source | Classification | Datasets | Ingestion Approach | Evaluation |
|--------|---------------|----------|-------------------|------------|
| {{source-name}} | {{transactional DB / event stream / SaaS API / file-based}} | {{dataset list}} | {{full / incremental / CDC}} | [evaluation](../../sources/{{source-name}}/evaluation.md) |

## Freshness Requirements

Quantify in specific time units — not adjectives. Ask: "What business decision changes if the data is 5 minutes old instead of 5 seconds old?"

| Dataset | Required Freshness | Justification | Ingestion Strategy |
|---------|-------------------|---------------|-------------------|
| {{dataset}} | {{e.g., 2 hours, 15 minutes, daily}} | {{business reason}} | {{batch / micro-batch / streaming}} |

## SLA Tier and Dimensions

**SLA Tier:** {{prototype / production-grade}}

**Rationale:** {{why this tier — consumer dependency, business criticality}}

### SLA Dimensions

Define the indicator (SLI) first, set the objective (SLO), then negotiate the agreement (SLA).

| Dimension | SLI (What to Measure) | SLO (Target) | SLA (Commitment) | Error Budget |
|-----------|----------------------|--------------|-------------------|-------------|
| Timeliness | {{e.g., max age of latest record}} | {{e.g., 99.5% within 2h}} | {{e.g., 99% within 4h}} | {{e.g., ~7.2h/month}} |
| Completeness | {{e.g., row count vs expected}} | {{e.g., 99.9% of expected rows}} | {{e.g., 99% of expected rows}} | {{e.g., ~7.2h/month}} |
| {{additional}} | {{measure}} | {{target}} | {{commitment}} | {{budget}} |

## Quality Dimensions

Initial dimensions and thresholds derived from profiling baselines and consumption tolerances. Refined by `/dos:assess-quality`.

| Dimension | Threshold | Baseline (from profiling) | Rationale |
|-----------|-----------|--------------------------|-----------|
| Completeness | {{e.g., > 99% non-null on required fields}} | {{profiling baseline}} | {{consumer tolerance}} |
| Uniqueness | {{e.g., 100% on primary keys}} | {{profiling baseline}} | {{deduplication requirement}} |
| Validity | {{e.g., > 98% in expected ranges}} | {{profiling baseline}} | {{business rule}} |
| Timeliness | {{e.g., < 2h staleness}} | {{N/A}} | {{freshness requirement}} |
| {{additional}} | {{threshold}} | {{baseline}} | {{rationale}} |

## Modeling Recommendation

_Populated by `/dos:select-model`. Placeholder until modeling decision is made._

**Recommended approach:** {{Kimball star schema / Data Vault / OBT / TBD}}

**Rationale:** {{based on query patterns, team size, platform, compliance needs}}

**Platform considerations:** {{platform-specific guidance}}

## MoSCoW Prioritization

### Must Have

- {{requirements without which the data product has no value}}

### Should Have

- {{important requirements deliverable iteratively}}

### Could Have

- {{nice-to-haves deprioritized under pressure}}

### Won't Have in v1

Explicitly descoped. These are NOT implicit commitments for future delivery — they are conscious decisions about what this version does not include.

- {{explicitly descoped items with rationale}}

## Next Steps

Based on this scope document, the recommended next skills are:

1. **`/dos:select-model`** — Choose a data modeling approach (Kimball, Data Vault, OBT) based on query patterns, team size, and platform. Updates the Modeling Recommendation section above.
2. **`/dos:define-contract`** — Define a data contract covering schema, quality rules, SLAs, and ownership. Consumes consumers, SLAs, and quality dimensions from this scope.
3. **`/dos:assess-quality`** — Set up quality engineering with dimensions, thresholds, scoring, and validation tooling. Consumes quality dimensions and SLA targets from this scope.
4. **`/dos:design-pipeline`** — Architecture the data pipeline from source to serving layer. Consumes source inventory, freshness requirements, and SLA tier from this scope.

## Changelog

| Date | Version | Change | Author |
|------|---------|--------|--------|
| {{date}} | 1.0.0 | Initial scope | {{author}} |
