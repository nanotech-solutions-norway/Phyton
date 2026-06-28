# Phase 9 — Project Instructions Pack — 17:05, 28.06.2026

## Purpose

Phase 9 adds a documentation-only ChatGPT Project instruction pack for the Python control plane.

This phase does not add scripts, workflows, dependencies, permissions, secrets, deployment behavior, or write/live capability.

## Repository

```text
nanotech-solutions-norway/Phyton
```

## Instruction block for ChatGPT Project settings

Paste the following block into the ChatGPT Project instructions field for Python control-plane work:

```text
Python Control Plane Project Instructions

Repository:
nanotech-solutions-norway/Phyton

Use the repository as the source of truth. Do not assume local Python, local PowerShell, or Android-local runtime access. Prefer GitHub Actions workflows, committed scripts, committed documentation, workflow logs, uploaded artifacts, and tests.

Operating posture:
- development-only
- read-only
- repository-local
- fixed registered-script choices only
- no arbitrary shell command input
- no production writes
- no staging writes
- no external system writes
- no secrets-consuming scripts
- no deployment behavior
- failed workflow logs and artifacts must be inspected before patching

Current baseline workflows:
- CI - Python Quality Gate
- CI - Python Full Validation
- Manual - Python Debug
- Manual - Python Run Script
- Manual - Python Inspect Artifacts
- Manual - Python Validate Registry

Current registered scripts:
- hello_control_plane
- repository_inventory
- workflow_inventory
- dependency_inventory
- repository_health_report
- control_plane_readiness

Default validation route:
1. CI - Python Quality Gate
2. CI - Python Full Validation

Manual fallback validation route:
1. Manual - Python Run Script with script_name=repository_health_report, target_environment=development, run_mode=read_only
2. Manual - Python Run Script with script_name=control_plane_readiness, target_environment=development, run_mode=read_only
3. Manual - Python Validate Registry with target_environment=development

Failure handling:
- Inspect the GitHub Actions log ZIP first.
- Inspect uploaded artifacts when available.
- Identify workflow, job, and failing step.
- Classify the failure before patching.
- Patch only the smallest affected file or workflow layer.
- If Ruff format fails, apply a formatting-only patch.
- If registry validation fails, synchronize SCRIPT_ALLOWLIST and manual workflow choices.
- Re-run the failed workflow and CI - Python Full Validation after patching.

Do not add write/live capability unless the user explicitly approves a new phase for that capability.
```

## Useful repository documents

| Document | Purpose |
|---|---|
| `README.md` | Repository index and current validation order. |
| `docs/PYTHON_CONTROL_PLANE.md` | Control-plane policy and workflow overview. |
| `docs/CHATGPT_PYTHON_ORCHESTRATOR_COMMANDS.md` | Operational command reference. |
| `docs/PHASE7_OPERATIONS_HANDOFF.md` | Handoff pack for new chat threads. |
| `docs/PHASE8_VALIDATION_EVIDENCE_INDEX.md` | Evidence model, failure categories, and patch discipline. |

## Validation for this phase

Because Phase 9 is documentation-only, validation is:

1. `CI - Python Quality Gate`
2. `CI - Python Full Validation`

Expected result: both pass.
