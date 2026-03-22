---
name: Kimball Dimensional Modeling
description: "Kimball's star schema methodology is the strongest prescriptive default for analytics engineering — 90%+ enterprise adoption, cloud vendor endorsement, BI tool alignment, proven from solo practitioners to Uber/Netflix/Spotify scale."
type: context
related:
  - docs/research/2026-03-22-data-modeling.research.md
  - docs/context/data-vault-modeling.md
  - docs/context/obt-wide-table-patterns.md
  - docs/context/data-model-selection.md
---

## Key Insight

Kimball dimensional modeling is the strongest prescriptive default for analytics engineering. ACH analysis across 15 evidence items found only 3 inconsistencies for Kimball vs 7 for OBT. It works at any team size (Zearn: billions of rows, 1 data person; Uber: 100+ petabytes) and aligns with how BI tools, cloud vendors, and business users think about data.

## The Methodology

Kimball's four-step process:

1. **Pick a business process** to model — prioritize business user questions over abstract entities
2. **Decide on the grain** at the most atomic level — line items, not orders — enabling future detailed analysis
3. **Choose applicable dimensions** by asking how business users describe the data
4. **Identify numeric facts** that populate fact table rows

Core philosophy: "do the hard work now, to make it easy to query later."

Star schemas denormalize dimension attributes into wide tables to reduce join complexity for analytic workloads. The fact table sits at the center, surrounded by dimension tables connected by foreign keys.

## Fact Table Types

- **Transaction:** one row per event (most common)
- **Periodic snapshot:** cumulative measurements at regular intervals
- **Accumulating snapshot:** tracks progress through multi-stage processes
- **Factless:** records dimension relationships without measurements (e.g., attendance)

Fact properties: additive (sum across all dimensions), semi-additive (some dimensions only), non-additive (cannot be summed).

## Dimension Design

- **Surrogate keys:** system-generated integers replacing natural identifiers
- **Denormalized structure:** flattened hierarchies enabling direct navigation
- **Role-playing:** single dimension referenced multiple times (e.g., order date vs ship date)
- **Degenerate:** dimension attributes stored in the fact table (e.g., order number)
- **Junk dimensions:** combine low-cardinality flags into a single table
- **Conformed dimensions:** shared definitions across fact tables enabling "drilling across"

## Slowly Changing Dimensions (SCD)

- **Type 0:** retain original values (immutable)
- **Type 1:** overwrite with current values (no history)
- **Type 2:** add new row with effective dating (full history)
- **Type 3:** add column for previous value (limited history)

Modern approach: snapshot entire dimension tables daily, leveraging cheap storage instead of complex ETL logic.

## Enterprise Integration

The **bus architecture** maps business processes and dimensional conformance through an enterprise matrix, guiding phased data warehouse development. Conformed dimensions maintain identical definitions across multiple fact tables.

## Known Limitations

- **Real-time gap:** traditional ETL processes were not designed for streaming
- **Centipede schema:** too many dimensions degrades join performance
- **Conformed dimension maintenance** requires enterprise-wide coordination
- **Snowflaking** (normalizing dimensions) adds complexity and can hurt performance — generally avoid it

## Why It Wins

Snowflake recommends storing "final consumable data in the Kimball dimensional data model." Databricks notes star schema and Data Vault are "quite popular." Microsoft Fabric states star schema design "is optimized for analytic query workloads." Tableau and Power BI are "designed with star schemas in mind." A Fortune 500 reduced a 1,000-line dbt model into 21 modular Kimball models with 179 tests replacing just 2.

## Takeaway

Start with Kimball. Add complexity only when you have evidence that something else is needed. The four-step process forces clarity about business questions before writing any SQL.
