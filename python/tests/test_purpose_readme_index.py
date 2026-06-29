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


def test_readme_preserves_purpose_tokens() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")
    missing = [token for token in REQUIRED_PURPOSE_TOKENS if token not in readme]

    assert missing == []
