"""Tests for workflow inventory script."""

from __future__ import annotations

from pathlib import Path

from python.scripts.workflow_inventory import (
    collect_workflow_inventory,
    count_top_level_jobs,
    infer_triggers,
    inspect_workflow,
    read_workflow_name,
)


def workflow_lines() -> list[str]:
    """Return a minimal workflow fixture."""

    return [
        "name: Example Workflow",
        "",
        "on:",
        "  push:",
        "  workflow_dispatch:",
        "",
        "jobs:",
        "  first-job:",
        "    runs-on: ubuntu-latest",
        "  second-job:",
        "    runs-on: ubuntu-latest",
    ]


def test_read_workflow_name() -> None:
    assert read_workflow_name(workflow_lines(), "fallback") == "Example Workflow"


def test_count_top_level_jobs() -> None:
    assert count_top_level_jobs(workflow_lines()) == 2


def test_infer_triggers() -> None:
    assert infer_triggers(workflow_lines()) == ["push", "workflow_dispatch"]


def test_inspect_workflow(tmp_path: Path) -> None:
    workflow_path = tmp_path / ".github" / "workflows" / "example.yml"
    workflow_path.parent.mkdir(parents=True)
    workflow_path.write_text("\n".join(workflow_lines()) + "\n", encoding="utf-8")

    result = inspect_workflow(workflow_path, tmp_path)

    assert result["name"] == "Example Workflow"
    assert result["job_count"] == 2
    assert result["path"] == ".github/workflows/example.yml"


def test_collect_workflow_inventory(tmp_path: Path) -> None:
    workflow_path = tmp_path / ".github" / "workflows" / "example.yml"
    workflow_path.parent.mkdir(parents=True)
    workflow_path.write_text("\n".join(workflow_lines()) + "\n", encoding="utf-8")

    inventory = collect_workflow_inventory(tmp_path)

    assert inventory["status"] == "success"
    assert inventory["workflow_count"] == 1
