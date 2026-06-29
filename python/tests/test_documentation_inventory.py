"""Tests for the documentation inventory script."""

from __future__ import annotations

from python.scripts import documentation_inventory


def test_documentation_inventory_script_name() -> None:
    assert documentation_inventory.SCRIPT_NAME == "documentation_inventory"


def test_documentation_inventory_directory() -> None:
    assert documentation_inventory.DOCUMENTATION_DIRECTORY == "docs"
