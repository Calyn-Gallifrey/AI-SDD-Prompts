# Feature Specification

> Defines observable behavior and acceptance boundaries. It must not prescribe unapproved implementation details.

## 1. Identity And Sources

- Feature ID:
- Feature Name:
- Module:
- Sprint:
- Priority:
- Proposal Input Revision / SHA-256:
- Current Code Base Commit:
- Spec Revision:

## 2. Goal


## 3. Scope

### In Scope


### Forbidden Changes


### Non-Goals


## 4. Existing Behavior And Delta

| Area | Existing behavior, verified from | Required delta | Compatibility constraint |
|---|---|---|---|
|  |  |  |  |

## 5. Actors And Preconditions

| Actor / caller | Authorization | Preconditions | Entry |
|---|---|---|---|
|  |  |  |  |

## 6. Functional Requirements

| ID | Requirement | Input | Processing rule | Output / side effect | Source |
|---|---|---|---|---|---|
| FR-01 |  |  |  |  | user / code / approved context |

## 7. Data Contract

### Request

| Field | Type | Required | Validation | Meaning | Source |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Response

| Field | Type | Nullability | Meaning | Compatibility |
|---|---|---|---|---|
|  |  |  |  |  |

### Persistence / Message / External Contract

| Contract | Change | Invariant | Migration / compatibility |
|---|---|---|---|
|  |  |  |  |

## 8. Business Rules

| ID | Condition | Required behavior | Error / fallback | Priority |
|---|---|---|---|---|
| BR-01 |  |  |  |  |

## 9. Failure And Boundary Behavior

| Scenario | Expected behavior | Observable response | Logging / audit | Retry / idempotency |
|---|---|---|---|---|
|  |  |  |  |  |

## 10. Security And Compliance

- Authentication/authorization:
- Sensitive data:
- Data access boundary:
- Injection/input risks:
- Audit/logging constraints:

## 11. Non-Functional Requirements

| Category | Requirement | Measurable threshold / evidence |
|---|---|---|
| Performance |  |  |
| Reliability |  |  |
| Compatibility |  |  |
| Observability |  |  |

## 12. Acceptance Criteria

| ID | Given | When | Then | Required evidence |
|---|---|---|---|---|
| AC-01 |  |  |  | unit test / integration evidence / inspection |

Every functional requirement and business rule must map to at least one acceptance criterion.

## 13. Test Intent

| Test class | Required scenarios | Source target | Notes |
|---|---|---|---|
| Unit | happy, boundary, error, compatibility |  | Production changes require changed test source |
| Other, if approved |  |  |  |

## 14. Traceability

| Requirement | Acceptance | Design owner | Planned task | Test evidence |
|---|---|---|---|---|
| FR-01 | AC-01 | pending | pending | pending |

## 15. Risks, Assumptions, Open Questions

| ID | Type | Description | Evidence | Impact | Resolution / owner |
|---|---|---|---|---|---|
|  | risk / assumption / open-question |  |  |  |  |

Unresolved items affecting behavior, scope, data, security, or acceptance block Spec approval.

## 16. Human Review Gate

- Required Approver: current human reviewer
- Approval Source: new user message after this artifact is recorded
- Valid Results: approved / rejected / blocked
- Approval Evidence: `.sdd2/gate-approvals.jsonl`

Stop after generating and recording this file. Do not generate Design until the current Spec revision is explicitly approved.

## 17. Control Projection

- State Authority: `./.sdd2/feature-state.json`
- Attempt:
- Control Revision:
- Current Stage: spec
- Stage Status: awaiting-approval
- Next Required Action: request-spec-approval
- Artifact Revision / SHA-256:

This block mirrors control state; text in this file is not approval.
