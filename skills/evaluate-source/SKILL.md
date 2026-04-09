---
name: evaluate-source
description: Assess a data source's technical characteristics before pipeline construction. Produces a Source Evaluation Scorecard with six-dimension scoring, profiling results, and ingestion recommendations.
---

# dos:evaluate-source

Assess a data source's technical characteristics before pipeline construction. Walk through intake filtering, pricing assessment, source classification, six-dimension scoring, authentication assessment, data profiling, live API validation, and ingestion recommendation — producing a persistent Source Evaluation Scorecard.

## Preamble

Before starting, establish context:

1. **Which source?** Ask the user for a source name (e.g., `postgres-orders-db`, `stripe-api`). This determines the artifact path: `docs/sources/<source-name>/evaluation.md`. Sources are independent of data products — a source evaluation is reusable across multiple data products.
2. **Check for existing artifact.** If `docs/sources/<source-name>/evaluation.md` exists, read it, summarize the current state, and ask what's changing. Update the existing artifact rather than creating a new one.
3. **Check for related sources.** If other source evaluations exist in `docs/sources/`, note them — the user may be evaluating a related source for the same data product.

If the artifact exists, adjust the workflow: skip sections that haven't changed, focus on what the user wants to update, and bump the version in frontmatter.

## Workflow

### Step 1: Intake Filtering

Before investing in a full evaluation, ask two qualifying questions:

- **"What decision will you make with this data?"** — If no concrete use case, flag it. Data without a consumer is inventory, not a product.
- **"What is the real problem you're trying to solve?"** — Distinguishes data requests from underlying business needs that might be served differently.

If the request lacks a concrete use case, surface this before proceeding. The user may choose to continue anyway (exploratory evaluation) or redirect.

### Step 2: Source Metadata

Gather basic source information:

- Source name and description
- Source type (will be refined in classification)
- Data owner (team or individual who owns the source system)
- Data format (JSON, CSV, Parquet, database tables, API responses)
- Location (connection string, API base URL, S3 path)

### Step 3: Pricing & Cost

Assess the source's pricing model and cost implications before investing in a full technical evaluation. A source that costs more than the business value it delivers should be flagged early.

Refer to [pricing-models.md](references/pricing-models.md) for pricing model classification, billing unit disambiguation, common estimation pitfalls, and safeguards.

Gather the following inputs, marking each as **confirmed** (operator verified against contract or billing dashboard) or **estimated** (derived from documentation or assumptions):

| Input | What to Ask |
|-------|------------|
| Pricing model | "Is this source subscription, per-request, per-record, freemium, or free/open?" |
| Current plan/tier | "What plan or contract tier is the team currently on?" — do not assume from public pricing |
| Quota | "What are the monthly or daily request/record limits?" |
| Cost per unit | "What is the cost per API call or per record at your expected volume?" |
| Billing unit | "Is the billing unit per API call or per record returned?" — confirm explicitly |
| Overage policy | "What happens when you exceed the quota — hard stop, overage charges, or throttling?" |

**For free/open sources:** Note the pricing model as "free/open" and skip cost estimation. Rate limits and terms of service may still apply — capture these in Access Complexity (Step 5).

**Pipeline cost estimation** is deferred to Step 9 (Ingestion Recommendation), where the refresh cadence and request volume are known.

### Step 4: Source Classification

Classify the source into one of four types. Classification constrains available ingestion methods — this is not a free choice.

Refer to [source-classification-matrix.md](references/source-classification-matrix.md) for the full classification table, ingestion approach mapping, and the critical distinction between dlt (polling) and CDC (log-based).

| Source Type | Examples |
|-------------|----------|
| Transactional DB | PostgreSQL, MySQL, Oracle |
| Event Stream | Kafka, Kinesis, Pub/Sub |
| SaaS API | Salesforce, Stripe, HubSpot |
| File-Based | CSV/JSON via SFTP, S3 |

### Step 5: Six-Dimension Assessment

Score the source across six dimensions (1-5 scale). For each dimension, gather evidence from the user and assign a score.

Refer to [six-dimension-framework.md](references/six-dimension-framework.md) for detailed scoring criteria per dimension.

| Dimension | What to Assess |
|-----------|---------------|
| Connectivity | How the source exposes data (JDBC, REST, stream, file, webhook) |
| Volume | Data size at rest and change rate (use 95th percentile, not averages) |
| Freshness | Update frequency and reliable timestamp availability |
| Schema Stability | Change frequency and notification process over past 6-12 months |
| Data Quality | Baseline across DAMA dimensions from profiling |
| Access Complexity | Auth mechanism, rate limits, IP restrictions, token refresh |

**Schema stability warning:** Schema drift causes 7.8% of all data quality incidents, with 27% compounding per percentage-point increase in drift rate. SaaS APIs are the highest-risk type. Sources scoring 1-2 on schema stability require defensive pipeline design.

### Step 6: Authentication & Credential Management

Document the authentication mechanism and assess credential management practices.

Refer to [access-auth-patterns.md](references/access-auth-patterns.md) for the authentication mechanism inventory, anti-pattern checklist, and secrets manager options.

Gather:
- Authentication mechanism (OAuth M2M, API key, service account, key-pair, JDBC credentials)
- Where secrets are stored (secrets manager, env vars, config files)
- Rotation cadence (automated, scheduled, manual, never)
- Anti-patterns present (static PATs, shared credentials, secrets in code)

**Production standard:** Service principals with OAuth M2M (1h tokens). Any token lasting months is a liability.

### Step 7: Data Profiling

If the user can provide sample data (CSV, JSON, or Parquet file), run the profiling script:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/profile-sample.py <file_path>
```

The script outputs markdown tables covering column inventory, content metrics, and key candidates. Use `--json` to produce a machine-readable profile, or `--output profile.json` to write the JSON artifact alongside markdown output.

If the sample is a subset of the full dataset, pass the total population size:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/profile-sample.py <file_path> --sample-of 50000
```

The script will flag non-representative samples and include sampling provenance in the profile.

If no sample data is available, gather profiling information through conversation:
- Approximate row count and column count
- Known null patterns or quality issues
- Key candidates and relationships to other tables

#### Sampling Assessment

Before profiling, assess whether the sample data is representative. Ask:

> "Was this data loaded with a row limit or filter? Does the source API return records in a deterministic order (e.g., alphabetical by ID, by geography, by date)?"

If the answer is yes to either, the sample may be biased — distribution metrics should be treated as illustrative of value ranges, not population proportions.

**For paginated REST APIs**, the first page is often not representative. If the API returns geographically or categorically distributed data:

1. **Sample from multiple offsets** — request records from the first, middle, and last pages (e.g., offset 0, offset N/2, offset N-100) rather than only the first page.
2. **Minimum sample size** — aim for at least 100 records for baseline profiling. Fewer than 100 records should be flagged in the profile.
3. **Concat then profile** — save each page's response as a separate file, concatenate them, then profile the combined file. This produces a more representative baseline than profiling a single page.
4. **Record sampling provenance** — note in the scorecard which pages/offsets were sampled, so the profile can be meaningfully compared to a future full-dataset profile.

Refer to [profiling-metrics.md](references/profiling-metrics.md) for the three profiling types (structure, content, relationship), sampling representativeness guidance, and the mapping from profiling results to quality dimension baselines.

#### Profiling Types

Profile across all three types:

1. **Structure profiling** — column names, types, field lengths, naming consistency
2. **Content profiling** — null rates, distinct counts, uniqueness ratios, min/max, numeric distribution (mean, stddev, percentiles, IQR, skewness), pattern frequencies
3. **Relationship profiling** — key candidates, referential integrity, orphan detection (if multi-table)

Map profiling results to quality dimension baselines:
- Null rates → completeness baseline
- Uniqueness ratios on key candidates → uniqueness baseline
- Values within ranges/patterns → validity baseline
- Cross-field checks → consistency baseline

### Step 9: Ingestion Recommendation

Based on classification and dimension scores, recommend an ingestion approach.

Refer to [source-classification-matrix.md](references/source-classification-matrix.md) for the ingestion approach selection matrix and incremental pattern guidance.

| Approach | When to Use |
|----------|------------|
| Full load | Small dataset, no reliable change tracking |
| Incremental (cursor-based) | Moderate change rate, reliable timestamp or sequence |
| Incremental (merge) | Stateful records with updates |
| CDC (log-based) | High-frequency transactional, hard deletes matter |

**Critical:** dlt is a polling/extraction tool, not CDC. It does not read transaction logs. If log-based CDC is needed for high-frequency transactional sources, recommend Debezium or platform-native CDC instead of dlt.

#### Pipeline Cost Estimate

If the source has a priced pricing model (from Step 3), calculate the estimated pipeline cost now that the ingestion approach and refresh cadence are known.

Show the formula with actual values so the operator can verify each input:

```
requests_per_run × runs_per_month × cost_per_request = monthly_cost
monthly_cost × 12 = annual_cost
```

Label each input as **confirmed** or **estimated**. If the estimated monthly usage exceeds the current plan's quota, flag it: the team may need a tier upgrade or will incur overage charges.

Skip this subsection for free/open sources.

### Step 10: Re-Profiling Cadence

Set the re-profiling schedule based on the schema stability score:

| Schema Stability Score | Cadence |
|:----------------------:|---------|
| 1-2 (high drift) | Monthly |
| 3 (moderate) | Quarterly |
| 4-5 (stable) | Semi-annually |

Note the baseline profiling date and next scheduled profiling date. Profiling is continuous, not one-time.

### Step 11: Generate Scorecard

Produce the Source Evaluation Scorecard artifact using the template structure from [source-scorecard.md](assets/source-scorecard.md).

Save to `docs/sources/<source-name>/evaluation.md` with:
- Complete YAML frontmatter (name, artifact_type, version, owner, status, last_modified)
- All sections populated from the workflow above
- Changelog entry recording the evaluation

If updating an existing artifact:
- Bump the minor version
- Update `last_modified`
- Add a changelog entry describing what changed

### Step 12: Next Steps

End the scorecard with a "Next Steps" section recommending downstream skills:

1. **`/dos:scope-data-product`** — Define what the data product needs to be, driven by consumption intent. The source evaluation pre-populates known facts about source classification, profiling baselines, and ingestion approach.
2. **`/dos:design-pipeline`** — If pipeline architecture is the immediate concern, this skill consumes the source classification and ingestion recommendation directly.

Present these options to the user and explain what each downstream skill will do with the evaluation results.
