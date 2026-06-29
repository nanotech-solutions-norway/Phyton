"""Tests for README purpose coverage."""

from __future__ import annotations

from pathlib import Path

REQUIRED_PURPOSE_TOKENS = (
    "## Purpose",
    "Use GitHub Actions as the execution runtime for controlled Python operations.",
    "ChatGPT acts as orchestrator",
    "which workflow to run",
    "which artifacts to inspect",
    "which isolated patch to apply next",
)


def readme_text() -> str:
    return (Path.cwd() / "README.md").read_text(encoding="utf-8")


def purpose_section(readme: str) -> str:
    start = readme.index("## Purpose")
    end = readme.index("## Operating posture", start)
    return readme[start:end]


def test_readme_preserves_purpose_tokens() -> None:
    readme = readme_text()
    missing = [token for token in REQUIRED_PURPOSE_TOKENS if token not in readme]

    assert missing == []


def test_readme_purpose_tokens_are_in_purpose_section() -> None:
    section = purpose_section(readme_text())
    missing = [token for token in REQUIRED_PURPOSE_TOKENS if token not in section]

    assert missing == []
