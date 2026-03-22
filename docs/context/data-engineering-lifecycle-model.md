---
name: "Data Engineering Lifecycle Model"
description: "Reis & Housley's lifecycle (Generation, Storage, Ingestion, Transformation, Serving + six undercurrents) is the organizing spine for data engineering work; DAMA-DMBOK provides the governance taxonomy overlay; DDIA and Kimball are domain-depth references, not competing frameworks."
type: context
related:
  - docs/research/2026-03-22-canonical-frameworks-lifecycle.research.md
  - docs/context/kimball-dimensional-modeling.md
  - docs/context/data-governance-foundations.md
  - docs/context/medallion-architecture.md
---

## Selected Model: Reis & Housley Data Engineering Lifecycle

The Reis & Housley lifecycle is the canonical organizing framework for modern data engineering. It structures work into five stages and six cross-cutting undercurrents that together cover the full scope of data engineering from source to consumer.

**Five lifecycle stages:**
1. **Generation** -- data creation at source systems (databases, APIs, IoT, SaaS)
2. **Storage** -- foundational layer underlying ingestion, transformation, and serving
3. **Ingestion** -- moving data from sources into processing/storage platforms
4. **Transformation** -- converting raw data into formats useful for analytics, ML, operations
5. **Serving** -- delivering processed data via BI, ML models, reverse ETL, APIs

**Six undercurrents** (cross-cutting concerns spanning all stages):
1. Security
2. Data management
3. DataOps
4. Data architecture
5. Orchestration
6. Software engineering

## Why This Model

The Reis lifecycle satisfies four criteria that no alternative framework matches:

- **Lifecycle completeness.** Covers source-to-consumer with no major engineering activity falling outside the framework.
- **Stage granularity.** Each stage maps directly to distinct tool categories -- dlt/Airbyte for ingestion, dbt/Spark for transformation, orchestrators as the cross-cutting concern. Skills can be unambiguously tagged to a stage.
- **Cross-cutting support.** The undercurrents model concerns like orchestration and security as spanning all stages, matching how engineers actually experience them.
- **Community consensus.** Structures the DeepLearning.AI/AWS Coursera certification, referenced across universities and Fortune 500 companies, sustained O'Reilly bestseller for 2.5+ years, independently reproduced by practitioners worldwide.

No competing framework provides equivalent coverage. The Kimball lifecycle is data-warehousing-specific. DAMA-DMBOK is enterprise-management-scoped. DDIA has no lifecycle structure. Data Mesh is organizational architecture, not a workflow lifecycle.

## Canonical Reference Set

The four frameworks are complementary, not competing:

| Role | Framework | Scope |
|------|-----------|-------|
| Organizing spine | Reis & Housley lifecycle | Full engineering workflow |
| Governance overlay | DAMA-DMBOK 11 knowledge areas | Data management taxonomy within the "data management" undercurrent |
| Distributed systems depth | Kleppmann's DDIA (2nd ed, 2026) | Storage internals, replication, consistency, batch/stream theory |
| Dimensional modeling | Kimball four-step process | Star schemas, conformed dimensions, SCDs within the Transformation stage |

## Known Gaps

The Reis lifecycle does not address ML/AI engineering as a first-class lifecycle element. ML serving appears under the Serving stage, but feature engineering, model training, and model monitoring are absent. As data engineering increasingly overlaps with ML engineering (feature stores, training data pipelines), this gap may require extension -- either a seventh undercurrent or an explicit ML sub-lifecycle.

The framework is intentionally technology-agnostic and provides no runnable code, configuration, or implementation patterns. It tells you what stages exist and why; tool selection and architecture decisions (medallion, star schema, data vault) require separate guidance.

## Takeaway

Use the Reis lifecycle stages as the top-level organizational spine. Tag engineering skills to stages and undercurrents. Layer DAMA knowledge areas into governance-related skills. Reference DDIA for storage and systems decisions. Reference Kimball for dimensional modeling within transformation. This layered approach provides navigational structure (Reis) with domain depth (DAMA, DDIA, Kimball) where each framework is strongest.
