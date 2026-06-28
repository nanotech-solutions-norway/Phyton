"""Tests for GitHub Actions workflow policy invariants."""

from __future__ import annotations

from pathlib import Path

WORKFLOW_PATHS = (
    ".github/workflows/ci-python-quality.yml",
    ".github/workflows/ci-python-full-validation.yml",
    ".github/workflows/manual-python-run-script.yml",
    ".github/workflows/manual-python-debug.yml",
    ".github/workflows/manual-python-inspect-artifacts.yml",
    ".github/workflows/manual-python-validate-registry.yml",
)

FORBIDDEN_WORKFLOW_TOKENS = (
    "contents: write",
    "actions: write",
    "packages: write",
    "id-token: write",
    "permissions: write-all",
)

MANUAL_RUN_REQUIRED_OPTIONS = (
    "hello_control_plane",
    "repository_inventory",
    "workflow_inventory",
    "dependency_inventory",
    "repository_health_report",
    "control_plane_readiness",
)


def read_workflow(relative_path: str) -> str:
    return (Path.cwd() / relative_path).read_text(encoding="utf-8")


def test_expected_workflows_exist() -> None:
    missing = [path for path in WORKFLOW_PATHS if not (Path.cwd() / path).is_file()]

    assert missing == []


def test_workflows_use_read_only_permissions() -> None:
    failures = []
    for path in WORKFLOW_PATHS:
        content = read_workflow(path)
        if "permissions:" not in content:
            failures.append(f"{path}: missing permissions block")
        if "contents: read" not in content:
            failures.append(f"{path}: missing contents read permission")
        if "actions: read" not in content:
            failures.append(f"{path}: missing actions read permission")

    assert failures == []


def test_workflows_do_not_request_write_permissions() -> None:
    failures = []
    for path in WORKFLOW_PATHS:
        content = read_workflow(path)
        for token in FORBIDDEN_WORKFLOW_TOKENS:
            if token in content:
                failures.append(f"{path}: contains forbidden token {token}")

    assert failures == []


def test_manual_runner_keeps_fixed_safe_inputs() -> None:
    content = read_workflow(".github/workflows/manual-python-run-script.yml")

    for script_name in MANUAL_RUN_REQUIRED_OPTIONS:
        assert f"- {script_name}" in content

    assert "default: development" in content
    assert "default: read_only" in content
    assert "- development" in content
    assert "- read_only" in content
    assert "target_environment" in content
    assert "run_mode" in content


def test_workflows_do_not_expose_free_form_commands() -> None:
    failures = []
    for path in WORKFLOW_PATHS:
        content = read_workflow(path)
        if "command:" in content:
            failures.append(f"{path}: exposes command input")
        if "shell_command" in content:
            failures.append(f"{path}: exposes shell command input")

    assert failures == []
