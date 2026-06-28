"""Generate a consolidated read-only repository health report."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from python.scripts.dependency_inventory import collect_dependency_inventory
from python.scripts.repository_inventory import collect_repository_inventory
from python.scripts.workflow_inventory import collect_workflow_inventory
from python.tools.script_allowlist import SCRIPT_ALLOWLIST
from python.tools.validate_script_registry import validate_registry

SCRIPT_NAME = "repository_health_report"
REQUIRED_DOCS = (
    "README.md",
    "docs/PYTHON_CONTROL_PLANE.md",
    "docs/CHATGPT_PYTHON_ORCHESTRATOR_COMMANDS.md",
    "docs/PHASE2_ARTIFACT_INSPECTION_AND_FAILURE_TRIAGE.md",
    "docs/PHASE3_CONTROLLED_SCRIPT_EXPANSION.md",
    "docs/PHASE4_READ_ONLY_REPOSITORY_INTELLIGENCE.md",
    "docs/PHASE5_REPOSITORY_HEALTH_REPORT.md",
)
REQUIRED_WORKFLOWS = (
    ".github/workflows/ci-python-quality.yml",
    ".github/workflows/ci-python-full-validation.yml",
    ".github/workflows/manual-python-run-script.yml",
    ".github/workflows/manual-python-debug.yml",
    ".github/workflows/manual-python-inspect-artifacts.yml",
    ".github/workflows/manual-python-validate-registry.yml",
)


def enforce_development_environment() -> None:
    """Enforce development-only execution."""

    target_environment = os.environ.get(
        "PYTHON_CONTROL_PLANE_TARGET_ENVIRONMENT",
        "development",
    )
    if target_environment != "development":
        raise RuntimeError("Phase 5 health reports are development-only.")


def check_required_paths(
    repo_root: Path,
    paths: tuple[str, ...],
    label: str,
) -> list[str]:
    """Return findings for missing required paths."""

    findings = []
    for relative_path in paths:
        if not (repo_root / relative_path).is_file():
            findings.append(f"Missing {label}: {relative_path}")
    return findings


def find_unregistered_scripts(repo_root: Path) -> list[str]:
    """Return scripts under python/scripts that are not in SCRIPT_ALLOWLIST."""

    scripts_dir = repo_root / "python" / "scripts"
    registered_paths = set(SCRIPT_ALLOWLIST.values())
    unregistered = []
    if not scripts_dir.is_dir():
        return ["Missing scripts directory: python/scripts"]

    for script_path in sorted(scripts_dir.glob("*.py")):
        relative_path = str(script_path.relative_to(repo_root))
        if relative_path not in registered_paths:
            unregistered.append(relative_path)
    return unregistered


def classify_health(findings: list[str], warnings: list[str]) -> str:
    """Classify consolidated repository health."""

    if findings:
        return "attention_required"
    if warnings:
        return "manual_review_required"
    return "healthy"


def build_health_report(repo_root: Path) -> dict[str, Any]:
    """Build the consolidated repository health report."""

    repository_inventory = collect_repository_inventory(repo_root)
    workflow_inventory = collect_workflow_inventory(repo_root)
    dependency_inventory = collect_dependency_inventory(repo_root)
    registry_report = validate_registry(repo_root)

    findings = []
    warnings = []
    findings.extend(check_required_paths(repo_root, REQUIRED_DOCS, "documentation file"))
    findings.extend(check_required_paths(repo_root, REQUIRED_WORKFLOWS, "workflow file"))

    unregistered_scripts = find_unregistered_scripts(repo_root)
    if unregistered_scripts:
        findings.extend(
            f"Unregistered Python script: {script_path}"
            for script_path in unregistered_scripts
        )

    if registry_report.status != "success":
        findings.extend(registry_report.errors)

    if dependency_inventory["dependency_count"] == 0:
        warnings.append("No Python dependencies found in requirements files.")

    if workflow_inventory["workflow_count"] < len(REQUIRED_WORKFLOWS):
        findings.append("Workflow inventory count is lower than required workflow set.")

    status = classify_health(findings, warnings)

    return {
        "status": status,
        "script": SCRIPT_NAME,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "findings": findings,
        "warnings": warnings,
        "registered_scripts": sorted(SCRIPT_ALLOWLIST),
        "repository_summary": {
            "file_count": repository_inventory["file_count"],
            "total_bytes": repository_inventory["total_bytes"],
        },
        "workflow_summary": {
            "workflow_count": workflow_inventory["workflow_count"],
            "workflows": workflow_inventory["workflows"],
        },
        "dependency_summary": {
            "dependency_count": dependency_inventory["dependency_count"],
            "files": dependency_inventory["files"],
        },
        "registry_summary": registry_report.to_jsonable(),
        "production_writes": "out_of_scope",
        "staging_writes": "out_of_scope",
        "external_writes": "out_of_scope",
    }


def write_markdown_report(output_path: Path, report: dict[str, Any]) -> None:
    """Write a Markdown health report."""

    lines = [
        "# Repository Health Report",
        "",
        f"Generated UTC: {report['created_at_utc']}",
        f"Status: {report['status']}",
        "",
        "## Summary",
        "",
        f"- Files: {report['repository_summary']['file_count']}",
        f"- Workflows: {report['workflow_summary']['workflow_count']}",
        f"- Dependencies: {report['dependency_summary']['dependency_count']}",
        f"- Registered scripts: {len(report['registered_scripts'])}",
        "",
        "## Findings",
        "",
    ]

    if report["findings"]:
        lines.extend(f"- {finding}" for finding in report["findings"])
    else:
        lines.append("- None")

    lines.extend(["", "## Warnings", ""])
    if report["warnings"]:
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.append("- None")

    lines.extend(["", "## Registered scripts", ""])
    lines.extend(f"- `{script}`" for script in report["registered_scripts"])

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Build health report and write JSON/Markdown artifacts."""

    enforce_development_environment()
    repo_root = Path.cwd().resolve()
    output_dir = Path(
        os.environ.get("PYTHON_CONTROL_PLANE_OUTPUT_DIR", "artifacts/python-run")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_health_report(repo_root)
    (output_dir / "repository-health-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown_report(output_dir / "repository-health-report.md", report)

    print(f"repository_health_report completed with status: {report['status']}")
    return 0 if report["status"] in {"healthy", "manual_review_required"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
