#!/usr/bin/env python3
"""Validate a data-product.md artifact before code generation.

Checks that a data-product.md file exists, has valid frontmatter, has the
correct artifact_type, and that each required section is not a pending marker.

Usage:
    python validate-data-product.py <data-product-name> [--require <sections>]

Arguments:
    data-product-name   Name of the data product (maps to docs/data-products/<name>/data-product.md)
    --require           Comma-separated list of sections to validate as non-pending
                        e.g. sources,contract,quality,architecture

Exit codes:
    0 — all checks passed
    2 — blocking error (missing artifact, invalid structure, pending section)
"""

import argparse
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


def section_is_pending(text: str, section: str) -> bool:
    """Return True if the section heading is followed immediately by a pending marker."""
    pattern = rf"^##\s+{re.escape(section.title())}\s*\n(<!--\s*pending:)"
    return bool(re.search(pattern, text, re.MULTILINE | re.IGNORECASE))


def section_exists(text: str, section: str) -> bool:
    """Return True if an H2 heading for the section exists in the body."""
    return bool(re.search(rf"^##\s+{re.escape(section.title())}", text, re.MULTILINE | re.IGNORECASE))


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a data-product.md artifact.")
    parser.add_argument("name", help="Data product name")
    parser.add_argument(
        "--require",
        default="",
        help="Comma-separated section names that must be non-pending",
    )
    args = parser.parse_args()

    name = args.name
    artifact = Path(f"docs/data-products/{name}/data-product.md")

    # 1. File exists
    if not artifact.exists():
        fail(
            f"data-product not found: {artifact}",
            f"Run /dos:scope-data-product to create the data product for '{name}'.",
        )

    text = artifact.read_text()

    # 2. Valid frontmatter with required fields
    fm = parse_frontmatter(text)
    if not fm:
        fail(
            f"No valid YAML frontmatter in {artifact}.",
            f"Run /dos:scope-data-product to regenerate the data product for '{name}'.",
        )

    required_fields = ["name", "artifact_type", "status", "version"]
    missing_fields = [f for f in required_fields if f not in fm]
    if missing_fields:
        fail(
            f"Missing frontmatter fields in {artifact}: {', '.join(missing_fields)}",
            f"Run /dos:scope-data-product to repair the data product for '{name}'.",
        )

    # 3. artifact_type == "data-product"
    if fm.get("artifact_type") != "data-product":
        fail(
            f"artifact_type is '{fm.get('artifact_type')}' in {artifact}, expected 'data-product'.",
            f"Check that {artifact} was created by /dos:scope-data-product.",
        )

    # 4. Each required section must exist and not be pending
    if args.require:
        sections = [s.strip() for s in args.require.split(",") if s.strip()]
        for section in sections:
            if not section_exists(text, section):
                fail(
                    f"Section '{section}' is pending or missing in {artifact}",
                    f"Run /dos:scope-data-product to populate the {section.title()} section",
                )
            if section_is_pending(text, section):
                fail(
                    f"Section '{section}' is pending or missing in {artifact}",
                    f"Run /dos:scope-data-product to populate the {section.title()} section",
                )

    print(f"PASS: data-product '{name}' passes validation")


if __name__ == "__main__":
    main()
