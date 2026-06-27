"""Generate a read-only inventory of repository files."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_NAME = "repository_inventory"
EXCLUDED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "artifacts",
    "TestResults",
}


def enforce_development_environment() -> None:
    """Enforce development-only execution."""

    target_environment = os.environ.get(
        "PYTHON_CONTROL_PLANE_TARGET_ENVIRONMENT",
        "development",
    )
    if target_environment != "development":
        raise RuntimeError("Phase 4 inventory scripts are development-only.")


def should_skip(path: Path) -> bool:
    """Return whether a path should be skipped during inventory."""

    return any(part in EXCLUDED_DIRECTORIES for part in path.parts)


def collect_repository_inventory(repo_root: Path) -> dict[str, Any]:
    """Collect repository file counts and size summaries."""

    files: list[dict[str, Any]] = []
    extension_counts: dict[str, int] = {}
    top_level_counts: dict[str, int] = {}
    total_bytes = 0

    for path in sorted(repo_root.rglob("*")):
        relative_path = path.relative_to(repo_root)
        if should_skip(relative_path) or not path.is_file():
            continue

        size_bytes = path.stat().st_size
        suffix = path.suffix.lower() or "[no extension]"
        top_level = relative_path.parts[0] if relative_path.parts else "."

        files.append(
            {
                "path": str(relative_path),
                "size_bytes": size_bytes,
                "suffix": suffix,
                "top_level": top_level,
            }
        )
        extension_counts[suffix] = extension_counts.get(suffix, 0) + 1
        top_level_counts[top_level] = top_level_counts.get(top_level, 0) + 1
        total_bytes += size_bytes

    return {
        "status": "success",
        "script": SCRIPT_NAME,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo_root),
        "file_count": len(files),
        "total_bytes": total_bytes,
        "extension_counts": dict(sorted(extension_counts.items())),
        "top_level_counts": dict(sorted(top_level_counts.items())),
        "files": files,
        "production_writes": "out_of_scope",
        "staging_writes": "out_of_scope",
        "external_writes": "out_of_scope",
    }


def write_markdown_report(output_path: Path, inventory: dict[str, Any]) -> None:
    """Write a Markdown repository inventory report."""

    lines = [
        "# Repository Inventory Report",
        "",
        f"Generated UTC: {inventory['created_at_utc']}",
        f"Status: {inventory['status']}",
        f"Files: {inventory['file_count']}",
        f"Total bytes: {inventory['total_bytes']}",
        "",
        "## Top-level counts",
        "",
    ]

    top_level_counts = inventory["top_level_counts"]
    for key, value in top_level_counts.items():
        lines.append(f"- `{key}`: {value}")

    lines.extend(["", "## Extension counts", ""])
    extension_counts = inventory["extension_counts"]
    for key, value in extension_counts.items():
        lines.append(f"- `{key}`: {value}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Collect inventory and write JSON/Markdown artifacts."""

    enforce_development_environment()
    repo_root = Path.cwd().resolve()
    output_dir = Path(
        os.environ.get("PYTHON_CONTROL_PLANE_OUTPUT_DIR", "artifacts/python-run")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    inventory = collect_repository_inventory(repo_root)
    (output_dir / "repository-inventory.json").write_text(
        json.dumps(inventory, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown_report(output_dir / "repository-inventory.md", inventory)

    print("repository_inventory completed in development mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
