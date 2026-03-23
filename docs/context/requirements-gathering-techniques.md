---
name: Requirements Gathering Techniques
description: "Requirements gathering is a social discipline, not a documentation exercise -- stakeholder interviews and workshops outperform surveys; the Data Product Canvas provides an eight-block framework for collaborative scoping starting from consumers; MoSCoW prioritization forces explicit descoping decisions that prevent scope creep"
type: context
related:
  - docs/research/2026-03-22-data-product-scoping.research.md
  - docs/context/consumption-driven-architecture.md
  - docs/context/data-contracts.md
  - docs/context/data-product-lifecycle.md
---

## Key Takeaway

The dominant failure mode in data projects is building the right technology for the wrong requirements. Requirements gathering is fundamentally social -- it requires sustained conversation with stakeholders who often cannot articulate what they need because they lack vocabulary for data concepts like freshness, granularity, and completeness. Structure the social process with frameworks (Data Product Canvas, MoSCoW), but never substitute documentation for conversation.

## Three Techniques That Work

1. **Semi-structured stakeholder interviews** -- Open-ended conversations guided by a question framework, not a fixed script. Ask about business decisions the stakeholder makes, what data they look at, and what happens when the data is wrong or late. This surfaces implicit requirements that surveys miss.

2. **Collaborative workshops** -- Multi-stakeholder sessions using visual frameworks (e.g., the Data Product Canvas) to co-create requirements. Workshops surface conflicting assumptions between stakeholders -- e.g., marketing expects hourly refresh while finance expects nightly -- that would otherwise emerge as production incidents.

3. **Observation and reverse-engineering** -- Review existing dashboards, SQL queries, spreadsheets, and ad-hoc exports to understand how data is actually consumed, not how stakeholders say it is consumed. Query logs (BigQuery INFORMATION_SCHEMA.JOBS, Snowflake QUERY_HISTORY) reveal actual access patterns, join frequencies, and filter usage that directly inform modeling and materialization decisions.

## The Data Product Canvas

Eight building blocks completed in sequence, deliberately starting with consumers before sources and architecture:

1. **Domain** -- Who owns and maintains this data product
2. **Data Product Name** -- Unique identifier following naming conventions
3. **Consumer and Use Case(s)** -- Who consumes this and for what analytical purpose
4. **Data Contract** -- Output ports, formats, protocols, data models, semantics, usage terms
5. **Sources** -- Input mechanisms and data origins
6. **Data Product Architecture** -- Internal design: ingestion, storage, transformations
7. **Ubiquitous Language** -- Shared domain terminology
8. **Classification** -- Source-aligned, aggregate, or consumer-aligned

The ordering enforces consumption-driven design: define who needs what before deciding how to build it. The canvas was designed for data mesh contexts and does not explicitly address cost constraints, pipeline complexity estimates, or operational burden. Augment it with feasibility analysis.

## MoSCoW Prioritization

When multiple consumers have competing requirements, MoSCoW forces explicit priority decisions:

- **Must have** -- Requirements without which the data product has no value (e.g., "must include order ID and customer ID")
- **Should have** -- Important requirements deliverable iteratively (e.g., "should include product category enrichment")
- **Could have** -- Nice-to-haves deprioritized under pressure (e.g., "could include historical trend calculations")
- **Won't have** -- Explicitly descoped for future consideration (e.g., "won't include real-time streaming in v1")

Explicit descoping prevents scope creep -- the single largest source of data project delays.

## Consumption-First Traversal

Requirements gathering should work the data engineering lifecycle (Generation -> Ingestion -> Transformation -> Serving -> Consumption) backward. Start at Consumption: What decisions do consumers make? What data do they need? Then work backward through Serving, Transformation, Ingestion, and Generation constraints. This prevents the dominant anti-pattern of building pipelines source-forward and discovering at delivery that the output does not match consumer expectations.

## Decision Rules

1. Interview stakeholders before writing a single line of pipeline code. Ask about decisions, not data.
2. Use the Data Product Canvas in workshops to surface conflicting assumptions early.
3. Apply MoSCoW to every requirements list -- unstated "Won't have" items become implicit commitments.
4. Review actual query logs alongside stated requirements. What people do with data and what they say they do often diverge.
