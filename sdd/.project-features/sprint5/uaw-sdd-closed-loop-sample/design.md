# UAW-SDD 新版闭环样板 Design

> 样板用途声明：本文件展示新版 `design.md` 如何承接已确认 spec。
> 本文件只设计样板资产结构，不对应真实业务代码。

## 1. 设计基本信息

- 功能名称：uaw-sdd-closed-loop-sample
- 功能类型：query
- 所属模块：sample
- 对应 spec：`./spec.md`
- design 文件路径：`./design.md`
- 当前状态：已确认

## 2. Spec 输入摘要

- 功能目标：展示新版 UAW-SDD 完整闭环资产结构。
- 变更范围：新增样板资产目录和五个核心文件。
- 不可变边界：不修改真实源码，不伪造真实评审或测试结果。
- 验收标准：路径、流程、检查项、状态区、审计区全部符合新版要求。

## 3. 结构设计

样板目录：

```text
.project-features/sprint5/uaw-sdd-closed-loop-sample/
├── proposal-input.md
├── spec.md
├── design.md
├── tasks.md
└── archive.md
```

## 4. 模块划分

| 层 / 模块 | 路径 | 说明 |
|---|---|---|
| 功能资产目录 | `.project-features/sprint5/uaw-sdd-closed-loop-sample/` | 新版 SDD 闭环样板 |
| 知识路由 | `.project-ai/context/1.index.md` | 中央路由和阶段闸门依据 |
| 代码评审规则 | `.project-ai/rules/code-review/UAW-Code-Review.md` | 双入口 Code Review 边界依据 |
| 测试规则 | `.project-ai/rules/testing/` | Unit Test Gate 规则依据 |

## 5. 请求流程 / Sequence Flow

1. Proposal 定义样板目的和禁止事项。
2. Spec 固定样板目标、边界和验收标准。
3. Design 固定样板资产结构和评审边界。
4. Tasks 展示阶段执行、检查项、Review Gate、Auto-fix Gate、Unit Test Gate。
5. Archive 归档样板结论和下一次使用方式。

## 6. Code Review 设计交接约束

SDD 内部 Code Review 必须体现：

- 入口为 `SDD_TASK_CODE_REVIEW`。
- 不读取 HTML 模板。
- 不生成 HTML 报告。
- Findings 只作为 Auto-fix 和 Unit Test 的输入。

Standalone Git 范围 Review 只在独立评审任务中使用，不参与本样板 archive 的强制前置条件。

## 7. 测试设计考量

本样板不涉及真实代码，因此 Unit Test Generation 记录为 not applicable。

替代验证方式：

- 文档路径一致性检查。
- 闸门关键词检查。
- 检查项无空白未处理状态。
- `git diff --check`。

## 8. 需传递给 Tasks 的执行约束

- 不新增真实源码文件。
- 不生成 HTML 报告。
- 不创建 `reports/code-review` 目录。
- `tasks.md` 和 `archive.md` 中所有检查项必须使用 `[x]` 或 `[✓]`。

## Process Status

- Current Stage: Archive
- Stage Status: archived
- Last Completed Step: Design confirmed for process sample
- Next Required Step: None
- Human Confirmation Required: no
- Allowed Next Action: Use as process sample only
- Forbidden Next Action: Treat design paths as real implementation files
- Updated At: 2026-05-28 Asia/Shanghai

## Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-28 | Design | Confirm sample asset structure and gates | spec.md | design.md | pass | Tasks |
