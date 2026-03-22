---
name: "Data Product Scoping & Business Requirements"
description: "Requirements gathering is a social discipline, not a documentation exercise — stakeholder interviews and workshops outperform written surveys for data contexts; the Data Product Canvas provides a structured eight-block framework (domain, consumers, data contract, sources, architecture, ubiquitous language, classification) for collaborative scoping; consumption patterns should drive architecture: query shape determines modeling choice (joins → star schema, scan-heavy → wide table), freshness needs determine incremental strategy (daily → batch, sub-minute → streaming), and consumer SLAs determine pipeline investment level; consumer-defined data contracts invert the traditional approach by placing requirements at the consumption point, not the production point; data product versioning follows semantic versioning with backward compatibility as the default — breaking changes require deprecation windows and migration paths; the SLI/SLO/SLA hierarchy borrowed from SRE provides the measurement framework for data product reliability; the Data Engineering Lifecycle (Generation→Ingestion→Transformation→Serving→Consumption) frames requirements gathering as starting from Consumption and working backward through the lifecycle"
type: research
sources:
  - https://dataconomy.com/2024/12/17/effective-strategies-for-gathering-requirements-in-your-data-project/
  - https://www.getdbt.com/blog/data-product-slas-and-slos
  - https://www.datamesh-architecture.com/data-product-canvas
  - https://www.equalexperts.com/blog/data/what-is-a-data-product-owner-responsibilities-challenges-and-best-practices/
  - https://dataproducts.substack.com/p/the-production-grade-data-pipeline
  - https://dataproducts.substack.com/p/the-consumer-defined-data-contract
  - https://martinfowler.com/articles/data-mesh-principles.html
  - https://moderndata101.substack.com/p/managing-the-evolving-data-products-landscape-p2
  - https://www.owox.com/blog/articles/real-time-data-freshness-slas
  - https://www.bigeye.com/blog/defining-data-quality-with-slas
  - https://cloud.google.com/discover/what-is-data-as-a-product
  - https://www.ovaledge.com/blog/data-product-strategy-guide
  - https://www.alation.com/blog/data-product-lifecycle/
  - https://www.fiveonefour.com/blog/OLAP-on-Tap-The-Art-of-Letting-Go-of-Normalization
  - https://www.onehouse.ai/blog/choosing-the-right-data-ingestion-method-batch-streaming-and-hybrid-approaches
  - https://longdatadevlog.com/brain/product-requirement-document-template/
  - https://www.ascend.io/blog/the-anti-pattern-in-big-data
  - https://www.getdbt.com/blog/data-slas-best-practices
  - https://www.confluent.io/learn/data-product/
  - https://bitol-io.github.io/open-data-contract-standard/v3.0.0/
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-operations-reliability.research.md
  - docs/research/2026-03-22-quality-engineering.research.md
  - docs/research/2026-03-22-data-discovery.research.md
  - docs/research/2026-03-22-pipeline-design-architecture.research.md
  - docs/research/2026-03-22-data-modeling.research.md
---

## Summary

**Research question:** How should data engineers scope, document, and manage business requirements for data products — and how do requirements drive architecture decisions?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 20 | **Searches:** 12 across Google

**Key findings:**
- Requirements gathering is a social discipline, not a documentation exercise — stakeholder interviews and collaborative workshops produce higher-fidelity requirements than written surveys or assumption-driven design, and the MoSCoW method (Must/Should/Could/Won't) provides a practical prioritization framework for competing consumer demands
- The Data Product Canvas provides an eight-block structured framework (domain, consumers/use cases, data contract, sources, architecture, ubiquitous language, classification) for collaborative data product scoping — starting from consumers, not sources
- Consumption patterns should drive architecture decisions: query shape determines modeling choice (join-heavy analytics → star schema; scan-heavy columnar queries → wide flat tables), freshness needs determine ingestion strategy (daily tolerance → batch; sub-minute → streaming), and consumer SLAs determine pipeline investment level
- Consumer-defined data contracts invert the traditional approach — requirements originate at the consumption point, not the production point, because producers lack visibility into downstream usage patterns and expectations
- Data product versioning follows semantic versioning with backward compatibility as the default; breaking changes require deprecation windows, dual-write migration periods, and explicit consumer notification
- The SLI/SLO/SLA hierarchy borrowed from SRE provides the measurement framework for data product reliability, with error budgets translating business commitments into measurable targets with acceptable violation rates

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://dataconomy.com/2024/12/17/effective-strategies-for-gathering-requirements-in-your-data-project/ | Effective strategies for gathering requirements in data projects | Dataconomy | 2024 | T5 | verified — practitioner article |
| 2 | https://www.getdbt.com/blog/data-product-slas-and-slos | How to ensure data product SLAs and SLOs | dbt Labs | 2024 | T4 | verified — vendor blog |
| 3 | https://www.datamesh-architecture.com/data-product-canvas | Data Product Canvas | datamesh-architecture.com (Visengeriyeva) | current | T3 | verified — community framework |
| 4 | https://www.equalexperts.com/blog/data/what-is-a-data-product-owner-responsibilities-challenges-and-best-practices/ | What is a Data Product Owner? | Equal Experts | 2024 | T4 | verified — consultancy blog |
| 5 | https://dataproducts.substack.com/p/the-production-grade-data-pipeline | The Production-Grade Data Pipeline | Chad Sanderson | 2024 | T3 | verified — industry practitioner |
| 6 | https://dataproducts.substack.com/p/the-consumer-defined-data-contract | The Consumer-Defined Data Contract | Chad Sanderson | 2024 | T3 | verified — industry practitioner |
| 7 | https://martinfowler.com/articles/data-mesh-principles.html | Data Mesh Principles | Zhamak Dehghani / Martin Fowler | 2020 | T2 | verified — foundational reference |
| 8 | https://moderndata101.substack.com/p/managing-the-evolving-data-products-landscape-p2 | Versioning, Cataloging, and Decommissioning Data Products | ModernData101 | 2024 | T5 | verified — practitioner blog |
| 9 | https://www.owox.com/blog/articles/real-time-data-freshness-slas | Defining Data Freshness SLAs for Business Users | OWOX | 2024 | T4 | verified — vendor blog |
| 10 | https://www.bigeye.com/blog/defining-data-quality-with-slas | Defining data quality with SLAs | Bigeye | 2024 | T4 | verified — vendor blog |
| 11 | https://cloud.google.com/discover/what-is-data-as-a-product | What is data as a product (DaaP)? | Google Cloud | current | T2 | verified — cloud provider docs |
| 12 | https://www.ovaledge.com/blog/data-product-strategy-guide | Data Product Strategy: Build for Value in 2026 | OvalEdge | 2026 | T4 | verified — vendor blog |
| 13 | https://www.alation.com/blog/data-product-lifecycle/ | Stages of the Data Product Lifecycle | Alation | 2024 | T4 | verified — vendor blog |
| 14 | https://www.fiveonefour.com/blog/OLAP-on-Tap-The-Art-of-Letting-Go-of-Normalization | OLAP Schema Design: Why Wide Flat Tables Beat Star Schemas | FiveOneFour | 2024 | T5 | verified — practitioner blog |
| 15 | https://www.onehouse.ai/blog/choosing-the-right-data-ingestion-method-batch-streaming-and-hybrid-approaches | Choosing the Right Data Ingestion Method | Onehouse | 2024 | T4 | verified — vendor blog |
| 16 | https://longdatadevlog.com/brain/product-requirement-document-template/ | Data Product Requirement Document Template | Long Bui | 2024 | T5 | verified — practitioner blog |
| 17 | https://www.ascend.io/blog/the-anti-pattern-in-big-data | The Anti-Pattern in Big Data | Ascend | 2024 | T4 | verified — vendor blog |
| 18 | https://www.getdbt.com/blog/data-slas-best-practices | What are data SLAs? Best practices | dbt Labs | 2024 | T4 | verified — vendor blog |
| 19 | https://www.confluent.io/learn/data-product/ | Understanding Data Products | Confluent | current | T4 | verified — vendor docs |
| 20 | https://bitol-io.github.io/open-data-contract-standard/v3.0.0/ | Open Data Contract Standard (ODCS) v3.0 | BITOL / Linux Foundation | current | T2 | verified — open standard |

---

## Sub-question 1: Stakeholder Requirement Gathering Techniques for Data Contexts

### Requirements gathering is social, not procedural

The dominant failure mode in data projects is not choosing the wrong technology — it is building the right technology for the wrong requirements. Effective requirements gathering for data products is fundamentally a social discipline: it requires sustained conversation with stakeholders who often cannot articulate what they need because they lack vocabulary for data concepts like freshness, granularity, and completeness [1][4].

Three techniques consistently produce high-fidelity requirements in data contexts:

1. **Semi-structured stakeholder interviews** — Open-ended conversations guided by a question framework rather than a fixed script. The interviewer asks about business decisions the stakeholder makes, what data they look at to make those decisions, and what happens when the data is wrong or late. This surfaces implicit requirements that surveys miss [1].

2. **Collaborative workshops** — Multi-stakeholder sessions using visual frameworks (e.g., the Data Product Canvas) to co-create requirements. Workshops surface conflicting assumptions between stakeholders — e.g., marketing expects hourly refresh while finance expects nightly — that would otherwise emerge as production incidents [1][3].

3. **Observation and reverse-engineering** — Reviewing existing dashboards, SQL queries, spreadsheet workflows, and ad-hoc data exports to understand how data is actually consumed, not how stakeholders say it is consumed. Query logs from BigQuery, Snowflake, or BI tools reveal actual access patterns, join frequencies, and filter usage that directly inform modeling and materialization decisions [14].

### The Data Product Canvas

The Data Product Canvas, developed by Larysa Visengeriyeva, provides a structured framework for collaborative data product scoping [3]. It comprises eight building blocks completed in sequence:

1. **Domain** — Who owns and maintains this data product
2. **Data Product Name** — Unique identifier following organizational naming conventions
3. **Consumer and Use Case(s)** — Who consumes this product and for what analytical purpose
4. **Data Contract** — Output ports, formats, protocols, data models, semantics, usage terms
5. **Sources** — Input mechanisms and data origins
6. **Data Product Architecture** — Internal design: ingestion, storage, transformations
7. **Ubiquitous Language** — Shared domain terminology among stakeholders
8. **Classification** — Source-aligned, aggregate, or consumer-aligned

The canvas deliberately starts with consumers and use cases (block 3) before sources (block 5) and architecture (block 6). This ordering enforces consumption-driven design — teams define who needs what before deciding how to build it.

### MoSCoW prioritization for competing requirements

When multiple consumers have competing requirements — different freshness needs, different granularity expectations, conflicting SLA demands — the MoSCoW method provides a practical prioritization framework [1]:

- **Must have** — Requirements without which the data product has no value (e.g., "must include order ID and customer ID")
- **Should have** — Important requirements that can be delivered iteratively (e.g., "should include product category enrichment")
- **Could have** — Nice-to-have requirements deprioritized under time or cost pressure (e.g., "could include historical trend calculations")
- **Won't have** — Explicitly descoped requirements documented for future consideration (e.g., "won't include real-time streaming in v1")

This framework forces explicit descoping decisions that prevent scope creep — the single largest source of data project delays.

---

## Sub-question 2: Use Case Documentation (Query Patterns, Update Frequency, Consumer SLAs)

### Documenting consumption patterns

A data product requirement document must capture five consumption dimensions that directly drive architecture decisions [2][9][16]:

1. **Query patterns** — What questions will consumers ask? What columns appear in WHERE, GROUP BY, and JOIN clauses? What aggregation granularity is needed (daily, hourly, per-transaction)? These patterns determine partitioning strategy, indexing, and whether a star schema or wide table is appropriate.

2. **Update frequency** — How fresh must the data be? "Real-time" is almost never the actual requirement — most "we need real-time" requests are actually "we need hourly" or "we need 5-minute" requests [15]. Specific freshness tiers by business function [9]:
   - Marketing campaigns: hourly refresh
   - Sales CRM: daily refresh by 8 AM
   - Financial reporting: nightly after business hours
   - Strategic planning: weekly or monthly

3. **Consumer SLAs** — What is the acceptable downtime? What happens when data is late? Consumer-facing dashboards displaying real-time metrics require more stringent SLAs than internal reporting used for monthly planning [2][18].

4. **Volume and cardinality** — How many rows? How many distinct values in key columns? This determines storage format, compression strategy, and whether materialized views or pre-aggregations are needed.

5. **Access patterns** — Interactive queries via BI tool? Programmatic API access? Batch export? Each pattern implies different infrastructure and SLA commitments.

### Freshness SLA tiers

Data freshness SLAs should be documented as formal agreements specifying dataset name, refresh time, frequency, and responsible owner [9]. The key insight is that not every dataset needs constant updates — an hourly ad refresh might cost 8-10x more than a daily schedule but rarely changes outcomes. Match frequency to business value, not to technical capability.

Once historical data is verified, it should remain unchanged. Only new periods continue refreshing. Adding "last updated" timestamps to dashboards eliminates confusion about data currency and builds stakeholder confidence [9].

### SLI/SLO/SLA hierarchy

The SRE-derived hierarchy provides the measurement framework [10][18]:

- **SLI (Service Level Indicator)** — The measured metric: hours since dataset refresh, percentage of values matching required patterns, null value rate in critical fields. SLIs should follow a consistent ratio format: `(# good events) / (# total events)`.
- **SLO (Service Level Objective)** — The internal target: "less than 6 hours since dataset refreshed," "at least 99.9% of values match required format."
- **SLA (Service Level Agreement)** — The contractual commitment combining multiple SLOs with error budgets. A 99.9% uptime SLA permits approximately 43 minutes and 50 seconds of monthly failures.

Error budgets translate these commitments into actionable priorities: when the budget is consumed, teams shift from feature work to reliability work. Burn rate monitoring — how quickly the error budget is being consumed — provides early warning before SLA breach [10].

---

## Sub-question 3: Reverse-Engineering Architecture Choices from Consumption Patterns

### Query shape determines modeling choice

The mapping from consumption pattern to data model is not arbitrary — it follows predictable rules [14]:

**Join-heavy analytical queries** (e.g., "revenue by product category by region by quarter") → **Star schema**. Star schemas optimize for multidimensional slicing by pre-joining dimensions into denormalized tables while keeping the fact table normalized. Most OLAP engines implement "star-join" optimizations for this pattern.

**Scan-heavy columnar queries** (e.g., "all attributes of users who purchased in the last 30 days") → **Wide flat table (OBT)**. Modern columnar engines (ClickHouse, DuckDB) only scan referenced columns, making table width irrelevant to query cost. Fewer tables mean fewer joins, and columnar compression makes storage duplication cheap. The design heuristic: denormalize data when it appears in WHERE, GROUP BY, or SELECT clauses [14].

**High-cardinality entity lookups** (e.g., "get all events for user X") → **Entity-centric model** with partitioning on the lookup key. This is a fundamentally different access pattern from analytical aggregation and may warrant a separate serving layer.

**Ad-hoc exploration** (unpredictable query patterns) → **Retain flexibility**. Star schemas provide a reasonable default because they support both simple lookups and complex joins. Wide tables are harder to restructure if the wrong columns were denormalized.

The decision rule: "Design for the queries you'll run most often, not the data you'll edit" [14].

### Freshness needs determine incremental strategy

Freshness requirements map directly to ingestion approach [15]:

| Freshness Need | Approach | Typical Use Cases |
|---|---|---|
| 24+ hours | Full refresh or daily batch | Financial reporting, regulatory compliance |
| 1-24 hours | Incremental batch (append/merge) | Operational dashboards, CRM pipeline |
| 1-60 minutes | Micro-batch or incremental update | User activity feeds, campaign monitoring |
| Sub-minute | Streaming (Kafka, Flink, Spark Structured Streaming) | Fraud detection, recommendations |

The critical insight: incremental batch update gives 80-90% of streaming's freshness benefit at much lower cost and operational complexity [15]. Most teams should default to incremental batch and upgrade to streaming only when sub-minute freshness is a validated requirement — not when a stakeholder says "real-time" without quantifying what they mean.

### Consumer SLAs determine pipeline investment level

Chad Sanderson distinguishes prototype pipelines from production-grade pipelines [5]. The distinction is driven by consumer requirements:

- **Prototype** — Ad-hoc exploration, internal data science experimentation. No SLA, no data contract, minimal monitoring. Acceptable failure mode: "the data is wrong, I'll re-run it."
- **Production-grade** — External consumers, financial reporting, ML model training. Formal SLA, data contracts, comprehensive monitoring, retry logic, and change management. Acceptable failure mode: "the data was late by 15 minutes, within error budget."

The investment in pipeline maturity should be proportional to the consumer's dependency on the data. Financial reporting and ML models warrant production-grade investment; ad-hoc exploration can remain prototype-stage [5].

---

## Sub-question 4: Requirement Change Management

### Detecting when consumer needs shift

Consumer needs shift continuously, but teams rarely detect the shift until it surfaces as a production incident. Three mechanisms provide early warning:

1. **Query log analysis** — Monitor actual query patterns in the warehouse (Snowflake QUERY_HISTORY, BigQuery INFORMATION_SCHEMA.JOBS). Look for new tables being joined, new columns appearing in WHERE clauses, new users accessing the data, or increasing query frequency. These signals indicate evolving consumption that may outgrow the current model [14].

2. **Usage analytics** — Track data product adoption metrics: number of active consumers, query frequency, downstream dependency count. Declining usage signals a product approaching retirement; increasing usage signals a product that may need SLA upgrades [12][13].

3. **Stakeholder feedback loops** — Regular (quarterly) reviews with key consumers to assess whether the data product still meets their needs. Domain teams should hold feedback sessions before major enhancements to understand evolving needs contextually [12].

### Propagating changes back through pipeline design

When consumer requirements change, the change must propagate backward through the pipeline — from serving layer to transformation to ingestion. This is where data contracts become essential [6][20].

The Open Data Contract Standard (ODCS v3.0) provides a machine-readable specification for formalizing producer-consumer agreements [20]. A data contract defines:
- **Schema** — Column names, types, nullability, keys (logical and physical representations)
- **Data quality rules** — Freshness, row count expectations, uniqueness, custom SQL checks
- **SLA** — Availability and performance commitments
- **Semantics** — Business meaning of fields and relationships

When a consumer needs a new field, higher freshness, or different granularity, the change request modifies the data contract. The contract change triggers a review of upstream impact: Does the source system provide this field? Does the ingestion frequency need to increase? Does the transformation logic need to change? This structured propagation prevents ad-hoc pipeline modifications that introduce technical debt [5][6].

### Consumer-defined data contracts

Chad Sanderson argues that data contracts should be consumer-defined rather than producer-defined [6]. The reasoning: data producers (application engineers) lack visibility into how downstream teams use their data. A product manager — not an engineer — should define requirements. Similarly, a data product owner — not the source system team — should define what the data contract requires.

Sanderson describes a three-phase maturity model for consumer-defined contracts:

1. **Awareness** — Producers understand when their changes affect consumers through pre-deployment notification
2. **Collaboration** — Producers communicate breaking changes in advance, enabling downstream teams to prepare
3. **Contract ownership** — Producers maintain formal contracts with clear versioning and evolution processes

This approach generates problem visibility that catalyzes organizational culture change around data quality and stewardship [6].

---

## Sub-question 5: Data Product Thinking (Ownership, SLAs, Versioning)

### Data as a product principles

Zhamak Dehghani's data mesh framework defines data as a product through several essential characteristics [7]:

- **Discoverable** — Users can find relevant datasets through catalogs and search
- **Addressable** — Unique, stable identifiers for programmatic access
- **Trustworthy** — Quality metrics visible and actively maintained
- **Self-describing** — Schema, semantics, and usage documentation travel with the data
- **Interoperable** — Standardized interfaces accommodate diverse consumption preferences
- **Secure** — Access controls and governance enforced at the product boundary

The data product is the "architectural quantum" — the smallest independently deployable unit encapsulating code, data/metadata, and infrastructure [7]. This framing applies regardless of whether an organization adopts full data mesh; the product thinking is separable from the organizational model.

### Data product ownership

The Data Product Owner role bridges technical complexity with business outcomes [4]. Core responsibilities:

- **Requirements and prioritization** — Collaborate with business analysts to define specifications, translate business needs into actionable tasks, maintain the product roadmap, and prioritize based on consumer needs
- **Quality stewardship** — Measure and communicate data quality, maintain SLAs for freshness and timeliness, manage upstream data owner relationships
- **Impact measurement** — Define and track KPIs, monitor engagement and usage metrics, report on product value
- **Cost management** — Understand infrastructure expenses, identify optimization opportunities, ensure value exceeds operational cost
- **Communication and adoption** — Promote the product to potential users, translate technical concepts for business stakeholders, manage expectations

The primary challenge is articulating data concepts to non-technical stakeholders who underestimate the complexity behind pipelines, ML models, and analytics infrastructure. Education becomes a core responsibility [4].

### Data product versioning

Six versioning approaches are used in practice [8]:

1. **Semantic versioning (SemVer)** — MAJOR.MINOR.PATCH for data product iterations. MAJOR for breaking schema changes, MINOR for backward-compatible additions, PATCH for quality fixes.
2. **API versioning** — Version control on output port interfaces to maintain backward compatibility
3. **Schema versioning** — Managed schema changes using tools like Avro or Protobuf that support evolution and compatibility rules
4. **Event versioning** — Version identifiers on transmitted data events
5. **Time-based snapshots** — Captures of data product state at specific moments (Snowflake Time Travel, Delta Lake versioning)
6. **Data lineage and metadata management** — Tracking lineage for effective version understanding

Breaking changes require a structured process [8]:
- Announce changes early with explicit timelines
- Provide migration guides and consumer support
- Use dual-write patterns during transition periods (write to both old and new schemas)
- Deploy readers (consumers) first for backward-compatible updates
- Soft deprecation (mark as deprecated, continue support) before hard deprecation (removal after notice period)

### Data product lifecycle

Data products move through four stages [13]:

1. **Ideate** — Define objectives, identify use cases delivering measurable outcomes, gather requirements through stakeholder collaboration
2. **Design** — Create data contracts specifying structure, quality expectations, update frequencies, and SLOs; establish governance checkpoints
3. **Operationalize** — Build, test, deploy, and monitor; shift data quality accountability to development teams
4. **Evolve** — Collect user feedback, review governance compliance, track usage metrics, determine when products should be retired

Usage analytics drive investment decisions at every stage: declining usage signals approaching retirement; increasing usage signals needed SLA upgrades [12][13].

---

## Sub-question 6: Prioritization of Competing Consumer Requirements

### Prioritization frameworks

When multiple consumers compete for data product investment, four criteria determine priority [12]:

1. **Business criticality** — Does this data product support revenue-driving processes or regulatory reporting? These take precedence over nice-to-have analytics.
2. **Usage and adoption** — Active utilization in downstream workflows demonstrates validated demand. Low-usage products should be scrutinized before receiving further investment.
3. **Data quality and freshness** — Products with degrading quality or freshness violations need immediate attention regardless of planned roadmap.
4. **Stakeholder demand** — Consistent requests from multiple consumers signal genuine need, while single-consumer requests should be evaluated against broader utility.

### Consumption-first architecture within the data engineering lifecycle

The Fundamentals of Data Engineering lifecycle (Reis & Housley) defines stages as Generation → Ingestion → Transformation → Serving → Consumption [implied from lifecycle model]. Requirements gathering should work this lifecycle backward: start at Consumption (what do consumers need?), then determine Serving requirements (what format, freshness, access pattern?), then Transformation requirements (what business logic, what joins, what aggregations?), then Ingestion requirements (what sources, what frequency, what volume?), and finally Generation constraints (what does the source system provide, what are its limitations?).

This backward traversal — consumption-first — prevents the common anti-pattern of building pipelines from source forward and discovering at the end that the output does not match consumer expectations [17]. The "dump petabytes into a data lake" approach fails precisely because it inverts this order: it starts at Generation and hopes Consumption will figure itself out [17].

### Avoiding over-engineering

Three anti-patterns emerge from misaligned requirements:

1. **Premature streaming** — Building streaming infrastructure when daily batch meets the actual freshness requirement. Streaming infrastructure costs 5-10x more to build and operate than batch for equivalent data volume [15].
2. **Over-normalization** — Building complex dimensional models when consumers run simple queries that a wide table would serve better. Let the query pattern dictate the model, not textbook conventions [14].
3. **Universal SLAs** — Applying the same SLA to every data product regardless of criticality. Tiered SLAs (critical/standard/best-effort) allocate engineering effort proportionally to business impact [2][18].

---

## Challenge

Challenger research targeted the novelty of data product thinking, the practical applicability of consumer-defined contracts, and the robustness of requirement-to-architecture mappings. Six claims were challenged.

### Requirements gathering is social, not procedural

Multiple sources frame requirements gathering as fundamentally a social process requiring "a deep level of curiosity" and sustained stakeholder engagement [1][4]. This framing is correct but risks understating the importance of structure. Unstructured conversations with stakeholders produce inconsistent requirements that are hard to compare across consumers. The Data Product Canvas [3] and structured requirement templates [16] provide the scaffolding that makes the social process productive. The finding stands: gathering is social, but documentation frameworks are what make the social output actionable.

### The Data Product Canvas is comprehensive

The canvas covers eight building blocks and provides useful structure for workshops [3]. However, it was designed for data mesh contexts and does not explicitly address several practical concerns: cost constraints, pipeline complexity estimates, or operational burden assessment. Teams adopting the canvas should augment it with feasibility analysis and cost estimation — the canvas captures what consumers want but not what is economically viable to build.

### Consumer-defined contracts invert traditional requirements gathering

Sanderson's argument that contracts should be consumer-defined [6] is compelling but assumes a level of organizational maturity that most teams lack. In practice, most data teams do not have dedicated data product owners, and consumers cannot articulate quality expectations without guidance. The three-phase maturity model (awareness → collaboration → contract ownership) acknowledges this gap, but the transition from Phase 1 to Phase 3 requires significant organizational investment. The principle is sound; the implementation path is harder than presented.

### Query shape deterministically maps to modeling choice

The mapping from query pattern to model (join-heavy → star schema, scan-heavy → wide table) is a useful heuristic but not deterministic [14]. Mixed workloads — where some consumers need star-schema-style joins and others need wide-table scans — require either multiple materializations or a compromise model. The heuristic is correct for dominant query patterns but breaks down when a single data product serves heterogeneous consumers with fundamentally different access patterns.

### Most "real-time" requirements are actually "hourly"

Multiple sources assert that stakeholders overstate freshness requirements [15][9]. This is consistently observed in practice, but the claim should not be used to dismiss genuine real-time needs. Fraud detection, recommendation engines, and operational alerting genuinely require sub-second freshness. The correct practice is to quantify the freshness requirement before dismissing it — ask "What business decision changes if the data is 5 minutes old instead of 5 seconds old?" — not to assume the stakeholder is wrong.

### Data product versioning with SemVer is straightforward

SemVer provides a useful vocabulary (MAJOR/MINOR/PATCH) for data product changes [8], but applying it to data is harder than applying it to APIs. A schema change that adds a nullable column is clearly MINOR. But what about a change in data distribution (same schema, different values)? Or a change in freshness (same data, different delivery time)? SemVer covers structural changes but does not address behavioral changes that may equally break downstream consumers. Teams should extend SemVer with behavioral contracts (SLA/quality dimensions) to capture the full scope of breaking changes.

---

## Findings

### Finding 1: Requirements gathering must start from consumption and work backward through the lifecycle
**Confidence: HIGH**

The data engineering lifecycle (Generation → Ingestion → Transformation → Serving → Consumption) provides the organizational spine for requirements gathering, but the traversal direction must be reversed. Start at Consumption: What decisions do consumers make? What data do they need? How fresh must it be? What access pattern do they prefer? Then work backward: What serving format supports those patterns? What transformations produce that format? What ingestion approach delivers the required freshness? What source system constraints exist? This backward traversal — consumption-first — prevents the dominant anti-pattern of building pipelines source-forward and discovering at delivery that the output does not match consumer expectations. The Data Product Canvas enforces this ordering by placing consumers and use cases (block 3) before sources (block 5) and architecture (block 6). Multiple sources independently converge on this principle: Sanderson's consumer-defined contracts, Dehghani's data-as-a-product, and the practical freshness SLA frameworks all begin with the consumer.

### Finding 2: Consumption patterns map to architecture decisions through predictable heuristics
**Confidence: HIGH**

Three consumption dimensions drive three architecture decisions with high predictability. First, query shape determines modeling choice: join-heavy multidimensional analytics favor star schemas; scan-heavy columnar queries favor wide flat tables; entity lookups favor partitioned entity-centric models. Second, freshness requirements determine ingestion strategy: 24+ hour tolerance maps to batch; 1-60 minute tolerance maps to micro-batch or incremental; sub-minute tolerance maps to streaming. Third, consumer SLA criticality determines pipeline investment level: ad-hoc exploration warrants prototype-stage pipelines; financial reporting and ML training warrant production-grade pipelines with contracts, monitoring, and retry logic. These heuristics are not deterministic — mixed workloads and heterogeneous consumers create exceptions — but they provide a strong default that prevents both over-engineering and under-engineering.

### Finding 3: The SLI/SLO/SLA hierarchy provides the measurement framework for data product reliability
**Confidence: HIGH**

Borrowing directly from SRE practice, the three-tier measurement hierarchy translates business reliability commitments into engineering targets. SLIs measure specific performance aspects (hours since refresh, null rate, format compliance). SLOs set internal targets (less than 6 hours since refresh, 99.9% format compliance). SLAs formalize external commitments with error budgets that define acceptable violation rates. Error budgets are the operational lever: they translate "how reliable should this be?" into "how much unreliability can we tolerate before shifting from feature work to reliability work?" Burn rate monitoring provides early warning before SLA breach. Different data products warrant different SLA commitments based on business criticality — tiered SLAs (critical/standard/best-effort) allocate engineering effort proportionally. Baseline measurement over several months should precede SLA commitments to avoid promising targets that current infrastructure cannot achieve.

### Finding 4: Data product ownership requires a dedicated role bridging business and technical domains
**Confidence: MODERATE**

The Data Product Owner role — accountable for maximizing data product value — is essential for sustained data product quality. The role requires understanding both business domain context (what decisions consumers make, what data they need) and technical constraints (pipeline complexity, infrastructure cost, platform limitations). Without this role, requirements gathering defaults to either business stakeholders who cannot articulate technical constraints or data engineers who cannot prioritize business value. The role's core responsibilities include requirements and prioritization, quality stewardship, impact measurement, cost management, and consumer communication. However, most organizations lack this role, and the industry lacks institutional maturity around it — there is no canonical training path, certification, or widely adopted job description. Teams without a dedicated data product owner should assign these responsibilities explicitly to an existing role rather than leaving them unowned.

### Finding 5: Consumer-defined data contracts formalize requirements into enforceable agreements
**Confidence: MODERATE**

Data contracts — structured agreements between producers and consumers defining schema, quality rules, SLAs, and semantics — are the mechanism that converts requirements into enforceable commitments. The Open Data Contract Standard (ODCS v3.0) provides a machine-readable specification. Consumer-defined contracts (originating from consumption needs rather than production capabilities) are more effective because producers lack visibility into downstream usage patterns. However, consumer-defined contracts require organizational maturity: consumers must be able to articulate quality expectations (which they rarely can without guidance), and producers must accept accountability for meeting those expectations (which requires cultural change). The three-phase maturity model (awareness → collaboration → contract ownership) provides a practical adoption path, but most organizations are at Phase 1 or earlier. Contracts are most valuable for production-grade data products serving external consumers; prototype-stage products can operate without them.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Requirements gathering is a social discipline — interviews and workshops outperform surveys | [1][4] | verified | Consistently observed across multiple practitioner sources |
| 2 | The Data Product Canvas has eight building blocks starting from domain and consumers | [3] | verified | Open-source framework under CC BY 4.0 license |
| 3 | MoSCoW (Must/Should/Could/Won't) is an effective prioritization method for competing data requirements | [1] | verified | Standard technique adapted from project management |
| 4 | Most "real-time" requirements are actually "hourly" or "5-minute" when quantified | [15][9] | qualified | Common observation but should not be used to dismiss genuine real-time needs |
| 5 | Consumer-defined data contracts are more effective than producer-defined contracts | [6] | qualified | Compelling argument but requires organizational maturity most teams lack |
| 6 | Query shape maps to modeling choice: join-heavy → star schema, scan-heavy → wide table | [14] | qualified | Useful heuristic for dominant patterns; breaks down for mixed workloads |
| 7 | SemVer applies to data product versioning (MAJOR/MINOR/PATCH) | [8] | qualified | Covers structural changes but not behavioral changes (SLA, quality shifts) |
| 8 | Data freshness SLAs should match business value, not technical capability | [9] | verified | Hourly refresh costs 8-10x daily schedule with rarely different outcomes |
| 9 | SLI/SLO/SLA hierarchy from SRE applies directly to data product reliability | [10][18] | verified | Widely adopted; error budgets provide actionable prioritization |
| 10 | Data Product Owner is accountable for maximizing data product value | [4][7] | verified | Defined in both data mesh and practitioner sources |
| 11 | ODCS v3.0 provides machine-readable data contract specification | [20] | verified | Open standard under BITOL / Linux Foundation |
| 12 | Data product lifecycle has four stages: Ideate, Design, Operationalize, Evolve | [13] | verified | Multiple sources converge on similar stage models |
| 13 | Breaking changes require deprecation windows and dual-write migration periods | [8] | verified | Standard practice from API versioning adapted to data products |
| 14 | Building pipelines source-forward without consumption requirements is the dominant anti-pattern | [5][17] | verified | Multiple sources identify this independently |
| 15 | Error budgets translate SLA commitments into actionable engineering priorities | [10][18] | verified | Directly borrowed from SRE practice; well-established pattern |
