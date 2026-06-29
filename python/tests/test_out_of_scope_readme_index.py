"""Tests for README out-of-scope coverage."""

from __future__ import annotations

from pathlib import Path

REQUIRED_OUT_OF_SCOPE_TOKENS = (
    "## Out of scope",
    "- Production writes.",
    "- Staging writes.",
    "- External system writes.",
    "- Secrets-consuming Python scripts.",
    "- Arbitrary command execution.",
    "- Deployment workflows.",
    "- Modifying project data outside this repository.",
)


def readme_text() -> str:
    return (Path.cwd() / "README.md").read_text(encoding="utf-8")


def out_of_scope_section(readme: str) -> str:
    start = readme.index("## Out of scope")
    return readme[start:]


def test_readme_preserves_out_of_scope_tokens() -> None:
    readme = readme_text()
    missing = [token for token in REQUIRED_OUT_OF_SCOPE_TOKENS if token not in readme]

    assert missing == []


def test_readme_out_of_scope_row_count_matches_required_tokens() -> None:
    section = out_of_scope_section(readme_text())
    rows = [line for line in section.splitlines() if line.startswith("- ")]

    assert len(rows) == len(REQUIRED_OUT_OF_SCOPE_TOKENS) - 1
