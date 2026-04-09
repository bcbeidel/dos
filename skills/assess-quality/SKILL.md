---
name: assess-quality
description: Design a quality assessment configuration for a data product. Produces a Quality Configuration artifact with selected dimensions, scoring method, action thresholds, validation tooling, and anomaly detection approach.
---

# dos:assess-quality

Design a quality assessment configuration for a data product. Walk through dimension selection, measurement methods, scoring, action thresholds, validation tooling, and anomaly detection -- producing a persistent Quality Configuration artifact.

## Preamble

Before starting, establish context:

1. **Which data product?** Ask the user for a data product name (e.g., `customer-orders`, `revenue-metrics`). This determines the artifact path: `docs/data-products/<name>/quality-config.md`.
2. **Check for existing quality config.** If `docs/data-products/<name>/quality-config.md` exists, read it, summarize the current state, and ask what's changing. Update the existing artifact rather than creating a new one.
3. **Check for scope document.** If `docs/data-products/<name>/scope.md` exists, read it -- consumer definitions, use cases, and SLA requirements will pre-populate quality dimensions and thresholds.
4. **Check for data contract.** If `docs/data-products/<name>/contract.md` exists, read it -- schema definitions and guarantees will inform validation rules and dimension selection.

If the quality config exists, adjust the workflow: skip sections that haven't changed, focus on what the user wants to update, and bump the version in frontmatter.

### Reference Materials

This skill uses the following curated references:

- [quality-dimensions.md](references/quality-dimensions.md) -- Six-dimension consensus, dimension selection as a design decision, fitness-for-use principle
- [scoring-methods.md](references/scoring-methods.md) -- Test fail rate vs failed row count, weighted aggregation, action thresholds
- [sla-error-budgets.md](references/sla-error-budgets.md) -- SLI/SLO/SLA hierarchy, error budget calculation, tiered SLA structures
- [validation-tiers.md](references/validation-tiers.md) -- Three-tier execution strategy, tool selection by tier, scaling down guidance
- [anomaly-methods.md](references/anomaly-methods.md) -- Three detection layers, point anomaly and drift methods, maturity progression
- [dbt-test-selection.md](references/dbt-test-selection.md) -- Rule type classification and dbt test mapping for implementation guidance

Output template: [quality-config-template.md](assets/quality-config-template.md)

## Workflow

### Step 1: Check Existing State

If a quality config already exists at `docs/data-products/<name>/quality-config.md`:

1. Read the existing artifact
2. Summarize: current dimensions, scoring method, thresholds, validation tier, anomaly approach
3. Ask: "What needs to change?"
4. Skip unchanged sections in the workflow below

If no quality config exists, proceed from Step 2.

### Step 2: Pre-Populate from Existing Artifacts

If a scope document or data contract exists, extract relevant context:

**From scope document:**
- Consumer list and their use cases (drives dimension selection)
- SLA requirements (drives threshold calibration)
- Data characteristics (drives anomaly method selection)

**From data contract:**
- Schema definitions (drives validity checks)
- Guarantees and constraints (drives completeness and uniqueness checks)
- Freshness requirements (drives timeliness thresholds)

**From existing dbt models (if any):**
- Search for existing dbt models (`models/**/*.sql`) and schema YAMLs (`models/**/*.yml`) for this data product. Record actual model names and column names. When the quality config references specific models or columns — in measurement methods, rule SQL, or example queries — use names verified against the codebase, not names inferred from the contract alone.

Present pre-populated values to the user for confirmation or adjustment. Do not silently inherit values -- the user must see and approve what was carried forward.

### Step 3: Select Quality Dimensions

Present the six-dimension consensus as a starting vocabulary:

1. **Accuracy** -- How closely data represents reality
2. **Completeness** -- Whether all required records and fields are present
3. **Consistency** -- Whether data agrees across systems and within itself
4. **Timeliness** -- Whether data is available when needed
5. **Validity** -- Whether data conforms to defined formats, types, and business rules
6. **Uniqueness** -- Whether data is free of unintended duplicates

Refer to [quality-dimensions.md](references/quality-dimensions.md) for detailed definitions and the selection process.

Guide the user to select 4-10 dimensions:

- Ask which dimensions matter most for their consumers and use cases
- Suggest domain-specific dimensions beyond the six if relevant (e.g., usefulness, freshness as distinct from timeliness)
- Explain that dimension selection is a design decision, not a checkbox exercise
- If scope or contract pre-populated dimensions, present those as a starting proposal

**Fitness for use:** Quality is relative to the consumer. A 5% null rate may be acceptable for trend analysis but catastrophic for a customer-facing report. Each dimension's importance depends on who uses the data and for what purpose.

### Step 4: Define Measurement Methods and Thresholds

For each selected dimension, define:

1. **Measurement method** -- The specific calculation or check (e.g., `(total_rows - null_count) / total_rows` for completeness)
2. **Green threshold** -- Score above which no action is needed
3. **Yellow threshold** -- Score below which investigation is required
4. **Red threshold** -- Score below which remediation is required

Refer to [scoring-methods.md](references/scoring-methods.md) for the three-tier action threshold framework.

**Threshold calibration guidance:**
- Financial reporting tables may require 99.5% completeness at the green threshold
- Internal analytics tables may tolerate 95%
- Thresholds must be calibrated per data product -- no single set fits all use cases
- If the scope document specifies SLA targets, use those as starting points

**Rule type classification:** For each measurement method, classify the underlying rule type using [dbt-test-selection.md](references/dbt-test-selection.md). The rule type determines which dbt test implements the check. Do not map directly from dimension to test -- a single dimension (e.g., validity) spans multiple rule types (enum membership, numeric range, string pattern, expression) that require different dbt tests.

For stateful rules (run-over-run comparisons, metric stability checks), flag explicitly that these require singular tests with baseline storage. Reference the implementation patterns in dbt-test-selection.md and note the pattern in the quality config output.

### Step 5: Choose Scoring Method

Present two options:

1. **Test fail rate** -- Each test binary (passed=1.0, warning=0.5, failed=0.0), averaged within each dimension
2. **Failed row count** -- `(total_rows - failed_rows) / total_rows`, averaged across tests per dimension

**Recommend failed row count** for finer granularity: a test failing on 1 row out of 1M scores 99.9999% rather than 0.0. Test fail rate is simpler but loses proportionality -- a test that fails on 1 row scores identically to one that fails on all rows.

Refer to [scoring-methods.md](references/scoring-methods.md) for detailed comparison and examples.

### Step 6: Assign Weights

Guide weight assignment:

1. Weights must sum to 1.0
2. Weight assignment is a business decision, not an engineering one
3. Stakeholders must participate -- do not assign weights unilaterally
4. Higher weights on dimensions that matter most to primary consumers

**Composite score formula:**

```
Quality Score = SUM(dimension_score * weight) for all dimensions
```

Normalize dimension scores to percentages before aggregation. Explain the aggregation tension: a composite of 92% could mean all dimensions at 92% (healthy) or completeness at 100% while accuracy is at 70% (dangerous). Composite scores serve communication; dimension-level scores serve investigation.

### Step 7: Define Action Thresholds with Owners

For the composite score and any per-dimension overrides:

| Threshold | Default Range | Required Definition |
|-----------|:------------:|-------------------|
| **Green** | 90-100% | No action required |
| **Yellow** | 70-89% | Investigation required, with response SLA and assigned owner |
| **Red** | Below 70% | Remediation required, with response SLA and assigned owner |

Every threshold must have:
- A defined action to take when breached
- A defined owner responsible for taking that action
- A response SLA (how quickly the owner must act)

Without these operational bindings, quality scores become vanity metrics.

Refer to [sla-error-budgets.md](references/sla-error-budgets.md) for error budget mechanics that complement threshold-based actions.

### Step 8: Recommend Validation Tooling by Tier

Based on team size, existing stack, and data product tier, recommend validation tools across three execution environments:

| Tier | Environment | Recommended Tools |
|------|------------|-------------------|
| **Tier 1** | Local development | Pandera + pytest, dbt unit tests (v1.8+) |
| **Tier 2** | CI pipeline | dbt data tests + dbt-expectations (Metaplane fork) |
| **Tier 3** | Production | Soda / Great Expectations, dbt source freshness |

Refer to [validation-tiers.md](references/validation-tiers.md) for the full three-tier strategy and scaling-down guidance.

**Scaling guidance for small teams (1-3 engineers):**
1. Start with dbt tests in CI and production -- already in the stack
2. Add Pandera only for Python-heavy pipelines (dlt extractors, custom transformations)
3. Defer Soda/GE until dedicated platform engineering capacity exists

Ask about team size and current tooling before recommending. The three-tier strategy is a target architecture, not a minimum viable setup.

**Test selection by rule type:** When recommending specific dbt tests, use the rule-type-to-test mapping in [dbt-test-selection.md](references/dbt-test-selection.md) rather than mapping from dimension name alone. This prevents mismatches where a validity rule is mapped to `accepted_values` when it actually requires `expression_is_true` or a regex test.

### Step 9: Recommend Anomaly Detection Approach

Based on data characteristics, volume, and team maturity, recommend an anomaly detection approach:

Refer to [anomaly-methods.md](references/anomaly-methods.md) for the three detection layers and method selection guide.

**Layer recommendations:**

1. **Rule-based (always)** -- Known constraints from dimension definitions. Deploy immediately.
2. **Statistical (when ready):**
   - Normal distributions: z-score (|z| > 3)
   - Skewed distributions: IQR (Tukey's fences)
   - Time-series metrics: SPC control charts
3. **Distribution drift (for production monitoring):**
   - Small datasets (<1K rows): KS test
   - Large datasets (100K+ rows): Wasserstein Distance

**Maturity progression:** Start with rules-only. Add statistical methods when rules are stable. Introduce ML-based detection only at scale (100K+ observations) and only alongside established rules.

### Step 10: Generate Quality Configuration

Produce the quality configuration artifact using the template from [quality-config-template.md](assets/quality-config-template.md).

Save to `docs/data-products/<name>/quality-config.md` with:
- Complete YAML frontmatter (name, artifact_type, version, owner, status, last_modified)
- All sections populated from the workflow above
- Changelog entry recording the configuration

If updating an existing artifact:
- Bump the minor version
- Update `last_modified`
- Add a changelog entry describing what changed

### Step 11: Next Steps

End the quality configuration with a "Next Steps" section recommending downstream skills:

1. **`/dos:implement-models`** -- Implement the dbt models with quality tests embedded based on this configuration. The quality config drives which generic and singular tests are applied per model.
2. **`/dos:define-contract`** -- If a data contract does not yet exist, define one. The quality config provides the measurement side; the contract provides the commitment side.

Present these options to the user and explain what each downstream skill will do with the quality configuration results.
