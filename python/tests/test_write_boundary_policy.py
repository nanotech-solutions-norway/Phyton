"""Tests for write-boundary policy invariants."""

from __future__ import annotations

from pathlib import Path

README_REQUIRED_OUT_OF_SCOPE = (
    "- Production writes.",
    "- Staging writes.",
    "- External system writes.",
    "- Secrets-consuming Python scripts.",
    "- Arbitrary command execution.",
    "- Deployment workflows.",
    "- Modifying project data outside this repository.",
)

FORBIDDEN_WORKFLOW_BOUNDARY_TOKENS = (
    "target_environment=production",
    "target_environment=staging",
    "run_mode=write",
    "run_mode=live",
    "WRITE_TOOLS_ENABLED: true",
)

WORKFLOW_PATHS = (
    ".github/workflows/ci-python-quality.yml",
    ".github/workflows/ci-python-full-validation.yml",
    ".github/workflows/manual-python-run-script.yml",
    ".github/workflows/manual-python-debug.yml",
    ".github/workflows/manual-python-inspect-artifacts.yml",
    ".github/workflows/manual-python-validate-registry.yml",
)


def read_file(path: str) -> str:
    return (Path.cwd() / path).read_text(encoding="utf-8")


def test_readme_preserves_write_boundaries() -> None:
    readme = read_file("README.md")
    missing = [line for line in README_REQUIRED_OUT_OF_SCOPE if line not in readme]

    assert missing == []


def test_manual_runner_remains_development_read_only() -> None:
    content = read_file(".github/workflows/manual-python-run-script.yml")

    assert "default: development" in content
    assert "default: read_only" in content
    assert "- development" in content
    assert "- read_only" in content
    assert "target_environment=development" in content
    assert "run_mode=read_only" in content


def test_workflows_do_not_enable_write_or_live_modes() -> None:
    failures = []
    for workflow_path in WORKFLOW_PATHS:
        content = read_file(workflow_path)
        for token in FORBIDDEN_WORKFLOW_BOUNDARY_TOKENS:
            if token in content:
                failures.append(f"{workflow_path}: contains forbidden token {token}")

    assert failures == []
