---
name: uaw-unit-test
description: 生成、更新、执行并总结以 Java 为主的 UAW 单元测试。用于独立单元测试任务，或 SDD2 Code Review 后的测试生成。SDD 模式采用两轮交接，确保已变更测试源码在执行和生成 Unit Test Summary 前重新冻结并完整复审。
---

# UAW 单元测试

## 核心契约

每项可访问且目标可识别的生产代码变更，都必须生成或更新真实单元测试源码。文字计划、评审备注、手工检查或单独的 `unit-test-summary.md` 永远不能替代测试实现。

读取 `references/testing-profile-routing.md`、`references/java/` 下选中的目标规则，以及 `references/templates/unit-test-summary-template.md`。

所有人类可读指令与新生成 Summary 遵循 `skills/uaw-sdd-ai-coding/references/language-policy.md`，以简体中文为主体。代码、依赖、Profile、命令和状态枚举保持精确。

不得为了适配偏好风格而新增或升级测试依赖。当前构建依赖和邻近可执行测试是主要约定。无法确认项目文件、目标代码、框架或可运行入口时，返回 `blocked`，并给出精确恢复信息。

## SDD 模式：两轮执行

### 第一轮：生成测试源码

从 `uaw-sdd-ai-coding` 接收：

- 当前 Feature、状态和冻结实现范围；
- 已批准 Spec、Design 和 Tasks；
- 不可变 Code Review Findings 和 Auto-fix Summary；
- 精确生产符号和已捕获测试路径模式。

在已批准路径下创建或更新测试，返回已变更测试路径和所选 Profile 证据。此时不得创建 Unit Test Summary。

测试源码变化会使旧范围失效。把控制权返回 `uaw-sdd-ai-coding`，由其冻结新的生产+测试快照，完整重跑 Code Review，并在同一快照上关闭 Auto-fix。

### 第二轮：执行并总结

只有 Code Review 在当前冻结范围为 `passed`，且 Auto-fix 在同一范围为 `passed` 或 `not-required` 后才能运行。验证至少一个已变更测试源码匹配已捕获测试路径。

使用项目真实支持的入口执行最小相关单元测试。生成 `unit-test-summary.md`，记录命令/环境、退出码、数量、失败/跳过、测试源码哈希和当前范围 SHA-256。把控制权返回主 Skill，执行确定性 Unit Test Gate 并等待人工 Unit Test Summary 批准。

`passed` 要求测试入口确实执行，并由退出码或结果证明成功。IDE、CI、Wrapper、本地 CLI 和项目脚本都可作为入口，但证据必须可复现。手工验证只能补充，不能通过 SDD Unit Test Gate。

## Standalone 模式

读取 `references/input-examples.md`。只向用户询问无法安全发现的事实：项目根目录、目标含糊时的测试目标，以及存在多个 Agent 无法使用的验证环境时的偏好。

先生成或更新测试源码，再尽可能执行。Standalone Summary 可以因明确原因记录为 `not-run`，并给出后续运行命令，但不得表述为已通过。

## 必需发现证据

记录：

- 构建工具/Wrapper 和模块；
- Java、存在时的 Spring Boot、JUnit Platform、Mockito、断言库；
- Surefire/Gradle 测试配置和 JDK 兼容性；
- 邻近可执行测试风格；
- 目标依赖和 Mock 边界；
- 只有目标代码使用时才记录 UAW 工具可用性。

## 输出

- 一个或多个新增/更新的单元测试源码路径；
- 已选测试 Profile 和目标规则；
- 可执行测试证据，或 `blocked`/`not-run` 结果；
- 只有源码生成后才创建 `unit-test-summary.md`。

成功 SDD 流程中，测试源码变更不得为 `none`。SDD 测试为 `failed`、`blocked` 或 `not-run` 时，禁止成功 Archive。

## 参考文件

- `references/testing-profile-routing.md`：基于证据选择框架/Profile。
- `references/java/`：按测试目标分类的生成规则。
- `references/templates/unit-test-summary-template.md`：Summary 与 Gate 证据。
- `references/input-examples.md`：仅用于 Standalone 输入示例。
