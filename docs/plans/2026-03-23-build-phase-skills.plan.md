---
name: Build Phase Skills
description: Implement 2 Build-phase skills (implement-source, implement-models) that generate code from data product specification artifacts, completing the Discover→Scope→Design→Build chain.
type: plan
status: completed
related:
  - docs/designs/2026-03-23-dos-skill-library-design.md
  - docs/plans/2026-03-23-scope-design-skills.plan.md
  - docs/plans/2026-03-23-foundation-evaluate-source.plan.md
---

# Build Phase Skills

**Goal:** Deliver 2 usable skills covering the Build phase of the data product lifecycle. After this plan, a user can generate dlt pipeline code and dbt source definitions from source evaluations (`dos:implement-source`), and generate dbt models, schema YAMLs, tests, and contract enforcement from data product specifications (`dos:implement-models`). These are the first code-generating skills — they consume the markdown artifacts produced by Discover/Scope/Design skills and translate them into working pipeline code.

**Scope:**

Must have:
- `skills/implement-source/` — SKILL.md, 3 references, 1 upstream validation script
- `skills/implement-models/` — SKILL.md, 4 references, 1 upstream validation script
- All SKILL.md files under 500 lines with progressive disclosure to references/
- All skills follow the Build-phase preamble pattern: read specs → validate upstream artifacts → check existing code → diff-or-generate
- Upstream artifact validation scripts that deterministically check artifact presence, frontmatter validity, and required section completeness before LLM code generation begins
- Iteration bounds enforced in SKILL.md (cap at 3-5 iterations, loop detection)
- Skills update upstream specification artifact status and changelog after code generation
- References inline within workflow steps (not in a separate summary section)
- Each SKILL.md handles the absent-upstream-artifact edge case gracefully (report what's missing, suggest which skill to run)

Won't have:
- `dos:review-pipeline` (Verify phase) — separate plan
- Claude Code hook wiring — portable core only
- Orchestrator integration (no Airflow DAGs, Dagster assets, Prefect flows)
- Streaming pipeline support (batch/incremental only)
- Modifications to existing Discover/Scope/Design phase skills
- Asset templates in assets/ — Build skills produce code in the project codebase, not markdown artifacts
- Prescribed code output directory structure — skills detect project layout (e.g., `dbt_project.yml`) or ask the user for output locations at runtime

**Approach:** Follow a references-then-scripts-then-SKILL.md order, adapted from the template-first pattern validated in prior plans (Build-phase skills have no asset templates, so references serve as the first authoring step). Build-phase skills differ from Design-phase skills: they produce code rather than markdown artifacts, require upstream artifact validation before LLM work, enforce iteration bounds, and update specification artifact status after generation. The two skills are independent — implement-source (EL via dlt) and implement-models (T via dbt) can be built in parallel. Curate references by extracting decision matrices, configuration patterns, and platform-specific pitfalls from the context corpus. Validation scripts implement the design's "Upstream Artifact Validation" requirement as Python scripts (consistent with the existing profile-sample.py precedent) returning exit 0 (pass) or exit 2 (blocking error) with structured error messages.

**Lessons applied from prior retrospectives:**
- Subagent prompts include explicit structural conventions (inline references, no summary sections)
- Validation criteria include semantic checks (edge case handling, cross-artifact consistency) alongside structural checks
- Edge-case-specific validation: verify SKILL.md behavior when upstream artifacts are absent
- Index updates are a sequential post-step, not per-chunk

**File Changes:**

- Create: `skills/implement-source/references/dlt-pipeline-patterns.md`
- Create: `skills/implement-source/references/dbt-source-config.md`
- Create: `skills/implement-source/references/auth-config-patterns.md`
- Create: `skills/implement-source/scripts/validate-upstream.py`
- Create: `skills/implement-source/SKILL.md`
- Create: `skills/implement-models/references/dbt-model-patterns.md`
- Create: `skills/implement-models/references/dbt-testing-patterns.md`
- Create: `skills/implement-models/references/contract-enforcement.md`
- Create: `skills/implement-models/references/cross-platform-sql.md`
- Create: `skills/implement-models/scripts/validate-upstream.py`
- Create: `skills/implement-models/SKILL.md`
- Modify: `README.md` (add 2 skills to table)
- Modify: `docs/plans/_index.md` (add this plan)

**Branch:** `feat/build-phase-skills`
**PR:** TBD

---

## Chunk 1: implement-source

### Task 1: implement-source references

**Files:**
- Create: `skills/implement-source/references/dlt-pipeline-patterns.md`
- Create: `skills/implement-source/references/dbt-source-config.md`
- Create: `skills/implement-source/references/auth-config-patterns.md`

- [x] **Step 1:** Read `docs/context/cdc-mechanisms-tooling.md`, `docs/context/incremental-loading-patterns.md`, and `docs/context/dlt-destination-type-mapping.md`. Extract into `dlt-pipeline-patterns.md`: dlt source/resource definition patterns, write dispositions (replace, append, merge) with risk flags, incremental loading configuration (cursor fields, merge keys), dlt-specific pitfalls (bug #2782, silent env var failures, silent destination fallback, nested data divergence at `max_table_nesting=0`), and the CDC boundary — dlt is polling-only, recommend Debezium for log-based CDC. Target under 120 lines. Convention: decision tables and code snippets, no explanatory prose. <!-- sha:b419409 -->
- [x] **Step 2:** Read `docs/context/data-freshness-slas.md` and `docs/context/ci-cd-pipeline-design.md`. Extract into `dbt-source-config.md`: dbt source YAML structure (source, table, column definitions), `loaded_at_field` and freshness threshold configuration, the reminder that `dbt source freshness` must be wired as a separate orchestrator step (not included in `dbt build`), and column definition patterns from contract schema. Target under 80 lines. <!-- sha:b419409 -->
- [x] **Step 3:** Read `docs/context/secrets-environment-management.md` and `docs/context/secrets-management-rotation.md`. Extract into `auth-config-patterns.md`: auth mechanism patterns by source type (OAuth M2M, API key, service account, key-pair, JDBC credentials), credential management assessment criteria (where secrets live, rotation cadence, anti-patterns), and dlt config/secrets separation guidance (config.toml vs secrets.toml vs env vars). Target under 80 lines. <!-- sha:b419409 -->
- [x] **Step 4:** Verify: `wc -l skills/implement-source/references/*.md` — all under 120 lines. 3 files present. Each file contains decision tables or configuration snippets, not explanatory prose. <!-- sha:b419409 -->
- [x] **Step 5:** Commit <!-- sha:b419409 -->

---

### Task 2: implement-source upstream validation script

**Files:**
- Create: `skills/implement-source/scripts/validate-upstream.py`

**Depends on:** None (independent of Task 1)

- [x] **Step 1:** Create `validate-upstream.py` that accepts a source name as argument and validates: (a) `docs/sources/<source>/evaluation.md` exists, (b) file has valid YAML frontmatter between `---` delimiters, (c) frontmatter contains required fields: `name`, `artifact_type`, `version`, `status`, (d) body contains required sections for code generation: source type/classification, auth mechanism, ingestion approach. Exit 0 on success. Exit 2 on failure with structured error message: location (file path + missing field/section), expected content, and which skill to run to fix it (e.g., "Run dos:evaluate-source to create the missing scorecard"). Python stdlib only, no external dependencies. <!-- sha:9f47876 -->
- [x] **Step 2:** Verify: `python skills/implement-source/scripts/validate-upstream.py nonexistent-source` — exits with code 2 and error message mentioning `dos:evaluate-source`. `wc -l skills/implement-source/scripts/validate-upstream.py` — under 100 lines. <!-- sha:9f47876 -->
- [x] **Step 3:** Commit <!-- sha:9f47876 -->

---

### Task 3: SKILL.md for implement-source

**Files:**
- Create: `skills/implement-source/SKILL.md`

**Depends on:** Tasks 1, 2

- [x] **Step 1:** Write SKILL.md implementing the 10-step workflow from the design (lines 398-427). Key requirements:
  - **Preamble:** Ask which source to implement. This skill implements one source at a time. Check for existing evaluation scorecard in `docs/sources/<source>/evaluation.md`. Run `scripts/validate-upstream.py` before proceeding. If validation fails, report what's missing and suggest `dos:evaluate-source`.
  - **Optional input detection:** After identifying the source, ask which data product this source is for (if any). If a data product is named, check for `docs/data-products/<name>/pipeline-architecture.md` and `docs/data-products/<name>/contract.md` — report availability and pre-populate from them if present. This is handled in the preamble, not the validation script, because the source-to-data-product mapping is a runtime question.
  - **Build-phase pattern:** Check if dlt pipeline code already exists for this source. If code exists, diff specification artifacts against current code and propose updates. If no code exists, generate from specifications.
  - **CDC boundary:** dlt is polling-only. If scorecard recommends CDC, guide user to Debezium or platform-native CDC instead. Explicitly state dlt is appropriate for API extraction, file-based sources, and database polling with cursor-based incremental loading.
  - **dlt pitfalls:** Surface bug #2782, silent env var failures, silent destination fallback, and nested data divergence. Reference `dlt-pipeline-patterns.md` inline at the relevant workflow step.
  - **dbt source generation:** Generate source YAML with `loaded_at_field`, freshness thresholds, and column definitions. Reference `dbt-source-config.md` inline. Remind user about `dbt source freshness` wiring.
  - **Iteration bounds:** Cap at 3-5 iterations if generated code fails validation. Loop detection: if 3 consecutive iterations produce >90% similar output, stop and explain.
  - **Traceability:** After code generation, update source evaluation scorecard status and add generated file paths to changelog.
  - **Next steps:** Suggest `dos:implement-models` and `dos:review-pipeline`.
  - **Structural convention:** References inline within workflow steps, never in a separate summary section. <!-- sha:666dffb -->
- [x] **Step 2:** Verify: `wc -l skills/implement-source/SKILL.md` — under 500 lines. Contains inline references to all 3 reference files. Contains `validate-upstream.py` invocation in preamble. Contains CDC boundary guidance. Contains iteration bounds. Contains instruction to update upstream artifact status. Contains graceful handling when scorecard is absent (error message + suggestion to run evaluate-source). <!-- sha:666dffb -->
- [x] **Step 3:** Commit <!-- sha:666dffb -->

---

## Chunk 2: implement-models

### Task 4: implement-models references

**Files:**
- Create: `skills/implement-models/references/dbt-model-patterns.md`
- Create: `skills/implement-models/references/dbt-testing-patterns.md`
- Create: `skills/implement-models/references/contract-enforcement.md`
- Create: `skills/implement-models/references/cross-platform-sql.md`

- [x] **Step 1:** Read `docs/context/kimball-dimensional-modeling.md`, `docs/context/medallion-architecture.md`, and `docs/context/obt-wide-table-patterns.md`. Extract into `dbt-model-patterns.md`: model generation by layer (staging → intermediate → marts), materialization selection per layer, naming conventions, one-model-per-source-table rule for staging, and modeling approach patterns (star schema facts/dims, wide tables, entity-centric). Target under 120 lines. <!-- sha:40b95de -->
- [x] **Step 2:** Read `docs/context/tiered-validation-strategy.md` and `docs/context/data-validation-tool-comparison.md`. Extract into `dbt-testing-patterns.md`: generic test mapping from quality dimensions (not_null, unique, accepted_values, relationships), dbt-expectations tests for distribution/range checks, dbt unit test patterns (v1.8+), and three-tier validation strategy (local Pandera+pytest, CI dbt tests, production Soda/GE). Target under 100 lines. <!-- sha:40b95de -->
- [x] **Step 3:** Read `docs/context/data-contract-structure.md` and `docs/context/data-contract-enforcement-versioning.md`. Extract into `contract-enforcement.md`: `contract: { enforced: true }` configuration, column definition patterns from contract schema, the false confidence warning (DuckDB enforces constraints but Snowflake/Databricks treat most as metadata-only), and the rule to add explicit dbt tests for every constraint the production warehouse does not enforce. Target under 80 lines. <!-- sha:40b95de -->
- [x] **Step 4:** Read `docs/context/dbt-adapter-dialect-gaps.md` and `docs/context/cross-platform-portability-strategy.md`. Extract into `cross-platform-sql.md`: the 38 cross-database macros and their zero coverage for JSON path extraction/regex/array flattening, ClickHouse-specific incompatibilities (no merge incremental, no Python models, CTE+INSERT failure, ReplicatedMergeTree dedup), semi-structured data handling requirements (dispatch shim implementations), and platform detection guidance. Target under 100 lines. <!-- sha:40b95de -->
- [x] **Step 5:** Verify: `wc -l skills/implement-models/references/*.md` — all under 120 lines. 4 files present. Each file contains decision tables, configuration snippets, or compatibility matrices, not explanatory prose. <!-- sha:40b95de -->
- [x] **Step 6:** Commit <!-- sha:40b95de -->

---

### Task 5: implement-models upstream validation script

**Files:**
- Create: `skills/implement-models/scripts/validate-upstream.py`

**Depends on:** None (independent of Task 4)

- [x] **Step 1:** Create `validate-upstream.py` that accepts a data product name as argument and validates: (a) `docs/data-products/<name>/contract.md` exists (required — contract is the primary input), (b) file has valid YAML frontmatter, (c) frontmatter contains required fields: `name`, `artifact_type`, `version`, `status`, (d) body contains a schema section with at least one object/property definition (cannot generate models without schema). Optionally check for quality config and pipeline architecture (report as "available" or "not found — will skip enrichment"). Exit 0 on success. Exit 2 on failure with structured error: location, expected content, and which skill to run (e.g., "Run dos:define-contract to create the contract"). Python stdlib only, no external dependencies. <!-- sha:ce0a183 -->
- [x] **Step 2:** Verify: `python skills/implement-models/scripts/validate-upstream.py nonexistent-product` — exits with code 2 and error message mentioning `dos:define-contract`. `wc -l skills/implement-models/scripts/validate-upstream.py` — under 100 lines. <!-- sha:ce0a183 -->
- [x] **Step 3:** Commit <!-- sha:ce0a183 -->

---

### Task 6: SKILL.md for implement-models

**Files:**
- Create: `skills/implement-models/SKILL.md`

**Depends on:** Tasks 4, 5

- [x] **Step 1:** Write SKILL.md implementing the 11-step workflow from the design (lines 439-467). Key requirements:
  - **Preamble:** Ask which data product to implement. Check for existing contract in `docs/data-products/<name>/contract.md`. Run `scripts/validate-upstream.py` before proceeding. If validation fails, report what's missing and suggest `dos:define-contract`. Also check for quality config, pipeline architecture, and scope (optional enrichment inputs).
  - **Build-phase pattern:** Check if dbt models already exist for this data product. If models exist, diff contract/quality config against current code and propose updates to align. If no models exist, generate from specifications.
  - **Platform detection:** Before generating code, detect target platform and flag incompatibilities. Reference `cross-platform-sql.md` inline. ClickHouse: no merge incremental, no Python models, CTEs fail with INSERT, ReplicatedMergeTree dedup. Semi-structured data: require dispatch shim implementations before proceeding.
  - **Layer-by-layer generation:** Staging (rename, cast, view/ephemeral, one per source table) → Intermediate (joins, enrichments, table/incremental) → Marts (consumer-facing, contract enforcement enabled). Reference `dbt-model-patterns.md` inline at this step.
  - **Schema YAML generation:** Column definitions from contract, `contract: { enforced: true }` on marts, generic tests from quality config, dbt-expectations tests for distribution checks. Reference `dbt-testing-patterns.md` inline.
  - **Contract enforcement warning:** DuckDB enforces all constraints at build time but Snowflake/Databricks treat most as metadata-only. Add explicit dbt tests for every constraint the production warehouse does not enforce. Reference `contract-enforcement.md` inline.
  - **Unit tests:** Generate dbt unit tests (v1.8+) for critical transformation logic.
  - **Iteration bounds:** Cap at 3-5 iterations. Loop detection at >90% similarity across 3 consecutive attempts.
  - **Traceability:** After code generation, update contract and quality config status to reflect implementation state and note generated file paths in changelog.
  - **Next steps:** Suggest `dos:review-pipeline`.
  - **Structural convention:** References inline within workflow steps, never in a separate summary section. <!-- sha:95a87f3 -->
- [x] **Step 2:** Verify: `wc -l skills/implement-models/SKILL.md` — under 500 lines. Contains inline references to all 4 reference files. Contains `validate-upstream.py` invocation in preamble. Contains platform detection with ClickHouse and semi-structured data flags. Contains layer-by-layer generation pattern. Contains contract enforcement false confidence warning. Contains iteration bounds. Contains instruction to update upstream artifact status. Contains graceful handling when contract is absent. <!-- sha:95a87f3 -->
- [x] **Step 3:** Commit <!-- sha:95a87f3 -->

---

## Chunk 3: Integration

### Task 7: Update project documentation

**Files:**
- Modify: `README.md` (add 2 skills to table)
- Modify: `docs/plans/_index.md` (add this plan)

**Depends on:** Tasks 3, 6

- [x] **Step 1:** Add `dos:implement-source` and `dos:implement-models` to the README.md skills table with descriptions matching the design document. <!-- sha:a2607cf -->
- [x] **Step 2:** Add this plan to `docs/plans/_index.md`. <!-- sha:a2607cf -->
- [x] **Step 3:** Verify: `grep -c "dos:" README.md` — shows 9 matches (8 table rows + 1 header). `grep "build-phase" docs/plans/_index.md` — plan listed. <!-- sha:a2607cf -->
- [x] **Step 4:** Commit <!-- sha:a2607cf -->

---

## Validation

- [ ] `ls skills/` — shows 8 directories: evaluate-source, scope-data-product, select-model, define-contract, assess-quality, design-pipeline, implement-source, implement-models
- [ ] `for d in implement-source implement-models; do wc -l skills/$d/SKILL.md; done` — both under 500 lines
- [ ] `for d in implement-source implement-models; do head -4 skills/$d/SKILL.md; done` — both have Agent Skills spec frontmatter with `name` and `description`
- [ ] `ls skills/implement-source/references/` — 3 files (dlt-pipeline-patterns, dbt-source-config, auth-config-patterns)
- [ ] `ls skills/implement-models/references/` — 4 files (dbt-model-patterns, dbt-testing-patterns, contract-enforcement, cross-platform-sql)
- [ ] `ls skills/implement-source/scripts/` — validate-upstream.py present
- [ ] `ls skills/implement-models/scripts/` — validate-upstream.py present
- [ ] `python skills/implement-source/scripts/validate-upstream.py nonexistent` — exits 2 with error referencing dos:evaluate-source
- [ ] `python skills/implement-models/scripts/validate-upstream.py nonexistent` — exits 2 with error referencing dos:define-contract
- [ ] **Semantic: Edge case handling** — both SKILL.md files contain explicit instructions for when upstream artifacts are absent (graceful error with skill suggestion, not a crash or silent skip)
- [ ] **Semantic: Build-phase pattern** — both SKILL.md files contain the check-for-existing-code pattern (diff-and-update vs generate-from-scratch)
- [ ] **Semantic: Iteration bounds** — both SKILL.md files contain 3-5 iteration cap and >90% similarity loop detection
- [ ] **Semantic: Traceability** — both SKILL.md files contain instructions to update upstream artifact status and changelog after code generation
- [ ] **Semantic: Inline references** — both SKILL.md files reference curated files inline within workflow steps, never in a separate summary section
- [ ] **Semantic: Cross-skill consistency** — verify that implement-source and implement-models SKILL.md files use consistent terminology for dbt source references (implement-source generates source definitions; implement-models references those sources via `{{ source() }}` in staging models)
- [ ] `grep -c "dos:" README.md` — 8 skills listed

## Notes (optional)
