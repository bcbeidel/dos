---
name: Data Vault Modeling
description: "Data Vault provides audit-complete history through immutable hub-link-satellite structures but creates 300-500 tables in year one — reserve for regulated environments with 5+ engineers and automation tooling."
type: context
related:
  - docs/research/2026-03-22-data-modeling.research.md
  - docs/context/kimball-dimensional-modeling.md
  - docs/context/obt-wide-table-patterns.md
  - docs/context/data-model-selection.md
---

## Key Insight

Data Vault is for enterprise audit and compliance environments only. It creates 300-500 tables in a typical medium-sized organization's first year, requires automation tooling, and demands a team of 5+ engineers. Skip it for small teams, few sources, or straightforward reporting. When you do need it, it delivers genuine value: full historical tracking with append-only immutability.

## Architecture

Data Vault 2.0 is a hybrid approach combining aspects of third normal form and star schema, resulting in a "historical-tracking, detail-oriented, uniquely-linked set of normalized tables."

Three entity types:

**Hubs** store unique business keys — the identifiers that define a business entity regardless of source system. Hubs are immutable: once a business key is loaded, it never changes. They use hash keys (e.g., `BINARY(32)`) derived from natural business keys.

**Links** store relationships between hubs. Every relationship (customer-to-order, order-to-product) gets its own table. Links support many-to-many relationships inherently and are immutable once recorded.

**Satellites** store time-stamped descriptive attributes. Every time an attribute changes, a new satellite row is inserted — full history is preserved without modifying existing rows. Each row includes an effective date for point-in-time reconstruction.

## Strengths

- **Audit trail is built-in.** The additive, append-only nature means you can retrieve the state of data as understood at any point in time.
- **Schema changes are isolated.** Changes only affect specific satellites; the rest of the model remains stable.
- **Source flexibility is high.** New sources integrate by adding hubs, links, and satellites without modifying existing structures.
- **Insert-only patterns align with cloud cost models.** Snowflake's cheap storage / expensive compute model favors never updating or deleting records.

## When It Fails

- **Small teams.** Without automation, "engineers spend weeks building infrastructure instead of delivering analytics."
- **Few sources.** Fewer than 5 stable data sources do not justify the overhead.
- **Straightforward reporting.** The query complexity is real — "more complex than querying `dim_customers` directly."
- **Limited budgets.** Specialized tooling (WhereScape, automate-dv) is effectively required.
- **The Explanation Tax.** "You will spend a lot of time explaining the nuances to stakeholders, both technical and non-technical."

Data Vault produces 3x as many tables as equivalent relational models, with "unwieldy and complex join conditions." It should "be treated with caution...there are many traps for the unwary."

## Platform Considerations

**Snowflake** is the strongest fit. Columnar storage and automatic query optimization handle multi-table queries efficiently. Decoupled storage (cheap) and compute (expensive) make storing complete history affordable.

**Databricks** works but the Raw Data Vault is extremely complex to query directly — almost always requires transformation into star schemas for the Gold layer.

Data Vault always requires a presentation layer (typically star schemas) for business user consumption. It is an integration-layer strategy, not a consumption-layer one.

## Takeaway

If you need GDPR compliance, full audit trails, or must integrate 5+ volatile source systems with a team that can sustain the complexity, Data Vault's overhead is justified. Otherwise, start with Kimball and add Data Vault patterns only where the complexity genuinely helps.
