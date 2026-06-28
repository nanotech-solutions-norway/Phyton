"""Tests for GitHub Actions artifact contract invariants."""

from __future__ import annotations

from pathlib import Path

ARTIFACT_CONTRACTS = {
    ".github/workflows/ci-python-quality.yml": (
        "name: python-quality-test-results",
        "path: TestResults/python/*.xml",
    ),
    ".github/workflows/ci-python-full-validation.yml": (
        "name: python-full-validation-artifacts",
        "TestResults/python-full-validation/**",
        "artifacts/python-full-validation/**",
    ),
    ".github/workflows/manual-python-debug.yml": (
        "name: python-debug-artifacts",
        "path: artifacts/python-debug/**",
    ),
    ".github/workflows/manual-python-run-script.yml": (
        "name: python-script-output",
        "path: artifacts/python-run/**",
    ),
    ".github/workflows/manual-python-inspect-artifacts.yml": (
        "name: python-artifact-inspection-report",
        "path: artifacts/python-inspection/**",
    ),
    ".github/workflows/manual-python-validate-registry.yml": (
        "name: python-registry-validation-report",
        "path: artifacts/python-registry-validation/**",
    ),
}


def test_workflow_artifact_contracts_are_present() -> None:
    failures = []
    for workflow_path, required_tokens in ARTIFACT_CONTRACTS.items():
        content = (Path.cwd() / workflow_path).read_text(encoding="utf-8")
        for token in required_tokens:
            if token not in content:
                failures.append(f"{workflow_path}: missing {token}")

    assert failures == []


def test_workflows_upload_artifacts_even_after_failures() -> None:
    failures = []
    for workflow_path in ARTIFACT_CONTRACTS:
        content = (Path.cwd() / workflow_path).read_text(encoding="utf-8")
        if "uses: actions/upload-artifact@v4" not in content:
            failures.append(f"{workflow_path}: missing upload-artifact step")
        if "if: always()" not in content:
            failures.append(f"{workflow_path}: artifact upload is not always-on")

    assert failures == []
