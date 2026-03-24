# Consumption-to-Architecture Heuristics

Architecture should be derived from consumption patterns, not chosen upfront. Three dimensions of consumer behavior map predictably to architecture decisions.

## Query Shape -> Modeling Choice

| Query Pattern | Recommended Model | Reasoning |
|---|---|---|
| Join-heavy multidimensional analytics | Star schema | OLAP engines implement star-join optimizations; pre-joined dimensions |
| Scan-heavy columnar queries | Wide flat table (OBT) | Columnar engines only scan referenced columns; width is irrelevant |
| High-cardinality entity lookups | Entity-centric model | Partition on lookup key; may need separate serving layer |
| Ad-hoc exploration | Star schema (default) | Supports both simple lookups and complex joins |

**Heuristic:** Denormalize data when it appears in WHERE, GROUP BY, or SELECT clauses. Design for the queries you run most often. Mixed workloads with heterogeneous consumers may require multiple materializations.

## Freshness Needs -> Ingestion Strategy

| Freshness Need | Approach | Typical Use Cases |
|---|---|---|
| 24+ hours | Full refresh or daily batch | Financial reporting, regulatory compliance |
| 1-24 hours | Incremental batch (append/merge) | Operational dashboards, CRM pipeline |
| 1-60 minutes | Micro-batch or incremental update | User activity feeds, campaign monitoring |
| Sub-minute | Streaming (Kafka, Flink) | Fraud detection, recommendations |

Incremental batch gives 80-90% of streaming's freshness benefit at much lower cost. Default to incremental batch and upgrade to streaming only when sub-minute freshness is validated.

**Key question:** "What business decision changes if the data is 5 minutes old instead of 5 seconds old?"

## Consumer SLAs -> Pipeline Investment

| Tier | Characteristics | Acceptable Failure |
|---|---|---|
| Prototype | Ad-hoc, no SLA, minimal monitoring | "Data is wrong, I'll re-run it" |
| Production-grade | Formal SLA, data contracts, retry logic, change management | "Data was late by 15 min, within error budget" |

Pipeline investment should be proportional to consumer dependency.

## Anti-Patterns from Misaligned Requirements

1. **Premature streaming** -- Building streaming when daily batch meets freshness needs. Costs 5-10x more.
2. **Over-normalization** -- Complex dimensional models when consumers run simple wide-table queries.
3. **Universal SLAs** -- Same SLA for every data product regardless of criticality. Use tiered SLAs.

## Decision Rules

1. Document the dominant query pattern before choosing a data model.
2. Quantify freshness in minutes/hours, not adjectives like "real-time."
3. Classify each data product as prototype or production-grade based on consumer dependency.
4. Match pipeline investment to the tier.
