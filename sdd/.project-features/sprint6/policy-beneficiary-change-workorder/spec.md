# 功能级 Spec

# 1. 基本信息

- 功能名称：policy-beneficiary-change-workorder
- 功能类型：submit
- 所属模块：policy / workorder
- 所在 sprint：sprint6
- 优先级：P1
- 风险等级：medium
- 对应 proposal：`./proposal-input.md`
- spec 文件路径：`./spec.md`
- 当前状态：confirmed

# 2. Proposal 输入摘要

## 一句话目标

- 新增保单受益人变更工单提交接口，生成待处理工单并返回脱敏受益人信息。

## 业务背景 / 触发原因

- BA 需求要求支持保单受益人变更提交能力。
- 本次同时用于验证真实迭代中“开发个人简要设计 → proposal → spec → design → tasks → code → review → unit test → archive”的 SDD 闭环。

## 提案原始范围

- 新增受益人变更工单创建接口。
- 新增受益人变更工单请求、响应、实体、关系枚举。
- 新增受益人变更工单 Service。
- 新增受益人变更工单 Repository 抽象和内存实现。
- 新增 Service / Controller 单元测试。

## 提案禁止变更项

- 不接真实数据库。
- 不改已有保单信息变更工单接口。
- 不引入前端。
- 不修改 SDD 体系文件。
- 不生成 SDD 内部 Code Review HTML 报告。

## 提案优先级

- P1

# 3. Context Assembly（上下文装配结果）

## Base Context（默认装配）

- 当前项目目录结构：`uaw-sdd-demo/`
- 当前模块基础语境：policy / workorder
- 当前代码扫描范围：`uaw-sdd-demo/src/main/java/com/example/uawsdddemo/` 与 `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/`
- 通用开发规范：Spring Boot Controller / Service / Repository / DTO / Entity 分层

## Conditional Context（按任务命中的上下文）

- 历史功能资产：不适用，本次为新增 submit 功能。
- 外部依赖背景：不适用，本次无外部系统。
- 兼容性背景：不得破坏已有 `/api/work-orders/policy-info-change`。
- 特殊领域知识：受益人证件号属于敏感信息，响应必须脱敏。

## 引用文件清单

- `.project-ai/context/1.index.md`
- `.project-ai/templates/1.proposal-input-template.md`
- `.project-ai/templates/2.spec-template.md`
- `.project-ai/templates/3.design-template.md`
- `.project-ai/templates/4.tasks-template.md`
- `.project-ai/rules/code-review/UAW-Code-Review.md`
- `.project-ai/rules/testing/`
- `uaw-sdd-demo/pom.xml`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/`

# 4. 当前现状（As-Is Baseline）

## 当前 Git 实物基线

- 现有接口：`POST /api/work-orders/policy-info-change`，`GET /api/work-orders/policy-info-change/{workOrderId}`
- 现有 service：`PolicyInfoChangeWorkOrderService`
- 现有 mapper：无
- 现有 repository：`PolicyInfoChangeWorkOrderRepository` 与内存实现
- 现有对象：保单信息变更工单 DTO / Entity / Enum
- 现有流程：创建保单信息变更工单并做基础重复校验

## 当前存在问题 / 缺口

- 没有保单受益人变更工单能力。
- 没有受益人关系枚举。
- 没有受益人证件号脱敏响应。
- 没有受益人变更工单测试。

# 5. 历史功能资产（仅 enhancement / refactor）

- 不适用：本次为新增 submit 功能，不读取历史功能目录。

# 6. 功能目标（To-Be）

## 本次必须达成

- 新增 `POST /api/work-orders/policy-beneficiary-change`。
- 支持创建受益人变更待处理工单。
- 校验受益比例范围为 1-100。
- 校验同一保单、同一受益人证件号、待处理状态不可重复提交。
- 响应中证件号必须脱敏。
- 补充 Service / Controller 单元测试。

## 本次完成后预期结果

- 合法请求返回 `201 Created`。
- 重复提交返回 400。
- 受益比例非法返回 400。
- 请求必填字段缺失返回 400。
- `mvn test` 通过。

## 业务价值

- 支持受益人变更工单提交。
- 验证 SDD 从开发个人简要设计进入正式流程的可执行性。

# 7. 变更范围（In Scope）

## 包含范围

- 新增接口
- 新增 Service 逻辑
- 新增 Repository 抽象与内存实现
- 新增 DTO / Entity / Enum
- 补充测试

## 明确交付物

- `PolicyBeneficiaryChangeWorkOrderController.java`
- `PolicyBeneficiaryChangeWorkOrderService.java`
- `PolicyBeneficiaryChangeWorkOrderRepository.java`
- `InMemoryPolicyBeneficiaryChangeWorkOrderRepository.java`
- `CreatePolicyBeneficiaryChangeWorkOrderRequest.java`
- `PolicyBeneficiaryChangeWorkOrderResponse.java`
- `PolicyBeneficiaryChangeWorkOrder.java`
- `BeneficiaryRelationType.java`
- `PolicyBeneficiaryChangeWorkOrderServiceTest.java`
- `PolicyBeneficiaryChangeWorkOrderControllerTest.java`

# 8. 非范围（Out of Scope）

本次明确不做：

- 前端页面。
- 真实数据库表结构。
- 审批流。
- 查询受益人变更工单详情接口。
- 外部保单系统联动。
- SDD 体系文件调整。

# 9. 不可变边界（Constraints / Non-goals）

明确禁止：

- 不改已有 API path。
- 不改保单信息变更工单已有行为。
- 不接真实数据库。
- 不生成 SDD 内部 Code Review HTML 报告。
- 不把本次 demo 实现当作生产持久化方案。

# 10. Domain Mapping（领域映射）

| 业务概念 | 系统对象 | 来源 |
|---|---|---|
| 保单号 | policyNo | 请求入参 |
| 受益人姓名 | beneficiaryName | 请求入参 |
| 受益人证件号 | beneficiaryIdNo | 请求入参，实体保存，响应脱敏 |
| 受益人与投保人关系 | BeneficiaryRelationType | 请求入参与枚举 |
| 受益比例 | benefitRatio | 请求入参 |
| 工单状态 | WorkOrderStatus | 系统生成 |

# 11. 依赖识别

## 内部依赖

- Spring Web
- Spring Validation
- 现有异常类
- 现有异常处理器
- 现有 `WorkOrderStatus`

## 外部依赖

- 无。

## 数据依赖

- 内存仓储，不依赖数据库。

# 12. 风险识别

## 技术风险

- 内存仓储仅适合流程验证。
- 重复提交判断需避免明显的 exists + save 分离窗口。

## 兼容风险

- 新接口路径独立，不影响现有接口。

## 交付风险

- 本次由 Codex 代理人工审核，适合流程完整性验证，不代表真实生产审批。

## 数据风险

- 证件号敏感，响应必须脱敏。

## 风险重点（供 design 引用）

- 敏感字段脱敏。
- 重复提交原子性。
- 不破坏已有接口。

# 13. 回滚策略

若合并失败：

- 回退新增受益人变更工单相关类和测试。
- 保留 SDD 资产作为流程验证记录。

# 14. 验收标准（Acceptance Criteria）

- `POST /api/work-orders/policy-beneficiary-change` 存在。
- 合法请求返回 `201 Created`。
- 响应包含脱敏证件号 `beneficiaryIdNoMasked`，不返回明文证件号。
- `benefitRatio < 1` 或 `> 100` 返回 400。
- 同一保单 + 同一受益人证件号 + SUBMITTED 状态重复提交返回 400。
- 必填字段缺失返回 400。
- Service / Controller 测试覆盖主路径和异常路径。
- `mvn test` 通过。

# 15. 代理人工审核记录

| Time | Stage | Reviewer Role | Result | Comment |
|---|---|---|---|---|
| 2026-05-29 12:20:03 +0800 | Spec | Codex 扮演人类审核 | 通过 | Spec 明确目标、范围、非范围、验收标准和敏感字段要求 |

# Process Status（强制｜流程闸门）

- Current Stage：Archive
- Stage Status：archived
- Last Completed Step：archive.md 已生成并完成代理最终审核
- Next Required Step：流程复盘与问题确认
- Human Confirmation Required：no（本轮由用户授权 Codex 扮演人类审核）
- Allowed Next Action：检查归档结果，确认是否要调整 SDD 体系模板
- Forbidden Next Action：未经用户确认直接修改 SDD 体系模板
- Updated At：2026-05-29 12:34:45 +0800

# Process Audit Trail（强制｜过程审核轨迹）

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-29 12:20:03 +0800 | Spec | 根据 proposal 生成 Spec | proposal-input.md、当前代码扫描 | spec.md | 通过代理审核 | Design |
| 2026-05-29 12:34:45 +0800 | Archive | 同步最终流程状态 | 全部 SDD 资产和代码 | archive.md | 通过代理审核 | Done |
