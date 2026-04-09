---
name: "evaluate-source: Live API Validation and Pricing Assessment"
description: "Add Step 3 (Pricing), Step 8 (Live API Validation), and Step 9 cost addendum — renumber all steps to a clean 1-12 sequence"
type: plan
status: completed
branch: api-validation-and-pricing
related:
  - docs/designs/2026-04-08-evaluate-source-api-validation-and-pricing.design.md
  - skills/evaluate-source/SKILL.md
---

# Plan: evaluate-source — Live API Validation and Pricing Assessment

## Goal

Add pricing/cost assessment and live API validation steps to evaluate-source,
renumber all steps to a clean 1-12 sequence, closing issues #10 and #11.

## Scope

### Must have
- Step 3 (Pricing & Cost) in SKILL.md with safeguards
- Step 8 (Live API Validation) in SKILL.md, conditional on SaaS API classification
- Step 9 pipeline cost estimate addendum (in Ingestion Recommendation)
- Renumber all SKILL.md steps from 1-10 to 1-12
- New `references/pricing-models.md` reference file
- Scorecard template sections for pricing and live validation
- Cost as a factor in Access Complexity scoring

### Won't have
- Automated curl execution or API clients
- Cost comparison across sources
- Rate limit / load testing
- Cost monitoring or alerting

## Approach

Template-first authoring per CLAUDE.md: write scorecard template sections
first (Task 1), then reference material (Task 2), then SKILL.md workflow
(Tasks 3-4), then dimension framework update (Task 5). Each task is
independently verifiable and gets its own commit.

**Step renumbering scheme:**

| New # | Step | Was |
|:-----:|------|:---:|
| 1 | Intake Filtering | 1 |
| 2 | Source Metadata | 2 |
| **3** | **Pricing & Cost** | new |
| 4 | Source Classification | 3 |
| 5 | Six-Dimension Assessment | 4 |
| 6 | Authentication & Credential Management | 5 |
| 7 | Data Profiling | 6 |
| **8** | **Live API Validation** | new |
| 9 | Ingestion Recommendation (+ cost estimate) | 7 |
| 10 | Re-Profiling Cadence | 8 |
| 11 | Generate Scorecard | 9 |
| 12 | Next Steps | 10 |

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `skills/evaluate-source/assets/source-scorecard.md` | modify | Add Pricing & Cost section; add live validation record to Data Profiling |
| `skills/evaluate-source/references/pricing-models.md` | create | Pricing model classification table with billing units, quotas, pitfalls |
| `skills/evaluate-source/SKILL.md` | modify | Renumber steps 1-12; add Step 3 (Pricing), Step 8 (Live API Validation), Step 9 cost addendum |
| `skills/evaluate-source/references/six-dimension-framework.md` | modify | Add cost factor to Access Complexity criteria |

## Tasks

### Chunk 1: Templates and References

- [x] **Task 1: Add Pricing & Cost and Live Validation sections to scorecard template** <!-- sha:93a2ae2 -->
  - Add a "Pricing & Cost" section after "Authentication & Credential Management" with:
    pricing inputs table (model, tier, quota, unit cost, overage) with confirmation status column,
    pipeline cost estimate with formula and inputs
  - Add a "Live API Validation" subsection to "Data Profiling Results" with:
    validation performed (yes/no/N/A), requests made, corrections applied
  - Verify: `grep -c "Pricing" skills/evaluate-source/assets/source-scorecard.md` returns ≥1;
    `grep -c "Live API Validation" skills/evaluate-source/assets/source-scorecard.md` returns ≥1
  - Commit: `feat(scorecard): add pricing and live validation template sections`

- [x] **Task 2: Create pricing-models.md reference file** <!-- sha:f740dba -->
  - Create `skills/evaluate-source/references/pricing-models.md` with:
    pricing model classification table (subscription, per-request, per-record, freemium, free/open),
    billing unit disambiguation table (per-call vs per-record vs per-row-returned),
    common estimation pitfalls (from issue #11: wrong tier, wrong billing unit, doc estimates vs actuals),
    cost estimation safeguards checklist
  - Verify: `wc -l skills/evaluate-source/references/pricing-models.md` is between 40-200 lines;
    `head -5 skills/evaluate-source/references/pricing-models.md` shows a markdown heading
  - Commit: `feat(references): add pricing-models.md classification table`

### Chunk 2: SKILL.md Workflow Steps

- [x] **Task 3: Renumber steps and add Step 3 (Pricing & Cost) with Step 9 cost addendum** <!-- sha:e415b64 -->
  - Renumber all existing steps from 1-10 to the new 1-12 scheme (see Approach table)
  - Insert new Step 3 (Pricing & Cost) between Source Metadata and Source Classification:
    gather pricing model, tier, quota, unit cost, overage policy;
    each input marked confirmed/estimated;
    reference pricing-models.md inline;
    skip guidance for free/open sources
  - Add pipeline cost estimate subsection to Step 9 (Ingestion Recommendation):
    formula: requests_per_run x runs_per_month x cost_per_request;
    show formula with actual values;
    flag if monthly cost exceeds quota
  - Verify: `grep "Step 3: Pricing" skills/evaluate-source/SKILL.md` returns a match;
    `grep "Step 12" skills/evaluate-source/SKILL.md` returns a match;
    `grep "Pipeline Cost Estimate" skills/evaluate-source/SKILL.md` returns a match
  - Commit: `feat(skill): add pricing step and renumber evaluate-source workflow 1-12 (#11)`

- [x] **Task 4: Add Step 8 (Live API Validation)** <!-- sha:4403f37 -->
  - Insert Step 8 (Live API Validation) between Data Profiling (Step 7) and
    Ingestion Recommendation (Step 9):
    trigger condition (SaaS API or REST source classification only);
    3-request validation checklist (single record, different-parameter batch, profile comparison);
    correction prompt before proceeding;
    reference to --json profiling output for structured comparison
  - Verify: `grep "Step 8" skills/evaluate-source/SKILL.md` returns a match;
    `grep "Live API Validation" skills/evaluate-source/SKILL.md` returns a match
  - Commit: `feat(skill): add live API validation step to evaluate-source (#10)`

### Chunk 3: Dimension Framework

- [x] **Task 5: Add cost factor to Access Complexity in six-dimension-framework.md** <!-- sha:c15b361 -->
  - Update Access Complexity scoring criteria to note that cost/pricing
    complexity is a contributing factor — expensive APIs with strict quotas
    or opaque billing increase operational complexity
  - This is a light touch: add cost as a consideration in the score 2-3 range,
    not a new dimension
  - Verify: `grep -i "cost\|pricing" skills/evaluate-source/references/six-dimension-framework.md`
    returns at least one match
  - Commit: `feat(references): add cost factor to Access Complexity scoring (#11)`

## Validation

After all tasks are complete:

1. **Scorecard template renders:** All new sections use valid markdown table syntax
   with `{{placeholder}}` convention matching existing sections
2. **SKILL.md step flow:** Steps read in order 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12
   with no gaps and no broken cross-references
3. **Reference file consistency:** pricing-models.md follows existing reference
   conventions (under 200 lines, tables not prose, no explanatory narrative)
4. **Inline references:** SKILL.md references pricing-models.md using the
   `[filename](references/filename)` pattern matching existing references
5. **Issue coverage:** #10 acceptance criteria (conditional step, 3-request checklist,
   correction prompt) and #11 acceptance criteria (pricing inputs, cost estimate,
   safeguards) are all addressable from the skill workflow
