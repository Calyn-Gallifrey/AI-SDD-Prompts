# Feature 实现任务（Tasks）

> Tasks 批准后成为不可变实现计划。运行进度、Phase Review、快照和事件保存在 `.sdd2/`；不得编辑本文件来叙述执行过程。正文必须以简体中文为主体。

## 1. 基本信息与已批准输入

- Feature ID：
- 功能名称：
- 所属模块：
- 已批准 Spec 修订/SHA-256：
- 已批准 Design 修订/SHA-256：
- Design 批准记录哈希：
- Tasks 修订：

## 2. 交付边界

### 目标


### 允许路径

```text
<精确且受限的路径模式>
```

### 禁止路径

```text
<路径模式>
```

### 测试路径模式

```text
<精确且受限的测试源码路径模式>
```

### 非目标


## 3. 前置条件

| 检查项 | 证据 | 结果 |
|---|---|---|
| 当前 Proposal/Spec/Design 修订已记录 | 修订/哈希 | `verified` / `blocked` |
| Spec 和 Design 批准绑定当前哈希 | 批准记录哈希 | `verified` / `blocked` |
| 已检查当前代码基线 | Commit + 符号 | `verified` / `blocked` |
| 路由规则/上下文当前有效且可追溯 | 来源记录 | `verified` / `blocked` |
| 范围模式足够窄且互不冲突 | 路径清单 | `verified` / `blocked` |
| 可识别测试框架/Profile | 构建/测试证据 | `verified` / `blocked` |

Tasks 批准前每行都必须为 `verified`。`blocked` 必须先解决，不得在此留下未来阶段占位符。

## 4. Phase 计划

| Phase ID | 目标 | 输入 | 精确文件/符号 | 操作 | 验证 | 依赖 | Phase Review |
|---|---|---|---|---|---|---|---|
| Phase1 |  |  |  |  |  |  | 必需人工审核 |

规则：

1. 每个 Phase 产生一个完整、可评审的变更。
2. 每个文件都必须位于允许路径内，并映射到已批准 Design 元素。
3. 不得把无关清理或 Refactor 与 Feature 工作混合。
4. 每个 Phase 实现后停止；只有新的明确人工 Phase Review 批准被持久化后，才能开始下一 Phase。
5. Phase 如变为不需要，必须通过正常资产修订和重新批准更新 Design 与 Tasks，不得静默跳过。
6. 生产代码变更必须包含测试源码 Phase，不得标记为不适用。

## 5. 详细任务

### Phase1

- 目标：
- 前置条件：
- 文件/符号：
- 有序编辑步骤：
- 复用的既有工具/约定：
- 错误、安全和事务要求：
- 新增/更新测试：
- 预期验证证据：
- 完成标准：
- 明确禁止事项：

为计划中的每个 Phase ID 重复本节。

## 6. 需求可追溯性

| Spec 需求/验收项 | Design 所有者 | Phase/任务 | 生产符号 | 测试目标 |
|---|---|---|---|---|
| FR-01 / AC-01 |  |  |  |  |

每项已批准需求和验收标准都必须映射到实现与测试工作；否则在 Tasks 批准前明确标记为阻塞。

## 7. 实现完成检查

这是确定性的就绪检查，不是额外推断出的人工 Gate。只有以下条件全部满足才通过：

- 每个已声明 Phase 都有当前人工 Phase Review 批准；
- Git 分支和 worktree 锁仍与 Feature 匹配；
- 所有已变更生产、测试和配置文件都位于已批准范围内；
- 未吸收无关的预先变更；
- 实现快照已冻结，包含 Base Commit、Head/Tree ID、文件哈希和快照 SHA-256；
- Tasks、Design 和 Spec 自批准后均未改变修订。

通过后以 `SDD_TASK_CODE_REVIEW` 模式调用 `uaw-code-review`。失败时保持 `blocked`，并执行 `.sdd2/feature-state.json.next_required_action`。

## 8. Code Review 交接

- 入口模式：`SDD_TASK_CODE_REVIEW`
- 范围权威来源：`./.sdd2/implementation-scope.json.frozen_snapshot`
- 必需 SDD 输入：当前已批准 Spec、Design、Tasks
- 输出：`./code-review-findings.md`
- Findings 是不可变首次评审证据；修复记录到 `auto-fix-summary.md`。
- 评审后任何实现、测试或配置变更都会使评审失效，并要求重新冻结和完整复审。

## 9. Auto-fix 与 Unit Test 交接

- Auto-fix 输出：`./auto-fix-summary.md`
- Unit Test 入口：`uaw-unit-test`，SDD 模式
- Unit Test 输出：生成/更新的测试源码和 `./unit-test-summary.md`
- Unit Test Gate 必须绑定到 Code Review 已通过且 Auto-fix 已关闭的同一范围哈希。
- 手工、CI 或 IDE 验证可作补充；生产变更时不能替代已变更测试源码。

## 10. 人工 Tasks Gate

- 必需审核人：当前人工审核人
- 批准证据：`.sdd2/gate-approvals.jsonl`
- 有效结果：`approved` / `rejected` / `blocked`

生成并记录本文件后停止。当前 Tasks 修订未被明确批准，且实现范围捕获未成功前，不得编辑生产或测试代码。

## 11. 控制状态投影

- 状态权威文件：`./.sdd2/feature-state.json`
- Attempt：
- 控制修订：
- 当前阶段：`tasks`
- 阶段状态：`awaiting-approval`
- 下一必需动作：`request-tasks-approval`
- 资产修订/SHA-256：

本节只投影控制状态；文件内文字不构成批准。
