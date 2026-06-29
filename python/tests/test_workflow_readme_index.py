"""Tests for README workflow index coverage."""

from __future__ import annotations

from pathlib import Path


def workflow_paths() -> list[Path]:
    return sorted((Path.cwd() / ".github" / "workflows").glob("*.yml"))


def workflow_name(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("name: "):
            return line.removeprefix("name: ").strip()

    msg = f"{path}: missing workflow name"
    raise AssertionError(msg)


def test_readme_indexes_workflow_paths() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")
    missing = [
        path.relative_to(Path.cwd()).as_posix()
        for path in workflow_paths()
        if f"`{path.relative_to(Path.cwd()).as_posix()}`" not in readme
    ]

    assert missing == []


def test_readme_indexes_workflow_names() -> None:
    readme = (Path.cwd() / "README.md").read_text(encoding="utf-8")
    missing = [
        name
        for name in map(workflow_name, workflow_paths())
        if f"`{name}`" not in readme
    ]

    assert missing == []


def test_workflow_index_has_entries() -> None:
    assert workflow_paths() != []
