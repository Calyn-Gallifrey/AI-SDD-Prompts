# Input Examples

本文件提供 uaw-code-review Standalone 模式的输入样例。SDD 模式由 `uaw-sdd-ai-coding` 触发，评审输入由 SDD 流程上下文提供。

## Standalone Git Range Review（独立 Git 范围评审）

```text
Entry Mode（入口模式）：STANDALONE_GIT_RANGE_REVIEW

Review Scope Type（评审范围类型）：branch diff

Base Branch（基准分支）：origin/develop

Target Branch（目标分支）：HEAD

Exclude Merge Commits（排除合并提交）：yes

Exclude Generated Files（排除生成文件）：yes

Report Output Directory（报告输出目录）：reports/code-review/2026-06-09/

Report Output Date（报告输出日期）：2026-06-09
```

## Standalone Worktree Snapshot Review（独立工作区快照评审）

```text
Entry Mode（入口模式）：STANDALONE_WORKTREE_SNAPSHOT_REVIEW

Review Scope Type（评审范围类型）：worktree snapshot

Target Path（目标路径）：/path/to/project

Include Untracked Files（包含未跟踪文件）：yes

Baseline（基准）：current HEAD

Formal Merge Gate（是否正式合并门禁）：no

Report Output Directory（报告输出目录）：reports/code-review/2026-06-09/

Report Output Date（报告输出日期）：2026-06-09
```
