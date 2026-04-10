---
name: scope-data-product
description: Populate a data-product.md living document section by section — Overview, Sources, Contract, Quality, Architecture — and maintain its Changelog. Collapses define-contract, assess-quality, design-pipeline, select-model, and the original scope-data-product into one skill.
---

# dos:scope-data-product

Populate and maintain the `data-product.md` living document. Works section by section through Overview, Sources, Contract, Quality, and Architecture. Handles both first-time scaffolding and targeted re-runs when sections need updating.

## Preamble

**Step 1: Identify the data product.**
Ask the user for the data product name (e.g., `orders`, `customer-360`). The artifact path is `docs/data-products/<name>/data-product.md`.

**Step 2: Determine mode.**

- **New mode** — file does not exist:
  - Create `docs/data-products/<name>/` directory.
  - Copy `skills/scope-data-product/assets/data-product.md` to the path.
  - Substitute `{{name}}` → the data product name and `{{last_modified}}` → today's date in frontmatter.
  - Confirm scaffold with user. All sections start as pending markers.

- **Re-run mode** — file exists:
  - Read the file. Build a prioritized agenda:
    1. Sections that still contain a `<!-- pending:` marker.
    2. Sections named in recent Changelog "potentially affected" lines.
  - Present the agenda to the user. Confirm which sections to work through.
  - The user can add sections or stop at any point.

---

## Workflow

### Step 1: Overview

References: [interview-questions.md](references/interview-questions.md), [consumption-heuristics.md](references/consumption-heuristics.md), [sla-hierarchy.md](references/sla-hierarchy.md)

Produce:
- **Consumer table** — consumer, role, use case, decision enabled. Load `docs/sources/` scorecards if available.
- **Query patterns** — for each consumer, classify using [consumption-heuristics.md](references/consumption-heuristics.md): join-heavy, scan-heavy, entity lookup, or ad-hoc.
- **SLA commitments in plain language** — timeliness with a specific delivery window, completeness, availability. Use [sla-hierarchy.md](references/sla-hierarchy.md) for SLI/SLO/SLA hierarchy and error budget framing. "Monthly" is not an SLA; "by the 15th of each month" is.
- **MoSCoW prioritization** — if consumers have competing requirements, apply Must/Should/Could/Won't. Refer to [interview-questions.md](references/interview-questions.md) for the canvas framework.

Write the section. Immediately after the `## Overview` heading, insert:
```
<!-- last-updated: <date> | skill: scope-data-product | version: <version> -->
```

**Consistency check:** If SLA commitments changed, flag Contract as potentially affected.

---

### Step 2: Sources

Produce:
- **Source inventory table** — source name, classification, datasets, ingestion approach, incremental key, freshness requirement. Pull from `docs/sources/<name>/` scorecards where available.
- **Cross-pipeline dependencies** — list upstream data products this product depends on, with relative links.
- **Infrastructure references** — use `tool::component.identifier` shorthand (e.g., `dbx::pipeline.ingest-orders`, `airbyte::connection.salesforce-crm`).

Write the section with metadata comment.

**Consistency check:** If sources changed, flag Architecture as potentially affected.

---

### Step 3: Contract

References: [odcs-structure.md](references/odcs-structure.md), [enforcement-layers.md](references/enforcement-layers.md), [versioning-patterns.md](references/versioning-patterns.md)

Produce:
- **Schema table** — field, type, nullable, description, constraints. Use [odcs-structure.md](references/odcs-structure.md) for ODCS field structure.
- **SLA terms** — freshness, completeness, availability as measurable thresholds (not adjectives). Must match the plain-language commitments in Overview.
- **Consumer commitments** — what downstream consumers can rely on, including backward-compatibility window.
- **Enforcement notes** — which enforcement layers apply per [enforcement-layers.md](references/enforcement-layers.md). Version bump rules per [versioning-patterns.md](references/versioning-patterns.md).

Write the section with metadata comment.

**Consistency check:** If schema changed or new fields added, flag Quality as potentially affected.

---

### Step 4: Quality

References: [quality-dimensions.md](references/quality-dimensions.md), [dbt-test-selection.md](references/dbt-test-selection.md), [anomaly-methods.md](references/anomaly-methods.md), [scoring-methods.md](references/scoring-methods.md), [sla-error-budgets.md](references/sla-error-budgets.md), [validation-tiers.md](references/validation-tiers.md), [quality-dimension-selection.md](references/quality-dimension-selection.md)

Produce:
- **Quality dimensions table** — dimension, measurement method, rule type, threshold, dbt test, owner. Select dimensions using [quality-dimension-selection.md](references/quality-dimension-selection.md); refer to [quality-dimensions.md](references/quality-dimensions.md) for the six-dimension consensus.
- **Test mapping** — use [dbt-test-selection.md](references/dbt-test-selection.md) to map each rule type to a specific dbt test.
- **Anomaly detection** — for high-stakes dimensions, apply [anomaly-methods.md](references/anomaly-methods.md) to select detection approach.
- **Scoring weights** — use [scoring-methods.md](references/scoring-methods.md) to weight dimensions by consumer dependency.
- **Alert thresholds** — use [sla-error-budgets.md](references/sla-error-budgets.md) to derive alert triggers from SLA error budgets.
- **Validation tiers** — assign each rule to a tier per [validation-tiers.md](references/validation-tiers.md): blocking, warning, informational.

Write the section with metadata comment.

---

### Step 5: Architecture

References: [layering-strategy.md](references/layering-strategy.md), [consumption-to-architecture.md](references/consumption-to-architecture.md), [incremental-patterns.md](references/incremental-patterns.md), [schema-evolution-patterns.md](references/schema-evolution-patterns.md), [model-decision-matrix.md](references/model-decision-matrix.md), [platform-modeling-guidance.md](references/platform-modeling-guidance.md)

Produce:
- **Model selection rationale** — Kimball, Data Vault, or OBT. Use [model-decision-matrix.md](references/model-decision-matrix.md) and query patterns from Overview. Apply [platform-modeling-guidance.md](references/platform-modeling-guidance.md) for platform-specific constraints.
- **Layer description** — staging, intermediate, marts layout per [layering-strategy.md](references/layering-strategy.md). Consumption-to-layer mapping per [consumption-to-architecture.md](references/consumption-to-architecture.md).
- **Model inventory table** — model name, layer, materialization, description.
- **Incremental patterns** — select strategy (append, delete+insert, merge, microbatch) per [incremental-patterns.md](references/incremental-patterns.md).
- **Schema evolution** — note ADD COLUMN / DROP COLUMN / TYPE CHANGE handling per [schema-evolution-patterns.md](references/schema-evolution-patterns.md).
- **Compute and scheduling declarations** — use `tool::component.identifier` shorthand (e.g., `dbx::job.transform-orders`, `dbx::pipeline.dlt-orders`). Include schedule, cluster config, task dependencies.
- **Cross-pipeline dependency ordering** — list upstream data products and their expected completion time relative to this product's SLA.

Write the section with metadata comment.

---

### After each completed section

Present the cross-section consistency table entries relevant to the section just completed. Ask: "Do you want to continue to the affected sections now, or note them for a future run?" Record the decision in the Changelog entry regardless.

---

### Step 6: Version and Changelog

Determine version bump:
- **MAJOR** — breaking contract change: field removal, type change, SLA tightening. Confirm with user before proceeding.
- **MINOR** — backward-compatible: new column, threshold recalibration, architecture refactor, new source.
- **PATCH** — docs, metadata, or comment-only changes.

Update `version` and `last_modified` in frontmatter.

Append a Changelog entry in this format:

```markdown
### v<version> — <date>

| Field | Value |
|-------|-------|
| version | <version> |
| date | <date> |
| skill | scope-data-product |
| sections updated | <comma-separated list> |
| change | <one-line summary> |
| reason | <why this changed> |
| potentially affected | <downstream sections or skills> |
```

---

## Cross-Section Consistency Rules

| Section updated | Potentially affects | Reason |
|---|---|---|
| Architecture | Quality | Tests reference layer structure |
| Architecture | Contract | Enrichment moves may change output schema |
| Contract | Quality | New or removed fields need quality rules |
| Sources | Architecture | New or removed sources may not be reflected in the layer model |
| Overview (SLAs) | Contract | Plain-language SLA changes may not match Contract thresholds |
