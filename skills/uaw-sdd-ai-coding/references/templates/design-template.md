# Feature Technical Design

> Converts the approved Spec delta into an implementable design grounded in current code and routed UAW rules.

## 1. Identity And Approved Inputs

- Feature ID:
- Feature Name:
- Module:
- Approved Spec Revision / SHA-256:
- Spec Approval Record Hash:
- Git Baseline Commit:
- Design Revision:

## 2. Design Summary

- Existing architecture:
- Proposed delta:
- Why this is the smallest correct change:
- Preserved behavior:

## 3. Source And Rule Provenance

| Source / rule | Path / symbol | Revision / freshness | Used for | Conflict resolution |
|---|---|---|---|---|
| Current code |  | commit | baseline | current implementation facts win |
| Routed UAW rule |  | runtime version | constraint | control contract wins for process |
| Transaction/context reference |  | verified-at | business context | unresolved conflict blocks |

## 4. Component Delta

| Component | Existing symbol/path | Change | Responsibility after change | Explicitly unchanged |
|---|---|---|---|---|
| Controller / entry |  |  |  |  |
| Service / strategy |  |  |  |  |
| Gateway / adapter |  |  |  |  |
| Persistence |  |  |  |  |
| Model / mapping |  |  |  |  |
| Config / script |  |  |  |  |
| Test |  |  |  |  |

Use `not-applicable` only with a concrete reason tied to the approved Spec.

## 5. Interaction Flow

```text
caller -> entry -> application/service -> gateway/repository -> response
```

Describe ordering, transaction boundaries, retries, idempotency, and failure propagation.

## 6. API And Data Design

### API

| Method/path or entry | Request type | Response type | Authorization | Compatibility |
|---|---|---|---|---|
|  |  |  |  |  |

### Model Mapping

| Source | Target | Mapping method | Null/default rule | Naming rule |
|---|---|---|---|---|
|  |  |  |  |  |

### Persistence / External Integration

| Operation | Boundary | Query/contract | Timeout/retry | Failure mapping |
|---|---|---|---|---|
|  |  |  |  |  |

## 7. Business Rule Placement

| Spec rule | Owning symbol | Why here | Verification |
|---|---|---|---|
| BR-01 |  |  |  |

## 8. Error, Security, And Observability

| Concern | Design | Existing utility/convention | Evidence |
|---|---|---|---|
| Validation |  |  |  |
| Authorization |  |  |  |
| Exception mapping |  |  |  |
| Logging/audit |  |  |  |
| Sensitive data |  |  |  |

## 9. Transaction And Concurrency

- Transaction owner and propagation:
- Lock/concurrency strategy:
- Idempotency key/behavior:
- Partial-failure handling:
- Rollback boundary:

## 10. Migration And Compatibility

- Database/config/script change:
- Rollout order:
- Backward compatibility:
- Rollback plan:
- Data repair, if any:

## 11. Implementation Scope

### Allowed Paths

```text
<narrow path pattern>
```

### Forbidden Paths

```text
<path pattern>
```

### Required Phases

| Phase ID | Purpose | Expected files | Human Phase Review required |
|---|---|---|---|
| Phase1 |  |  | yes |

### Test Path Patterns

```text
<narrow test source pattern>
```

The Skill converts these approved values into `.sdd2/implementation-scope.json`. Repository-wide wildcards are invalid.

## 12. Test Design

| Test target | Profile | Scenarios | Mock boundary | Assertions | Source path |
|---|---|---|---|---|---|
|  | method / service / strategy / controller / static |  |  |  |  |

Production changes require at least one generated or updated test source. Manual verification may supplement but never replace it.

## 13. Review Hotspots

| Risk | Related Spec/Design | Exact review check | Severity if violated |
|---|---|---|---|
|  |  |  |  |

## 14. Traceability

| Spec requirement | Design section/symbol | Planned phase | Test case |
|---|---|---|---|
| FR-01 |  |  |  |

## 15. Alternatives And Decisions

| Decision | Options considered | Selected | Reason | Cost/risk |
|---|---|---|---|---|
|  |  |  |  |  |

## 16. Risks And Open Questions

| ID | Description | Impact | Owner | Must resolve before |
|---|---|---|---|---|
|  |  |  |  | Tasks / implementation |

## 17. Human Review Gate

- Required Approver: current human reviewer
- Approval Evidence: `.sdd2/gate-approvals.jsonl`
- Valid Results: approved / rejected / blocked

Stop after generating and recording this file. Do not generate Tasks until the current Design revision is explicitly approved.

## 18. Control Projection

- State Authority: `./.sdd2/feature-state.json`
- Attempt:
- Control Revision:
- Current Stage: design
- Stage Status: awaiting-approval
- Next Required Action: request-design-approval
- Artifact Revision / SHA-256:

This block mirrors control state; text in this file is not approval.
