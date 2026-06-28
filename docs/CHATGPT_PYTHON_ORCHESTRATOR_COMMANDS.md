# ChatGPT Python Orchestrator Commands — 14:35, 28.06.2026

## Command: Python: run quality gate instructions

Use when the user wants baseline Python validation.

Action for ChatGPT:

1. Instruct the user to review `CI - Python Quality Gate` in `nanotech-solutions-norway/Phyton`.
2. If failed, request the GitHub Actions log ZIP or relevant artifact.
3. Do not propose code changes until logs or artifacts have been inspected.

Expected result:

- Workflow succeeds.
- Artifact `python-quality-test-results` is available.

## Command: Python: run full validation

Use for default validation after Phase 5.

Action for ChatGPT:

1. Use `CI - Python Full Validation` as the primary validation workflow.
2. Review `python-full-validation-artifacts` after completion.
3. If failed, inspect the workflow log ZIP and uploaded artifacts before patching.

Expected result:

- Workflow succeeds.
- Artifact `python-full-validation-artifacts` is available.

## Command: Python: run registered script

Use when the user wants to run a repository-registered Python script.

Action for ChatGPT:

1. Confirm the script exists in the documented registry.
2. Instruct the user to run `Manual - Python Run Script` if manual execution is needed.
3. Select one registered script key.
4. Select `target_environment=development`.
5. Select `run_mode=read_only`.
6. Inspect `python-script-output` after completion.

Current registered script keys:

- `hello_control_plane`
- `repository_inventory`
- `workflow_inventory`
- `dependency_inventory`
- `repository_health_report`

## Command: Python: debug failed run

Use when any Python workflow fails.

Action for ChatGPT:

1. Request the failed workflow log ZIP or uploaded artifacts.
2. Run `Manual - Python Debug` with `target_environment=development` if additional diagnostics are needed.
3. Start with `diagnostic_level=baseline`.
4. Escalate to `diagnostic_level=dependencies` or `diagnostic_level=repository` only when needed.
5. Patch only the smallest isolated layer after evidence is reviewed.

Expected result:

- Artifact `python-debug-artifacts` is available.
- No secrets are printed.

## Command: Python: inspect artifacts

Use when the user wants a local artifact inspection report or validation support.

Action for ChatGPT:

1. Use `CI - Python Full Validation` artifact inspection output when available.
2. For manual fallback, run `Manual - Python Inspect Artifacts`.
3. Select `target_environment=development`.
4. Select `inspection_mode=sample` for baseline validation.
5. If the report indicates `attention_required`, inspect the generated Markdown/JSON report before patching.

Expected result:

- Workflow succeeds.
- Artifact contains `inspection-report.json`, `inspection-report.md`, `pytest-stdout.txt`, and `pytest-exit-code.txt`.

## Command: Python: validate registry

Use when the user wants to validate registered Python scripts, workflow choices, or registry state.

Action for ChatGPT:

1. Prefer the registry validation result inside `CI - Python Full Validation`.
2. For manual fallback, run `Manual - Python Validate Registry`.
3. Select `target_environment=development`.
4. If the report status is `failed`, inspect `registry-validation-report.json` before patching.

Expected result:

- Workflow succeeds.
- Artifact contains `registry-validation-report.json`, `registry-validation-report.md`, and `stdout.txt`.

## Command: Python: inspect Python workflow logs

Use when the user uploads a GitHub Actions log ZIP.

Action for ChatGPT:

1. Read the log ZIP.
2. Identify failing workflow, job, and step.
3. Separate dependency failures, syntax/import failures, lint/format failures, mypy failures, pytest failures, workflow configuration failures, and policy guardrail failures.
4. Recommend one minimal patch or a no-change rerun if the issue is transient.
5. Provide the next validation sequence.

## Command: Python: add new registered script

Use when the user wants a new Python script added to the registry.

Action for ChatGPT:

1. Copy `python/templates/approved_script_template.py` into `python/scripts/` with a new script name.
2. Replace `SCRIPT_NAME` in the copied script.
3. Add tests under `python/tests/`.
4. Add the script to `SCRIPT_ALLOWLIST` in `python/tools/script_allowlist.py`.
5. Add the same script key to the `manual-python-run-script.yml` workflow_dispatch choices.
6. Keep the script development-only unless a later approved phase adds stronger gates.
7. Run the full validation sequence, including registry validation.

Minimum validation:

1. `CI - Python Quality Gate`
2. `CI - Python Full Validation`
3. `Manual - Python Validate Registry` when manual confirmation is needed.

## Command: Python: continue next safe phase

Use when the current phase has passed all validations.

Action for ChatGPT:

1. Review current artifacts and latest workflow status.
2. Confirm no production write capability was introduced.
3. Propose or deploy the smallest next phase.
4. Keep write-capable Python operations deferred unless explicitly approved.
5. Use `CI - Python Full Validation` as the default validation route.

## Phase 5 validation order

Default validation:

1. `CI - Python Full Validation`

Manual fallback validation:

1. `CI - Python Quality Gate`
2. `Manual - Python Debug`
   - `target_environment=development`
   - `diagnostic_level=repository`
3. `Manual - Python Run Script`
   - `script_name=repository_health_report`
   - `target_environment=development`
   - `run_mode=read_only`
4. `Manual - Python Inspect Artifacts`
   - `target_environment=development`
   - `inspection_mode=sample`
5. `Manual - Python Validate Registry`
   - `target_environment=development`

## Cross-repository validation note

If Python orchestration is being used alongside the PowerShell control plane, validate `nanotech-solutions-norway/Powershell-` separately with `CI - PowerShell Quality Gate`. Do not place Python workflows back into the PowerShell repository.

## Failure rule

When a Python workflow fails, ChatGPT must inspect the GitHub Actions log ZIP or uploaded artifact before proposing a repository patch.
