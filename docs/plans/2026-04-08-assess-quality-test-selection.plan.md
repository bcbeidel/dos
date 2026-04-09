---
name: assess-quality dbt Test Selection Reference
description: Add rule-type-to-dbt-test mapping reference to assess-quality, fixing wrong test suggestions (#31) and missing run-over-run patterns (#15).
type: plan
status: executing
related:
  - docs/designs/assess-quality-test-selection-brainstorm.md
  - docs/research/2026-04-08-dbt-test-selection-patterns.research.md
---

# assess-quality dbt Test Selection Reference

**Goal:** When assess-quality defines a quality rule, it selects the correct dbt test implementation based on rule type (pattern, range, enum, stateful) rather than quality dimension name. This eliminates wrong test suggestions (#31) and provides concrete implementation patterns for run-over-run consistency checks (#15).

**Scope:**

Must have:
- New reference file mapping 15+ stateless rule types and 4 stateful rule types to their correct dbt tests
- Singular test patterns for run-over-run checks (seed-based and snapshot-based)
- SKILL.md wired to use the reference in Steps 4 and 8
- Quality config template updated with a Rule Type column
- Issues #31 and #15 closeable after merge

Won't have:
- Changes to `implement-models` references (follow-up; it already has `dbt-testing-patterns.md` which can be updated separately)
- Elementary package integration guidance (documented in research, but assess-quality is a design skill, not a build skill)
- Changes to any existing quality-config artifacts in `docs/data-products/`

**Approach:** Create a single reference file (`dbt-test-selection.md`) organized as decision tables mapping rule types to dbt tests, with a separate section for stateful implementation patterns. Wire it into SKILL.md at the two points where test selection occurs (measurement method definition and tooling recommendation). Add a Rule Type column to the template so downstream skills can read the classification.

**File Changes:**
- Create: `skills/assess-quality/references/dbt-test-selection.md`
- Modify: `skills/assess-quality/SKILL.md` (add reference link, add rule-type guidance to Steps 4 and 8)
- Modify: `skills/assess-quality/assets/quality-config-template.md` (add Rule Type column to dimensions table)

**Branch:** `feat/31-15-assess-quality-test-selection`
**PR:** TBD

---

### Task 1: Create dbt-test-selection.md reference

**Files:**
- Create: `skills/assess-quality/references/dbt-test-selection.md`

- [ ] **Step 1:** Create the reference file with three sections: (1) Rule Type Taxonomy table listing all stateless and stateful rule types with descriptions and examples, (2) Stateless Rule Mapping table mapping each rule type to its dbt test, package, and config example, (3) Stateful Rule Mapping section with two concrete singular test SQL patterns (seed-based baselines and snapshot-based baselines) and a recommendation ladder by team size. Source content from the brainstorm design doc's "Rule Type to dbt Test Mapping" tables and the research doc's "Rule Type to Test Implementation Mapping" section. End with 5 decision rules. Keep under 200 lines per project convention.
- [ ] **Step 2:** Verify: `wc -l skills/assess-quality/references/dbt-test-selection.md` returns under 200. Verify file contains all three sections: "Rule Type Taxonomy", "Stateless Rule Mapping", "Stateful Rule Mapping".
- [ ] **Step 3:** Commit: `feat(assess-quality): add dbt-test-selection reference (#31, #15)`

---

### Task 2: Wire reference into SKILL.md

**Files:**
- Modify: `skills/assess-quality/SKILL.md` (Reference Materials section, Step 4, Step 8)

**Depends on:** Task 1

- [ ] **Step 1:** Add `dbt-test-selection.md` to the Reference Materials list in the Preamble section. Add rule-type classification guidance to Step 4 (after threshold calibration guidance): instruct the skill to classify each measurement method into a rule type using the reference, and flag stateful rules as requiring singular tests. Add test-selection-by-rule-type guidance to Step 8 (after scaling guidance): instruct the skill to use the rule-type mapping rather than dimension names when recommending specific dbt tests.
- [ ] **Step 2:** Verify: `wc -l skills/assess-quality/SKILL.md` returns under 500 (skill line limit). Verify: `grep -c 'dbt-test-selection.md' skills/assess-quality/SKILL.md` returns 3 (reference list + Step 4 + Step 8).
- [ ] **Step 3:** Commit: `feat(assess-quality): wire dbt-test-selection into SKILL.md steps 4 and 8`

---

### Task 3: Add Rule Type column to quality config template

**Files:**
- Modify: `skills/assess-quality/assets/quality-config-template.md`

**Depends on:** Task 1

- [ ] **Step 1:** Add a `Rule Type` column to the Quality Dimensions table (between Dimension and Measurement Method). Update the table header row, separator row, and all example rows. Add a note below the table explaining that rule types come from the taxonomy in `dbt-test-selection.md` and are used by downstream skills to select the correct dbt test. Update the consistency row's measurement method to distinguish referential-integrity from metric-stability rule types.
- [ ] **Step 2:** Verify: `grep 'Rule Type' skills/assess-quality/assets/quality-config-template.md` returns the header row. Verify template still renders valid markdown.
- [ ] **Step 3:** Commit: `feat(assess-quality): add rule type column to quality config template`

---

### Task 4: Close issues and update indexes

**Depends on:** Tasks 1, 2, 3

- [ ] **Step 1:** Update `docs/plans/_index.md` with this plan entry.
- [ ] **Step 2:** Verify all changes are committed and the branch is clean: `git status` shows clean working tree.
- [ ] **Step 3:** Commit any remaining index updates.

---

## Validation

- [ ] `wc -l skills/assess-quality/references/dbt-test-selection.md` -- under 200 lines
- [ ] `wc -l skills/assess-quality/SKILL.md` -- under 500 lines
- [ ] `grep 'expression_is_true' skills/assess-quality/references/dbt-test-selection.md` -- string-pattern rule maps to expression_is_true, not not_accepted_values (the #31 fix)
- [ ] `grep 'metric-stability' skills/assess-quality/references/dbt-test-selection.md` -- stateful rule type exists with singular test pattern (the #15 fix)
- [ ] `grep 'Rule Type' skills/assess-quality/assets/quality-config-template.md` -- template includes rule type column
- [ ] `grep -c 'dbt-test-selection.md' skills/assess-quality/SKILL.md` -- returns 3 (referenced in 3 places)
