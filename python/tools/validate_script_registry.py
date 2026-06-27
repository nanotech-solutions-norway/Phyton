"""Validate Python script registry and workflow dispatch choices."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from python.tools.script_allowlist import SCRIPT_ALLOWLIST


@dataclass(frozen=True)
class WorkflowScriptOptions:
    """Script-related workflow_dispatch options."""

    default_script: str
    script_options: tuple[str, ...]


@dataclass(frozen=True)
class RegistryValidationReport:
    """Structured registry validation result."""

    status: str
    allowlist_scripts: tuple[str, ...]
    workflow_scripts: tuple[str, ...]
    default_script: str
    errors: tuple[str, ...]
    created_at_utc: str

    def to_jsonable(self) -> dict[str, Any]:
        """Return a JSON-safe report dictionary."""

        payload = asdict(self)
        payload["allowlist_scripts"] = list(self.allowlist_scripts)
        payload["workflow_scripts"] = list(self.workflow_scripts)
        payload["errors"] = list(self.errors)
        return payload


def _leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _clean_yaml_scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def extract_workflow_script_options(workflow_path: Path) -> WorkflowScriptOptions:
    """Extract script_name default and options from the manual run workflow."""

    lines = workflow_path.read_text(encoding="utf-8").splitlines()
    in_script_input = False
    in_options = False
    script_input_indent = 0
    options_indent = 0
    default_script = ""
    script_options: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        indent = _leading_spaces(line)
        if stripped == "script_name:":
            in_script_input = True
            in_options = False
            script_input_indent = indent
            continue

        if in_script_input and indent <= script_input_indent and stripped.endswith(":"):
            break

        if not in_script_input:
            continue

        if stripped.startswith("default:"):
            default_script = _clean_yaml_scalar(stripped.split(":", 1)[1])
            continue

        if stripped == "options:":
            in_options = True
            options_indent = indent
            continue

        if in_options:
            if indent <= options_indent and stripped.endswith(":"):
                in_options = False
                continue
            if stripped.startswith("- "):
                script_options.append(_clean_yaml_scalar(stripped[2:]))

    return WorkflowScriptOptions(
        default_script=default_script,
        script_options=tuple(script_options),
    )


def validate_registry(repo_root: Path | None = None) -> RegistryValidationReport:
    """Validate allowlist, registered paths, and workflow choices."""

    root = (repo_root or Path.cwd()).resolve()
    errors: list[str] = []
    scripts_dir = (root / "python" / "scripts").resolve()
    allowlist_scripts = tuple(sorted(SCRIPT_ALLOWLIST))

    if not allowlist_scripts:
        errors.append("SCRIPT_ALLOWLIST must contain at least one script.")

    seen_paths: set[str] = set()
    for script_name, relative_path in sorted(SCRIPT_ALLOWLIST.items()):
        if not script_name.strip():
            errors.append("Script names must be non-empty.")
        if any(token in script_name for token in ("/", "\\", "..")):
            errors.append(f"Script name is unsafe: {script_name}")
        if not relative_path.startswith("python/scripts/"):
            errors.append(
                f"Script path must stay under python/scripts: {relative_path}"
            )
        if relative_path in seen_paths:
            errors.append(f"Duplicate script path registered: {relative_path}")
        seen_paths.add(relative_path)

        script_path = (root / relative_path).resolve()
        try:
            script_path.relative_to(scripts_dir)
        except ValueError:
            errors.append(f"Script path is outside python/scripts: {relative_path}")
        if script_path.suffix != ".py":
            errors.append(f"Script path must point to a Python file: {relative_path}")
        if not script_path.is_file():
            errors.append(f"Registered script file is missing: {relative_path}")

    workflow_path = root / ".github" / "workflows" / "manual-python-run-script.yml"
    workflow_scripts: tuple[str, ...] = ()
    default_script = ""
    if not workflow_path.is_file():
        errors.append("Manual Python run workflow is missing.")
    else:
        workflow_options = extract_workflow_script_options(workflow_path)
        workflow_scripts = tuple(sorted(workflow_options.script_options))
        default_script = workflow_options.default_script

        if set(workflow_scripts) != set(allowlist_scripts):
            errors.append(
                "Workflow script_name options must match SCRIPT_ALLOWLIST exactly."
            )
        if default_script not in set(allowlist_scripts):
            errors.append(
                "Workflow script_name default must exist in SCRIPT_ALLOWLIST."
            )

    status = "success" if not errors else "failed"
    return RegistryValidationReport(
        status=status,
        allowlist_scripts=allowlist_scripts,
        workflow_scripts=workflow_scripts,
        default_script=default_script,
        errors=tuple(errors),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
    )


def write_report_files(report: RegistryValidationReport, output_dir: Path) -> None:
    """Write registry validation JSON and Markdown reports."""

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "registry-validation-report.json").write_text(
        json.dumps(report.to_jsonable(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# Python Script Registry Validation Report",
        "",
        f"Generated UTC: {report.created_at_utc}",
        f"Status: {report.status}",
        "",
        "## Allowlist scripts",
        "",
        *[f"- `{script}`" for script in report.allowlist_scripts],
        "",
        "## Workflow scripts",
        "",
        *[f"- `{script}`" for script in report.workflow_scripts],
        "",
        f"Default script: `{report.default_script}`",
        "",
        "## Errors",
        "",
    ]
    if report.errors:
        lines.extend(f"- {error}" for error in report.errors)
    else:
        lines.append("- None")

    (output_dir / "registry-validation-report.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    """Parse registry validation arguments."""

    parser = argparse.ArgumentParser(description="Validate Python script registry.")
    parser.add_argument(
        "--output-dir",
        default="artifacts/python-registry-validation",
        help="Directory for registry validation reports.",
    )
    return parser.parse_args()


def main() -> int:
    """Validate registry state and write reports."""

    args = parse_args()
    report = validate_registry()
    write_report_files(report, Path(args.output_dir))
    print(f"Registry validation status: {report.status}")
    if report.errors:
        for error in report.errors:
            print(f"- {error}")
    return 0 if report.status == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
