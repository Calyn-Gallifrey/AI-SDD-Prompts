# UAW-SDD 新版闭环样板 Tasks

> 样板用途声明：本文件展示新版 `tasks.md` 如何记录执行、检查、评审、修复和测试闸门。
> 本文件中的 Findings、Auto-fix 和 Unit Test Summary 均为流程示例，不代表真实代码评审或真实测试执行。

## 1. 基本信息

- 功能名称：uaw-sdd-closed-loop-sample
- 功能类型：query
- 所属模块：sample
- 对应 spec：`./spec.md`
- 对应 design：`./design.md`
- tasks 文件路径：`./tasks.md`
- 执行模式：standard
- 当前状态：archived

## 2. 输入确认

- [x] proposal-input.md 已存在。
- [x] spec.md 已确认。
- [x] design.md 已确认。
- [x] 当前代码扫描不适用：本样板不对应真实源码修改。
- [x] enhancement / refactor 历史资产不适用：本样板为新建流程样板。

## 3. 执行总原则

- [x] 严格按 spec 范围施工：仅创建样板资产。
- [x] 严格按 design 落位施工：只在样板目录下生成五个核心文件。
- [x] 不改真实业务代码。
- [x] 不生成 Standalone HTML 报告。
- [x] 不创建 `reports/code-review` 目录。

## 4. Phase 拆解

## Phase 1：资产结构施工

输出物：

- `proposal-input.md`
- `spec.md`
- `design.md`
- `tasks.md`
- `archive.md`

检查项：

- [x] 文件均落在 `.project-features/sprint5/uaw-sdd-closed-loop-sample/`。
- [x] 未在约定外目录生成流程资产。
- [x] 未修改真实业务代码。

## Phase 2：流程闸门施工

检查项：

- [x] Standard Lane 包含 `SDD_TASK_CODE_REVIEW`。
- [x] Review-driven Auto-fix Gate 已记录。
- [x] Unit Test Gate 已记录。
- [x] Archive Gate 已记录。

## Phase 3：交付整理

检查项：

- [x] Code Review Findings 已输出为示例证据。
- [x] Auto-fix Summary 已输出为示例证据。
- [x] Unit Test Summary 已输出为 not applicable，并说明原因。
- [x] Process Status 已更新。
- [x] Process Audit Trail 已更新。

## 5. Code Review Gate

入口模式：

```text
Entry Mode: SDD_TASK_CODE_REVIEW
Feature Directory: .project-features/sprint5/uaw-sdd-closed-loop-sample/
SDD Artifacts:
- ./proposal-input.md
- ./spec.md
- ./design.md
- ./tasks.md
```

说明：以上信息由 SDD 流程上下文等价提供，不要求用户手动填写。

SDD 内部 Code Review 输出规则：

- [x] 不读取 HTML 模板。
- [x] 不生成 HTML 报告。
- [x] 不创建 `reports/code-review` 目录。
- [x] 直接输出 Code Review Findings。

## 5.1 Code Review Findings

| 问题编号 | 严重程度 | 文件 | 方法 / 类 | 问题摘要 | 修复建议 | 是否阻塞 |
|---|---|---|---|---|---|---|
| SAMPLE-CR-001 | Suggestion | `tasks.md` | 不适用 | 样板必须持续声明不可作为真实执行证据 | 在样板文件顶部保留用途声明 | no |

## 5.2 Code Review 结果

- Code Review 结论：通过
- P0 数量：0
- P1 数量：0
- P2 数量：0
- Suggestion 数量：1
- 是否需要 Review-driven Auto-fix：yes
- Fix Scope：样板用途声明和流程边界文字
- Files allowed to modify：本样板目录内五个 Markdown 文件
- Files forbidden to modify：真实业务源码、HTML 报告模板、旧版样板目录
- Unit tests required：no
- Archive allowed：yes after Auto-fix and Unit Test Summary

## 6. Review-driven Auto-fix Gate

## 6.1 修复结果

- [x] Fixed Issues：SAMPLE-CR-001
- [x] Modified Files：本样板目录内五个 Markdown 文件
- [x] Test Files Added / Updated：不适用，本样板不对应真实代码
- [x] Issues Not Fixed：无
- [x] Remaining Risks：使用者可能误把示例证据当真实证据，已通过用途声明控制

## 7. Unit Test Gate

## 7.1 测试规则来源

- `.project-ai/rules/testing/`

## 7.2 单元测试要求

- [x] 核心业务路径不适用：本样板无真实业务代码。
- [x] 异常路径不适用：本样板无真实业务代码。
- [x] 边界条件不适用：本样板无真实业务代码。
- [x] Code Review 修复点已覆盖：通过文档一致性检查覆盖。
- [x] 测试命名、Mock、断言不适用：未生成测试代码。

## 7.3 Unit Test Summary

- 新增测试文件：无
- 修改测试文件：无
- 覆盖场景：文档路径、流程闸门、检查项状态、用途声明
- 未覆盖场景及原因：真实 Java 单测不适用，本样板不对应真实源码修改
- 测试结论：not applicable

## 8. Archive Gate

- [x] spec.md 最终状态已更新。
- [x] design.md 最终状态已更新。
- [x] tasks.md 最终状态已更新。
- [x] Code Review 已完成。
- [x] Review-driven Auto-fix 已完成。
- [x] Unit Test Summary 已完成并记录 not applicable 原因。

## Process Status

- Current Stage: Archive
- Stage Status: archived
- Last Completed Step: Archive Gate passed for process sample
- Next Required Step: None
- Human Confirmation Required: no
- Allowed Next Action: Use as process sample only
- Forbidden Next Action: Use sample Findings as real review evidence
- Updated At: 2026-05-28 Asia/Shanghai

## Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-28 | Tasks | Generate sample task plan and gates | spec.md, design.md | tasks.md | pass | SDD_TASK_CODE_REVIEW |
| 2026-05-28 | SDD_TASK_CODE_REVIEW | Produce sample Findings | tasks.md | SAMPLE-CR-001 | pass | Review-driven Auto-fix |
| 2026-05-28 | Auto-fix | Preserve sample disclaimer and boundaries | SAMPLE-CR-001 | Auto-fix Summary | pass | Unit Test Summary |
| 2026-05-28 | Unit Test | Record not applicable reason | testing rules | Unit Test Summary | pass | Archive |
