---
name: Data Source Onboarding
description: "Structured discovery workflows reduce onboarding from months to weeks by front-loading profiling, quality assessment, and metadata documentation before pipeline construction; data profiling has three types (structure, content, relationship); intake forms filter requests and capture technical requirements"
type: context
related:
  - docs/research/2026-03-22-data-discovery.research.md
  - docs/context/source-system-evaluation.md
  - docs/context/data-contracts.md
  - docs/context/data-catalog-selection.md
---

## Key Takeaway

Discovery is assessment, not implementation. Steps 1-5 of a structured onboarding workflow happen before any pipeline code is written. By validating quality and structure before building, teams avoid the expensive pattern of discovering issues during dashboard creation or executive reporting. Automation reduces the mechanical onboarding work (connector setup, schema mapping, initial profiling) from weeks to days. The full cycle including business context, quality benchmarking, and governance integration remains multi-week for complex sources.

## Minimum Viable Discovery Workflow

The OvalEdge 8-step model is comprehensive but assumes organizational maturity most teams lack. The practical minimum is four steps:

1. **Define scope** -- Identify stakeholders, regulatory requirements, and measurable outcomes. What decision will be made with this data?
2. **Inventory sources** -- Document source type, location, ownership, format, and volume. Build the source catalog entry.
3. **Validate access** -- Confirm connectivity, permissions, and credentials. Access problems are the most common onboarding blocker.
4. **Assess quality** -- Run data profiling to establish the baseline. This is where most skipped steps cost the most.

Steps 5-8 (classify, prepare, explore, govern) require catalog tooling, stewardship roles, and governance processes. Add them as organizational maturity allows.

## Data Profiling: Three Types

Profiling is the measurement foundation for source evaluation. Without it, quality assessment is subjective ("the data looks fine") and volume baselines are absent ("it's about this big").

**Structure discovery** -- How is data formatted and organized? Field types, lengths, patterns, formatting consistency. Reveals whether a phone number field contains text, whether date fields use consistent formats, whether numeric fields contain non-numeric values.

**Content discovery** -- Are individual data values accurate and consistent? Missing values, incorrect values, ambiguous data, domain violations. Structure discovery is quantitative; content discovery is qualitative.

**Relationship discovery** -- How does this data connect to other datasets? Foreign key relationships, shared identifiers, join candidates, cross-source linkages. Essential for new sources that must integrate with existing assets.

Profiling findings directly determine ingestion layer (based on source format), transformation logic (based on quality issues), storage selection (based on data structure), and monitoring parameters (based on quality benchmarks).

## Intake Forms as Structured Friction

Effective intake processes introduce "just enough friction to filter out lazy asks" while remaining accessible. Two filtering questions that distinguish serious requests from casual ones:

- "What decision will you make or action will you take with this data?"
- "What is the real problem you're trying to solve?"

For operational rigor, capture concrete technical details before triaging: source application, generating hosts, data format, file paths, sample data, sensitive data classification, retention requirements, and impact/urgency assessment for outages.

## Metadata Documentation

New source metadata must cover two categories:

**Technical metadata** (machine-harvested): Schema structure, data volumes, refresh schedules, access patterns, query performance, storage location. Automated via catalog connectors.

**Business metadata** (human-curated): Ownership, plain-language definitions, quality scores, certification status, use cases, compliance indicators (PII classification, retention). Cannot be fully automated.

The 80/20 principle: machines handle technical metadata at scale while humans provide strategic context. Catalogs relying solely on automated harvesting are technically complete but semantically empty. Catalogs relying solely on manual entry decay within months.
