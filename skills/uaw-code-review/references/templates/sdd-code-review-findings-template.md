# SDD Code Review Findings

> Immutable first-pass findings for one frozen SDD2 implementation scope. Fix status belongs in `auto-fix-summary.md`.

## 1. Review Identity

- Entry Mode: `SDD_TASK_CODE_REVIEW`
- Feature ID:
- Attempt:
- Review Time:
- Reviewer Role: AI code reviewer
- Conclusion: passed / failed / blocked
- Unit tests required: yes

## 2. Frozen Scope Evidence

- Repository:
- Branch:
- Base Commit:
- Head Commit:
- Head Tree:
- Scope Snapshot SHA-256:
- Spec Revision / SHA-256:
- Design Revision / SHA-256:
- Tasks Revision / SHA-256:

| Changed file | Frozen SHA-256 / deleted | Reviewed | Notes |
|---|---|---|---|
|  |  | yes / blocked |  |

## 3. Preconditions

| Check | Result | Evidence |
|---|---|---|
| SDD2 control validation | checked-pass / blocked |  |
| Current Spec/Design/Tasks approvals | checked-pass / blocked |  |
| Required Phase Reviews | checked-pass / blocked |  |
| Frozen scope current and allowed | checked-pass / blocked |  |
| Artifact hashes current | checked-pass / blocked |  |

## 4. Mandatory Review Categories

| Category | Result | Evidence / finding IDs |
|---|---|---|
| Scope and traceability | checked-pass / checked-finding / blocked |  |
| Correctness | checked-pass / checked-finding / blocked |  |
| Compatibility | checked-pass / checked-finding / blocked |  |
| Security | checked-pass / checked-finding / blocked |  |
| Transactions and concurrency | checked-pass / checked-finding / blocked |  |
| Integration | checked-pass / checked-finding / blocked |  |
| Persistence | checked-pass / checked-finding / blocked |  |
| Maintainability | checked-pass / checked-finding / blocked |  |
| Observability | checked-pass / checked-finding / blocked |  |
| Tests | checked-pass / checked-finding / blocked |  |

No row may remain unresolved when recording a `passed` or `failed` conclusion.

## 5. Findings

| ID | Severity | Blocking | Path | Symbol / diff location | SDD/rule evidence | Problem and consequence | Required fix |
|---|---|---|---|---|---|---|---|
| CR-001 | P0 / P1 / P2 | yes / no |  |  |  |  |  |

If none: `No actionable findings on the frozen scope.`

## 6. Requirement And Test Impact

| Requirement / acceptance | Production symbol | Existing/required test source | Missing scenario / regression risk |
|---|---|---|---|
|  |  |  |  |

## 7. Auto-fix Handoff

- Findings count: P0= / P1= / P2= / blocking P2=
- Auto-fix required: yes / no-fix-record-required
- Highest-priority finding:
- Scope-changing fix expected: yes / no
- Next artifact: `./auto-fix-summary.md`

Even when no code fix is required, `auto-fix-summary.md` must record `not-required` with evidence.

## 8. Limitations

| Limitation | Impact | Blocking | Recovery |
|---|---|---|---|
|  |  | yes / no |  |

## 9. Gate Record

- Findings Artifact SHA-256:
- Scope Snapshot SHA-256:
- Gate Result: passed / failed / blocked
- Reproducible Evidence:
- Archive Allowed: no; later SDD2 gates remain mandatory

After recording this artifact, do not edit it to reflect fixes. Return control to `uaw-sdd-ai-coding`.
