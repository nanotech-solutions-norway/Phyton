"""Generate a read-only inventory of repository documentation files."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_NAME = "documentation_inventory"
DOCUMENTATION_DIRECTORY = "docs"


def enforce_development_environment() -> None:
    """Enforce development-only execution."""

    target_environment = os.environ.get(
        "PYTHON_CONTROL_PLANE_TARGET_ENVIRONMENT",
        "development",
    )
    if target_environment != "development":
        raise RuntimeError("Documentation inventory is development-only.")


def inspect_markdown_file(path: Path, repo_root: Path) -> dict[str, Any]:
    """Inspect one Markdown documentation file."""

    lines = path.read_text(encoding="utf-8").splitlines()
    headings = [line.strip() for line in lines if line.startswith("#")]

    return {
        "path": path.relative_to(repo_root).as_posix(),
        "line_count": len(lines),
        "heading_count": len(headings),
        "first_heading": headings[0] if headings else "",
    }


def collect_documentation_inventory(repo_root: Path) -> dict[str, Any]:
    """Collect documentation inventory data."""

    docs_dir = repo_root / DOCUMENTATION_DIRECTORY
    files = []
    if docs_dir.is_dir():
        files = [
            inspect_markdown_file(path, repo_root)
            for path in sorted(docs_dir.glob("*.md"))
            if path.is_file()
        ]

    phase_documents = [
        file_info for file_info in files if file_info["path"].startswith("docs/PHASE")
    ]

    return {
        "status": "success",
        "script": SCRIPT_NAME,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "documentation_directory": DOCUMENTATION_DIRECTORY,
        "documentation_file_count": len(files),
        "phase_document_count": len(phase_documents),
        "files": files,
        "production_writes": "out_of_scope",
        "staging_writes": "out_of_scope",
        "external_writes": "out_of_scope",
    }


def write_markdown_report(output_path: Path, inventory: dict[str, Any]) -> None:
    """Write a Markdown documentation inventory report."""

    lines = [
        "# Documentation Inventory Report",
        "",
        f"Generated UTC: {inventory['created_at_utc']}",
        f"Status: {inventory['status']}",
        f"Documentation files: {inventory['documentation_file_count']}",
        f"Phase documents: {inventory['phase_document_count']}",
        "",
        "| File | Lines | Headings | First heading |",
        "|---|---:|---:|---|",
    ]

    for file_info in inventory["files"]:
        lines.append(
            "| "
            f"`{file_info['path']}` | "
            f"{file_info['line_count']} | "
            f"{file_info['heading_count']} | "
            f"{file_info['first_heading']} |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Collect documentation inventory and write JSON/Markdown artifacts."""

    enforce_development_environment()
    repo_root = Path.cwd().resolve()
    output_dir = Path(
        os.environ.get("PYTHON_CONTROL_PLANE_OUTPUT_DIR", "artifacts/python-run")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    inventory = collect_documentation_inventory(repo_root)
    (output_dir / "documentation-inventory.json").write_text(
        json.dumps(inventory, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown_report(output_dir / "documentation-inventory.md", inventory)

    print("documentation_inventory completed in development mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
