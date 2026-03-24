---
name: select-model
description: Guide the user through choosing a data modeling approach (Kimball, Data Vault, OBT) based on team size, source count, compliance needs, query patterns, platform, and change velocity. Updates the scope document's modeling recommendation section.
---

# dos:select-model

Guide the user through choosing a data modeling approach (Kimball, Data Vault, OBT) based on constraints gathered from the scope document and conversation. Apply the decision matrix, surface platform-specific guidance and counter-evidence, then persist the recommendation to the scope document.

## Preamble

Before starting, establish context:

1. **Which data product?** Ask the user for a data product name (e.g., `orders`, `customer-360`). This determines the artifact path: `docs/data-products/<name>/scope.md`.
2. **Check for existing scope document.** If `docs/data-products/<name>/scope.md` exists, read it and extract any pre-populated constraints: query patterns, platform, team size, compliance needs, source count, change velocity. Summarize what the scope document already tells us about modeling constraints.
3. **Check for existing modeling recommendation.** If the scope document already has a modeling recommendation section populated, summarize it and ask whether the user wants to revisit or update the recommendation.

If the scope document exists with constraints already defined, skip gathering those constraints again in the workflow — use what the scope provides and only ask about gaps.

## Workflow

### Step 1: Extract Scope Constraints

If a scope document exists at `docs/data-products/<name>/scope.md`, extract:

- **Query patterns** — dominant consumption pattern (join-heavy, scan-heavy, entity lookup, ad-hoc)
- **Target platform** — where the data product will be served (DuckDB, Snowflake, Databricks, BigQuery, ClickHouse, other)
- **Team size** — number of data/analytics engineers who will build and maintain
- **Compliance needs** — regulatory requirements (GDPR, SOX, HIPAA, audit trail requirements)
- **Source count** — number of source systems feeding the data product
- **Change velocity** — how frequently source schemas or business rules change

Present what was extracted and note any gaps that need to be filled.

### Step 2: Gather Missing Constraints

For any constraint not available from the scope document, ask the user directly. Gather all missing items in a single pass rather than one at a time.

| Constraint | Question |
|------------|----------|
| Team size | How many data/analytics engineers will build and maintain this? |
| Source count | How many source systems feed this data product? |
| Compliance needs | Are there regulatory or audit trail requirements (GDPR, SOX, HIPAA)? |
| Query pattern | What is the dominant query pattern? (Mixed analytics, flat exports, complex cross-domain, ad-hoc exploration) |
| Target platform | What is the target platform? (DuckDB, Snowflake, Databricks, BigQuery, ClickHouse) |
| Change velocity | How frequently do source schemas or business rules change? (Low, moderate, high) |

All six constraints are needed to apply the decision matrix. If the user cannot answer some, note the uncertainty and apply the default (Kimball) with the caveat that the recommendation should be revisited once constraints are clearer.

### Step 3: Apply Decision Matrix

Apply the decision matrix to recommend a modeling approach.

Refer to [model-decision-matrix.md](references/model-decision-matrix.md) for the full selection criteria matrix, decision rules, and pragmatism principle.

**Decision rules:**

1. **Data Vault** — Recommend when ALL of these hold:
   - 5+ engineers with automation tooling
   - 5+ source systems with frequent changes
   - Regulated environment requiring audit trails (GDPR, SOX, HIPAA)
   - If only some hold, note Data Vault patterns that could be selectively adopted (e.g., satellite-style history tracking) without full Data Vault commitment.

2. **OBT as serving layer** — Recommend when:
   - Consumers primarily need simple flat queries, CSV exports, or API responses
   - Sources are few and stable (low change velocity)
   - Platform strongly favors wide tables (BigQuery, Databricks with Liquid Clustering)
   - Even when recommending OBT, recommend Kimball as the upstream source-of-truth with OBT as a downstream mart.

3. **Kimball** — Default for everything else. Works at any team size, aligns with all major BI tools, endorsed by all cloud vendors.

Present the recommendation with the reasoning mapped back to constraints. Show which factors drove the decision.

### Step 4: Surface Platform-Specific Guidance

Based on the target platform, surface relevant optimization guidance.

Refer to [platform-modeling-guidance.md](references/platform-modeling-guidance.md) for platform-specific recommendations, the hybrid pattern, and optimization priorities.

| Platform | Key Guidance |
|----------|-------------|
| **DuckDB** | Joins are cheap (DPhyp optimizer). Star schema is natural. Wide tables inflate storage 6.3x. |
| **Snowflake** | Storage cheap, compute expensive. Kimball for reporting. Data Vault aligns with insert-only cost model. |
| **Databricks** | Optimization > model choice. Liquid Clustering essential. Medallion layering recommended. |
| **BigQuery** | OBT shows 49% improvement. Consider OBT marts on Kimball core. |
| **ClickHouse** | MergeTree favors star schema. Materialized views for pre-aggregation. Avoid denormalization. |

If the platform is not listed, apply the Kimball default and note that platform-specific optimization should be researched separately.

### Step 5: Flag Counter-Evidence

Present evidence that challenges the recommendation, so the user can make an informed decision rather than blindly following the default.

Refer to [platform-modeling-guidance.md](references/platform-modeling-guidance.md) for counter-evidence details.

**Always surface:**

- **Fivetran benchmarks:** OBT outperforms star schema 10-45% for BI-style queries on some platforms.
- **BigQuery specifics:** 49% average improvement with OBT if that is the target platform.
- **Databricks Liquid Clustering:** Optimized OBT (1.13s) outperformed standard relational model (2.6s) — optimization matters more than model choice.
- **Semantic layer wildcard:** dbt Semantic Layer and AtScale may render the physical modeling choice less consequential. If the user is investing in a semantic layer, optimize for compute cost and maintenance simplicity instead of query ergonomics.

Frame counter-evidence as: "Here is what challenges this recommendation — here is why we still recommend X given your constraints."

### Step 6: Deliver Recommendation and Update Scope Document

Deliver the final recommendation with:

1. **Recommended model** — Kimball, Data Vault, or Kimball + OBT serving layer
2. **Reasoning** — which constraints drove the decision, mapped to the decision matrix
3. **Platform optimizations** — specific actions for the target platform
4. **Counter-evidence considered** — what was weighed and why the recommendation still holds
5. **Caveats** — conditions under which the recommendation should be revisited

**Always persist the recommendation to the scope document.** Conversational-only output breaks the artifact chain. Update `docs/data-products/<name>/scope.md`:

- Populate the **Modeling Recommendation** section with:
  - Chosen approach and reasoning
  - Platform-specific optimizations to apply
  - Counter-evidence considered
  - Conditions for revisiting
- Bump the minor version in frontmatter
- Update `last_modified`
- Add a changelog entry: "Added modeling recommendation: [approach] based on [key constraints]"

If no scope document exists yet, create one using the frontmatter schema from `docs/data-products/_index.md` (name, artifact_type: scope, version: 1.0.0, owner, status: draft, last_modified). Populate at minimum the modeling recommendation section plus the constraints gathered during this workflow. Note in the changelog that remaining sections should be completed via `/dos:scope-data-product`.

### Step 7: Next Steps

End with a "Next Steps" section recommending downstream skills:

1. **`/dos:define-contract`** — Define a data contract covering schema, quality rules, SLAs, and ownership. The modeling recommendation informs schema structure and contract constraints.
2. **`/dos:implement-models`** — Build the dbt models implementing the chosen modeling approach. Consumes the modeling recommendation directly.

If the scope document is incomplete (missing consumers, SLAs, quality dimensions), also suggest:

3. **`/dos:scope-data-product`** — Complete the full scope if it was not done before select-model.

Present these options to the user and explain what each downstream skill will do with the modeling recommendation.
