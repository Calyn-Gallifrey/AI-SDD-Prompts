---
name: uaw-code-review
description: 以三种明确模式之一评审 UAW 代码变更：使用固定 SDD2 范围并输出 Markdown Findings 的 SDD_TASK_CODE_REVIEW、输出 HTML 报告的独立 Git Range 评审，或输出非正式合并 Gate HTML 报告的独立 worktree 快照评审。用于 SDD2 自动代码评审，或用户直接要求评审分支、Commit、日期范围、项目、目录和未提交代码时。
---

# UAW 代码评审

## 只选择一种模式

- `SDD_TASK_CODE_REVIEW`：由 `uaw-sdd-ai-coding` 调用，只输出 `code-review-findings.md`。
- `STANDALONE_GIT_RANGE_REVIEW`：用户直接指定明确 Git Range，输出 HTML 汇总和开发者报告。
- `STANDALONE_WORKTREE_SNAPSHOT_REVIEW`：用户直接指定目录/未提交快照，输出明确标注为非正式合并 Gate 的 HTML 报告。

读取 `references/code-review-rules.md` 并遵循所选模式。禁止跨模式混用输入、Gate 或输出。

所有人类可读指令和新生成报告必须遵循 `skills/uaw-sdd-ai-coding/references/language-policy.md`，以简体中文为主体。路径、代码、命令、枚举和外部契约原文保持精确。

## SDD 模式

要求 SDD 上下文提供全部以下输入：

- Feature 目录和 `.sdd2/feature-state.json`；
- 当前已批准的 `spec.md`、`design.md` 和 `tasks.md`；
- 全部必需人工 Phase Review；
- 包含当前冻结快照的 `.sdd2/implementation-scope.json`；
- 精确变更文件清单和输出路径。

评审前运行 SDD2 控制校验器。实现范围只能使用冻结清单和哈希，不得根据上游漂移、`git status` 或 Feature 目录推断。输入缺失或过期时返回 `blocked`，不得降级为 Standalone 模式。

不得读取 HTML 模板、创建 `reports/code-review`、修复代码或生成测试/Archive 内容。使用 `references/templates/sdd-code-review-findings-template.md` 写入不可变的首次 Findings，再把控制权返回 `uaw-sdd-ai-coding` 执行 Auto-fix。

每个强制评审类别都必须包含证据。生产代码变更后续始终需要单元测试源码工作。

## Standalone 模式

读取 `references/input-examples.md`，只询问缺失的必需范围字段。

Git Range 模式在评审前冻结 Base/Head Commit ID 和 Diff Hash。Worktree 模式冻结 HEAD、目标路径、变更/未跟踪文件哈希和快照哈希。不得静默扩展任一范围。

使用以下模板生成报告：

- `references/templates/summary-report-template.html`
- `references/templates/personal-report-template.html`

Standalone 评审不执行 SDD Gate；除非用户另行明确要求实现，否则绝不自动修复代码。

## 参考文件

- `references/code-review-rules.md`：评审模式、范围捕获、检查项、严重度和结论的权威规则。
- `references/input-examples.md`：Standalone 输入结构。
- `references/templates/sdd-code-review-findings-template.md`：仅用于 SDD 的 Markdown 输出。
- `references/templates/standalone-review-input-template.md`：Standalone 范围规范化。
- HTML 模板：仅用于 Standalone 输出。
