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


def test_readme_preserves_out_of_scope_tokens() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")
    missing = [
        token
        for token in REQUIRED_OUT_OF_SCOPE_TOKENS
        if token not in readme
    ]

    assert missing == []
