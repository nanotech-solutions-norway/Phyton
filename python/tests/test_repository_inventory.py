"""Tests for repository inventory script."""

from __future__ import annotations

from pathlib import Path

from python.scripts.repository_inventory import (
    collect_repository_inventory,
    should_skip,
)


def test_should_skip_excluded_directory() -> None:
    assert should_skip(Path(".git/config")) is True
    assert should_skip(Path("python/scripts/example.py")) is False


def test_collect_repository_inventory_counts_files(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello\n", encoding="utf-8")
    scripts_dir = tmp_path / "python" / "scripts"
    scripts_dir.mkdir(parents=True)
    (scripts_dir / "example.py").write_text("print('hello')\n", encoding="utf-8")
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("ignored\n", encoding="utf-8")

    inventory = collect_repository_inventory(tmp_path)

    assert inventory["status"] == "success"
    assert inventory["file_count"] == 2
    assert inventory["extension_counts"][".md"] == 1
    assert inventory["extension_counts"][".py"] == 1
    assert ".git" not in inventory["top_level_counts"]
