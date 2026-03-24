# Model Decision Matrix

Decision framework for choosing between Kimball, Data Vault, and OBT.

## Decision Rules

**Default to Kimball.** It works at any team size, aligns with BI tools and cloud vendors, and has 90%+ enterprise adoption. Add complexity only when evidence demands it.

**Choose Data Vault when:** 5+ engineers with automation tooling, 5+ source systems with frequent changes, and regulated environments requiring audit trails (GDPR, SOX). Data Vault creates 300-500 tables in a typical first year and always requires a star schema presentation layer for consumption.

**Choose OBT when:** consumers need simple flat queries, sources are few and stable, and the platform favors it (BigQuery, Databricks with Liquid Clustering). Use OBT as a serving layer on top of Kimball, not as a standalone architecture.

## Selection Criteria Matrix

| Factor | Choose Kimball | Choose Data Vault | Choose OBT |
|--------|---------------|-------------------|------------|
| Team size | Any | 5+ engineers with automation | Any (rapid start) |
| Source count | Any | 5+ with frequent changes | Few, stable |
| Compliance needs | Standard | Audit trail / GDPR / regulated | Minimal |
| Query pattern | Mixed analytics + drill-down | Complex cross-domain joins | Simple flat queries, CSV/API export |
| BI tool | Tableau, Power BI, Looker | N/A (needs star schema layer) | Tools without relationship support |
| Change velocity | Moderate | High (changes isolated to satellites) | Low (changes cascade) |
| Platform fit | All platforms | Snowflake, Databricks | BigQuery, Databricks with Liquid Clustering |

## The Pragmatism Principle

The biggest risk is not choosing wrong -- it is spending weeks debating modeling approaches before writing your first dbt model. Zearn runs billions of rows with 1 data person. ThriftBooks handles ~100M units with a pragmatic three-layer architecture.

## The Semantic Layer Wildcard

dbt Semantic Layer and AtScale are abstracting business logic above physical models. If semantic layers mature as projected, the physical modeling choice becomes an implementation detail. AtScale reports LLMs achieve near-perfect accuracy with semantic grounding versus 20% without it.

**Implication:** if investing heavily in a semantic layer, optimize the physical model for compute cost and maintenance simplicity rather than query ergonomics.

## Decision Shortcut

1. Do you have 5+ engineers, 5+ volatile sources, and regulatory audit requirements? -> Data Vault
2. Do consumers only need flat exports or your platform strongly favors wide tables? -> OBT as serving layer
3. Everything else -> Kimball

## Takeaway

Default to Kimball. Optimize for your platform. Use OBT as a serving layer when consumers need it. Reserve Data Vault for regulated environments with the team to sustain it. Watch the semantic layer space.
