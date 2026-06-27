# Phase 2 — Artifact Inspection and Failure Triage — 15:22, 27.06.2026

## Purpose

Phase 2 adds a read-only Python artifact inspection and failure triage layer to `nanotech-solutions-norway/Phyton`.

The layer helps ChatGPT and the repository operator classify local workflow artifacts before proposing patches. It does not fetch private logs, call external systems, use secrets, or perform production/staging writes.

## Added components

| File | Purpose |
|---|---|
| `python/tools/classify_failure.py` | Classifies failure signals into standard categories. |
| `python/tools/inspect_test_results.py` | Inspects local XML/text/JSON artifacts and writes JSON/Markdown reports. |
| `python/tests/test_failure_classifier.py` | Tests classifier behavior. |
| `python/tests/test_artifact_inspection.py` | Tests local artifact inspection behavior. |
| `.github/workflows/manual-python-inspect-artifacts.yml` | Manual read-only artifact inspection workflow. |

## Failure categories

| Category | Meaning |
|---|---|
| `dependency_failure` | pip/package installation or dependency resolution failure. |
| `syntax_import_failure` | Python syntax, import, module, name, or indentation failure. |
| `lint_format_failure` | Ruff formatting or lint failure. |
| `typing_failure` | mypy typing validation failure. |
| `pytest_failure` | pytest test failure or setup failure. |
| `workflow_configuration_failure` | GitHub Actions YAML/workflow configuration failure. |
| `policy_guardrail_failure` | Development-only/read-only/allowlist guardrail failure. |
| `no_failure_detected` | No failure signal detected. |
| `unknown_failure` | Non-empty diagnostic text did not match a known category. |

## Manual workflow

Workflow:

```text
Manual - Python Inspect Artifacts
```

Inputs:

```text
target_environment=development
inspection_mode=sample | repository
```

The workflow:

1. checks out `main`;
2. sets up Python;
3. installs runtime and development dependencies;
4. enforces development-only inspection;
5. generates a local pytest XML report;
6. captures pytest stdout and exit status;
7. runs `python.tools.inspect_test_results`;
8. uploads `python-artifact-inspection-report`.

## Expected artifact

```text
python-artifact-inspection-report
```

Expected files:

```text
inspection-report.json
inspection-report.md
pytest-stdout.txt
pytest-exit-code.txt
```

## Security posture

Phase 2 remains:

- read-only;
- development-only;
- local-artifact only;
- no production writes;
- no staging writes;
- no external system writes;
- no arbitrary command input;
- no secrets or full environment dumps.

## Validation sequence

1. `CI - Python Quality Gate`
2. `Manual - Python Debug`
   - `target_environment=development`
   - `diagnostic_level=repository`
3. `Manual - Python Run Script`
   - `script_name=hello_control_plane`
   - `target_environment=development`
   - `run_mode=read_only`
4. `Manual - Python Inspect Artifacts`
   - `target_environment=development`
   - `inspection_mode=sample`

## Failure handling rule

If any Phase 2 workflow fails, inspect the GitHub Actions log ZIP and uploaded artifacts before patching.
