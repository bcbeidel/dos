# Pricing Models Reference

Assess source pricing before investing in a full evaluation. Cost errors compound — wrong tier, wrong billing unit, and wrong volume estimate produced a 16x overstatement in a real evaluation session.

## Pricing Model Classification

| Model | How You Pay | Quota Pattern | Watch For |
|-------|------------|---------------|-----------|
| **Subscription** | Fixed monthly/annual fee | Tier-based limits (e.g., 10K requests/month on Basic) | Tier upgrade thresholds; features gated by plan |
| **Per-request** | Per API call made | Daily or monthly call limits | Batch endpoints that return multiple records per call — cost per *record* differs from cost per *request* |
| **Per-record** | Per record returned | Often combined with request limits | Pagination: one request may return 100 records but bill for 100 units |
| **Freemium** | Free tier with paid overage | Hard limit, then pay-per-use or upgrade | Free tier may have reduced rate limits or missing endpoints |
| **Free / Open** | No cost | Rate limits may still apply | Terms of service restrictions; attribution requirements |

## Billing Unit Disambiguation

The billing unit is the single most common source of cost estimation errors.

| Billing Unit | What It Counts | Example |
|-------------|---------------|---------|
| Per API call | Each HTTP request, regardless of records returned | 1 request returning 100 records = 1 billable unit |
| Per record returned | Each record in the response body | 1 request returning 100 records = 100 billable units |
| Per row written | Each row stored or synced to destination | May differ from records returned if transformation expands/filters |
| Per compute unit | Processing time or data volume | Snowflake credits, BigQuery slots |

**Always confirm:** "Is the billing unit per API call or per record returned?" A 100x difference is common.

## Common Estimation Pitfalls

| Pitfall | How It Happens | Mitigation |
|---------|---------------|------------|
| Wrong tier assumed | Using public pricing page instead of actual contract | Ask for the current plan/contract tier directly |
| Wrong billing unit | Assuming per-request when it's per-record (or vice versa) | Confirm billing unit explicitly before estimating |
| Documentation volume estimates | Using "up to 1M records" from docs when actual is 50K | Query actual production row count or check billing dashboard |
| Ignoring pagination costs | Estimating 1 request when full extraction requires 100 pages | Calculate: total_records / page_size = requests needed |
| Missing rate limit impact | Not accounting for throttling that slows extraction | Check if rate limits require spreading requests across time windows |
| Overage surprise | Assuming hard stop when the API charges per excess unit | Confirm overage policy before first production run |

## Cost Estimation Safeguards

Before finalizing a pipeline cost estimate, verify each input:

| Safeguard | Check |
|-----------|-------|
| Plan/tier is confirmed | Operator verified against contract or billing dashboard — not assumed from public pricing |
| Billing unit is confirmed | Operator explicitly stated "per API call" or "per record" — not inferred |
| Volume is from actuals | Row count from production query or billing dashboard — not documentation estimates |
| Pagination is accounted for | Total requests = total_records / page_size, not 1 |
| Calculations are shown | Formula with actual values printed so operator can catch errors |
| Each input is labeled | "confirmed" (operator verified) or "estimated" (from docs or assumptions) |
