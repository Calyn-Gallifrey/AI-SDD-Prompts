# Standalone Code Review 输入模板

> 本模板仅用于独立代码评审，不属于 SDD 功能任务链路。
> SDD 流程内代码评审必须继续使用 `SDD_TASK_CODE_REVIEW`，并且不得生成 HTML 报告。

---

# 1. 入口模式（必须填写）

只能选择一个：

- `STANDALONE_GIT_RANGE_REVIEW`
- `STANDALONE_WORKTREE_SNAPSHOT_REVIEW`

填写：

- （=== 填写在这里 ===）

---

# 2. Git Range Review 输入

> 当入口模式为 `STANDALONE_GIT_RANGE_REVIEW` 时必须填写本节。
> 该模式可作为正式合并前代码评审依据。

## Review Scope Type

只能选择一个：

- branch diff
- commit list
- date range

填写：

- （=== 填写在这里 ===）

## Branch Diff

- Base branch：
- Target branch：
- Exclude merge commits：yes / no
- Exclude generated files：yes / no

## Commit List

- Commit hashes：

## Date Range

- Start time：
- End time：
- Target branch：
- Exclude merge commits：yes / no
- Exclude generated files：yes / no

---

# 3. Worktree Snapshot Review 输入

> 当入口模式为 `STANDALONE_WORKTREE_SNAPSHOT_REVIEW` 时必须填写本节。
> 该模式只适用于未提交新工程、临时 demo、迁移前盘点。
> 该模式不得作为正式合并闸门。

## Target Path

- （=== 填写工程目录或模块目录 ===）

## Include Untracked Files

- yes / no

## Baseline

- none
- current HEAD
- specified ref：

## Formal Merge Gate

- no

说明：

- 若需要正式合并评审，必须先形成 Git range，再使用 `STANDALONE_GIT_RANGE_REVIEW`。
- 报告首页必须标明：`Scope Deviation: worktree snapshot, not Git range`。

---

# 4. 报告输出（必须填写）

## Report Output Directory

- （=== 填写在这里 ===）

推荐：

- `.project-features/<SprintN>/<feature-name>/reports/code-review/YYYY-MM-DD/`

## Report Output Date

- YYYY-MM-DD

---

# 5. 审核前自检

- [ ] 已选择唯一 Entry Mode
- [ ] Git Range 模式已提供 branch / commit / date range
- [ ] Worktree Snapshot 模式已提供 Target Path
- [ ] 已明确是否包含 untracked files
- [ ] 已明确 Report Output Directory
- [ ] 已明确 Report Output Date
- [ ] 已确认本次 Standalone 报告不替代 SDD 内部 `code-review-findings.md`
