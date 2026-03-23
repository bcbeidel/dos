---
name: "Quality Engineering"
description: "Data quality is context-dependent ('fitness for use'), not absolute — the same data can be high quality for one use case and poor for another; DAMA-DMBOK's six dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness) are a useful starting taxonomy but 127 distinct dimensions have been identified across literature; data profiling (structure, content, relationship) provides the measurement foundation; anomaly detection should combine rule-based checks with statistical methods (z-score for normal distributions, IQR for skewed data, KS test for drift) — ML-based approaches add value only at scale; composite quality scores require weighted dimension aggregation with business-driven weights; SLAs must follow the SLI/SLO/SLA hierarchy borrowed from SRE with error budgets driving prioritization; Gartner estimates poor data quality costs organizations $12.9M annually"
type: research
sources:
  - https://www.getdbt.com/blog/data-quality-dimensions
  - https://www.ibm.com/think/topics/data-quality-dimensions
  - https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2022.850611/full
  - https://miosoft.com/resources/articles/data-quality-dimensions-untangled.html
  - https://www.altexsoft.com/blog/data-profiling/
  - https://en.wikipedia.org/wiki/Data_profiling
  - https://www.evidentlyai.com/ml-in-production/data-drift
  - https://www.evidentlyai.com/blog/data-drift-detection-large-datasets
  - https://asq.org/quality-resources/statistical-process-control
  - https://www.ataccama.com/blog/anomaly-detection-rules-based
  - https://dl.acm.org/doi/10.1145/3593434.3593445
  - https://arxiv.org/abs/2303.15068
  - https://www.bigeye.com/blog/defining-data-quality-with-slas
  - https://www.getdbt.com/blog/data-product-slas-and-slos
  - https://www.decube.io/post/define-data-quality-sla
  - https://www.elementary-data.com/post/measuring-data-health-a-guide
  - https://www.datafold.com/data-quality-guide/what-is-data-quality/
  - https://www.gartner.com/en/data-analytics/topics/data-quality
  - https://www.tandfonline.com/doi/abs/10.1080/07421222.1996.11518099
  - https://dama-nl.org/dimensions-of-data-quality-en/
  - https://www.acceldata.io/article/how-to-measure-data-quality
related:
  - docs/plans/2026-03-21-data-pipeline-research-context.plan.md
  - docs/research/2026-03-22-operations-reliability.research.md
---

## Summary

**Research question:** What methods and frameworks should data engineers use to measure and monitor data quality?

**Mode:** Technical | **SIFT rigor:** High | **Sources:** 21 | **Searches:** 12 across Google

**Key findings:**
- Data quality is fundamentally context-dependent — "fitness for use" — not an absolute property. The same dataset can be high quality for one use case and poor for another. DAMA-DMBOK defines this but practitioners still treat quality as a binary pass/fail.
- The six-dimension taxonomy (accuracy, completeness, consistency, timeliness, validity, uniqueness) is the most widely adopted framework, but DAMA NL identified 127 distinct dimensions across literature, and the original Wang & Strong 1996 framework defined 15 dimensions in four categories. Dimension selection must be driven by use case, not framework completeness.
- Data profiling (structure, content, relationship analysis) is the measurement foundation — you cannot score quality without first understanding shape, distribution, completeness, and cardinality of your data.
- Anomaly and drift detection should layer rule-based checks (known constraints) with statistical methods (z-score, IQR, KS test, PSI) — ML-based approaches add value only at scale (100K+ observations) and require hybrid deployment alongside rules.
- Composite quality scores use weighted dimension aggregation: score each dimension as a percentage, assign business-driven weights, compute weighted average. Elementary's approach (test fail rate or failed row count) demonstrates practical implementation in the dbt ecosystem.
- Data quality SLAs must follow the SLI/SLO/SLA hierarchy from SRE: SLIs measure specific quality indicators, SLOs set target ranges, SLAs formalize commitments with error budgets. Error budget consumption drives prioritization between reliability work and new features.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://www.getdbt.com/blog/data-quality-dimensions | Data quality dimensions | dbt Labs | 2024 | T4 | verified — vendor blog |
| 2 | https://www.ibm.com/think/topics/data-quality-dimensions | What are data quality dimensions? | IBM | current | T2 | verified |
| 3 | https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2022.850611/full | A survey of data quality measurement and monitoring tools | Frontiers | 2022 | T1 | verified — peer-reviewed |
| 4 | https://miosoft.com/resources/articles/data-quality-dimensions-untangled.html | Data quality dimensions untangled | Miosoft | 2023 | T5 | verified — vendor article |
| 5 | https://www.altexsoft.com/blog/data-profiling/ | Data profiling process, examples, and techniques | AltexSoft | 2024 | T4 | verified — tech consultancy |
| 6 | https://en.wikipedia.org/wiki/Data_profiling | Data profiling | Wikipedia | current | T3 | verified |
| 7 | https://www.evidentlyai.com/ml-in-production/data-drift | What is data drift in ML, and how to detect and handle it | Evidently AI | 2024 | T4 | verified — vendor docs |
| 8 | https://www.evidentlyai.com/blog/data-drift-detection-large-datasets | Which test is the best? Comparing 5 drift detection methods | Evidently AI | 2024 | T4 | verified — empirical comparison |
| 9 | https://asq.org/quality-resources/statistical-process-control | What is statistical process control? | ASQ | current | T2 | verified — professional org |
| 10 | https://www.ataccama.com/blog/anomaly-detection-rules-based | Rules-based vs anomaly detection: what's best? | Ataccama | 2024 | T4 | verified — vendor blog |
| 11 | https://dl.acm.org/doi/10.1145/3593434.3593445 | DQSOps: Data quality scoring operations framework | ACM EASE | 2023 | T1 | verified — peer-reviewed |
| 12 | https://arxiv.org/abs/2303.15068 | DQSOps: Data quality scoring operations framework (preprint) | arXiv | 2023 | T2 | verified — preprint of [11] |
| 13 | https://www.bigeye.com/blog/defining-data-quality-with-slas | Defining data quality with SLAs | Bigeye | 2024 | T4 | verified — vendor blog |
| 14 | https://www.getdbt.com/blog/data-product-slas-and-slos | How to ensure data product SLAs and SLOs | dbt Labs | 2024 | T4 | verified — vendor blog |
| 15 | https://www.decube.io/post/define-data-quality-sla | Defining data quality with SLA: metrics, monitoring, and remediation | Decube | 2024 | T5 | verified — vendor blog |
| 16 | https://www.elementary-data.com/post/measuring-data-health-a-guide | Measuring data health: a full guide | Elementary | 2024 | T4 | verified — vendor blog |
| 17 | https://www.datafold.com/data-quality-guide/what-is-data-quality/ | Understanding the eight dimensions of data quality | Datafold | 2024 | T4 | verified — vendor guide |
| 18 | https://www.gartner.com/en/data-analytics/topics/data-quality | Data quality: why it matters | Gartner | current | T2 | verified — analyst firm |
| 19 | https://www.tandfonline.com/doi/abs/10.1080/07421222.1996.11518099 | Beyond accuracy: what data quality means to data consumers | Wang & Strong | 1996 | T1 | verified — foundational paper |
| 20 | https://dama-nl.org/dimensions-of-data-quality-en/ | Dimensions of data quality | DAMA NL | 2020 | T2 | verified — professional org |
| 21 | https://www.acceldata.io/article/how-to-measure-data-quality | Measuring data quality: essential metrics | Acceldata | 2024 | T4 | verified — vendor article |

---

## Sub-question 1: Data Profiling Techniques

### What data profiling is and why it comes first

Data profiling is the systematic examination of data to collect statistics and summaries that characterize its structure, content, and relationships [5][6]. Profiling must precede any quality measurement because you cannot score what you have not characterized. Without knowing a column's distribution, cardinality, and null rate, quality rules are guesses rather than informed assertions.

### Three types of profiling

Data profiling divides into three categories, each examining a different scope [5][6]:

**Structure profiling** examines metadata and format: column names, data types, field lengths, constraints, and naming consistency. This answers "What shape is the data?" — the most basic question before any quality assessment begins.

**Content profiling** examines actual values: null/missing value rates, value distributions (frequency histograms), outlier detection, format pattern analysis, and range validation. Key metrics include completeness (percentage of non-null values), uniqueness (distinct values / total values), and cardinality (count of distinct values per column). Descriptive statistics — min, max, mean, median, mode, standard deviation, percentiles (25th, 50th, 75th) — characterize numeric distributions.

**Relationship profiling** examines connections across columns and tables: primary/foreign key integrity, cross-column dependencies, orphaned records, circular references, and referential consistency. This is critical for data that spans multiple tables or systems.

### Key profiling metrics

The core metrics produced by data profiling map directly to quality dimensions [5][6]:

| Metric | Calculation | Quality Dimension |
|--------|-------------|-------------------|
| Null rate | NULL count / total rows | Completeness |
| Distinct count | COUNT(DISTINCT column) | Cardinality |
| Uniqueness ratio | Distinct count / total rows | Uniqueness |
| Value frequency | COUNT per distinct value | Distribution |
| Min/max range | MIN(column), MAX(column) | Validity |
| Standard deviation | STDDEV(column) | Distribution shape |
| Pattern frequency | Regex match count / total | Validity |

Cardinality analysis deserves specific attention: a column with cardinality equal to row count is a candidate primary key; a column with very low cardinality (e.g., 3 values in 10M rows) is a categorical field; cardinality that changes unexpectedly between profiling runs signals a data issue [5].

### Profiling as a continuous practice

Profiling is not a one-time activity. Initial profiling establishes baselines; ongoing profiling detects drift. The four-step workflow is: (1) profile to understand current state, (2) define quality rules based on profiles, (3) monitor against those rules, (4) re-profile periodically to update baselines [5]. Tools range from enterprise platforms (Ataccama, Talend) to open-source options (YData Profiling, Soda Core) [5].

---

## Sub-question 2: Data Quality Dimension Taxonomy

### The origin: Wang & Strong 1996

The concept of data quality dimensions was formalized in 1996 by Richard Wang and Diane Strong in their paper "Beyond Accuracy: What Data Quality Means to Data Consumers" [19]. This foundational research identified 15 dimensions organized into four categories: **Intrinsic DQ** (quality inherent to the data itself), **Contextual DQ** (quality relative to the task at hand), **Representational DQ** (quality of data format and meaning), and **Accessibility DQ** (quality of data availability and security). The key insight was that data consumers have a much broader quality conceptualization than data professionals recognize — accuracy alone is insufficient.

### The six-dimension consensus

Despite no universal standard, the industry has converged on six core dimensions [1][2][4]:

1. **Accuracy** — how closely data represents reality. Measurement: validation against trusted reference sources, statistical sampling, cross-system reconciliation.
2. **Completeness** — whether all required records and fields are present. Measurement: null rate (NULL count / total rows), missing record detection against expected volume.
3. **Consistency** — whether data agrees across systems and within itself. Measurement: cross-system comparison, referential integrity checks, value agreement across duplicated fields.
4. **Timeliness** — whether data is available when needed. Measurement: time delta between event occurrence and data availability, freshness SLA compliance rate.
5. **Validity** — whether data conforms to defined formats, types, and business rules. Measurement: regex pattern matching, range checks, accepted-value validation.
6. **Uniqueness** — whether data is free of unintended duplicates. Measurement: duplicate row detection, primary key violation rate.

### Beyond six: the dimension proliferation problem

The six-dimension consensus is a useful starting point, but it papers over real complexity. DAMA NL's 2020 research identified **60 standardized dimensions** from which 12 common dimensions were selected — and a broader survey found **127 distinct dimensions** across reliable sources [4][20]. Different organizations adopt different subsets: Collibra replaces timeliness with integrity; PricewaterhouseCoopers substitutes uniqueness with integrity; the US Department of Interior uses 11 dimensions; academic frameworks range from 4 to 16 [4].

The practical implication: **dimension selection is a design decision, not a standard to adopt wholesale**. Teams should select 4-10 dimensions based on their specific use cases, data characteristics, and stakeholder needs [4]. The six-dimension framework works as a communication tool and starting vocabulary, but treating it as exhaustive misses context-specific dimensions like usefulness (is the data actually consumed?) and freshness (distinct from timeliness — how recently was data updated?) [1][17].

### DAMA-DMBOK's quality framework

DAMA-DMBOK v2 (Chapter 13) defines Data Quality Management as the planning, implementation, and control of activities that apply quality management techniques to data to assure it is fit for consumption. The standard lists accuracy, completeness, consistency, timeliness, validity, uniqueness, integrity, and reasonability as core dimensions [20]. The framework emphasizes that quality is not a single metric but a multi-dimensional assessment relative to intended use — the "fitness for use" principle.

---

## Sub-question 3: Anomaly and Drift Detection Methods

### Statistical methods for point anomaly detection

Three foundational statistical methods detect anomalous individual values [7][8]:

**Z-score method**: Measures how many standard deviations a value is from the mean. Formula: `z = (x - mean) / std_dev`. Threshold: |z| > 3 is the standard outlier boundary. Best for: normally distributed data. Limitation: sensitive to extreme values because mean and standard deviation are themselves affected by outliers. Inappropriate for skewed distributions.

**IQR (Interquartile Range) method**: Uses quartiles rather than mean/std. Formula: `IQR = Q3 - Q1`; outlier boundaries at `Q1 - 1.5*IQR` and `Q3 + 1.5*IQR` (Tukey's fences). Best for: skewed or non-normal distributions. More robust than z-score because quartiles are not distorted by extreme values.

**Statistical Process Control (SPC)**: Borrowed from manufacturing quality management [9]. Control charts plot metrics over time with a center line (mean) and control limits at 3 standard deviations (UCL/LCL). The key concept is distinguishing **common cause variation** (inherent, expected) from **special cause variation** (assignable, requiring investigation). Western Electric rules and Nelson rules define patterns that indicate special cause variation — runs above/below center line, trends, oscillations. SPC applies directly to data pipeline metrics: plot daily row counts, null rates, or value distributions on control charts and investigate when points exceed control limits or exhibit patterns.

### Distribution drift detection

Drift detection compares two distributions (reference vs. current) to detect whether data has changed significantly [7][8]:

| Method | Best For | Sensitivity | Threshold |
|--------|----------|-------------|-----------|
| Kolmogorov-Smirnov (KS) test | Small datasets (<1K rows) | Very high | p-value < 0.05 |
| Population Stability Index (PSI) | Stable distributions, finance | Low | < 0.1 no change, 0.1-0.2 moderate, > 0.2 significant |
| Wasserstein Distance | Large datasets, balanced sensitivity | Moderate | 0.1 standard deviations |
| Jensen-Shannon Divergence | Large datasets | Moderate | 0.1 on 0-1 scale |
| KL Divergence | Large datasets | Low | Asymmetric — order matters |

Critical implementation detail: KS test becomes overly sensitive on large datasets (100K+ rows), flagging shifts as small as 0.5% that have no practical significance [8]. For large datasets, Wasserstein Distance offers the best compromise between sensitivity and practical relevance. PSI is widely used in credit risk modeling but barely detects segment-level drift [8].

### When to use each method

The selection depends on three factors: dataset size, distribution shape, and operational tolerance [7][8]:

- **Small datasets, high stakes**: KS test (most sensitive, statistically rigorous)
- **Large datasets, balanced approach**: Wasserstein Distance (interpretable, moderate sensitivity)
- **Established PSI workflows**: PSI (organizational consistency, well-understood thresholds)
- **Normal distributions, point anomalies**: Z-score (simple, fast, widely understood)
- **Skewed distributions, point anomalies**: IQR (robust to outliers)
- **Time series monitoring**: SPC control charts (pattern detection, not just threshold breach)

### ML-based anomaly detection

ML approaches (autoencoders, isolation forests, DBSCAN clustering) learn expected data patterns and flag deviations without manual threshold configuration [10]. Their primary advantage is discovering anomalies humans would not write rules for — complex multi-column relationships, subtle distribution shifts, and novel failure modes. Their primary disadvantage is the black-box problem: when an ML model flags an anomaly, explaining why to a data consumer is difficult.

The consensus is a **hybrid approach**: rules for known constraints and compliance requirements; statistical methods for distribution monitoring; ML for discovering unknown-unknowns at scale [10]. Organizations typically mature from rule-based (low maturity) through heavy ML reliance (moderate maturity) to balanced hybrid deployment (optimal maturity) [10].

---

## Sub-question 4: Quality Scoring and Measurement Frameworks

### Composite quality score calculation

A composite data quality score combines individual dimension scores into a single metric using weighted aggregation [11][16][21]:

1. **Define dimensions**: Select 4-7 dimensions relevant to the use case (e.g., completeness, accuracy, validity, freshness)
2. **Score each dimension**: Convert measurement results to percentages (e.g., 97% completeness, 92% validity)
3. **Assign weights**: Domain experts assign importance weights that sum to 1.0 (e.g., completeness=0.3, accuracy=0.3, validity=0.2, freshness=0.2)
4. **Compute weighted average**: `Quality Score = sum(dimension_score * weight)` for all dimensions
5. **Standardize**: Normalize scores before aggregation so different metrics integrate equally [11]

### Elementary's practical scoring approach

Elementary Data implements two scoring methods that work within the dbt ecosystem [16]:

**Test fail rate**: Each test receives a binary score — passed=1.0, warning=0.5, failed=0.0 — and scores are averaged across tests within a dimension. Example: 3 passing tests + 1 warning = (3*1.0 + 1*0.5) / 4 = 87.5%.

**Failed row count**: Dimension scores measure the proportion of affected rows. Formula: `(total_rows - failed_rows) / total_rows`, averaged across tests. Example: 3 passing tests (1,000 rows each) + 1 test with 100 failures = (3*1.0 + 1*0.9) / 4 = 97.5%.

The failed row count method provides finer granularity — a test that fails on 1 row out of 1M scores 99.9999% rather than 0.0. Elementary maps common dbt tests to quality dimensions automatically: `not_null` maps to completeness, `unique` to uniqueness, `accepted_values` to accuracy, `relationships` to consistency [16].

### DQSOps: ML-accelerated scoring

The DQSOps framework (ACM EASE 2023) introduces ML prediction to accelerate quality scoring [11][12]. The architecture has two paths: a **standard-based scorer** that periodically computes ground-truth quality scores across configured dimensions, and an **ML predictor** trained on historical scores that estimates quality in real-time between standard scoring cycles. The ML path achieves significant computational speedup while maintaining high prediction accuracy — critical for high-velocity streaming data where full dimension scoring on every data window is prohibitively expensive.

### What makes a score actionable

A quality score is only useful if it triggers specific actions at defined thresholds. Three-tier classification is the minimum viable approach:

- **Green (90-100%)**: No action required, data is fit for use
- **Yellow (70-89%)**: Investigation required, data may be degraded
- **Red (below 70%)**: Remediation required, data is unfit for use

Thresholds must be calibrated per use case — a financial reporting table may require 99.5% completeness (green threshold), while an internal analytics table may tolerate 95%. Without defined actions at each threshold, scores become vanity metrics that teams monitor but never act on [13][16].

---

## Sub-question 5: SLA Definition and Tracking

### The SLI/SLO/SLA hierarchy

Data quality SLAs borrow directly from SRE's reliability hierarchy [13][14]:

**Service Level Indicators (SLIs)** are specific, measurable quality metrics: "hours since dataset refreshed," "percentage of non-null values in email column," "percentage of rows passing referential integrity check." SLIs must be derived from actual measurement queries, not aspirational descriptions.

**Service Level Objectives (SLOs)** set target ranges for each SLI: "less than 6 hours since refresh," "at least 99.9% non-null," "100% referential integrity." SLOs are internal engineering targets, typically stricter than external commitments.

**Service Level Agreements (SLAs)** combine multiple SLOs into a formal commitment with consequences for breach. An SLA of 99.9% uptime (three nines) allows approximately 43 minutes of downtime per month [13].

### Error budgets for data quality

Error budgets define the acceptable amount of quality degradation over a measurement window [13][14]. A 99.5% freshness SLA allows approximately 3.6 hours of cumulative staleness per month. Error budget consumption drives engineering prioritization:

- **Budget > 50% remaining**: Ship new features confidently
- **Budget 25-50% remaining**: Review what is consuming the budget, slow risky changes
- **Budget < 25% remaining**: Freeze new features, focus on reliability

This framework resolves the perpetual tension between data teams building new pipelines and maintaining existing ones — the error budget makes the trade-off explicit and data-driven rather than political [13].

### Implementation roadmap

Six steps to implement data quality SLAs [13][14]:

1. **Identify high-value targets**: Executive dashboards, core ML models, customer-facing data products. Not all data deserves an SLA — over-SLA-ing creates the same noise problem as over-alerting.
2. **Define SLIs and SLOs through engineer-stakeholder collaboration**: Engineers propose technically feasible SLIs; stakeholders define acceptable SLO ranges. This must be a conversation, not a unilateral engineering decision.
3. **Document the SLA**: Include clear definitions, actual measurement queries (not prose descriptions), and consequence definitions. Ambiguous SLAs are worse than no SLAs.
4. **Implement SLI tracking**: Centralize measurement with error budget visibility. Monitoring frequency must align with SLA granularity — checking every 30 minutes for a 1-hour SLA [14].
5. **Establish alerting**: Alerts on SLO violation, not just SLA breach. By the time an SLA is breached, the error budget is already consumed.
6. **Monitor error budget consumption**: Track burn rate over time to guide quarterly reviews and team prioritization decisions.

### Tiered SLA structures

Different data products warrant different SLA commitments [14][15]:

- **Tier 1 (customer-facing)**: Strictest SLAs, smallest error budgets, fastest response times. Example: payment transaction data with 99.9% completeness, 15-minute freshness.
- **Tier 2 (operational)**: Moderate SLAs aligned with business cadence. Example: daily sales reporting with 99% completeness, 2-hour freshness.
- **Tier 3 (analytical)**: Relaxed SLAs, larger error budgets. Example: trend analysis data with 95% completeness, 24-hour freshness.

The cost of maintaining SLAs scales with strictness — a 99.9% SLA requires significantly more engineering investment than 99%. Teams should start with Tier 1 SLAs for critical data products and expand coverage as measurement infrastructure matures [14].

---

## Challenge

Challenger research targeted three areas: the measurability of data quality, the actionability of quality scores, and the practical applicability of DAMA-DMBOK's framework to modern data stacks. Five claims were challenged.

### Is data quality measurable or is it context-dependent?

Both. Data quality has been associated with the "fitness for use" principle since the 1980s — the same data can be high quality for one use case and poor for another [3][19]. A dataset with 5% null values in an email column is perfectly acceptable for aggregate analytics but catastrophically incomplete for a marketing email campaign. The Frontiers survey (2022) distinguishes "hard dimensions" (accuracy, completeness, timeliness) that can be measured objectively using check routines from "soft dimensions" that require subjective evaluation [3]. But even "hard" measurement requires preceding subjective definition — what counts as "accurate" or "complete" is domain-specific. The practical resolution: quality is measurable within a defined context. The context (who uses this data, for what purpose, with what tolerance) must be defined before measurement begins. Teams that skip context definition produce metrics that are technically correct but operationally useless.

### Do quality scores actually drive action?

Not automatically, and often not at all. The Frontiers survey found that most organizations rely on manual, ad-hoc quality validation rather than systematic automation [3]. A quality score of 94.2% is meaningless without three things: (1) a defined threshold below which action is required, (2) a defined action to take when the threshold is breached, and (3) a defined owner responsible for taking that action. Elementary's tiered approach (green/yellow/red with mapped actions) addresses this by coupling scores to response procedures [16]. The SRE-derived error budget model adds temporal dynamics — a score can be acceptable today but trigger action based on burn rate trajectory. Without these operational bindings, quality dashboards become the data equivalent of unread email: technically present, practically ignored. The healthcare sector provides supporting evidence: structured quality improvement approaches using PDSA cycles show measurable improvement, but only when measurement is coupled with systematic remediation workflows.

### Is DAMA-DMBOK's quality framework practical for modern data stacks?

Partially. DAMA-DMBOK provides the theoretical foundation — the dimension taxonomy, the "fitness for use" principle, the quality management lifecycle — but it offers limited tactical guidance for implementation [20]. The framework does not describe relationships between knowledge areas, does not address modern data pipeline architectures (ELT, streaming, lakehouse), and provides no tooling-specific guidance. The 2020 revision acknowledges this gap, and DMBOK 3.0 (started 2025) aims to modernize the framework. In practice, teams should use DAMA-DMBOK's dimensions as a communication vocabulary and starting taxonomy, then implement measurement using ecosystem-specific tooling: dbt tests for validity/completeness/uniqueness, source freshness for timeliness, Elementary or similar for composite scoring, and SLA frameworks borrowed from SRE rather than from DAMA's governance-heavy model. The framework's strength is organizational alignment; its weakness is engineering execution.

### 127 dimensions is too many — the taxonomy has fragmented beyond usefulness

The fragmentation is real but the conclusion is wrong. DAMA NL's research found 127 distinct dimension definitions, but many are synonyms, overlapping concepts, or context-specific variants of the same underlying property [4][20]. The US Department of Interior's 11 dimensions include "accurate to reality" and "accurate to surrogate source" as separate dimensions — a distinction that matters for their regulatory context but would be collapsed into "accuracy" for most data engineering teams [4]. The practical response is not to adopt all 127 but to use the six-dimension consensus as a starting vocabulary and extend with domain-specific dimensions as needed. The 127-dimension finding actually validates the "fitness for use" principle: quality dimensions proliferate because quality requirements are context-dependent.

### Composite scores hide more than they reveal

This criticism has merit. A composite score of 92% could mean all dimensions are at 92% (healthy) or that completeness is at 100% while accuracy is at 70% (dangerous). Weighted aggregation partially addresses this — if accuracy has a higher weight, the composite score drops more when accuracy degrades. But the fundamental tension between summary metrics and actionable detail remains. The resolution: composite scores serve leadership communication and trend tracking; dimension-level scores serve engineering investigation and remediation. Both are necessary. Teams that report only composite scores will miss dimension-specific degradation. Teams that report only dimension scores will overwhelm stakeholders with detail. Elementary's approach — composite score on the dashboard, dimension drill-down on click — gets this right [16].

---

## Findings

### Finding 1: Data quality is context-dependent and measurement requires explicit use-case definition
**Confidence: HIGH**

Data quality assessment cannot begin without defining who uses the data, for what purpose, and with what tolerance for imperfection. The "fitness for use" principle, established by Wang & Strong in 1996 and adopted by DAMA-DMBOK, means the same data can be simultaneously high quality and low quality depending on the consumer. Practical implication: quality rules, thresholds, and SLAs must be defined per data product and per consumer, not per table. A table-level quality score without consumer context is a technically measurable but operationally meaningless metric. Teams should define quality contracts at the data product level — who consumes this data, what dimensions matter to them, and what thresholds trigger action.

### Finding 2: Data profiling provides the measurement foundation and must precede rule definition
**Confidence: HIGH**

Structure profiling (shape, types, constraints), content profiling (distributions, null rates, cardinality, value patterns), and relationship profiling (key integrity, cross-table dependencies) produce the baselines against which quality is measured. Without profiling, quality rules are assumptions. Key profiling outputs — null rate for completeness, distinct count ratio for uniqueness, value frequency for distribution analysis, min/max/std for validity — map directly to quality dimensions. Profiling must be continuous, not one-time: initial profiling establishes baselines, ongoing profiling detects drift, and periodic re-profiling updates baselines as data legitimately evolves.

### Finding 3: Anomaly detection requires a layered approach — rules, statistics, and ML each serve different purposes
**Confidence: HIGH**

Rule-based checks enforce known constraints (not-null, accepted values, referential integrity) and are interpretable, editable, and immediately deployable. Statistical methods (z-score for normal data, IQR for skewed data, SPC control charts for time series) detect unexpected values and patterns without domain expertise. Distribution drift tests (KS for small datasets, Wasserstein for large datasets, PSI for stable distributions) detect shifts between reference and current data. ML-based approaches (autoencoders, isolation forests) discover unknown-unknowns at scale but require training data and produce opaque results. The optimal deployment is layered: rules as the foundation, statistics for distribution monitoring, ML for discovery — with each layer feeding findings back into rule refinement. Organizations that deploy ML without a strong rule foundation skip the highest-value, lowest-cost quality checks.

### Finding 4: Composite quality scores require weighted dimension aggregation with explicit action thresholds
**Confidence: MODERATE**

Scoring quality across dimensions requires four design decisions: which dimensions to include (use-case-driven, typically 4-7), how to score each dimension (percentage of passing checks or ratio of passing rows), how to weight dimensions (business-driven — accuracy may matter more than completeness for financial data, or vice versa), and what thresholds trigger action (green/yellow/red with mapped responses). Elementary's dbt-native approach demonstrates practical implementation: automatic test-to-dimension mapping, two scoring methods (test fail rate vs. failed row count), and historical trend tracking. The DQSOps framework introduces ML acceleration for high-velocity data. The moderate confidence reflects the limited evidence that composite scores drive better outcomes than dimension-level monitoring alone — the aggregation adds communication value but may reduce action specificity.

### Finding 5: Data quality SLAs must follow the SLI/SLO/SLA hierarchy with error budgets
**Confidence: HIGH**

The SRE-derived framework — SLIs measure, SLOs target, SLAs commit, error budgets prioritize — provides the most practical structure for data quality commitments. Error budgets resolve the feature-vs-reliability tension by making the trade-off quantitative: when the budget is healthy, ship features; when it is depleted, fix quality. Implementation requires tiered SLA structures (not all data deserves the same commitment), measurement queries (not prose descriptions), and monitoring frequency aligned with SLA granularity. Gartner's estimate of $12.9M annual cost of poor data quality provides business justification, but the SLA framework's real value is operational: it converts abstract quality aspirations into concrete engineering priorities with defined response procedures.

---

## Claims

| # | Claim | Source | Status | Notes |
|---|-------|--------|--------|-------|
| 1 | Wang & Strong 1996 identified 15 data quality dimensions in four categories | [19] | verified | Foundational paper; categories: intrinsic, contextual, representational, accessibility |
| 2 | DAMA NL identified 60 standardized dimensions and 127 distinct definitions across literature | [20] | verified | 2020 research; 12 common dimensions selected from the 60 |
| 3 | Six-dimension consensus (accuracy, completeness, consistency, timeliness, validity, uniqueness) is the most widely adopted | [1][2][4] | verified | Adopted by IBM, DAMA, dbt Labs; minor variations exist across organizations |
| 4 | Data quality is fundamentally context-dependent ("fitness for use") | [3][19] | verified | Established since 1980s; same data can be high/low quality depending on use case |
| 5 | KS test becomes overly sensitive on large datasets (100K+ rows), flagging 0.5% shifts | [8] | verified | Empirical comparison of 5 methods; Wasserstein recommended for large datasets |
| 6 | PSI thresholds: <0.1 no change, 0.1-0.2 moderate, >0.2 significant | [8] | verified | Standard thresholds, widely used in credit risk modeling |
| 7 | Elementary scores quality via test fail rate or failed row count methods | [16] | verified | Maps dbt tests to dimensions automatically; tracks historical trends |
| 8 | DQSOps achieves significant computational speedup via ML prediction while maintaining accuracy | [11][12] | verified | Peer-reviewed; dual-path architecture (ML prediction + standard scoring) |
| 9 | SLA error budgets drive engineering prioritization (>50% budget = ship, <25% = fix reliability) | [13] | qualified | SRE-derived framework; data-specific evidence is limited, but SRE precedent is strong |
| 10 | Gartner estimates poor data quality costs organizations $12.9M annually | [18] | verified | 2020 Gartner research; earlier 2017 estimate was $15M |
| 11 | Most organizations rely on manual, ad-hoc quality validation rather than systematic automation | [3] | verified | Frontiers peer-reviewed survey (2022); 667 tools identified but systematic adoption is low |
| 12 | Optimal anomaly detection combines rule-based and ML approaches in hybrid deployment | [10] | verified | Maturity model: rules-only (low) to ML-heavy (moderate) to balanced hybrid (optimal) |
| 13 | DAMA-DMBOK provides theoretical foundation but limited tactical execution guidance | [4][20] | verified | DMBOK 3.0 (started 2025) aims to address modern data stack gaps |
| 14 | Z-score uses |z|>3 threshold for normal data; IQR uses 1.5*IQR Tukey fences for skewed data | [7][8] | verified | Standard statistical methods; IQR more robust to outliers |
| 15 | SPC control charts use 3-sigma limits with Western Electric / Nelson rules for pattern detection | [9] | verified | ASQ professional standard; borrowed from manufacturing quality management |
