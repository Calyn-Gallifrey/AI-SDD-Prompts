# spec.md - policy-beneficiary-email-change

## 1. Overview

本功能在现有 `uaw-sdd-demo` 的保单受益人变更工单能力上，新增“修改受益人邮箱”的工单入口。

目标是新增一个独立 API：`POST /api/work-orders/policy-beneficiary-change/email`。该 API 接收保单号、受益人姓名、证件号、新邮箱和提交人，创建状态为 `SUBMITTED` 的受益人邮箱变更工单，并返回工单号、脱敏证件号、新邮箱和状态。

## 2. Scope

### 2.1 In Scope

- 新增邮箱变更请求 DTO。
- 扩展受益人变更工单实体，保存 `beneficiaryEmail`。
- 扩展受益人变更工单响应 DTO，返回 `beneficiaryEmail`。
- 在现有 Controller 增加 `/email` 子路径。
- 在现有 Service 增加邮箱变更创建逻辑。
- 复用现有 Repository 的重复提交控制。
- 增加 Service、Controller、Repository 单元测试。
- 更新 README API 示例。

### 2.2 Out of Scope

- 不接入数据库。
- 不接入真实用户上下文。
- 不接入外部通知或邮件服务。
- 不修改现有 `POST /api/work-orders/policy-beneficiary-change` 请求语义。
- 不修改保单信息变更工单能力。

## 3. Functional Requirements

| ID | Requirement | Acceptance Criteria |
|---|---|---|
| FR-1 | 支持创建受益人邮箱变更工单 | `POST /api/work-orders/policy-beneficiary-change/email` 成功返回 HTTP 201 和工单信息。 |
| FR-2 | 校验必填字段 | policyNo、beneficiaryName、beneficiaryIdNo、beneficiaryEmail、requester 为空时返回 400。 |
| FR-3 | 校验邮箱格式 | beneficiaryEmail 不符合邮箱格式时返回 400。 |
| FR-4 | 邮箱归一化 | service 层保存和返回 trim 后小写的邮箱。 |
| FR-5 | 重复提交控制 | 同一 policyNo + beneficiaryIdNo 已有 SUBMITTED 工单时返回 400。 |
| FR-6 | 证件号脱敏 | 响应只返回 beneficiaryIdNoMasked，不返回 beneficiaryIdNo。 |

## 4. Non-functional Requirements

- 不引入新依赖。
- 不扩大修改范围到无关模块。
- 单元测试必须覆盖成功、格式错误、重复提交、Controller validation。
- 当前 demo 无真实数据库，本次保存仍使用 in-memory repository。

## 5. Risks and Confirmations

| Type | Item | Handling |
|---|---|---|
| 已确认 | 当前 demo 使用 JUnit4 + Mockito + Vintage | 继续沿用现有测试风格。 |
| 推断 | 邮箱按小写归一化 | 在 design/tasks/archive 中记录。 |
| 待确认 | 真实 UAW 是否允许同一受益人多个提交中变更工单 | demo 沿用现有重复提交规则。 |

## 6. Human Review

| Review Stage | Reviewer Role | Review Result | Review Comments | Required Fixes | Next Stage Allowed |
|---|---|---|---|---|---|
| spec | AI-as-human-reviewer | 通过 | 范围、非范围、验收标准和风险均清晰，可以进入 design。 | 无 | yes |

## Process Status

Current Stage：archive

Stage Status：closed

Last Completed Step：archive completed

Next Required Step：无

Blocked Reason：无

## Process Audit Trail

| Time | Stage | Action | Result | Next Step |
|---|---|---|---|---|
| 2026-06-11 12:40 | spec | AI generated spec.md | draft completed | human review |
| 2026-06-11 12:41 | spec-review | AI-as-human-reviewer reviewed spec.md | passed | generate design.md |
| 2026-06-11 12:50 | archive-sync | AI synchronized final process status | closed | none |
