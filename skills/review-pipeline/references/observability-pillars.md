# Data Observability Pillars

## Observability vs Monitoring

| Discipline | Question Answered | What It Watches | Tools |
|-----------|-------------------|-----------------|-------|
| **Pipeline monitoring** | "Did the pipeline run?" | Throughput, latency, error rate, resource utilization | Orchestrator-native (Airflow, Dagster, Prefect) |
| **Data observability** | "Is the output data trustworthy?" | Freshness, volume, distribution, schema, lineage | dbt tests, Dagster asset checks, Monte Carlo |

Both are needed. Instrument pipeline monitoring first (orchestrator-native), then layer data observability on top.

## Five Baseline Metrics

Assess in this order (highest signal-to-investment ratio first):

### 1. Freshness

**Question:** Is data arriving on time?
**Measure:** Time since most recent valid data arrived in each destination table.
**Assessment criteria:**
- Freshness thresholds defined per table? (warn_after, error_after)
- `dbt source freshness` wired as separate orchestrator step?
- Monitoring frequency aligned with SLA granularity?

### 2. Volume

**Question:** Did the expected number of rows arrive?
**Measure:** Row count comparison against baseline (previous run, historical average).
**Assessment criteria:**
- Row count checks in place? (dbt-expectations `expect_table_row_count_to_be_between`)
- Baseline established for comparison?
- Detects partial loads, dropped partitions, silent upstream failures?

### 3. Distribution

**Question:** Are values within expected ranges?
**Measure:** Statistical comparison of value distributions against historical baselines.
**Assessment criteria:**
- Distribution checks on key numeric columns?
- Anomaly detection method appropriate? (rule-based for known constraints, statistical for distributions, ML only at scale)
- Catches data corruption, unit changes, upstream logic shifts?

### 4. Schema

**Question:** Have columns or types changed?
**Measure:** Schema comparison against contract or previous known-good state.
**Assessment criteria:**
- Contract enforcement enabled on critical models?
- Schema drift detection in place?
- Breaking change detection via `state:modified+` in CI?

### 5. Lineage

**Question:** What upstream changes impact this table?
**Measure:** Dependency graph from source to consumption.
**Assessment criteria:**
- Lineage documented? (dbt docs, DataHub, manual)
- Cross-system lineage (beyond dbt DAG)?
- Blast radius analysis possible during incidents?

## Implementation Order

Start with freshness and volume — they provide the highest signal-to-investment ratio. Add distribution, schema, and lineage as the system matures.
