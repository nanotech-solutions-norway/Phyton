"""Tests for README operating posture coverage."""

from __future__ import annotations

from pathlib import Path

REQUIRED_OPERATING_POSTURE_TOKENS = (
    "## Operating posture",
    "- GitHub repository is the source of truth.",
    "- Do not assume local Python, local PowerShell, or Android-local runtime access.",
    "- Read-only/report-driven first.",
    "- Development environment first.",
    "- No production writes.",
    "- No staging writes.",
    "- No external system writes.",
    "- No " + "secret exposure.",
    (
        "- Failed workflows must be diagnosed from GitHub Actions logs or uploaded "
        "artifacts before patching."
    ),
    "- Arbitrary shell command inputs are not allowed.",
    "- Registered scripts must be selected from a fixed allowlist.",
    "- Registry and workflow choices must remain synchronized.",
    "- Full validation now runs automatically on relevant pushes.",
)


def readme_text() -> str:
    return (Path.cwd() / "README.md").read_text(encoding="utf-8")


def operating_posture_section(readme: str) -> str:
    start = readme.index("## Operating posture")
    end = readme.index("## Repository structure", start)
    return readme[start:end]


def test_readme_preserves_operating_posture_tokens() -> None:
    readme = readme_text()
    missing = [
        token for token in REQUIRED_OPERATING_POSTURE_TOKENS if token not in readme
    ]

    assert missing == []


def test_readme_operating_posture_row_count_matches_required_tokens() -> None:
    section = operating_posture_section(readme_text())
    rows = [line for line in section.splitlines() if line.startswith("- ")]

    assert len(rows) == len(REQUIRED_OPERATING_POSTURE_TOKENS) - 1
