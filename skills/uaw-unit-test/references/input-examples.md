# Input Templates

本文件提供 uaw-unit-test Standalone 模式的 Java 单元测试输入结构模板。SDD 模式由 `uaw-sdd-ai-coding` 触发，并从 SDD 资产与代码变更中推导测试输入。

## 使用规则

1. 尖括号 `<...>` 表示占位符，必须由真实项目路径、测试目标和验证入口替换。
2. 本文件不提供默认测试类名、默认运行配置或默认项目路径。
3. SDD 模式下不得复制本文件中的占位符作为 Unit Test Summary 的真实执行记录。

## Java Unit Test（Java 单元测试）

Standalone 模式仅要求用户提供无法稳定从项目文件扫描的信息；构建工具、Java 版本、Spring Boot 版本、测试框架、变更文件、现有测试风格和 UAW 工具类由 Skill 扫描识别。

```text
Project Root（项目根目录）：<absolute-java-project-root>

Test Target（测试目标）：<changed code, class, method, module, or feature under test>

Validation Method（单元测试执行方式）：<IDE | Wrapper | Local CLI | CI | Script | pending>

Actual Test Entry（实际执行入口）：<IDE run configuration, test class, command, CI job, script path, or pending>

Special Notes（补充说明）：
<special constraints, supplemental manual checks, known risks, unavailable local tools, or none>
```

无法提供 `Actual Test Entry（实际执行入口）` 时，可以先生成测试，并在 Unit Test Summary 中将执行状态记录为 `not-run`；不得记录为已执行成功。手工检查只能作为补充证据，不能通过 SDD Unit Test Gate。
