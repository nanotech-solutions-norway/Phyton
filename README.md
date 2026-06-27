# Python GitHub Control Plane — 15:22, 27.06.2026

This repository is the separate Python execution, testing, debugging, validation, artifact inspection, and failure triage control-plane layer for NanoTech Solutions Norway projects.

Repository name: `nanotech-solutions-norway/Phyton`

## Purpose

Use GitHub Actions as the execution runtime for controlled Python operations. ChatGPT acts as orchestrator and should instruct which workflow to run, which artifacts to inspect, and which isolated patch to apply next.

## Operating posture

- GitHub repository is the source of truth.
- Do not assume local Python, local PowerShell, or Android-local runtime access.
- Read-only/report-driven first.
- Development environment first.
- No production writes.
- No staging writes.
- No external system writes.
- No secret exposure.
- Failed workflows must be diagnosed from GitHub Actions logs or uploaded artifacts before patching.
- Arbitrary shell command inputs are not allowed.
- Registered scripts must be selected from a fixed allowlist.

## Repository structure

| Path | Purpose |
|---|---|
| `python/scripts/` | Registered Python scripts for manual GitHub Actions execution. |
| `python/tools/` | Allowlist, runner, diagnostics, artifact inspection, and failure classification tools. |
| `python/examples/` | Non-production examples. |
| `python/tests/` | pytest tests and execution guardrails. |
| `python/requirements.txt` | Runtime dependencies. |
| `python/requirements-dev.txt` | Development validation dependencies. |
| `.github/workflows/ci-python-quality.yml` | Python quality gate. |
| `.github/workflows/manual-python-run-script.yml` | Manual registered-script runner. |
| `.github/workflows/manual-python-debug.yml` | Manual debug workflow. |
| `.github/workflows/manual-python-inspect-artifacts.yml` | Manual artifact inspection and failure triage workflow. |
| `docs/PYTHON_CONTROL_PLANE.md` | Control-plane specification. |
| `docs/CHATGPT_PYTHON_ORCHESTRATOR_COMMANDS.md` | ChatGPT orchestration commands. |
| `docs/PHASE2_ARTIFACT_INSPECTION_AND_FAILURE_TRIAGE.md` | Phase 2 artifact inspection and triage specification. |

## Workflows

| Workflow | Purpose |
|---|---|
| `CI - Python Quality Gate` | Ruff format check, Ruff lint, mypy, pytest. |
| `Manual - Python Debug` | Sanitized Python diagnostics and artifact upload. |
| `Manual - Python Run Script` | Development-only registered Python script execution. |
| `Manual - Python Inspect Artifacts` | Read-only local artifact inspection and failure classification. |

## Validation order

1. Run `CI - Python Quality Gate`.
2. Run `Manual - Python Debug` with `target_environment=development`, `diagnostic_level=repository`.
3. Run `Manual - Python Run Script` with `script_name=hello_control_plane`, `target_environment=development`, `run_mode=read_only`.
4. Run `Manual - Python Inspect Artifacts` with `target_environment=development`, `inspection_mode=sample`.

## Out of scope

- Production writes.
- Staging writes.
- External system writes.
- Secrets-consuming Python scripts.
- Arbitrary command execution.
- Deployment workflows.
- Modifying project data outside this repository.
