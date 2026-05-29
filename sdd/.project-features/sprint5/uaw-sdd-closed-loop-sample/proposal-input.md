# UAW-SDD 新版闭环样板提案入口

> 样板用途声明：本目录用于展示 2026-05-28 更新后的 UAW-SDD 完整闭环结构。
> 本样板不对应真实业务代码、真实 Git Diff、真实 Code Review 或真实测试执行结果。
> 新功能可参考本目录的阶段、闸门、状态和审计写法，但不得把本文档中的示例证据当成真实交付证据。

## 1. 任务基本信息

- 功能名称：uaw-sdd-closed-loop-sample
- 功能类型：query
- 所属模块：sample
- 一句话目标：展示一个新版 UAW-SDD 功能从 proposal 到 archive 的完整闭环资产结构。
- 所在 sprint：sprint5
- 优先级：P1
- 风险等级：low

## 2. 变更识别信息

- 变更范围：Documentation Sample / Process Sample
- 禁止变更：不修改真实业务代码、不生成真实报告目录、不伪造真实测试结果。
- 输出目录：`.project-features/sprint5/uaw-sdd-closed-loop-sample/`

## 3. AI 知识底座路径

- AI 知识底座根目录：`.project-ai/`
- 索引文件：`.project-ai/context/1.index.md`
- 模板目录：`.project-ai/templates/`
- Code Review 规则：`.project-ai/rules/code-review/UAW-Code-Review.md`
- 测试规则：`.project-ai/rules/testing/`

## 4. 执行要求

本样板必须展示以下闭环：

```text
Proposal
→ Spec
→ Human Confirmation
→ Design
→ Human Confirmation
→ Tasks
→ Human Confirmation
→ Code Implementation
→ SDD_TASK_CODE_REVIEW
→ Review-driven Auto-fix
→ Unit Test Generation
→ Unit Test Summary
→ Archive
```

约束：

1. SDD 内部 Code Review 不读取 HTML 模板。
2. SDD 内部 Code Review 不生成 HTML 报告。
3. Archive 前必须记录 Code Review Findings、Auto-fix Summary、Unit Test Summary。
4. 所有检查项不得遗留空白未处理状态。
5. 每个核心文件必须包含 Process Status 和 Process Audit Trail。

## 5. 预期交付物

- `proposal-input.md`
- `spec.md`
- `design.md`
- `tasks.md`
- `archive.md`

## Process Status

- Current Stage: Archive
- Stage Status: archived
- Last Completed Step: Proposal captured and linked to sample closed-loop assets
- Next Required Step: None
- Human Confirmation Required: no
- Allowed Next Action: Use as process sample only
- Forbidden Next Action: Treat this sample as real implementation evidence
- Updated At: 2026-05-28 Asia/Shanghai

## Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-28 | Proposal | Create sample proposal | UAW-SDD updated rules | proposal-input.md | pass | Spec |
