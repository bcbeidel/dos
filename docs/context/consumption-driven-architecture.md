---
name: Consumption-Driven Architecture
description: "Three consumption dimensions drive architecture decisions through predictable heuristics: query shape determines modeling choice (join-heavy -> star schema, scan-heavy -> wide table), freshness needs determine ingestion strategy (daily -> batch, sub-minute -> streaming), and consumer SLA criticality determines pipeline investment level (prototype vs production-grade)"
type: context
related:
  - docs/research/2026-03-22-data-product-scoping.research.md
  - docs/context/requirements-gathering-techniques.md
  - docs/context/data-model-selection.md
  - docs/context/incremental-loading-patterns.md
  - docs/context/data-freshness-slas.md
---

## Key Takeaway

Architecture should be derived from consumption patterns, not chosen upfront. Three dimensions of consumer behavior map predictably to three architecture decisions. These heuristics are not deterministic -- mixed workloads create exceptions -- but they provide strong defaults that prevent both over-engineering and under-engineering.

## Query Shape -> Modeling Choice

| Query Pattern | Model | Reasoning |
|---|---|---|
| Join-heavy multidimensional analytics ("revenue by category by region by quarter") | Star schema | OLAP engines implement star-join optimizations; pre-joined dimensions with normalized facts |
| Scan-heavy columnar queries ("all attributes of users who purchased in 30 days") | Wide flat table (OBT) | Columnar engines only scan referenced columns; width is irrelevant to query cost; fewer joins |
| High-cardinality entity lookups ("all events for user X") | Entity-centric model | Partition on lookup key; different access pattern from analytical aggregation; may need separate serving layer |
| Ad-hoc exploration (unpredictable patterns) | Star schema (default) | Supports both simple lookups and complex joins; easier to restructure than wide tables |

The design heuristic: denormalize data when it appears in WHERE, GROUP BY, or SELECT clauses. Design for the queries you run most often, not the data you edit.

Mixed workloads where some consumers need star-schema joins and others need wide-table scans require either multiple materializations or a compromise model. The heuristic works for dominant query patterns but breaks down for heterogeneous consumers.

## Freshness Needs -> Ingestion Strategy

| Freshness Need | Approach | Typical Use Cases |
|---|---|---|
| 24+ hours | Full refresh or daily batch | Financial reporting, regulatory compliance |
| 1-24 hours | Incremental batch (append/merge) | Operational dashboards, CRM pipeline |
| 1-60 minutes | Micro-batch or incremental update | User activity feeds, campaign monitoring |
| Sub-minute | Streaming (Kafka, Flink, Spark Structured Streaming) | Fraud detection, recommendations |

Incremental batch gives 80-90% of streaming's freshness benefit at much lower cost and operational complexity. Default to incremental batch and upgrade to streaming only when sub-minute freshness is a validated requirement.

Most "real-time" requirements are actually "hourly" or "5-minute" when quantified. The correct practice: ask "What business decision changes if the data is 5 minutes old instead of 5 seconds old?" Do not assume the stakeholder is wrong, but do quantify before building streaming infrastructure that costs 5-10x more to build and operate.

## Consumer SLAs -> Pipeline Investment Level

Two distinct tiers of pipeline maturity, driven by consumer dependency:

**Prototype** -- Ad-hoc exploration, internal data science experimentation. No SLA, no data contract, minimal monitoring. Acceptable failure mode: "the data is wrong, I'll re-run it."

**Production-grade** -- External consumers, financial reporting, ML model training. Formal SLA, data contracts, comprehensive monitoring, retry logic, and change management. Acceptable failure mode: "the data was late by 15 minutes, within error budget."

Pipeline investment should be proportional to consumer dependency on the data. Financial reporting and ML models warrant production-grade investment. Ad-hoc exploration can remain prototype-stage.

## Three Anti-Patterns from Misaligned Requirements

1. **Premature streaming** -- Building streaming infrastructure when daily batch meets the actual freshness requirement. Streaming costs 5-10x more for equivalent data volume.
2. **Over-normalization** -- Building complex dimensional models when consumers run simple queries a wide table would serve better. Let the query pattern dictate the model.
3. **Universal SLAs** -- Applying the same SLA to every data product regardless of criticality. Tiered SLAs (critical/standard/best-effort) allocate engineering effort proportionally to business impact.

## Decision Rules

1. Document the dominant query pattern before choosing a data model.
2. Quantify freshness requirements in minutes/hours, not adjectives like "real-time."
3. Classify each data product as prototype or production-grade based on consumer dependency.
4. Match pipeline investment to the tier -- do not build production-grade infrastructure for prototype consumers.
