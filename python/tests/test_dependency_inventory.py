"""Tests for dependency inventory script."""

from __future__ import annotations

from pathlib import Path

from python.scripts.dependency_inventory import (
    collect_dependency_inventory,
    inspect_requirements_file,
    parse_requirement_line,
)


def test_parse_requirement_line_ignores_blank_and_comment() -> None:
    assert parse_requirement_line("") is None
    assert parse_requirement_line("# comment") is None


def test_parse_requirement_line_with_version_spec() -> None:
    result = parse_requirement_line("pytest>=8.4,<9")

    assert result is not None
    assert result["package"] == "pytest"
    assert result["operator"] == ">="
    assert result["version_spec"] == "8.4,<9"


def test_inspect_requirements_file(tmp_path: Path) -> None:
    requirements = tmp_path / "python" / "requirements-dev.txt"
    requirements.parent.mkdir(parents=True)
    requirements.write_text("pytest>=8.4,<9\nruff>=0.12,<1\n", encoding="utf-8")

    result = inspect_requirements_file(requirements, tmp_path)

    assert result["exists"] is True
    assert result["dependency_count"] == 2
    assert result["dependencies"][0]["package"] == "pytest"


def test_collect_dependency_inventory(tmp_path: Path) -> None:
    python_dir = tmp_path / "python"
    python_dir.mkdir()
    (python_dir / "requirements.txt").write_text("\n", encoding="utf-8")
    (python_dir / "requirements-dev.txt").write_text("pytest>=8.4,<9\n", encoding="utf-8")

    inventory = collect_dependency_inventory(tmp_path)

    assert inventory["status"] == "success"
    assert inventory["dependency_count"] == 1
