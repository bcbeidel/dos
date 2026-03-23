---
name: Data Contracts
description: "Data contracts (ODCS v3.1) formalize producer-consumer agreements around schema, quality rules, SLAs, and ownership; the technology is mature but organizational adoption is the real challenge -- source system owners must accept accountability for produced data"
type: context
related:
  - docs/research/2026-03-22-data-discovery.research.md
  - docs/research/2026-03-22-data-product-scoping.research.md
  - docs/context/source-system-evaluation.md
  - docs/context/schema-drift-risk.md
  - docs/context/schema-evolution.md
  - docs/context/data-source-onboarding.md
  - docs/context/requirements-gathering-techniques.md
  - docs/context/change-propagation-pipelines.md
---

## Key Takeaway

Data contracts shift data quality accountability from consumers to producers. The technology is production-ready (ODCS v3.1 under Linux Foundation governance). The adoption challenge is organizational: application engineering teams must accept responsibility for the data they produce. Start with high-value sources where quality failure costs are obvious, negotiate contracts with willing producer teams, and expand incrementally. Mandating contracts across all sources without buy-in produces shelf-ware.

## What a Data Contract Contains

A data contract formalizes the agreement between a data producer and its consumers in a machine-readable format. The Open Data Contract Standard (ODCS) v3.1.0, governed by Bitol under the Linux Foundation, is the recommended standard (the Data Contract Specification has been deprecated in favor of ODCS).

Four core components for source onboarding:

**Schema definition** -- Field names, types, nullability, precision, and structure (including nested/complex types). This is the contract's core: what the producer commits to deliver.

**Quality rules** -- Minimum row counts, null percentage thresholds, uniqueness constraints, value range checks. These translate the profiling baseline into enforceable expectations.

**SLAs** -- Freshness threshold (maximum age of latest data), availability percentage, latency (source-to-destination delay), retention period, and update frequency.

**Ownership** -- Producer team, consumer teams, escalation contacts, and lifecycle status (proposed, active, deprecated, retired).

## Enforcement in Practice

dlt provides a pragmatic implementation with four contract modes applied to tables, columns, and data_types:

- **evolve** -- No constraints; new tables and columns created automatically. Use during development.
- **freeze** -- Raises exception on non-conforming data. Use in production for stable, contract-governed sources.
- **discard_row** -- Drops entire rows that violate schema. Use for event streams with variant structures.
- **discard_value** -- Strips non-conforming fields, loads the rest. Resilient production default that tolerates drift without losing records.

Recommended progression: `evolve` during initial discovery to infer schema, then `freeze` or `discard_value` in production. Schema changes in production should be explicit and deliberate, not automatic.

## Why Adoption Is Hard

Data contracts require source system owners (typically application engineers) to accept accountability for data they produce. This is a cultural shift -- historically, data quality has been treated as the data team's problem. Three patterns that work:

1. **Start with willing producers** -- Find teams that already care about their data's downstream impact. Build the first contracts collaboratively.
2. **Tie to business cost** -- Quantify the cost of quality failures for high-value sources. Schema drift causes 7.8% of data quality incidents; incidents average 15 hours to resolve.
3. **Keep contracts lightweight** -- A contract covering schema, three quality rules, and one SLA is better than no contract. Expand coverage over time.

The ecosystem fragmentation (Data Contract Specification deprecated in favor of ODCS) signals that standards are not yet fully settled, but ODCS has institutional credibility through Linux Foundation governance and PayPal lineage.

## Consumer-Defined vs Producer-Defined

Data contracts should be consumer-defined rather than producer-defined. Producers (application engineers) lack visibility into how downstream teams use their data. A data product owner -- not the source system team -- should define what the contract requires.

Consumer-defined contracts invert the traditional approach: requirements originate at the consumption point, not the production point. This generates problem visibility that catalyzes organizational culture change around data quality and stewardship.

Three-phase maturity model for consumer-defined contracts:

1. **Awareness** -- Producers understand when their changes affect consumers through pre-deployment notification.
2. **Collaboration** -- Producers communicate breaking changes in advance, enabling downstream teams to prepare.
3. **Contract ownership** -- Producers maintain formal contracts with clear versioning and evolution processes.

Most organizations are at Phase 1 or earlier. The transition to Phase 3 requires significant organizational investment.

## Versioning Contracts

Data product versioning follows semantic versioning (MAJOR.MINOR.PATCH). SemVer covers structural changes (column removal = MAJOR, nullable column addition = MINOR) but not behavioral changes -- a shift in data distribution or freshness can equally break downstream consumers. Extend SemVer with behavioral dimensions (SLA changes, quality metric shifts).

Breaking changes require: announce with explicit timelines, provide migration guides, use dual-write patterns during transition, deploy consumers first for backward-compatible updates, and soft-deprecate before hard-deprecate.
