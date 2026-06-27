"""Classify Python workflow and artifact failure signals."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class FailureClassification:
    """Structured failure classification result."""

    category: str
    severity: str
    matched_signal: str
    confidence: str


SIGNALS: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    (
        "policy_guardrail_failure",
        "high",
        "high",
        (
            "foundation phase only permits",
            "not registered",
            "unsafe script name",
            "escaped python/scripts",
            "read_only",
        ),
    ),
    (
        "dependency_failure",
        "high",
        "high",
        (
            "no matching distribution found",
            "could not find a version that satisfies",
            "failed building wheel",
            "pip install",
            "resolutionimpossible",
        ),
    ),
    (
        "syntax_import_failure",
        "high",
        "high",
        (
            "syntaxerror",
            "modulenotfounderror",
            "importerror",
            "nameerror",
            "indentationerror",
        ),
    ),
    (
        "lint_format_failure",
        "medium",
        "high",
        (
            "ruff check",
            "ruff format",
            "would reformat",
            "found 1 error",
            "formatting check failed",
        ),
    ),
    (
        "typing_failure",
        "medium",
        "high",
        (
            "mypy",
            "error:",
            "found 1 error in",
            "found 2 errors in",
            "incompatible return value type",
        ),
    ),
    (
        "pytest_failure",
        "medium",
        "high",
        (
            "pytest",
            "failed",
            "error at setup",
            "assertionerror",
            "short test summary info",
        ),
    ),
    (
        "workflow_configuration_failure",
        "high",
        "medium",
        (
            "invalid workflow file",
            "you have an error in your yaml syntax",
            "unrecognized named-value",
            "the workflow is not valid",
            "every step must define a uses or run key",
        ),
    ),
)


def classify_text(text: str) -> FailureClassification:
    """Classify text from logs, reports, or artifacts."""

    normalized = text.lower()
    if not normalized.strip():
        return FailureClassification(
            category="no_failure_detected",
            severity="none",
            matched_signal="",
            confidence="medium",
        )

    for category, severity, confidence, patterns in SIGNALS:
        for pattern in patterns:
            if pattern in normalized:
                return FailureClassification(
                    category=category,
                    severity=severity,
                    matched_signal=pattern,
                    confidence=confidence,
                )

    success_markers = (
        "status: success",
        '"status": "success"',
        "passed",
        "completed in development mode",
    )
    if any(marker in normalized for marker in success_markers):
        return FailureClassification(
            category="no_failure_detected",
            severity="none",
            matched_signal="success marker",
            confidence="medium",
        )

    return FailureClassification(
        category="unknown_failure",
        severity="unknown",
        matched_signal="unclassified text",
        confidence="low",
    )


def build_failure_record(source_name: str, text: str) -> dict[str, str]:
    """Create a JSON-safe classification record."""

    result = classify_text(text)
    payload = asdict(result)
    payload["source_name"] = source_name
    payload["created_at_utc"] = datetime.now(timezone.utc).isoformat()
    return payload
