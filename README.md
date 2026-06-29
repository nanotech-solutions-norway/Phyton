# Python GitHub Control Plane — 21:20, 28.06.2026

This repository is the separate Python execution, testing, debugging, validation, artifact inspection, failure triage, controlled script expansion, read-only repository intelligence, repository health-report, control-plane readiness, operations handoff, validation evidence index, project instructions, deferred capability roadmap, test coverage, documentation index guardrails, workflow policy guardrails, registered script path guardrails, artifact contract guardrails, workflow trigger guardrails, dependency file guardrails, Python runtime version guardrails, write boundary guardrails, and manual workflow input guardrails layer for NanoTech Solutions Norway projects.

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
- Registry and workflow choices must remain synchronized.
- Full validation now runs automatically on relevant pushes.

## Repository structure

| Path | Purpose |
|---|---|
| `python/scripts/` | Registered Python scripts for manual GitHub Actions execution. |
| `python/templates/` | Templates for future registered scripts. |
| `python/tools/` | Allowlist, runner, diagnostics, artifact inspection, failure classification, and registry validation tools. |
| `python/examples/` | Non-production examples. |
| `python/tests/` | pytest tests and execution guardrails. |
| `python/requirements.txt` | Runtime dependencies. |
| `python/requirements-dev.txt` | Development validation dependencies. |
| `.github/workflows/ci-python-quality.yml` | Python quality gate. |
| `.github/workflows/ci-python-full-validation.yml` | Automatic full validation workflow. |
| `.github/workflows/manual-python-run-script.yml` | Manual registered-script runner. |
| `.github/workflows/manual-python-debug.yml` | Manual debug workflow. |
| `.github/workflows/manual-python-inspect-artifacts.yml` | Manual artifact inspection and failure triage workflow. |
| `.github/workflows/manual-python-validate-registry.yml` | Manual registry synchronization validation workflow. |
| `docs/PYTHON_CONTROL_PLANE.md` | Control-plane specification. |
| `docs/CHATGPT_PYTHON_ORCHESTRATOR_COMMANDS.md` | ChatGPT orchestration commands. |
| `docs/PHASE2_ARTIFACT_INSPECTION_AND_FAILURE_TRIAGE.md` | Phase 2 artifact inspection and triage specification. |
| `docs/PHASE3_CONTROLLED_SCRIPT_EXPANSION.md` | Phase 3 controlled script expansion specification. |
| `docs/PHASE4_READ_ONLY_REPOSITORY_INTELLIGENCE.md` | Phase 4 repository intelligence specification. |
| `docs/PHASE5_REPOSITORY_HEALTH_REPORT.md` | Phase 5 repository health report specification. |
| `docs/PHASE6_CONTROL_PLANE_READINESS.md` | Phase 6 control-plane readiness specification. |
| `docs/PHASE7_OPERATIONS_HANDOFF.md` | Phase 7 operations handoff pack. |
| `docs/PHASE8_VALIDATION_EVIDENCE_INDEX.md` | Phase 8 validation evidence index. |
| `docs/PHASE9_PROJECT_INSTRUCTIONS_PACK.md` | Phase 9 project instructions pack. |
| `docs/PHASE10_DEFERRED_CAPABILITY_ROADMAP.md` | Phase 10 deferred capability roadmap. |
| `python/tests/test_control_plane_readiness.py` | Phase 11 readiness helper test coverage. |
| `python/tests/test_documentation_index.py` | Phase 12 documentation index guardrail tests. |
| `python/tests/test_workflow_policy.py` | Phase 13 workflow policy guardrail tests. |
| `python/tests/test_script_path_policy.py` | Phase 14 registered script path guardrail tests. |
| `python/tests/test_artifact_contract.py` | Phase 15 artifact contract guardrail tests. |
| `python/tests/test_workflow_triggers.py` | Phase 16 workflow trigger guardrail tests. |
| `python/tests/test_dependency_policy.py` | Phase 17 dependency file guardrail tests. |
| `python/tests/test_python_runtime_policy.py` | Phase 18 Python runtime version guardrail tests. |
| `python/tests/test_write_boundary_policy.py` | Phase 19 write boundary guardrail tests. |
| `python/tests/test_manual_workflow_inputs.py` | Phase 20 manual workflow input guardrail tests. |

## Workflows

| Workflow | Purpose |
|---|---|
| `CI - Python Quality Gate` | Ruff format check, Ruff lint, mypy, pytest. |
| `CI - Python Full Validation` | Automatic full validation, registered script runs, artifact inspection, registry validation. |
| `Manual - Python Debug` | Sanitized Python diagnostics and artifact upload. |
| `Manual - Python Run Script` | Development-only registered Python script execution. |
| `Manual - Python Inspect Artifacts` | Read-only local artifact inspection and failure classification. |
| `Manual - Python Validate Registry` | Validate allowlist and workflow script choices stay synchronized. |

## Registered scripts

| Script key | Purpose |
|---|---|
| `hello_control_plane` | Foundation validation script. |
| `repository_inventory` | Repository file inventory report. |
| `workflow_inventory` | GitHub Actions workflow inventory report. |
| `dependency_inventory` | Python dependency file inventory report. |
| `repository_health_report` | Consolidated repository health report. |
| `control_plane_readiness` | Control-plane readiness report. |

## Validation order

Default validation now runs through `CI - Python Full Validation` on relevant pushes.

Manual fallback validation:

1. Run `CI - Python Quality Gate`.
2. Run `CI - Python Full Validation`.
3. Run `Manual - Python Debug` with `target_environment=development`, `diagnostic_level=repository`.
4. Run `Manual - Python Run Script` with `script_name=repository_health_report`, `target_environment=development`, `run_mode=read_only`.
5. Run `Manual - Python Run Script` with `script_name=control_plane_readiness`, `target_environment=development`, `run_mode=read_only`.
6. Run `Manual - Python Inspect Artifacts` with `target_environment=development`, `inspection_mode=sample`.
7. Run `Manual - Python Validate Registry` with `target_environment=development`.

## Out of scope

- Production writes.
- Staging writes.
- External system writes.
- Secrets-consuming Python scripts.
- Arbitrary command execution.
- Deployment workflows.
- Modifying project data outside this repository.
