"""Run one registered Python script from the control-plane allowlist."""

from __future__ import annotations

import argparse
import json
import os
import runpy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from python.tools.script_allowlist import ScriptSelectionError, resolve_allowed_script


def utc_now() -> str:
    """Return the current UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Run a registered Python script.")
    parser.add_argument("--script", required=True, help="Registered script key.")
    parser.add_argument(
        "--target-environment",
        required=True,
        choices=("development",),
        help="Foundation phase only permits development execution.",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts/python-run",
        help="Directory for execution artifacts.",
    )
    return parser.parse_args()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write a JSON artifact."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    """Run the selected script and write a controlled execution summary."""

    args = parse_args()
    repo_root = Path.cwd().resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {
        "status": "started",
        "script": args.script,
        "target_environment": args.target_environment,
        "started_at_utc": utc_now(),
        "repo": os.environ.get("GITHUB_REPOSITORY", "local-or-unknown"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "local-or-unknown"),
        "production_writes": "out_of_scope",
    }

    try:
        script_path = resolve_allowed_script(args.script, repo_root=repo_root)
        os.environ["PYTHON_CONTROL_PLANE_TARGET_ENVIRONMENT"] = args.target_environment
        os.environ["PYTHON_CONTROL_PLANE_OUTPUT_DIR"] = str(output_dir)
        os.environ["PYTHON_CONTROL_PLANE_SCRIPT"] = args.script

        try:
            runpy.run_path(str(script_path), run_name="__main__")
        except SystemExit as exc:
            if exc.code not in (0, None):
                message = f"Script exited with status {exc.code}."
                raise RuntimeError(message) from exc

        summary["status"] = "success"
        summary["completed_at_utc"] = utc_now()
        summary["script_path"] = str(script_path.relative_to(repo_root))
        write_json(output_dir / "run-summary.json", summary)
        print(f"Python script completed: {args.script}")
        return 0

    except ScriptSelectionError as exc:
        summary["status"] = "rejected"
        summary["completed_at_utc"] = utc_now()
        summary["error"] = str(exc)
        write_json(output_dir / "run-summary.json", summary)
        print(f"Python script rejected: {exc}")
        return 2

    except Exception as exc:  # noqa: BLE001 - write controlled diagnostic artifact.
        summary["status"] = "failed"
        summary["completed_at_utc"] = utc_now()
        summary["error_type"] = type(exc).__name__
        summary["error"] = str(exc)
        write_json(output_dir / "run-summary.json", summary)
        print(f"Python script failed: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
