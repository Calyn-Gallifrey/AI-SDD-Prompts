# unit-test-summary.md - i-need-document-workorder

> HISTORICAL EXAMPLE ONLY (quarantined 2026-07-14): this file predates deterministic SDD2 control. Approval, reviewer, status, and business text below is legacy illustration, not valid gate evidence or reusable requirement input.

## Unit Test Summary

Entry Mode：SDD_UNIT_TEST

Test Time：2026-06-11 14:43

Project Root：`uaw-sdd-demo`

Test Target：本次 I need document 工单代码与既有工单回归测试

Validation Method：Local CLI

Execution Environment：本机

Actual Test Entry：`mvn test`

## Auto-detected Profile

| Item | Result |
|---|---|
| Build Tool | Maven |
| Java Compile Target | 17 |
| Spring Boot Version | 3.3.5 |
| Test Framework | JUnit4 + MockitoJUnitRunner + JUnit Vintage |
| Existing Test Style | Legacy-Mockito |
| UAW Utility Dependency | No-UAW-Util |

## Selected Testing Profile

Selected Testing Profile：`Legacy-Mockito`

Selection rationale：
- `pom.xml` 使用 Spring Boot 3.3.5，测试依赖包含 JUnit Vintage。
- 既有测试以 JUnit4 `@RunWith(MockitoJUnitRunner.class)` 和 Mockito 为主。
- 本次新增测试延续既有 Legacy-Mockito 风格，避免在同一 demo 工程内混用测试风格。

Not Applicable Rules：
- UAW 测试工具类规则不适用，当前 demo 未引入 UAW 单元测试工具类。
- JUnit5-only 规则不适用，当前工程以 JUnit4 + Vintage 兼容模式运行。

Test Framework Risks：
- JUnit Vintage 兼容模式可运行当前测试，但长期应在真实项目中统一 JUnit4 / JUnit5 策略。
- Byte Buddy 在新 JDK 下存在 `sun.misc.Unsafe` warning，当前未导致测试失败。

Additional Dependencies Required：no

## Test Files Added / Updated

- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/INeedDocumentWorkOrderServiceTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/INeedDocumentWorkOrderControllerTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/repository/InMemoryINeedDocumentWorkOrderRepositoryTest.java`

## Test Result

| Metric | Result |
|---|---|
| Build | SUCCESS |
| Tests Run | 36 |
| Failures | 0 |
| Errors | 0 |
| Skipped | 0 |

## Covered Scenarios

- Service 成功提交 `QUERY_DOCUMENT` 工单。
- Service 成功提交 `SEND_DOCUMENT` 工单并归一化邮箱。
- Service 拦截 `SEND_DOCUMENT` 缺少邮箱。
- Service 拦截空白文档类型。
- Service 拦截缺少 `requestType` 的直接调用。
- Controller 成功创建 I need document 工单并返回 HTTP 201。
- Controller validation 对缺少保单号、空文档类型返回 HTTP 400。
- Repository 保存和查询。
- 既有保单信息变更和受益人变更测试全部回归通过。

## Warnings

测试运行中仍存在 Byte Buddy 使用 `sun.misc.Unsafe` 的 JVM warning。该 warning 未导致测试失败。

## Remaining Test Risks

- 当前 demo 下游平台为 in-memory client，未覆盖真实 HTTP 协议、认证、超时、重试、错误码和幂等。
- 当前 demo 未接入真实保单归属、客户身份或坐席权限校验。
- 文档类型暂按字符串处理，真实项目应接入枚举、配置或下游字典。

## Unit Test Gate

Unit Test Gate Result：passed

Archive allowed：yes
