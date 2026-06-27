"""Inspect local Python test reports and workflow artifacts."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from python.tools.classify_failure import build_failure_record, classify_text

TEXT_SUFFIXES = {".log", ".md", ".txt", ".out", ".err", ".json"}
XML_SUFFIXES = {".xml"}


def parse_args() -> argparse.Namespace:
    """Parse inspection arguments."""

    parser = argparse.ArgumentParser(
        description="Inspect Python artifacts and reports."
    )
    parser.add_argument(
        "--input-dir",
        action="append",
        default=[],
        help="Directory to inspect. May be supplied multiple times.",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts/python-inspection",
        help="Directory for generated inspection reports.",
    )
    parser.add_argument(
        "--mode",
        choices=("sample", "repository"),
        default="sample",
        help="Inspection mode. Both modes remain read-only.",
    )
    return parser.parse_args()


def safe_read_text(path: Path, max_chars: int = 50_000) -> str:
    """Read bounded text for classification."""

    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError as exc:
        return f"read_error: {type(exc).__name__}: {exc}"


def parse_junit_xml(path: Path) -> dict[str, Any]:
    """Parse a pytest JUnit XML report."""

    tree = ET.parse(path)
    root = tree.getroot()

    test_suites = []
    if root.tag == "testsuite":
        test_suites = [root]
    else:
        test_suites = list(root.findall("testsuite"))

    tests = 0
    failures = 0
    errors = 0
    skipped = 0
    for suite in test_suites:
        tests += int(float(suite.attrib.get("tests", "0")))
        failures += int(float(suite.attrib.get("failures", "0")))
        errors += int(float(suite.attrib.get("errors", "0")))
        skipped += int(float(suite.attrib.get("skipped", "0")))

    status = "success" if failures == 0 and errors == 0 else "failed"
    classification_text = "pytest failed" if status == "failed" else "status: success"
    classification = classify_text(classification_text)

    return {
        "path": str(path),
        "type": "junit_xml",
        "tests": tests,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "status": status,
        "classification": classification.category,
        "severity": classification.severity,
    }


def inspect_file(path: Path) -> dict[str, Any]:
    """Inspect one local artifact file."""

    if path.suffix.lower() in XML_SUFFIXES:
        try:
            return parse_junit_xml(path)
        except (ET.ParseError, OSError, ValueError) as exc:
            record = build_failure_record(str(path), f"xml parse failure {exc}")
            return {"path": str(path), "type": "xml_parse_error", **record}

    if path.suffix.lower() in TEXT_SUFFIXES:
        text = safe_read_text(path)
        record = build_failure_record(str(path), text)
        return {"path": str(path), "type": "text", **record}

    return {
        "path": str(path),
        "type": "unsupported",
        "classification": "not_inspected",
        "severity": "none",
    }


def collect_files(input_dirs: list[str]) -> list[Path]:
    """Collect supported files from input directories."""

    files: list[Path] = []
    for input_dir in input_dirs:
        root = Path(input_dir)
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES | XML_SUFFIXES:
                files.append(path)
    return files


def summarize(inspections: list[dict[str, Any]]) -> dict[str, Any]:
    """Build an aggregate inspection summary."""

    categories: dict[str, int] = {}
    severities: dict[str, int] = {}
    for item in inspections:
        category = str(item.get("classification", item.get("category", "unknown")))
        severity = str(item.get("severity", "unknown"))
        categories[category] = categories.get(category, 0) + 1
        severities[severity] = severities.get(severity, 0) + 1

    has_failures = any(
        item.get("status") == "failed" or item.get("severity") in {"medium", "high"}
        for item in inspections
    )

    return {
        "status": "attention_required" if has_failures else "success",
        "files_inspected": len(inspections),
        "categories": categories,
        "severities": severities,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    inspections: list[dict[str, Any]],
) -> None:
    """Write a Markdown inspection report."""

    lines = [
        "# Python Artifact Inspection Report",
        "",
        f"Generated UTC: {summary['created_at_utc']}",
        f"Status: {summary['status']}",
        f"Files inspected: {summary['files_inspected']}",
        "",
        "## Findings",
        "",
        "| File | Type | Classification | Severity | Status |",
        "|---|---|---|---|---|",
    ]

    for item in inspections:
        classification = item.get("classification", item.get("category", "unknown"))
        lines.append(
            "| "
            f"{item.get('path', '')} | "
            f"{item.get('type', '')} | "
            f"{classification} | "
            f"{item.get('severity', '')} | "
            f"{item.get('status', '')} |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Inspect configured local paths and write reports."""

    args = parse_args()
    input_dirs = args.input_dir or ["TestResults", "artifacts"]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = collect_files(input_dirs)
    inspections = [inspect_file(path) for path in files]
    summary = summarize(inspections)

    report = {
        "mode": args.mode,
        "summary": summary,
        "inspections": inspections,
        "inputs": input_dirs,
        "external_writes": "out_of_scope",
        "secrets_policy": "secrets and environment dumps are not collected",
    }

    (output_dir / "inspection-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_markdown(output_dir / "inspection-report.md", summary, inspections)

    print(f"Artifact inspection completed. Files inspected: {len(inspections)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
