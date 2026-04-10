---
name: Pipeline Document Consolidation
description: Replace 6 per-pipeline DOS artifacts with a single data-product.md and collapse 9 skills into 4 (scope-source, scope-data-product, implement-source, implement-data-product)
type: design
status: draft
related:
  - docs/research/2026-04-10-pipeline-artifact-consolidation.research.md
  - docs/research/2026-04-10-tool-infrastructure-declaration.research.md
---

# Pipeline Document Consolidation

## Problem

The DOS skill chain produces 6 artifact files per pipeline plus a plan — 7 files total. This creates four compounding problems:

**Drift.** Artifacts fall out of sync after implementation changes. The noaa_stations incident: `pipeline-architecture.md` was updated to v1.1.0 after enrichment moved from Python to dbt; `contract.md` and `quality-config.md` were not updated. They now describe a pipeline that no longer exists. Nothing in the structure made this visible.

**Sprawl.** 7 files per pipeline with no single entry point. An engineer wanting to understand a pipeline must open multiple files to piece together the full picture.

**Usability during active development.** Writing and updating a pipeline requires context-switching across multiple files in a single session. Skills produce artifacts sequentially; the result is a growing pile of loosely-related documents.

**Overhead exceeds value.** Artifacts are produced by skills but rarely consulted after initial creation. The pipeline review artifact had become the de facto source of truth not because it was designed that way, but because it was the only file that captured what had changed. Maintaining 7 documents costs more than their separation is worth.

## Design Decision

**Replace the 6 per-pipeline artifacts with a single `data-product.md` per data product, and collapse 9 skills into 4.**

The pipeline is a means to an end — SLAs, quality thresholds, architecture, and contract are all expressions of what the data product *is* and what it commits to. The document is named `data-product.md`, not `pipeline.md`, because the pipeline is implementation detail; the data product is the deliverable.

`data-product.md` is a maintained document — a living specification updated in place as the data product evolves. Git history provides point-in-time records. A structured Changelog section captures what changed, why, and which sections may be affected.

### Why not supersession (ADR pattern)?

The ADR research supports immutability for discrete decision records. But a data product specification is not an individual decision — it is the full specification of a system that evolves continuously. Supersession would produce one new file per change, recreating the sprawl problem. A maintained document with a changelog achieves the same traceability without file proliferation.

### Why not the journal/append-only approach (issue #23's original proposal)?

Append-only documents cannot reflect current state. The Contract section must describe the current schema, not a history of schema changes. The Changelog captures the history; the sections capture the present.

### Why not keep contract and quality as separate files?

`contract.md` and `quality-config.yaml` are DOS design documents, not machine-executed configs. The dbt enforcement layer lives in the project's `schema.yml` and test files — not in DOS artifacts. There is no technical constraint requiring them to remain discrete. The usability and overhead arguments apply equally to all 6 artifacts.

### Why not keep review-pipeline as a standalone skill?

Review was functioning as verification, not documentation. A checklist run after a change is a quality gate on the skill's own work — it belongs inside the skill that made the change, not as a separate artifact-producing step.

## Revised Skill Chain

This design collapses 9 skills into 4, organized around two prefixes: **scope** (decisions and specifications) and **implement** (code generation).

```
scope-source → scope-data-product → implement-source → implement-data-product
```

| Skill | Phase | Owns | Replaces |
|---|---|---|---|
| `scope-source` | Discover | `docs/sources/<name>/` scorecard | `evaluate-source` |
| `scope-data-product` | Scope | All sections of `data-product.md` | `scope-data-product` + `define-contract` + `assess-quality` + `design-pipeline` + `select-model` |
| `implement-source` | Build | dlt extraction code | `implement-source` (unchanged in purpose) |
| `implement-data-product` | Build | dbt models + schema.yml + tests + orchestration artifacts | `implement-models` |

`review-pipeline` and `select-model` are deprecated. `select-model`'s model selection logic (Kimball vs Data Vault vs OBT) is absorbed into the Architecture section of `scope-data-product`.

### `scope-data-product` — section-gated reference loading

`scope-data-product` absorbs four skills' worth of reference material. To stay within the 500-line SKILL.md limit, references are loaded section-by-section: each workflow step cites only the reference files relevant to that section. Steps that are skipped (section already populated, user bails) never load their references. The full reference set is distributed across steps, not declared at the top of the skill.

### `scope-data-product` — re-run behavior

On re-run, the skill builds an agenda from two signals:
1. Sections that are still pending markers
2. Sections flagged as "Potentially affected" in recent Changelog entries

It presents this as a prioritized list and lets the user confirm which sections to work through. The user can add sections not on the list or bail at any point. Sections not visited in the session remain unchanged.

### `scope-data-product` — cross-section consistency rules

When any section is updated, the skill checks whether related sections may now be stale. Concrete relationships:

| Section updated | Potentially affects | Reason |
|---|---|---|
| Architecture | Quality | Tests reference layer structure; if enrichment moves layers, test targets change |
| Architecture | Contract | If enrichment moves, output schema may change |
| Contract | Quality | New or removed fields need corresponding quality rules |
| Sources | Architecture | New or removed sources may not be reflected in the layer model |
| Overview (SLAs) | Contract | Plain-language SLA changes may not be reflected in Contract thresholds |

The warn-and-prompt fires after a section is written: the skill surfaces affected sections, asks whether to continue to them now, and notes the outcome in the Changelog entry regardless.

### `implement-source` behavior

Reads `data-product.md` Sources and Contract sections for pipeline context (ingestion approach, incremental key, schema) in addition to the source scorecard. The source scorecard remains the primary input for extraction code generation. Requires both the source scorecard and `data-product.md` to pass validation before proceeding.

### `implement-data-product` scope

Generates dbt models, `schema.yml` contracts and tests, and orchestration artifacts (DABs `databricks.yml` job/pipeline resources, or equivalent for the active orchestrator). Reads Contract, Quality, and Architecture sections from `data-product.md`. Requires `data-product.md` to pass validation before code generation begins.

## The `data-product.md` Artifact

### Location

```
docs/data-products/<name>/data-product.md
```

### Frontmatter Schema

```yaml
---
name: <data-product-name>
artifact_type: data-product
version: 1.0.0
owner: <owner>
status: draft | active | deprecated
last_modified: <YYYY-MM-DD>
data_product: <name>
sources:
  - <source-name>
---
```

`version` follows semantic versioning:
- **MAJOR**: Breaking contract change — schema removal, type change, SLA tightening, consumer removal
- **MINOR**: Backward-compatible change — new column, threshold recalibration, architecture refactor, new consumer
- **PATCH**: Documentation, metadata, non-functional updates

Version is bumped by the skill based on the nature of the change, with confirmation from the user for MAJOR bumps.

### Section Structure

Sections are introduced by H2 headings. Skipped sections are scaffolded with a pending marker so the full expected structure is always visible.

**Pending marker:**
```markdown
## Contract
<!-- pending: run /dos:scope-data-product to populate this section -->
```

**Section-level metadata** — immediately after the H2 heading on every populated section:
```markdown
## Contract
<!-- last-updated: 2026-04-10 | skill: scope-data-product | version: 1.0.0 -->
```

### Sections

**## Overview**
Consumer table (consumer, role, use case, decision enabled), query patterns (dominant access shape per consumer), and SLA commitments in plain language. Answers: *who needs this data and why?*

**## Sources**
Source inventory table (source name, classification, datasets, ingestion approach, incremental key, freshness requirement), cross-pipeline dependencies, and relative links to source scorecards in `docs/sources/<name>/`. Infrastructure references use the `tool::component.identifier` shorthand where applicable (e.g., `dlt::source.noaa.stations`, `dbt::source.noaa.stations`). Answers: *where does the data come from and how does it arrive?*

**## Contract**
Schema table (field name, type, nullable, description, constraints), SLA terms (freshness, completeness, availability as measurable thresholds), consumer commitments, and enforcement notes (which dbt model and config enforces this contract). Answers: *what does this data product promise to deliver?*

**## Quality**
Quality dimensions table (dimension, measurement method, rule type, threshold, dbt test, owner), scoring weights, and alert thresholds. Answers: *how do we know the data is good?*

**## Architecture**
Model selection rationale (Kimball vs Data Vault vs OBT — absorbed from `select-model`), layer description (raw → staging → intermediate → mart or equivalent), model inventory table (model name, layer, materialization, description), compute and scheduling declarations using `tool::component.identifier` shorthand (`dbt::target.<name>`, `dbx::job.<name>`), and cross-pipeline dependency ordering. Answers: *how is the data product built?*

**## Changelog**
Append-only, chronological. Each entry records the version bump, date, authoring skill, sections updated, what changed, why, and which other sections are potentially affected.

```markdown
## Changelog

### v1.1.0 — 2026-04-10 (scope-data-product)
**Sections updated:** Architecture
**Change:** Moved enrichment from Python processing_steps in dlt to dbt intermediate layer (int_noaa__stations_enriched).
**Reason:** Extraction boundary violation — enrichment logic does not belong in the extraction layer.
**Potentially affected:** Quality (enrichment-layer tests may need updating).
```

## Validation Scripts

Two scripts gate code generation. Both exit 0 on pass and exit 2 with a structured message on failure.

### `validate-upstream.py` (unchanged contract)

Used by `implement-source`. Validates that the source scorecard exists and passes structural checks. Contract and behavior are unchanged from the current implementation.

### `validate-data-product.py` (new)

Used by both build-phase skills, with different required sections per skill.

**`implement-source` invocation:**
```bash
python ${CLAUDE_SKILL_DIR}/scripts/validate-data-product.py <data-product-name> --require sources
```
Validates: `data-product.md` exists, has valid frontmatter, and the Sources section is populated and non-pending.

**`implement-data-product` invocation:**
```bash
python ${CLAUDE_SKILL_DIR}/scripts/validate-data-product.py <data-product-name> --require contract,quality,architecture
```
Validates: `data-product.md` exists, has valid frontmatter, and Contract + Quality + Architecture sections are all populated and non-pending.

Failure message format: identifies the specific section(s) failing, states which pending marker was found or which section is absent, and specifies the corrective invocation (`/dos:scope-data-product`).

## Acceptance Criteria

1. Running `scope-data-product` on a new data product creates `docs/data-products/<name>/data-product.md` with completed sections populated and all skipped sections scaffolded as pending markers.

2. Running `scope-data-product` on an existing data product presents a prioritized agenda of pending and consistency-flagged sections. The user selects which to work through. Each completed section is updated in-place with an updated `<!-- last-updated: -->` comment, a version bump to frontmatter, and a new Changelog entry.

3. The Changelog section is append-only. No skill removes or modifies existing entries.

4. `validate-data-product.py --require sources` passes for `implement-source` when the Sources section is populated. `validate-data-product.py --require contract,quality,architecture` passes for `implement-data-product` when all three sections are populated.

5. Each populated section carries a `<!-- last-updated: | skill: | version: -->` comment immediately after its H2 heading.

6. Source scorecard files in `docs/sources/` are unchanged. The Sources section of `data-product.md` references them by relative path.

7. `git log --follow -- docs/data-products/<name>/data-product.md` reveals the full modification history of the data product.

8. `implement-data-product` produces orchestration artifacts (DABs YAML or equivalent) alongside dbt models when the Architecture section specifies an orchestrator.

9. Existing data products with the old 6-file layout can be migrated: `scope-data-product` detects legacy artifact files, incorporates their content into the appropriate sections, and prompts to archive the originals. Legacy `reviews/` files are discarded — git history preserves their content.

## Out of Scope

- Source scorecard structure changes (`docs/sources/` layout unchanged)
- Plan structure (`docs/plans/` unchanged)
- Per-section YAML frontmatter blocks
- dbt project `schema.yml` or test file changes (enforcement layer is separate from DOS artifacts)
- Specific orchestration artifact format for `implement-data-product` (determined during implementation based on Architecture section content)

## Changelog

### v0.3.0 — 2026-04-10 (brainstorm)
Resolved all pre-planning ambiguities: renamed artifact to `data-product.md`; added section-gated reference loading architecture for `scope-data-product`; split validate-upstream.py into two scripts with separate concerns; absorbed `select-model` into `scope-data-product` Architecture step; defined concrete cross-section consistency rules; specified re-run agenda as pending + consistency-flagged sections; migration discards legacy `reviews/` files.

### v0.2.0 — 2026-04-10 (brainstorm)
Revised skill chain: 7 skills → 4. Introduced `scope-source`, `scope-data-product`, `implement-source`, `implement-data-product` naming. `implement-data-product` includes orchestration artifacts. `review-pipeline` deprecated.

### v0.1.0 — 2026-04-10 (brainstorm)
Initial design draft. Closes issue #23.
