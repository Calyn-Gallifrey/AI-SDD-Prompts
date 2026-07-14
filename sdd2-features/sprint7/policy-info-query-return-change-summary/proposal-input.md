# proposal-input.md

> HISTORICAL EXAMPLE ONLY (quarantined 2026-07-14): this file predates deterministic SDD2 control. Approval, reviewer, status, and business text below is legacy illustration, not valid gate evidence or reusable requirement input.

## Basic Information

SDD Version（SDD版本）：SDD2.0

Executed Skill（执行 Skill）：uaw-sdd-ai-coding

Feature Name（功能名称）：policy-info-query-return-change-summary

Feature Type（功能类型）：enhancement

Module（所属模块）：uaw-sdd-demo / policy-info-change query

Sprint（迭代）：sprint7

Priority（优先级）：P2

Project Root（代码工程根目录）：uaw-sdd-demo

Output Directory（输出目录）：sdd2-features/sprint7/policy-info-query-return-change-summary/

Goal（一句话目标）：增强现有保单信息变更工单查询接口，在响应中新增 `changeSummary` 字段，便于前端直接展示变更摘要。

## Current Requirement

### API

GET /api/work-orders/policy-info-change/{workOrderId}

### Request Params

| Name | Type | Required | Source | Description |
|---|---|---|---|---|
| workOrderId | String | yes | path | 工单号，既有字段。 |

### Response Params

| Name | Type | Status | Description |
|---|---|---|---|
| workOrderId | String | existing | 工单号。 |
| policyNo | String | existing | 保单号。 |
| changeFieldType | ChangeFieldType | existing | 变更字段类型。 |
| oldValue | String | existing | 原值。 |
| newValue | String | existing | 新值。 |
| requester | String | existing | 提交人。 |
| status | WorkOrderStatus | existing | 工单状态。 |
| createdAt | Instant | existing | 创建时间。 |
| changeSummary | String | added | 变更摘要，格式为 `{changeFieldType}: {oldValue} -> {newValue}`。 |

## Business Logic

1. 复用现有 `PolicyInfoChangeWorkOrderService#get` 查询逻辑。
2. 在 `PolicyInfoChangeWorkOrderResponse` 中新增 `changeSummary` 字段。
3. 在 service response mapping 中由既有字段派生 `changeSummary`。
4. Controller 序列化响应时返回新增字段。
5. 未查询到工单时继续返回现有 404 行为。

## Change Scope

- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/PolicyInfoChangeWorkOrderResponse.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderServiceTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderControllerTest.java`
- `uaw-sdd-demo/README.md`

## Forbidden Changes

- 不新增 API。
- 不新增工单类型。
- 不新增数据库表或 repository 方法。
- 不修改 `POST /api/work-orders/policy-info-change` 的请求语义。
- 不改受益人变更和 I need document 相关功能。

## Confirmed Facts

- 当前已有 `GET /api/work-orders/policy-info-change/{workOrderId}` 查询接口。
- 当前响应 DTO 已包含 `changeFieldType`、`oldValue`、`newValue`。
- 本次需求只需要增强既有查询响应，不需要新增提交流程。

## Assumptions

- demo 中 `changeSummary` 使用简单字符串拼接。
- 真实 UAW 工程如有统一字段文案规则，应在 design 审核时补充。

## Open Questions

- 真实项目中 `changeSummary` 的展示文案是否需要由前端组装或走字典转换。

## SDD Flow

brief-design.md → proposal-input.md → spec.md → design.md → tasks.md → implementation → code-review-findings.md → Auto-fix Summary → Unit Test Summary → archive.md

## Process Status

| Field | Value |
|---|---|
| Current Stage | archive-sync |
| Stage Status | archived |
| Last Completed Step | archive status sync |
| Next Required Step | none |
| Blocked Reason | none |
| Human Confirmation Required | no |
| Updated At | 2026-06-17 14:10 CST |

## Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next |
|---|---|---|---|---|---|---|
| 2026-06-17 14:10 CST | brief-design | Captured confirmed brief design | confirmed validation requirement | brief-design.md | passed | proposal |
| 2026-06-17 14:10 CST | proposal | Assembled internal proposal input | brief-design.md | proposal-input.md | confirmed | spec |
| 2026-06-17 14:17 CST | archive-sync | Synced final status after code review, auto-fix, and unit test | final SDD assets | proposal-input.md | archived | archive |

## Generalization Compliance

- Feature directory is derived from the confirmed current `Feature Name`.
- The scope is limited to an existing query response delta.
- No template placeholder, historical demo feature name, API path, or business flow is used as requirement content.
- No new work order, submit flow, table, repository method, or unrelated module is introduced.
