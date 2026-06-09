# Input Examples

All standalone human input examples must use:

```text
English Field（中文字段）：example value
```

SDD mode is automatically triggered by `uaw-sdd-ai-coding`; it derives inputs from SDD assets and code changes.

## Java Unit Test（Java 单元测试）

Keep user input minimal. The skill must scan project files for build tool, Java version, Spring Boot version, test framework, changed files, existing test style, and UAW utility classes.

```text
Project Root（项目根目录）：/path/to/java-project

Test Target（测试目标）：本次变更代码

Validation Method（验证方式）：IDE

Actual Test Entry（实际执行入口）：IntelliJ run configuration: PolicyChangeWorkorderServiceTest

Special Notes（补充说明）：
不确定项目是 JUnit4 还是 JUnit5，请先自动扫描 pom.xml 和现有测试代码。
```

If the user cannot provide `Actual Test Entry（实际执行入口）`, continue by generating tests and mark execution as pending in Unit Test Summary. Do not fabricate a successful test run.
