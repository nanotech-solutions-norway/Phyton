"""Guardrail tests for the Python script allowlist."""

from __future__ import annotations

from pathlib import Path

import pytest

from python.tools.script_allowlist import (
    ScriptSelectionError,
    list_allowed_scripts,
    resolve_allowed_script,
)


def test_script_allowlist_contains_sample_script() -> None:
    assert "hello_control_plane" in list_allowed_scripts()


def test_resolve_allowed_script_stays_under_scripts_directory() -> None:
    repo_root = Path.cwd()
    script_path = resolve_allowed_script("hello_control_plane", repo_root=repo_root)

    assert script_path.name == "hello_control_plane.py"
    assert script_path.is_file()
    assert script_path.relative_to(repo_root / "python" / "scripts")


@pytest.mark.parametrize(
    "script_name",
    [
        "",
        "../hello_control_plane",
        "python/scripts/hello_control_plane.py",
        "hello_control_plane; echo unsafe",
        "unknown_script",
    ],
)
def test_unregistered_script_names_are_rejected(script_name: str) -> None:
    with pytest.raises(ScriptSelectionError):
        resolve_allowed_script(script_name, repo_root=Path.cwd())


def test_allowed_script_keys_have_no_path_tokens() -> None:
    for script_name in list_allowed_scripts():
        assert "/" not in script_name
        assert "\\" not in script_name
        assert ".." not in script_name
