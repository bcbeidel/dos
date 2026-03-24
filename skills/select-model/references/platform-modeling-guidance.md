# Platform Modeling Guidance

How a model is optimized matters more than which model is chosen. Each platform has characteristics that favor specific patterns.

## Platform-Specific Guidance

### DuckDB

Joins are cheap. The DPhyp algorithm finds optimal join orders, putting multi-join star schema queries within 2x of wide table speed. Wide tables inflated storage 6.3x in TPC-H benchmarks (26GB to 164GB). Star schemas are the natural fit. Use proper data types -- DATETIME uses 3.3GB vs VARCHAR at 5.2GB on 554M rows.

**Recommendation:** Star schema (Kimball). Joins cost little; storage savings are significant.

### Snowflake

Decouples storage (cheap) from compute (expensive). Data Vault's insert-only patterns align with this cost structure. Star schemas recommended for stable reporting. Snowflake recommends storing "final consumable data in the Kimball dimensional data model." Wide tables recommended only when "query speed matters more than storage efficiency or update flexibility."

**Recommendation:** Kimball for reporting; Data Vault for integration layer in regulated environments.

### Databricks

"How a model is optimized is more important than which model is chosen." Liquid Clustering is essential for large tables regardless of model -- achieved >20x speedup, reducing query time from 3.5s to 1.13s. Delta Live Tables automates SCD Type 2. The medallion architecture (Bronze raw, Silver OBTs for exploration, Gold star schemas for production) is the recommended layered approach.

**Recommendation:** Medallion layering with Liquid Clustering. Model choice is secondary to optimization.

### ClickHouse

Append-only MergeTree engine makes denormalization expensive. Star schema with one or two joins matches the JOIN algorithm's strengths. Use materialized views for pre-aggregation instead of flattening.

**Recommendation:** Star schema with materialized views. Avoid wide denormalized tables.

## Counter-Evidence

These results are real and platform-specific. They do not invalidate Kimball as a default but they matter when optimizing for a specific platform:

- **Fivetran benchmarks:** OBT outperforms star schema 10-45% for BI-style queries
- **BigQuery:** 49% average improvement with OBT over star schema
- **Databricks Liquid Clustering:** Optimized OBT (1.13s) outperformed standard relational model (2.6s)

## The Hybrid Pattern

Brooklyn Data's evidence-backed approach: Kimball fact/dimension tables as upstream source-of-truth, with OBT data marts flattened for BI consumption. This gives query simplicity of OBT with governance and maintainability of dimensional modeling.

Databricks recommends the same layered approach: Silver OBTs for rapid integration, Gold star schemas once requirements stabilize.

## Takeaway

Platform optimization matters more than model choice. The right model configured wrong will lose to the wrong model configured right. Start with Kimball, apply platform-specific optimizations, and add OBT serving layers where consumers need them.
