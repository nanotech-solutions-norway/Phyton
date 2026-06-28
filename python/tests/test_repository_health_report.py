"""Tests for repository health report script."""

from __future__ import annotations

from pathlib import Path

from python.scripts.repository_health_report import (
    build_health_report,
    check_required_paths,
    classify_health,
    find_unregistered_scripts,
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
        path.write_text("name: Example\njobs:\n  test:\n    runs-on: ubuntu-latest\n", encoding="utf-8")
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
    """Write the minimum files needed for a healthy fixture."""

    required_docs = (
        "README.md",
        "docs/PYTHON_CONTROL_PLANE.md",
        "docs/CHATGPT_PYTHON_ORCHESTRATOR_COMMANDS.md",
        "docs/PHASE2_ARTIFACT_INSPECTION_AND_FAILURE_TRIAGE.md",
        "docs/PHASE3_CONTROLLED_SCRIPT_EXPANSION.md",
        "docs/PHASE4_READ_ONLY_REPOSITORY_INTELLIGENCE.md",
        "docs/PHASE5_REPOSITORY_HEALTH_REPORT.md",
    )
    for relative_path in required_docs:
        file_path = repo_root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("placeholder\n", encoding="utf-8")

    workflow_names = (
        "ci-python-quality.yml",
        "ci-python-full-validation.yml",
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

    python_dir = repo_root / "python"
    python_dir.mkdir(exist_ok=True)
    (python_dir / "requirements.txt").write_text("\n", encoding="utf-8")
    (python_dir / "requirements-dev.txt").write_text("pytest>=8.4,<9\n", encoding="utf-8")


def test_classify_health() -> None:
    assert classify_health([], []) == "healthy"
    assert classify_health([], ["warning"]) == "manual_review_required"
    assert classify_health(["finding"], []) == "attention_required"


def test_check_required_paths_detects_missing_file(tmp_path: Path) -> None:
    findings = check_required_paths(tmp_path, ("missing.md",), "documentation file")

    assert findings == ["Missing documentation file: missing.md"]


def test_find_unregistered_scripts(tmp_path: Path) -> None:
    write_registered_script_files(tmp_path)
    extra_script = tmp_path / "python" / "scripts" / "extra.py"
    extra_script.write_text("pass\n", encoding="utf-8")

    assert find_unregistered_scripts(tmp_path) == ["python/scripts/extra.py"]


def test_build_health_report_healthy_fixture(tmp_path: Path) -> None:
    write_registered_script_files(tmp_path)
    write_required_files(tmp_path)

    report = build_health_report(tmp_path)

    assert report["status"] == "healthy"
    assert report["findings"] == []
    assert "hello_control_plane" in report["registered_scripts"]
