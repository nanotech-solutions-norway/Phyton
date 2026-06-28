"""Tests for README documentation index invariants."""

from __future__ import annotations

from pathlib import Path

REQUIRED_INDEX_PATHS = (
    "docs/PYTHON_CONTROL_PLANE.md",
    "docs/CHATGPT_PYTHON_ORCHESTRATOR_COMMANDS.md",
    "docs/PHASE2_ARTIFACT_INSPECTION_AND_FAILURE_TRIAGE.md",
    "docs/PHASE3_CONTROLLED_SCRIPT_EXPANSION.md",
    "docs/PHASE4_READ_ONLY_REPOSITORY_INTELLIGENCE.md",
    "docs/PHASE5_REPOSITORY_HEALTH_REPORT.md",
    "docs/PHASE6_CONTROL_PLANE_READINESS.md",
    "docs/PHASE7_OPERATIONS_HANDOFF.md",
    "docs/PHASE8_VALIDATION_EVIDENCE_INDEX.md",
    "docs/PHASE9_PROJECT_INSTRUCTIONS_PACK.md",
    "docs/PHASE10_DEFERRED_CAPABILITY_ROADMAP.md",
    "python/tests/test_control_plane_readiness.py",
)


def test_readme_indexes_required_documents() -> None:
    repo_root = Path.cwd()
    readme = (repo_root / "README.md").read_text(encoding="utf-8")

    missing = [path for path in REQUIRED_INDEX_PATHS if path not in readme]

    assert missing == []


def test_indexed_documents_exist() -> None:
    repo_root = Path.cwd()
    missing = [
        path for path in REQUIRED_INDEX_PATHS if not (repo_root / path).is_file()
    ]

    assert missing == []
