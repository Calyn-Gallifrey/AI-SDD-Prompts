# proposal-input.md

> HISTORICAL EXAMPLE ONLY (quarantined 2026-07-14): this file predates deterministic SDD2 control. Approval, reviewer, status, and business text below is legacy illustration, not valid gate evidence or reusable requirement input.

本文件由 `uaw-sdd-ai-coding` 根据 `Brief Design（人工简要设计）` 自动组装，开发不需要手工填写。

## 1. Task Basic Information

SDD Version（SDD版本）：SDD2.0

Feature Workspace Root（功能资产根目录）：sdd2-features

Feature Name（功能名称）：policy-beneficiary-email-change

Feature Type（功能类型）：enhancement

Module（所属模块）：transaction / policy beneficiary

Goal（一句话目标）：在现有保单受益人变更工单能力上新增修改受益人邮箱的工单入口，支持坐席提交指定保单、受益人证件号和新邮箱，并返回工单号。

## 2. Change Identification

Change Scope（变更范围）：API, Service, Repository, Model, Test, README

Forbidden Changes（禁止变更）：
- 不改现有 POST /api/work-orders/policy-beneficiary-change 的请求语义。
- 不改现有保单信息变更工单能力。
- 不引入数据库或外部系统调用。
- 不引入新的第三方依赖。
- 不改无关 transaction 功能。

Priority（优先级）：P1

Sprint（迭代）：sprint6

Output Directory（输出目录）：sdd2-features/sprint6/policy-beneficiary-email-change/

## 3. Requirement Details

API（接口）：POST /api/work-orders/policy-beneficiary-change/email

Request Params（入参）：
- policyNo：保单号，必填。
- beneficiaryName：受益人姓名，必填。
- beneficiaryIdNo：受益人证件号，必填。
- beneficiaryEmail：受益人新邮箱，必填，必须符合邮箱格式。
- requester：提交人，必填。

Response Params（出参）：
- workOrderId：工单号。
- policyNo：保单号。
- beneficiaryName：受益人姓名。
- beneficiaryIdNoMasked：脱敏证件号。
- beneficiaryEmail：受益人新邮箱。
- requester：提交人。
- status：工单状态。
- createdAt：创建时间。

Business Logic（业务逻辑）：
1. 校验必填字段。
2. 校验 beneficiaryEmail 邮箱格式，并做 trim + lower-case 归一化。
3. 复用现有 policyNo + beneficiaryIdNo 的提交中工单重复控制。
4. 保存状态为 SUBMITTED 的邮箱变更工单。
5. 返回工单号、脱敏证件号、新邮箱和状态。

Related Impact（关联逻辑与影响面）：
现有保单受益人变更工单 controller/service/entity/repository/response/test，重复提交控制，证件号脱敏，Spring Validation，JUnit4 + Mockito 测试。

Confirmed Facts（已确认信息）：
- 当前 demo 已有保单受益人变更工单能力。
- 当前 demo 使用 Spring Boot 3.3.5、Java 17、Maven、JUnit4 + Mockito + Vintage。
- 当前已有重复提交控制：同一 policyNo + beneficiaryIdNo 的 SUBMITTED 工单不可重复提交。

Assumptions（推断信息）：
- 修改受益人邮箱属于保单受益人变更工单的一个增强入口。
- 工单初始状态沿用 SUBMITTED。
- 邮箱大小写按业务归一化为小写。
- 当前 demo 无真实登录上下文，因此 requester 仍由请求显式传入。

Open Questions（待确认问题）：
- 真实 UAW 工程中 beneficiaryIdNo 是否应改由受益人唯一 ID 传入。
- 真实 UAW 工程中邮箱是否需要额外做黑名单、域名或长度规则。
- 真实 UAW 工程中是否允许同时存在“受益人信息变更”和“受益人邮箱变更”两个提交中工单。

## 4. Code Project Context

Reference Basis（参考依据）：当前 `uaw-sdd-demo` 工程内已有保单受益人变更工单代码。

Current Code Project Root（当前代码工程根目录）：uaw-sdd-demo/

## 5. SDD Execution Requirements

AI Knowledge Base（AI 知识底座）：skills/uaw-sdd-ai-coding/references、skills/uaw-code-review/references、skills/uaw-unit-test/references

Code Baseline（代码基线）：当前 Git working tree + uaw-sdd-demo 基线测试通过

Required Flow（强制流程）：

```text
proposal-input.md → spec.md → design.md → tasks.md → implementation → code-review-findings.md → Auto-fix → Unit Test Summary → archive.md
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
| 2026-06-11 12:39 | brief-design | AI parsed required fields | passed | assemble proposal-input.md |
| 2026-06-11 12:40 | proposal | legacy-simulated-reviewer (not valid approval) confirmed proposal input | passed | generate spec.md |
| 2026-06-11 12:50 | archive-sync | AI synchronized final process status | archived | none |
