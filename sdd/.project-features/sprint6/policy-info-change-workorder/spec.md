# 功能级 Spec

# 1. 基本信息

- 功能名称：policy-info-change-workorder
- 功能类型：submit
- 所属模块：policy / workorder
- 所在 sprint：sprint6
- 优先级：P1
- 风险等级：medium
- 对应 proposal：`./proposal-input.md`
- spec 文件路径：`./spec.md`
- 当前状态：confirmed（模拟确认）

# 2. Proposal 输入摘要

## 一句话目标

- 新增保单信息变更工单的创建与查询能力，用于验证 UAW-SDD 从提案到归档的完整闭环。

## 业务背景 / 触发原因

- 公司内网准备投入 AI Coding 前，需要用一个可执行的 Spring Boot + Maven 工程验证 SDD 体系是否能从需求输入、设计、施工、代码评审、自动修复、测试到归档完整闭环。

## 提案原始范围

- 创建一个新的 Spring Boot Maven 工程。
- 模拟新增“保单信息变更工单”能力。
- 覆盖接口层、业务层、仓储层、模型层、单元测试与 Maven 配置。
- 输出 SDD 试跑资产并识别体系问题。

## 提案禁止变更项

- 不接入真实数据库。
- 不引入公司内网专有依赖。
- 不实现前端。
- 不生成 SDD 内部 Code Review HTML 报告。

## 提案优先级

- P1。

# 3. Context Assembly（上下文装配结果）

## Base Context（默认装配）

- 已读取 `.project-ai/context/1.index.md`。
- 已读取 proposal / spec / design / tasks / archive 模板。
- 已读取 SDD 内部 Code Review 入口规则。
- 已扫描新建代码工程 `uaw-sdd-demo/`。

## Conditional Context（按任务命中的上下文）

- 历史功能资产：不适用，本次为新增模拟功能。
- 外部依赖背景：不适用，本次不接外部系统。
- 兼容性背景：Spring Boot 3.3.5、Maven 3.9.16、本地 Maven 使用 Java 26.0.1。
- 特殊领域知识：保单信息变更工单需要避免相同保单、相同变更字段、相同新值的待处理重复提交。

## 引用文件清单

- `.project-ai/context/1.index.md`
- `.project-ai/templates/1.proposal-input-template.md`
- `.project-ai/templates/2.spec-template.md`
- `.project-ai/templates/3.design-template.md`
- `.project-ai/templates/4.tasks-template.md`
- `.project-ai/templates/5.archive-template.md`
- `.project-ai/rules/code-review/UAW-Code-Review.md`
- `uaw-sdd-demo/pom.xml`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/`

# 4. 当前现状（As-Is Baseline）

## 当前 Git 实物基线

- 现有接口：本次创建前无示例工程接口。
- 现有 service：本次创建前无示例工程 service。
- 现有 mapper：本次不使用 mapper。
- 现有 repository：本次创建前无示例工程 repository。
- 现有对象：本次创建前无示例工程 DTO / Entity / Enum。
- 现有流程：已有 SDD 体系文件，但没有真实 Spring Boot 工程试跑记录。

## 当前存在问题 / 缺口

- SDD 资产目录与代码工程目录不在同一根下，模板缺少明确的“代码工程根目录”字段。
- SDD 模板没有前置环境预检闸门，无法提前发现 Maven 实际运行 JDK 与命令行 `java` 不一致的问题。
- SDD 流程要求人工确认，但模拟试跑没有专门的“模拟确认 / 用户授权自动执行”状态表达。

# 5. 历史功能资产

- 不适用：本次不是 enhancement / refactor。

# 6. 功能目标（To-Be）

## 本次必须达成

- 新建 Maven 管理的 Spring Boot 工程 `uaw-sdd-demo/`。
- 新增保单信息变更工单创建接口。
- 新增保单信息变更工单查询接口。
- 实现基础业务校验：新旧值不能一致。
- 实现重复提交校验：同一保单、同一变更字段、同一新值已有待处理工单时拒绝提交。
- 补充服务层与接口层测试。
- 按 SDD 标准流程记录 Code Review、Auto-fix、Unit Test Summary 和 Archive。
- 输出 SDD 体系问题报告。

## 本次完成后预期结果

- `mvn test` 可通过。
- 本次流程资产可作为后续 SDD 体系优化的复盘输入，而不是直接作为生产业务样板。

## 业务价值

- 用低风险示例功能验证 SDD 体系在真实代码工程中的执行链路。
- 提前暴露内网 AI Coding 使用前的流程、模板、环境和规则适配问题。

# 7. 变更范围（In Scope）

## 包含范围

- 新增 Spring Boot Maven 工程。
- 新增 Controller / Service / Repository / DTO / Entity / Enum / Exception Handler。
- 新增 JUnit4 + Mockito 测试。
- 调整 Maven 测试运行配置以兼容当前本地 JDK。
- 输出本次 SDD 试跑文档。

## 明确交付物

- `uaw-sdd-demo/pom.xml`
- `uaw-sdd-demo/.gitignore`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/**`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/**`
- `uaw-sdd-demo/README.md`
- `.project-features/sprint6/policy-info-change-workorder/proposal-input.md`
- `.project-features/sprint6/policy-info-change-workorder/spec.md`
- `.project-features/sprint6/policy-info-change-workorder/design.md`
- `.project-features/sprint6/policy-info-change-workorder/tasks.md`
- `.project-features/sprint6/policy-info-change-workorder/archive.md`
- `.project-features/sprint6/policy-info-change-workorder/sdd-system-findings.md`

# 8. 非范围（Out of Scope）

本次明确不做：

- 不接真实数据库。
- 不实现审批流、撤销、完成、拒绝状态流转。
- 不做权限系统。
- 不做前端页面。
- 不对接公司真实保单系统。
- 不把示例工程直接声明为生产可用工程。

# 9. 不可变边界（Constraints / Non-goals）

明确禁止：

- 不生成 SDD 内部 Code Review HTML 报告。
- 不创建 `reports/code-review/YYYY-MM-DD/`。
- 不读取 Code Review HTML 模板作为本次 SDD 内部评审依据。
- 不改动无关历史功能代码。
- 不伪造人工确认记录。

补充：

- 本次所有确认均为“用户授权的模拟试跑确认”，不能等同生产需求审批。

# 10. Domain Mapping（领域映射）

| 业务概念 | 系统对象 | 来源 |
|---|---|---|
| 保单号 | `policyNo` | 请求入参 |
| 变更字段 | `ChangeFieldType` | 请求入参与枚举 |
| 变更前值 | `oldValue` | 请求入参 |
| 变更后值 | `newValue` | 请求入参 |
| 提交人 | `requester` | 请求入参 |
| 工单编号 | `workOrderId` | 系统生成 |
| 工单状态 | `WorkOrderStatus` | 系统生成 |

# 11. 依赖识别

## 内部依赖

- Spring Boot Web
- Spring Validation
- JUnit4
- Mockito
- Maven Surefire

## 外部依赖

- 无业务外部依赖。

## 数据依赖

- 本次使用内存仓储 `ConcurrentHashMap`，不依赖数据库。

# 12. 风险识别

## 技术风险

- Maven 实际运行在 Java 26，Mockito / Byte Buddy 默认不支持该 class file 版本，可能导致测试失败。
- 使用内存仓储只能验证流程，不具备生产持久化能力。

## 兼容风险

- SDD testing 规则偏 UAW 存量工程，和 Spring Boot 3 默认 JUnit5 风格存在适配成本。

## 交付风险

- 如果 SDD 资产根目录和代码工程根目录不显式区分，AI 容易扫描错范围。

## 数据风险

- 本次不落库，无生产数据风险。

## 风险重点（供 design 引用）

- 测试运行环境必须记录。
- 内存仓储必须标注为模拟实现。
- 模拟确认必须与真实人工确认区分。

# 13. 回滚策略

若试跑失败：

- 删除或暂停使用 `uaw-sdd-demo/` 示例工程。
- 保留失败记录作为 SDD 问题证据。
- 不将本次样板作为正式业务模板推广。

# 14. 验收标准（Acceptance Criteria）

- 创建工单接口 `POST /api/work-orders/policy-info-change` 可接收合法请求并返回 `201 Created`。
- 查询工单接口 `GET /api/work-orders/policy-info-change/{workOrderId}` 可返回已创建工单。
- `oldValue` 与 `newValue` 一致时返回业务错误。
- 重复待处理工单提交时返回业务错误。
- 请求必填字段缺失时返回参数校验错误。
- 服务层与接口层测试覆盖正常、异常、边界路径。
- `mvn test` 最终通过。
- SDD 内部 Code Review、Auto-fix、Unit Test Summary、Archive 均有记录。
- 输出 SDD 体系问题清单。

# Process Status

- Current Stage：Archive
- Stage Status：archived
- Last Completed Step：Spec 已确认并被 Design / Tasks / Implementation 使用
- Next Required Step：无，已归档
- Human Confirmation Required：no
- Allowed Next Action：作为本次试跑知识基线读取
- Forbidden Next Action：不得把“模拟确认”解释为正式人工评审通过
- Updated At：2026-05-28 17:06:26 +0800

# Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-28 16:35:00 +0800 | Spec | 装配 SDD 上下文并定义范围 | proposal-input.md、1.index.md、模板 | spec.md | 通过，模拟确认 | Design |
| 2026-05-28 17:06:26 +0800 | Spec | 回写试跑暴露的目录与环境风险 | Maven 环境、代码目录现状 | spec.md | 通过，进入归档 | Archive |
