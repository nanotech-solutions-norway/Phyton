"""Tests for Python failure classification."""

from __future__ import annotations

import pytest

from python.tools.classify_failure import classify_text


@pytest.mark.parametrize(
    ("text", "expected_category"),
    [
        ("No matching distribution found for package-x", "dependency_failure"),
        ("ModuleNotFoundError: No module named example", "syntax_import_failure"),
        ("ruff format --check would reformat file.py", "lint_format_failure"),
        ("mypy error: incompatible return value type", "typing_failure"),
        ("pytest failed with AssertionError", "pytest_failure"),
        ("Invalid workflow file: yaml syntax", "workflow_configuration_failure"),
        (
            "Foundation phase only permits target_environment=development",
            "policy_guardrail_failure",
        ),
        ('{"status": "success"}', "no_failure_detected"),
    ],
)
def test_classify_text_known_signals(text: str, expected_category: str) -> None:
    result = classify_text(text)

    assert result.category == expected_category


def test_empty_text_has_no_failure_detected() -> None:
    result = classify_text("")

    assert result.category == "no_failure_detected"
    assert result.severity == "none"


def test_unknown_text_is_low_confidence_unknown_failure() -> None:
    result = classify_text("unexpected non-empty diagnostic text")

    assert result.category == "unknown_failure"
    assert result.confidence == "low"
