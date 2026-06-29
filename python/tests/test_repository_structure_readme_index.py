"""Tests for README repository structure coverage."""

from __future__ import annotations

from pathlib import Path

REQUIRED_REPOSITORY_STRUCTURE_TOKENS = (
    "## Repository structure",
    "| Path | Purpose |",
    "`python/scripts/`",
    "`python/templates/`",
    "`python/tools/`",
    "`python/examples/`",
    "`python/tests/`",
    "`python/requirements.txt`",
    "`python/requirements-dev.txt`",
    "`.github/workflows/ci-python-quality.yml`",
    "`.github/workflows/ci-python-full-validation.yml`",
    "`.github/workflows/manual-python-run-script.yml`",
    "`.github/workflows/manual-python-debug.yml`",
    "`.github/workflows/manual-python-inspect-artifacts.yml`",
    "`.github/workflows/manual-python-validate-registry.yml`",
)


def test_readme_preserves_repository_structure_tokens() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")
    missing = [
        token for token in REQUIRED_REPOSITORY_STRUCTURE_TOKENS if token not in readme
    ]

    assert missing == []
