"""Generate a read-only inventory of GitHub Actions workflows."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_NAME = "workflow_inventory"


def enforce_development_environment() -> None:
    """Enforce development-only execution."""

    target_environment = os.environ.get(
        "PYTHON_CONTROL_PLANE_TARGET_ENVIRONMENT",
        "development",
    )
    if target_environment != "development":
        raise RuntimeError("Phase 4 inventory scripts are development-only.")


def read_workflow_name(lines: list[str], fallback: str) -> str:
    """Read workflow name from YAML text without external dependencies."""

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("name:"):
            value = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            return value or fallback
    return fallback


def count_top_level_jobs(lines: list[str]) -> int:
    """Count direct job identifiers under the jobs block."""

    in_jobs = False
    job_count = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        leading_spaces = len(line) - len(line.lstrip(" "))
        if stripped == "jobs:":
            in_jobs = True
            continue

        if in_jobs and leading_spaces == 0 and stripped.endswith(":"):
            break

        if in_jobs and leading_spaces == 2 and stripped.endswith(":"):
            job_count += 1

    return job_count


def infer_triggers(lines: list[str]) -> list[str]:
    """Infer common workflow triggers from YAML text."""

    triggers = []
    trigger_names = ["push", "pull_request", "workflow_dispatch", "schedule"]
    for trigger in trigger_names:
        if any(line.strip().startswith(f"{trigger}:") for line in lines):
            triggers.append(trigger)
    return triggers


def inspect_workflow(path: Path, repo_root: Path) -> dict[str, Any]:
    """Inspect one workflow file."""

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    relative_path = path.relative_to(repo_root)

    return {
        "path": str(relative_path),
        "name": read_workflow_name(lines, path.stem),
        "job_count": count_top_level_jobs(lines),
        "triggers": infer_triggers(lines),
        "line_count": len(lines),
    }


def collect_workflow_inventory(repo_root: Path) -> dict[str, Any]:
    """Collect workflow inventory data."""

    workflows_dir = repo_root / ".github" / "workflows"
    workflows = []
    if workflows_dir.is_dir():
        for path in sorted(workflows_dir.glob("*.yml")):
            workflows.append(inspect_workflow(path, repo_root))

    return {
        "status": "success",
        "script": SCRIPT_NAME,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "workflow_count": len(workflows),
        "workflows": workflows,
        "production_writes": "out_of_scope",
        "staging_writes": "out_of_scope",
        "external_writes": "out_of_scope",
    }


def write_markdown_report(output_path: Path, inventory: dict[str, Any]) -> None:
    """Write a Markdown workflow inventory report."""

    lines = [
        "# Workflow Inventory Report",
        "",
        f"Generated UTC: {inventory['created_at_utc']}",
        f"Status: {inventory['status']}",
        f"Workflows: {inventory['workflow_count']}",
        "",
        "| Workflow | Path | Jobs | Triggers |",
        "|---|---|---:|---|",
    ]

    workflows = inventory["workflows"]
    for workflow in workflows:
        triggers = ", ".join(workflow["triggers"]) or "none detected"
        lines.append(
            "| "
            f"{workflow['name']} | "
            f"`{workflow['path']}` | "
            f"{workflow['job_count']} | "
            f"{triggers} |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Collect workflow inventory and write JSON/Markdown artifacts."""

    enforce_development_environment()
    repo_root = Path.cwd().resolve()
    output_dir = Path(
        os.environ.get("PYTHON_CONTROL_PLANE_OUTPUT_DIR", "artifacts/python-run")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    inventory = collect_workflow_inventory(repo_root)
    (output_dir / "workflow-inventory.json").write_text(
        json.dumps(inventory, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown_report(output_dir / "workflow-inventory.md", inventory)

    print("workflow_inventory completed in development mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
