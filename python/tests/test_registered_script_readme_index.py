"""Tests for README registered script index coverage."""

from __future__ import annotations

from pathlib import Path

from python.tools.script_allowlist import SCRIPT_ALLOWLIST


def test_readme_indexes_registered_script_keys() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")
    missing = [
        script_name
        for script_name in sorted(SCRIPT_ALLOWLIST)
        if f"`{script_name}`" not in readme
    ]

    assert missing == []


def test_readme_registered_script_table_exists() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")

    assert "## Registered scripts" in readme
    assert "| Script key | Purpose |" in readme
