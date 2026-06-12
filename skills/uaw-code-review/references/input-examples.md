# Input Templates

本文件提供 uaw-code-review Standalone 模式的输入结构模板。SDD 模式由 `uaw-sdd-ai-coding` 触发，评审输入由 SDD 流程上下文提供。

## 使用规则

1. 尖括号 `<...>` 表示占位符，必须由真实评审范围替换。
2. 本文件不提供默认分支、默认路径、默认报告目录或默认报告日期。
3. Standalone 模式的评审范围必须来自用户明确指定的 Git range 或 worktree snapshot。

## Standalone Git Range Review（独立 Git 范围评审）

```text
Entry Mode（入口模式）：STANDALONE_GIT_RANGE_REVIEW

Review Scope Type（评审范围类型）：<branch diff | commit list | date range>

Base Branch（基准分支）：<base-branch-or-commit>

Target Branch（目标分支）：<target-branch-or-HEAD>

Exclude Merge Commits（排除合并提交）：<yes | no>

Exclude Generated Files（排除生成文件）：<yes | no>

Report Output Directory（报告输出目录）：<report-output-directory>

Report Output Date（报告输出日期）：<YYYY-MM-DD>
```

## Standalone Worktree Snapshot Review（独立工作区快照评审）

```text
Entry Mode（入口模式）：STANDALONE_WORKTREE_SNAPSHOT_REVIEW

Review Scope Type（评审范围类型）：worktree snapshot

Target Path（目标路径）：<absolute-project-or-module-path>

Include Untracked Files（包含未跟踪文件）：<yes | no>

Baseline（基准）：<current HEAD | specified baseline>

Formal Merge Gate（是否正式合并门禁）：<yes | no>

Report Output Directory（报告输出目录）：<report-output-directory>

Report Output Date（报告输出日期）：<YYYY-MM-DD>
```
