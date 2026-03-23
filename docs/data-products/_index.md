# Data Products

Data product artifacts live in `docs/data-products/<name>/`, one directory per data product. Skills create and update these artifacts as living specifications that evolve over time.

## Directory Structure

```
docs/data-products/
  <name>/
    source-evaluation.md      # From dos:evaluate-source
    scope.md                  # From dos:scope-data-product
    contract.md               # From dos:define-contract (ODCS-aligned)
    quality-config.md         # From dos:assess-quality
    pipeline-architecture.md  # From dos:design-pipeline
    reviews/                  # From dos:review-pipeline (append-only)
      YYYY-MM-DD-review.md
```

## Artifact Frontmatter Schema

Every artifact includes YAML frontmatter with these required fields:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Data product name (matches directory name) |
| `artifact_type` | enum | One of: `source-evaluation`, `scope`, `contract`, `quality-config`, `pipeline-architecture` |
| `version` | semver | Artifact version (see versioning rules below) |
| `owner` | string | Team or individual responsible |
| `status` | enum | One of: `draft`, `active`, `deprecated` |
| `last_modified` | date | ISO 8601 date of last substantive change |

Example:

```yaml
---
name: orders
artifact_type: source-evaluation
version: 1.0.0
owner: analytics-engineering
status: active
last_modified: 2026-03-23
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

| Type | Produced By | Consumed By |
|------|-------------|-------------|
| `source-evaluation` | `dos:evaluate-source` | scope-data-product, implement-source, design-pipeline |
| `scope` | `dos:scope-data-product` | select-model, define-contract, assess-quality, design-pipeline, implement-models |
| `contract` | `dos:define-contract` | implement-models, assess-quality, review-pipeline |
| `quality-config` | `dos:assess-quality` | implement-models, review-pipeline |
| `pipeline-architecture` | `dos:design-pipeline` | implement-source, implement-models, review-pipeline |
