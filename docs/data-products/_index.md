# Data Products & Sources

Sources and data products are distinct entities with independent lifecycles. Source evaluations live in `docs/sources/` and are reusable across data products. Data product specifications live in `docs/data-products/`. The scope document is the join point — it declares which sources a data product consumes.

## Directory Structure

```
docs/
  sources/                          # Independent source evaluations
    <source-name>/
      evaluation.md                 # From dos:evaluate-source
  data-products/                    # Data product specifications
    <product-name>/
      scope.md                      # From dos:scope-data-product (references sources)
      contract.md                   # From dos:define-contract (ODCS-aligned)
      quality-config.md             # From dos:assess-quality
      pipeline-architecture.md      # From dos:design-pipeline
      reviews/                      # From dos:review-pipeline (append-only)
        YYYY-MM-DD-review.md
```

**Relationships:**
- One source can feed multiple data products (e.g., `postgres-orders-db` feeds both "orders" and "customer-360")
- One data product can consume multiple sources (e.g., "orders" consumes `postgres-orders-db`, `stripe-api`, and `shipping-events`)
- A source evaluation can profile multiple datasets within a single source (e.g., multiple tables in a database)

## Artifact Frontmatter Schema

Every artifact includes YAML frontmatter with these required fields:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Source name or data product name (matches directory name) |
| `artifact_type` | enum | One of: `source-evaluation`, `scope`, `contract`, `quality-config`, `pipeline-architecture` |
| `version` | semver | Artifact version (see versioning rules below) |
| `owner` | string | Team or individual responsible |
| `status` | enum | One of: `draft`, `active`, `deprecated` |
| `last_modified` | date | ISO 8601 date of last substantive change |

Source evaluation example:

```yaml
---
name: postgres-orders-db
artifact_type: source-evaluation
version: 1.0.0
owner: analytics-engineering
status: active
last_modified: 2026-03-23
---
```

Data product scope example:

```yaml
---
name: orders
artifact_type: scope
version: 1.0.0
owner: analytics-engineering
status: active
last_modified: 2026-03-23
sources:
  - postgres-orders-db
  - stripe-api
---
```

## Versioning Rules

- **Contracts** follow semantic versioning: additive changes (new column) → minor bump, breaking changes (removed column, type change) → major bump with expand-contract pattern.
- **Quality configs, scope documents, source evaluations** use simple incrementing versions. Any substantive change bumps the minor version.
- **Pipeline architecture** documents are versioned but changes are typically documented in the changelog rather than requiring formal versioning.

Git is the concurrency mechanism. Skills update `last_modified` and `version` as part of their update flow. Merge conflicts surface as text conflicts resolved through normal git workflow.

## Changelog Convention

Every artifact ends with a changelog section tracking evolution:

```markdown
## Changelog

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-03-23 | 1.0.0 | Initial evaluation | @analyst |
```

## Artifact Types

| Type | Location | Produced By | Consumed By |
|------|----------|-------------|-------------|
| `source-evaluation` | `docs/sources/<source>/` | `dos:evaluate-source` | scope-data-product, implement-source, design-pipeline |
| `scope` | `docs/data-products/<name>/` | `dos:scope-data-product` | select-model, define-contract, assess-quality, design-pipeline, implement-models |
| `contract` | `docs/data-products/<name>/` | `dos:define-contract` | implement-models, assess-quality, review-pipeline |
| `quality-config` | `docs/data-products/<name>/` | `dos:assess-quality` | implement-models, review-pipeline |
| `pipeline-architecture` | `docs/data-products/<name>/` | `dos:design-pipeline` | implement-source, implement-models, review-pipeline |
