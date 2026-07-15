# SDD 代码评审发现（Code Review Findings）

> 针对一个冻结 SDD2 实现范围的不可变首次评审发现。修复状态只能记录在 `auto-fix-summary.md`。正文必须以简体中文为主体。

## 1. 评审信息

- 入口模式：`SDD_TASK_CODE_REVIEW`
- Feature ID：
- Attempt：
- 评审时间：
- 评审人角色：AI 代码评审人
- 结论：`passed` / `failed` / `blocked`
- 是否需要单元测试：`yes`

## 2. 冻结范围证据

- 仓库：
- 分支：
- Base Commit：
- Head Commit：
- Head Tree：
- 范围快照 SHA-256：
- Spec 修订/SHA-256：
- Design 修订/SHA-256：
- Tasks 修订/SHA-256：

| 变更文件 | 冻结 SHA-256/删除标记 | 是否已评审 | 说明 |
|---|---|---|---|
|  |  | `yes` / `blocked` |  |

## 3. 前置条件

| 检查项 | 结果 | 证据 |
|---|---|---|
| SDD2 控制校验 | `checked-pass` / `blocked` |  |
| 当前 Spec/Design/Tasks 批准 | `checked-pass` / `blocked` |  |
| 必需 Phase Review | `checked-pass` / `blocked` |  |
| 冻结范围当前有效且被允许 | `checked-pass` / `blocked` |  |
| 资产哈希当前有效 | `checked-pass` / `blocked` |  |

## 4. 强制评审类别

| 类别 | 结果 | 证据/Finding ID |
|---|---|---|
| 范围与可追溯性 | `checked-pass` / `checked-finding` / `blocked` |  |
| 正确性 | `checked-pass` / `checked-finding` / `blocked` |  |
| 兼容性 | `checked-pass` / `checked-finding` / `blocked` |  |
| 安全 | `checked-pass` / `checked-finding` / `blocked` |  |
| 事务与并发 | `checked-pass` / `checked-finding` / `blocked` |  |
| 集成 | `checked-pass` / `checked-finding` / `blocked` |  |
| 持久化 | `checked-pass` / `checked-finding` / `blocked` |  |
| 可维护性 | `checked-pass` / `checked-finding` / `blocked` |  |
| 可观测性 | `checked-pass` / `checked-finding` / `blocked` |  |
| 测试 | `checked-pass` / `checked-finding` / `blocked` |  |

记录 `passed` 或 `failed` 结论时，任何一行都不得处于未解决状态。

## 5. 评审发现

| ID | 严重度 | 是否阻塞 | 路径 | 符号/Diff 位置 | SDD/规则证据 | 问题与后果 | 必需修复 |
|---|---|---|---|---|---|---|---|
| CR-001 | P0/P1/P2 | `yes` / `no` |  |  |  |  |  |

没有问题时写：`当前冻结范围未发现可行动问题。`

## 6. 需求与测试影响

| 需求/验收项 | 生产符号 | 既有/必需测试源码 | 缺失场景/回归风险 |
|---|---|---|---|
|  |  |  |  |

## 7. Auto-fix 交接

- Findings 数量：P0= / P1= / P2= / 阻塞 P2=
- 是否需要 Auto-fix：`yes` / `no-fix-record-required`
- 最高优先级 Finding：
- 是否预计改变范围：`yes` / `no`
- 下一资产：`./auto-fix-summary.md`

即使无需修改代码，`auto-fix-summary.md` 也必须用证据记录 `not-required`。

## 8. 限制

| 限制 | 影响 | 是否阻塞 | 恢复方式 |
|---|---|---|---|
|  |  | `yes` / `no` |  |

## 9. Gate 记录

- Findings 资产 SHA-256：
- 范围快照 SHA-256：
- Gate 结果：`passed` / `failed` / `blocked`
- 可复现证据：
- 是否允许 Archive：否；后续 SDD2 Gate 仍为必需项

记录本资产后不得编辑它来反映修复。将控制权返回 `uaw-sdd-ai-coding`。
