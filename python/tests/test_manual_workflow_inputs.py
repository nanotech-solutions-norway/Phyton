"""Tests for manual workflow input policy invariants."""

from __future__ import annotations

from pathlib import Path

MANUAL_WORKFLOWS = (
    ".github/workflows/manual-python-run-script.yml",
    ".github/workflows/manual-python-debug.yml",
    ".github/workflows/manual-python-inspect-artifacts.yml",
    ".github/workflows/manual-python-validate-registry.yml",
)

FORBIDDEN_MANUAL_INPUT_TOKENS = (
    "type: string",
    "type: boolean",
    "default: production",
    "default: staging",
    "- production",
    "- staging",
    "- write",
    "- live",
)


def read_workflow(path: str) -> str:
    return (Path.cwd() / path).read_text(encoding="utf-8")


def test_manual_workflows_use_choice_inputs() -> None:
    failures = []
    for workflow_path in MANUAL_WORKFLOWS:
        content = read_workflow(workflow_path)
        if "workflow_dispatch:" not in content:
            failures.append(f"{workflow_path}: missing workflow dispatch")
        if "inputs:" not in content:
            failures.append(f"{workflow_path}: missing inputs block")
        if "type: choice" not in content:
            failures.append(f"{workflow_path}: missing choice input type")

    assert failures == []


def test_manual_workflows_keep_development_environment() -> None:
    failures = []
    for workflow_path in MANUAL_WORKFLOWS:
        content = read_workflow(workflow_path)
        if "target_environment:" not in content:
            failures.append(f"{workflow_path}: missing target_environment input")
        if "default: development" not in content:
            failures.append(f"{workflow_path}: missing development default")
        if "- development" not in content:
            failures.append(f"{workflow_path}: missing development option")

    assert failures == []


def test_manual_workflows_do_not_expose_unsafe_input_values() -> None:
    failures = []
    for workflow_path in MANUAL_WORKFLOWS:
        content = read_workflow(workflow_path)
        for token in FORBIDDEN_MANUAL_INPUT_TOKENS:
            if token in content:
                failures.append(f"{workflow_path}: contains forbidden token {token}")

    assert failures == []


def test_manual_run_script_remains_read_only() -> None:
    content = read_workflow(".github/workflows/manual-python-run-script.yml")

    assert "run_mode:" in content
    assert "default: read_only" in content
    assert "- read_only" in content
