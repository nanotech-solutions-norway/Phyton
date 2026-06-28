# Phase 5 — Repository Health Report — 14:35, 28.06.2026

## Purpose

Phase 5 adds a consolidated read-only repository health report to `nanotech-solutions-norway/Phyton`.

The phase also adds an automatic full-validation workflow so Python control-plane changes are validated on push.

## Added registered script

| Script key | File | Purpose |
|---|---|---|
| `repository_health_report` | `python/scripts/repository_health_report.py` | Builds a consolidated repository health report from inventory, dependency, workflow, and registry checks. |

## Automatic validation workflow

Added workflow:

```text
CI - Python Full Validation
```

File:

```text
.github/workflows/ci-python-full-validation.yml
```

Triggers:

- push to `main` affecting Python, workflow, docs, or README files;
- manual workflow dispatch.

## Full-validation sequence

The automatic full-validation workflow performs:

1. Ruff format check.
2. Ruff lint.
3. mypy typing validation.
4. pytest.
5. Registered script run for `hello_control_plane`.
6. Registered script run for `repository_inventory`.
7. Registered script run for `workflow_inventory`.
8. Registered script run for `dependency_inventory`.
9. Registered script run for `repository_health_report`.
10. Artifact inspection.
11. Registry validation.
12. Artifact upload.

Expected artifact:

```text
python-full-validation-artifacts
```

## Health classification

The health script classifies the repository as:

| Status | Meaning |
|---|---|
| `healthy` | Required docs, workflows, scripts, dependency files, and registry state are present and synchronized. |
| `manual_review_required` | No blocking finding, but warning-level review items exist. |
| `attention_required` | Blocking findings exist and should be corrected. |

## Health report checks

The script checks:

- required documentation files;
- required workflow files;
- registered script files;
- unregistered Python scripts under `python/scripts/`;
- registry validation status;
- dependency file inventory;
- workflow inventory count.

## Script output files

When run through `Manual - Python Run Script` with `script_name=repository_health_report`, expected files are:

```text
run-summary.json
repository-health-report.json
repository-health-report.md
stdout.txt
```

## Security posture

Phase 5 remains:

- development-only;
- read-only;
- repository-local;
- no production writes;
- no staging writes;
- no external system writes;
- no secrets-consuming scripts;
- no deployment workflow.

## Validation sequence

The automatic workflow now validates the full suite. Manual fallback validation remains:

1. `CI - Python Quality Gate`
2. `CI - Python Full Validation`
3. `Manual - Python Debug`
   - `target_environment=development`
   - `diagnostic_level=repository`
4. `Manual - Python Run Script`
   - `script_name=repository_health_report`
   - `target_environment=development`
   - `run_mode=read_only`
5. `Manual - Python Inspect Artifacts`
   - `target_environment=development`
   - `inspection_mode=sample`
6. `Manual - Python Validate Registry`
   - `target_environment=development`

## Failure handling rule

If the automatic full-validation workflow fails, inspect the GitHub Actions log ZIP and uploaded artifacts before patching.
