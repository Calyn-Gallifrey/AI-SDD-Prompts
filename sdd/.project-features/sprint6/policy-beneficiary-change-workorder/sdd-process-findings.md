# SDD 流程试跑问题报告

# 1. 结论

本次从“开发个人简要设计 -> proposal-input -> spec -> design -> tasks -> 代码生成 -> SDD 内部 Code Review -> Auto-fix -> Unit Test -> Archive”跑通了完整链路。

代码侧未发现 P0 / P1 阻断问题；发现 1 个 P2 测试覆盖缺口，已通过 Review-driven Auto-fix 修复。

流程侧存在若干可改进点，主要集中在需求来源追溯、每个 Phase 的人工审核记录、过程状态同步、测试 Profile 与验证方式记录。按用户约束，本报告只列问题和建议，不修改 SDD 体系模板。

# 2. 已确认结果

- 已生成开发个人简要设计：`developer-brief-design.md`
- 已生成 proposal：`proposal-input.md`
- 已生成并审核 spec：`spec.md`
- 已生成并审核 design：`design.md`
- 已生成并执行 tasks：`tasks.md`
- 已实现功能代码与单元测试
- 已执行 SDD 内部 Code Review，未生成 HTML 报告
- 已完成 Auto-fix
- 已完成 Unit Test Summary
- 已生成归档：`archive.md`

# 3. 代码审核问题

| 编号 | 严重程度 | 分类 | 依据 | 处理状态 |
|---|---|---|---|---|
| CR-BEN-001 | P2 | 测试覆盖 | 初版 Service 测试 mock 了 Repository，只能证明 Service 调用，不能直接证明 Repository business key 去重 | 已补充 `InMemoryPolicyBeneficiaryChangeWorkOrderRepositoryTest.java` |

当前代码剩余风险：

- demo 使用内存仓储，不代表真实 DB 并发和事务能力。
- 证件号只做脱敏演示，未做真实证件格式校验。
- 正式内网 UAW 工程需要重新接入 CurrentUser、日志、审计、权限和数据库约束。

# 4. SDD 流程问题

| 编号 | 严重程度 | 问题 | 依据与影响 | 建议 |
|---|---|---|---|---|
| SDD-F-001 | P1 | proposal 对“开发个人简要设计来源”的追溯字段不够显式 | 用户真实用法是先写个人简要设计再生成 proposal；本次需要在 proposal 中手工记录来源，否则后续 reviewer 很难判断 proposal 是否忠实承接原始简设 | 在 proposal 模板中增加“简要设计来源 / 文件路径 / 生成依据”字段，需用户确认后再改体系 |
| SDD-F-002 | P1 | 各阶段 Process Status 容易出现历史状态滞后 | spec/design/proposal 生成时会写 Next Required Step；流程后续推进后，如果不回写，早期文件会长期停留在旧状态 | 明确是只维护当前阶段状态，还是 Archive 时统一回写全链路状态；需用户确认策略 |
| SDD-F-003 | P2 | tasks 中 Phase 级人工审核记录不够标准化 | 用户要求 tasks 的每个 phase 都人工审核；当前可记录，但没有统一表格字段约束 reviewer、时间、结果、问题编号 | 可在 tasks 模板中增加 Phase Review 表；需用户确认后再改体系 |
| SDD-F-004 | P2 | SDD 资产目录与代码工程目录分离时，扫描根目录仍需人工强调 | 本仓库中 SDD 位于 `sdd/`，代码工程位于 `uaw-sdd-demo/`；若 proposal 未显式写清，AI 可能扫描错目录 | 保留“代码工程根目录”字段并要求 proposal 必填实际工程路径 |
| SDD-F-005 | P2 | 测试 Profile 的选择需要更强制地落入 tasks / archive | 当前 demo 是 Spring Boot 3.3.5 + JUnit4 Vintage，容易和默认 JUnit5 判断冲突；本次手工记录后才清楚 | tasks / archive 中固定记录 Testing Profile、版本、依赖、风险 |
| SDD-F-006 | P2 | 验证命令不应绑定单一环境 | 用户已指出不能假设所有电脑都有 shell Maven；本次实际使用 `mvn test`，但正式体系应允许记录 IDE Maven、CI、wrapper 或本地命令 | 将“实际验证方式”作为记录字段，而不是把 `mvn` 作为硬性预检 |
| SDD-F-007 | P2 | SDD 内部 Code Review Findings 缺少默认独立 Markdown 产物约定 | 当前可以写入 tasks/archive，但如果需要审计检索，缺少统一文件名会降低可追溯性 | 可考虑约定 `code-review-findings.md`，但只有用户确认后再改体系 |

# 5. 风险与待确认点

- 待确认：正式内网使用时，是否要求早期 proposal/spec/design 的 Process Status 在 Archive 时回写为最终状态。
- 待确认：是否需要把 Phase 级人工审核做成模板强制字段。
- 待确认：是否需要新增 SDD 内部 Code Review 的 Markdown Findings 文件名约定。
- 待确认：测试验证是否只记录实际方式，不强制 shell Maven。

# 6. 下一步建议

## P0

- 暂无必须立即阻断上线前使用的 P0 流程问题。

## P1

- 先确认 SDD-F-001 和 SDD-F-002 的处理策略：proposal 是否强制记录“个人简要设计来源”，以及 Archive 时是否需要回写全链路 Process Status。

## P2

- 再确认是否把 Phase Review、Testing Profile、实际验证方式、Code Review Findings 文件名约定纳入模板。确认后再改 `.project-ai` 体系文件。
