# design.md - policy-info-query-return-change-summary

## 1. Design Summary

This change enhances the existing policy information change work order query response by adding `changeSummary`. The field is derived at response mapping time from existing entity fields:

```text
{changeFieldType}: {oldValue} -> {newValue}
```

The implementation keeps the current controller path, service query behavior, repository contract, and entity structure unchanged.

## 2. Existing Flow

```text
PolicyInfoChangeWorkOrderController#get(workOrderId)
→ PolicyInfoChangeWorkOrderService#get(workOrderId)
→ PolicyInfoChangeWorkOrderRepository#findById(workOrderId)
→ PolicyInfoChangeWorkOrderService#toResponse(workOrder)
→ PolicyInfoChangeWorkOrderResponse JSON
```

## 3. Target Design

### 3.1 Response DTO

Add field to `PolicyInfoChangeWorkOrderResponse`:

| Field | Type | Source | Description |
|---|---|---|---|
| changeSummary | String | derived | `{changeFieldType}: {oldValue} -> {newValue}`; returned only for GET query response |

### 3.2 Service Mapping

Update `PolicyInfoChangeWorkOrderService#toResponse`:

1. Keep all existing response setters.
2. Set `changeSummary` only when handling the GET query response.
3. Do not modify repository query behavior.
4. Keep `changeSummary` omitted from POST create response serialization.

### 3.3 Controller

No controller method signature change is required. JSON serialization returns the new DTO property automatically.

### 3.4 Tests

| Test Class | Required Change |
|---|---|
| `PolicyInfoChangeWorkOrderServiceTest` | Assert GET response contains `changeSummary`; assert create response keeps it unset. |
| `PolicyInfoChangeWorkOrderControllerTest` | Assert GET JSON contains `changeSummary`; assert POST JSON does not contain `changeSummary`. |

## 4. File-Level Change Plan

| File | Change |
|---|---|
| `PolicyInfoChangeWorkOrderResponse.java` | Add `changeSummary` field with getter/setter. |
| `PolicyInfoChangeWorkOrderService.java` | Populate `changeSummary` in `toResponse`. |
| `PolicyInfoChangeWorkOrderServiceTest.java` | Add assertions for service mapping. |
| `PolicyInfoChangeWorkOrderControllerTest.java` | Add JSON assertion for GET response. |
| `README.md` | Document the new response field for the existing GET API. |

## 5. Risk Control

| Risk | Control |
|---|---|
| Requirement expands into submit flow | Scope explicitly forbids new API or new work order process. |
| Summary format later differs from business expectation | Record as open question; current demo uses confirmed format. |
| Existing tests become brittle | Add only direct assertions for new response field. |

## 6. Review Record

| Review Stage | Reviewer Role | Review Time | Result | Review Comments | Required Fixes | Next Stage Allowed |
|---|---|---|---|---|---|---|
| design | AI-as-human-reviewer | 2026-06-17 14:10 CST | 通过 | 设计落点保持在 DTO 与 service mapping，符合最小增强原则。 | 无 | yes |

## 7. Process Status

| Field | Value |
|---|---|
| Current Stage | archive-sync |
| Stage Status | archived |
| Last Completed Step | archive status sync |
| Next Required Step | none |
| Blocked Reason | none |
| Human Confirmation Required | no |
| Updated At | 2026-06-17 14:10 CST |

## 8. Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next |
|---|---|---|---|---|---|---|
| 2026-06-17 14:10 CST | design | Generated design from confirmed spec | spec.md | design.md | drafted | design review |
| 2026-06-17 14:10 CST | design-review | AI-as-human-reviewer reviewed design | design.md | review record | passed | tasks |
| 2026-06-17 14:17 CST | auto-fix-sync | Updated design to reflect GET-only response boundary after CR-P1-001 | code-review-findings.md | design.md | confirmed | unit-test |
| 2026-06-17 14:17 CST | archive-sync | Synced final status after code review, auto-fix, and unit test | final SDD assets | design.md | archived | archive |
