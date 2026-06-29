"""Tests for README validation order coverage."""

from __future__ import annotations

from pathlib import Path

REQUIRED_VALIDATION_SECTION_TOKENS = (
    "## Validation order",
    "Default validation now runs through `CI - Python Full Validation`",
    "Manual fallback validation:",
)

REQUIRED_VALIDATION_WORKFLOWS = (
    "CI - Python Quality Gate",
    "CI - Python Full Validation",
    "Manual - Python Debug",
    "Manual - Python Run Script",
    "Manual - Python Inspect Artifacts",
    "Manual - Python Validate Registry",
)

REQUIRED_VALIDATION_INPUTS = (
    "target_environment=development",
    "diagnostic_level=repository",
    "script_name=repository_health_report",
    "script_name=control_plane_readiness",
    "run_mode=read_only",
    "inspection_mode=sample",
)


def readme_text() -> str:
    return (Path.cwd() / "README.md").read_text(encoding="utf-8")


def test_readme_preserves_validation_order_section() -> None:
    readme = readme_text()
    missing = [token for token in REQUIRED_VALIDATION_SECTION_TOKENS if token not in readme]

    assert missing == []


def test_readme_indexes_validation_workflows() -> None:
    readme = readme_text()
    missing = [
        workflow_name
        for workflow_name in REQUIRED_VALIDATION_WORKFLOWS
        if f"`{workflow_name}`" not in readme
    ]

    assert missing == []


def test_readme_indexes_safe_manual_validation_inputs() -> None:
    readme = readme_text()
    missing = [token for token in REQUIRED_VALIDATION_INPUTS if token not in readme]

    assert missing == []
