---
name: Data Model Selection Criteria
description: "Decision framework for choosing between Kimball, Data Vault, and OBT — platform optimization matters more than model choice, and semantic layers may make this debate less consequential."
type: context
related:
  - docs/research/2026-03-22-data-modeling.research.md
  - docs/context/kimball-dimensional-modeling.md
  - docs/context/data-vault-modeling.md
  - docs/context/obt-wide-table-patterns.md
---

## Key Insight

Platform optimization matters more than model choice. Databricks Liquid Clustering achieved 20x speedup on OBT. DuckDB's DPhyp join optimizer narrows the star-vs-OBT gap. The right model configured wrong will lose to the wrong model configured right. Start with Kimball, optimize for your platform, and add complexity only when pain emerges.

## Decision Framework

| Factor | Choose Kimball | Choose Data Vault | Choose OBT |
|--------|---------------|-------------------|------------|
| Team size | Any | 5+ engineers with automation | Any (rapid start) |
| Source count | Any | 5+ with frequent changes | Few, stable |
| Compliance needs | Standard | Audit trail / GDPR / regulated | Minimal |
| Query pattern | Mixed analytics + drill-down | Complex cross-domain joins | Simple flat queries, CSV/API export |
| BI tool | Tableau, Power BI, Looker | N/A (needs star schema presentation) | Tools without relationship support |
| Change velocity | Moderate | High (changes isolated to satellites) | Low (changes cascade) |
| Platform fit | All platforms | Snowflake, Databricks | BigQuery, Databricks with Liquid Clustering |

## Platform-Specific Guidance

**DuckDB:** Joins are cheap. The DPhyp algorithm finds optimal join orders, putting multi-join queries within 2x of wide table speed. Wide tables inflated storage 6.3x in TPC-H benchmarks. Star schemas are the natural fit. Use proper data types — DATETIME uses 3.3GB vs VARCHAR at 5.2GB on 554M rows.

**Snowflake:** Decouples storage (cheap) from compute (expensive). Data Vault's insert-only patterns align with this cost structure. Star schemas recommended for stable reporting. Wide tables recommended only when "query speed matters more than storage efficiency or update flexibility."

**Databricks:** "How a model is optimized is more important than which model is chosen." Liquid Clustering is essential for large tables regardless of model. Delta Live Tables automates SCD Type 2. The medallion architecture (Bronze raw, Silver OBTs for exploration, Gold star schemas for production) is the recommended layered approach.

**ClickHouse:** Append-only MergeTree engine makes denormalization expensive. Star schema with one or two joins matches the JOIN algorithm's strengths. Use materialized views for pre-aggregation instead of flattening.

## Counter-Evidence Worth Knowing

- Fivetran benchmarks show OBT outperforms star schema 10-45% for BI-style queries
- BigQuery sees 49% average improvement with OBT
- These are real performance gaps on specific platforms — they do not invalidate Kimball as a default but they matter for platform-specific optimization

## The Semantic Layer Wildcard

dbt Semantic Layer and AtScale are abstracting business logic above physical models. If semantic layers mature as projected, the physical modeling choice becomes an implementation detail. This is the strongest challenge to the entire modeling debate. AtScale reports LLMs achieve near-perfect accuracy with semantic grounding versus 20% without it.

The implication: if you are investing heavily in a semantic layer, optimize your physical model for compute cost and maintenance simplicity rather than query ergonomics — the semantic layer handles that.

## The Pragmatism Principle

The biggest risk is not choosing wrong — it is spending weeks debating modeling approaches before writing your first dbt model. Zearn runs billions of rows with 1 data person. ThriftBooks handles ~100M units with a pragmatic three-layer architecture. The dbt community advises: "these schemas can be useful, but should only be used if they are useful to you, not just because it's what people usually do."

## Takeaway

Default to Kimball. Optimize for your platform. Use OBT as a serving layer when consumers need it. Reserve Data Vault for regulated environments. Watch the semantic layer space — it may render this entire decision less important within a few years.
