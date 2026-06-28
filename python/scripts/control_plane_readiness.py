"""Generate a read-only Python control-plane readiness report."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from python.scripts.repository_health_report import build_health_report
from python.tools.script_allowlist import SCRIPT_ALLOWLIST

SCRIPT_NAME = "control_plane_readiness"
REQUIRED_DOCS = (
    "README.md",
    "docs/PYTHON_CONTROL_PLANE.md",
    "docs/CHATGPT_PYTHON_ORCHESTRATOR_COMMANDS.md",
    "docs/PHASE6_CONTROL_PLANE_READINESS.md",
)
REQUIRED_SCRIPTS = (
    "hello_control_plane",
    "repository_inventory",
    "workflow_inventory",
    "dependency_inventory",
    "repository_health_report",
    "control_plane_readiness",
)
MANUAL_RUN_WORKFLOW = ".github/workflows/manual-python-run-script.yml"


def enforce_development_environment() -> None:
    """Enforce development-only execution."""

    target_environment = os.environ.get(
        "PYTHON_CONTROL_PLANE_TARGET_ENVIRONMENT",
        "development",
    )
    if target_environment != "development":
        raise RuntimeError("Phase 6 readiness reports are development-only.")


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


def check_required_scripts() -> list[str]:
    """Return findings for missing required script registrations."""

    findings = []
    for script_name in REQUIRED_SCRIPTS:
        if script_name not in SCRIPT_ALLOWLIST:
            findings.append(f"Missing registered script: {script_name}")
    return findings


def check_workflow_mentions(
    repo_root: Path,
    workflow_path: str,
    script_name: str,
) -> list[str]:
    """Return findings if a workflow does not mention a required script."""

    path = repo_root / workflow_path
    if not path.is_file():
        return [f"Missing workflow: {workflow_path}"]

    content = path.read_text(encoding="utf-8")
    if script_name not in content:
        return [f"Workflow does not include {script_name}: {workflow_path}"]
    return []


def classify_readiness(findings: list[str], health_status: str) -> str:
    """Classify readiness state."""

    if findings:
        return "attention_required"
    if health_status != "healthy":
        return "manual_review_required"
    return "ready"


def build_readiness_report(repo_root: Path) -> dict[str, Any]:
    """Build the readiness report."""

    health_report = build_health_report(repo_root)
    findings = []
    findings.extend(
        check_required_paths(repo_root, REQUIRED_DOCS, "readiness file")
    )
    findings.extend(check_required_scripts())
    findings.extend(
        check_workflow_mentions(repo_root, MANUAL_RUN_WORKFLOW, SCRIPT_NAME)
    )

    status = classify_readiness(findings, str(health_report["status"]))

    return {
        "status": status,
        "script": SCRIPT_NAME,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "findings": findings,
        "health_status": health_report["status"],
        "registered_scripts": sorted(SCRIPT_ALLOWLIST),
        "required_scripts": list(REQUIRED_SCRIPTS),
        "scope": "development-only read-only control plane",
        "production_writes": "out_of_scope",
        "staging_writes": "out_of_scope",
        "external_writes": "out_of_scope",
    }


def write_markdown_report(output_path: Path, report: dict[str, Any]) -> None:
    """Write a Markdown readiness report."""

    lines = [
        "# Python Control Plane Readiness Report",
        "",
        f"Generated UTC: {report['created_at_utc']}",
        f"Status: {report['status']}",
        f"Health status: {report['health_status']}",
        f"Scope: {report['scope']}",
        "",
        "## Findings",
        "",
    ]

    if report["findings"]:
        lines.extend(f"- {finding}" for finding in report["findings"])
    else:
        lines.append("- None")

    lines.extend(["", "## Required scripts", ""])
    lines.extend(f"- `{script}`" for script in report["required_scripts"])

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Build readiness report and write JSON/Markdown artifacts."""

    enforce_development_environment()
    repo_root = Path.cwd().resolve()
    output_dir = Path(
        os.environ.get("PYTHON_CONTROL_PLANE_OUTPUT_DIR", "artifacts/python-run")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_readiness_report(repo_root)
    (output_dir / "control-plane-readiness.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown_report(output_dir / "control-plane-readiness.md", report)

    print(f"control_plane_readiness completed with status: {report['status']}")
    return 0 if report["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
