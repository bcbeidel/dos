# Changelog

All notable changes to the dos plugin are documented here.

## [0.4.0] — 2026-04-10

First stable release. Collapses the 9-skill Discover→Scope→Design→Build→Verify chain into 4 skills, replaces the 6-file per-pipeline artifact structure with a single `data-product.md` living document, and eliminates artifact drift by making `data-product.md` the sole specification consumed by build-phase skills. Closes #23.

### Breaking Changes

- **Skill chain restructured**: 9 skills → 4 active skills. Any `/dos:` invocations using deprecated skill names will not route to replacement skills automatically.
- **Artifact structure replaced**: the 6-file per-pipeline layout (`scope.md`, `contract.md`, `quality-config.md`, `pipeline-architecture.md`, `reviews/`) is replaced by a single `docs/data-products/<name>/data-product.md`. Existing artifacts under the old structure are not migrated automatically.
- **`evaluate-source` renamed to `scope-source`**: invocations of `/dos:evaluate-source` must be updated to `/dos:scope-source`.
- **`implement-models` replaced by `implement-data-product`**: invocations of `/dos:implement-models` must be updated to `/dos:implement-data-product`.

### Added

- `dos:scope-data-product` — fully rewritten to a 5-section workflow (Overview, Sources, Contract, Quality, Architecture) that populates a single `data-product.md` living document. Collapses `define-contract`, `assess-quality`, `design-pipeline`, and `select-model` into one skill with section-gated reference loading and cross-section consistency checks.
- `dos:implement-data-product` — new build-phase skill that generates dbt models, schema YAMLs, tests, contract enforcement, and orchestration artifacts (Databricks Asset Bundles) from `data-product.md`. Replaces `implement-models`.
- `data-product.md` asset template — living document with YAML frontmatter, 5 pending-marker sections, and a pre-populated Changelog scaffold.
- `validate-data-product.py` — validation script (in both `implement-source/scripts/` and `implement-data-product/scripts/`) that checks file existence, frontmatter validity, `artifact_type`, and non-pending required sections. Exit 2 on failure with structured ERROR/FIX output.
- Orchestration artifact generation in `implement-data-product` Step 9 — reads `tool::component.identifier` shorthands from the Architecture section to generate Databricks Asset Bundles job/pipeline resource blocks.
- 15 reference files consolidated into `skills/scope-data-product/references/` (from `define-contract`, `assess-quality`, `design-pipeline`, `select-model`).

### Changed

- `dos:scope-source` (renamed from `evaluate-source`) — frontmatter `name` field updated; all other content preserved.
- `dos:implement-source` — updated to validate `data-product.md` Sources section before code generation, read ingestion context from `data-product.md` instead of standalone `contract.md`/`scope.md`, and append Changelog entry to `data-product.md` on completion. Next-step suggestion updated from `review-pipeline` to `implement-data-product`.
- `CLAUDE.md` skill chain table updated to reflect 4-skill architecture and `docs/data-products/<name>/data-product.md` output path.

### Deprecated

The following skills are retained with their reference files but marked `status: deprecated`. They will not receive further updates and may be removed in a future release.

- `dos:define-contract` → replaced by `dos:scope-data-product` (Contract section)
- `dos:assess-quality` → replaced by `dos:scope-data-product` (Quality section)
- `dos:design-pipeline` → replaced by `dos:scope-data-product` (Architecture section)
- `dos:select-model` → replaced by `dos:scope-data-product` (Architecture section)
- `dos:review-pipeline` → absorbed into `dos:implement-data-product` and `dos:implement-source`
- `dos:implement-models` → replaced by `dos:implement-data-product`

## [0.3.3] — 2026-04-09

### Added
- `design-pipeline` Step 2b: Cross-Pipeline Dependencies — surfaces runtime dependencies when intermediate models join across staging domains, with DAG ordering and first-time setup checklist (#25)
- Cross-Pipeline Dependencies section in pipeline-architecture template with dependency table and prerequisite checklist

## [0.3.2] — 2026-04-09

### Added
- `implement-models` detects composite `unique_key` lists in existing and new models, recommends `dbt_utils.generate_surrogate_key` with the original columns kept as a `unique_combination_of_columns` validation test (#28)
- Surrogate Keys for Composite Keys section in `dbt-model-patterns.md` with SQL pattern, tradeoff table, and validation test example

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
