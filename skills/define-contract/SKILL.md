---
name: define-contract
description: Define or update an ODCS v3.1-aligned data contract covering schema, quality rules, SLAs, ownership, and enforcement strategy. Produces a persistent contract artifact at docs/data-products/<name>/contract.md.
---

# dos:define-contract

Define or update a data contract for a data product following the Open Data Contract Standard (ODCS) v3.1. Walk through schema definition, quality rules, SLAs, ownership, versioning, and enforcement — producing a persistent contract artifact that downstream skills consume.

## Preamble

Before starting, establish context:

1. **Which data product?** Ask the user for a data product name (e.g., `orders`, `customer-360`). This determines the artifact path: `docs/data-products/<product-name>/contract.md`.
2. **Check for existing contract.** If `docs/data-products/<product-name>/contract.md` exists, read it, summarize the current state (version, status, schema objects, quality rules, SLAs), and ask what's changing. Update the existing contract rather than creating a new one.
3. **Check for scope document.** If `docs/data-products/<product-name>/scope.md` exists, read it to pre-populate: consumers and use cases, source inventory, freshness requirements, SLA dimensions, quality dimensions with initial thresholds. The scope document is the primary input for contract definition.
4. **Check for source evaluations.** If source evaluations exist in `docs/sources/`, note profiling baselines that can seed quality rules and schema definitions.

If the contract exists, adjust the workflow: skip sections that haven't changed, focus on what the user wants to update, and apply versioning rules (Step 7) to determine the correct version bump.

## References

These curated knowledge files provide detailed guidance for each workflow step:

- [odcs-structure.md](references/odcs-structure.md) — ODCS v3.1 section inventory, four core components, ODCS vs dbt contracts, consumer-defined vs producer-defined contracts
- [enforcement-layers.md](references/enforcement-layers.md) — Three enforcement layers (CI-time, build-time, runtime), tiered enforcement actions, cultural adoption guidance
- [versioning-patterns.md](references/versioning-patterns.md) — Semantic versioning rules, expand-contract pattern, breaking vs additive change classification, compatibility modes
- [contract-template.md](assets/contract-template.md) — Output artifact template with all 11 ODCS sections

## Workflow

### Step 1: Check for Existing Contract

If a contract already exists at `docs/data-products/<product-name>/contract.md`:

1. Read the contract and summarize: current version, status, number of objects/properties defined, quality rules count, SLA targets, enforcement layers configured.
2. Ask the user: "What needs to change?" Common triggers:
   - Adding new objects or properties to the schema
   - Updating quality rules based on observed data behavior
   - Adjusting SLAs after operational experience
   - Responding to a planned schema change from a producer
3. Proceed to the relevant step(s) based on what's changing. Apply versioning in Step 7.

If no contract exists, proceed to Step 2.

### Step 2: Pre-Populate from Scope Document

If `docs/data-products/<product-name>/scope.md` exists, extract and present:

| Scope Section | Maps to Contract Section |
|---------------|------------------------|
| Consumers and use cases | Roles, Team |
| Source inventory and datasets | Schema (objects) |
| Freshness requirements | SLA (freshness, frequency) |
| SLA tier and dimensions | SLA (all dimensions) |
| Quality dimensions with thresholds | Data Quality rules |
| Owner | Fundamentals, Team |

Present the pre-populated values and ask the user to confirm or adjust before proceeding. The scope document is the starting point — the contract adds precision (exact types, specific thresholds, enforcement actions).

If no scope document exists, gather this information conversationally in subsequent steps.

### Step 3: Define or Update Schema

For each object (table) in the data product:

1. **Name the object** — Use the ODCS convention: "objects" not "tables", "properties" not "columns".
2. **Define properties** — For each property, specify:
   - **Name** — snake_case preferred for consistency
   - **Logical type** — string, integer, long, float, double, boolean, date, timestamp, decimal(p,s)
   - **Nullable** — yes or no (default: yes for optional fields)
   - **Constraints** — PK, FK(target), UNIQUE, CHECK(expr), or none
   - **Description** — Business meaning, not just technical definition
3. **Define relationships** — Foreign keys and cross-object references.

If source evaluations exist, use profiling results (column types, nullability, uniqueness ratios) to pre-populate property definitions. Confirm with the user — profiled types are inferred, not guaranteed.

Refer to [odcs-structure.md](references/odcs-structure.md) for the ODCS naming conventions and field-level requirements.

**Guidance:**
- Every property must be explicitly listed. ODCS and dbt contracts both require exhaustive property definitions.
- Choose logical types, not platform-specific types. Map to platform types during implementation.
- Primary keys should be NOT NULL with a UNIQUE constraint. Identify key candidates from profiling.

### Step 4: Define or Update Quality Rules

Define quality rules at two levels:

**Property-level rules** (per-property checks):
- **Completeness** — null rate thresholds (e.g., `null_rate < 0.02`)
- **Validity** — range checks, pattern matching, enum membership
- **Uniqueness** — uniqueness ratio on key candidates

**Object-level rules** (cross-property or aggregate checks):
- **Row count** — minimum expected volume per load
- **Consistency** — cross-field relationships that must hold
- **Timeliness** — record-level freshness checks

For each rule, specify:
- **Rule ID** — sequential identifier (Q-001, Q-101)
- **Severity** — critical (block writes), warning (alert), informational (log)
- **Rule expression** — SQL, plain text, or threshold

If the scope document defined quality dimensions with initial thresholds, use those as starting values. If source evaluations exist, use profiling baselines (null rates, uniqueness ratios, value ranges) to set realistic thresholds.

**Guidance:**
- Start with completeness and validity — highest signal-to-investment ratio.
- Use thresholds, not absolutes: `null_rate < 0.02` is more sustainable than `null_rate = 0`.
- A contract with three quality rules is better than no contract. Expand coverage over time.

### Step 5: Define or Update SLAs

Define service-level agreements across six dimensions:

| Dimension | What to Define | Example |
|-----------|---------------|---------|
| **Freshness** | Maximum age of latest data | Data no more than 4 hours stale |
| **Availability** | Uptime percentage | 99.5% availability |
| **Latency** | Source-to-destination delay | End-to-end < 30 minutes |
| **Retention** | How long data is kept | 13 months rolling |
| **Update Frequency** | How often data refreshes | Hourly / daily at 6am UTC |
| **Backup** | Recovery capability | Daily snapshots, 7-day retention |

For each SLA:
- Define the target value
- Specify how it is measured (SLI)
- Calculate the error budget (e.g., 99.5% = ~3.6 hours/month of allowed violation)

If the scope document defined freshness requirements or SLA tiers, use those as inputs.

Refer to [odcs-structure.md](references/odcs-structure.md) for ODCS SLA field definitions.

**Guidance:**
- Start with freshness and availability — they provide the highest signal.
- Set SLOs stricter than SLAs to provide buffer before customer-facing breaches.
- Error budgets make SLA conversations concrete: "99.5% compliance" is actionable; "data should be fresh" is not.

### Step 6: Define Ownership, Support, and Governance

Populate the Team, Roles, and Support sections:

**Team:**
- Data product owner (accountable for the contract)
- Producer team (maintains the source and meets SLAs)
- Consumer team(s) (reads data, reports issues)
- Steward (governance oversight, if applicable)

**Roles:**
- Who can approve schema changes and version bumps?
- Who must be notified of breaking changes?
- Who is responsible for migrating on major version bumps?

**Support:**
- Primary contact channel (Slack, email)
- Escalation path (who if primary is unresponsive)
- Support hours
- Incident process (link to runbook)
- Notification channel for contract changes

**Guidance:**
- Contracts require source system owners to accept accountability for data quality. This is a cultural shift. Start with willing producers.
- The data product owner — not the source system team — should define what the contract requires (consumer-defined approach).

### Step 7: Apply Versioning

Determine the correct version bump based on changes made:

Refer to [versioning-patterns.md](references/versioning-patterns.md) for the full classification table and expand-contract pattern.

| Change Type | Version Bump | Migration Required? |
|-------------|-------------|-------------------|
| Remove property, change type incompatibly, tighten nullability | MAJOR | Yes — expand-contract pattern |
| Add optional property, add quality rule, add new SLA dimension | MINOR | No |
| Documentation, metadata, comment changes | PATCH | No |
| Relax SLA (less strict for consumers) | MINOR | No |
| Tighten SLA (more strict for consumers) | MAJOR | Yes — announce with timeline |

**For MAJOR version changes:**
1. Do not remove or change elements in place.
2. Apply the expand-contract pattern:
   - **Expand:** Add new elements alongside existing ones.
   - **Migrate:** Give consumers time to switch. Set a deprecation date on the old version.
   - **Contract:** Remove old elements after all consumers have migrated.
3. Document the migration path in the changelog.

**For new contracts:** Start at version `1.0.0`.

### Step 8: Define Enforcement Strategy

Configure enforcement across three layers:

Refer to [enforcement-layers.md](references/enforcement-layers.md) for tool mappings and tiered enforcement actions.

**CI-Time (pre-deploy):**
- What tool detects breaking changes? (dbt Cloud CI, schema registry, Data Contract CLI)
- What happens on detection? (block merge, require version bump)

**Build-Time (transformation):**
- Is `contract: { enforced: true }` set in dbt models?
- What contract mode for ingestion? (freeze, discard_row, discard_value)

**Runtime (post-load):**
- Which quality rules are enforced at runtime? (map from Step 4)
- What is the circuit breaker threshold? (how many violations before blocking)
- What alerting is configured? (PagerDuty for critical, Slack for warnings)

Not all three layers are required immediately. Specify which layers are active now and which are planned. A contract with build-time enforcement only is better than a contract with no enforcement.

### Step 9: Generate Contract

Produce the full ODCS v3.1-aligned contract using the template from [contract-template.md](assets/contract-template.md).

Save to `docs/data-products/<product-name>/contract.md` with:
- Complete YAML frontmatter (name, artifact_type: contract, version, owner, status, last_modified)
- All 11 ODCS sections populated from the workflow above
- Versioning section with current rules
- Enforcement strategy with active layers
- Changelog entry recording the creation or update

**Populate peripheral sections with reasonable defaults if not discussed:**
- **References:** Link to scope document if it exists
- **Pricing:** "No pricing model applied" unless the team uses chargeback
- **Infrastructure:** Populate if known from source evaluations; otherwise mark as TBD
- **Custom Properties:** Include data classification if known; otherwise leave empty with example keys

If updating an existing contract:
- Apply the version bump from Step 7
- Update `last_modified`
- Add a changelog entry describing what changed
- Preserve sections that were not modified

### Step 10: Generate dbt Contract Snippet (Optional)

If the team uses dbt for transformation, offer to generate a dbt-compatible contract snippet:

1. **Check existing models first.** Search for existing dbt models (`models/**/*.sql`) and schema YAMLs (`models/**/*.yml`). If models already exist for this data product, use the actual model and column names from the codebase — do not invent names from the contract's logical object names alone.
2. Map each object to a dbt model name. If no existing models are found, apply the naming convention `stg_<source>__<table>` / `fct_<process>` / `dim_<entity>` and confirm with the user.
3. Map each property to a column with `data_type` and constraints
4. Set `contract: { enforced: true }`
5. Include only schema enforcement — dbt contracts do not cover quality rules or SLAs

Present the snippet for the user to add to their dbt model YAML. This is a convenience output, not a separate artifact.

**Remind the user:** dbt contracts enforce schema structure only. Quality rules (Step 4) and SLAs (Step 5) require separate enforcement tooling (Soda, Great Expectations, dbt tests, circuit breakers).

### Step 11: Next Steps

End the contract with a "Next Steps" section recommending downstream skills:

1. **`/dos:assess-quality`** — Translate the contract's quality rules into a full quality configuration with scoring methods, weighted aggregation, action thresholds, and validation tooling. The contract's Data Quality section is the primary input.
2. **`/dos:implement-models`** — Build the dbt models that implement this contract. The schema section maps directly to model definitions. If a dbt contract snippet was generated (Step 10), it provides the starting configuration.

Present these options to the user and explain what each downstream skill will do with the contract.
