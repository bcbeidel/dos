# Research


| File | Description |
| --- | --- |
| [2026-03-21-pipeline-design-architecture.research.md](2026-03-21-pipeline-design-architecture.research.md) | "Medallion architecture is a useful organizing pattern but not a universal default; incremental loading has five core patterns with silent failure risks; batch vs streaming choice hinges on latency needs not technology preference; schema evolution tooling support varies significantly across dbt, dlt, and Delta Lake" |
| [2026-03-22-data-modeling.research.md](2026-03-22-data-modeling.research.md) | "Kimball dimensional modeling is the strongest prescriptive default for analytics engineering; Data Vault reserved for enterprise audit/compliance with 5+ engineers; OBT best as downstream mart layer, not standalone architecture. Platform optimization matters more than model choice." |
| [2026-03-22-open-table-formats.research.md](2026-03-22-open-table-formats.research.md) | "Comparison of Delta Lake, Iceberg, Parquet, ORC, and Avro — capabilities, cross-platform compatibility, catalog interop, and format selection guidance" |
| [2026-03-22-production-platform-landscape.research.md](2026-03-22-production-platform-landscape.research.md) | "How ClickHouse, BigQuery, Redshift, Athena, Databricks, and Snowflake compare as analytical data platforms" |
| [2026-03-22-development-workflow.research.md](2026-03-22-development-workflow.research.md) | "DuckDB local dev is fast but hides dialect and concurrency divergence; three-tier validation (pre-commit, PR CI with slim builds, production deploy) is the emerging best practice; dbt and dlt have parallel but non-unified environment management; SQLFluff pre-commit hooks are 10x slower with dbt templater" |
