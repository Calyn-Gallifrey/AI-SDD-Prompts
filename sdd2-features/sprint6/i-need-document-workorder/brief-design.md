# Brief Design（人工简要设计）

> HISTORICAL EXAMPLE ONLY (quarantined 2026-07-14): this file predates deterministic SDD2 control. Approval, reviewer, status, and business text below is legacy illustration, not valid gate evidence or reusable requirement input.

Feature Name（功能名称）：i-need-document-workorder

Feature Type（功能类型）：enhancement

Module（所属模块）：transaction / document

Sprint（迭代）：sprint6

Priority（优先级）：P1

Goal（一句话目标）：新增 I need document 工单提交能力，支持 Servicing 坐席根据保单客户来电，提交“查询保单文档”或“发送保单文档给客户”的工单到下游平台，并返回工单号和下游提交号。

API（接口）：POST /api/work-orders/i-need-document

Request Params（入参）：
- policyNo：保单号，必填。
- customerName：客户姓名，必填。
- requestType：请求类型，必填，支持 QUERY_DOCUMENT 和 SEND_DOCUMENT。
- documentTypes：文档类型列表，必填，至少一个文档类型。
- deliveryEmail：发送邮箱，SEND_DOCUMENT 时必填，QUERY_DOCUMENT 时不需要。
- requester：提交工单的客服坐席，必填。

Response Params（出参）：
- workOrderId：UAW 工单号。
- policyNo：保单号。
- customerName：客户姓名。
- requestType：请求类型。
- documentTypes：文档类型列表。
- deliveryEmail：发送邮箱。
- downstreamSubmissionId：下游平台提交号。
- status：工单状态。
- createdAt：创建时间。

Business Logic（业务逻辑）：
1. 校验 policyNo、customerName、requestType、documentTypes、requester 必填。
2. 校验 documentTypes 中不能包含空白文档类型。
3. requestType 为 SEND_DOCUMENT 时，deliveryEmail 必填且必须符合邮箱格式，并做 trim + lower-case 归一化。
4. requestType 为 QUERY_DOCUMENT 时，不要求 deliveryEmail。
5. 创建状态为 SUBMITTED 的 I need document 工单。
6. 将工单提交到下游文档工单平台，记录下游提交号。
7. 返回 UAW 工单号、下游提交号和工单状态。

Change Scope（变更范围）：API, Service, Downstream Client, Repository, Model, Test, README

Forbidden Changes（禁止变更）：
- 不改现有保单信息变更工单接口。
- 不改现有保单受益人变更工单接口。
- 不接入真实下游系统。
- 不引入新的第三方依赖。
- 不改无关 transaction 功能。

Related Impact（关联逻辑与影响面）：
Spring Validation、工单状态初始化、下游提交号模拟、文档类型列表校验、邮箱归一化、Controller / Service / Repository 单元测试。

Confirmed Facts（已确认信息）：
- 业务背景来自 Servicing 保险电销平台 UAW。
- 客户可来电要求查询保单下文档，或要求客服发文档给保单客户。
- 坐席需要填写 I need document 工单表单并提交到下游平台。
- 当前 demo 工程是 Spring Boot + Maven，已有多个工单 API 样例。

Assumptions（推断信息）：
- demo 中使用 in-memory repository 保存工单。
- demo 中使用 in-memory downstream client 模拟下游平台返回提交号。
- 工单初始状态沿用 `SUBMITTED`。
- 文档类型暂按字符串列表处理，不新增文档类型枚举。

Open Questions（待确认问题）：
- 真实 UAW 下游平台接口协议、返回码和失败重试策略。
- 真实文档类型是否来自枚举、配置表或下游接口。
- 真实场景是否需要校验保单归属和客户身份。
