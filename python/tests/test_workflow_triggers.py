"""Tests for GitHub Actions workflow trigger invariants."""

from __future__ import annotations

from pathlib import Path

CI_TRIGGER_PATHS = (
    '      - "python/**"',
    '      - ".github/workflows/*.yml"',
    '      - "docs/**"',
    '      - "README.md"',
)

CI_WORKFLOWS = (
    ".github/workflows/ci-python-quality.yml",
    ".github/workflows/ci-python-full-validation.yml",
)

MANUAL_WORKFLOWS = (
    ".github/workflows/manual-python-run-script.yml",
    ".github/workflows/manual-python-debug.yml",
    ".github/workflows/manual-python-inspect-artifacts.yml",
    ".github/workflows/manual-python-validate-registry.yml",
)


def read_workflow(path: str) -> str:
    return (Path.cwd() / path).read_text(encoding="utf-8")


def test_ci_workflows_cover_core_paths() -> None:
    failures = []
    for workflow_path in CI_WORKFLOWS:
        content = read_workflow(workflow_path)
        for trigger_path in CI_TRIGGER_PATHS:
            if trigger_path not in content:
                failures.append(f"{workflow_path}: missing trigger path {trigger_path}")

    assert failures == []


def test_quality_gate_runs_on_pull_request() -> None:
    content = read_workflow(".github/workflows/ci-python-quality.yml")

    assert "pull_request:" in content
    assert "branches: [ main ]" in content


def test_validation_workflows_allow_manual_dispatch() -> None:
    failures = []
    for workflow_path in (*CI_WORKFLOWS, *MANUAL_WORKFLOWS):
        content = read_workflow(workflow_path)
        if "workflow_dispatch:" not in content:
            failures.append(f"{workflow_path}: missing workflow_dispatch")

    assert failures == []


def test_ci_workflows_run_on_main_push() -> None:
    failures = []
    for workflow_path in CI_WORKFLOWS:
        content = read_workflow(workflow_path)
        if "push:" not in content:
            failures.append(f"{workflow_path}: missing push trigger")
        if "branches: [ main ]" not in content:
            failures.append(f"{workflow_path}: missing main branch trigger")

    assert failures == []
