# Phase 4 — Read-Only Repository Intelligence — 00:10, 28.06.2026

## Purpose

Phase 4 adds the first practical registered Python inventory scripts to `nanotech-solutions-norway/Phyton`.

The scripts are development-only, repository-local, and report-producing. They do not use secrets, deploy software, or modify project data.

## Added registered scripts

| Script key | File | Purpose |
|---|---|---|
| `repository_inventory` | `python/scripts/repository_inventory.py` | Report repository files, file sizes, extensions, and top-level folders. |
| `workflow_inventory` | `python/scripts/workflow_inventory.py` | Report GitHub Actions workflow names, jobs, and detected triggers. |
| `dependency_inventory` | `python/scripts/dependency_inventory.py` | Report Python runtime and development dependency files. |

## Existing registered script retained

```text
hello_control_plane
```

## Registration model

The Phase 4 scripts are registered in both required control points:

1. `SCRIPT_ALLOWLIST` in `python/tools/script_allowlist.py`.
2. `.github/workflows/manual-python-run-script.yml` under `workflow_dispatch.inputs.script_name.options`.

The Phase 3 registry validator confirms that these remain synchronized.

## Output artifacts

All Phase 4 scripts use:

```text
Manual - Python Run Script
```

Common inputs:

```text
target_environment=development
run_mode=read_only
```

Expected script-specific report files:

| Script key | JSON report | Markdown report |
|---|---|---|
| `repository_inventory` | `repository-inventory.json` | `repository-inventory.md` |
| `workflow_inventory` | `workflow-inventory.json` | `workflow-inventory.md` |
| `dependency_inventory` | `dependency-inventory.json` | `dependency-inventory.md` |

## Tests added

| Test file | Coverage |
|---|---|
| `python/tests/test_repository_inventory.py` | Repository file inventory and excluded-folder behavior. |
| `python/tests/test_workflow_inventory.py` | Workflow name, job count, trigger inference, and inventory collection. |
| `python/tests/test_dependency_inventory.py` | Requirements parsing and dependency inventory collection. |
| `python/tests/test_script_registry_sync.py` | Updated to validate the live allowlist instead of a fixed one-script set. |

## Security posture

Phase 4 remains:

- development-only;
- read-only;
- repository-local;
- no production writes;
- no staging writes;
- no external system writes;
- no secrets-consuming scripts;
- no deployment workflows.

## Validation sequence

1. `CI - Python Quality Gate`
2. `Manual - Python Debug`
   - `target_environment=development`
   - `diagnostic_level=repository`
3. `Manual - Python Run Script`
   - `script_name=hello_control_plane`
   - `target_environment=development`
   - `run_mode=read_only`
4. `Manual - Python Run Script`
   - `script_name=repository_inventory`
   - `target_environment=development`
   - `run_mode=read_only`
5. `Manual - Python Run Script`
   - `script_name=workflow_inventory`
   - `target_environment=development`
   - `run_mode=read_only`
6. `Manual - Python Run Script`
   - `script_name=dependency_inventory`
   - `target_environment=development`
   - `run_mode=read_only`
7. `Manual - Python Inspect Artifacts`
   - `target_environment=development`
   - `inspection_mode=sample`
8. `Manual - Python Validate Registry`
   - `target_environment=development`

## Failure handling rule

If any Phase 4 workflow fails, inspect the GitHub Actions log ZIP and uploaded artifacts before patching.
