# CLAUDE.md

## What This Is

A Claude Code plugin (`dos`) with 4 active skills covering the data engineering lifecycle: Discover → Scope → Build. Skills are invoked as `/dos:<skill-name>` and produce persistent artifacts in `docs/`.

## Project Structure

```
skills/<name>/           # Each skill is a directory
  SKILL.md               # Portable Agent Skills spec (<500 lines)
  references/            # Curated decision tables, criteria (<200 lines each)
  assets/                # Output artifact templates (markdown with YAML frontmatter)
  scripts/               # Deterministic validation (Python, exit 0=pass, 2=fail)
docs/
  sources/               # Source evaluation scorecards (from scope-source)
  data-products/<name>/data-product.md  # Single living document: Overview, Sources, Contract, Quality, Architecture, Changelog
  context/               # 66 research-backed context files (authoring inputs, not runtime)
  designs/               # Design documents
  plans/                 # Implementation plans with task checkboxes
  research/              # SIFT-framework research documents
```

## Skill Architecture

- **SKILL.md** is the portable core. Under 500 lines. References loaded via relative links.
- **References** contain decision matrices, criteria tables, platform-specific thresholds. No explanatory prose.
- **Assets** are artifact templates with `{{placeholder}}` syntax and YAML frontmatter.
- **Scripts** validate upstream artifacts before LLM work (Build-phase skills only).
- Skills are CRUD operators on artifacts — they check for existing artifacts before creating new ones.
- Every artifact has YAML frontmatter: `name`, `artifact_type`, `version`, `owner`, `status`, `last_modified`.
- Every artifact ends with a changelog and "Next Steps" suggesting downstream skills.

## Skill Chain

| Phase | Skills | Output Location |
|-------|--------|-----------------|
| Discover | `scope-source` | `docs/sources/<source>/` |
| Scope | `scope-data-product` | `docs/data-products/<name>/data-product.md` |
| Build | `implement-source` | project codebase |
| Build | `implement-data-product` | project codebase + orchestration artifacts |

Each skill works independently. When chained, downstream skills consume upstream artifacts to skip redundant questions.

## Key Conventions

- **Template-first authoring:** When creating or modifying skills, write the asset template before references, and references before SKILL.md.
- **Inline references only:** SKILL.md references curated files inline within workflow steps, never in a separate summary section.
- **Graceful degradation:** Every skill works without upstream artifacts. Missing artifacts mean more questions, not errors.
- **Build-phase scripts:** `implement-source` and `implement-data-product` run `validate-data-product.py` before code generation. Exit 2 = blocking error with structured fix suggestion.

## Working with Context Files

Context files in `docs/context/` are authoring inputs distilled into skill references. They are NOT runtime dependencies — skills carry their own knowledge. When modifying a skill's references, read the source context files listed in the design document's reference table.

@AGENTS.md
