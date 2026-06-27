"""Tests for Python script registry synchronization."""

from __future__ import annotations

import json
from pathlib import Path

from python.tools.script_allowlist import SCRIPT_ALLOWLIST
from python.tools.validate_script_registry import (
    extract_workflow_script_options,
    validate_registry,
    write_report_files,
)


def write_manual_workflow(path: Path, script_options: list[str]) -> None:
    """Write a minimal manual workflow for registry tests."""

    options = "\n".join(f"          - {script}" for script in script_options)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""name: Manual - Python Run Script

on:
  workflow_dispatch:
    inputs:
      script_name:
        description: "Registered Python script to run"
        required: true
        type: choice
        default: hello_control_plane
        options:
{options}
      target_environment:
        description: "Target environment"
        required: true
        type: choice
        default: development
        options:
          - development
""",
        encoding="utf-8",
    )


def write_registered_script_files(repo_root: Path) -> None:
    """Write placeholder script files for the current allowlist."""

    for relative_path in SCRIPT_ALLOWLIST.values():
        script_path = repo_root / relative_path
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text("print('placeholder')\n", encoding="utf-8")


def test_current_repository_registry_is_synchronized() -> None:
    report = validate_registry(Path.cwd())

    assert report.status == "success"
    assert report.errors == ()
    assert report.default_script == "hello_control_plane"


def test_extract_workflow_script_options(tmp_path: Path) -> None:
    workflow_path = tmp_path / "manual-python-run-script.yml"
    write_manual_workflow(workflow_path, ["hello_control_plane"])

    options = extract_workflow_script_options(workflow_path)

    assert options.default_script == "hello_control_plane"
    assert options.script_options == ("hello_control_plane",)


def test_validate_registry_detects_workflow_mismatch(tmp_path: Path) -> None:
    write_registered_script_files(tmp_path)
    write_manual_workflow(
        tmp_path / ".github" / "workflows" / "manual-python-run-script.yml",
        ["different_script"],
    )

    report = validate_registry(tmp_path)

    assert report.status == "failed"
    expected_error = "Workflow script_name options must match SCRIPT_ALLOWLIST exactly."
    assert expected_error in report.errors


def test_write_report_files(tmp_path: Path) -> None:
    write_registered_script_files(tmp_path)
    write_manual_workflow(
        tmp_path / ".github" / "workflows" / "manual-python-run-script.yml",
        list(SCRIPT_ALLOWLIST),
    )
    output_dir = tmp_path / "artifacts"
    report = validate_registry(tmp_path)

    write_report_files(report, output_dir)

    payload = json.loads(
        (output_dir / "registry-validation-report.json").read_text(encoding="utf-8")
    )
    assert payload["status"] == "success"
    assert (output_dir / "registry-validation-report.md").is_file()
