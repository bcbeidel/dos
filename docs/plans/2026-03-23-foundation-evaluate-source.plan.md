---
name: Foundation + dos:evaluate-source
description: Scaffold the skill architecture and implement the first skill end-to-end, validating directory conventions, SKILL.md constraints, reference curation, artifact templates, and the scripts/ pattern.
type: plan
status: executing
related:
  - docs/designs/2026-03-23-dos-skill-library-design.md
---

# Foundation + dos:evaluate-source

**Goal:** Deliver the first usable skill (`/dos:evaluate-source`) with the full skill architecture in place — directory structure, artifact templates, curated references, and validation scripts. This skill is the entry point to the data product workflow and exercises every architectural pattern from the design. Implementing it first surfaces constraint violations (500-line SKILL.md limit, reference curation approach, artifact format) before committing to 8 more skills.

**Scope:**

Must have:
- `skills/dos-evaluate-source/SKILL.md` under 500 lines, following Agent Skills spec with Claude Code extensions
- `skills/dos-evaluate-source/references/` with 4 curated reference files distilled from context corpus
- `skills/dos-evaluate-source/assets/source-scorecard.md` artifact template
- `skills/dos-evaluate-source/scripts/profile-sample.py` profiling script
- `docs/data-products/` directory with conventions documented
- Skill invocable as `/dos:evaluate-source` via the plugin
- Artifact output matches the design's frontmatter and changelog conventions

Won't have:
- Any other skills (scope-data-product, define-contract, etc.) — those are Plan 2 and Plan 3
- Shared `.claude/hooks/` validation scripts — defer until multiple skills need shared checks
- Claude Code hook wiring in SKILL.md frontmatter — get the portable core working first
- Integration with any external tools (dlt, dbt, databases) — this skill is advisory, not code-generating
- Automated testing framework — verify manually and via line counts for now

**Approach:** Work artifact-template-first as the design recommends: define the source scorecard template before writing SKILL.md instructions, since the template defines the structure the skill reads and writes. Distill context files into focused reference files extracting only decision matrices, criteria tables, and checklists — no explanatory prose. Write SKILL.md last, referencing the template and references. The profiling script is a standalone Python tool (stdlib + DuckDB) that produces structured markdown tables. Validate the 500-line constraint empirically and document findings.

**File Changes:**

- Create: `docs/data-products/_index.md` (artifact directory conventions)
- Create: `skills/dos-evaluate-source/assets/source-scorecard.md` (artifact template)
- Create: `skills/dos-evaluate-source/references/six-dimension-framework.md`
- Create: `skills/dos-evaluate-source/references/source-classification-matrix.md`
- Create: `skills/dos-evaluate-source/references/access-auth-patterns.md`
- Create: `skills/dos-evaluate-source/references/profiling-metrics.md`
- Create: `skills/dos-evaluate-source/scripts/profile-sample.py`
- Create: `skills/dos-evaluate-source/SKILL.md`
- Modify: `docs/plans/_index.md` (add this plan)
- Modify: `README.md` (add evaluate-source to skills table)

**Branch:** `feat/dos-skill-library-design` (current branch)
**PR:** TBD

---

## Chunk 1: Artifact Foundation

### Task 1: Data product directory conventions

**Files:**
- Create: `docs/data-products/_index.md`

- [x] **Step 1:** Create `docs/data-products/_index.md` documenting the artifact directory conventions from the design: directory-per-data-product structure, frontmatter schema (`name`, `artifact_type`, `version`, `owner`, `status`, `last_modified`), changelog convention, and the list of artifact types (`source-evaluation`, `scope`, `contract`, `quality-config`, `pipeline-architecture`, `reviews/`). This file serves as the reference for all skills that create or update artifacts. <!-- sha:8b42d28 -->
- [x] **Step 2:** Verify: `test -f docs/data-products/_index.md && head -5 docs/data-products/_index.md` — file exists and starts with YAML frontmatter or markdown header. <!-- sha:8b42d28 -->
- [x] **Step 3:** Commit: "docs: add data product artifact directory conventions" <!-- sha:8b42d28 -->

---

### Task 2: Source scorecard artifact template

**Files:**
- Create: `skills/dos-evaluate-source/assets/source-scorecard.md`

**Depends on:** Task 1

- [x] **Step 1:** Create the source scorecard template in `skills/dos-evaluate-source/assets/source-scorecard.md`. The template must include: YAML frontmatter (with all required artifact fields), sections for source metadata (type, ownership, format, location), source classification, six-dimension scoring table (connectivity, volume, freshness, schema stability, data quality, access complexity), authentication mechanism, credential management assessment, profiling results (structure, content, relationship subsections), ingestion recommendation, re-profiling cadence, and a "Next Steps" section pointing to `dos:scope-data-product`. Use placeholder values (e.g., `{{name}}`, `[score: 1-5]`) where skills will fill in data. <!-- sha:0794f7e -->
- [x] **Step 2:** Verify: the template contains all sections from the design's evaluate-source workflow (steps 2-10). Check for: six-dimension scoring table, profiling subsections (structure, content, relationship), ingestion recommendation, and "Next Steps" mentioning `dos:scope-data-product`. <!-- sha:0794f7e -->
- [x] **Step 3:** Commit: "feat: add source scorecard artifact template" <!-- sha:0794f7e -->

---

## Chunk 2: Curated References

### Task 3: Six-dimension framework reference

**Files:**
- Create: `skills/dos-evaluate-source/references/six-dimension-framework.md`

- [x] **Step 1:** Read `docs/context/source-system-evaluation.md` and `docs/context/schema-drift-risk.md`. Extract the six-dimension assessment framework (connectivity, volume, freshness, schema stability, data quality, access complexity) into a focused reference file. Include: dimension definitions, scoring criteria (what makes a 1 vs 5), and the key finding that schema drift causes 7.8% of quality incidents with 27% compounding. Format as tables and criteria lists — no explanatory prose. Target under 200 lines. <!-- sha:04715af -->
- [x] **Step 2:** Verify: `wc -l skills/dos-evaluate-source/references/six-dimension-framework.md` — under 200 lines (actual: 97 lines). File contains a scoring table with all six dimensions. <!-- sha:04715af -->
- [x] **Step 3:** Commit: "feat: add six-dimension framework reference for evaluate-source" <!-- sha:04715af -->

---

### Task 4: Source classification matrix reference

**Files:**
- Create: `skills/dos-evaluate-source/references/source-classification-matrix.md`

- [x] **Step 1:** Read `docs/context/source-system-evaluation.md` and `docs/context/incremental-loading-patterns.md`. Extract the source classification matrix (transactional DB, event stream, SaaS API, file-based) and map each type to: typical ingestion approaches, incremental strategy fit, and silent failure modes. Include the key finding that dlt is a polling tool (not CDC) — if log-based CDC is needed, recommend Debezium. Format as a decision matrix table. Target under 150 lines. <!-- sha:b7d7650 -->
- [x] **Step 2:** Verify: `wc -l skills/dos-evaluate-source/references/source-classification-matrix.md` — under 150 lines (actual: 59 lines). File contains a classification table with at least 4 source types. <!-- sha:b7d7650 -->
- [x] **Step 3:** Commit: "feat: add source classification matrix reference for evaluate-source" <!-- sha:b7d7650 -->

---

### Task 5: Access and auth patterns reference

**Files:**
- Create: `skills/dos-evaluate-source/references/access-auth-patterns.md`

- [x] **Step 1:** Read `docs/context/secrets-management-rotation.md` and `docs/context/secrets-environment-management.md`. Extract authentication mechanism inventory (OAuth M2M, API key, service account, key-pair, JDBC credentials), credential management anti-patterns (static PATs, shared credentials), and rotation cadence guidance. Include the key finding that service principals with OAuth M2M (1h tokens) are the production auth standard. Format as a checklist and comparison table. Target under 150 lines. <!-- sha:b7425d4 -->
- [x] **Step 2:** Verify: `wc -l skills/dos-evaluate-source/references/access-auth-patterns.md` — under 150 lines (actual: 55 lines). File lists at least 5 auth mechanisms. <!-- sha:b7425d4 -->
- [x] **Step 3:** Commit: "feat: add access and auth patterns reference for evaluate-source" <!-- sha:b7425d4 -->

---

### Task 6: Profiling metrics reference

**Files:**
- Create: `skills/dos-evaluate-source/references/profiling-metrics.md`

- [x] **Step 1:** Read `docs/context/data-profiling.md`. Extract the three profiling types (structure, content, relationship) with their specific metrics: structure (column names, types, field lengths, naming consistency), content (null rates, distinct counts, uniqueness ratios, min/max, distributions, pattern frequencies), relationship (key candidates, referential integrity, orphan detection). Include mapping from profiling results to quality dimension baselines. Format as structured metric lists per profiling type. Target under 150 lines. <!-- sha:8f5c7a5 -->
- [x] **Step 2:** Verify: `wc -l skills/dos-evaluate-source/references/profiling-metrics.md` — under 150 lines (actual: 72 lines). File contains all three profiling types with their metrics listed. <!-- sha:8f5c7a5 -->
- [x] **Step 3:** Commit: "feat: add profiling metrics reference for evaluate-source" <!-- sha:8f5c7a5 -->

---

## Chunk 3: Profiling Script

### Task 7: Sample profiling script

**Files:**
- Create: `skills/dos-evaluate-source/scripts/profile-sample.py`

- [x] **Step 1:** Create `profile-sample.py` that accepts a file path (CSV, JSON, or Parquet) via command-line argument and computes core profiling metrics. Use Python stdlib for CSV/JSON and DuckDB for Parquet and heavier computation. Output structured markdown tables covering: column inventory (name, inferred type, nullable), content metrics per column (null count, null rate, distinct count, uniqueness ratio, min, max), and summary statistics (row count, column count). The script should exit 0 on success and print to stdout. Include a `--help` flag documenting usage. <!-- sha:f89e230 -->
- [x] **Step 2:** Verify: `python3 skills/dos-evaluate-source/scripts/profile-sample.py --help` — exits 0 and prints usage information. <!-- sha:f89e230 -->
- [x] **Step 3:** Create a small test CSV and verify — outputs markdown tables with column metrics showing null rates (33.3%) for `name` and `value` columns, identifies `id` as key candidate. <!-- sha:f89e230 -->
- [x] **Step 4:** Commit: "feat: add sample profiling script for evaluate-source" <!-- sha:f89e230 -->

---

## Chunk 4: SKILL.md

### Task 8: SKILL.md for dos:evaluate-source

**Files:**
- Create: `skills/dos-evaluate-source/SKILL.md`

**Depends on:** Tasks 2, 3, 4, 5, 6, 7

- [x] **Step 1:** Write `skills/dos-evaluate-source/SKILL.md` implementing the full evaluate-source workflow from the design (steps 1-10). The file must: use only base Agent Skills spec fields in frontmatter (`name`, `description`) for portability; start with a preamble check (ask which data product, check for existing artifacts in `docs/data-products/<name>/`); reference the 4 curated files via relative markdown links for progressive disclosure; reference the asset template for output structure; reference the profiling script for sample data analysis; end output with "Next Steps" suggesting `dos:scope-data-product`. Follow the 10-step workflow exactly as specified in the design. <!-- sha:0210462 -->
- [x] **Step 2:** Verify: `wc -l skills/dos-evaluate-source/SKILL.md` — 162 lines, well under 500-line budget (338 lines headroom). <!-- sha:0210462 -->
- [x] **Step 3:** Verify content: SKILL.md references all 4 reference files, the asset template, and the profiling script. Contains preamble check, intake filtering questions, and "Next Steps" section. <!-- sha:0210462 -->
- [x] **Step 4:** Commit: "feat: add SKILL.md for dos:evaluate-source" <!-- sha:0210462 -->

---

## Chunk 5: Integration and Documentation

### Task 9: Update project documentation

**Files:**
- Modify: `README.md` (add evaluate-source to skills table)
- Modify: `docs/plans/_index.md` (add this plan)

- [x] **Step 1:** Update `README.md` skills table to list `dos:evaluate-source` with its description: "Assess a data source's technical characteristics before pipeline construction." <!-- sha:b1b6e17 -->
- [x] **Step 2:** Update `docs/plans/_index.md` to include this plan file. <!-- sha:b1b6e17 -->
- [x] **Step 3:** Verify: `grep "evaluate-source" README.md` — shows the skill in the table. <!-- sha:b1b6e17 -->
- [x] **Step 4:** Commit: "docs: add evaluate-source to README and plan index" <!-- sha:b1b6e17 -->

---

### Task 10: Architecture validation and findings

- [x] **Step 1:** Record findings from the implementation in a `## Notes` section appended to this plan file. See Notes section below.
- [x] **Step 2:** Findings documented with specific recommendations. No design doc changes required — all constraints validated successfully.
- [x] **Step 3:** Commit: "docs: record architecture validation findings from evaluate-source"

---

## Validation

- [ ] `wc -l skills/dos-evaluate-source/SKILL.md` — under 500 lines
- [ ] `ls skills/dos-evaluate-source/references/` — shows 4 reference files (six-dimension-framework.md, source-classification-matrix.md, access-auth-patterns.md, profiling-metrics.md)
- [ ] `ls skills/dos-evaluate-source/assets/` — shows source-scorecard.md
- [ ] `python3 skills/dos-evaluate-source/scripts/profile-sample.py --help` — exits 0
- [ ] `head -10 skills/dos-evaluate-source/SKILL.md` — shows Agent Skills spec frontmatter with `name` and `description`
- [ ] `grep "dos:scope-data-product" skills/dos-evaluate-source/SKILL.md` — "Next Steps" references the downstream skill
- [ ] `test -f docs/data-products/_index.md` — artifact directory conventions exist
- [ ] `grep "evaluate-source" README.md` — skill listed in project README
- [ ] All files created follow the project's markdown conventions (YAML frontmatter, key insights first)

## Notes

### Architecture Validation Findings

**(a) SKILL.md line count: 162 / 500 (68% headroom)**

The 500-line constraint is generous for this skill. With progressive disclosure to references/, the SKILL.md focuses on workflow steps and brief inline context, delegating detailed decision matrices and scoring criteria to reference files. 162 lines covers the full 10-step workflow comfortably.

**Projection for remaining skills:** Design-phase skills (define-contract, assess-quality) may run longer due to more complex decision trees, but unlikely to exceed 300 lines given this precedent. Build-phase skills (implement-source, implement-models) may push closer to 400 lines since they include code generation patterns and platform-specific guidance. The 500-line budget appears sound.

**(b) Progressive disclosure to references/ works well**

The pattern is effective: SKILL.md states *what* to assess and *why*, references contain the *detailed criteria* (scoring tables, decision matrices, checklists). The `Refer to [file](path) for...` pattern provides clear signals for when agents should load additional context.

Key observation: references averaged 71 lines (range: 55-97). This is well under the design's 200-line target. The "extract only decision matrices, criteria tables, checklists — no explanatory prose" guideline works — the context files contain substantial prose that correctly got filtered out.

**(c) Template-first approach validated**

Writing the source scorecard template (136 lines) before SKILL.md was the right sequence. The template defined the artifact structure, and the SKILL.md workflow steps naturally mapped to template sections. When writing Step 9 (Generate Scorecard), pointing to the template was trivial because the structure was already established.

**Recommendation for Plans 2-3:** Continue template-first. For skills that update existing artifacts (e.g., select-model updates the scope document), define the update schema in the template before writing the SKILL.md.

**(d) Conventions validated — no changes needed**

| Convention | Status | Notes |
|-----------|--------|-------|
| 500-line SKILL.md limit | Validated | 68% headroom on a mid-complexity skill |
| References under 200 lines | Validated | All under 100 lines; 200 is conservative |
| Agent Skills spec frontmatter only | Validated | Only `name` and `description` in frontmatter |
| Preamble check pattern | Validated | Clean pattern: ask data product name → check existing → adjust |
| "Next Steps" closing | Validated | Natural flow — user knows what to do next |

**One recommendation for remaining skills:** The profiling script (282 lines) is the largest single file. Build-phase scripts (code generators, validators) will likely be larger. Consider whether scripts/ should have a size guideline or if they're intentionally unconstrained (since they're deterministic tools, not LLM instructions).

### File Size Summary

| Component | Lines | % of Total |
|-----------|------:|:----------:|
| SKILL.md | 162 | 19% |
| References (4 files) | 283 | 33% |
| Asset template | 136 | 16% |
| Profiling script | 282 | 33% |
| **Total skill footprint** | **863** | |
