# Review-Driven Auto-fix Summary

> Records dispositions and fixes without rewriting the original Code Review findings.

## 1. Identity And Scope

- Feature ID:
- Attempt:
- Code Review Findings Revision / SHA-256:
- Reviewed Scope SHA-256:
- Code Revision Before Auto-fix:
- Code Revision After Auto-fix:
- Auto-fix Result: passed / not-required / failed / blocked

## 2. Findings Disposition

| Finding ID | Severity | Original location | Disposition | Changed files/symbols | Fix description | Verification | Residual risk |
|---|---|---|---|---|---|---|---|
| CR-001 | P0/P1/P2 |  | fixed / accepted-risk / rejected-with-evidence / blocked |  |  |  |  |

Do not delete, reword, or mark resolved inside `code-review-findings.md`. This table is the only disposition record.

## 3. Scope Change

- Production/test/config changed: yes / no
- New Frozen Scope SHA-256:
- Full Code Review rerun required: yes / no
- Full Code Review rerun result/evidence:

Any code, test, configuration, Design, or Tasks change requires a new scope freeze and full Code Review. A targeted spot-check cannot replace it.

## 4. No-Fix Path

Complete only when result is `not-required`:

- Findings count by severity:
- Why no code change is required:
- Evidence that Code Review passed on the current scope:

## 5. Validation

| Check | Method / command | Environment | Exit/result | Evidence |
|---|---|---|---|---|
| Build/static check |  |  |  |  |
| Finding-specific verification |  |  |  |  |

## 6. Remaining Items

| ID | Owner | Reason unresolved | Blocking | Required next action |
|---|---|---|---|---|
|  |  |  | yes / no |  |

P0, P1, and explicitly blocking P2 items must be closed before Unit Test. Risk acceptance does not convert a failed Code Review into a passed gate without the required current human decision and process state.

## 7. Unit Test Handoff

- Current Scope SHA-256:
- Production symbols changed:
- Required test targets/scenarios:
- Regression risks from fixes:
- Unit Test allowed: yes / no

## 8. Control Projection

- State Authority: `./.sdd2/feature-state.json`
- Attempt:
- Control Revision:
- Current Stage: auto-fix
- Stage Status:
- Next Required Action:
- Artifact Revision / SHA-256:

This artifact is a quality-gate record, not human stage approval.
