#!/usr/bin/env python3
"""
Script to update frontmatter of markdown files under 2022/ and 2023/ folders.

Features:
- Add/update 'date' field to YYYY-mm-ddT00:00:00+08:00 format from filename
- Rename 'tag' (if exists) to 'tags'
- Replace spaces in tags with underscores
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml


def extract_date_from_filename(filename: str) -> Optional[str]:
    """Extract date from filename in format YYYY-mm-dd and convert to ISO format."""
    # Look for YYYY-mm-dd pattern in filename
    date_pattern = r"(\d{4}-\d{2}-\d{2})"
    match = re.search(date_pattern, filename)

    if match:
        date_str = match.group(1)
        try:
            # Validate the date format
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None
        else:
            return f"{date_str}T00:00:00+08:00"
    return None


def clean_tags(tags: list[str]) -> list[str]:
    """Replace spaces in tags with underscores."""
    return [tag.replace(" ", "_") for tag in tags]


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse frontmatter from markdown content."""
    if not content.startswith("---\n"):
        return {}, content

    # Find the end of frontmatter
    end_marker = content.find("\n---\n", 4)
    if end_marker == -1:
        return {}, content

    frontmatter_str = content[4:end_marker]
    body = content[end_marker + 5 :]

    try:
        frontmatter = yaml.safe_load(frontmatter_str) or {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML frontmatter: {e}")
        return {}, content
    else:
        return frontmatter, body


def serialize_frontmatter(frontmatter: dict[str, Any]) -> str:
    """Serialize frontmatter back to YAML string."""
    if not frontmatter:
        return ""

    yaml_str = yaml.dump(
        frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=True
    )
    return f"---\n{yaml_str}---\n"


def update_frontmatter(frontmatter: dict[str, Any], filename: str) -> dict[str, Any]:
    """Update frontmatter according to the requirements."""
    updated = frontmatter.copy()

    # 1. Add/update date field from filename
    extracted_date = extract_date_from_filename(filename)
    if extracted_date:
        updated["date"] = extracted_date

    # 2. Rename 'tag' to 'tags' if it exists
    if "tag" in updated:
        if "tags" not in updated:
            updated["tags"] = updated["tag"]
        del updated["tag"]

    # 3. Replace spaces in tags with underscores
    if "tags" in updated and isinstance(updated["tags"], list):
        updated["tags"] = clean_tags(updated["tags"])

    return updated


def process_markdown_file(file_path: Path) -> bool:
    """Process a single markdown file and update its frontmatter."""
    try:
        with file_path.open(encoding="utf-8") as f:
            content = f.read()

        frontmatter, body = parse_frontmatter(content)

        # Skip files without frontmatter
        if not frontmatter:
            print(f"Skipping {file_path} - no frontmatter found")
            return False

        original_frontmatter = frontmatter.copy()
        updated_frontmatter = update_frontmatter(frontmatter, file_path.name)

        # Check if anything changed
        if original_frontmatter == updated_frontmatter:
            print(f"No changes needed for {file_path}")
            return False

        # Write back the updated content
        new_content = serialize_frontmatter(updated_frontmatter) + body

        with file_path.open("w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Updated {file_path}")

        # Show what changed
        if "date" in updated_frontmatter and updated_frontmatter[
            "date"
        ] != original_frontmatter.get("date"):
            print(f"  - Updated date: {updated_frontmatter['date']}")

        if "tag" in original_frontmatter:
            print(f"  - Renamed 'tag' to 'tags'")

        if "tags" in updated_frontmatter and "tags" in original_frontmatter:
            if updated_frontmatter["tags"] != original_frontmatter["tags"]:
                print(
                    f"  - Updated tags: {original_frontmatter['tags']} -> {updated_frontmatter['tags']}"
                )

        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to process all markdown files in 2022/ and 2023/ folders."""
    script_dir = Path(__file__).parent
    folders_to_process = ["2022", "2023"]

    total_files = 0
    updated_files = 0

    for folder in folders_to_process:
        folder_path = script_dir / folder

        if not folder_path.exists():
            print(f"Folder {folder_path} does not exist, skipping...")
            continue

        print(f"\nProcessing folder: {folder_path}")

        # Find all markdown files recursively
        for md_file in folder_path.rglob("*.md"):
            total_files += 1
            if process_markdown_file(md_file):
                updated_files += 1

    print(f"\n--- Summary ---")
    print(f"Total files processed: {total_files}")
    print(f"Files updated: {updated_files}")
    print(f"Files unchanged: {total_files - updated_files}")


if __name__ == "__main__":
    main()
