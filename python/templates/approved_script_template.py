"""Template for future registered Python control-plane scripts.

Copy this file into python/scripts/ and rename it when adding a new registered
script. Do not execute this template directly through GitHub Actions.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "replace_with_registered_script_name"


def build_payload() -> dict[str, str]:
    """Build the script output payload."""

    target_environment = os.environ.get(
        "PYTHON_CONTROL_PLANE_TARGET_ENVIRONMENT",
        "development",
    )

    if target_environment != "development":
        raise RuntimeError(
            "Registered scripts must remain development-only by default."
        )

    return {
        "status": "success",
        "script": SCRIPT_NAME,
        "target_environment": target_environment,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "production_writes": "out_of_scope",
        "staging_writes": "out_of_scope",
        "external_writes": "out_of_scope",
    }


def main() -> int:
    """Write a JSON output artifact for the registered script."""

    output_dir = Path(
        os.environ.get("PYTHON_CONTROL_PLANE_OUTPUT_DIR", "artifacts/python-run")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{SCRIPT_NAME}-output.json"
    output_path.write_text(
        json.dumps(build_payload(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(f"{SCRIPT_NAME} completed in development mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
