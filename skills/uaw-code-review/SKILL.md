---
name: uaw-code-review
description: Review UAW code changes in standalone HTML report mode or SDD findings mode. Use when the user asks for code review, branch diff review, commit/date range review, worktree snapshot review, project code audit, or when the SDD AI coding skill automatically triggers SDD_TASK_CODE_REVIEW after tasks implementation.
---

# UAW Code Review

## Core Contract

This skill performs UAW code review in two operating families:

- Standalone mode: the user requests code review directly and provides Git range or worktree snapshot input. The output is HTML reports.
- SDD mode: `uaw-sdd-ai-coding` invokes this skill after tasks implementation. The output is `code-review-findings.md`.

Read `references/input-examples.md` before requesting standalone input. The examples define the expected standalone review input structures.

## Mode Selection

Use `SDD_TASK_CODE_REVIEW` when invoked from SDD context and the feature directory contains or provides equivalent access to:

- `proposal-input.md`
- `spec.md`
- `design.md`
- `tasks.md`
- implemented code changes

Use `STANDALONE_GIT_RANGE_REVIEW` when the user provides a branch diff, commit list, or date range.

Use `STANDALONE_WORKTREE_SNAPSHOT_REVIEW` when the user only provides a project/module path or asks to review uncommitted/demo code.

If the user asks for standalone review without a Git range or worktree path, ask for the missing fields using `references/input-examples.md`.

## SDD Mode Rules

In SDD mode:

- Entry Mode, Feature Directory, SDD Artifacts, and report output directory are provided by SDD context.
- HTML reports are not generated.
- HTML report templates are not used.
- `reports/code-review/YYYY-MM-DD/` is not created.
- Output only `code-review-findings.md` in the current feature asset directory.
- Return the Findings to `uaw-sdd-ai-coding` for Review-driven Auto-fix.

## Standalone Mode Rules

In standalone mode:

- SDD stage gates are not executed.
- `proposal-input.md`, `spec.md`, `design.md`, and `tasks.md` are optional unless the user explicitly asks to include them.
- Generate `代码评审统计报告.html` and `{开发者姓名}_代码评审报告.html`.
- For worktree snapshot review, mark the report as `Scope Deviation: worktree snapshot, not Git range`.
- Code fixes require a separate explicit fix request.

## References

- `references/input-examples.md`: standalone review input examples.
- `references/code-review-rules.md`: detailed UAW review rules and severity model.
- `references/templates/sdd-code-review-findings-template.md`: SDD findings output template.
- `references/templates/standalone-review-input-template.md`: standalone input source template.
- `references/templates/summary-report-template.html`: standalone summary HTML template.
- `references/templates/personal-report-template.html`: standalone personal HTML template.
