"""Generate a read-only inventory of Python dependency files."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_NAME = "dependency_inventory"
REQUIREMENT_FILES = (
    "python/requirements.txt",
    "python/requirements-dev.txt",
)


def enforce_development_environment() -> None:
    """Enforce development-only execution."""

    target_environment = os.environ.get(
        "PYTHON_CONTROL_PLANE_TARGET_ENVIRONMENT",
        "development",
    )
    if target_environment != "development":
        raise RuntimeError("Phase 4 inventory scripts are development-only.")


def parse_requirement_line(line: str) -> dict[str, str] | None:
    """Parse one requirements file line."""

    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    for separator in (">=", "<=", "==", "~=", ">", "<"):
        if separator in stripped:
            package, version_spec = stripped.split(separator, 1)
            return {
                "raw": stripped,
                "package": package.strip(),
                "operator": separator,
                "version_spec": version_spec.strip(),
            }

    return {
        "raw": stripped,
        "package": stripped,
        "operator": "",
        "version_spec": "",
    }


def inspect_requirements_file(path: Path, repo_root: Path) -> dict[str, Any]:
    """Inspect one requirements file."""

    entries = []
    if path.is_file():
        lines = path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            parsed = parse_requirement_line(line)
            if parsed is None:
                continue
            parsed["line_number"] = str(line_number)
            entries.append(parsed)
    else:
        lines = []

    return {
        "path": str(path.relative_to(repo_root)),
        "exists": path.is_file(),
        "line_count": len(lines),
        "dependency_count": len(entries),
        "dependencies": entries,
    }


def collect_dependency_inventory(repo_root: Path) -> dict[str, Any]:
    """Collect dependency inventory data."""

    files = [
        inspect_requirements_file(repo_root / relative_path, repo_root)
        for relative_path in REQUIREMENT_FILES
    ]
    dependency_count = sum(int(file_info["dependency_count"]) for file_info in files)

    return {
        "status": "success",
        "script": SCRIPT_NAME,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "dependency_count": dependency_count,
        "files": files,
        "production_writes": "out_of_scope",
        "staging_writes": "out_of_scope",
        "external_writes": "out_of_scope",
    }


def write_markdown_report(output_path: Path, inventory: dict[str, Any]) -> None:
    """Write a Markdown dependency inventory report."""

    lines = [
        "# Dependency Inventory Report",
        "",
        f"Generated UTC: {inventory['created_at_utc']}",
        f"Status: {inventory['status']}",
        f"Dependencies: {inventory['dependency_count']}",
        "",
        "| File | Package | Operator | Version spec |",
        "|---|---|---|---|",
    ]

    for file_info in inventory["files"]:
        for dependency in file_info["dependencies"]:
            lines.append(
                "| "
                f"`{file_info['path']}` | "
                f"`{dependency['package']}` | "
                f"`{dependency['operator']}` | "
                f"`{dependency['version_spec']}` |"
            )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Collect dependency inventory and write JSON/Markdown artifacts."""

    enforce_development_environment()
    repo_root = Path.cwd().resolve()
    output_dir = Path(
        os.environ.get("PYTHON_CONTROL_PLANE_OUTPUT_DIR", "artifacts/python-run")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    inventory = collect_dependency_inventory(repo_root)
    (output_dir / "dependency-inventory.json").write_text(
        json.dumps(inventory, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown_report(output_dir / "dependency-inventory.md", inventory)

    print("dependency_inventory completed in development mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
