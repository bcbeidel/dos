---
name: OBT and Wide Table Patterns
description: "OBT (One Big Table) is best as a downstream mart layer, not standalone architecture — originated from BigQuery's join limitations, not architectural principle. Brooklyn Data's hybrid (Kimball core + OBT marts) is the evidence-backed pattern."
type: context
related:
  - docs/research/2026-03-22-data-modeling.research.md
  - docs/context/kimball-dimensional-modeling.md
  - docs/context/data-vault-modeling.md
  - docs/context/data-model-selection.md
---

## Key Insight

OBT excels as a downstream reporting layer built on top of a Kimball core, not as a standalone architecture. The "OBT as modern default" claim is not well-supported — it originated around 2021-2022 from BigQuery's limited joining capabilities, a platform constraint rather than an architectural principle.

## What OBT Is

OBT consolidates a fact table with most dimensional attributes as additional columns into a single wide, denormalized table. It "simplifies querying by reducing the need for multiple joins" and "enhances query response time, notably with column encoding and without joins."

In columnar databases, wider tables do not increase scan cost because the engine skips columns not referenced in the query. SIMD processing allows "thousands of values per CPU tick." The design heuristic: "Design for the queries you'll run most often, not the data you'll edit."

## Where OBT Works

- **BI tools without relationship support** (Preset, some embedded analytics)
- **CSV exports and flat API responses**
- **Rapid prototyping and proof of concept**
- **Databricks with Liquid Clustering** — achieved >20x task speedup, reducing query time from 3.5s to 1.13s. An optimized OBT (1.13s) outperformed a standard relational model (2.6s).

## Where OBT Fails

**Dimension change cascades.** When a product is renamed in a star schema, one row updates in the dimension table. In OBT, that name might exist in millions of rows, requiring reloading or updating every occurrence. OBTs require manual MERGE statements that "become operationally expensive as tables grow."

**SCD awkwardness.** Managing slowly changing dimensions in OBT means full SCD history creates multiple wide rows per entity, exploding table size and complexity.

**Governance drift.** Without explicit facts, dimensions, and conformed definitions, concepts like "Customer" or "Region" drift across multiple OBTs.

**PII blast radius.** OBTs "concentrate all data including PII into single assets," increasing the blast radius of misconfigured permissions. Star schemas inherently reduce this risk by segregating sensitive data into specific dimension tables.

**Storage overhead.** TPC-H conversion from normalized to wide table inflated storage from 26GB to 164GB (6.3x).

## The "OBT as Default" Claim Is Weak

Blockmill disputes it directly: "Some people say with modern compute power and cheap storage, this is the 'One size fits all'. I disagree." Alibaba Cloud's DuckDB analysis concludes organizations can "abandon the complex and cumbersome wide table model" in favor of "efficient queries directly against normalized star or snowflake schemas."

ACH analysis found 7 items of evidence inconsistent with OBT as a default, versus only 3 inconsistent with Kimball.

## The Evidence-Backed Pattern: Hybrid

Brooklyn Data's production approach: Kimball fact/dimension tables flow into OBT data marts for BI consumption. Using Kimball models as the upstream source-of-truth reduces redundancy issues when OBT layers remain downstream.

Dhristhi recommends the same layered approach:
1. Build Silver OBTs for rapid integration and immediate data science value
2. Create Gold star schemas once requirements stabilize
3. Apply platform optimizations (Liquid Clustering, Unity Catalog) to all large tables

## Takeaway

Use OBT as a serving layer, not a modeling strategy. Build Kimball facts and dimensions as your source of truth, then flatten into OBTs where specific consumers need it. The hybrid pattern gives you the query simplicity of OBT with the governance and maintainability of dimensional modeling.
