# Unit Test Summary Template

> 本模板是 `uaw-unit-test` 的强制输出模板。
> SDD 模式下必须输出到当前功能资产目录的 `unit-test-summary.md`。
> Standalone 模式下按用户指定目录输出；未指定目录时，在被测项目内创建可追溯的测试摘要文件。

---

# unit-test-summary.md - {feature-or-target-name}

## Unit Test Summary

Entry Mode：SDD_UNIT_TEST / STANDALONE_UNIT_TEST

Test Time：YYYY-MM-DD HH:mm

Project Root：`{project-root}`

Test Target：{test-target}

Validation Method：IDE / Wrapper / Local CLI / CI / Script / Manual / Other

Execution Environment：本机 / CI / 开发容器 / IDE / 其他

Actual Test Entry：`{command-or-ide-config-or-ci-job-or-script-or-manual-steps}`

## Auto-detected Profile

| Item | Result |
|---|---|
| Build Tool | Maven / Gradle / Maven Wrapper / Gradle Wrapper / Other |
| Java Compile Target | {java-version-or-unknown-with-reason} |
| Spring Boot Version | {spring-boot-version-or-not-applicable} |
| Test Framework | JUnit4 / JUnit5 / JUnit4 + Vintage / Legacy-Mockito / Other |
| Existing Test Style | {existing-test-style} |
| UAW Utility Dependency | UAW-Util / No-UAW-Util / Unknown |
| Changed Files Source | SDD tasks / git diff / worktree snapshot / user input |

## Selected Testing Profile

Selected Testing Profile：`UAW-JUnit4` / `SpringBoot-JUnit5` / `Legacy-Mockito` / `No-UAW-Util` / `Other`

Compatible Profile：`{optional-compatible-profile-or-none}`

Selection rationale：
- {reason-1}
- {reason-2}

Not Applicable Rules：
- {rule-or-profile-not-applicable-and-reason}

Test Framework Risks：
- {risk-or-none}

Additional Dependencies Required：yes / no

Dependency Notes：{dependency-change-needed-or-none}

## Test Files Added / Updated

Added：
- `{test-file-path-or-none}`

Updated：
- `{test-file-path-or-none}`

Existing Tests Referenced：
- `{existing-test-file-path-or-none}`

## Coverage Summary

Covered Scenarios：
- {covered-business-path}
- {covered-exception-or-boundary-path}

Code Review Fixes Covered：
- {code-review-finding-id-or-not-applicable}

Not Covered：
- {not-covered-scope-and-reason}

## Test Result

| Metric | Result |
|---|---|
| Build | SUCCESS / FAILED / NOT_RUN / NOT_APPLICABLE |
| Tests Run | {number-or-not-run} |
| Failures | {number-or-not-run} |
| Errors | {number-or-not-run} |
| Skipped | {number-or-not-run} |

## Warnings / Failure / Skipped Notes

Warnings：
- {warning-or-none}

Failures：
- {failure-summary-or-none}

Skipped：
- {skipped-summary-or-none}

If tests were not executed：
- Reason：{reason}
- Alternative Validation：{ide-ci-script-manual-or-none}
- Archive Impact：allowed / blocked / conditional

## Remaining Test Risks

- {remaining-risk-or-none}

## SDD Linkage

SDD Feature Directory：`{feature-directory-or-not-applicable}`

Source Artifacts：
- `proposal-input.md` / not applicable
- `spec.md` / not applicable
- `design.md` / not applicable
- `tasks.md` / not applicable
- `code-review-findings.md` / not applicable
- `auto-fix-summary.md` / not applicable

## Unit Test Gate

Unit Test Gate Result：passed / blocked / conditional / not applicable

Archive allowed：yes / no / conditional

Gate Notes：{notes-or-none}

---

# Template Rules

1. 不得删除模板章节；不适用的章节必须写 `not applicable` 并说明原因。
2. 测试成功结果必须来自实际执行记录；未执行测试必须写明未执行原因、替代验证方式和归档影响。
3. 必须记录 `Selected Testing Profile`、选择依据、不适用规则、测试框架风险和是否需要补充依赖。
4. 必须记录新增或修改的测试文件；没有新增或修改时必须写明原因。
5. 必须记录 warning / failure / skipped，即使测试最终通过。
6. SDD 模式下必须关联 `tasks.md`、`code-review-findings.md` 和 `auto-fix-summary.md`；如不适用必须说明原因。
