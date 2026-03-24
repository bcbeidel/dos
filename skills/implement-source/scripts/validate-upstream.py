#!/usr/bin/env python3
"""Validate upstream artifacts required by dos:implement-source.

Checks that a source evaluation scorecard exists, has valid frontmatter,
and contains required sections for code generation.

Usage:
    python validate-upstream.py <source-name>

Exit codes:
    0 — all checks passed
    2 — blocking error (missing artifact, invalid structure)
"""

import re
import sys
from pathlib import Path


def parse_frontmatter(text: str) -> dict[str, str]:
    """Extract YAML frontmatter fields as simple key-value pairs."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def fail(message: str, fix: str) -> None:
    """Print structured error and exit with code 2."""
    print(f"ERROR: {message}")
    print(f"FIX:   {fix}")
    sys.exit(2)


def main() -> None:
    if len(sys.argv) < 2:
        fail("No source name provided.", "Usage: python validate-upstream.py <source-name>")

    source = sys.argv[1]
    artifact = Path(f"docs/sources/{source}/evaluation.md")

    # Check file exists
    if not artifact.exists():
        fail(
            f"Source evaluation not found: {artifact}",
            f"Run dos:evaluate-source to create the scorecard for '{source}'.",
        )

    text = artifact.read_text()

    # Check frontmatter exists
    fm = parse_frontmatter(text)
    if not fm:
        fail(
            f"No valid YAML frontmatter in {artifact}.",
            f"Run dos:evaluate-source to regenerate the scorecard for '{source}'.",
        )

    # Check required frontmatter fields
    required = ["name", "artifact_type", "version", "status"]
    missing = [f for f in required if f not in fm]
    if missing:
        fail(
            f"Missing frontmatter fields in {artifact}: {', '.join(missing)}",
            f"Run dos:evaluate-source to add missing fields: {', '.join(missing)}.",
        )

    # Check required body sections
    body = text.split("---", 2)[-1] if text.count("---") >= 2 else text
    sections = {
        "Source Classification": "source type/classification",
        "Authentication": "auth mechanism",
        "Ingestion Recommendation": "ingestion approach",
    }
    missing_sections = []
    for heading, desc in sections.items():
        if not re.search(rf"^#+\s.*{re.escape(heading)}", body, re.MULTILINE | re.IGNORECASE):
            missing_sections.append(f"{heading} ({desc})")

    if missing_sections:
        fail(
            f"Missing required sections in {artifact}: {'; '.join(missing_sections)}",
            f"Run dos:evaluate-source to complete the scorecard for '{source}'.",
        )

    print(f"OK: {artifact} — valid scorecard with all required fields and sections.")


if __name__ == "__main__":
    main()
