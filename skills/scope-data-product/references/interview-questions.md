# Stakeholder Interview and Scoping Framework

Requirements gathering is social, not documentary. Structure the process with frameworks but never substitute documentation for conversation.

## Data Product Canvas

Eight building blocks, completed in consumption-first order:

1. **Domain** — Who owns and maintains this data product
2. **Data Product Name** — Unique identifier following naming conventions
3. **Consumer and Use Case(s)** — Who consumes this, for what analytical purpose
4. **Data Contract** — Output ports, formats, protocols, data models, semantics, usage terms
5. **Sources** — Input mechanisms and data origins
6. **Data Product Architecture** — Internal design: ingestion, storage, transformations
7. **Ubiquitous Language** — Shared domain terminology
8. **Classification** — Source-aligned, aggregate, or consumer-aligned

The ordering enforces consumption-driven design: define who needs what before deciding how to build it.

## Stakeholder Interview Questions

### Understanding Consumption

- "What decisions do you make with this data?"
- "What happens when the data is wrong or late?"
- "How frequently do you need updated data — and what changes if it's 5 minutes old vs 5 seconds?"
- "What do you look at first when you open the dashboard/report?"
- "Walk me through the last time you used this data to make a decision."

### Understanding Sources

- "Where does this data come from originally?"
- "Who owns the source system? How do you reach them when something breaks?"
- "Has the format or structure changed in the past 6-12 months?"

### Understanding Quality

- "What does 'wrong data' look like in your context?"
- "What's the minimum quality level where the data is still useful to you?"
- "Have you encountered data quality issues? What happened?"

## Empirical Validation

Supplement interviews with observation — review actual usage:
- **Dashboards:** Which filters, dimensions, and measures are used
- **SQL queries:** Join patterns, filter clauses, aggregation granularity
- **Query logs:** BigQuery `INFORMATION_SCHEMA.JOBS`, Snowflake `QUERY_HISTORY` for actual access patterns

What people do with data and what they say they do often diverge.

## MoSCoW Prioritization

When multiple consumers have competing requirements:

- **Must have** — Requirements without which the data product has no value
- **Should have** — Important, deliverable iteratively
- **Could have** — Nice-to-haves deprioritized under pressure
- **Won't have** — Explicitly descoped for future consideration

Explicit descoping prevents scope creep — the single largest source of data project delays.

## Consumption-First Traversal

Work the lifecycle backward: Consumption -> Serving -> Transformation -> Ingestion -> Generation. Start with what consumers need, then determine what to build.
