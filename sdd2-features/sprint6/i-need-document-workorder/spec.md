# spec.md - i-need-document-workorder

## 1. Overview

本功能在 `uaw-sdd-demo` 中新增 I need document 工单提交能力。Servicing 坐席接到保单客户来电后，可以为客户提交“查询保单文档”或“发送保单文档给客户”的工单，并将工单提交到下游文档工单平台。

目标 API：`POST /api/work-orders/i-need-document`。

## 2. Scope

### 2.1 In Scope

- 新增 I need document 请求 DTO。
- 新增 I need document 响应 DTO。
- 新增请求类型枚举。
- 新增 I need document 工单实体。
- 新增 in-memory repository。
- 新增 demo downstream client，模拟下游平台提交并返回提交号。
- 新增 Controller 和 Service。
- 增加 Controller、Service、Repository 单元测试。
- 更新 README API 示例。

### 2.2 Out of Scope

- 不接入真实下游平台。
- 不接入真实保单查询或文档查询。
- 不校验真实客户身份和保单归属。
- 不新增数据库表。
- 不修改现有工单接口。
- 不引入新依赖。

## 3. Functional Requirements

| ID | Requirement | Acceptance Criteria |
|---|---|---|
| FR-1 | 支持提交 I need document 工单 | `POST /api/work-orders/i-need-document` 成功返回 HTTP 201、工单号、下游提交号和状态。 |
| FR-2 | 支持查询文档请求 | `requestType=QUERY_DOCUMENT` 时允许不传 `deliveryEmail`。 |
| FR-3 | 支持发送文档请求 | `requestType=SEND_DOCUMENT` 时必须传合法 `deliveryEmail`。 |
| FR-4 | 校验文档类型列表 | `documentTypes` 至少包含一个非空文档类型，列表中空白项返回 400。 |
| FR-5 | 邮箱归一化 | `deliveryEmail` 执行 trim + lower-case 后保存和返回。 |
| FR-6 | 模拟下游提交 | Service 必须调用 downstream client，响应中返回 `downstreamSubmissionId`。 |

## 4. Non-functional Requirements

- 不引入新第三方依赖。
- 遵守现有 Spring Boot Controller / Service / Repository 分层。
- 沿用 JUnit4 + Mockito 测试风格。
- SDD 内部 Code Review 不生成 HTML 报告。
- Unit Test Summary 必须记录实际验证入口。

## 5. Risks and Confirmations

| Type | Item | Handling |
|---|---|---|
| 已确认 | 当前 demo 不接真实下游 | 用 in-memory downstream client 模拟。 |
| 推断 | 工单初始状态为 SUBMITTED | 沿用现有 `WorkOrderStatus.SUBMITTED`。 |
| 推断 | 文档类型暂不建枚举 | 使用字符串列表，Service 校验非空。 |
| 待确认 | 真实下游接口协议 | Archive 中记录真实项目落地风险。 |

## 6. Human Review

| Review Stage | Reviewer Role | Review Result | Review Comments | Required Fixes | Next Stage Allowed |
|---|---|---|---|---|---|
| spec | AI-as-human-reviewer | 通过 | 范围、非范围、验收标准、下游模拟边界清晰，可以进入 design。 | 无 | yes |

## Process Status

Current Stage：archive

Stage Status：archived

Last Completed Step：archive completed

Next Required Step：无

Blocked Reason：无

## Process Audit Trail

| Time | Stage | Action | Result | Next Step |
|---|---|---|---|---|
| 2026-06-11 14:36 | spec | AI generated spec.md | draft completed | human review |
| 2026-06-11 14:37 | spec-review | AI-as-human-reviewer reviewed spec.md | passed | generate design.md |
| 2026-06-11 14:43 | archive-sync | AI synchronized final process status | archived | none |
