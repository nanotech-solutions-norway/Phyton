# Phase 3 — Controlled Python Script Expansion — 15:45, 27.06.2026

## Purpose

Phase 3 adds a controlled process for expanding registered Python scripts in `nanotech-solutions-norway/Phyton`.

The phase keeps execution development-only and read-only by default. It adds a script template, a registry validator, synchronization tests, and a manual registry validation workflow.

## Added components

| File | Purpose |
|---|---|
| `python/templates/approved_script_template.py` | Template for future registered scripts. |
| `python/tools/validate_script_registry.py` | Validates script registry, script paths, and workflow choices. |
| `python/tests/test_script_registry_sync.py` | Tests registry/workflow synchronization. |
| `.github/workflows/manual-python-validate-registry.yml` | Manual registry validation workflow. |

## Registry rule

A Python script is executable through GitHub Actions only when all of the following are true:

1. The script exists under `python/scripts/`.
2. The script is listed in `SCRIPT_ALLOWLIST` in `python/tools/script_allowlist.py`.
3. The same script key exists in `.github/workflows/manual-python-run-script.yml` under `workflow_dispatch.inputs.script_name.options`.
4. The selected script key contains no path tokens.
5. The resolved script path remains under `python/scripts/`.
6. The full Python quality gate passes.
7. The registry validation workflow passes.

## Current registered script

```text
hello_control_plane
```

No new executable scripts are added in Phase 3. Phase 3 adds only the expansion mechanism and validation guardrails.

## Manual workflow

Workflow:

```text
Manual - Python Validate Registry
```

Input:

```text
target_environment=development
```

Expected artifact:

```text
python-registry-validation-report
```

Expected files:

```text
registry-validation-report.json
registry-validation-report.md
stdout.txt
```

## Validation behavior

The registry validator checks:

- allowlist is non-empty;
- script keys are non-empty and contain no path tokens;
- registered paths start with `python/scripts/`;
- registered paths resolve inside `python/scripts/`;
- registered paths point to `.py` files;
- registered script files exist;
- workflow `script_name` options exactly match `SCRIPT_ALLOWLIST`;
- workflow default script exists in `SCRIPT_ALLOWLIST`.

## Security posture

Phase 3 remains:

- development-only;
- read-only by default;
- no production writes;
- no staging writes;
- no external system writes;
- no arbitrary command execution;
- no secrets-consuming scripts.

## Adding a future registered script

1. Copy `python/templates/approved_script_template.py` into `python/scripts/` with a new script name.
2. Replace `SCRIPT_NAME` in the copied script.
3. Add unit tests under `python/tests/`.
4. Add the script key and path to `SCRIPT_ALLOWLIST`.
5. Add the same script key to `.github/workflows/manual-python-run-script.yml`.
6. Run the full validation sequence.

## Phase 3 validation sequence

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
5. `Manual - Python Validate Registry`
   - `target_environment=development`

## Failure handling rule

If any Phase 3 workflow fails, inspect the GitHub Actions log ZIP and uploaded artifacts before patching.
