# Anomaly Detection Methods

Anomaly detection requires a layered approach. Rules enforce known constraints and are immediately deployable. Statistical methods detect unexpected values without domain expertise. ML discovers unknown-unknowns at scale but produces opaque results. Organizations that deploy ML without a strong rule foundation skip the highest-value, lowest-cost checks.

## Three Detection Layers

1. **Rule-based** -- Known constraints (not-null, range, accepted values). Highest value, lowest cost. Deploy first.
2. **Statistical** -- Detect unexpected values without manual rules. Add after rules are established.
3. **ML-based** -- Autoencoders, isolation forests, DBSCAN. Only at scale (100K+ observations) alongside rules.

## Point Anomaly Methods

**Z-score:** Measures standard deviations from the mean. Threshold: |z| > 3. Best for normally distributed data. Limitation: sensitive to extreme values because mean and stddev are themselves affected by outliers.

**IQR (Interquartile Range):** Outlier boundaries at Q1 - 1.5*IQR and Q3 + 1.5*IQR (Tukey's fences). Best for skewed or non-normal distributions. More robust than z-score because quartiles are not distorted by extreme values.

**SPC (Statistical Process Control):** Control charts plot metrics over time with control limits at 3 standard deviations. Distinguishes common cause variation (expected) from special cause variation (requires investigation). Applies directly to pipeline metrics: daily row counts, null rates, value distributions.

## Distribution Drift Methods

| Method | Best For | Threshold | Key Detail |
|--------|----------|-----------|------------|
| KS test | Small datasets (<1K rows) | p < 0.05 | Overly sensitive at 100K+ rows |
| PSI | Stable distributions, finance | <0.1 no change, 0.1-0.2 moderate, >0.2 significant | Barely detects segment-level drift |
| Wasserstein Distance | Large datasets | Context-dependent | Best compromise for sensitivity vs practical relevance |
| Jensen-Shannon Divergence | Large datasets | 0.1 on 0-1 scale | Symmetric alternative to KL Divergence |

## Method Selection Guide

- **Normal distributions, point anomalies:** Z-score
- **Skewed distributions, point anomalies:** IQR
- **Time-series monitoring (row counts, null rates):** SPC control charts
- **Small datasets, high stakes:** KS test (most sensitive)
- **Large datasets (100K+ rows):** Wasserstein Distance (best compromise)

## Maturity Progression

1. **Rules-only** (start here) -- Known constraints, immediately deployable
2. **Rules + statistical** -- Add z-score/IQR for point anomalies, SPC for time-series
3. **Hybrid** (optimal) -- Rules + statistics + ML, each layer feeding findings back into rule refinement
