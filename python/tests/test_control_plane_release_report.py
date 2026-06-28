"""Tests for the control-plane release closure report."""

from __future__ import annotations

from pathlib import Path

from python.scripts.control_plane_release_report import (
    REQUIRED_REGISTERED_SCRIPTS,
    build_release_report,
    check_registered_scripts,
    check_required_paths,
    check_workflow_mentions,
    classify_release,
)
from python.tools.script_allowlist import SCRIPT_ALLOWLIST


def write_registered_script_files(repo_root: Path) -> None:
    """Write placeholder script files for the current allowlist."""

    for relative_path in SCRIPT_ALLOWLIST.values():
        script_path = repo_root / relative_path
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text("pass\n", encoding="utf-8")


def write_minimal_workflow(path: Path, script_options: list[str] | None = None) -> None:
    """Write a minimal workflow fixture."""

    path.parent.mkdir(parents=True, exist_ok=True)
    if script_options is None:
        path.write_text(
            "name: Example\njobs:\n  test:\n    runs-on: ubuntu-latest\n",
            encoding="utf-8",
        )
        return

    options = "\n".join(f"          - {script}" for script in script_options)
    path.write_text(
        "name: Manual - Python Run Script\n"
        "workflow_dispatch:\n"
        "  inputs:\n"
        "    script_name:\n"
        "      default: hello_control_plane\n"
        "      options:\n"
        f"{options}\n",
        encoding="utf-8",
    )


def write_required_files(repo_root: Path) -> None:
    """Write the minimum files needed for a release-ready fixture."""

    required_docs = (
        "README.md",
        "docs/PYTHON_CONTROL_PLANE.md",
        "docs/CHATGPT_PYTHON_ORCHESTRATOR_COMMANDS.md",
        "docs/PHASE2_ARTIFACT_INSPECTION_AND_FAILURE_TRIAGE.md",
        "docs/PHASE3_CONTROLLED_SCRIPT_EXPANSION.md",
        "docs/PHASE4_READ_ONLY_REPOSITORY_INTELLIGENCE.md",
        "docs/PHASE5_REPOSITORY_HEALTH_REPORT.md",
        "docs/PHASE6_CONTROL_PLANE_RELEASE_CLOSURE.md",
    )
    for relative_path in required_docs:
        file_path = repo_root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("placeholder\n", encoding="utf-8")

    workflow_names = (
        "ci-python-quality.yml",
        "manual-python-debug.yml",
        "manual-python-inspect-artifacts.yml",
        "manual-python-validate-registry.yml",
    )
    workflows_dir = repo_root / ".github" / "workflows"
    for workflow_name in workflow_names:
        write_minimal_workflow(workflows_dir / workflow_name)

    write_minimal_workflow(
        workflows_dir / "manual-python-run-script.yml",
        list(SCRIPT_ALLOWLIST),
    )
    full_validation = workflows_dir / "ci-python-full-validation.yml"
    full_validation.parent.mkdir(parents=True, exist_ok=True)
    full_validation.write_text(
        "name: CI - Python Full Validation\n"
        "jobs:\n"
        "  test:\n"
        "    steps:\n"
        "      - run: control_plane_release_report\n",
        encoding="utf-8",
    )

    python_dir = repo_root / "python"
    python_dir.mkdir(exist_ok=True)
    (python_dir / "requirements.txt").write_text("\n", encoding="utf-8")
    dev_requirements = python_dir / "requirements-dev.txt"
    dev_requirements.write_text("pytest>=8.4,<9\n", encoding="utf-8")


def test_classify_release() -> None:
    assert classify_release([], "healthy") == "release_ready"
    assert classify_release([], "manual_review_required") == "manual_review_required"
    assert classify_release(["finding"], "healthy") == "attention_required"


def test_check_required_paths_detects_missing_file(tmp_path: Path) -> None:
    findings = check_required_paths(tmp_path, ("missing.md",), "release file")

    assert findings == ["Missing release file: missing.md"]


def test_check_registered_scripts() -> None:
    assert check_registered_scripts() == []
    assert "control_plane_release_report" in REQUIRED_REGISTERED_SCRIPTS


def test_check_workflow_mentions(tmp_path: Path) -> None:
    workflow_path = tmp_path / ".github" / "workflows" / "example.yml"
    workflow_path.parent.mkdir(parents=True)
    workflow_path.write_text("control_plane_release_report\n", encoding="utf-8")

    findings = check_workflow_mentions(
        tmp_path,
        ".github/workflows/example.yml",
        "control_plane_release_report",
    )

    assert findings == []


def test_build_release_report_ready_fixture(tmp_path: Path) -> None:
    write_registered_script_files(tmp_path)
    write_required_files(tmp_path)

    report = build_release_report(tmp_path)

    assert report["status"] == "release_ready"
    assert report["findings"] == []
    assert "control_plane_release_report" in report["registered_scripts"]
