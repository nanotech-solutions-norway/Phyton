"""Tests for README workflows section coverage."""

from __future__ import annotations

from pathlib import Path


def workflows_section(readme: str) -> str:
    start = readme.index("## Workflows")
    end = readme.index("## Registered scripts", start)
    return readme[start:end]


def test_readme_preserves_workflows_section_table() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")
    section = workflows_section(readme)

    assert "| Workflow | Purpose |" in section
    assert "|---|---|" in section


def test_readme_preserves_workflows_section_row_count() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")
    section = workflows_section(readme)
    rows = [line for line in section.splitlines() if line.startswith("| `")]

    assert len(rows) == 6
