---
name: implement-source Extraction Boundary Guardian
description: Add runtime behavior modeling, mechanical raw-first enforcement, and cost-aware validation to implement-source, consolidating issues #33, #30, #29, #26, #24, #16.
type: plan
status: completed
related:
  - docs/designs/2026-04-08-implement-source-boundary-guardian.design.md
  - skills/implement-source/SKILL.md
---

# implement-source Extraction Boundary Guardian

**Goal:** The `implement-source` skill actively guards the extraction boundary — catching array/merge conflicts, raw-first violations, and cost-blind retry recommendations before generating code. This replaces passive prose guidance with mechanical verification, resolving 6 open issues in a single cohesive change.

**Scope:**

Must have:
- Two new reference files (`extraction-boundary-rules.md`, `dlt-runtime-behaviors.md`)
- Cost-aware retry section in `dlt-pipeline-patterns.md`
- New workflow Step 2: "Verify Extraction Boundary"
- Fixed `validate-upstream.py` invocation with graceful fallback
- Preamble Step 5 expanded with boundary violation scanning
- Old Step 3 ("Flag dlt Configuration Pitfalls") absorbed

Won't have:
- New Python validation scripts
- Changes to other skills
- Changes to asset templates or `auth-config-patterns.md` or `dbt-source-config.md`

**Approach:** Template-first authoring — write the two new reference files first, expand the existing reference, then modify SKILL.md. The new references carry the knowledge (what dlt does at runtime, what raw-first means as checkable rules). SKILL.md changes are structural: a new verification step that references those files, absorption of the redundant pitfalls step, and a script path fix.

**File Changes:**
- Create: `skills/implement-source/references/extraction-boundary-rules.md`
- Create: `skills/implement-source/references/dlt-runtime-behaviors.md`
- Modify: `skills/implement-source/references/dlt-pipeline-patterns.md` (add cost-aware retry section)
- Modify: `skills/implement-source/SKILL.md` (fix script path, expand preamble step 5, add workflow Step 2, enrich Step 3, absorb old Step 3)

**Branch:** `feat/implement-source-boundary-guardian`
**PR:** TBD

---

## Chunk 1: Reference Files

### Task 1: Extraction boundary rules reference

**Files:**
- Create: `skills/implement-source/references/extraction-boundary-rules.md`

- [x] **Step 1:** Create `extraction-boundary-rules.md` covering: raw-first definition, violation patterns to scan for (lambdas with model_dump, schema imports in extract files, enrichment/cross-domain lookups in processing_steps), remediation routing (staging vs intermediate), and cost-of-retry principle (calculate retry cost for quota-billed APIs, flag if >$10).
- [x] **Step 2:** Verify: `wc -l skills/implement-source/references/extraction-boundary-rules.md` — under 200 lines. Verify file contains sections for violation patterns, remediation routing, and cost-of-retry. <!-- 67 lines -->
- [x] **Step 3:** Commit. <!-- sha:0c83c23 -->

---

### Task 2: dlt runtime behaviors reference

**Files:**
- Create: `skills/implement-source/references/dlt-runtime-behaviors.md`

- [x] **Step 1:** Create `dlt-runtime-behaviors.md` covering: array fields creating child tables under merge (with remediation: columns type declaration + JSON serialization), schema caching on field changes (with remediation: cache reset instructions), and cross-reference to nested data divergence in `dlt-pipeline-patterns.md`.
- [x] **Step 2:** Verify: `wc -l skills/implement-source/references/dlt-runtime-behaviors.md` — under 200 lines. Verify file contains sections for array/child tables and schema caching. <!-- 75 lines -->
- [x] **Step 3:** Commit. <!-- sha:3518928 -->

---

### Task 3: Cost-aware retry section in dlt-pipeline-patterns

**Files:**
- Modify: `skills/implement-source/references/dlt-pipeline-patterns.md` (add cost-aware retry section)

- [x] **Step 1:** Add a "Cost-Aware Retry Configuration" section to `dlt-pipeline-patterns.md`. Cover: full-state retry vs idempotent retry distinction, cost calculation formula (`api_calls_per_run × overage_price`), threshold guidance (flag if >$10), and cross-reference to `extraction-boundary-rules.md`.
- [x] **Step 2:** Verify: `wc -l skills/implement-source/references/dlt-pipeline-patterns.md` — under 200 lines. Verify file contains "Cost-Aware Retry" heading. <!-- 101 lines -->
- [x] **Step 3:** Commit. <!-- sha:dba4187 -->

---

## Chunk 2: SKILL.md Modifications

### Task 4: Fix preamble — script path and boundary scanning

**Files:**
- Modify: `skills/implement-source/SKILL.md` (Preamble section)

**Depends on:** Tasks 1, 2

- [x] **Step 1:** In Preamble Step 2, verify the `validate-upstream.py` invocation uses `${CLAUDE_SKILL_DIR}/scripts/validate-upstream.py`. Add a fallback instruction: if the script is not found, fall back to an explicit manual checklist (confirm scorecard exists, has valid frontmatter, contains required sections).
- [x] **Step 2:** In Preamble Step 5 ("Check for existing code"), add: when existing extraction code is found, scan for extraction boundary violations per `extraction-boundary-rules.md` and report findings before asking what's changing.
- [x] **Step 3:** Verify: grep SKILL.md for `${CLAUDE_SKILL_DIR}` in the script invocation. Verify Preamble Step 5 references `extraction-boundary-rules.md`.
- [x] **Step 4:** Commit. <!-- sha:79552a1 -->

---

### Task 5: Restructure workflow — new Step 2, enriched Step 3, absorb old Step 3

**Files:**
- Modify: `skills/implement-source/SKILL.md` (Workflow section)

**Depends on:** Tasks 1, 2, 3, 4

- [x] **Step 1:** Add new Step 2: "Verify Extraction Boundary." Reference `extraction-boundary-rules.md` for raw-first violation scanning and cost-of-retry checks. Reference `dlt-runtime-behaviors.md` for array field detection under merge and schema cache impact assessment. Specify blocking vs advisory finding types.
- [x] **Step 2:** Renumber old Step 2 ("Generate dlt Pipeline") to Step 3. Add inline reference to `dlt-runtime-behaviors.md` for array field handling (columns declaration + JSON serialization) and schema cache reset warning in generated code comments.
- [x] **Step 3:** Remove old Step 3 ("Flag dlt Configuration Pitfalls") entirely. Its 4 pitfalls are already in `dlt-pipeline-patterns.md` "Known Pitfalls" section, which Step 3 (Generate dlt Pipeline) already references.
- [x] **Step 4:** Renumber remaining steps (old 4→4, old 5→5, old 6→6, old 7→7). <!-- Net zero: +1 new step, -1 absorbed step -->
- [x] **Step 5:** Verify: `wc -l skills/implement-source/SKILL.md` — under 500 lines. Verify "Verify Extraction Boundary" heading exists. Verify "Flag dlt Configuration Pitfalls" heading does not exist. Verify Step 3 references `dlt-runtime-behaviors.md`. <!-- 145 lines, all checks pass -->
- [x] **Step 6:** Commit. <!-- sha:b31d327 -->

---

## Validation

- [x] `wc -l skills/implement-source/SKILL.md` — under 500 lines <!-- 145 -->
- [x] `wc -l skills/implement-source/references/extraction-boundary-rules.md` — under 200 lines <!-- 67 -->
- [x] `wc -l skills/implement-source/references/dlt-runtime-behaviors.md` — under 200 lines <!-- 75 -->
- [x] `wc -l skills/implement-source/references/dlt-pipeline-patterns.md` — under 200 lines <!-- 101 -->
- [x] `grep -c "Verify Extraction Boundary" skills/implement-source/SKILL.md` — returns 1+ <!-- 1 -->
- [x] `grep -c "Flag dlt Configuration Pitfalls" skills/implement-source/SKILL.md` — returns 0 <!-- 0 -->
- [x] `grep -c "extraction-boundary-rules.md" skills/implement-source/SKILL.md` — returns 1+ <!-- 4 -->
- [x] `grep -c "dlt-runtime-behaviors.md" skills/implement-source/SKILL.md` — returns 1+ <!-- 4 -->
- [x] `grep -c "CLAUDE_SKILL_DIR" skills/implement-source/SKILL.md` — returns 1+ <!-- 1 -->
- [x] `grep -c "Cost-Aware Retry" skills/implement-source/references/dlt-pipeline-patterns.md` — returns 1+ <!-- 1 -->
