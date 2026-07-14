---
name: uaw-code-review
description: "Review UAW changes in one of three explicit modes: SDD_TASK_CODE_REVIEW with fixed SDD2 scope and Markdown findings, standalone Git range review with HTML reports, or standalone worktree snapshot review with HTML reports. Use for SDD2 automatic review or direct branch, commit, date-range, project, directory, or uncommitted-code review requests."
---

# UAW Code Review

## Select Exactly One Mode

- `SDD_TASK_CODE_REVIEW`: invoked by `uaw-sdd-ai-coding`; output only `code-review-findings.md`.
- `STANDALONE_GIT_RANGE_REVIEW`: direct user request with an explicit Git range; output HTML summary and developer reports.
- `STANDALONE_WORKTREE_SNAPSHOT_REVIEW`: direct user request for a directory/uncommitted snapshot; output HTML reports labeled non-merge-gate snapshot.

Read `references/code-review-rules.md` and follow the selected mode. Never mix inputs, gates, or outputs across modes.

## SDD Mode

Require all of the following from SDD context:

- Feature directory and `.sdd2/feature-state.json`;
- current approved `spec.md`, `design.md`, and `tasks.md`;
- all required human Phase Reviews;
- `.sdd2/implementation-scope.json` with a current frozen snapshot;
- exact changed-file manifest and output path.

Run the SDD2 control validator before review. Use only the frozen manifest and hashes as implementation scope; never infer it from upstream drift, `git status`, or the feature directory. Missing/stale input is `blocked`, not a reason to downgrade to standalone mode.

Do not read HTML templates, create `reports/code-review`, fix code, or generate test/Archive content. Write immutable first-pass findings using `references/templates/sdd-code-review-findings-template.md`, then return control to `uaw-sdd-ai-coding` for Auto-fix.

Every mandatory review category must contain evidence. Production changes always require unit-test source work downstream.

## Standalone Modes

Read `references/input-examples.md`. Ask only for required missing scope fields.

Git range mode freezes base/head commit IDs and a diff hash before review. Worktree mode freezes HEAD, target path, changed/untracked file hashes, and a snapshot hash. Do not silently expand either scope.

Generate reports from:

- `references/templates/summary-report-template.html`
- `references/templates/personal-report-template.html`

Standalone review does not execute SDD gates and never auto-fixes code unless the user separately requests implementation.

## References

- `references/code-review-rules.md`: authoritative review modes, scope capture, checks, severity, and conclusions.
- `references/input-examples.md`: standalone input structures.
- `references/templates/sdd-code-review-findings-template.md`: SDD-only Markdown output.
- `references/templates/standalone-review-input-template.md`: standalone scope normalization.
- HTML templates: standalone outputs only.
