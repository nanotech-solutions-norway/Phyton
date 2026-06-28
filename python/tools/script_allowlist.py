"""Script allowlist for controlled Python execution."""

from __future__ import annotations

from pathlib import Path

SCRIPT_ALLOWLIST: dict[str, str] = {
    "control_plane_readiness": "python/scripts/control_plane_readiness.py",
    "dependency_inventory": "python/scripts/dependency_inventory.py",
    "hello_control_plane": "python/scripts/hello_control_plane.py",
    "repository_health_report": "python/scripts/repository_health_report.py",
    "repository_inventory": "python/scripts/repository_inventory.py",
    "workflow_inventory": "python/scripts/workflow_inventory.py",
}


class ScriptSelectionError(ValueError):
    """Raised when a selected script is outside the allowlist."""


def list_allowed_scripts() -> tuple[str, ...]:
    """Return allowed script names in stable order."""

    return tuple(sorted(SCRIPT_ALLOWLIST))


def resolve_allowed_script(script_name: str, repo_root: Path | None = None) -> Path:
    """Resolve a script key to a repository-local script path."""

    if not script_name or any(token in script_name for token in ("/", "\\", "..")):
        message = "Unsafe script name. Select a registered script key."
        raise ScriptSelectionError(message)

    if script_name not in SCRIPT_ALLOWLIST:
        allowed = ", ".join(list_allowed_scripts())
        message = f"Script is not registered. Allowed scripts: {allowed}"
        raise ScriptSelectionError(message)

    root = (repo_root or Path.cwd()).resolve()
    scripts_dir = (root / "python" / "scripts").resolve()
    script_path = (root / SCRIPT_ALLOWLIST[script_name]).resolve()

    try:
        script_path.relative_to(scripts_dir)
    except ValueError as exc:
        message = "Registered script path escaped python/scripts."
        raise ScriptSelectionError(message) from exc

    if not script_path.is_file():
        raise ScriptSelectionError(f"Registered script file is missing: {script_path}")

    return script_path
