"""Minimal development-only Python control-plane script."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def build_payload() -> dict[str, str]:
    """Build a small execution payload."""

    target_environment = os.environ.get(
        "PYTHON_CONTROL_PLANE_TARGET_ENVIRONMENT",
        "development",
    )

    if target_environment != "development":
        raise RuntimeError("Foundation phase only permits development execution.")

    return {
        "status": "success",
        "script": "hello_control_plane",
        "target_environment": target_environment,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "execution_model": "GitHub Actions with ChatGPT orchestration",
        "production_writes": "out_of_scope",
    }


def write_markdown_report(output_path: Path, payload: dict[str, str]) -> None:
    """Write a Markdown hello-control-plane report."""

    lines = [
        "# Hello Control Plane Report",
        "",
        f"Generated UTC: {payload['created_at_utc']}",
        f"Status: {payload['status']}",
        f"Script: {payload['script']}",
        f"Target environment: {payload['target_environment']}",
        f"Execution model: {payload['execution_model']}",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Write JSON and Markdown output artifacts."""

    output_dir = Path(
        os.environ.get("PYTHON_CONTROL_PLANE_OUTPUT_DIR", "artifacts/python-run")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = build_payload()
    output_path = output_dir / "hello-control-plane-output.json"
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown_report(output_dir / "hello-control-plane-output.md", payload)

    print("hello_control_plane completed in development mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
