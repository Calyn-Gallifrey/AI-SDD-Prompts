# 独立代码评审（Standalone Code Review）输入模板

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

# 2. Git Range 评审输入

> 当入口模式为 `STANDALONE_GIT_RANGE_REVIEW` 时必须填写本节。
> 该模式可作为正式合并前代码评审依据。

## 评审范围类型（Review Scope Type）

只能选择一个：

- branch diff
- commit list
- date range

填写：

- （=== 填写在这里 ===）

## 分支差异（Branch Diff）

- 基准分支（Base Branch）：
- 目标分支（Target Branch）：
- 是否排除 Merge Commit：`yes` / `no`
- 是否排除生成文件：`yes` / `no`

## Commit 清单

- Commit Hash：

## 日期范围（Date Range）

- 开始时间：
- 结束时间：
- 目标分支：
- 是否排除 Merge Commit：`yes` / `no`
- 是否排除生成文件：`yes` / `no`

---

# 3. Worktree 快照评审输入

> 当入口模式为 `STANDALONE_WORKTREE_SNAPSHOT_REVIEW` 时必须填写本节。
> 该模式只适用于未提交新工程、临时 demo、迁移前盘点。
> 该模式不得作为正式合并闸门。

## 目标路径（Target Path）

- （=== 填写工程目录或模块目录 ===）

## 是否包含未跟踪文件

- yes / no

## 基线（Baseline）

- none
- current HEAD
- specified ref：

## 是否作为正式合并 Gate

- no

说明：

- 若需要正式合并评审，必须先形成 Git range，再使用 `STANDALONE_GIT_RANGE_REVIEW`。
- 报告首页必须标明：`Scope Deviation: worktree snapshot, not Git range`。

---

# 4. 报告输出（必须填写）

## 报告输出目录

- （=== 填写在这里 ===）

推荐：

- `reports/code-review/YYYY-MM-DD/`
- `sdd2-features/<SprintN>/<feature-name>/reports/code-review/YYYY-MM-DD/`（仅限用户明确要求输出到 SDD 功能目录）

## 报告输出日期

- YYYY-MM-DD

---

# 5. 审核前自检

- [ ] 已选择唯一入口模式（Entry Mode）
- [ ] Git Range 模式已提供 branch / commit / date range
- [ ] Worktree Snapshot 模式已提供目标路径
- [ ] 已明确是否包含未跟踪文件
- [ ] 已明确报告输出目录
- [ ] 已明确报告输出日期
- [ ] 已确认本次 Standalone 报告不替代 SDD 内部 `code-review-findings.md`
