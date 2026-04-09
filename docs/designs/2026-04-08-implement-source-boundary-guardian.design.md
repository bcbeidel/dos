---
name: implement-source Extraction Boundary Guardian
description: Redesign implement-source from scorecard-to-code translator to extraction boundary guardian, consolidating 6 open issues into runtime behavior modeling, mechanical principle enforcement, and honest safety infrastructure.
type: design
status: draft
related:
  - skills/implement-source/SKILL.md
  - skills/implement-source/references/dlt-pipeline-patterns.md
---

# implement-source: Extraction Boundary Guardian

## Purpose

Redesign `implement-source` so it actively guards the extraction boundary rather than passively translating scorecard fields to dlt code. The skill must understand dlt's runtime behavior, mechanically enforce raw-first extraction, and treat operational cost as a design input.

This consolidates 6 open issues (#33, #30, #29, #26, #24, #16) into a single cohesive change based on three capability gaps:

1. **Runtime behavior modeling** — the skill must know what dlt *does* at runtime, not just what its API accepts (#33, #26).
2. **Mechanical principle enforcement** — raw-first extraction must be verified by scanning code, not stated as prose (#24, #30).
3. **Honest safety infrastructure** — validation must work, and operational cost must be a first-class input (#29, #16).

## Behavior

### New Workflow Step: Verify Extraction Boundary

A new step runs between "Validate Ingestion Approach" (Step 1) and "Generate dlt Pipeline" (Step 3), applying codified rules before any code is generated or modified:

| Check | Input | Finding Type | Trigger |
|-------|-------|-------------|---------|
| Raw-first violation scan | Existing pipeline code | **Blocking** | `processing_steps` with lambdas that reshape, enrich, or derive fields not in the source response |
| Array field detection | Scorecard field types + write disposition | **Blocking** | Array/list field when write disposition is `merge` |
| Cost-of-retry calculation | Scorecard pricing data + API call volume | **Blocking** (if >$10) | Quota-billed API source with retry config recommendation |
| Schema cache impact | Proposed field changes vs. existing code | **Advisory** | Fields removed or renamed from a previously-run pipeline |

Blocking findings must be resolved before the skill proceeds to code generation. Advisory findings are reported and documented in generated code.

### Enriched Code Generation

When generating dlt pipeline code, the skill now:

- Declares array fields as `text` with JSON serialization when write disposition is `merge`.
- Includes a comment in generated code warning that field removal/rename requires wiping `~/.dlt/pipelines/<name>/` and local database files.
- References `dlt-runtime-behaviors.md` for platform-specific nested data handling.
- Does not recommend `max_retries > 0` for quota-billed APIs without presenting the cost tradeoff.

### Absorbed Step: Flag dlt Configuration Pitfalls

Current Step 3 (4 config pitfalls) is removed as a standalone step. Its content is already documented in `dlt-pipeline-patterns.md` under "Known Pitfalls," which Step 3 (Generate dlt Pipeline) references. No knowledge is lost.

### Fixed Upstream Validation

The `validate-upstream.py` invocation in Preamble Step 2 reliably resolves to the script in the skill's `scripts/` directory. If the script is not found, the skill falls back to an explicit manual checklist rather than silently skipping validation.

## Scope

### Must Have

- New reference file: `extraction-boundary-rules.md` — raw-first rules, violation patterns, cost-of-retry principle
- New reference file: `dlt-runtime-behaviors.md` — child table creation, schema caching, cross-platform divergence
- New workflow Step 2: "Verify Extraction Boundary" with blocking/advisory findings
- Expanded `dlt-pipeline-patterns.md` with cost-aware retry section
- Fixed `validate-upstream.py` invocation with graceful fallback
- Preamble Step 5 expanded to scan existing code for boundary violations
- Old Step 3 absorbed — content covered by references

### Won't Have

- New Python validation scripts for automated pattern detection
- Changes to other skills (review-pipeline, evaluate-source, implement-models)
- Changes to asset templates, auth-config-patterns.md, or dbt-source-config.md
- Automated schema-type inference from source APIs

## Constraints

- SKILL.md stays under 500 lines. Absorbing Step 3 reclaims ~20 lines; new Step 2 fits in ~25-30 lines by delegating to references.
- Reference files stay under 200 lines each.
- Template-first authoring order: write reference files before modifying SKILL.md.
- The skill still works without upstream artifacts (graceful degradation). The verification step reports findings but only blocks on clear violations, not missing information.

## Acceptance Criteria

1. **Array fields under merge are caught before generation.** When the scorecard indicates an array/list field and write disposition is `merge`, Step 2 flags it as blocking and Step 3 generates the `columns` declaration + JSON serialization pattern.
2. **Raw-first violations in existing code are detected.** When existing pipeline code contains `processing_steps` with lambdas that call `model_dump()`, import schema modules, or perform enrichment, Step 2 reports them as blocking violations with specific remediation routing (staging vs. intermediate).
3. **validate-upstream.py runs successfully.** The preamble script invocation resolves to the script in the skill's `scripts/` directory. If not found, falls back to an explicit manual checklist.
4. **Schema cache reset is documented in generated code.** Generated pipeline code includes a comment warning that field removal/rename requires wiping `~/.dlt/pipelines/<name>/`.
5. **Cost-of-retry is calculated for quota-billed APIs.** When the scorecard contains API pricing data, Step 2 calculates retry cost and flags if >$10 before recommending retry configuration.
6. **Old Step 3 content remains accessible.** The 4 config pitfalls (Bug #2782, silent env vars, silent destination fallback, nested data divergence) are reachable via `dlt-pipeline-patterns.md`, which the generation step references.

## Issue Coverage

| Issue | Root Cause | Addressed By |
|-------|-----------|-------------|
| #33 array child tables | Skill doesn't model dlt runtime behavior | `dlt-runtime-behaviors.md` + Step 2 blocking check + Step 3 generation pattern |
| #30 rename lambda detection | Raw-first is prose, not verification | `extraction-boundary-rules.md` + Preamble step 5 scan + Step 2 blocking check |
| #29 phantom script | Safety infrastructure doesn't exist | Preamble step 2 path fix + graceful fallback |
| #26 schema cache reset | Skill doesn't model dlt runtime behavior | `dlt-runtime-behaviors.md` + Step 3 generated code comment |
| #24 raw-first enforcement | Raw-first is prose, not verification | `extraction-boundary-rules.md` + Step 2 blocking check |
| #16 cost-of-retry | Operational cost treated as outside scope | `extraction-boundary-rules.md` + Step 2 cost calculation |

## Changelog

| Date | Change |
|------|--------|
| 2026-04-08 | Initial design — consolidates #33, #30, #29, #26, #24, #16 |
