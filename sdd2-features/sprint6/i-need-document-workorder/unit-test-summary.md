# unit-test-summary.md - i-need-document-workorder

## Unit Test Summary

Entry Mode：SDD_UNIT_TEST

Test Time：2026-06-11 14:42

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

## Unit Test Gate

Unit Test Gate Result：passed

Archive allowed：yes
