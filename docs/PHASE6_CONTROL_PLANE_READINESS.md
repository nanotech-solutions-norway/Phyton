# Phase 6 — Control Plane Readiness — 15:50, 28.06.2026

## Purpose

Phase 6 adds a read-only readiness report for the Python control plane in `nanotech-solutions-norway/Phyton`.

The phase keeps the same operating posture as the previous phases:

- development-only;
- read-only;
- repository-local;
- no production writes;
- no staging writes;
- no external system writes;
- no secrets-consuming scripts.

## Added registered script

| Script key | File | Purpose |
|---|---|---|
| `control_plane_readiness` | `python/scripts/control_plane_readiness.py` | Builds a readiness report from repository health, required docs, required scripts, and manual workflow registration. |

## Output files

When run through `Manual - Python Run Script` with `script_name=control_plane_readiness`, expected files are:

```text
run-summary.json
control-plane-readiness.json
control-plane-readiness.md
stdout.txt
```

## Readiness states

| Status | Meaning |
|---|---|
| `ready` | Repository health is healthy and the required readiness surface is present. |
| `manual_review_required` | Repository health needs review but no readiness finding blocks execution. |
| `attention_required` | A required file, script registration, or workflow choice is missing. |

## Validation sequence

Default validation remains:

1. `CI - Python Quality Gate`
2. `CI - Python Full Validation`

Manual readiness validation:

1. `Manual - Python Run Script`
   - `script_name=control_plane_readiness`
   - `target_environment=development`
   - `run_mode=read_only`
2. `Manual - Python Validate Registry`
   - `target_environment=development`

## Failure handling rule

If any workflow fails, inspect the GitHub Actions log ZIP and uploaded artifacts before patching.
