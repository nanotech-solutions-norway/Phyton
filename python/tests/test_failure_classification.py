"""Tests for Python failure classification signals."""

from __future__ import annotations

from python.tools.classify_failure import build_failure_record, classify_text


def test_classifies_health_report_attention_status() -> None:
    result = classify_text("completed with status: attention_required")

    assert result.category == "report_attention_required"
    assert result.severity == "medium"
    assert result.confidence == "high"


def test_classifies_mypy_annotation_error() -> None:
    result = classify_text("Need type annotation")

    assert result.category == "typing_failure"
    assert result.severity == "medium"
    assert result.matched_signal == "need type annotation"


def test_classifies_ruff_format_check_failure() -> None:
    result = classify_text("ruff format --check\nwould reformat")

    assert result.category == "lint_format_failure"
    assert result.severity == "medium"


def test_build_failure_record_preserves_source_name() -> None:
    record = build_failure_record("pytest-output", "short test summary info")

    assert record["source_name"] == "pytest-output"
    assert record["category"] == "pytest_failure"
