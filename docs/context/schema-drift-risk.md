---
name: Schema Drift Risk
description: "Schema drift causes 7.8% of data quality incidents with 27% compounding per percentage-point increase in drift rate; pre-onboarding assessment should measure change frequency, notification process, and version control; the 7.8% figure understates true impact because drift triggers cascading failures categorized elsewhere"
type: context
related:
  - docs/research/2026-03-22-data-discovery.research.md
  - docs/context/schema-evolution.md
  - docs/context/source-system-evaluation.md
  - docs/context/data-contracts.md
  - docs/context/data-observability-pillars.md
---

## Key Takeaway

Schema drift is not an abstract risk -- it is measurable and its impact compounds. At 7.8% of data quality incidents and 27% compounding per percentage-point increase in drift rate, schema stability directly predicts pipeline reliability. The 7.8% figure understates the true impact because drift often triggers cascading failures categorized under "pipeline execution faults" (26.2%) or "ingestion disruptions" (16.6%). Assess schema stability before onboarding any source. Discover it through measurement, not through your first production incident.

## Quantified Impact

Monte Carlo's analysis of 11M+ monitored tables:

- Schema drift accounts for **7.8% of all data quality incidents**
- Production incidents increase **27% for each percentage-point increase in schema drift rate**
- Teams average **67 data incidents per month**, with 68% taking 4+ hours to detect and 15 hours average to resolve
- **1 data quality issue per 10 tables annually** (up from 1 per 15 in 2020-2023)

Schema drift is particularly dangerous because it causes silent data corruption. A pipeline may not fail outright but instead produce truncated, misaligned, or incorrectly typed data. A column type change from integer to string can flow through transformation layers without raising errors while producing incorrect analytical results.

## Pre-Onboarding Assessment Criteria

Before onboarding a source, evaluate four factors:

1. **Schema change frequency** -- Track field additions/deletions over time. SaaS APIs may change monthly; stable transactional databases change quarterly or less.
2. **Change notification process** -- Does the source owner inform consumers before changes? Even a Slack notification when a migration touches a pipeline-feeding table is sufficient.
3. **Change documentation** -- Are schema changes version-controlled and logged? Track modifications similar to software code.
4. **Historical stability** -- What is the schema-drift incident count over the past 6-12 months? This identifies unstable data providers.

Sources that fail these criteria require defensive pipeline design: schema validation at ingestion, quarantine tables for unexpected fields, and contract modes that halt or degrade gracefully rather than silently propagating changes.

## Five Prevention Strategies

1. **Schema validation before loading** -- Compare incoming data structure against the expected schema contract before writing to destination.
2. **Schema tracking and versioning** -- Maintain metadata snapshots and version-control schema definitions.
3. **Quarantine unexpected fields** -- Isolate unknown columns rather than silently ingesting them.
4. **Change logging** -- Document when and why structural changes occur.
5. **Regular pipeline reviews** -- Monitor shared data sources for cascading schema impacts.

## SaaS APIs: The Highest-Risk Source Type

SaaS APIs are the most schema-volatile source type. Vendors change APIs without notice, deprecate endpoints, and impose breaking schema changes. A source with a 3% monthly schema change rate does not produce a 3% incident rate -- it produces a systematically degrading reliability profile due to the 27% compounding effect. Managed connectors (Airbyte, Fivetran) absorb some of this volatility but introduce their own lag in adapting to vendor changes.

## Relationship to Schema Evolution

Schema drift risk assessment (this file) determines *whether* a source is stable enough to onboard and what defenses are needed. Schema evolution (see related) addresses *how* to handle changes once they occur -- compatibility rules, the expand-and-contract pattern, and tool-specific behavior in dbt/dlt/Delta Lake.
