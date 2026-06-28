"""Tests for dependency file policy invariants."""

from __future__ import annotations

from pathlib import Path

REQUIRED_DEV_DEPENDENCIES = ("pytest", "ruff", "mypy")
REQUIREMENT_FILES = (
    "python/requirements.txt",
    "python/requirements-dev.txt",
)
WORKFLOWS_REFERENCING_REQUIREMENTS = (
    ".github/workflows/ci-python-quality.yml",
    ".github/workflows/ci-python-full-validation.yml",
    ".github/workflows/manual-python-run-script.yml",
    ".github/workflows/manual-python-debug.yml",
    ".github/workflows/manual-python-inspect-artifacts.yml",
    ".github/workflows/manual-python-validate-registry.yml",
)


def read_lines(path: str) -> list[str]:
    return (Path.cwd() / path).read_text(encoding="utf-8").splitlines()


def requirement_entries(path: str) -> list[str]:
    lines = read_lines(path)
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def test_requirement_files_exist() -> None:
    missing = [path for path in REQUIREMENT_FILES if not (Path.cwd() / path).is_file()]

    assert missing == []


def test_runtime_requirements_remain_standard_library_only() -> None:
    assert requirement_entries("python/requirements.txt") == []


def test_development_requirements_include_validation_tools() -> None:
    entries = requirement_entries("python/requirements-dev.txt")
    missing = [
        dependency
        for dependency in REQUIRED_DEV_DEPENDENCIES
        if not any(entry.startswith(dependency) for entry in entries)
    ]

    assert missing == []


def test_workflows_reference_dependency_files() -> None:
    failures = []
    for workflow_path in WORKFLOWS_REFERENCING_REQUIREMENTS:
        content = (Path.cwd() / workflow_path).read_text(encoding="utf-8")
        if "python/requirements.txt" not in content:
            failures.append(f"{workflow_path}: missing runtime requirements reference")

    assert failures == []
