"""Tests for control-plane readiness helpers."""

from __future__ import annotations

from pathlib import Path

from python.scripts.control_plane_readiness import (
    REQUIRED_SCRIPTS,
    check_required_paths,
    check_required_scripts,
    check_workflow_mentions,
    classify_readiness,
)


def test_classify_readiness() -> None:
    assert classify_readiness([], "healthy") == "ready"
    assert classify_readiness([], "manual_review_required") == "manual_review_required"
    assert classify_readiness(["finding"], "healthy") == "attention_required"


def test_check_required_paths_detects_missing_file(tmp_path: Path) -> None:
    findings = check_required_paths(tmp_path, ("missing.md",), "readiness file")

    assert findings == ["Missing readiness file: missing.md"]


def test_check_required_scripts_current_allowlist() -> None:
    assert "control_plane_readiness" in REQUIRED_SCRIPTS
    assert check_required_scripts() == []


def test_check_workflow_mentions_detects_missing_workflow(tmp_path: Path) -> None:
    findings = check_workflow_mentions(
        tmp_path,
        ".github/workflows/missing.yml",
        "control_plane_readiness",
    )

    assert findings == ["Missing workflow: .github/workflows/missing.yml"]


def test_check_workflow_mentions_detects_script_choice(tmp_path: Path) -> None:
    workflow_path = tmp_path / ".github" / "workflows" / "manual.yml"
    workflow_path.parent.mkdir(parents=True)
    workflow_path.write_text("control_plane_readiness\n", encoding="utf-8")

    findings = check_workflow_mentions(
        tmp_path,
        ".github/workflows/manual.yml",
        "control_plane_readiness",
    )

    assert findings == []
