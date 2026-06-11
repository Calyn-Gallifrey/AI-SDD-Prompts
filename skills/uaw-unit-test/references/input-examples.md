# Input Examples

本文件提供 uaw-unit-test Standalone 模式的 Java 单元测试输入样例。SDD 模式由 `uaw-sdd-ai-coding` 触发，并从 SDD 资产与代码变更中推导测试输入。

## Java Unit Test（Java 单元测试）

Standalone 模式仅要求用户提供无法稳定从项目文件扫描的信息；构建工具、Java 版本、Spring Boot 版本、测试框架、变更文件、现有测试风格和 UAW 工具类由 Skill 扫描识别。

```text
Project Root（项目根目录）：/path/to/java-project

Test Target（测试目标）：本次变更代码

Validation Method（验证方式）：IDE

Actual Test Entry（实际执行入口）：IntelliJ run configuration: PolicyChangeWorkorderServiceTest

Special Notes（补充说明）：
不确定项目是 JUnit4 还是 JUnit5，需先自动扫描 pom.xml 和现有测试代码。
```

无法提供 `Actual Test Entry（实际执行入口）` 时，可以先生成测试，并在 Unit Test Summary 中将执行状态记录为 pending；不得记录为已执行成功。
