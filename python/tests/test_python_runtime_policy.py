"""Tests for Python runtime version policy invariants."""

from __future__ import annotations

from pathlib import Path

EXPECTED_PYTHON_VERSION = 'python-version: "3.13"'
EXPECTED_CACHE_SETTING = 'cache: "pip"'
EXPECTED_CACHE_DEPENDENCY_PATHS = (
    "python/requirements.txt",
    "python/requirements-dev.txt",
)
PYTHON_WORKFLOWS = (
    ".github/workflows/ci-python-quality.yml",
    ".github/workflows/ci-python-full-validation.yml",
    ".github/workflows/manual-python-run-script.yml",
    ".github/workflows/manual-python-debug.yml",
    ".github/workflows/manual-python-inspect-artifacts.yml",
    ".github/workflows/manual-python-validate-registry.yml",
)


def read_workflow(path: str) -> str:
    return (Path.cwd() / path).read_text(encoding="utf-8")


def test_workflows_pin_expected_python_version() -> None:
    failures = []
    for workflow_path in PYTHON_WORKFLOWS:
        content = read_workflow(workflow_path)
        if EXPECTED_PYTHON_VERSION not in content:
            failures.append(f"{workflow_path}: missing Python 3.13 runtime")

    assert failures == []


def test_workflows_use_pip_cache() -> None:
    failures = []
    for workflow_path in PYTHON_WORKFLOWS:
        content = read_workflow(workflow_path)
        if EXPECTED_CACHE_SETTING not in content:
            failures.append(f"{workflow_path}: missing pip cache setting")

    assert failures == []


def test_workflows_cache_expected_dependency_files() -> None:
    failures = []
    for workflow_path in PYTHON_WORKFLOWS:
        content = read_workflow(workflow_path)
        for dependency_path in EXPECTED_CACHE_DEPENDENCY_PATHS:
            if dependency_path not in content:
                failures.append(f"{workflow_path}: missing cache path {dependency_path}")

    assert failures == []
