# Python Control Plane Foundation — 15:05, 27.06.2026

## Purpose

This document defines the foundation layer for Python execution in `nanotech-solutions-norway/Phyton`.

The `Phyton` repository is the Python source of truth. ChatGPT acts as the orchestration layer that instructs which GitHub Actions workflow to run, which logs or artifacts to inspect, and which isolated patch should be applied next. ChatGPT must not assume local Python, local PowerShell, or Android-local runtime access.

## Operating posture

- GitHub Actions is the execution runtime.
- The foundation phase is development-only.
- Production writes are out of scope.
- Staging writes are out of scope.
- External system writes are out of scope.
- Secrets must not be printed in workflow logs.
- Python scripts must be selected from a fixed workflow choice list and validated by the repository allowlist.
- Failed workflows must be debugged from GitHub Actions logs and uploaded artifacts before proposing fixes.
- Write-capable Python workflows require a later explicit phase and approval gate.

## Folder structure

| Path | Purpose |
|---|---|
| `python/scripts/` | Registered Python scripts that may be executed through the manual workflow. |
| `python/tools/` | Internal runner, allowlist, and diagnostic utilities. |
| `python/examples/` | Read-only examples and future non-production references. |
| `python/tests/` | pytest tests and execution guardrails. |
| `python/requirements.txt` | Runtime dependencies for controlled scripts. |
| `python/requirements-dev.txt` | Validation dependencies for pytest, Ruff, and mypy. |
| `.github/workflows/ci-python-quality.yml` | Python quality gate. |
| `.github/workflows/manual-python-run-script.yml` | Manual registered-script execution workflow. |
| `.github/workflows/manual-python-debug.yml` | Manual sanitized debug workflow. |

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

### Manual - Python Run Script

Purpose:

1. Run only a fixed workflow_dispatch script option.
2. Enforce `target_environment=development`.
3. Enforce `run_mode=read_only`.
4. Resolve the selected script through `python/tools/script_allowlist.py`.
5. Execute the selected script and upload JSON/stdout artifacts.

Expected artifact:

- `python-script-output`

Registered foundation script:

- `hello_control_plane`

### Manual - Python Debug

Purpose:

1. Capture sanitized Python diagnostics.
2. Capture Python version, pip version, dependency state when selected, and repository structure when selected.
3. Upload debug artifacts.
4. Avoid printing secrets, tokens, or full environment dumps.

Expected artifact:

- `python-debug-artifacts`

## Dependency strategy

The foundation uses two requirements files:

- `python/requirements.txt` for runtime dependencies.
- `python/requirements-dev.txt` for validation dependencies.

The workflows use pip caching based on both requirements files. New dependencies should be added only when needed by a registered script or validation layer. Private package indexes, credentials, and authenticated package installation remain out of scope for the foundation phase.

## Script allowlist policy

The manual run workflow exposes only fixed `workflow_dispatch` choices. The selected value is validated again by `python/tools/script_allowlist.py`.

A script is not runnable merely because it exists under `python/scripts/`. To register a new script, the allowlist and workflow input list must both be patched, then the Python quality gate must pass.

## Debug policy

Debug workflows must collect artifacts instead of printing broad state. They may print tool versions and sanitized summaries. They must not print:

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
