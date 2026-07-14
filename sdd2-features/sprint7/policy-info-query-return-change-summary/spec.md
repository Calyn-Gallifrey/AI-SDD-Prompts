# spec.md - policy-info-query-return-change-summary

> HISTORICAL EXAMPLE ONLY (quarantined 2026-07-14): this file predates deterministic SDD2 control. Approval, reviewer, status, and business text below is legacy illustration, not valid gate evidence or reusable requirement input.

## 1. Requirement Summary

Enhance the existing policy information change work order query API:

```http
GET /api/work-orders/policy-info-change/{workOrderId}
```

The response must include a new read-only field `changeSummary`. The field is derived from existing work order data and must not change the API path, request parameters, submit flow, persistence model, or duplicate-check behavior.

## 2. Scope

### In Scope

- Add `changeSummary` to `PolicyInfoChangeWorkOrderResponse`.
- Populate `changeSummary` in `PolicyInfoChangeWorkOrderService#toResponse`.
- Cover the new field in service unit test and controller serialization test.
- Update README query response description.

### Out of Scope

- New work order type.
- New API endpoint.
- New database table, mapper, or repository method.
- Changes to `POST /api/work-orders/policy-info-change`.
- Changes to beneficiary or I need document modules.

## 3. Functional Requirements

| ID | Requirement | Acceptance Criteria |
|---|---|---|
| FR-1 | Existing query returns `changeSummary` | Successful GET response contains `changeSummary`. |
| FR-2 | Summary is derived consistently | For a work order with `changeFieldType=HOLDER_PHONE`, `oldValue=13800000000`, `newValue=13900000000`, response `changeSummary` is `HOLDER_PHONE: 13800000000 -> 13900000000`. |
| FR-3 | Existing behavior remains unchanged | Missing work order still returns existing not-found behavior. |
| FR-4 | No scope expansion | No new endpoint, repository method, entity field, table, or unrelated module change is introduced. |

## 4. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Compatibility | Existing response fields remain unchanged. |
| Maintainability | Summary generation stays in service mapping and uses existing fields. |
| Testability | Unit tests verify service mapping and controller JSON serialization. |

## 5. Acceptance Validation

- `PolicyInfoChangeWorkOrderServiceTest` verifies GET response mapping contains `changeSummary` and create response keeps it unset.
- `PolicyInfoChangeWorkOrderControllerTest` verifies GET JSON contains `changeSummary` and POST JSON does not contain `changeSummary`.
- Full Maven test suite passes when local Maven is available.

## 6. Review Record

| Review Stage | Reviewer Role | Review Time | Result | Review Comments | Required Fixes | Next Stage Allowed |
|---|---|---|---|---|---|---|
| spec | legacy-simulated-reviewer (not valid approval) | 2026-06-17 14:10 CST | 通过 | 需求范围限定为既有查询响应新增派生字段，验收标准可测试，非范围约束明确。 | 无 | yes |

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
| 2026-06-17 14:10 CST | spec | Generated spec from proposal-input.md | proposal-input.md | spec.md | drafted | spec review |
| 2026-06-17 14:10 CST | spec-review | legacy-simulated-reviewer (not valid approval) reviewed spec | spec.md | review record | passed | design |
| 2026-06-17 14:17 CST | archive-sync | Synced final status after code review, auto-fix, and unit test | final SDD assets | spec.md | archived | archive |
