---
name: Anomaly and Drift Detection
description: "Anomaly detection should layer rule-based checks (known constraints) with statistical methods (z-score, IQR, SPC, KS test) and ML approaches (only at scale) -- each serves a different purpose; KS test is overly sensitive on large datasets; Wasserstein Distance is the best large-dataset compromise"
type: context
related:
  - docs/research/2026-03-22-quality-engineering.research.md
  - docs/context/data-profiling.md
  - docs/context/data-quality-scoring.md
  - docs/context/data-observability-pillars.md
---

## Key Takeaway

Anomaly detection requires a layered approach. Rules enforce known constraints and are immediately deployable. Statistical methods detect unexpected values without domain expertise. ML discovers unknown-unknowns at scale but produces opaque results. Organizations that deploy ML without a strong rule foundation skip the highest-value, lowest-cost quality checks. The optimal deployment layers all three, with each layer feeding findings back into rule refinement.

## Point Anomaly Detection

Three foundational methods for detecting anomalous individual values:

**Z-score**: Measures how many standard deviations a value is from the mean. Threshold: |z| > 3. Best for normally distributed data. Limitation: sensitive to extreme values because mean and standard deviation are themselves affected by outliers. Inappropriate for skewed distributions.

**IQR (Interquartile Range)**: Uses quartiles rather than mean/std. Outlier boundaries at Q1 - 1.5*IQR and Q3 + 1.5*IQR (Tukey's fences). Best for skewed or non-normal distributions. More robust than z-score because quartiles are not distorted by extreme values.

**Statistical Process Control (SPC)**: Control charts plot metrics over time with a center line (mean) and control limits at 3 standard deviations. Distinguishes common cause variation (inherent, expected) from special cause variation (assignable, requiring investigation). Western Electric and Nelson rules define patterns indicating special cause variation -- runs, trends, oscillations. Applies directly to pipeline metrics: plot daily row counts, null rates, or value distributions and investigate when points exceed control limits or exhibit patterns.

## Distribution Drift Detection

Drift detection compares a reference distribution to a current distribution:

| Method | Best For | Sensitivity | Key Detail |
|--------|----------|-------------|------------|
| KS test | Small datasets (<1K rows) | Very high | p-value < 0.05; overly sensitive at 100K+ rows |
| PSI | Stable distributions, finance | Low | <0.1 = no change, 0.1-0.2 = moderate, >0.2 = significant |
| Wasserstein Distance | Large datasets | Moderate | Best compromise between sensitivity and practical relevance |
| Jensen-Shannon Divergence | Large datasets | Moderate | 0.1 on 0-1 scale |
| KL Divergence | Large datasets | Low | Asymmetric -- order matters |

Critical implementation detail: KS test becomes overly sensitive on large datasets (100K+ rows), flagging shifts as small as 0.5% that have no practical significance. For large datasets, Wasserstein Distance offers the best compromise. PSI is widely used in credit risk modeling but barely detects segment-level drift.

## Method Selection Guide

- **Small datasets, high stakes**: KS test (most sensitive, statistically rigorous)
- **Large datasets, balanced approach**: Wasserstein Distance (interpretable, moderate sensitivity)
- **Normal distributions, point anomalies**: Z-score (simple, fast)
- **Skewed distributions, point anomalies**: IQR (robust to outliers)
- **Time series monitoring**: SPC control charts (pattern detection, not just threshold breach)

## ML-Based Approaches

ML methods (autoencoders, isolation forests, DBSCAN) learn expected patterns and flag deviations without manual thresholds. Primary advantage: discovering anomalies humans would not write rules for. Primary disadvantage: the black-box problem -- explaining why an anomaly was flagged is difficult.

The maturity progression: rules-only (low maturity) to ML-heavy (moderate maturity) to balanced hybrid (optimal maturity). ML adds value only at scale (100K+ observations) and requires hybrid deployment alongside rules.

## Decision Rules

1. Start with rule-based checks for known constraints. This is the highest-value, lowest-cost layer.
2. Add statistical methods (z-score or IQR) for distribution monitoring before considering ML.
3. Use KS test for small datasets; switch to Wasserstein Distance above 100K rows.
4. Deploy SPC control charts for time-series pipeline metrics (row counts, null rates).
5. Introduce ML-based detection only after rules and statistics are established, and only at sufficient data scale.
