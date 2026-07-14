# SDD2.0 Internal Operator Control

`sdd2-control-contract.md` is authoritative. This file maps normal workflow actions to the internal deterministic CLI. These commands are run by the Skill, never by the developer.

Set once while operating the Skill:

```bash
CONTROL=skills/uaw-sdd-ai-coding/scripts/sdd2_control.py
```

## Command Map

| Workflow action | Internal command |
|---|---|
| Initialize after Brief persistence | `python3 "$CONTROL" init --feature-dir <dir> --feature-id <id> --mode real` |
| Resume/current-state check | `python3 "$CONTROL" resume --feature-dir <dir>` |
| Record changed public artifact | `python3 "$CONTROL" record-artifact --feature-dir <dir> --stage <stage>` |
| Persist explicit current approval | `python3 "$CONTROL" approve --feature-dir <dir> --stage <stage> --source user-message --approver-role human --approval-text <exact-message> --message-id <id-if-available>` |
| Capture clean implementation scope | `python3 "$CONTROL" capture-scope --feature-dir <dir> --allowed-path <pattern> --forbidden-path <pattern> --required-phase <phase> --test-path <pattern>` |
| Record Phase Review | `python3 "$CONTROL" phase-review --feature-dir <dir> --phase <phase> --approval-text <exact-message> --message-id <id-if-available>` |
| Freeze current code/test scope | `python3 "$CONTROL" freeze-scope --feature-dir <dir>` |
| Record quality gate | `python3 "$CONTROL" quality-gate --feature-dir <dir> --gate <code-review|auto-fix|unit-test> --result <result> --evidence <reproducible-evidence>` |
| Prepare immutable Archive evidence | `python3 "$CONTROL" prepare-archive --feature-dir <dir>` |
| Check Archive eligibility | `python3 "$CONTROL" archive-check --feature-dir <dir> --require-archive` |
| Validate all controls | `python3 "$CONTROL" validate --feature-dir <dir>` |
| Explicit failed-flow closure | `python3 "$CONTROL" close --feature-dir <dir> --result <closed-with-risk|aborted> --approval-text <exact-message>` |
| Explicit new attempt | `python3 "$CONTROL" restart-attempt --feature-dir <dir> --approval-text <exact-message>` |

Repeat `--allowed-path`, `--forbidden-path`, `--required-phase`, and `--test-path` as needed. Patterns must be narrow; `*`, `**`, repository root, and absolute paths are rejected.

Use `--non-production-change` only when the approved Tasks contain no production-code change. Record the justification in Design and Tasks. It must not be used to bypass test-source requirements.

## Approval Handling

Do not execute `approve` from the same assistant turn that generated the gate artifact. Wait for a new user message. Pass the exact approval text without rewriting it. If the platform exposes a stable message ID, record it; otherwise leave it absent and retain timestamp, exact text, artifact revision, artifact hash, and approval hash-chain evidence.

For an explicitly authorized demo only:

1. initialize with `--mode demo`;
2. persist the separate current user authorization with `authorize-demo`;
3. use `source=demo-simulation` and `approver-role=ai-as-human-reviewer`;
4. label every output as simulation evidence, not human approval.

## Error Handling

Exit code meanings:

- `0`: action succeeded and returned current structured result.
- `1`: validation/check completed and found blocking errors.
- `2`: command or transition was rejected.

For `1` or `2`, stop. Preserve the returned error, update the human-readable artifact status only as a projection of `.sdd2/feature-state.json`, and follow `resume.next_required_action`. Never edit control JSON/JSONL by hand.

## Recovery Rules

- Missing/mismatched lock: resume may reacquire only when no other feature owns the worktree; otherwise use another worktree.
- Scope drift: freeze the new snapshot, then rerun Code Review, Auto-fix closure, Unit Test, Unit Test Summary approval, and Archive evidence as invalidated.
- Artifact drift: record the changed artifact, then repeat all invalidated downstream actions.
- Hash-chain corruption: stop and retain evidence; do not repair or rewrite history automatically.
- Failed/blocked test: fix and rerun on current scope, or obtain explicit user risk closure/abort. Never complete Archive.
- Interrupted session: call `resume`; do not infer state from conversation history.
- Repeated execution: use `restart-attempt` only after a new explicit user retry/restart message.

## Historical Examples

Use `migrate-legacy` once to quarantine pre-control examples. It records existing artifacts as historical, stores no fabricated approvals, marks the state `superseded`, and disables resume/progression.
