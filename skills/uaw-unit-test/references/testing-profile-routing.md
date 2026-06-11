# Testing Profile Routing

> 本文件用于在生成或评审单元测试前选择测试规则 Profile。
> 生成或评审单元测试前必须先识别项目技术栈，测试规则不得跨技术栈套用。

---

# 1. 必须先识别的信息

在生成 tests 或执行 Code Review 前，必须读取并记录：

- `pom.xml` / `build.gradle`
- Spring Boot 版本
- Java 目标版本
- 测试依赖：JUnit4 / JUnit5 / Vintage / Mockito / AssertJ
- 可用验证方式：IDE / Wrapper / Local CLI / CI / Script / Manual / Other
- 实际测试执行入口：命令、IDE 配置名、CI Job、脚本路径或手工验证说明
- 是否存在 UAW 工具类：
  - CurrentUser
  - LogUtil
  - MyJsonUtil
  - MyStringUtil
  - MyCollectionUtil
  - Preconditions

---

# 2. Profile 选择

只能选择一个主 Profile，可附加一个兼容 Profile。

## UAW-JUnit4

适用：

- 存量 UAW 工程。
- 已使用 JUnit4、MockitoJUnitRunner、UAW 工具类。
- 项目已有测试大量采用 JUnit4 风格。

优先读取：

- `10.如何生成方法的单元测试.md`
- `29-1如何service的单元测试.md`
- `29-2如何生成静态static方法的单元测试.md`
- `29-3如何编写controller单元测试规范.md`
- `29-4如何创建ServiceStrategy的单元测试.md`

## SpringBoot-JUnit5

适用：

- Spring Boot 2.4+ / 3.x 新工程。
- `spring-boot-starter-test` 默认启用 JUnit Jupiter。
- 项目没有强制使用 JUnit4。

规则：

1. 优先使用 JUnit Jupiter：`org.junit.jupiter.api.Test`。
2. 优先使用 `@ExtendWith(MockitoExtension.class)`。
3. MockMvc 可使用 standalone 或 Spring test slice，需贴合现有工程风格。
4. 不得为适配 JUnit4 规则引入 Vintage，除非项目已明确要求。

## Legacy-Mockito

适用：

- 项目仍需 JUnit4，但运行 JDK 与 Mockito / Byte Buddy 兼容性存在风险。

规则：

1. 必须记录实际测试执行器及运行 JDK。
2. 如需 `-Dnet.bytebuddy.experimental=true`，必须写入 tasks、Unit Test Summary 和 archive。
3. 正式内网建议固定构建 JDK，不建议长期依赖 experimental 参数。

## No-UAW-Util

适用：

- 独立 demo、迁移工程、非 UAW 工程。
- 工程不存在 CurrentUser / LogUtil / MyJsonUtil 等工具类。

规则：

1. 不得硬性要求使用不存在的 UAW 工具类。
2. 必须在 design / tasks / review 中记录“UAW 工具类不适用”。
3. 如果后续迁入 UAW 工程，应重新评审工具类、用户上下文、日志与 JSON 规范。

---

# 3. 输出要求

生成或更新 Unit Test Summary 时，必须使用：

```text
skills/uaw-unit-test/references/templates/unit-test-summary-template.md
```

在 `design.md`、`tasks.md`、`code-review-findings.md` 或 Archive 中必须记录：

- Selected Testing Profile：
- 选择依据：
- 不适用规则：
- 测试框架风险：
- 是否需要补充依赖：
- Validation Method：IDE / Wrapper / Local CLI / CI / Script / Manual / Other
- Execution Environment：
- 实际执行入口：
- warning / failure / skipped 说明：

---

# 4. 验证方式规则

SDD 不强制绑定单一命令行工具。

允许的验证方式：

- IDE 内置 Maven / Gradle
- Maven Wrapper / Gradle Wrapper
- 本机 Maven / Gradle
- CI Pipeline
- 项目脚本
- 手工接口验证
- 其他经团队确认的验证方式

规则：

1. 不得把本机是否安装 `mvn` 或 `gradle` 作为进入 SDD 流程的前置条件。
2. 若当前环境无法执行命令，必须记录无法执行原因和替代验证方式。
3. 若使用 IDE 或 CI 验证，必须记录配置名、Job 名称或可追溯入口。
4. 若测试不适用，必须记录不适用原因、风险影响和是否允许 Archive。
5. 验证方式记录不得替代测试用例设计和 Code Review。

---

# 5. 禁止事项

1. 禁止未识别技术栈就生成测试。
2. 禁止为符合旧规则而引入不必要依赖。
3. 禁止在不存在 UAW 工具类的工程里使用 MyJsonUtil / CurrentUser 规则。
4. 禁止只记录最终测试通过，不记录测试环境 warning / failure。
5. 禁止将单一命令行工具作为所有工程的唯一验证路径。
