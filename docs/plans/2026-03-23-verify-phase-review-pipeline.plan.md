---
name: Verify Phase — review-pipeline
description: Implement the final Tier 1 skill (dos:review-pipeline) that audits data pipelines against best practices, completing the 9-skill Discover→Scope→Design→Build→Verify chain.
type: plan
status: executing
related:
  - docs/designs/2026-03-23-dos-skill-library-design.md
  - docs/plans/2026-03-23-build-phase-skills.plan.md
  - docs/plans/2026-03-23-scope-design-skills.plan.md
---

# Verify Phase — review-pipeline

**Goal:** Deliver the final Tier 1 skill, `dos:review-pipeline`, which audits existing data pipelines against best practices across five dimensions (observability, validation, CI/CD, SLAs, retry/failure handling). After this plan, all 9 foundational skills are complete — a user can go from source evaluation through scoping, design, implementation, and operational review, with each skill producing artifacts that the next consumes.

**Scope:**

Must have:
- `skills/review-pipeline/` — SKILL.md, 4 references, 1 asset template (review checklist)
- SKILL.md under 500 lines with progressive disclosure to references/
- Follows the Design-phase preamble pattern: ask which data product, check for existing artifacts, adjust workflow
- Review checklist template with YAML frontmatter, findings by severity, and recommendations
- Reviews are append-only — appended to `docs/data-products/<name>/reviews/`, never overwritten
- Artifact-to-implementation gap detection (contract says X, code does Y)
- Graceful degradation when upstream artifacts are absent (the skill audits the pipeline itself, artifacts just enrich the review)
- References inline within workflow steps (not in a separate summary section)

Won't have:
- Automated pipeline scanning scripts — this is an advisory skill, not a code-analysis tool
- Upstream artifact validation scripts — review-pipeline works without any artifacts (graceful degradation), unlike Build-phase skills which require them
- Modifications to existing skills
- Orchestrator-specific review logic (Airflow, Dagster, Prefect)
- Claude Code hook wiring — portable core only

**Approach:** Follow the validated template-first authoring order (asset → references → SKILL.md). review-pipeline is a Design-like skill: it produces a markdown artifact (review checklist), not code. Unlike Build-phase skills, it has no required upstream artifacts — it works by auditing the pipeline directly, with artifacts providing enrichment context. The review checklist template should be authored first since it defines the structure the SKILL.md instructions produce. The 4 reference files are curated from 6 context corpus files per the design's reference table.

**Lessons applied from prior retrospectives:**
- Template-first authoring order (validated across all prior plans)
- Subagent prompts with explicit structural conventions (inline references only)
- Validation criteria include semantic checks (edge case handling, graceful degradation)
- Cross-artifact consistency check (review checklist references match upstream artifact formats)

**File Changes:**

- Create: `skills/review-pipeline/assets/review-checklist.md`
- Create: `skills/review-pipeline/references/observability-pillars.md`
- Create: `skills/review-pipeline/references/validation-audit.md`
- Create: `skills/review-pipeline/references/sla-checklist.md`
- Create: `skills/review-pipeline/references/retry-patterns.md`
- Create: `skills/review-pipeline/SKILL.md`
- Modify: `README.md` (add 1 skill to table)
- Modify: `docs/plans/_index.md` (add this plan)

**Branch:** `feat/verify-phase-review-pipeline`
**PR:** TBD

---

### Task 1: Review checklist asset template

**Files:**
- Create: `skills/review-pipeline/assets/review-checklist.md`

- [x] **Step 1:** Create the review checklist template. Must include: YAML frontmatter (standard artifact fields: `name`, `artifact_type: pipeline-review`, `version`, `owner`, `status`, `last_modified`, plus `review_date` and `data_product` fields), sections for pipeline inventory (orchestrator, transformation tool, validation tools, monitoring), observability assessment (freshness, volume, distribution, schema, lineage), validation assessment (three-tier strategy gaps), CI/CD assessment (pre-commit, PR validation, production deployment with three slim CI blind spots), SLA compliance assessment (CI-time, build-time, runtime enforcement layers with error budget quantification), retry and failure handling assessment (terminal vs transient classification, backoff strategy, dead letter queue), artifact-vs-implementation gaps section, findings summary table (finding, severity, category, recommendation), a "Recommendations" section prioritized by severity, a "Next Steps" section that recommends re-running upstream skills based on findings (e.g., `/dos:define-contract` if contract-vs-code gaps found, `/dos:design-pipeline` if observability gaps found), and a changelog section with a single entry (reviews are append-only, so the changelog will only ever have one entry — included for convention consistency with other artifacts). Review-pipeline is the terminal skill — its next steps loop back to upstream skills rather than introducing new ones.
- [x] **Step 2:** Verify: template contains all sections from the design's review-pipeline workflow (steps 1-10). Contains findings table with severity column. Contains artifact-vs-implementation gap section. Contains "Next Steps" section that recommends upstream skills based on findings (loop-back, not new downstream skills). <!-- sha:d582132 -->
- [x] **Step 3:** Commit <!-- sha:d582132 -->

---

### Task 2: review-pipeline references

**Files:**
- Create: `skills/review-pipeline/references/observability-pillars.md`
- Create: `skills/review-pipeline/references/validation-audit.md`
- Create: `skills/review-pipeline/references/sla-checklist.md`
- Create: `skills/review-pipeline/references/retry-patterns.md`

- [x] **Step 1:** Read `docs/context/data-observability-pillars.md`. Extract into `observability-pillars.md`: the five baseline metrics (freshness, volume, distribution, schema, lineage) with assessment criteria for each, the distinction between observability (infer data health from outputs) and monitoring (watch execution metrics), recommended implementation order (freshness and volume first for highest signal-to-investment ratio), and tool mapping. Target under 100 lines.
- [x] **Step 2:** Read `docs/context/tiered-validation-strategy.md` and `docs/context/ci-cd-pipeline-design.md`. Extract into `validation-audit.md`: three-tier validation strategy with gap detection criteria (what to check at each tier), the three known slim CI blind spots (var()/env_var() false negatives, incremental full-refresh in CI, manifest staleness), and CI/CD tier assessment (pre-commit, PR validation, production deployment). Target under 100 lines.
- [x] **Step 3:** Read `docs/context/data-freshness-slas.md` and `docs/context/data-quality-slas.md`. Extract into `sla-checklist.md`: three-layer enforcement assessment (CI-time breaking change detection, build-time contract enforcement, runtime quality checks), SLA quantification criteria (error budgets vs aspirational), `dbt source freshness` wiring check, and the false confidence warning about metadata-only constraints. Target under 80 lines.
- [x] **Step 4:** Read `docs/context/retry-failure-patterns.md`. Extract into `retry-patterns.md`: failure mode classification (terminal vs transient), retry strategy assessment (exponential backoff with jitter, not fixed-interval), dead letter queue presence, and the dlt-specific flag (no default retry — must use tenacity or equivalent). Target under 80 lines.
- [x] **Step 5:** Verify: `wc -l skills/review-pipeline/references/*.md` — all under 100 lines. 4 files present. <!-- sha:9eb3ba9 -->
- [x] **Step 6:** Commit <!-- sha:9eb3ba9 -->

---

### Task 3: SKILL.md for review-pipeline

**Files:**
- Create: `skills/review-pipeline/SKILL.md`

**Depends on:** Tasks 1, 2

- [x] **Step 1:** Write SKILL.md implementing the 10-step workflow from the design (lines 480-516). Key requirements:
  - **Preamble:** Ask which data product to review. Check for existing artifacts in `docs/data-products/<name>/` (scope, contract, quality config, pipeline architecture). Check for existing reviews in `docs/data-products/<name>/reviews/`. If artifacts exist, load them for context enrichment. If no artifacts exist, proceed by auditing the pipeline directly — ask the user about their pipeline setup. This skill works without any upstream artifacts.
  - **Pipeline inventory:** Ask about or detect: orchestrator, transformation tool (dbt), extraction tool (dlt), validation tools, monitoring setup.
  - **Five assessment dimensions:** Observability (reference `observability-pillars.md` inline), validation (reference `validation-audit.md` inline), CI/CD (reference `validation-audit.md` inline for slim CI blind spots), SLA compliance (reference `sla-checklist.md` inline), retry/failure handling (reference `retry-patterns.md` inline).
  - **Artifact-vs-implementation gap detection:** If artifacts exist, compare what they specify against what the pipeline actually does. Flag discrepancies (e.g., contract specifies column X but model doesn't include it).
  - **Append-only reviews:** Save to `docs/data-products/<name>/reviews/<date>-review.md`. Never overwrite existing reviews.
  - **Terminal skill with loop-back:** Next Steps section recommends re-running upstream skills based on findings (e.g., `/dos:define-contract` if contract-vs-code gaps, `/dos:design-pipeline` if observability gaps). This is loop-back, not new downstream skills — consistent with the design's "informs next iteration" label.
  - **Structural convention:** References inline within workflow steps, never in a separate summary section.
- [x] **Step 2:** Verify: `wc -l skills/review-pipeline/SKILL.md` — under 500 lines. Contains inline references to all 4 reference files and the asset template. Contains preamble that works without upstream artifacts (graceful degradation). Contains all 5 assessment dimensions. Contains artifact-vs-implementation gap detection. Contains append-only review instruction. Does NOT suggest downstream skills in next steps. <!-- sha:5e8089f -->
- [x] **Step 3:** Commit <!-- sha:5e8089f -->

---

### Task 4: Update project documentation

**Files:**
- Modify: `README.md` (add 1 skill to table)
- Modify: `docs/plans/_index.md` (add this plan)

**Depends on:** Task 3

- [x] **Step 1:** Add `dos:review-pipeline` to the README.md skills table with description matching the design document. <!-- sha:2692fab -->
- [x] **Step 2:** Add this plan to `docs/plans/_index.md`. <!-- sha:2692fab -->
- [x] **Step 3:** Verify: `grep -c "dos:" README.md` — shows 10 matches (9 table rows + 1 header). `grep "verify-phase" docs/plans/_index.md` — plan listed. <!-- sha:2692fab -->
- [x] **Step 4:** Commit <!-- sha:2692fab -->

---

## Validation

- [ ] `ls skills/` — shows 9 directories: evaluate-source, scope-data-product, select-model, define-contract, assess-quality, design-pipeline, implement-source, implement-models, review-pipeline
- [ ] `wc -l skills/review-pipeline/SKILL.md` — under 500 lines
- [ ] `head -4 skills/review-pipeline/SKILL.md` — has Agent Skills spec frontmatter with `name` and `description`
- [ ] `ls skills/review-pipeline/references/` — 4 files (observability-pillars, validation-audit, sla-checklist, retry-patterns)
- [ ] `ls skills/review-pipeline/assets/` — 1 file (review-checklist.md)
- [ ] `grep -c "dos:" README.md` — 10 (9 skills + 1 header)
- [ ] **Semantic: Graceful degradation** — SKILL.md contains explicit instructions for when upstream artifacts are absent (audit pipeline directly, ask user about setup, not an error)
- [ ] **Semantic: Append-only reviews** — SKILL.md contains instruction to save to `reviews/<date>-review.md` and never overwrite existing reviews
- [ ] **Semantic: Terminal skill with loop-back** — SKILL.md next steps recommend re-running upstream skills based on findings (loop-back), not new downstream skills
- [ ] **Semantic: Five assessment dimensions** — SKILL.md covers observability, validation, CI/CD, SLA compliance, and retry/failure handling
- [ ] **Semantic: Artifact-vs-implementation gap detection** — SKILL.md contains instructions to compare artifact specifications against actual pipeline code
- [ ] **Semantic: Inline references** — SKILL.md references curated files inline within workflow steps, never in a separate summary section
- [ ] **Semantic: Cross-artifact consistency** — review checklist template's sections align with the assessment dimensions in SKILL.md (1:1 mapping)

## Notes (optional)
