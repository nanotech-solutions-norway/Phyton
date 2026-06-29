"""Tests for README registered script index coverage."""

from __future__ import annotations

from pathlib import Path

from python.tools.script_allowlist import SCRIPT_ALLOWLIST


def readme_text() -> str:
    return (Path.cwd() / "README.md").read_text(encoding="utf-8")


def registered_scripts_section(readme: str) -> str:
    start = readme.index("## Registered scripts")
    end = readme.index("## Validation order", start)
    return readme[start:end]


def test_readme_indexes_registered_script_keys() -> None:
    readme = readme_text()
    missing = [
        script_name
        for script_name in sorted(SCRIPT_ALLOWLIST)
        if f"`{script_name}`" not in readme
    ]

    assert missing == []


def test_readme_registered_script_table_exists() -> None:
    readme = readme_text()

    assert "## Registered scripts" in readme
    assert "| Script key | Purpose |" in readme


def test_readme_registered_script_row_count_matches_allowlist() -> None:
    section = registered_scripts_section(readme_text())
    rows = [line for line in section.splitlines() if line.startswith("| `")]

    assert len(rows) == len(SCRIPT_ALLOWLIST)
