"""Tests for registered script path policy invariants."""

from __future__ import annotations

from pathlib import Path

from python.tools.script_allowlist import SCRIPT_ALLOWLIST, resolve_allowed_script


def test_registered_script_keys_are_plain_names() -> None:
    invalid = [
        script_name
        for script_name in SCRIPT_ALLOWLIST
        if not script_name or "/" in script_name or "\\" in script_name or ".." in script_name
    ]

    assert invalid == []


def test_registered_script_paths_stay_inside_scripts_directory() -> None:
    invalid = [
        script_path
        for script_path in SCRIPT_ALLOWLIST.values()
        if not script_path.startswith("python/scripts/") or not script_path.endswith(".py")
    ]

    assert invalid == []


def test_registered_script_paths_are_unique() -> None:
    paths = list(SCRIPT_ALLOWLIST.values())

    assert len(paths) == len(set(paths))


def test_registered_script_files_exist_and_resolve() -> None:
    repo_root = Path.cwd()
    resolved_paths = [
        resolve_allowed_script(script_name, repo_root)
        for script_name in sorted(SCRIPT_ALLOWLIST)
    ]

    assert all(path.is_file() for path in resolved_paths)
    assert all(path.suffix == ".py" for path in resolved_paths)
