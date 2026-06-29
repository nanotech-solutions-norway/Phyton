"""Tests for README phase index coverage."""

from __future__ import annotations

from pathlib import Path

REQUIRED_PHASE_INDEX_ENTRIES = (
    "python/tests/test_control_plane_readiness.py",
    "python/tests/test_documentation_index.py",
    "python/tests/test_workflow_policy.py",
    "python/tests/test_script_path_policy.py",
    "python/tests/test_artifact_contract.py",
    "python/tests/test_workflow_triggers.py",
    "python/tests/test_dependency_policy.py",
    "python/tests/test_python_runtime_policy.py",
    "python/tests/test_write_boundary_policy.py",
    "python/tests/test_manual_workflow_inputs.py",
    "python/tests/test_readme_phase_index.py",
    "python/tests/test_registered_script_readme_index.py",
)


def test_readme_indexes_phase_guardrail_tests() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")
    missing = [
        phase_entry
        for phase_entry in REQUIRED_PHASE_INDEX_ENTRIES
        if phase_entry not in readme
    ]

    assert missing == []


def test_phase_guardrail_test_files_exist() -> None:
    missing = [
        phase_entry
        for phase_entry in REQUIRED_PHASE_INDEX_ENTRIES
        if not (Path.cwd() / phase_entry).is_file()
    ]

    assert missing == []
