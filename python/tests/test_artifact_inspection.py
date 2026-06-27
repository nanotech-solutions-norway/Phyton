"""Tests for local artifact inspection."""

from __future__ import annotations

import json
from pathlib import Path

from python.tools.inspect_test_results import (
    collect_files,
    inspect_file,
    main,
    parse_junit_xml,
)


def test_parse_junit_xml_success(tmp_path: Path) -> None:
    report = tmp_path / "pytest-results.xml"
    report.write_text(
        '<testsuite name="pytest" tests="2" failures="0" errors="0" skipped="0" />',
        encoding="utf-8",
    )

    result = parse_junit_xml(report)

    assert result["status"] == "success"
    assert result["tests"] == 2
    assert result["classification"] == "no_failure_detected"


def test_parse_junit_xml_failure(tmp_path: Path) -> None:
    report = tmp_path / "pytest-results.xml"
    report.write_text(
        '<testsuite name="pytest" tests="2" failures="1" errors="0" skipped="0" />',
        encoding="utf-8",
    )

    result = parse_junit_xml(report)

    assert result["status"] == "failed"
    assert result["classification"] == "pytest_failure"


def test_inspect_text_file_classifies_dependency_failure(tmp_path: Path) -> None:
    log_file = tmp_path / "install.log"
    log_file.write_text("No matching distribution found", encoding="utf-8")

    result = inspect_file(log_file)

    assert result["category"] == "dependency_failure"


def test_collect_files_uses_supported_suffixes(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("status: success", encoding="utf-8")
    (tmp_path / "b.xml").write_text("<testsuite />", encoding="utf-8")
    (tmp_path / "c.bin").write_bytes(b"ignored")

    files = collect_files([str(tmp_path)])

    assert sorted(path.name for path in files) == ["a.txt", "b.xml"]


def test_main_writes_reports(tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    (input_dir / "pytest-results.xml").write_text(
        '<testsuite name="pytest" tests="1" failures="0" errors="0" skipped="0" />',
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "inspect_test_results",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--mode",
            "sample",
        ],
    )

    assert main() == 0

    report = json.loads(
        (output_dir / "inspection-report.json").read_text(encoding="utf-8")
    )
    assert report["summary"]["files_inspected"] == 1
    assert (output_dir / "inspection-report.md").is_file()
