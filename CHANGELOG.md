# Changelog

All notable changes to the dos plugin are documented here.

## [0.3.1] — 2026-04-09

### Fixed
- `scope-data-product` now requires a specific delivery window for timeliness SLAs — cadence alone no longer passes as a valid SLA (#12)
- `review-pipeline` now detects missing `dbt source freshness` wiring as **critical** when freshness thresholds are defined in source YAML but absent from the production job (#17)

### Added
- Delivery Window Guidance table in `sla-hierarchy.md` with bad/good SLA examples per cadence
- Freshness Wiring Detection table in `sla-checklist.md` with condition/severity/finding classification

## [0.3.0] — 2026-04-08

### Changed
- Redesigned `implement-source` from scorecard-to-code translator to extraction boundary guardian (#33, #30, #29, #26, #24, #16)
- New workflow Step 2: "Verify Extraction Boundary" with blocking/advisory checks before code generation
- Absorbed Step 3 ("Flag dlt Configuration Pitfalls") — content covered by existing `dlt-pipeline-patterns.md` references

### Added
- `references/extraction-boundary-rules.md` — raw-first extraction rules, violation patterns, cost-of-retry principle, remediation routing
- `references/dlt-runtime-behaviors.md` — array/child table creation under merge, schema caching on field changes
- Cost-Aware Retry Configuration section in `dlt-pipeline-patterns.md`
- Graceful fallback for `validate-upstream.py` when script is not found

### Fixed
- `implement-source` now detects array/list fields under merge write disposition before generating code (#33)
- `implement-source` now scans existing code for raw-first violations (model_dump lambdas, schema imports, enrichment logic) (#30, #24)
- `validate-upstream.py` invocation falls back to manual checklist instead of silently skipping (#29)
- Schema cache reset warning included in generated pipeline code comments (#26)
- Cost-of-retry calculated for quota-billed APIs before recommending `max_retries` increases (#16)

## [0.2.0] — 2026-04-08

### Added
- `evaluate-source` Step 3: Pricing & Cost assessment with safeguards against common cost estimation errors — confirms plan tier, billing unit, and shows transparent calculations (#11)
- `evaluate-source` Step 8: Live API Validation for SaaS API/REST sources — 3-request validation checklist with correction prompt before saving the scorecard (#10)
- Pipeline Cost Estimate subsection in Step 9 (Ingestion Recommendation) with formula and confirmed/estimated input labels (#11)
- Sampling provenance metadata in profiling output — tracks sample size, total population, sampling method, and representativeness warnings (#22, #27)
- `--json` and `--output` flags for `profile-sample.py` enabling machine-consumable profile output for downstream skill consumption (#22)
- `--sample-of` flag for `profile-sample.py` to record total population and auto-detect suspicious sample sizes (#22)
- `references/pricing-models.md` — pricing model classification, billing unit disambiguation, estimation pitfalls, and safeguards checklist (#11)
- Sampling & Representativeness section in `profiling-metrics.md` with bias signals, strategies for paginated APIs, and provenance recording guidance (#27)
- Sampling Provenance and Live API Validation sections in the source scorecard template (#10, #22)
- Cost/pricing as a factor in Access Complexity dimension scoring (#11)

### Changed
- Rewrote `profile-sample.py` to use DuckDB natively for all statistics — replaced custom Python type inference, percentile calculation, and frequency counting with `SUMMARIZE` and SQL (389 → 294 lines, zero new dependencies)
- Profile-first, render-second architecture: structured dict is the primary output, markdown tables are a rendered view
- Renumbered evaluate-source workflow from 10 steps to 12 steps (clean 1-12 sequence)
- Paginated REST API sampling guidance in Step 7 (Data Profiling) — recommends multi-page sampling with minimum 100-record threshold (#27)

## [0.1.2] — 2026-04-07

### Fixed
- Cross-artifact model name hallucination: `implement-models` now builds a model registry and validates all `{{ ref() }}` and `{{ source() }}` targets against the codebase before emitting code (#14)
- `define-contract` dbt snippet generation now checks existing models instead of inventing names from contract objects (#14)
- `assess-quality` now scans for existing dbt models to use verified names in quality rule SQL (#14)
- Generated dbt YAML now uses `data_tests:` with `arguments:`/`config:` nesting for dbt >= 1.10.5, fixing `MissingArgumentsPropertyInGenericTestDeprecation` warnings (#13)

## [0.1.1] — 2026-04-06

### Added
- `marketplace.json` for plugin registry installation (#8)

### Fixed
- Use `${CLAUDE_SKILL_DIR}` for `validate-upstream.py` path resolution in build-phase skills (#18)

## [0.1.0] — 2026-03-23

First release. All 9 Tier 1 skills implemented covering the full data engineering lifecycle.

### Added

**Discover phase**
- `dos:evaluate-source` — assess source systems with six-dimension scoring, data profiling, and ingestion recommendations

**Scope phase**
- `dos:scope-data-product` — define data products driven by consumption intent with SLA tiers and quality dimensions

**Design phase**
- `dos:select-model` — choose a data modeling approach (Kimball, Data Vault, OBT) based on constraints
- `dos:define-contract` — define ODCS v3.1-aligned data contracts with three-layer enforcement
- `dos:assess-quality` — set up quality dimensions, scoring methods, and tiered validation tooling
- `dos:design-pipeline` — architecture pipelines with layering strategy, incremental patterns, and idempotency

**Build phase**
- `dos:implement-source` — generate dlt pipeline code and dbt source definitions with CDC boundary detection
- `dos:implement-models` — generate dbt models, schema YAMLs, tests, and contract enforcement with platform detection

**Verify phase**
- `dos:review-pipeline` — audit pipelines across observability, validation, CI/CD, SLAs, and retry handling

**Foundation**
- 66 research-backed context files across 23 data engineering characteristic areas
- Skill library design document defining the 9-skill architecture
- Plugin scaffold with `plugin.json`, directory conventions, and portable Agent Skills spec
- `CLAUDE.md` with project conventions and skill architecture reference
- README with workflow diagram, skill chain, and getting started guidance
- GitHub Issue template for skill feedback collection
