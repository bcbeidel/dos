# Consumption-Driven Architecture Heuristics

Three dimensions of consumer behavior map to three architecture decisions. These are strong defaults, not deterministic rules — mixed workloads create exceptions.

## Query Shape -> Modeling Choice

| Query Pattern | Recommended Model | Reasoning |
|---|---|---|
| Join-heavy multidimensional analytics | Star schema | OLAP engines implement star-join optimizations; pre-joined dimensions with normalized facts |
| Scan-heavy columnar queries | Wide flat table (OBT) | Columnar engines only scan referenced columns; width irrelevant to query cost |
| High-cardinality entity lookups | Entity-centric model | Partition on lookup key; may need separate serving layer |
| Ad-hoc exploration (unpredictable) | Star schema (default) | Supports both simple lookups and complex joins; easier to restructure |

**Design heuristic:** Denormalize data when it appears in WHERE, GROUP BY, or SELECT clauses. Design for the queries you run most often, not the data you edit.

## Freshness Needs -> Ingestion Strategy

| Freshness Need | Approach | Typical Use Cases |
|---|---|---|
| 24+ hours | Full refresh or daily batch | Financial reporting, regulatory compliance |
| 1-24 hours | Incremental batch (append/merge) | Operational dashboards, CRM pipeline |
| 1-60 minutes | Micro-batch or incremental update | User activity feeds, campaign monitoring |
| Sub-minute | Streaming (Kafka, Flink) | Fraud detection, recommendations |

Incremental batch gives 80-90% of streaming's freshness benefit at much lower cost. Default to incremental batch; upgrade to streaming only when sub-minute freshness is a validated requirement.

**Key question:** "What business decision changes if the data is 5 minutes old instead of 5 seconds old?"

## Consumer SLA -> Pipeline Investment

| Tier | Characteristics | Failure Mode |
|---|---|---|
| **Prototype** | Ad-hoc exploration, internal data science. No SLA, no contract, minimal monitoring. | "The data is wrong, I'll re-run it." |
| **Production-grade** | External consumers, financial reporting, ML training. Formal SLA, data contracts, retry logic. | "The data was late by 15 minutes, within error budget." |

Pipeline investment should be proportional to consumer dependency.

## Three Anti-Patterns

1. **Premature streaming** — Building streaming when daily batch meets the actual requirement. Streaming costs 5-10x more.
2. **Over-normalization** — Complex dimensional models when consumers run simple queries a wide table would serve.
3. **Universal SLAs** — Same SLA for every data product regardless of criticality. Use tiered SLAs.

## Decision Rules

1. Document the dominant query pattern before choosing a data model.
2. Quantify freshness in minutes/hours, not adjectives.
3. Classify each data product as prototype or production-grade.
4. Match pipeline investment to the tier.
