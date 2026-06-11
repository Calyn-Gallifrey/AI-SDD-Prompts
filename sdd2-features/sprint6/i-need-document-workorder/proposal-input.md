# proposal-input.md

本文件由 `uaw-sdd-ai-coding` 根据 `Brief Design（人工简要设计）` 自动组装，开发不需要手工填写。

## 1. Task Basic Information

SDD Version（SDD版本）：SDD2.0

Feature Workspace Root（功能资产根目录）：sdd2-features

Feature Name（功能名称）：i-need-document-workorder

Feature Type（功能类型）：enhancement

Module（所属模块）：transaction / document

Goal（一句话目标）：新增 I need document 工单提交能力，支持 Servicing 坐席根据保单客户来电，提交“查询保单文档”或“发送保单文档给客户”的工单到下游平台，并返回工单号和下游提交号。

## 2. Change Identification

Change Scope（变更范围）：API, Service, Downstream Client, Repository, Model, Test, README

Forbidden Changes（禁止变更）：
- 不改现有保单信息变更工单接口。
- 不改现有保单受益人变更工单接口。
- 不接入真实下游系统。
- 不引入新的第三方依赖。
- 不改无关 transaction 功能。

Priority（优先级）：P1

Sprint（迭代）：sprint6

Output Directory（输出目录）：sdd2-features/sprint6/i-need-document-workorder/

## 3. Requirement Details

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
1. 校验必填字段。
2. 校验 documentTypes 中不能包含空白文档类型。
3. SEND_DOCUMENT 请求必须校验并归一化 deliveryEmail。
4. QUERY_DOCUMENT 请求不要求 deliveryEmail。
5. 创建状态为 SUBMITTED 的 I need document 工单。
6. 提交到 demo 下游文档工单平台并记录下游提交号。
7. 返回工单号、下游提交号和工单状态。

Related Impact（关联逻辑与影响面）：
新增 document 工单 controller/service/model/repository/downstream client/test，复用现有 WorkOrderStatus、异常处理和 Spring Validation。

Confirmed Facts（已确认信息）：
- 当前 demo 已有 Spring Boot + Maven 工单 API 样例。
- 当前 demo 已有全局异常处理和 `BadRequestException`。
- 当前 demo 测试风格为 JUnit4 + Mockito。

Assumptions（推断信息）：
- demo 不接入真实下游系统，使用 in-memory downstream client 模拟提交。
- 工单状态沿用 `SUBMITTED`。
- 文档类型暂按字符串列表处理。

Open Questions（待确认问题）：
- 真实下游平台接口协议。
- 真实文档类型来源。
- 真实保单权限和客户身份校验规则。

## 4. Reference Basis

Reference Assets（参考资产）：当前 `uaw-sdd-demo` 工程内已有保单信息变更和保单受益人变更工单代码。

Reference Notes（参考说明）：仅参考现有 demo 的 controller/service/repository/test 风格，不引用旧版 SDD 路径。

## 5. SDD Execution Requirements

AI Knowledge Base（AI 知识底座）：skills/uaw-sdd-ai-coding/references、skills/uaw-code-review/references、skills/uaw-unit-test/references

Code Baseline（代码基线）：当前 Git working tree + uaw-sdd-demo 基线测试通过

Required Flow（强制流程）：

```text
brief-design.md → proposal-input.md → spec.md → design.md → tasks.md → implementation → code-review-findings.md → Auto-fix → Unit Test Summary → archive.md
```

## Process Status

Current Stage：archive

Stage Status：archived

Last Completed Step：archive completed

Next Required Step：无

Blocked Reason：无

## Process Audit Trail

| Time | Stage | Action | Result | Next Step |
|---|---|---|---|---|
| 2026-06-11 14:35 | brief-design | AI parsed required fields | passed | assemble proposal-input.md |
| 2026-06-11 14:36 | proposal | AI-as-human-reviewer confirmed proposal input | passed | generate spec.md |
| 2026-06-11 14:43 | archive-sync | AI synchronized final process status | archived | none |
