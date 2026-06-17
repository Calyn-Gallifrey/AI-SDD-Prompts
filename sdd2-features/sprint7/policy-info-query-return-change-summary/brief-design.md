# Brief Design（人工简要设计）

Feature Name（功能名称）：policy-info-query-return-change-summary

Feature Type（功能类型）：enhancement

Module（所属模块）：uaw-sdd-demo / policy-info-change query

Sprint（迭代）：sprint7

Priority（优先级）：P2

Goal（一句话目标）：增强现有保单信息变更工单查询接口，在响应中新增 `changeSummary` 字段，便于前端直接展示变更摘要。

API（接口）：GET /api/work-orders/policy-info-change/{workOrderId}

Request Params（入参）：
- workOrderId：工单号，路径参数，既有字段。

Response Params（出参）：
- workOrderId：工单号，既有字段。
- policyNo：保单号，既有字段。
- changeFieldType：变更字段类型，既有字段。
- oldValue：原值，既有字段。
- newValue：新值，既有字段。
- requester：提交人，既有字段。
- status：工单状态，既有字段。
- createdAt：创建时间，既有字段。
- changeSummary：变更摘要，新增字段，格式为 `{changeFieldType}: {oldValue} -> {newValue}`。

Business Logic（业务逻辑）：
1. 复用现有 `workOrderId` 查询逻辑，不改变查询条件和异常处理。
2. 查询成功后，在响应 DTO 中补充 `changeSummary`。
3. `changeSummary` 由既有 `changeFieldType`、`oldValue`、`newValue` 派生，不新增持久化字段。
4. 未查询到工单时仍沿用现有 404 行为。

Change Scope（变更范围）：
Response DTO, Service mapping, Controller serialization test, Service unit test, README API response description

Forbidden Changes（禁止变更）：
- 不新增 API。
- 不新增工单类型。
- 不新增数据库表或 repository 方法。
- 不修改 `POST /api/work-orders/policy-info-change` 的请求语义。
- 不改受益人变更和 I need document 相关功能。

Related Impact（关联逻辑与影响面）：
现有保单信息变更工单查询响应会增加一个只读派生字段；既有字段保持兼容。

Confirmed Facts（已确认信息）：
- 当前已有 `GET /api/work-orders/policy-info-change/{workOrderId}` 查询接口。
- 当前响应 DTO 已包含 `changeFieldType`、`oldValue`、`newValue`。
- 本次需求只需要增强既有查询响应，不需要新增提交流程。

Assumptions（推断信息）：
- demo 中 `changeSummary` 使用简单字符串拼接即可满足验证目的。
- 真实 UAW 工程中如有统一文案或国际化规则，应在 design 审核阶段确认。

Open Questions（待确认问题）：
- 真实项目中 `changeSummary` 的展示文案是否需要由前端组装或走字典转换。

## Review Record

| Review Stage | Reviewer Role | Review Time | Result | Review Comments | Required Fixes | Next Stage Allowed |
|---|---|---|---|---|---|---|
| brief-design | AI-as-human-reviewer | 2026-06-17 14:10 | 通过 | 必填字段完整，范围明确为既有查询响应新增字段，禁止扩展项清晰。 | 无 | yes |
