---
name: Scope + Design Phase Skills
description: Implement 5 skills (scope-data-product, select-model, define-contract, assess-quality, design-pipeline) following the validated pattern from evaluate-source.
type: plan
status: completed
related:
  - docs/designs/2026-03-23-dos-skill-library-design.md
  - docs/plans/2026-03-23-foundation-evaluate-source.plan.md
---

# Scope + Design Phase Skills

**Goal:** Deliver 5 usable skills covering the Scope and Design phases of the data product lifecycle. After this plan, a user can go from source evaluation through scoping, modeling decisions, contract definition, quality configuration, and pipeline architecture — producing persistent artifacts at each step that downstream Build-phase skills will consume.

**Scope:**

Must have:
- `skills/scope-data-product/` — SKILL.md, 4 references, 1 asset template (scope document)
- `skills/select-model/` — SKILL.md, 2 references (no separate asset — updates scope document)
- `skills/define-contract/` — SKILL.md, 3 references, 1 asset template (contract)
- `skills/assess-quality/` — SKILL.md, 5 references, 1 asset template (quality config)
- `skills/design-pipeline/` — SKILL.md, 4 references, 1 asset template (pipeline architecture)
- All SKILL.md files under 500 lines with progressive disclosure to references/
- All skills follow the validated pattern: preamble check, workflow steps, next steps
- Artifact templates match the frontmatter schema in `docs/data-products/_index.md`

Won't have:
- Build-phase skills (implement-source, implement-models) — those are Plan 3
- Review-pipeline — Plan 3
- Validation scripts in scripts/ — design-phase skills are advisory, not code-generating
- Claude Code hook wiring — portable core only
- Modifications to evaluate-source

**Approach:** Follow the template-first pattern validated in Plan 1: for each skill, create the artifact template first, then curate references from the context corpus, then write SKILL.md last. Skills that share context files (e.g., scope and assess-quality both use data-quality-dimensions) produce independent reference extracts — each skill carries its own knowledge. The 5 skills can be built sequentially in dependency order: scope-data-product first (produces artifacts consumed by all others), then the 4 design skills (independent of each other).

**File Changes:**

- Create: `skills/scope-data-product/assets/scope-document.md`
- Create: `skills/scope-data-product/references/consumption-heuristics.md`
- Create: `skills/scope-data-product/references/interview-questions.md`
- Create: `skills/scope-data-product/references/sla-hierarchy.md`
- Create: `skills/scope-data-product/references/quality-dimension-selection.md`
- Create: `skills/scope-data-product/SKILL.md`
- Create: `skills/select-model/references/model-decision-matrix.md`
- Create: `skills/select-model/references/platform-modeling-guidance.md`
- Create: `skills/select-model/SKILL.md`
- Create: `skills/define-contract/assets/contract-template.md`
- Create: `skills/define-contract/references/odcs-structure.md`
- Create: `skills/define-contract/references/enforcement-layers.md`
- Create: `skills/define-contract/references/versioning-patterns.md`
- Create: `skills/define-contract/SKILL.md`
- Create: `skills/assess-quality/assets/quality-config-template.md`
- Create: `skills/assess-quality/references/quality-dimensions.md`
- Create: `skills/assess-quality/references/scoring-methods.md`
- Create: `skills/assess-quality/references/sla-error-budgets.md`
- Create: `skills/assess-quality/references/validation-tiers.md`
- Create: `skills/assess-quality/references/anomaly-methods.md`
- Create: `skills/assess-quality/SKILL.md`
- Create: `skills/design-pipeline/assets/pipeline-architecture-template.md`
- Create: `skills/design-pipeline/references/consumption-to-architecture.md`
- Create: `skills/design-pipeline/references/incremental-patterns.md`
- Create: `skills/design-pipeline/references/layering-strategy.md`
- Create: `skills/design-pipeline/references/schema-evolution-patterns.md`
- Create: `skills/design-pipeline/SKILL.md`
- Modify: `README.md` (add 5 skills to table)
- Modify: `docs/plans/_index.md` (add this plan)

**Branch:** `feat/scope-design-skills`
**PR:** TBD

---

## Chunk 1: scope-data-product

### Task 1: Scope document artifact template

**Files:**
- Create: `skills/scope-data-product/assets/scope-document.md`

- [x] **Step 1:** Create the scope document template. Must include: YAML frontmatter (with standard artifact fields plus a `sources` list field referencing source evaluations), sections for consumers and use cases, source inventory (which sources and datasets), query patterns, freshness requirements (in specific time units), SLA tier and dimensions, quality dimensions with initial thresholds, modeling recommendation placeholder, MoSCoW prioritization, explicit "Won't have in v1" section, next steps, and changelog. <!-- sha:ad3551f -->
- [x] **Step 2:** Verify: template contains all sections from the design's scope-data-product workflow. Check for: `sources` field in frontmatter, consumers section, freshness requirements, SLA dimensions, quality dimensions, "Won't have in v1" section, and next steps mentioning downstream skills. <!-- sha:ad3551f -->
- [x] **Step 3:** Commit <!-- sha:ad3551f -->

---

### Task 2: scope-data-product references

**Files:**
- Create: `skills/scope-data-product/references/consumption-heuristics.md`
- Create: `skills/scope-data-product/references/interview-questions.md`
- Create: `skills/scope-data-product/references/sla-hierarchy.md`
- Create: `skills/scope-data-product/references/quality-dimension-selection.md`

- [x] **Step 1:** Read `docs/context/consumption-driven-architecture.md`. Extract the three consumption dimensions (query shape → modeling, freshness → ingestion, SLA tier → investment) into `consumption-heuristics.md` as a decision table. Target under 100 lines. <!-- sha:b22809f -->
- [x] **Step 2:** Read `docs/context/requirements-gathering-techniques.md`. Extract the Data Product Canvas blocks, stakeholder interview patterns, and MoSCoW prioritization framework into `interview-questions.md`. Target under 100 lines. <!-- sha:b22809f -->
- [x] **Step 3:** Read `docs/context/data-freshness-slas.md` and `docs/context/data-quality-slas.md`. Extract the SLI/SLO/SLA hierarchy, five SLA dimensions, and error budget patterns into `sla-hierarchy.md`. Target under 100 lines. <!-- sha:b22809f -->
- [x] **Step 4:** Read `docs/context/data-quality-dimensions.md`. Extract the six-dimension consensus, dimension selection criteria, and guidance on which dimensions to start with into `quality-dimension-selection.md`. Target under 100 lines. <!-- sha:b22809f -->
- [x] **Step 5:** Verify: `wc -l skills/scope-data-product/references/*.md` — all under 100 lines. 4 files present. <!-- sha:b22809f -->
- [x] **Step 6:** Commit <!-- sha:b22809f -->

---

### Task 3: SKILL.md for scope-data-product

**Files:**
- Create: `skills/scope-data-product/SKILL.md`

**Depends on:** Tasks 1, 2

- [x] **Step 1:** Write SKILL.md implementing the full 12-step workflow from the design. Preamble asks which data product (not source — this is a data product skill). Check for existing scope in `docs/data-products/<name>/scope.md`. Check `docs/sources/` for available source evaluations to pre-populate. Reference all 4 curated files and the asset template. End with next steps suggesting select-model, define-contract, assess-quality, design-pipeline. <!-- sha:d6737a6 -->
- [x] **Step 2:** Verify: `wc -l skills/scope-data-product/SKILL.md` — under 500 lines. Contains references to all 4 reference files and the asset template. <!-- sha:d6737a6 -->
- [x] **Step 3:** Commit <!-- sha:d6737a6 -->

---

## Chunk 2: select-model

### Task 4: select-model references

**Files:**
- Create: `skills/select-model/references/model-decision-matrix.md`
- Create: `skills/select-model/references/platform-modeling-guidance.md`

- [x] **Step 1:** Read `docs/context/data-model-selection.md`. Extract the Kimball vs Data Vault vs OBT decision matrix with selection criteria (team size, source count, query pattern, compliance, change velocity) into `model-decision-matrix.md`. Target under 100 lines. <!-- sha:d845e27 -->
- [x] **Step 2:** Read `docs/context/kimball-dimensional-modeling.md`, `docs/context/obt-wide-table-patterns.md`, `docs/context/data-vault-modeling.md`, and `docs/context/data-model-selection.md`. Extract platform-specific modeling guidance (DuckDB, Snowflake, Databricks, ClickHouse) and counter-evidence into `platform-modeling-guidance.md`. Target under 100 lines. <!-- sha:d845e27 -->
- [x] **Step 3:** Verify: `wc -l skills/select-model/references/*.md` — all under 100 lines. 2 files present. <!-- sha:d845e27 -->
- [x] **Step 4:** Commit <!-- sha:d845e27 -->

---

### Task 5: SKILL.md for select-model

**Files:**
- Create: `skills/select-model/SKILL.md`

**Depends on:** Task 4

- [x] **Step 1:** Write SKILL.md implementing the 7-step workflow from the design. Preamble asks which data product, checks for existing scope document in `docs/data-products/<name>/scope.md`. No separate asset template — this skill updates the scope document's modeling recommendation section. Reference both curated files. End with next steps suggesting define-contract and implement-models. <!-- sha:d845e27 -->
- [x] **Step 2:** Verify: `wc -l skills/select-model/SKILL.md` — under 500 lines. Contains references to both reference files. Contains instruction to persist recommendation to scope document. <!-- sha:d845e27 -->
- [x] **Step 3:** Commit <!-- sha:d845e27 -->

---

## Chunk 3: define-contract

### Task 6: Contract artifact template

**Files:**
- Create: `skills/define-contract/assets/contract-template.md`

- [x] **Step 1:** Create the contract template aligned with ODCS v3.1. Must include: YAML frontmatter (standard artifact fields), sections for all 11 ODCS sections (Fundamentals, Schema, References, Data Quality, Support, Pricing, Team, Roles, SLA, Infrastructure, Custom Properties), versioning section with expand-contract guidance, enforcement strategy (CI-time, build-time, runtime), optional dbt contract snippet, next steps, and changelog. <!-- sha:ba75285 -->
- [x] **Step 2:** Verify: template contains all 11 ODCS sections, versioning guidance, enforcement strategy with three layers, and next steps mentioning assess-quality and implement-models. <!-- sha:ba75285 -->
- [x] **Step 3:** Commit <!-- sha:ba75285 -->

---

### Task 7: define-contract references

**Files:**
- Create: `skills/define-contract/references/odcs-structure.md`
- Create: `skills/define-contract/references/enforcement-layers.md`
- Create: `skills/define-contract/references/versioning-patterns.md`

- [x] **Step 1:** Read `docs/context/data-contract-structure.md` and `docs/context/data-contracts.md`. Extract the ODCS v3.1 section inventory and field-level requirements into `odcs-structure.md`. Target under 120 lines. <!-- sha:ba75285 -->
- [x] **Step 2:** Read `docs/context/data-contract-enforcement-versioning.md`. Extract the three enforcement layers (CI-time, build-time, runtime) with tool mappings into `enforcement-layers.md`. Target under 100 lines. <!-- sha:ba75285 -->
- [x] **Step 3:** Read `docs/context/data-contract-enforcement-versioning.md` and `docs/context/schema-evolution.md`. Extract semantic versioning rules, expand-contract pattern, and breaking vs additive change classification into `versioning-patterns.md`. Target under 100 lines. <!-- sha:ba75285 -->
- [x] **Step 4:** Verify: `wc -l skills/define-contract/references/*.md` — all under 120 lines. 3 files present. <!-- sha:ba75285 -->
- [x] **Step 5:** Commit <!-- sha:ba75285 -->

---

### Task 8: SKILL.md for define-contract

**Files:**
- Create: `skills/define-contract/SKILL.md`

**Depends on:** Tasks 6, 7

- [x] **Step 1:** Write SKILL.md implementing the 11-step workflow from the design. Preamble asks which data product, checks for existing contract in `docs/data-products/<name>/contract.md` and scope document. Reference all 3 curated files and the asset template. End with next steps suggesting assess-quality and implement-models. <!-- sha:ba75285 -->
- [x] **Step 2:** Verify: `wc -l skills/define-contract/SKILL.md` — under 500 lines. Contains references to all 3 reference files and the asset template. <!-- sha:ba75285 -->
- [x] **Step 3:** Commit <!-- sha:ba75285 -->

---

## Chunk 4: assess-quality

### Task 9: Quality config artifact template

**Files:**
- Create: `skills/assess-quality/assets/quality-config-template.md`

- [x] **Step 1:** Create the quality config template. Must include: YAML frontmatter (standard artifact fields), sections for selected quality dimensions with thresholds, measurement methods, scoring method and weights, composite score formula, action thresholds (green/yellow/red) with owners, validation tooling by tier (local/CI/production), anomaly detection approach, next steps, and changelog. <!-- sha:6e66cfd -->
- [x] **Step 2:** Verify: template contains quality dimensions table, scoring section, action thresholds with owners, validation tiers, anomaly detection section, and next steps mentioning implement-models. <!-- sha:6e66cfd -->
- [x] **Step 3:** Commit <!-- sha:6e66cfd -->

---

### Task 10: assess-quality references

**Files:**
- Create: `skills/assess-quality/references/quality-dimensions.md`
- Create: `skills/assess-quality/references/scoring-methods.md`
- Create: `skills/assess-quality/references/sla-error-budgets.md`
- Create: `skills/assess-quality/references/validation-tiers.md`
- Create: `skills/assess-quality/references/anomaly-methods.md`

- [x] **Step 1:** Read `docs/context/data-quality-dimensions.md`. Extract the six-dimension consensus with definitions and selection guidance into `quality-dimensions.md`. Target under 100 lines. <!-- sha:6e66cfd -->
- [x] **Step 2:** Read `docs/context/data-quality-scoring.md`. Extract scoring methods (test fail rate vs failed row count), weighted aggregation, and score interpretation into `scoring-methods.md`. Target under 80 lines. <!-- sha:6e66cfd -->
- [x] **Step 3:** Read `docs/context/data-quality-slas.md` and `docs/context/data-freshness-slas.md`. Extract SLI/SLO/SLA hierarchy, error budget calculation, and tiered SLA guidance into `sla-error-budgets.md`. Target under 100 lines. <!-- sha:6e66cfd -->
- [x] **Step 4:** Read `docs/context/tiered-validation-strategy.md` and `docs/context/data-validation-tool-comparison.md`. Extract three-tier validation mapping and tool comparison into `validation-tiers.md`. Target under 100 lines. <!-- sha:6e66cfd -->
- [x] **Step 5:** Read `docs/context/anomaly-drift-detection.md`. Extract anomaly detection approach selection (rule-based, statistical, ML) with method comparison into `anomaly-methods.md`. Target under 80 lines. <!-- sha:6e66cfd -->
- [x] **Step 6:** Verify: `wc -l skills/assess-quality/references/*.md` — all under 100 lines. 5 files present. <!-- sha:6e66cfd -->
- [x] **Step 7:** Commit <!-- sha:6e66cfd -->

---

### Task 11: SKILL.md for assess-quality

**Files:**
- Create: `skills/assess-quality/SKILL.md`

**Depends on:** Tasks 9, 10

- [x] **Step 1:** Write SKILL.md implementing the 11-step workflow from the design. Preamble asks which data product, checks for existing quality config in `docs/data-products/<name>/quality-config.md`, scope document, and contract. Reference all 5 curated files and the asset template. End with next steps suggesting implement-models and define-contract. <!-- sha:6e66cfd -->
- [x] **Step 2:** Verify: `wc -l skills/assess-quality/SKILL.md` — under 500 lines. Contains references to all 5 reference files and the asset template. <!-- sha:6e66cfd -->
- [x] **Step 3:** Commit <!-- sha:6e66cfd -->

---

## Chunk 5: design-pipeline

### Task 12: Pipeline architecture artifact template

**Files:**
- Create: `skills/design-pipeline/assets/pipeline-architecture-template.md`

- [x] **Step 1:** Create the pipeline architecture template. Must include: YAML frontmatter (standard artifact fields plus `sources` list), sections for source inventory with ingestion approaches per source, layering strategy (medallion or staging+marts), incremental loading pattern per source with silent failure modes, idempotency strategy, schema evolution approach, platform-specific considerations, anti-patterns flagged, next steps, and changelog. <!-- sha:3903629 -->
- [x] **Step 2:** Verify: template contains layering strategy, incremental patterns with failure modes, idempotency section, schema evolution, and next steps mentioning implement-source and implement-models. <!-- sha:3903629 -->
- [x] **Step 3:** Commit <!-- sha:3903629 -->

---

### Task 13: design-pipeline references

**Files:**
- Create: `skills/design-pipeline/references/consumption-to-architecture.md`
- Create: `skills/design-pipeline/references/incremental-patterns.md`
- Create: `skills/design-pipeline/references/layering-strategy.md`
- Create: `skills/design-pipeline/references/schema-evolution-patterns.md`

- [x] **Step 1:** Read `docs/context/consumption-driven-architecture.md`. Extract consumption-to-architecture heuristics (query shape → modeling, freshness → ingestion, SLA → investment) into `consumption-to-architecture.md`. Target under 80 lines. <!-- sha:3903629 -->
- [x] **Step 2:** Read `docs/context/incremental-loading-patterns.md`. Extract the five patterns, selection framework, silent failure modes per pattern, and idempotency strategies into `incremental-patterns.md`. Target under 120 lines. <!-- sha:3903629 -->
- [x] **Step 3:** Read `docs/context/medallion-architecture.md`. Extract medallion vs simpler layering decision criteria, layer responsibilities, and when each is appropriate into `layering-strategy.md`. Target under 80 lines. <!-- sha:3903629 -->
- [x] **Step 4:** Read `docs/context/schema-evolution.md`. Extract compatibility rules, expand-contract pattern, and tool-specific handling (dbt, dlt, Delta Lake) into `schema-evolution-patterns.md`. Target under 100 lines. <!-- sha:3903629 -->
- [x] **Step 5:** Verify: `wc -l skills/design-pipeline/references/*.md` — all under 120 lines. 4 files present. <!-- sha:3903629 -->
- [x] **Step 6:** Commit <!-- sha:3903629 -->

---

### Task 14: SKILL.md for design-pipeline

**Files:**
- Create: `skills/design-pipeline/SKILL.md`

**Depends on:** Tasks 12, 13

- [x] **Step 1:** Write SKILL.md implementing the 11-step workflow from the design. Preamble asks which data product, checks for existing pipeline architecture in `docs/data-products/<name>/pipeline-architecture.md`, scope document, and source evaluations in `docs/sources/`. Reference all 4 curated files and the asset template. End with next steps suggesting implement-source and implement-models. <!-- sha:3903629 -->
- [x] **Step 2:** Verify: `wc -l skills/design-pipeline/SKILL.md` — under 500 lines. Contains references to all 4 reference files and the asset template. <!-- sha:3903629 -->
- [x] **Step 3:** Commit <!-- sha:3903629 -->

---

## Chunk 6: Integration

### Task 15: Update project documentation

**Files:**
- Modify: `README.md` (add 5 skills to table)
- Modify: `docs/plans/_index.md` (add this plan)

- [x] **Step 1:** Update README.md skills table to add all 5 skills with descriptions. <!-- sha:efd2aa5 -->
- [x] **Step 2:** Update `docs/plans/_index.md` to include this plan. <!-- sha:efd2aa5 -->
- [x] **Step 3:** Verify: `grep -c "dos:" README.md` — shows 7 matches (6 table rows + 1 header). <!-- sha:efd2aa5 -->
- [x] **Step 4:** Commit <!-- sha:efd2aa5 -->

---

## Validation

- [ ] `ls skills/` — shows 6 directories: evaluate-source, scope-data-product, select-model, define-contract, assess-quality, design-pipeline
- [ ] `for d in scope-data-product select-model define-contract assess-quality design-pipeline; do wc -l skills/$d/SKILL.md; done` — all under 500 lines
- [ ] `for d in scope-data-product select-model define-contract assess-quality design-pipeline; do head -4 skills/$d/SKILL.md; done` — all have Agent Skills spec frontmatter with `name` and `description`
- [ ] `ls skills/scope-data-product/references/` — 4 files
- [ ] `ls skills/select-model/references/` — 2 files
- [ ] `ls skills/define-contract/references/` — 3 files
- [ ] `ls skills/assess-quality/references/` — 5 files
- [ ] `ls skills/design-pipeline/references/` — 4 files
- [ ] `ls skills/scope-data-product/assets/ skills/define-contract/assets/ skills/assess-quality/assets/ skills/design-pipeline/assets/` — 4 asset templates present
- [ ] `grep -c "dos:" README.md` — 6 skills listed
- [ ] Each SKILL.md contains a preamble check, workflow steps, and "Next Steps" section
- [ ] Artifact templates use the frontmatter schema from `docs/data-products/_index.md`
