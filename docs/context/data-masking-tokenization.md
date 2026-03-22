---
name: Data Masking and Tokenization Techniques
description: "Static vs dynamic masking, tokenization, pseudonymization vs anonymization, format-preserving encryption — what each technique actually protects against and where each fails"
type: context
related:
  - docs/research/2026-03-22-privacy-engineering.research.md
  - docs/context/privacy-regulatory-requirements.md
  - docs/context/right-to-erasure-implementation.md
---

## Key Takeaway

Dynamic data masking is a convenience layer, not a security boundary — it is bypassable by anyone who can write SQL. Pseudonymized data remains personal data under GDPR; anonymized data does not. This distinction drives architecture choices more than any technical consideration. NIST withdrew FF3 format-preserving encryption in February 2025; FF1 is the sole remaining approved standard.

## Static vs Dynamic Masking

**Static data masking (SDM)** permanently transforms sensitive data before distribution, creating sanitized copies with no reversible path to originals. Use for non-production environments, data sharing with third parties, and training datasets. Drawback: copies become stale.

**Dynamic data masking (DDM)** applies masking rules at query time based on user roles. Stored data is never altered. Adds 2-10% CPU overhead per query. DDM security weaknesses are well-documented:

- **WHERE clause bypass** — queries execute against unmasked data before output filtering
- **Aggregate exposure** — SUM, AVG, COUNT return actual values regardless of masking
- **Pattern extraction** — LIKE queries leak string data character-by-character (~6,000 iterations for a 24-character email)
- **ORDER BY disclosure** — sorting reveals relative rankings
- **Binary search attack** — ~20 queries pinpoint exact numeric values

Microsoft explicitly states DDM "doesn't aim to prevent database users from connecting directly...and running exhaustive queries that expose pieces of the sensitive data."

**Use DDM for:** production dashboards with controlled interfaces, customer support tools, read-only reporting where users cannot compose arbitrary SQL. **Never use DDM as** a sole compliance mechanism or protection against users with direct query access.

## Tokenization

Tokenization replaces sensitive values with randomly generated tokens. The original data resides in a separate secure vault. Unlike encryption, tokens have no mathematical relationship to originals — reversal requires vault access, not computation.

Performance cost is significant for analytical workloads: LIKE searches, JOINs, and mathematical operations require decrypting entire columns. Best for extremely sensitive data with zero analytical value — credit card numbers (PCI DSS), SSNs, account numbers. Not suitable for ML training, BI dashboards, or any context where data utility matters.

## Pseudonymization vs Anonymization

This distinction is architecturally consequential because it determines GDPR applicability.

**Pseudonymization** (GDPR Article 4(5)) replaces identifying information while maintaining the ability to re-identify with separately stored additional information. Pseudonymized data **remains personal data under GDPR** — subject to full regulatory obligations including right to erasure, consent management, and breach notification. Methods: tokenization, deterministic encryption, key-coding, hashing with salt.

**Anonymization** permanently destroys the pathway back to individuals. Anonymized data **falls outside GDPR scope entirely**. Even the person who performed anonymization cannot reverse it. Methods: k-anonymity, differential privacy, generalization, aggregation.

The trade-off is utility versus regulatory burden. Pseudonymization preserves individual-level analysis (patient outcomes, customer journeys, realistic test data). Anonymization eliminates GDPR compliance overhead but destroys individual-level granularity. Most production pipelines use pseudonymization because downstream analytics require individual-level data — but teams must understand that tokenized data is still personal data.

## Format-Preserving Encryption (FPE)

FPE encrypts data while maintaining original format, length, and character set. A 16-digit credit card number encrypts to another 16-digit number. Useful for legacy systems that validate input formats.

NIST SP 800-38G defined two modes: FF1 and FF3. **FF3 was withdrawn entirely in February 2025** due to the Beyne attack. FF1 remains the sole approved standard, using 10 Feistel rounds (vs FF3's 8), providing stronger security at lower throughput. Google Cloud offers FPE-FFX mode but notes it "lacks authentication and an initialization vector" — less secure than deterministic encryption.

## Encryption Baseline

- **At rest:** AES-256, all major cloud providers encrypt by default. Key rotation annually minimum, quarterly for highly sensitive data.
- **In transit:** TLS 1.2 minimum, TLS 1.3 preferred. Perfect Forward Secrecy prevents retrospective decryption.
- **In use:** Confidential computing (Intel SGX, AMD SEV) is emerging but not yet standard for data pipelines.

Encrypting one state but not the other creates exploitable gaps. GDPR Article 32 and HIPAA both require encryption coverage across states.

## Decision Rules

1. Use static masking for non-production environments. Dynamic masking is not a substitute.
2. Use tokenization only for data that has no analytical value (card numbers, SSNs).
3. Understand that pseudonymized data carries full GDPR obligations. If you need to escape GDPR, you need true anonymization.
4. Use FF1 for format-preserving encryption. Do not use FF3 — it is no longer approved.
5. Implement DDM as a UI convenience layer on top of stronger protections, never as the sole control.
