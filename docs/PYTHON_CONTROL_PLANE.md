# Python Control Plane Foundation — 14:35, 28.06.2026

## Purpose

This document defines the foundation, artifact inspection, controlled script expansion, read-only repository intelligence, and repository health-report layers for Python execution in `nanotech-solutions-norway/Phyton`.

The `Phyton` repository is the Python source of truth. ChatGPT acts as the orchestration layer that instructs which GitHub Actions workflow to run, which logs or artifacts to inspect, and which isolated patch should be applied next. ChatGPT must not assume local Python, local PowerShell, or Android-local runtime access.

## Operating posture

- GitHub Actions is the execution runtime.
- The current layers are development-only.
- Production writes are out of scope.
- Staging writes are out of scope.
- External system writes are out of scope.
- Secrets must not be printed in workflow logs.
- Python scripts must be selected from a fixed workflow choice list and validated by the repository allowlist.
- Registry and workflow choices must remain synchronized.
- Full validation now runs automatically on relevant pushes.
- Failed workflows must be debugged from GitHub Actions logs and uploaded artifacts before proposing fixes.
- Write-capable Python workflows require a later explicit phase and approval gate.

## Folder structure

| Path | Purpose |
|---|---|
| `python/scripts/` | Registered Python scripts that may be used through the manual workflow. |
| `python/templates/` | Templates for future registered scripts. |
| `python/tools/` | Internal runner, allowlist, diagnostic, artifact inspection, failure classification, and registry validation utilities. |
| `python/examples/` | Read-only examples and future non-production references. |
| `python/tests/` | pytest tests and execution guardrails. |
| `python/requirements.txt` | Runtime dependencies for controlled scripts. |
| `python/requirements-dev.txt` | Validation dependencies for pytest, Ruff, and mypy. |
| `.github/workflows/ci-python-quality.yml` | Python quality gate. |
| `.github/workflows/ci-python-full-validation.yml` | Automatic full validation workflow. |
| `.github/workflows/manual-python-run-script.yml` | Manual registered-script workflow. |
| `.github/workflows/manual-python-debug.yml` | Manual sanitized debug workflow. |
| `.github/workflows/manual-python-inspect-artifacts.yml` | Manual artifact inspection and failure triage workflow. |
| `.github/workflows/manual-python-validate-registry.yml` | Manual registry synchronization validation workflow. |

## Workflows

### CI - Python Quality Gate

Purpose:

1. Check out the repository.
2. Set up Python through GitHub Actions.
3. Install runtime and development dependencies.
4. Run Ruff formatting check.
5. Run Ruff lint.
6. Run mypy typing validation.
7. Run pytest.
8. Upload pytest XML reports as an artifact.

Expected artifact:

- `python-quality-test-results`

### CI - Python Full Validation

Purpose:

1. Run quality-gate checks.
2. Run pytest with XML output.
3. Run all registered baseline and report scripts.
4. Inspect generated validation artifacts.
5. Validate registry synchronization.
6. Upload full validation artifacts.

Expected artifact:

- `python-full-validation-artifacts`

### Manual - Python Run Script

Purpose:

1. Use only a fixed workflow_dispatch script option.
2. Enforce `target_environment=development`.
3. Enforce `run_mode=read_only`.
4. Resolve the selected script through `python/tools/script_allowlist.py`.
5. Produce JSON/stdout artifacts.

Expected artifact:

- `python-script-output`

Current registered scripts:

- `hello_control_plane`
- `repository_inventory`
- `workflow_inventory`
- `dependency_inventory`
- `repository_health_report`

### Manual - Python Debug

Purpose:

1. Capture sanitized Python diagnostics.
2. Capture Python version, pip version, dependency state when selected, and repository structure when selected.
3. Upload debug artifacts.
4. Avoid printing secrets, tokens, or full environment dumps.

Expected artifact:

- `python-debug-artifacts`

### Manual - Python Inspect Artifacts

Purpose:

1. Generate a local pytest XML report for inspection.
2. Capture pytest stdout and exit status.
3. Inspect local XML/text/JSON artifacts.
4. Classify local findings into standard failure categories.
5. Upload JSON and Markdown inspection reports.

Expected artifact:

- `python-artifact-inspection-report`

### Manual - Python Validate Registry

Purpose:

1. Validate `SCRIPT_ALLOWLIST`.
2. Validate that registered script files exist under `python/scripts/`.
3. Validate that `.github/workflows/manual-python-run-script.yml` script choices match `SCRIPT_ALLOWLIST`.
4. Upload JSON and Markdown registry reports.

Expected artifact:

- `python-registry-validation-report`

## Dependency strategy

The foundation uses two requirements files:

- `python/requirements.txt` for runtime dependencies.
- `python/requirements-dev.txt` for validation dependencies.

The workflows use pip caching based on both requirements files. New dependencies should be added only when needed by a registered script or validation layer. Private package indexes, credentials, and authenticated package installation remain out of scope.

## Script allowlist policy

The manual run workflow exposes only fixed `workflow_dispatch` choices. The selected value is validated again by `python/tools/script_allowlist.py`.

A script is not available merely because it exists under `python/scripts/`. To register a new script, the allowlist and workflow input list must both be patched, then the Python quality gate and registry validation workflow must pass.

## Repository intelligence policy

Phase 4 inventory scripts are repository-local and report-producing. They may inspect repository files, workflow YAML files, and Python requirements files. They must not use secrets, deploy software, or modify project data.

## Repository health policy

Phase 5 health reports consolidate inventory, dependency, workflow, and registry checks. The report can classify the repository as `healthy`, `manual_review_required`, or `attention_required`.

## Artifact inspection policy

Artifact inspection is local-artifact only. The Phase 2 workflow does not download prior workflow artifacts or fetch external logs. When the user provides a failed workflow log ZIP, ChatGPT must inspect that evidence before patching.

## Registry validation policy

The script registry must validate before a new registered script is considered available. The validator checks script keys, script paths, file existence, workflow choices, and workflow default values.

## Debug policy

Debug, inspection, and registry workflows must collect artifacts instead of printing broad state. They may print tool versions and sanitized summaries. They must not print:

- secrets;
- tokens;
- complete environment variable dumps;
- customer data;
- production credentials;
- private accounting data;
- private bank data.

## Out of scope

The following items are deferred:

- production writes;
- staging writes;
- external system writes;
- secrets-consuming Python scripts;
- long-running jobs;
- arbitrary command execution;
- dependency installation from private package sources;
- deployment workflows;
- modifying project data outside this repository.
