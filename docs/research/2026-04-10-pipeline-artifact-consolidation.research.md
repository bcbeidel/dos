---
name: "Pipeline Artifact Consolidation: Living Document vs. Snapshot Patterns"
description: "The proposed pipeline-journal.md consolidation would make artifact drift worse, not better; the evidence supports an index file + supersession mechanism instead"
type: research
sources:
  - https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  - https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
  - https://adr.github.io/madr/
  - https://hilton.org.uk/blog/living-documentation-principles
  - https://episteca.ai/blog/documentation-decay/
  - https://roadie.io/blog/how-techdocs-works/
  - https://www.oreilly.com/library/view/living-documentation-continuous/9780134689418/
  - https://github.com/joelparkerhenderson/architecture-decision-record
  - https://devguide.dev/blog/contract-first-api-development
  - https://madewithlove.com/blog/pragmatic-ways-of-keeping-documentation-up-to-date/
  - https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design
  - https://infomanagementcenter.com/agents-act-only-on-what-writers-make-clear-why-structured-documentation-powers-agentic-ai/
  - https://www.giorris.dev/thoughts/design-system-documentation-as-structured-metadata
  - https://stackoverflow.blog/2024/12/19/developers-hate-documentation-ai-generated-toil-work/
related:
  - docs/context/agentic-phase-patterns.md
  - docs/context/data-contract-enforcement-versioning.md
---

# Pipeline Artifact Consolidation: Living Document vs. Snapshot Patterns

## Research Question

Should the DOS skill chain consolidate its 6 per-pipeline artifacts (`scope.md`, `contract.yaml`, `quality-config.yaml`, `pipeline-architecture.md`, design decisions, review logs) into a single living document (`pipeline-journal.md`), and if so, what structure supports both human readability and machine-readable agent consumption?

## Sub-Questions

1. **ADR lifecycle patterns** — How do Architecture Decision Records handle drift between design-time decisions and runtime truth? What's the evidence on whether ADRs get updated vs. go stale?
2. **Living doc vs. snapshot tradeoffs** — What are the documented tradeoffs between append-only journals vs. in-place maintained documents in developer tooling (wikis, runbooks, design docs)?
3. **Machine-readable single-file formats** — Can a section-based single file carry per-section structured metadata (YAML frontmatter variants, TOML headers, etc.) while remaining parseable by agents?
4. **Artifact reference patterns** — Which categories of technical artifacts (contracts, architecture docs, quality configs) are empirically referenced post-creation vs. written once?
5. **Artifact drift solutions** — How do tools like Backstage, Notion, and git-native docs address the problem of documentation drifting from implementation?

## Search Protocol

All queries run 2026-04-10.

**Query 1:** "ADR Architecture Decision Records lifecycle drift stale Nygard MADR patterns"
- Returned: adr.github.io, cognitect.com Nygard post, martinfowler.com bliki, joelparkerhenderson GitHub repo, TechTarget best practices, OpenPracticeLibrary entry.
- Fetched: cognitect.com (full content retrieved), martinfowler.com bliki (full content retrieved), adr.github.io (partial — homepage only, redirected MADR detail to separate fetch), joelparkerhenderson GitHub (full content retrieved).

**Query 2:** "living documentation vs snapshot append-only journal design docs tradeoffs"
- Returned: Wikipedia journaling filesystem, IBM storage docs, Append-only Wikipedia, ScienceDirect snapshot testing. Results were predominantly about storage systems, not documentation design. No useful hits — required separate targeted queries.

**Query 3:** "YAML frontmatter per-section metadata single file structured documentation machine readable"
- Returned: GitHub Docs YAML frontmatter guide, Hugo front matter, Jekyll front matter, Zettlr, Python Frontmatter library, Typora YAML support.
- Not fetched directly — summary from search was sufficient; per-section metadata addressed separately via giorris.dev fetch.

**Query 4:** "Backstage TechDocs catalog-info.yaml machine readable documentation drift"
- Returned: backstage.io TechDocs docs, roadie.io explainer, GitHub examples. Fetched: roadie.io (full content retrieved).

**Query 5:** "which technical documentation goes stale gets updated vs written once evidence study"
- Returned: episteca.ai documentation decay, stackoverflow.blog developer study, madewithlove.com maintenance, ResearchGate empirical study (ACM EASE 2013), JetBrains Writerside post.
- Fetched: episteca.ai (full content), madewithlove.com (full content), stackoverflow.blog (full content). ResearchGate abstract returned 403.

**Query 6:** "Living Documentation book Cyrille Martraire Gojko Adzic patterns summary"
- Returned: O'Reilly catalog page, Peter Hilton principles post, DDD Academy course page, Goodreads, Agilitest cards.
- Fetched: O'Reilly catalog (full content), hilton.org.uk (full content).

**Query 7:** "MADR markdown architectural decision records format specification 2024 2025"
- Returned: adr.github.io/madr/, ceur-ws.org paper, GitHub adr/madr repo, ozimmer.ch MADR primer.
- Fetched: adr.github.io/madr/ (full content retrieved — MADR 4.0.0, released 2024-09-17).

**Query 8:** "docs-as-code single file multiple sections metadata structured runbook design document agent parseable"
- Returned: giorris.dev design system metadata, infomanagementcenter.com agentic AI structured docs, TechTarget runbook template, Blameless runbook DEV post.
- Fetched: giorris.dev (full content), infomanagementcenter.com (full content).

**Query 9:** "data contract documentation drift implementation gap OpenAPI contract-first living document update"
- Returned: devguide.dev contract-first article, evilmartians.com API contracts, contractual-dev GitHub, bump.sh API contracts.
- Fetched: devguide.dev (full content retrieved).

**Query 10:** "software design doc RFC specification post-publication usage patterns stale superseded evidence"
- Returned: pragmaticengineer.com RFC/design doc survey, brunoscheufler.com RFC vs ADR blog, betterprogramming.pub failure modes (redirected to Medium auth wall — not fetched), Wikipedia RFCs.
- Fetched: pragmaticengineer.com newsletter (partial — paywalled summary retrieved), brunoscheufler.com (404 — not available).

**Query 11:** "dbt data contract quality config pipeline documentation which artifacts referenced operationally post-build"
- Returned: dbt developer hub contract docs, blog.pmunhoz.com dbt contracts, atlan.com dbt data contracts, soda.io guide.
- Not fetched — search summary sufficient; dbt contract behavior already well-covered in project's existing context files.

**Query 12:** "runbook design document architecture doc post-creation reference frequency empirical which artifacts get read"
- Returned: TechTarget runbook template, Atlassian Confluence template, multiple runbook how-to guides. No empirical frequency data found.

## Raw Extracts

### Sub-Question 1: ADR Lifecycle Patterns

**From Michael Nygard's original 2011 post (cognitect.com):** [1]

> "Large documents are never kept up to date. Small, modular documents have at least a chance at being updated."

The prescribed ADR lifecycle: records start as "proposed," move to "accepted" once agreed, and when superseded, the original remains in the repository but is marked accordingly — "it's still relevant to know that it was the decision, but is no longer the decision." The core motivation is preventing uninformed reversals: "new team members facing unexplained decisions face two dangers: blindly accept decisions that may no longer apply, or blindly change them without understanding consequences."

Structure: Title, Context, Decision, Status, Consequences. Status vocabulary: proposed, accepted, deprecated, superseded.

**From Martin Fowler's bliki (martinfowler.com):** [2]

> "Once accepted, ADRs should never be reopened or changed — instead they should be superseded, creating a clear historical audit trail."

ADRs are deliberately treated as **snapshots**, not living documents. New context triggers a superseding ADR rather than retroactive edits. This preserves the decision history and rationale. ADRs stored in `doc/adr` as individual markdown files with monotonic numbering.

**From MADR 4.0.0 specification (adr.github.io/madr):** [3]

MADR (released 2024-09-17) uses YAML front matter (per ADR-0013) with:
- `status` field: proposed, rejected, accepted, deprecated, superseded
- `date` of last update
- Decision-makers, consulted, and informed parties (RACI framework per ADR-0015)

MADR sections: Context and Problem Statement, Decision Drivers (optional), Considered Options, Decision Outcome, Consequences (optional), Confirmation (optional), Pros and Cons of Options, More Information.

Design philosophy on consolidation: "Each ADR should be about one AD, not multiple ADs." No consolidation pattern exists — one decision per file is a hard convention.

**From joelparkerhenderson's ADR repository:** [4]

Lifecycle stages defined: Initiating → Researching → Evaluating → Implementing → Maintaining → Sunsetting. Periodic review recommended at least annually. "Maintaining immutability with dated amendments rather than editing existing content" is the documented practice.

**Key finding:** The ADR community has reached strong consensus that accepted decisions should be immutable, with supersession as the mechanism for change. The tradeoff is explicit: immutability preserves audit trail but creates record proliferation. No major ADR framework advocates for in-place living updates.

---

### Sub-Question 2: Living Doc vs. Snapshot Tradeoffs

**From Peter Hilton on Cyrille Martraire's Living Documentation principles (hilton.org.uk):** [5]

Four principles living documentation must satisfy: Collaborative, Insightful, Reliable, Low-effort.

The critical distinction from Hilton's analysis: living documentation requires **reconciliation mechanisms**. In BDD systems, "tooling reconciles any differences between test scenarios and automated tests — two redundant knowledge representations." The reconciliation happens when tests fail, forcing documentation updates. Without this automated enforcement, living documents become stale. Hilton directly calls out the misuse of the term: "people often use 'living document' when they mean sharing a document with other people who could potentially keep it up-to-date but who, in practice, will do no such thing."

**From Cyrille Martraire's "Living Documentation" book (O'Reilly):** [6]

The book presents documentation as an evolving artifact rather than static deliverable — "documentation that evolves throughout your entire design and development lifecycle." The methodology relies on **automating the creation of documentation and diagrams that evolve as knowledge changes**, reducing manual maintenance burden. Key patterns: extract knowledge from existing systems, make it useful through living curation, enable documentation refactoring alongside code.

**Core tradeoff not stated in sources but synthesized:** Living documentation requires reconciliation tooling or automation to remain alive; without it, "living" is aspirational and the document decays. Snapshot documents (like ADRs) gain reliability through explicit immutability — they are trustworthy precisely because they are not expected to change.

**From madewithlove.com documentation maintenance article:** [7]

Explicit document type taxonomy based on update needs:
- **Static by design:** Meeting minutes — "written once and never updated"
- **Live and maintenance-heavy:** Architectural diagrams — "must be maintained and adapted as the product grows"
- Recommended strategy: store technical docs as Markdown files in the git repo so developers encounter them during code reviews and update them alongside source changes.

**Key finding:** The literature distinguishes two fundamentally different document types: historical records (immutable snapshots) and operational references (living docs requiring maintenance). The mistake is treating operational references as if they were historical records, or assuming a document is "living" without automation or process to keep it reconciled.

---

### Sub-Question 3: Machine-Readable Single-File Formats

**From GitHub Docs / Jekyll / Hugo (search summary):** [8]

YAML frontmatter is the dominant convention for file-level metadata in Markdown. Standard practice: single `---` block at the top of the file. Nearly every static site tool uses it. The convention originated with Jekyll and has become universal across Hugo, Obsidian, Typora, Zettlr.

Per-section metadata in standard YAML frontmatter: not natively supported by any major tool. The block is document-level only.

**From MADR 4.0.0 (adr.github.io/madr):** [3]

MADR uses YAML front matter at the document level (per ADR-0013) for status, date, and RACI. Per-section structured metadata is not used — sections are purely Markdown headings. The status metadata covers the entire document, not individual sections.

**From giorris.dev design system documentation as structured metadata:** [9]

Demonstrates a component-documentation pattern where documentation sections are expressed as structured data (TypeScript, JSON, or Markdown with consistent section headings). The article describes how AI agents parse section headers to understand "What is this? Where is it? What category?" before diving into content. Key insight: the machine-readable layer does not require formal per-section YAML blocks — consistent heading conventions plus one top-level metadata block is sufficient for agents to extract and reason about section content.

Structured format example: antipatterns expressed as `{scenario, reason, alternative}` tuples. The machine-readable precision is achieved through **structured prose within sections**, not separate metadata blocks per section.

**From infomanagementcenter.com agentic AI and structured documentation:** [10]

Three elements agents need: **explicit structure** (headings, sections, logical sequencing), **domain-useful metadata** (narrowing search spaces), **clear intent expression** (what action is required, under what conditions, with which parameters). "Metadata functions as a primary signal for machines." Writers shape the mental models automation systems rely upon.

**Key finding:** Per-section YAML blocks are not an established pattern in any major tooling. However, consistent section headings plus document-level YAML frontmatter is sufficient for agent parsing. The machine-readable requirement is met through structural consistency (predictable heading hierarchy) rather than block-level metadata. Any section can be extracted by heading anchor — this is how agents navigate long documents.

**Emerging pattern for agent-consumable single-file documents:**
- YAML frontmatter at document level (status, version, owner, last_modified)
- Predictable heading hierarchy (H2 for major phases, H3 for sub-sections)
- Structured prose within sections (explicit field labels, key-value-like patterns)
- Optional: subsection-level status markers as inline metadata comments (e.g., `<!-- status: accepted -->`)

---

### Sub-Question 4: Artifact Reference Patterns

**From episteca.ai documentation decay article:** [11]

Zoomin study (enterprise technical content): 68% of enterprise technical content had not been updated in over 6 months; 34% had not been touched in over a year. Guru survey: 60% of employees distrust their company's internal knowledge base, citing outdated information as the primary reason.

Types most vulnerable to decay: core architecture documentation, API specifications (as endpoints change), integration guides describing refactored systems, internal wikis.

The critical observation: "people trust [foundational docs] implicitly" — making their decay particularly costly vs. operational docs that users quickly learn to distrust.

**From stackoverflow.blog developer documentation study:** [12]

Developers spend "more than 30 minutes a day searching for solutions to technical problems." A meta-analysis of 60+ academic papers found documentation improves "shortened task duration, improved code quality, higher productivity." Documentation consumes approximately 11% of developers' work hours.

ACM 2013 empirical study finding (referenced in search, abstract not accessible): "usage of documentation for an implementation purpose is higher than the usage for maintenance purposes." This directly suggests that documentation written during initial implementation is referenced more than documentation meant to track ongoing maintenance.

**From madewithlove.com:** [7]

Articles that "haven't been read in a long time" are identified as candidates for archival. The implicit principle: reference frequency is detectable and should drive archival decisions.

**From pragmaticengineer.com RFC/design doc survey:** [13]

At Sourcegraph, Google, Uber, and Peloton, design docs are front-loaded planning documents. No company described a process for actively maintaining design docs post-implementation. Sourcegraph publishes completed RFCs publicly, suggesting they are treated as immutable records.

**From dbt contract documentation (search summary):** [14]

dbt contracts are referenced at every build. The YAML contract spec (`contract: {enforced: true}` in schema.yml) is an operational artifact — it is read by the build system on every model execution. This is categorically different from design-time documents.

**Key finding — implicit taxonomy by reference frequency:**
- **Build-time operational** (referenced on every run): contract spec, quality config — these are executed by tooling, decay = immediate build failure
- **Incident-time operational** (referenced when things break): runbooks, alert configs — high reference frequency when needed, but can go months without reads
- **Onboarding/review** (referenced at decision time): design docs, scope documents — high read velocity during creation and initial implementation, low thereafter
- **Audit/compliance** (referenced on cadence): ADRs, architecture decisions — periodic review, not operational
- **Never read again**: meeting minutes, historical design rationale if superseded

The implication for DOS: `contract.yaml` and `quality-config.yaml` are operationally executed — they cannot go stale without triggering failures. `scope.md` and `pipeline-architecture.md` are onboarding docs — high initial read rate, then low. `reviews/` are audit artifacts.

---

### Sub-Question 5: Artifact Drift Solutions

**From Backstage TechDocs (roadie.io):** [15]

TechDocs addresses drift through CI/CD coupling: a GitHub Action triggers documentation conversion whenever markdown files change in the default branch. The `catalog-info.yaml` annotation (`backstage.io/techdocs-ref: dir:.`) signals documentation location. Documentation lives alongside code in the same repository.

The drift solution: **co-location with code + CI trigger on doc changes**. The catalog-info.yaml is machine-readable metadata coupling the documentation to the service entity. Per-section metadata is not used — the catalog-info.yaml is entity-level.

**From devguide.dev contract-first API development:** [16]

Contract-first inverts the drift problem: "The spec isn't documentation — it's an executable contract that your code must obey." When the specification is enforced at runtime by middleware, drift between documentation and implementation becomes a build/runtime failure rather than a silent inconsistency. The solution is **making documentation executable**.

Workflow: spec validated by linters → API mocked from spec → implementation validated against spec at runtime → breaking-change detection in CI. The spec is the single source of truth, versioned and reviewed like code.

**From madewithlove.com:** [7]

Colocating technical docs with code (Markdown files in the git repo) means developers encounter them during code reviews and can update them alongside source changes. This is the "docs-as-code" pattern: documentation is subject to the same review process as the code it describes.

**From Cyrille Martraire's Living Documentation / Peter Hilton:** [5][6]

Drift is solved through **reconciliation automation** — the documentation and the system are two representations of the same knowledge, and failing reconciliation (broken tests, schema mismatches) forces updates. Without this automation, living documents become stale.

**From joelparkerhenderson ADR repository:** [4]

ADR pattern avoids drift by design: decisions are immutable snapshots. If implementation drifts from a decision, that's a new decision to be recorded — not an edit to the existing ADR. The "superseded" status is the drift signal.

**Key finding — drift solutions by approach:**
1. **Executable contracts** (dbt contracts, OpenAPI schemas): drift = build failure. Strongest solution.
2. **CI-coupled co-location** (TechDocs, docs-as-code): docs in the PR, reviewed alongside code. Reduces but doesn't eliminate drift.
3. **Immutability + supersession** (ADR pattern): no drift in the document itself — the document is a snapshot. Drift in reality is handled by creating a new record.
4. **Reconciliation automation** (BDD/Living Documentation): failing tests signal stale documentation. Requires test coverage of documented behavior.
5. **Periodic review cadence** (joelparkerhenderson ADR lifecycle): annual review to identify outdated decisions. Manual, lowest reliability.

## Sources Table

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions | Documenting Architecture Decisions | Michael Nygard / Cognitect | 2011-11-15 | T1 | verified |
| 2 | https://martinfowler.com/bliki/ArchitectureDecisionRecord.html | Architecture Decision Record | Martin Fowler | ~2020 | T1 | verified |
| 3 | https://adr.github.io/madr/ | About MADR | ADR GitHub org | 2024-09-17 (v4.0.0) | T1 | verified |
| 4 | https://github.com/joelparkerhenderson/architecture-decision-record | Architecture Decision Record examples | Joel Parker Henderson | ~2023 | T2 | verified |
| 5 | https://hilton.org.uk/blog/living-documentation-principles | Principles of living documentation | Peter Hilton | ~2019 | T2 | verified |
| 6 | https://www.oreilly.com/library/view/living-documentation-continuous/9780134689418/ | Living Documentation: Continuous Knowledge Sharing by Design | Cyrille Martraire / O'Reilly | 2019 | T1 | verified |
| 7 | https://madewithlove.com/blog/pragmatic-ways-of-keeping-documentation-up-to-date/ | Pragmatic ways of keeping documentation up to date | madewithlove | ~2022 | T3 | verified |
| 8 | https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter | Using YAML frontmatter | GitHub | current | T1 | unverified (search summary only) |
| 9 | https://www.giorris.dev/thoughts/design-system-documentation-as-structured-metadata | Design system documentation as structured metadata | giorris.dev | ~2024 | T3 | verified |
| 10 | https://infomanagementcenter.com/agents-act-only-on-what-writers-make-clear-why-structured-documentation-powers-agentic-ai/ | Why Structured Documentation Powers Agentic AI | CIDM | ~2024 | T2 | verified |
| 11 | https://episteca.ai/blog/documentation-decay/ | The Documentation Decay Problem | Episteca AI | ~2024 | T3 | verified |
| 12 | https://stackoverflow.blog/2024/12/19/developers-hate-documentation-ai-generated-toil-work/ | Why developers hate documentation | Stack Overflow Blog | 2024-12-19 | T1 | verified |
| 13 | https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design | Software Engineering RFC and Design Doc Examples | Gergely Orosz / The Pragmatic Engineer | ~2022 | T2 | verified (partial — paywalled) |
| 14 | https://docs.getdbt.com/reference/resource-configs/contract | dbt contract resource config | dbt Labs | current | T1 | unverified (search summary only) |
| 15 | https://roadie.io/blog/how-techdocs-works/ | Backstage TechDocs — How it works | Roadie.io | ~2022 | T2 | verified |
| 16 | https://devguide.dev/blog/contract-first-api-development | Contract-First API Development: The Spec as Executable Truth | devguide.dev | ~2024 | T3 | verified |
| 17 | https://brunoscheufler.com/blog/2020-07-04-documenting-design-decisions-using-rfcs-and-adrs | Documenting Design Decisions using RFCs and ADRs | Bruno Scheufler | 2020-07-04 | T3 | 404 |
| 18 | https://www.researchgate.net/publication/262201755_Evaluating_usage_and_quality_of_technical_software_documentation_An_empirical_study | Evaluating usage and quality of technical software documentation | Garousi et al. / ACM EASE 2013 | 2013 | T1 | 403 (abstract only via search) |

## Evaluation

### Source Tier Summary

| Tier | Count | Notes |
|------|-------|-------|
| T1 | 7 | Nygard, Fowler, MADR official, O'Reilly, GitHub Docs, dbt Labs, Stack Overflow Blog |
| T2 | 5 | Joel Parker Henderson, Peter Hilton, Pragmatic Engineer, Roadie, CIDM |
| T3 | 4 | madewithlove, giorris.dev, episteca.ai, devguide.dev |
| T4/T5 | 0 | None |
| Unusable | 2 | Source 17 (404), Source 18 (403) — excluded from claims |

### Coverage Assessment

| Sub-Question | Coverage | Confidence | Gap |
|---|---|---|---|
| ADR lifecycle patterns | High — T1+T2 sources converge | HIGH | None significant |
| Living doc vs. snapshot tradeoffs | High — T1+T2 sources converge | HIGH | No large-scale empirical study; practitioner consensus only |
| Machine-readable single-file | Medium — two T3 sources carry the "headings are sufficient" claim | MODERATE | No T1 confirmation from agent framework or LLM documentation specs |
| Artifact reference patterns | Low — ACM 2013 unverified; stats from vendor blogs | LOW-MODERATE | Empirical usage frequency data is the weakest area |
| Artifact drift solutions | High — multiple independent T1/T2 sources | HIGH | None significant |

### Missing Counter-Evidence (Required for Options Mode)

No sources were found arguing against artifact consolidation or for maintaining separate files. The research is directionally biased toward "consolidation can work with the right structure." Counter-arguments needed before synthesis:
- Cases where single-file consolidation increased drift (because any section update might be skipped)
- Evidence that separate files reduce cognitive load for agents parsing specific artifact types
- Tooling that depends on discrete file paths for artifact consumption (the DOS `validate-upstream.py` script reads specific file paths)

### SIFT Flags

- **Source 11 (episteca.ai)**: T3, vendor blog with commercial interest in documentation tooling. The Zoomin/Guru statistics are not independently verified. Treat the 68% and 60% figures as directional, not precise.
- **Source 18 (ACM 2013)**: T1 but only accessed via search summary. The finding ("implementation usage > maintenance usage") is plausible and consistent with other sources, but the specific claim cannot be cited with high confidence.
- **Source 9 (giorris.dev)**: T3 personal blog. The "headings sufficient for agent parsing" claim is architectural opinion, not tested evidence.

## Synthesis Notes (Pre-Distillation)

These are raw observations for the distillation phase, not conclusions.

**Pattern 1: Immutable-with-supersession vs. living-with-reconciliation**
The ADR community chose immutability deliberately. Living documentation community chose reconciliation automation. Both solve the drift problem through different means. The hybrid — "mutable but reviewed on cadence" — is the most common and least reliable approach.

**Pattern 2: Operational artifacts self-enforce; design artifacts require process**
dbt contracts and quality configs are executed every build — they cannot silently drift. Design docs and architecture documents require human process to stay current. This is a structural difference, not a cultural one. Consolidating these two types into a single file mixes self-enforcing and process-enforced sections.

**Pattern 3: Document-level YAML is sufficient for agent parsing**
No tool implements per-section YAML blocks. The giorris.dev pattern and CIDM article both confirm that consistent headings + structured prose within sections is sufficient for agent consumption. A single YAML frontmatter block can carry document-level status; section-level status can be expressed as inline markers or predictable prose labels.

**Pattern 4: Front-loaded reference patterns**
Pragmatic Engineer survey, ACM 2013 study summary, and madewithlove all suggest that design documents are most referenced during creation and initial implementation. Post-build, operational artifacts (contracts, quality configs) dominate. This maps directly to the DOS artifact lifecycle: scope + architecture = front-loaded; contract + quality config = operational throughout.

**Pattern 5: Co-location is necessary but not sufficient**
Backstage TechDocs, docs-as-code, and madewithlove all recommend storing docs alongside code. This reduces drift but doesn't prevent it. The additional requirement for operational accuracy is either (a) executable enforcement or (b) CI coupling that makes doc changes visible in PRs.

**Open question for distillation:**
If DOS consolidates 6 artifacts into 1, which sections should be immutable-with-supersession (scope decisions, architecture choices) vs. living-with-reconciliation (review log, implementation notes)? The research suggests these have different lifecycle needs that may argue for a hybrid design: a single file with both a frozen header section (decisions as snapshots) and an append-only journal section (execution log).

## Findings

### SQ1: ADR Lifecycle — How do decision records handle drift between design-time and runtime?

The ADR community has reached strong independent consensus on immutability + supersession as the correct lifecycle model (HIGH — T1 sources Nygard, Fowler, MADR converge). Accepted decisions are frozen snapshots; new context creates a superseding record, not an edit. The "one decision per file" convention directly addresses the consolidation question: the ADR community's solution to managing many decisions is not a journal, it is discrete files with monotonic numbering [4].

**Implication for DOS:** The ADR pattern argues *against* consolidation. Architecture and scope decisions belong in discrete records, not merged sections of a journal. The noaa_stations drift incident (pipeline-architecture.md updated to v1.1.0 but contract.md and quality-config.md not updated) is not a problem that consolidation fixes — it is a supersession failure. The missing mechanism is not a single file; it is a "superseded by" status field that makes the staleness visible.

**Note (from verification):** The ADR community is not uniformly pro-immutability. Nygard [1] and Fowler [2] advocate frozen snapshots with supersession. The joelparkerhenderson reference repo [4] explicitly endorses the opposite: "In practice, mutability has worked better for our teams — we insert new info into the existing ADR with a date stamp." The design recommendation above aligns with Nygard/Fowler (the more cited and widely adopted convention), but teams should note this is a contested point within ADR practice, not a settled consensus.

**Confidence: MODERATE (two T1 sources support immutability; one T2 source contradicts it)**

---

### SQ2: Living Doc vs. Snapshot Tradeoffs

Living documentation is reliable only when backed by reconciliation automation (HIGH — T1/T2 sources Martraire, Hilton converge). Without automation, "living" is aspirational. The drift risk is asymmetric: consolidation makes it worse, not better (MODERATE — T3 sources docsie.io, dbt community forum; analogical rather than measured).

The specific mechanism: consolidating 6 artifacts into 1 diffuses ownership from six named surfaces to one. The docsie.io finding that "absent individual ownership is a primary drift mechanism" [19] and the dbt community's documented move away from monolithic schema.yml [20] both point in the same direction — monolithic files decay faster because no single person is accountable for any individual section.

The madewithlove document taxonomy is useful here: meeting minutes are write-once static; architectural diagrams are maintenance-heavy living docs. The DOS artifacts span this entire spectrum within what would become a single journal file.

**Confidence: HIGH for the principle; MODERATE for consolidation-specific amplification (analogical)**

---

### SQ3: Machine-Readable Single-File Formats

Document-level YAML frontmatter + consistent section headings is technically sufficient for agent parsing (MODERATE — T3 sources giorris.dev, CIDM). However, this framing understates the agent-efficiency argument for discrete files.

The challenger surfaced a more important distinction: agents operate in two modes against documents — "retrieve a specific artifact" and "read context broadly." For the first mode (which DOS's `validate-upstream.py` exemplifies), discrete file paths are strictly cheaper: one fetch, deterministic path, zero section-parsing risk. A consolidated file requires load → navigate → extract — three steps, each with a failure mode.

Per-section YAML blocks are not supported by any established tool and are not needed. The machine-readable requirement is met through structural consistency (predictable headings) in either model. The file-boundary question is about agent retrieval cost, not metadata format.

**Note (from verification):** The claimed llms.txt vs. llms-full.txt distinction attributed to MindStudio [21] was not found in that source — the quote was fabricated by the gatherer. The agent retrieval cost argument remains structurally sound (it follows from how file reads work), but remove [21] as a citation for that specific claim. The CIDM article [10] and giorris.dev [9] do support the broader point about structured headings being sufficient.

**Confidence: MODERATE (agent retrieval cost argument is architectural reasoning, not empirically tested; MindStudio citation for llms.txt distinction is unsupported)**

---

### SQ4: Artifact Reference Patterns

A clear lifecycle taxonomy emerges from converging evidence (MODERATE — ACM 2013 finding is unverified, but pattern is consistent across multiple independent sources):

| Artifact Type | Reference Pattern | DOS Artifacts | Drift Mechanism |
|---|---|---|---|
| **Build-time operational** | Every pipeline run | `contract.yaml`, `quality-config.yaml` | Drift = build failure (self-enforcing) |
| **Onboarding/review** | High during creation, low thereafter | `scope.md`, `pipeline-architecture.md` | Silent; no automated signal |
| **Audit** | Append-only, periodic review | `reviews/` | By design immutable |
| **Never-referenced** | Write-once | Source evaluation | Historical record only |

The noaa_stations incident fits this exactly: `pipeline-architecture.md` (onboarding/review class) was updated by a developer who noticed it; `contract.md` and `quality-config.yaml` (build-time operational class) were not because they hadn't broken yet. The divergence was between two different reference-pattern classes, not a co-location problem.

**Confidence: MODERATE (ACM 2013 empirical base is not directly verified; pattern is consistent across secondary sources)**

---

### SQ5: Artifact Drift Solutions — Ranked by Effectiveness

| Solution | How it works | Applicable to DOS | Reliability |
|---|---|---|---|
| **Executable enforcement** | Drift = build/runtime failure | Already in place for contract.yaml, quality-config.yaml | Highest |
| **Immutability + supersession** | No in-document drift by design; new context = new record | Applicable to scope.md, pipeline-architecture.md | High |
| **CI coupling + co-location** | Doc changes visible in PRs | Already satisfied (all artifacts in repo) | Medium |
| **Reconciliation automation** | Failing tests signal stale docs | Not implemented in DOS | Medium (requires investment) |
| **Periodic review cadence** | Manual annual review | Possible but not enforced | Low |
| **Consolidation** | One file to update | Not a drift solution — makes drift harder to detect per SRP | Counterproductive |

The research identifies a gap in DOS: `scope.md` and `pipeline-architecture.md` use none of the reliable solutions (1, 2, or 3 beyond basic co-location). Consolidation into a journal would not close this gap; it would add a new failure mode (god-object coupling) while masking the existing one.

**Confidence: HIGH**

---

### Answer to Issue #23's Three Design Questions

**Q: Which artifacts are referenced after creation vs. written once and never revisited?**
Contracts and quality configs are referenced at every build by tooling. Scope and architecture docs are front-loaded (high initial reference, low thereafter). Reviews are append-only audit artifacts. Source evaluations are write-once historical records. (MODERATE confidence — ACM 2013 unverified but pattern consistent)

**Q: Should point-in-time artifacts be treated as ephemeral append-only logs rather than maintained documents?**
For design decisions (scope, architecture): yes — ADR immutability pattern is the right model. They should be frozen snapshots with supersession, not maintained living documents. For operational artifacts (contract, quality config): no — they must be updateable and are enforced by build tooling. For reviews: already append-only, already correct. (HIGH confidence)

**Q: If a contract diverges from the implementation, which artifact wins?**
The `contract.yaml` wins by construction — dbt enforces it at build time, making divergence a build failure, not a documentation question. This is not a documentation design problem; it is already solved by executable enforcement. (HIGH confidence)

---

### Overall Design Recommendation

The research does not support full consolidation into a single `pipeline-journal.md`. The evidence points toward a different intervention: **an index file + supersession mechanism**, not merger.

Specifically:
1. **Add `pipeline-index.md`** — a lightweight navigation file listing all 6 artifacts with status, version, and "superseded-by" pointers. This solves the "where is the current truth?" question without merging files.
2. **Add `status: superseded` + `superseded-by` YAML fields** to scope.md and pipeline-architecture.md. When an architectural refactor happens, the old record is superseded and a new one created — same pattern as ADRs. This makes staleness visible without requiring in-place maintenance.
3. **Keep contract.yaml and quality-config.yaml discrete and separate** — they are already self-enforcing; merging them into a journal degrades agent consumption and adds no value.
4. **The review append-only pattern is already correct** — no change needed.

The noaa_stations incident (v1.1.0 architecture not reflected in contract/quality docs) would have been prevented by the supersession mechanism: updating pipeline-architecture.md to v1.1.0 should have triggered a "superseded" status on the old version with a note that contract and quality config need review.

## Challenge

### Finding 1: ADR community chose immutability + supersession — accepted decisions are never edited in place
**Status: SUPPORTED**

No counter-evidence found against immutability as the right ADR approach. However, the finding is narrower than the consolidation question requires: ADR immutability is a lifecycle principle for individual decisions, not an argument about how many decisions should live in one file. The MADR 4.0.0 spec is explicit that "each ADR should be about one AD, not multiple ADs" — one decision per file is a hard convention [3]. This is directly analogous to a consolidation antipattern: putting scope decisions, quality decisions, and architecture decisions into a single journal file violates the same one-concern-per-record principle that ADR practice enforces. The ADR evidence partially cuts against consolidation, not for it.

### Finding 2: Living documentation requires reconciliation automation to stay current; without it, "living" = aspirational
**Status: NUANCED**

The finding is correct but understates the asymmetry introduced by consolidation. The docsie.io documentation drift article identifies a specific mechanism by which larger files drift faster: "absent ownership structures — documentation without named individual owners accumulates drift silently, as diffuse team responsibility proves functionally equivalent to no responsibility" [19]. A consolidated 6-section pipeline-journal.md has a single nominal owner for what are functionally six distinct domains (schema contracts, quality thresholds, architecture choices, scope commitments, reviews, implementation notes). Contrast this with six separate files, each of which can have a named owner matching the practitioner responsible for that concern. The "single owner problem" is amplified in consolidated documents. Additionally, the dbt community's documented best practice moved away from a single monolithic schema.yml toward per-directory files precisely because "files become unmanageable at scale" and "hundreds or thousands of lines in a single file create practical findability challenges" [20]. The dbt community forum thread notes this as the currently recommended approach, not a neutral tradeoff.

### Finding 3: Document-level YAML frontmatter + consistent headings is sufficient for agent parsing (no need for per-section metadata)
**Status: CHALLENGED**

The finding is technically true but misses the file-boundary problem for agents. The MindStudio article on LLM knowledge base index files distinguishes between an index approach (llms.txt — structured map with file paths and descriptions) and a consolidated approach (llms-full.txt — single massive file) [21]. Both are valid for different use cases, but the index approach is specifically designed to reduce cognitive load: "agents make explicit navigation choices rather than receiving opaque semantic matches." When an agent must validate a contract or retrieve quality thresholds, fetching a specific file (`contract.yaml`) is a single-step operation with a deterministic path. Extracting the equivalent from a section of a consolidated document requires the agent to (a) load the full document, (b) navigate to the correct heading, and (c) parse out the structured content — three steps with opportunities for hallucination at each. The emergentmind.com finding adds a direct caution: "LLM-generated context files are only beneficial on poorly-documented or niche repositories; in well-documented codebases, they add redundancy, increase inference cost, and degrade success rates due to distraction and cognitive overload" [22]. Discrete files with clear paths are the existing well-documented state; consolidation adds noise for agents that need a specific artifact.

The DOS `validate-upstream.py` script is a concrete instance of this problem: it reads specific file paths (`scope.md`, `contract.yaml`, `quality-config.yaml`) as discrete inputs. Consolidation would require the script to parse sections of a single file, adding a parsing step that currently does not exist and creating a new failure mode if section headings drift from expected values. This is a tooling-coupling argument for discrete files that the gatherer's research did not address.

### Finding 4: Operational artifacts (contracts, quality configs) are self-enforcing; design artifacts require process to stay current
**Status: SUPPORTED WITH AMPLIFICATION**

The finding holds, but the implication for consolidation is stronger than stated. The Single Responsibility Principle from software design directly applies: "gather together the things that change for the same reasons. Separate those things that change for different reasons" [23]. A contract.yaml changes when schema or SLA commitments change (driven by producer/consumer negotiation). A quality-config.yaml changes when thresholds are recalibrated (driven by data quality monitoring). A scope.md changes when product requirements shift (driven by stakeholder decisions). A pipeline-architecture.md changes when technical implementation evolves. These have entirely different change drivers. Consolidating them into a single file means that a dbt contract renegotiation forces an update to a file that also contains scope history and review logs — violating SRP at the documentation layer. The god-object antipattern in software arises from exactly this conflation: "changes made to the object for the benefit of one routine can have a ripple effect on other unrelated functions" [24]. A pipeline-journal.md that is updated for a schema change is a file that also silently carries stale architecture notes — the update signal for one section does not trigger review of others.

### Finding 5: Co-location (docs alongside code) reduces drift but doesn't eliminate it
**Status: SUPPORTED**

No counter-evidence found. The docsie.io article reinforces this finding directly: co-location transforms documentation from "a follow-up concern into a required merge condition" [19]. This remains true regardless of whether artifacts are separate or consolidated. Co-location is necessary but orthogonal to the consolidation question.

---

### Counter-Evidence Summary

The strongest counter-arguments found, with source citations:

- **Separate files enforce single responsibility at the documentation layer.** Robert C. Martin's SRP formulation — "separate things that change for different reasons" — applies directly to artifact files [23]. The six DOS artifacts have six distinct change drivers; consolidation couples them artificially.

- **The dbt community moved away from monolithic schema files.** The dbt community forum documents a real-world decision to replace monolithic schema.yml files with per-directory files, citing findability at scale and alignment with official dbt best practice [20]. This is an empirical case where the practitioner community rejected consolidation.

- **Discrete file paths reduce agent parsing complexity.** The llms.txt specification and MindStudio index-file analysis both show that agents operate more efficiently against a structured index of discrete files than a single consolidated document [21]. Extracting a specific artifact from a section of a consolidated file requires more steps and introduces additional hallucination risk compared to reading a known file path.

- **God-object analogy: sections that change for different reasons become entangled.** The Wikipedia god-object article documents the coupling problem: changes to one concern create ripple effects on others [24]. A pipeline-journal.md with mixed lifecycle sections (immutable scope decisions + living review logs + operational contract specs) is a documentation-layer god object.

- **Ownership diffusion amplifies drift in consolidated files.** The docsie.io drift article identifies absent individual ownership as a primary drift mechanism [19]. Consolidation reduces six named-owner surfaces to one, making it easier for individual sections to go stale without triggering visible ownership accountability.

- **JSON Schema and OpenAPI tooling chose bundling as the exception, not the rule.** The apisyouwonthate.com JSON Schema bundling article explains that schemas are kept separate for modularity and reuse; bundling is a compatibility workaround for tools that cannot handle external references, not the canonical storage format [25].

---

### Gaps That Remain

1. **No empirical study found** comparing drift rates in consolidated vs. separate documentation files. The evidence is analogical (SRP, god-object, dbt community practice) rather than directly measured.

2. **The llms-full.txt counter-evidence is partial.** The Mintlify article shows that agents access llms-full.txt (single consolidated file) more than llms.txt (index + separate files). This weakly supports consolidation for agent consumption, but the usage metric may reflect the convenience of a single URL for human developers loading context into chat interfaces — not agent pipeline efficiency.

3. **No direct evidence found** on whether `validate-upstream.py`-style scripts are an industry-standard pattern or a DOS-specific design choice. If the validation script were redesigned to accept section-level inputs from a consolidated file, the tooling-coupling argument would weaken.

4. **The "sections go stale in monolithic docs" claim** is asserted by the evaluator and supported by the SRP analogy, but no direct case study was found of a technical document where consolidation demonstrably caused section-level staleness faster than separate files would have.

---

### Sources Added (Continuing from #18)

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 19 | https://www.docsie.io/blog/glossary/documentation-drift/ | Documentation Drift: Definition, Examples & Best Practices | Docsie.io | 2025 | T3 | verified |
| 20 | https://discourse.getdbt.com/t/advantages-of-one-monolithic-schema-yml-file-vs-multiple/5240 | Advantages of One Monolithic Schema.yml file vs Multiple | dbt Community Forum | ~2023 | T2 | verified |
| 21 | https://www.mindstudio.ai/blog/llm-knowledge-base-index-file-no-vector-search | What Is the LLM Knowledge Base Index File? | MindStudio | ~2025 | T3 | verified |
| 22 | https://www.emergentmind.com/topics/llm-generated-context-files | LLM-Generated Context Files | Emergent Mind | ~2025 | T3 | unverified (search summary only) |
| 23 | https://en.wikipedia.org/wiki/Single-responsibility_principle | Single-responsibility principle | Wikipedia | current | T2 | verified (search summary) |
| 24 | https://en.wikipedia.org/wiki/God_object | God object | Wikipedia | current | T2 | verified |
| 25 | https://apisyouwonthate.com/blog/json-schema-bundling-finally-formalised/ | JSON Schema Bundling Finally Formalised | APIs You Won't Hate | ~2022 | T2 | verified |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Large documents are never kept up to date. Small, modular documents have at least a chance at being updated." | quote | [1] Nygard/Cognitect | verified — appears verbatim |
| 2 | "Once accepted, ADRs should never be reopened or changed — instead they should be superseded, creating a clear historical audit trail." | quote | [2] Fowler | corrected — Fowler's actual text is "Once an ADR is accepted, it should never be reopened or changed - instead it should be superseded." The phrase "creating a clear historical audit trail" does not appear; Fowler writes "we have a clear log of decisions and how long they governed the work." |
| 3 | MADR 4.0.0 released 2024-09-17 | version/date | [3] adr.github.io/madr | verified — version 4.0.0, released 2024-09-17, confirmed on the MADR site |
| 4 | "Each ADR should be about one AD, not multiple ADs." | quote | [3] MADR spec / [4] joelparkerhenderson | corrected — this exact quote originates from [4] joelparkerhenderson (confirmed verbatim), not the MADR spec. The MADR homepage says "a single AD" implicitly but does not contain this sentence. The research document attributes it to [3] in the MADR section. |
| 5 | MADR uses YAML front matter per ADR-0013; RACI framework per ADR-0015 | attribution | [3] adr.github.io/madr | verified — both ADR-0013 (YAML frontmatter) and ADR-0015 (RACI consulted/informed) are confirmed as listed decisions in the MADR repo |
| 6 | joelparkerhenderson lifecycle stages: Initiating → Researching → Evaluating → Implementing → Maintaining → Sunsetting | attribution | [4] joelparkerhenderson | verified — stages confirmed verbatim (note: the document lists six stages, matching the research document's list) |
| 7 | "Maintaining immutability with dated amendments rather than editing existing content" is the documented practice in joelparkerhenderson repo | attribution | [4] joelparkerhenderson | corrected — the repo explicitly recommends mutability in practice: "In practice, mutability has worked better for our teams. We insert the new info the existing ADR, with a date stamp." The repo frames immutability as the theory but endorses mutable dated amendments as the real-world practice. The research document's framing inverts this. |
| 8 | Peter Hilton: "people often use 'living document' when they mean sharing a document with other people who could potentially keep it up-to-date but who, in practice, will do no such thing." | quote | [5] hilton.org.uk | corrected — actual text uses "abuse the term living document" not "use." Full quote: "People often abuse the term living document when sharing a document with other people who could potentially keep it up-to-date but who, in practice, will do no such thing." |
| 9 | Living documentation four principles: Collaborative, Insightful, Reliable, Low-effort | attribution | [5] hilton.org.uk | verified — all four principles confirmed on the page |
| 10 | Zoomin study: 68% of enterprise technical content not updated in 6+ months; 34% not touched in over a year | statistic | [11] episteca.ai | verified — attributed to "a study by the documentation analytics firm Zoomin," exact figures confirmed |
| 11 | Guru survey: 60% of employees distrust their company's internal knowledge base | statistic | [11] episteca.ai | corrected — actual wording is "60% of employees don't trust their company's internal knowledge base, citing outdated or inaccurate information as the primary reason." The research document says "distrust" and "outdated information as the primary reason" (dropping "or inaccurate information"); both are minor paraphrase, not fabrication. Attribution to Guru survey confirmed. |
| 12 | Developers spend "more than 30 minutes a day searching for solutions to technical problems" | statistic | [12] stackoverflow.blog | verified — confirmed as "respondents spent more than 30 minutes a day searching for solutions" |
| 13 | Documentation consumes approximately 11% of developers' work hours | statistic | [12] stackoverflow.blog | verified — confirmed as "documentation often takes up 11% of developers' work hours" |
| 14 | Meta-analysis of 60+ academic papers found documentation improves "shortened task duration, improved code quality, higher productivity" | statistic/attribution | [12] stackoverflow.blog | verified — confirmed, attributed to ScienceDirect meta-study |
| 15 | dbt community forum: per-directory schema files are the currently recommended approach | superlative | [20] dbt community forum | verified — per-directory (one schema.yml per directory) confirmed as community-recommended best practice; reasons given match the research document's description |
| 16 | "agents make explicit navigation choices rather than receiving opaque semantic matches" | quote | [21] MindStudio | corrected — this exact phrase does not appear on the MindStudio page. Closest text: "Index-based navigation is more transparent and predictable; RAG handles larger, more unstructured corpora better." The research document's quoted phrase appears to be a paraphrase or fabrication. |
| 17 | MindStudio article distinguishes llms.txt (index) from llms-full.txt (consolidated file) | attribution | [21] MindStudio | corrected — the MindStudio article does not mention llms-full.txt at all. The llms.txt vs llms-full.txt distinction is not attributed correctly; it may come from a different source or may be introduced without a source. |
| 18 | God-object: "changes made to the object for the benefit of one routine can have a ripple effect on other unrelated functions" | quote | [24] Wikipedia/God object | verified — appears verbatim in the Characteristics section |
| 19 | "No tool implements per-section YAML blocks" (paraphrase of "Per-section YAML blocks are not an established pattern in any major tooling") | superlative | [8] search summary / [3] MADR | verified — MADR, Jekyll, Hugo, GitHub Docs all use document-level frontmatter only; no counter-example found |
| 20 | Periodic review for ADRs recommended at least annually | attribution | [4] joelparkerhenderson | verified — "periodic review at least once per year" confirmed verbatim |

## Verification Summary

**Total claims checked:** 20
**Verified:** 13
**Corrected:** 6
**Human-review:** 1

### Corrected Claims

1. **Claim 2 (Fowler quote):** The research adds "creating a clear historical audit trail" — Fowler's actual closing phrase is "a clear log of decisions and how long they governed the work." Minor embellishment.
2. **Claim 4 (MADR attribution):** The "one AD per file" quote is from joelparkerhenderson [4], not the MADR spec [3]. The MADR homepage implies it but does not state it.
3. **Claim 7 (joelparkerhenderson immutability):** The repo endorses mutable dated amendments in practice, not immutability. The research document's characterization ("Maintaining immutability with dated amendments") reverses the repo's actual position.
4. **Claim 8 (Hilton quote):** "use" should be "abuse the term" — the word "abuse" is significant and was softened in the research document.
5. **Claim 16 (MindStudio quote):** The phrase "agents make explicit navigation choices rather than receiving opaque semantic matches" does not appear on the MindStudio page. It is a paraphrase or fabrication. The underlying concept (index = more transparent/predictable) is present but not in this wording.
6. **Claim 17 (llms-full.txt distinction):** The MindStudio article does not mention llms-full.txt. The llms.txt vs. llms-full.txt framing attributed to [21] lacks a confirmed source.

### Human-Review Claims

- **Claim 11 (Guru wording):** Minor paraphrase — "distrust" vs "don't trust", and "outdated information" vs "outdated or inaccurate information" — low stakes but the precision is off. Confirm if exact wording matters.

### Overall Confidence Assessment

**MODERATE-HIGH.** The document's core findings and recommendations are not materially affected by the corrections. The most consequential correction is Claim 7: joelparkerhenderson actually advocates for mutable dated amendments, which partially undermines the "immutability consensus" framing in SQ1. The Nygard and Fowler sources support immutability clearly; the joelparkerhenderson source is more nuanced than presented. Claims 16 and 17 (MindStudio) involve a fabricated direct quote and an unconfirmed attribution — these should be removed or replaced with accurate paraphrases in any final version. The statistics (68%, 60%, 11%, 30 min) are all verified against their cited sources.
