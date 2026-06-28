# Phase 8 — Validation Evidence Index — 16:55, 28.06.2026

## Purpose

Phase 8 adds a documentation-only validation evidence index for the Python control plane.

This phase does not add scripts, workflows, dependencies, permissions, secrets, deployment behavior, or write/live capability.

## Repository

```text
nanotech-solutions-norway/Phyton
```

## Evidence model

Validation evidence should be reviewed in this order:

1. GitHub Actions workflow result.
2. Failed step name, if any.
3. GitHub Actions log ZIP.
4. Uploaded workflow artifact ZIP.
5. Committed source file or workflow file.
6. Smallest evidence-backed patch.
7. Re-run of the failed workflow and full validation.

## Primary workflow evidence

| Workflow | Evidence artifact | Purpose |
|---|---|---|
| `CI - Python Quality Gate` | `python-quality-test-results` | Ruff format, Ruff lint, mypy, pytest. |
| `CI - Python Full Validation` | `python-full-validation-artifacts` | Full validation chain, script outputs, artifact inspection, registry validation. |
| `Manual - Python Debug` | `python-debug-artifacts` | Sanitized diagnostic evidence. |
| `Manual - Python Run Script` | `python-script-output` | Output from a selected registered script. |
| `Manual - Python Inspect Artifacts` | `python-artifact-inspection-report` | Local artifact inspection and failure classification. |
| `Manual - Python Validate Registry` | `python-registry-validation-report` | Allowlist and workflow-choice synchronization. |

## Current validated baseline

The current expected baseline is:

```text
CI - Python Quality Gate = Working
CI - Python Full Validation = Working
Manual - Python Debug = Working
Manual - Python Run Script = Working
Manual - Python Inspect Artifacts = Working
Manual - Python Validate Registry = Working
Manual - Python Run Script with script_name=control_plane_readiness = Working
```

## Current registered scripts

```text
hello_control_plane
repository_inventory
workflow_inventory
dependency_inventory
repository_health_report
control_plane_readiness
```

## Failure categories

When a failure occurs, classify it before patching:

| Category | Typical signal | Expected action |
|---|---|---|
| Ruff format | `Would reformat` | Apply formatting-only patch. |
| Ruff lint | `ruff check` reports code issue | Patch smallest lint issue. |
| mypy | typing validation fails | Patch type annotation or typing flow. |
| pytest | test failure or assertion failure | Inspect failing test and patch behavior or test fixture. |
| workflow filesystem | `No such file or directory` from `tee`, upload, or artifact step | Patch workflow directory creation or artifact path. |
| registry mismatch | `Manual - Python Validate Registry` fails | Sync `SCRIPT_ALLOWLIST` and workflow choices. |
| policy guardrail | non-development or non-read-only execution rejected | Preserve guardrail and correct caller inputs. |

## Patch discipline

Patch rules:

- do not patch without log or artifact evidence;
- patch the smallest affected file;
- prefer formatting-only fixes when the log identifies Ruff format only;
- do not broaden workflow permissions;
- do not add secrets;
- do not add production or staging writes;
- do not introduce arbitrary shell command inputs;
- re-run the failed workflow and `CI - Python Full Validation` after patching.

## Evidence retention

For each completed phase, retain:

- phase document;
- README index entry;
- relevant script registration entry, if a script was added;
- workflow artifact name;
- validation result stated by the user;
- failed log ZIPs when applicable;
- minimal patch commit references.

## Validation for this phase

Because Phase 8 is documentation-only, validation is:

1. `CI - Python Quality Gate`
2. `CI - Python Full Validation`

Expected result: both pass.
