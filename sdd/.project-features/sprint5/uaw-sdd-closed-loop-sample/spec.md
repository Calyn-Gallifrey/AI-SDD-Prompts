# UAW-SDD 新版闭环样板 Spec

> 样板用途声明：本文件展示新版 `spec.md` 的边界、验收和流程状态写法。
> 本文件不对应真实业务需求，不得作为真实代码实现依据。

## 1. 基本信息

- 功能名称：uaw-sdd-closed-loop-sample
- 功能类型：query
- 所属模块：sample
- 所在 sprint：sprint5
- 优先级：P1
- 风险等级：low
- 对应 proposal：`./proposal-input.md`
- spec 文件路径：`./spec.md`
- 当前状态：confirmed

## 2. Proposal 输入摘要

## 一句话目标

展示新版 UAW-SDD 完整闭环资产结构。

## 提案原始范围

- 创建一套仅用于流程说明的样板资产。
- 覆盖 Proposal、Spec、Design、Tasks、Code Review、Auto-fix、Unit Test Summary、Archive。
- 不修改真实源码。

## 提案禁止变更项

- 不伪造真实代码变更。
- 不伪造真实测试结果。
- 不读取或使用 Standalone HTML 报告模板。

## 3. Context Assembly

## Base Context

- `.project-ai/context/1.index.md`
- `.project-ai/templates/1.proposal-input-template.md`
- `.project-ai/templates/2.spec-template.md`
- `.project-ai/templates/3.design-template.md`
- `.project-ai/templates/4.tasks-template.md`
- `.project-ai/templates/5.archive-template.md`

## Conditional Context

- 历史功能资产：不适用，本样板为新建流程样板。
- 外部依赖背景：不适用。
- 兼容性背景：不适用。

## 4. 当前现状

- 已存在旧版样板：`.project-features/sprint5/agreement-information-query/`
- 旧版样板已标注为 2026-05-28 更新前资产。
- 当前缺少一套展示新版闭环的独立样板目录。

## 5. 功能目标

本次必须达成：

- 展示新版标准流程的阶段顺序。
- 展示 SDD 内部 `SDD_TASK_CODE_REVIEW` 与 Standalone 报告评审的边界。
- 展示 Auto-fix 和 Unit Test Summary 的归档证据写法。
- 展示 Process Status 和 Process Audit Trail 的落位方式。

## 6. 变更范围

## In Scope

- 新增样板功能资产目录。
- 新增五个样板核心文件。
- 使用示例数据展示流程闭环。

## Out of Scope

- 真实业务代码实现。
- 真实 Git Diff 代码评审。
- 真实单元测试执行。
- HTML 评审报告生成。

## 7. 验收标准

## 功能验收

- 样板目录包含五个核心文件。
- 五个核心文件均声明样板用途和不可作为真实证据。
- 流程顺序包含 `SDD_TASK_CODE_REVIEW`、Review-driven Auto-fix、Unit Test Summary。

## 技术验收

- 不出现旧版 index 路径。
- 不出现泛化 Code Review 流程链路。
- 不存在未处理的空白检查项。
- 每个核心文件包含 Process Status 和 Process Audit Trail。

## 8. 需传递给 Design 的约束

- Design 只设计样板资产结构，不设计真实代码。
- Design 必须展示 SDD 内部评审和 Standalone 评审边界。
- Design 必须说明 Unit Test 不适用时的替代验证方式。

## Process Status

- Current Stage: Archive
- Stage Status: archived
- Last Completed Step: Spec confirmed for process sample
- Next Required Step: None
- Human Confirmation Required: no
- Allowed Next Action: Use as process sample only
- Forbidden Next Action: Use as real feature specification
- Updated At: 2026-05-28 Asia/Shanghai

## Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-28 | Spec | Confirm sample scope and non-goals | proposal-input.md | spec.md | pass | Design |
