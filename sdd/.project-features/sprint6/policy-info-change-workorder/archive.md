# 功能级 Archive

# 1. 基本信息

- 功能名称：policy-info-change-workorder
- 功能类型：submit
- 所属模块：policy / workorder
- 所在 sprint：sprint6
- 对应目录：`.project-features/sprint6/policy-info-change-workorder/`
- 完成时间：2026-05-28 17:14:43 +0800
- 归档时间：2026-05-28 17:14:56 +0800
- 任务状态：已完成

# 2. 对应资产文件

- proposal：`./proposal-input.md`
- spec：`./spec.md`
- design：`./design.md`
- tasks：`./tasks.md`
- SDD 体系问题报告：`./sdd-system-findings.md`

# 3. 原始目标回顾

## 一句话目标

- 新增保单信息变更工单的创建与查询能力，用于验证 UAW-SDD 从提案到归档的完整闭环。

## 业务背景

- 公司内网准备投入 AI Coding，需要先用真实可执行工程验证 SDD 体系能否支撑完整工程交付。

## 本次最终是否达成

- 是。

## 若未完全达成，原因

- 不适用。本次按模拟边界达成；但不代表示例工程具备生产能力。

# 4. 最终实施结果

## 新增能力

- 新增保单信息变更工单创建接口。
- 新增保单信息变更工单查询接口。
- 新增新旧值一致校验。
- 新增待处理重复工单校验。
- 新增统一异常响应。
- 新增服务层与接口层测试。

## 修改能力

- 修改 Maven 配置，增加 Surefire 测试 JVM 参数，兼容当前 Maven Java 26 下 Mockito / Byte Buddy 运行。

## 删除 / 下线能力

- 无。

## 对外表现变化

- 新接口：`POST /api/work-orders/policy-info-change`
- 新接口：`GET /api/work-orders/policy-info-change/{workOrderId}`
- 字段变化：新增请求字段 `policyNo`、`changeFieldType`、`oldValue`、`newValue`、`requester`
- 行为变化：重复待处理变更请求会被拒绝

# 5. 最终结构落地结果

## 接口层

- 新增 Controller：`PolicyInfoChangeWorkOrderController`
- 新增 API：创建工单、查询工单

## 业务层

- 新增 Service：`PolicyInfoChangeWorkOrderService`
- 新增流程：参数后置业务校验、重复判断、实体保存、响应转换

## 数据层

- 新增 Repository：`PolicyInfoChangeWorkOrderRepository`
- 新增内存实现：`InMemoryPolicyInfoChangeWorkOrderRepository`
- SQL 变化：无

## 对象层

- 新增 DTO：`CreatePolicyInfoChangeWorkOrderRequest`
- 新增 DTO：`PolicyInfoChangeWorkOrderResponse`
- 新增 Entity：`PolicyInfoChangeWorkOrder`
- 新增 Enum：`ChangeFieldType`、`WorkOrderStatus`

## 集成层

- 无外部调用。

# 6. 主要变更文件清单

- `uaw-sdd-demo/pom.xml`
- `uaw-sdd-demo/.gitignore`
- `uaw-sdd-demo/README.md`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/PolicyInfoChangeWorkOrderRepository.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/InMemoryPolicyInfoChangeWorkOrderRepository.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/**`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderServiceTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderControllerTest.java`

# 7. 关键决策与取舍（高价值区）

## 为什么采用当前方案

- 独立 Spring Boot 工程能真实验证 Maven 编译、测试和依赖解析。
- 内存 Repository 能把验证重点放在 SDD 流程，而不是数据库环境准备。
- JUnit4 + Mockito 能贴近当前 UAW testing 规则，同时也暴露出该规则与现代 Spring Boot 默认测试栈的适配问题。

## 为什么没有采用其他方案

- 未使用真实数据库：本次目标是 SDD 流程验证，数据库会引入额外环境变量。
- 未使用 JUnit5：当前 UAW testing 规则偏 JUnit4，直接使用 JUnit5 会弱化对现有规则的验证。
- 未新增完整审批流：超出“新增保单信息变更工单创建与查询”的模拟范围。

## 哪些地方做了妥协

- 使用内存仓储替代真实持久化。
- 使用请求字段 `requester` 模拟当前用户上下文。
- 使用 Surefire JVM 参数兼容当前本地 Java 26，而不是强制切换 Maven JDK。

## 哪些方案被验证不可行

- 在当前 Maven Java 26 环境下，不做额外配置直接运行 Mockito 测试不可行；首次 `mvn test` 因 Byte Buddy 不支持 Java 26 class file 70 失败。

## 哪些存量资产被复用

- SDD context、templates、code-review rules。
- Spring Boot parent 管理的 Maven 依赖。

# 8. 当前仍然有效的边界

任务完成后，以下约束仍成立：

- 不改真实业务系统。
- 不接真实数据库。
- 不接外部保单系统。
- 不生成 SDD 内部 Code Review HTML 报告。
- 继续将本次工程视为 SDD 体系验证工程，而非生产工程。

# 9. 与原 Spec / Design 的偏差记录

| 类型 | 原计划 | 最终结果 | 原因 |
|---|---|---|---|
| 范围 | 新建 Spring Boot 工程并模拟工单能力 | 已完成 | 无偏差 |
| 设计 | Repository 使用内存实现 | 已完成 | 无偏差 |
| 技术实现 | Maven 测试应通过 | 首次失败后增加 Surefire 参数并通过 | Maven 实际运行 Java 26，Byte Buddy 默认不支持 |
| 交付节奏 | Code Review 后进入 Auto-fix 与 Unit Test | 已执行 | 无偏差 |
| 流程确认 | SDD 模板要求人工确认 | 本次使用“用户授权模拟确认” | 试跑场景没有正式人工审批环节 |

# 10. 质量结果

## Code Review 结果

- 结论：有条件通过，Auto-fix 后通过。
- P0：0
- P1：1，CR-001 Maven Java 26 / Byte Buddy / Mockito 测试兼容问题
- P2：1，CR-002 内存 Repository 不具备生产持久化能力
- Suggestion：1，CR-003 SDD testing 规则需要按技术栈 profile 化

## Review-driven Auto-fix 结果

- 已完成。
- 修复文件：`uaw-sdd-demo/pom.xml`
- 修复内容：增加 `maven-surefire-plugin` 配置，设置 `-Dnet.bytebuddy.experimental=true`
- 未修复问题及原因：
  - CR-002 不修复：内存仓储符合本次模拟边界。
  - CR-003 不修复：属于 SDD 体系优化，记录到 `sdd-system-findings.md`。

## Unit Test Summary

- pass
- 新增测试文件：
  - `PolicyInfoChangeWorkOrderServiceTest.java`
  - `PolicyInfoChangeWorkOrderControllerTest.java`
- 覆盖场景：
  - 创建成功
  - 新旧值一致
  - 重复待处理工单
  - 查询成功
  - 查询不存在
  - 请求参数校验失败
  - Controller 业务异常映射
- 未覆盖场景及原因：
  - 真实数据库：本次不接数据库
  - 权限审计：本次不接用户上下文
  - 外部系统：本次无外部依赖
- 最终验证命令：`mvn test`
- 最终验证结果：Tests run: 9, Failures: 0, Errors: 0, Skipped: 0
- 最终验证时间：2026-05-28 17:14:43 +0800

## 验证范围

- Unit Test：已执行
- Integration Test：不适用
- 手工验证：未执行，原因是本次验收以自动化测试为准
- 回归验证：独立工程全量测试通过

## 已知问题

- 本示例工程不是生产实现，内存仓储不会持久化。
- 本地 Maven 使用 Java 26 运行测试时仍会出现 Byte Buddy 动态 agent warning；测试通过但应在正式内网环境中固定 JDK。

# 11. 风险与遗留事项

## 当前风险

- SDD 体系缺少环境预检，正式使用时可能在不同开发机上出现测试结果不一致。
- SDD 体系缺少代码工程根目录字段，资产目录与代码目录分离时容易扫描错范围。
- SDD testing 规则对不同 Spring Boot / JUnit 技术栈适配不足。

## 未完成项

- 未将 SDD 体系问题修入核心模板。
- 未定义公司内网标准 JDK / Maven / 依赖缓存策略。
- 未建立模拟确认与真实人工确认的正式状态区分。

## 后续建议

- 先修 P0：工程根目录字段和环境预检闸门。
- 再修 P1：测试规则 profile 化、模拟确认状态、失败证据结构化。
- 最后修 P2：样板目录索引、Archive 模板阅读顺序、内网运行手册。

## 若继续演进，优先方向

- 把 `sdd-system-findings.md` 中的 P0 项回写到 `.project-ai/templates/` 与 `.project-ai/context/1.index.md`。
- 用公司真实服务模块再跑一次 SDD，验证规则是否仍过拟合示例工程。

# 12. 性能 / 稳定性复盘

- 查询性能是否符合预期：模拟数据量下符合预期。
- 是否出现慢 SQL：不适用，无 SQL。
- 外部依赖是否稳定：不适用，无外部依赖。
- 是否存在超时 / 重试问题：不适用。
- 是否建议后续优化：真实业务需使用数据库唯一约束或幂等键避免并发重复提交。

# 13. 回写资产记录

## 本次是否新增 / 修正规则

- 否。

涉及文件：

- 无。

## 本次是否更新上下文

- 否。

涉及文件：

- 无。

## 本次是否更新 Index

- 否。

涉及文件：

- 无。

## 本次是否优化模板

- 否。

涉及文件：

- 无。

说明：本次只输出问题报告，不直接修改核心 SDD 体系文件，避免把试跑发现与体系修复混在一个变更中。

# 14. 下一次 Enhancement / Refactor 阅读顺序

建议按以下顺序阅读：

1. 本文件 `archive.md`
2. `sdd-system-findings.md`
3. `spec.md`
4. `design.md`
5. 当前 Git 代码现状
6. `tasks.md`

原则：

1. Git 代码是实物基线。
2. 历史文档是知识基线。
3. 二者冲突，以 Git 为准。
4. 差异必须写入新 spec。

# 15. 下一次提案特别注意

## 最可能变化的点

- 从内存仓储切换到数据库。
- 从 JUnit4 切换到公司标准测试栈。
- 增加真实用户上下文、审计字段和权限控制。

## 最不建议再碰的区域

- 不建议在未修复 P0 体系问题前，把该样板直接复制到真实业务。

## 可直接复用的资产

- 分层目录结构。
- Service 业务校验示例。
- SDD Review / Auto-fix / Unit Test Summary 记录方式。

## 需要重新验证的假设

- 公司内网目标 JDK 版本。
- Maven 是否统一使用目标 JDK。
- 内网依赖仓库是否包含 Spring Boot 3.3.5 相关依赖。
- UAW 真实工程是否仍要求 JUnit4。

# 16. 归档质量自检

## 16.1 归档检查项标记规则执行结果

- [x] 基于最终确认版本编写：本次为模拟确认
- [x] 与当前 Git 代码一致：已按当前工作区记录
- [x] 已说明目标、边界、最终方案
- [x] 已记录关键决策与取舍
- [x] 已记录实施结果、风险、遗留问题
- [x] 已记录是否回写 rules / context / index / templates
- [x] 已给出下一次阅读顺序
- [x] 后续人员无需翻聊天记录即可接手

结论：

- 已满足本次模拟归档标准。

若未满足，缺失项：

- 无。

# 17. 最终结论

- 本次任务整体评价：功能工程与 SDD 闭环均已跑通，且暴露出正式内网推广前必须修复的流程问题。
- 是否建议作为同类功能参考样板：部分建议。可作为 SDD 试跑样板，不建议作为生产业务工程样板。
- 后续维护难度：medium
- 备注：最重要的结论不是示例功能本身，而是 SDD 体系需要补齐“代码工程根目录”和“环境预检”两个 P0 能力。

# 18. Code Review 归档证据

## 18.1 SDD 内部 Code Review 说明

本归档对应的是 SDD 流程内代码评审。

规则执行结果：

- [x] SDD 内部 Code Review 未生成 HTML 报告。
- [x] 不存在 `代码评审统计报告.html` 或个人代码评审报告路径。
- [x] 归档只记录 Code Review Findings、Auto-fix Summary、Unit Test Summary。
- [x] 如需独立代码评审报告，应另行使用 `Entry Mode: STANDALONE_GIT_RANGE_REVIEW`。

## 18.2 Code Review Findings

| 问题编号 | 严重程度 | 文件 | 问题摘要 | 处理结果 |
|---|---|---|---|---|
| CR-001 | P1 | `uaw-sdd-demo/pom.xml` | Maven Java 26 下 Mockito / Byte Buddy 首次测试失败 | 已修复 |
| CR-002 | P2 | `InMemoryPolicyInfoChangeWorkOrderRepository.java` | 内存仓储不适合生产 | 不修复，符合本次模拟边界 |
| CR-003 | Suggestion | SDD testing 规则 | 测试规则需按技术栈 profile 化 | 记录到体系问题报告 |

## 18.3 Auto-fix Summary

| 问题编号 | 修复文件 | 修复方式 | 是否完成 | 未完成原因 |
|---|---|---|---|---|
| CR-001 | `uaw-sdd-demo/pom.xml` | 增加 Surefire `-Dnet.bytebuddy.experimental=true` | 是 | 无 |
| CR-002 | 无 | 不修复 | 否 | 本次为模拟工程，不接生产持久化 |
| CR-003 | 无 | 不修复 | 否 | 属 SDD 体系优化 |

## 18.4 Unit Test Summary

| 测试文件 | 覆盖场景 | 结果 | 备注 |
|---|---|---|---|
| `PolicyInfoChangeWorkOrderServiceTest.java` | 创建成功、新旧值一致、重复提交、查询成功、查询不存在 | pass | 5 tests |
| `PolicyInfoChangeWorkOrderControllerTest.java` | 创建成功、参数校验失败、业务错误、查询成功 | pass | 4 tests |

## 18.5 Process Deviations

| Deviation | Reason | Approved By | Impact | Follow-up |
|---|---|---|---|---|
| 使用模拟确认替代人工确认 | 用户要求从头到尾模拟跑通 | 用户授权 | 不能作为真实审批证据 | 增加 SDD 模拟模式字段 |
| 使用 Surefire 参数兼容 Java 26 | 本地 Maven 实际使用 Java 26 | 执行代理 | 测试可通过但仍提示动态 agent warning | 正式内网固定 Maven JDK |
| 使用内存仓储 | 降低流程验证环境成本 | spec / design 模拟边界 | 非生产实现 | 真实业务补 DB 设计 |

归档判断：

- [x] Code Review Findings 已输出
- [x] Auto-fix 已完成或明确不需要
- [x] Unit Test Summary 已完成
- [x] 所有偏差已记录
- [x] spec/design/tasks 的 Process Status 已更新

# Process Status（强制｜流程闸门）

- Current Stage：Archive
- Stage Status：archived
- Last Completed Step：archive.md 生成
- Next Required Step：根据体系问题报告修订 SDD
- Human Confirmation Required：no
- Allowed Next Action：读取 `sdd-system-findings.md` 并制定修复计划
- Forbidden Next Action：不得把本次模拟确认当作正式人工确认
- Updated At：2026-05-28 17:14:56 +0800

# Process Audit Trail（强制｜过程审核轨迹）

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-28 16:30:00 +0800 | Proposal | 启动模拟 SDD 流程 | 用户请求 | proposal-input.md | 通过 | Spec |
| 2026-05-28 16:35:00 +0800 | Spec | 定义范围和验收 | proposal-input.md | spec.md | 通过，模拟确认 | Design |
| 2026-05-28 16:40:00 +0800 | Design | 设计工程结构和数据流 | spec.md | design.md | 通过，模拟确认 | Tasks |
| 2026-05-28 16:45:00 +0800 | Tasks | 拆解施工任务 | design.md | tasks.md | 通过，模拟确认 | Implementation |
| 2026-05-28 16:55:00 +0800 | Implementation | 实现代码和测试 | tasks.md | `uaw-sdd-demo/` | 完成 | Code Review |
| 2026-05-28 17:00:00 +0800 | Code Review | 执行 SDD_TASK_CODE_REVIEW | 代码与 SDD 资产 | Findings | 有条件通过 | Auto-fix |
| 2026-05-28 17:03:00 +0800 | Auto-fix | 修复 CR-001 | Findings | `pom.xml` | 完成 | Unit Test |
| 2026-05-28 17:14:43 +0800 | Unit Test | 执行 `mvn test` | 修复后代码 | 测试结果 | 9 tests pass | Archive |
| 2026-05-28 17:14:56 +0800 | Archive | 生成归档 | 全部资产 | archive.md | 完成 | None |
