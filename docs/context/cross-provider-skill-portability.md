---
name: Cross-Provider Skill Portability
description: "AGENTS.md (60,000+ projects, 20+ tools) provides project-level context while Agent Skills (16+ tools) packages reusable capabilities; simple skills port cleanly across providers but complex skills with hooks, subagent configs, or tool restrictions do not; GitHub Agent HQ makes cross-provider compatibility operationally necessary"
type: context
related:
  - docs/research/2026-03-22-skill-design.research.md
  - docs/context/agentic-phase-patterns.md
  - docs/context/deterministic-gates-hooks.md
---

## Key Takeaway

Two complementary open standards enable cross-provider skill portability: AGENTS.md for project context and Agent Skills for packaged capabilities. Simple skills consisting of instructions and utility scripts port cleanly across Claude Code, GitHub Copilot, Cursor, and OpenAI Codex. Complex skills using provider-specific features (Claude Code's `context: fork`, prompt/agent handler types, SubagentStop hooks) do not port without modification. GitHub Agent HQ -- where multiple providers work the same repository -- makes this not theoretical but operationally necessary.

## AGENTS.md: Project Context Standard

AGENTS.md is an open format standard stewarded by the Agentic AI Foundation under the Linux Foundation. OpenAI originated the spec in August 2025 for Codex CLI; in December 2025, the Linux Foundation announced AAIF with AGENTS.md as one of three founding projects alongside Anthropic's MCP and Block's goose.

As of March 2026, these tools natively parse AGENTS.md: GitHub Copilot, Cursor, Windsurf, Zed, JetBrains Junie, OpenAI Codex CLI, Google Jules, Gemini CLI, Devin, Aider, goose, and others. One AGENTS.md file works across every major AI coding tool.

AGENTS.md is standard Markdown with no mandatory fields or rigid structure. Best practice is to keep it under 150 lines covering build commands, code style, testing instructions, and project conventions. This deliberate minimalism is both its strength (universal compatibility) and weakness (no quality enforcement). Two AGENTS.md files from different projects may bear no structural resemblance.

## Agent Skills: Capability Standard

While AGENTS.md tells agents how a project works, Agent Skills (agentskills.io) give agents new capabilities -- PDF processing, database analysis, deployment workflows. The spec requires only two frontmatter fields (`name` and `description`) and imposes minimal structure. A project typically has one AGENTS.md and multiple skills.

As of March 2026, 16+ tools support Agent Skills including Claude Code, GitHub Copilot, Cursor, OpenAI Codex, and Gemini CLI. The skill name must be max 64 characters, lowercase letters/numbers/hyphens only.

## Provider-Specific Extensions

Each provider extends the base standards with proprietary features:

- **Claude Code**: `context: fork` for subagent isolation, `disable-model-invocation` for manual-only skills, hooks in YAML frontmatter, three handler types (command, prompt, agent)
- **GitHub Copilot**: `.github/copilot-instructions.md` for workspace instructions, agent plugins in preview, hooks in `.github/hooks/*.json`
- **OpenAI Codex**: AGENTS.md as primary configuration, skills following the Agent Skills spec

Cross-provider skills should use only the base Agent Skills specification fields (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`) and avoid provider-specific extensions in the core SKILL.md.

## GitHub Agent HQ

GitHub launched Agent HQ in February 2026, allowing Copilot Pro+ and Enterprise users to run coding agents from multiple providers (Copilot, Claude, OpenAI Codex) directly inside GitHub, GitHub Mobile, and VS Code. GitHub is expanding to include agents from Google, Cognition, and xAI. The same repository will be worked on by different agents from different providers, making portable skill design a practical requirement.

## Decision Rules

1. Write core skill logic in the portable Agent Skills format. Layer provider-specific orchestration on top.
2. Keep AGENTS.md under 150 lines: build commands, code style, testing instructions, conventions.
3. Use only base Agent Skills spec fields in SKILL.md for cross-provider compatibility.
4. Implement validation as shell scripts callable by any provider's hook system, not provider-specific handler types.
5. Test skills with at least two providers before claiming portability.
