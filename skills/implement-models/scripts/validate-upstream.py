#!/usr/bin/env python3
"""Validate upstream artifacts for dos:implement-models.

Usage: python validate-upstream.py <data-product-name>
Exit 0 on success, exit 2 on blocking error.
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


def check_optional(path: Path, label: str) -> None:
    """Report optional artifact availability."""
    if path.exists():
        print(f"  {label}: available ({path})")
    else:
        print(f"  {label}: not found — will skip enrichment")


def main() -> None:
    if len(sys.argv) < 2:
        fail("No data product name provided.", "Usage: python validate-upstream.py <data-product-name>")

    product = sys.argv[1]
    base = Path(f"docs/data-products/{product}")
    contract = base / "contract.md"

    # Check contract exists (required)
    if not contract.exists():
        fail(
            f"Contract not found: {contract}",
            f"Run dos:define-contract to create the contract for '{product}'.",
        )

    text = contract.read_text()

    # Check frontmatter exists
    fm = parse_frontmatter(text)
    if not fm:
        fail(
            f"No valid YAML frontmatter in {contract}.",
            f"Run dos:define-contract to regenerate the contract for '{product}'.",
        )

    # Check required frontmatter fields
    required = ["name", "artifact_type", "version", "status"]
    missing = [f for f in required if f not in fm]
    if missing:
        fail(
            f"Missing frontmatter fields in {contract}: {', '.join(missing)}",
            f"Run dos:define-contract to add missing fields: {', '.join(missing)}.",
        )

    # Check schema section with at least one object/property
    body = text.split("---", 2)[-1] if text.count("---") >= 2 else text
    if not re.search(r"^#+\s.*[Ss]chema", body, re.MULTILINE):
        fail(
            f"No schema section found in {contract}.",
            f"Run dos:define-contract to add a schema section for '{product}'.",
        )
    if not re.search(r"(object|property|column|table)", body, re.IGNORECASE):
        fail(
            f"Schema section in {contract} has no object/property definitions.",
            f"Run dos:define-contract to define at least one object with properties.",
        )

    print(f"OK: {contract} — valid contract with schema definitions.")

    # Report optional artifact availability
    print("Optional inputs:")
    check_optional(base / "quality-config.md", "Quality config")
    check_optional(base / "pipeline-architecture.md", "Pipeline architecture")
    check_optional(base / "scope.md", "Scope document")


if __name__ == "__main__":
    main()
