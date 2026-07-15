# 输入模板

本文件提供 `uaw-unit-test` Standalone 模式的 Java 单元测试输入结构。SDD 模式由 `uaw-sdd-ai-coding` 触发，并从 SDD 资产与代码变更中推导测试输入。

## 使用规则

1. 尖括号 `<...>` 表示占位符，必须由真实项目路径、测试目标和验证入口替换。
2. 本文件不提供默认测试类名、运行配置或项目路径。
3. SDD 模式不得把本文件占位符复制为 Unit Test Summary 的真实执行记录。
4. 人类可读输入说明和生成 Summary 必须以简体中文为主体；代码、类名、命令和配置 ID 保持原样。

## Java 单元测试

Standalone 模式只要求用户提供无法稳定从项目扫描获得的信息。构建工具、Java 版本、Spring Boot 版本、测试框架、变更文件、既有测试风格和 UAW 工具类由 Skill 扫描识别。

```text
Project Root（项目根目录）：<Java 项目绝对根目录>

Test Target（测试目标）：<被测的变更代码、Class、Method、Module 或 Feature>

Validation Method（单元测试执行方式）：<IDE | Wrapper | Local CLI | CI | Script | pending>

Actual Test Entry（实际执行入口）：<IDE Run Configuration、测试类、命令、CI Job、脚本路径，或 pending>

Special Notes（补充说明）：
<特殊约束、补充手工检查、已知风险、本地不可用工具，或“无”>
```

无法提供 `Actual Test Entry（实际执行入口）` 时，可先生成测试，并在 Unit Test Summary 中把执行状态记录为 `not-run`，不得记录为执行成功。手工检查只能作为补充证据，不能通过 SDD Unit Test Gate。
