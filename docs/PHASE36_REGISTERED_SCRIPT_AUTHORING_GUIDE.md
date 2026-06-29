# Phase 36 — Registered Script Authoring Guide — 19:18, 29.06.2026

## Purpose

Phase 36 documents the required pattern for adding future registered Python scripts safely.

This phase is documentation-only. It does not add scripts, workflows, dependencies, permissions, secrets, deployment behavior, staging writes, production writes, external system writes, or arbitrary command execution.

## Repository

```text
nanotech-solutions-norway/Phyton
```

## Authoring principle

A registered script is a repository-local Python entrypoint that can be selected through a fixed allowlist. It is not a free-form command runner.

Future scripts must be:

```text
development-only
read-only by default
repository-local
non-secret-consuming
non-deploying
non-destructive
selected from a fixed allowlist
validated by CI before use
```

## Required file pattern

A future script expansion should normally include:

```text
python/scripts/<script_key>.py
python/tests/test_<script_key>.py
```

If a helper is needed, it should live under:

```text
python/tools/
```

The registered script key must be added only through the repository's fixed allowlist mechanism. It must not introduce arbitrary shell input.

## Required script behavior

Each new registered script must:

1. run without secrets;
2. avoid network writes;
3. avoid filesystem writes outside approved artifact/report outputs;
4. avoid modifying project data outside this repository;
5. emit deterministic report output where practical;
6. fail clearly with actionable error messages;
7. support CI validation through pytest;
8. remain compatible with the existing GitHub Actions runner model.

## Required test coverage

Each new registered script should include tests for:

- importability;
- deterministic output shape;
- expected report headings or keys;
- safe failure behavior;
- absence of unsafe free-form command handling;
- consistency with the allowlist and manual workflow choices where relevant.

## Required documentation

Each future script expansion should include a short phase note documenting:

```text
script key
purpose
inputs
outputs
artifact names, if any
validation workflow
explicit non-goals
```

The phase note must state whether the script is read-only, whether it consumes secrets, and whether it writes outside the repository-local reporting scope.

## Disallowed patterns

Do not add scripts that:

- accept arbitrary shell commands;
- print secrets or environment dumps;
- deploy code;
- write to staging or production systems;
- write to external APIs;
- depend on local machine state outside the GitHub Actions runner;
- bypass the fixed allowlist;
- require hidden manual setup that is not documented.

## Review checklist before adding a script

Before a new registered script is accepted, confirm:

1. the script key is explicit and stable;
2. the operation is read-only or separately approved;
3. inputs are fixed choices, not free-form shell commands;
4. outputs are documented;
5. tests are added;
6. workflows do not gain unnecessary permissions;
7. CI validation passes;
8. failure logs are inspected before any correction patch.

## Recommended next phase

The recommended next phase is:

```text
Phase 37 — Safe Read-Only Script Expansion
```

Phase 37 may add one small repository-local read-only registered script if explicitly validated as safe and useful.

## Validation for this phase

Because Phase 36 is documentation-only, validation is:

1. `CI - Python Quality Gate`
2. `CI - Python Full Validation`

Expected result: both pass.
