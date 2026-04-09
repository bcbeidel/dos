---
name: "evaluate-source: Live API Validation and Pricing Assessment"
description: "Add two new steps to evaluate-source — conditional live API validation for REST sources (#10) and pricing/cost assessment with safeguards (#11)"
type: design
status: draft
related:
  - skills/evaluate-source/SKILL.md
  - skills/evaluate-source/assets/source-scorecard.md
  - skills/evaluate-source/references/profiling-metrics.md
  - skills/evaluate-source/references/six-dimension-framework.md
---

# evaluate-source: Live API Validation and Pricing Assessment

## Purpose

Two additions to the evaluate-source skill that address gaps found during
real source evaluation sessions:

1. **Live API validation (#10):** Code-derived scorecards for REST/SaaS API
   sources contain errors that only surface when hitting the API — wrong null
   rates, wire types differing from documentation, sub-field structures that
   require response inspection. A structured validation step catches these
   before the scorecard is saved.

2. **Pricing and cost assessment (#11):** Source evaluation has no cost
   dimension. A real session produced a 16x cost overstatement ($94,908/year
   vs. confirmed $5,748/year) because pricing model, billing unit, and data
   volume were all wrong. Pricing should be gathered early (before investing
   in full assessment) and pipeline cost estimated late (after the ingestion
   approach is known).

## Behavior

### Live API Validation (Step 6b)

**Trigger condition:** Source classification is SaaS API or any REST-based
source. Does not apply to Transactional DB, Event Stream, or File-Based
sources.

**When in the workflow:** After Step 6 (Data Profiling), before Step 7
(Ingestion Recommendation). The profiled data may have come from
documentation, code evidence, or a limited sample — this step validates
against the actual API.

**Validation checklist (3 requests):**

1. **Single record by ID** — Fetch one complete record to inspect the full
   wire format. Compare every field's actual type against the scorecard's
   inferred type. Flag any mismatches (e.g., documented as `date`, wire
   format is ISO 8601 datetime string).

2. **Small batch from a different parameter** — Fetch 10-25 records using
   a different geography, date range, category, or ID range than the
   original sample. Compare null rates against the profiled baseline.
   Flag any field where the observed null rate diverges by more than 20
   percentage points from the profiled value.

3. **Compare to profiled sample** — If the user can save the API responses
   as JSON, profile them with `profile-sample.py --json` and compare the
   two profile JSONs. Focus on: type mismatches, null rate divergence,
   new/missing fields, sub-field structure differences.

**Correction prompt:** After validation, ask: "Did the live API responses
reveal any differences from the profiled sample? If yes, correct the
scorecard before saving." List specific fields to review: types, null rates,
field structures, enum values.

**Scorecard addition:** The Data Profiling Results section should record
whether live validation was performed and any corrections made.

### Pricing and Cost Assessment

**Step 2b: Pricing Inputs** — Between Step 2 (Source Metadata) and Step 3
(Source Classification). Gather pricing data early because cost may affect
the scope decision (is this source worth pursuing at all?).

**Pricing inputs to gather:**

| Input | Description | Confirmation Status |
|-------|-------------|:-------------------:|
| Pricing model | Subscription, per-request, per-record, freemium, or free/open | confirmed / estimated |
| Current plan/tier | The actual contract or plan the team is on | confirmed / estimated |
| Quota | Monthly/daily request or record limits | confirmed / estimated |
| Cost per unit | At expected pipeline volume | confirmed / estimated |
| Overage policy | Hard stop, overage charges, throttling, or unlimited | confirmed / estimated |

**Safeguards** (from the issue's cost estimation errors):

- Ask for the current plan/contract tier — do not assume from public pricing
- Query actual production row count when available — do not use documentation
  estimates
- Confirm the billing unit explicitly: "per API call or per record?"
- Show calculations transparently so the operator can catch errors
- Mark each input as "confirmed" (operator verified) or "estimated" (derived
  from docs or assumptions)

**Step 7 addendum: Pipeline Cost Estimate** — After the ingestion approach
is known, calculate the estimated pipeline cost. This goes in Step 7
(Ingestion Recommendation) because it depends on refresh cadence, request
volume, and approach.

**Pipeline cost formula:**

```
requests_per_run × runs_per_month × cost_per_request = monthly_cost
```

Show the formula with actual values so the operator can verify each input.
Flag if monthly cost exceeds the quota (would require a tier upgrade or
trigger overage charges).

**Scorecard addition:** New "Pricing & Cost" section after Authentication,
with the pricing inputs table, pipeline cost estimate, and confirmation
status for each input.

## Components

### New files

| File | Purpose |
|------|---------|
| `references/pricing-models.md` | Classification table of pricing model types, billing units, quota patterns, and common estimation pitfalls |

### Modified files

| File | Change |
|------|--------|
| `SKILL.md` | Add Step 2b (Pricing Inputs), Step 6b (Live API Validation), and Step 7 pipeline cost addendum |
| `assets/source-scorecard.md` | Add Pricing & Cost section; add live validation record to Data Profiling Results |
| `references/six-dimension-framework.md` | Add cost as a factor in Access Complexity scoring criteria |

## Constraints

- The skill does not execute curl requests or API calls. It prompts the
  operator to run them and report the results.
- Pipeline cost estimates are rough order-of-magnitude — they are inputs
  to the scope decision, not financial forecasts.
- Cost comparison across alternative sources is out of scope — that belongs
  to scope-data-product.
- Rate limit testing or load testing is out of scope.
- Pricing step is skippable for free/open sources (the skill should detect
  "free" as a pricing model and skip the cost estimation).

## Acceptance Criteria

1. For a SaaS API source, Step 6b prompts the operator with a 3-request
   validation checklist and a correction prompt. Scorecard records whether
   validation was performed.
2. For a non-API source, Step 6b is skipped entirely — no prompt, no
   scorecard section.
3. Step 2b gathers pricing inputs with confirmation status. Free/open
   sources skip cost estimation.
4. Step 7 includes a pipeline cost estimate with transparent formula and
   all inputs labeled confirmed/estimated.
5. The scorecard Pricing & Cost section renders correctly with all fields
   populated.
6. Pricing reference file covers at least: subscription, per-request,
   per-record, freemium, and free/open pricing models.

## Changelog

| Date | Change |
|------|--------|
| 2026-04-08 | Initial design |
