# GitHub Notification Triage SOP — 00:56, 02.07.2026

## Purpose

Use Gmail notifications as an early-warning channel for GitHub Actions failures after repository changes.

## Scope

Repository: `nanotech-solutions-norway/Phyton`

This SOP applies after completing a new GitHub Actions change or validation-triggering repository update.

## Procedure

1. After the final pushed commit, allow a 3-minute notification grace period.
2. Search Gmail for recent GitHub notification messages from `notifications@github.com` related to this repository.
3. Open the relevant notification email and extract the workflow-run link or run ID.
4. Use the notification only to locate the workflow run.
5. Use GitHub Actions job steps, logs, and uploaded artifacts as the source of truth.
6. Patch only the smallest evidence-backed issue.
7. Revalidate with:
   - `CI - Python Quality Gate`
   - `CI - Python Full Validation`

## Boundary

This SOP does not authorize production writes, staging writes, external system writes, arbitrary command execution, or secrets-consuming scripts.
