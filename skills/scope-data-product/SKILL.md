---
name: scope-data-product
description: Define what a data product needs to be, driven by consumption intent. Produces a Data Product Scope Document with consumers, query patterns, freshness requirements, SLA dimensions, quality dimensions, and MoSCoW prioritization.
---

# dos:scope-data-product

Define what a data product needs to be, driven by consumption intent. Walk through stakeholder analysis, source inventory, freshness quantification, SLA definition, quality dimension selection, and prioritization — producing a persistent Data Product Scope Document.

## Preamble

Before starting, establish context:

1. **Which data product?** Ask the user for a data product name (e.g., `orders`, `customer-360`). This determines the artifact path: `docs/data-products/<name>/scope.md`.
2. **Check for existing artifact.** If `docs/data-products/<name>/scope.md` exists, read it, summarize the current state, and ask what's changing. Update the existing artifact rather than creating a new one.
3. **Check for source evaluations.** If source evaluations exist in `docs/sources/`, list them. Ask which sources this data product will consume. Load each referenced scorecard to pre-populate source classifications, profiling baselines, and ingestion recommendations.

If the artifact exists, adjust the workflow: skip sections that haven't changed, focus on what the user wants to update, and bump the version in frontmatter.

## Workflow

### Step 1: Load Source Context

If source scorecards exist in `docs/sources/`, load each referenced evaluation. Extract:
- Source type and classification
- Six-dimension scores (especially freshness, schema stability, data quality)
- Profiling baselines (completeness, uniqueness, validity)
- Ingestion recommendations

A data product may consume multiple sources. The scope document records which sources and datasets are in play.

If no source evaluations exist, proceed — the user will provide source information through conversation.

### Step 2: Consumers and Use Cases

Walk through the Data Product Canvas blocks in consumption-first order.

Refer to [interview-questions.md](references/interview-questions.md) for the full canvas framework, stakeholder interview patterns, and consumption-first traversal.

Identify:
- Who consumes this data product (teams, roles, systems)
- What decisions each consumer makes with the data
- What happens when the data is wrong or late

Supplement stated requirements with empirical evidence: review actual dashboards, SQL queries, or query logs to understand how data is actually consumed vs. how stakeholders say it is consumed.

### Step 3: Query Patterns

For each consumer, identify the dominant query pattern:

| Pattern | Description |
|---------|-------------|
| Join-heavy | Multidimensional analytics across multiple entities |
| Scan-heavy | Wide columnar queries selecting many attributes |
| Entity lookup | Point lookups on a specific entity (user, order) |
| Ad-hoc | Unpredictable exploration patterns |

Refer to [consumption-heuristics.md](references/consumption-heuristics.md) for query shape to modeling recommendations.

### Step 4: Source Inventory

Document which sources and datasets this data product will consume. For each source:
- Source name and classification
- Datasets needed from that source
- Ingestion approach (from evaluation or determined here)
- Link to evaluation scorecard if available

### Step 5: Freshness Requirements

Quantify freshness in specific time units — not adjectives like "real-time" or "near-real-time."

**Key question:** "What business decision changes if the data is 5 minutes old instead of 5 seconds old?"

For each dataset, define:
- Required freshness (e.g., "2 hours", "15 minutes", "daily")
- Business justification for that freshness
- Implied ingestion strategy (batch, micro-batch, streaming)

Refer to [consumption-heuristics.md](references/consumption-heuristics.md) for freshness-to-ingestion mapping.

### Step 6: SLA Tier Classification

Classify the data product's SLA tier:

| Tier | Characteristics |
|------|----------------|
| **Prototype** | Ad-hoc exploration, no SLA, re-run on failure |
| **Production-grade** | Formal SLA, error budgets, retry logic, change management |

Pipeline investment should be proportional to consumer dependency on the data.

### Step 7: Consumption-Driven Heuristics

Apply the three consumption dimensions to derive architecture defaults:

Refer to [consumption-heuristics.md](references/consumption-heuristics.md) for the full decision tables.

- **Query shape** → modeling recommendation (star schema, OBT, entity-centric)
- **Freshness need** → ingestion strategy (batch, incremental, streaming)
- **SLA tier** → pipeline investment level

### Step 8: Quality Dimensions

Select initial quality dimensions and derive thresholds from profiling baselines and consumption tolerances.

Refer to [quality-dimension-selection.md](references/quality-dimension-selection.md) for the six-dimension consensus, selection process, and profiling-to-dimension mapping.

For each selected dimension:
- Define the threshold (e.g., "> 99% completeness on required fields")
- Note the profiling baseline if available
- Document the consumer tolerance that justifies the threshold

### Step 9: SLA Dimensions

Define SLA dimensions using the SLI/SLO/SLA hierarchy.

Refer to [sla-hierarchy.md](references/sla-hierarchy.md) for the five SLA dimensions, error budget calculation, and tiered guidance.

At minimum, define timeliness and completeness SLAs. For each dimension:
1. Define the SLI (what to measure)
2. Set the SLO (internal target)
3. Negotiate the SLA (commitment)
4. Calculate the error budget

### Step 10: MoSCoW Prioritization

If multiple consumers have competing requirements, apply MoSCoW:

Refer to [interview-questions.md](references/interview-questions.md) for MoSCoW framework details.

- **Must have** — without which the data product has no value
- **Should have** — important, deliverable iteratively
- **Could have** — nice-to-haves deprioritized under pressure
- **Won't have** — explicitly descoped with rationale

Unstated "Won't have" items become implicit commitments. Make descoping explicit.

### Step 11: Generate Scope Document

Produce the Data Product Scope Document using the template structure from [scope-document.md](assets/scope-document.md).

Save to `docs/data-products/<name>/scope.md` with:
- Complete YAML frontmatter (name, artifact_type, version, owner, status, last_modified, sources)
- All sections populated from the workflow above
- Explicit "Won't have in v1" section
- Changelog entry recording the scoping session

If updating an existing artifact:
- Bump the minor version
- Update `last_modified`
- Add a changelog entry describing what changed

### Step 12: Next Steps

End the scope document with a "Next Steps" section recommending downstream skills:

1. **`/dos:select-model`** — Choose a data modeling approach based on query patterns, team size, and platform. Updates the scope document's modeling recommendation section.
2. **`/dos:define-contract`** — Define a data contract covering schema, quality rules, SLAs, and ownership.
3. **`/dos:assess-quality`** — Set up quality engineering with dimensions, thresholds, scoring, and validation tooling.
4. **`/dos:design-pipeline`** — Architecture the data pipeline from source to serving layer.

Present these options to the user and explain what each downstream skill will do with the scope document.
