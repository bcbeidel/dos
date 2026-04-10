---
name: Pipeline Document Consolidation
description: Replace 6 per-pipeline DOS artifacts with data-product.md; collapse 9 skills into 4 (scope-source, scope-data-product, implement-source, implement-data-product).
type: plan
status: completed
branch: feat/pipeline-document-consolidation
related:
  - docs/designs/2026-04-10-pipeline-document-consolidation.design.md
---

# Pipeline Document Consolidation

**Goal:** Replace the 6-file per-pipeline artifact structure with a single `data-product.md` living document, collapse 9 skills into 4, and eliminate artifact drift by making `data-product.md` the sole specification consumed by build-phase skills.

**Scope:**

Must have:
- `data-product.md` asset template with frontmatter schema and all 6 sections as pending markers
- `validate-data-product.py` validation script (separate from `validate-upstream.py`)
- `scope-data-product` SKILL.md rewrite: 5-section workflow with section-gated references, re-run behavior, cross-section consistency rules, Changelog append logic
- 15 reference files from deprecated skills copied into `skills/scope-data-product/references/`
- `implement-source` preamble updated to validate and read `data-product.md` Sources section
- `implement-data-product` skill (from `implement-models` + orchestration artifact generation)
- `scope-source` skill (renamed from `evaluate-source`)
- 6 deprecated SKILL.md files marked `status: deprecated`: define-contract, assess-quality, design-pipeline, select-model, review-pipeline, implement-models
- CLAUDE.md skill chain table updated

Won't have:
- Deletion of deprecated skill directories — archived, not removed; git history preserved
- Source scorecard structure changes (`docs/sources/` unchanged)
- Plan structure changes (`docs/plans/` unchanged)
- Per-section YAML frontmatter blocks
- Prescribed orchestration artifact format — implement-data-product reads Architecture section and determines format at runtime
- Migration of existing data products — no `docs/data-products/` entries exist yet

**Approach:** Template-first authoring. Asset template and validation script before any SKILL.md changes. References consolidated before the SKILL.md that references them. `implement-source` updated after the artifact template is stable. `implement-data-product` created as a new skill directory (content diverges substantially from `implement-models`). `evaluate-source` renamed via `git mv` to preserve history.

**File Changes:**
- Create: `skills/scope-data-product/assets/data-product.md`
- Create: `skills/implement-source/scripts/validate-data-product.py`
- Create: `skills/implement-data-product/scripts/validate-data-product.py` (identical to above — each skill uses `${CLAUDE_SKILL_DIR}/scripts/` prefix)
- Copy into `skills/scope-data-product/references/` (15 files from 4 deprecated skills):
  - From `define-contract/references/`: enforcement-layers.md, odcs-structure.md, versioning-patterns.md
  - From `assess-quality/references/`: anomaly-methods.md, dbt-test-selection.md, quality-dimensions.md, scoring-methods.md, sla-error-budgets.md, validation-tiers.md
  - From `design-pipeline/references/`: consumption-to-architecture.md, incremental-patterns.md, layering-strategy.md, schema-evolution-patterns.md
  - From `select-model/references/`: model-decision-matrix.md, platform-modeling-guidance.md
- Rewrite: `skills/scope-data-product/SKILL.md`
- Modify: `skills/implement-source/SKILL.md`
- Create: `skills/implement-data-product/references/` (4 files copied from `implement-models/references/`)
- Create: `skills/implement-data-product/SKILL.md`
- Rename: `skills/evaluate-source/` → `skills/scope-source/` via `git mv`
- Modify frontmatter (status: deprecated): `skills/define-contract/SKILL.md`, `skills/assess-quality/SKILL.md`, `skills/design-pipeline/SKILL.md`, `skills/select-model/SKILL.md`, `skills/review-pipeline/SKILL.md`, `skills/implement-models/SKILL.md`
- Update: `CLAUDE.md` (skill chain table)
- Update: `docs/plans/_index.md`

---

## Chunk 1: Artifact Template

### Task 1: data-product.md asset template

**Files:**
- Create: `skills/scope-data-product/assets/data-product.md`

- [x] **Step 1:** Create `skills/scope-data-product/assets/data-product.md` with: <!-- sha:b7f5078 -->
  - Frontmatter using `{{placeholder}}` syntax: `name`, `artifact_type: data-product`, `version: 0.1.0`, `owner`, `status: draft`, `last_modified`, `data_product`, `sources` (list)
  - H2 heading + pending marker for each of the 5 authored sections (Overview, Sources, Contract, Quality, Architecture):
    ```markdown
    ## Overview
    <!-- pending: run /dos:scope-data-product to populate this section -->
    ```
  - H2 Changelog section pre-populated with an example entry block showing the expected format (version, date, skill, sections updated, change, reason, potentially affected).

- [x] **Step 2:** Verify: `grep -c "<!-- pending:" skills/scope-data-product/assets/data-product.md` — returns 5. <!-- sha:b7f5078 -->

- [x] **Step 3:** Commit. <!-- sha:b7f5078 -->

---

## Chunk 2: Validation Script

### Task 2: validate-data-product.py

**Files:**
- Create: `skills/implement-source/scripts/validate-data-product.py`
- Create: `skills/implement-data-product/scripts/validate-data-product.py` (identical)

Both skills resolve scripts via `${CLAUDE_SKILL_DIR}/scripts/`, requiring the same file in both locations. Keep them in sync.

- [x] **Step 1:** Create `skills/implement-source/scripts/validate-data-product.py` with: <!-- sha:5fe5bb2 -->
  - Positional arg: `<data-product-name>`
  - `--require` flag: comma-separated section names (`sources`, `contract`, `quality`, `architecture`)
  - Resolves artifact path as `docs/data-products/<name>/data-product.md` from cwd
  - Validates in order:
    1. File exists
    2. Frontmatter is valid YAML with required fields: `name`, `artifact_type`, `status`, `version`
    3. `artifact_type == "data-product"`
    4. Each required section: H2 heading is present and the line immediately following is not a `<!-- pending:` marker
  - Exit 0: prints `PASS: data-product '<name>' passes validation`
  - Exit 2: structured message following `validate-upstream.py` style:
    ```
    ERROR: Section 'contract' is pending or missing in docs/data-products/<name>/data-product.md
    FIX: Run /dos:scope-data-product to populate the Contract section
    ```

- [x] **Step 2:** Create `skills/implement-data-product/scripts/` directory and copy the script there. <!-- sha:5fe5bb2 -->

- [x] **Step 3:** Verify error path: `python skills/implement-source/scripts/validate-data-product.py nonexistent-product --require sources; echo "exit: $?"` — prints an ERROR line and `exit: 2`. <!-- sha:5fe5bb2 -->

- [x] **Step 4:** Commit. <!-- sha:5fe5bb2 -->

---

## Chunk 3: Reference Consolidation

### Task 3: Copy reference files into scope-data-product

**Files:**
- Copy 15 files into `skills/scope-data-product/references/` (sources remain in their original locations for deprecated skills)

- [x] **Step 1:** Copy the following files into `skills/scope-data-product/references/`: <!-- sha:e0a0dfa -->
  - `skills/define-contract/references/enforcement-layers.md`
  - `skills/define-contract/references/odcs-structure.md`
  - `skills/define-contract/references/versioning-patterns.md`
  - `skills/assess-quality/references/anomaly-methods.md`
  - `skills/assess-quality/references/dbt-test-selection.md`
  - `skills/assess-quality/references/quality-dimensions.md`
  - `skills/assess-quality/references/scoring-methods.md`
  - `skills/assess-quality/references/sla-error-budgets.md`
  - `skills/assess-quality/references/validation-tiers.md`
  - `skills/design-pipeline/references/consumption-to-architecture.md`
  - `skills/design-pipeline/references/incremental-patterns.md`
  - `skills/design-pipeline/references/layering-strategy.md`
  - `skills/design-pipeline/references/schema-evolution-patterns.md`
  - `skills/select-model/references/model-decision-matrix.md`
  - `skills/select-model/references/platform-modeling-guidance.md`

- [x] **Step 2:** Verify: `ls skills/scope-data-product/references/ | wc -l` — returns 19 (4 original + 15 new). <!-- sha:e0a0dfa -->

- [x] **Step 3:** Verify no file exceeds 200 lines: `wc -l skills/scope-data-product/references/*.md` — inspect the totals column for any value over 200. <!-- sha:e0a0dfa -->

- [x] **Step 4:** Commit. <!-- sha:e0a0dfa -->

---

## Chunk 4: scope-data-product SKILL.md

### Task 4: Rewrite scope-data-product SKILL.md

**Files:**
- Rewrite: `skills/scope-data-product/SKILL.md`

**Depends on:** Tasks 1, 3

This rewrite collapses the content of 5 SKILL.md files (990 combined lines) into one file under 500 lines using section-gated reference loading — each step cites only the references for that section. Skipped steps never load their references.

- [x] **Step 1:** Write the new `skills/scope-data-product/SKILL.md` with this structure: <!-- sha:9102500 -->

  **Frontmatter:** `name: scope-data-product`, `description: ...`

  **Preamble:**
  1. Ask for the data product name
  2. Check for `docs/data-products/<name>/data-product.md`
     - **New mode** (no file): scaffold from the asset template — create the directory, copy the template, substitute `name` and `last_modified` in frontmatter, all sections start as pending markers
     - **Re-run mode** (file exists): build agenda from (a) sections with `<!-- pending:` markers and (b) sections named in recent Changelog "Potentially affected:" lines. Present prioritized list to user. User confirms which sections to work through. User can add sections or bail at any point.

  **Workflow — 5 steps, one per section:**

  **Step 1: Overview**
  Reference: `[interview-questions.md](references/interview-questions.md)`, `[consumption-heuristics.md](references/consumption-heuristics.md)`, `[sla-hierarchy.md](references/sla-hierarchy.md)`
  - Produce: consumer table (consumer, role, use case, decision enabled), query patterns, SLA commitments in plain language
  - Write section with `<!-- last-updated: <date> | skill: scope-data-product | version: <version> -->` immediately after H2
  - Consistency check: if SLAs changed, flag Contract as potentially affected

  **Step 2: Sources**
  - Produce: source inventory table (source name, classification, datasets, ingestion approach, incremental key, freshness requirement), cross-pipeline dependencies, relative links to `docs/sources/<name>/` scorecards, infrastructure references using `tool::component.identifier` shorthand
  - Write section with metadata comment
  - Consistency check: if sources changed, flag Architecture as potentially affected

  **Step 3: Contract**
  Reference: `[odcs-structure.md](references/odcs-structure.md)`, `[enforcement-layers.md](references/enforcement-layers.md)`, `[versioning-patterns.md](references/versioning-patterns.md)`
  - Produce: schema table (field, type, nullable, description, constraints), SLA terms (freshness, completeness, availability as measurable thresholds), consumer commitments, enforcement notes
  - Write section with metadata comment
  - Consistency check: if schema changed, flag Quality as potentially affected

  **Step 4: Quality**
  Reference: `[quality-dimensions.md](references/quality-dimensions.md)`, `[dbt-test-selection.md](references/dbt-test-selection.md)`, `[anomaly-methods.md](references/anomaly-methods.md)`, `[scoring-methods.md](references/scoring-methods.md)`, `[sla-error-budgets.md](references/sla-error-budgets.md)`, `[validation-tiers.md](references/validation-tiers.md)`, `[quality-dimension-selection.md](references/quality-dimension-selection.md)`
  - Produce: quality dimensions table (dimension, measurement method, rule type, threshold, dbt test, owner), scoring weights, alert thresholds
  - Write section with metadata comment

  **Step 5: Architecture**
  Reference: `[layering-strategy.md](references/layering-strategy.md)`, `[consumption-to-architecture.md](references/consumption-to-architecture.md)`, `[incremental-patterns.md](references/incremental-patterns.md)`, `[schema-evolution-patterns.md](references/schema-evolution-patterns.md)`, `[model-decision-matrix.md](references/model-decision-matrix.md)`, `[platform-modeling-guidance.md](references/platform-modeling-guidance.md)`
  - Produce: model selection rationale (Kimball vs Data Vault vs OBT), layer description, model inventory table (model name, layer, materialization, description), compute and scheduling declarations using `tool::component.identifier` shorthand, cross-pipeline dependency ordering
  - Write section with metadata comment

  **After each completed section:** present affected sections per the cross-section consistency table. Ask whether to continue to them now. Note outcome in the Changelog entry regardless.

  **Step 6: Version and Changelog**
  - Determine version bump: MAJOR (breaking contract change — schema removal, type change, SLA tightening), MINOR (backward-compatible — new column, threshold recalibration, architecture refactor), PATCH (docs/metadata only). Confirm MAJOR bumps with user.
  - Update `version` and `last_modified` in frontmatter
  - Append Changelog entry: version, date, skill, sections updated, change, reason, potentially affected

  **Cross-section consistency rules table** (at the end of the SKILL.md):

  | Section updated | Potentially affects | Reason |
  |---|---|---|
  | Architecture | Quality | Tests reference layer structure |
  | Architecture | Contract | Enrichment moves may change output schema |
  | Contract | Quality | New or removed fields need quality rules |
  | Sources | Architecture | New or removed sources may not be reflected in the layer model |
  | Overview (SLAs) | Contract | Plain-language SLA changes may not match Contract thresholds |

- [x] **Step 2:** Verify: `wc -l skills/scope-data-product/SKILL.md` — under 500 lines. <!-- sha:9102500 -->

- [x] **Step 3:** Verify all 19 references are cited: `grep "references/" skills/scope-data-product/SKILL.md | wc -l` — returns 19 or more. <!-- sha:9102500 -->

- [x] **Step 4:** Verify re-run behavior is present: `grep -c "pending" skills/scope-data-product/SKILL.md` — returns 1+. <!-- sha:9102500 -->

- [x] **Step 5:** Verify Changelog step is present: `grep -c "Changelog" skills/scope-data-product/SKILL.md` — returns 1+. <!-- sha:9102500 -->

- [x] **Step 6:** Commit. <!-- sha:9102500 -->

---

## Chunk 5: implement-source Update

### Task 5: Update implement-source SKILL.md

**Files:**
- Modify: `skills/implement-source/SKILL.md`

**Depends on:** Tasks 1, 2

- [x] **Step 1:** In Preamble Step 2 ("Validate upstream artifact"), after the existing `validate-upstream.py` call, add the `data-product.md` validation: <!-- sha:82b551c -->
  ```bash
  python ${CLAUDE_SKILL_DIR}/scripts/validate-data-product.py <product-name> --require sources
  ```
  If this fails, report the missing section and suggest `/dos:scope-data-product`. Do not proceed until both scripts pass.

- [x] **Step 2:** In Preamble Step 3 ("Read the contract") — change to read ingestion approach, incremental key, and schema context from `data-product.md` Sources and Contract sections. Remove any reference to reading `contract.md` as a standalone file. <!-- sha:82b551c -->

- [x] **Step 3:** In Preamble Step 4 ("Read optional artifacts") — remove `scope.md` and `quality-config.yaml` as standalone artifact paths. Note that if Contract and Quality sections of `data-product.md` are populated, they provide the same context. <!-- sha:82b551c -->

- [x] **Step 4:** In Step 9 ("Update Specification Artifacts") — change to append a Changelog entry to `data-product.md` (noting implement-source invocation, generated file paths, date) instead of updating `contract.md` status fields. <!-- sha:82b551c -->

- [x] **Step 5:** In Step 10 ("Next Steps") — change downstream suggestion from `/dos:review-pipeline` to `/dos:implement-data-product`. <!-- sha:82b551c -->

- [x] **Step 6:** Verify: `wc -l skills/implement-source/SKILL.md` — under 500 lines.
  Verify: `grep -c "validate-data-product.py" skills/implement-source/SKILL.md` — returns 1+.
  Verify: `grep -c "contract\.md" skills/implement-source/SKILL.md` — returns 0. <!-- sha:82b551c -->

- [x] **Step 7:** Commit. <!-- sha:82b551c -->

---

## Chunk 6: implement-data-product

### Task 6: Create implement-data-product skill structure

**Files:**
- Create: `skills/implement-data-product/references/` with 4 files copied from `implement-models/references/`

**Depends on:** Task 2 (scripts directory already created)

- [x] **Step 1:** Create `skills/implement-data-product/references/` and copy all 4 reference files from `skills/implement-models/references/`: contract-enforcement.md, cross-platform-sql.md, dbt-model-patterns.md, dbt-testing-patterns.md. <!-- sha:cca5d3a -->

- [x] **Step 2:** Verify: `ls skills/implement-data-product/references/ | wc -l` — returns 4. <!-- sha:cca5d3a -->

- [x] **Step 3:** Commit. <!-- sha:cca5d3a -->

### Task 7: Write implement-data-product SKILL.md

**Files:**
- Create: `skills/implement-data-product/SKILL.md`

**Depends on:** Tasks 1, 2, 6

Based on `skills/implement-models/SKILL.md` (10-step workflow) with targeted changes:

- **Preamble Step 1**: ask for data product name; path is `docs/data-products/<name>/data-product.md`
- **Preamble Step 2**: run `validate-data-product.py --require contract,quality,architecture` (replaces `validate-upstream.py`). On failure: report missing sections, suggest `/dos:scope-data-product`. Do not proceed.
- **Preamble Steps 3–7**: read Contract, Quality, Architecture sections from `data-product.md` in place of the separate `contract.md`, `quality-config.md`, `pipeline-architecture.md`, `scope.md` files
- **Steps 1–8**: preserve existing model generation workflow (platform detection, staging, intermediate, marts, cross-reference validation, schema YAML, contract enforcement, unit tests) — same logic, same references
- **New Step 9: Generate Orchestration Artifacts** — after code generation:
  - Read Architecture section for `tool::component.identifier` declarations
  - If `dbx::job.<name>` or `dbx::pipeline.<name>` is present: generate Databricks Asset Bundles `databricks.yml` job or DLT pipeline resource block. Refer to Architecture section for schedule, cluster config, task dependencies.
  - If another orchestrator shorthand is present: generate equivalent artifact per the declared tool
  - If no orchestrator is declared in Architecture: note absence, skip without error
- **Step 10 (was Step 9): Update Specification Artifacts** — append a Changelog entry to `data-product.md` (sections updated: Contract+Quality+Architecture, generated file paths, version bump to MINOR); do not update standalone `contract.md` or `quality-config.md` (deprecated)
- **Remove Step 11 (was Step 10)**: Next Steps — remove reference to `review-pipeline`

- [x] **Step 1:** Write the new `skills/implement-data-product/SKILL.md` following this structure. <!-- sha:c54c03a -->

- [x] **Step 2:** Verify: `wc -l skills/implement-data-product/SKILL.md` — under 500 lines.
  Verify: `grep -c "validate-data-product.py" skills/implement-data-product/SKILL.md` — returns 1+.
  Verify: `grep -c "contract,quality,architecture" skills/implement-data-product/SKILL.md` — returns 1+.
  Verify: `grep -c "rchestration" skills/implement-data-product/SKILL.md` — returns 1+. <!-- sha:c54c03a -->

- [x] **Step 3:** Commit. <!-- sha:c54c03a -->

---

## Chunk 7: scope-source

### Task 8: Rename evaluate-source to scope-source

**Files:**
- Rename: `skills/evaluate-source/` → `skills/scope-source/` via `git mv`
- Modify: `skills/scope-source/SKILL.md` (frontmatter `name:` field only)

- [x] **Step 1:** Run `git mv skills/evaluate-source skills/scope-source`. <!-- sha:8f2a82b -->

- [x] **Step 2:** Update frontmatter in `skills/scope-source/SKILL.md`: change `name: evaluate-source` to `name: scope-source`. No other changes to content. <!-- sha:8f2a82b -->

- [x] **Step 3:** Verify: `ls skills/scope-source/SKILL.md` — file exists.
  Verify: `grep "name: scope-source" skills/scope-source/SKILL.md` — matches.
  Verify: `ls skills/evaluate-source/ 2>&1` — "No such file or directory". <!-- sha:8f2a82b -->

- [x] **Step 4:** Commit. <!-- sha:8f2a82b -->

---

## Chunk 8: Deprecations

### Task 9: Mark deprecated skills

**Files:**
- Modify: `skills/define-contract/SKILL.md`
- Modify: `skills/assess-quality/SKILL.md`
- Modify: `skills/design-pipeline/SKILL.md`
- Modify: `skills/select-model/SKILL.md`
- Modify: `skills/review-pipeline/SKILL.md`
- Modify: `skills/implement-models/SKILL.md`

Replacements: define-contract/assess-quality/design-pipeline/select-model → `scope-data-product`; review-pipeline → absorbed into implement skills; implement-models → `implement-data-product`.

- [x] **Step 1:** In each of the 6 SKILL.md files, add `status: deprecated` and `deprecated_by: <replacement-skill>` to the YAML frontmatter. <!-- sha:b9b4929 -->

- [x] **Step 2:** Immediately after the closing `---` of the frontmatter, add a deprecation notice: <!-- sha:b9b4929 -->
  ```
  > **Deprecated.** This skill has been replaced by `/dos:<replacement>`.
  > Reference files are preserved for migration. Do not invoke directly.
  ```

- [x] **Step 3:** Verify: `grep -rl "status: deprecated" skills/` | wc -l` — returns 6. <!-- sha:b9b4929 -->

- [x] **Step 4:** Commit. <!-- sha:b9b4929 -->

---

## Chunk 9: Documentation

### Task 10: Update CLAUDE.md and plans index

**Files:**
- Modify: `CLAUDE.md` (skill chain table and project structure comments)
- Update: `docs/plans/_index.md`

- [x] **Step 1:** Update the skill chain table in `CLAUDE.md`: <!-- sha:5628fb5 -->

  | Phase | Skills | Output Location |
  |-------|--------|-----------------|
  | Discover | `scope-source` | `docs/sources/<source>/` |
  | Scope | `scope-data-product` | `docs/data-products/<name>/data-product.md` |
  | Build | `implement-source` | project codebase |
  | Build | `implement-data-product` | project codebase + orchestration artifacts |

- [x] **Step 2:** Update the project structure comment in `CLAUDE.md` to reflect `docs/data-products/<name>/data-product.md` replacing the 6-file structure. <!-- sha:5628fb5 -->

- [x] **Step 3:** Add this plan to `docs/plans/_index.md`. <!-- sha:5628fb5 (already present) -->

- [x] **Step 4:** Verify: `grep "scope-source" CLAUDE.md` — matches.
  Verify: `grep "implement-data-product" CLAUDE.md` — matches.
  Verify: `grep "pipeline-document-consolidation" docs/plans/_index.md` — matches. <!-- sha:5628fb5 -->

- [x] **Step 5:** Commit. <!-- sha:5628fb5 -->

---

## Validation

- `wc -l skills/scope-data-product/SKILL.md` — under 500 lines
- `wc -l skills/implement-data-product/SKILL.md` — under 500 lines
- `ls skills/scope-data-product/references/ | wc -l` — returns 19
- `ls skills/scope-data-product/assets/` — contains `data-product.md`
- `ls skills/implement-data-product/references/ | wc -l` — returns 4
- `python skills/implement-source/scripts/validate-data-product.py nonexistent --require sources; echo $?` — prints ERROR line, exits 2
- `python skills/implement-data-product/scripts/validate-data-product.py nonexistent --require contract,quality,architecture; echo $?` — exits 2
- `grep -c "status: deprecated" skills/define-contract/SKILL.md skills/assess-quality/SKILL.md skills/design-pipeline/SKILL.md skills/select-model/SKILL.md skills/review-pipeline/SKILL.md skills/implement-models/SKILL.md` — 6 matches total
- `ls skills/scope-source/SKILL.md` — file exists
- `ls skills/evaluate-source/ 2>&1` — "No such file or directory"
- `grep -c "validate-data-product.py" skills/implement-source/SKILL.md` — returns 1+
- `grep -c "validate-data-product.py" skills/implement-data-product/SKILL.md` — returns 1+
- `grep "scope-source\|scope-data-product\|implement-source\|implement-data-product" CLAUDE.md | wc -l` — returns 4+
- `grep -c "<!-- pending:" skills/scope-data-product/assets/data-product.md` — returns 5
