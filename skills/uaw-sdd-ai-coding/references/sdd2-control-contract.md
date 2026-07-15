# UAW-SDD 2.0 控制契约

本文件是 SDD2 阶段状态、批准、失效、实现范围、恢复和 Archive 资格的唯一事实来源。三项 Skill 可以摘要引用本契约，但不得重新定义。

## 1. 稳定的用户入口

公开入口保持不变：

```text
short brief prompt + invoke this Skill
```

开发者不运行控制命令，也不维护控制文件。`uaw-sdd-ai-coding` 在内部调用 `scripts/sdd2_control.py`。未来如需改变公开入口，必须先获得用户明确批准再实施。

## 2. 权威来源与优先级

1. `SKILL.md` 定义用户意图路由和不变入口。
2. 本文件定义流程语义。
3. `scripts/sdd2_control.py` 确定性执行本契约。
4. `references/schemas/` 下的 JSON Schema 定义持久化记录结构。
5. `references/language-policy.md` 定义人类可读文件与生成资产的语言要求。
6. 阶段模板定义人类可读资产内容。
7. 工程规则定义生产代码实现约束。
8. 示例不具权威性，永远不构成批准或需求。

低优先级来源与高优先级来源冲突时，按 `blocked` 停止，报告冲突且不得猜测。

## 3. Feature 资产与控制文件

九项公开资产固定为：

```text
brief-design.md
proposal-input.md
spec.md
design.md
tasks.md
code-review-findings.md
auto-fix-summary.md
unit-test-summary.md
archive.md
```

内部控制数据保存在同一个 Feature 目录：

```text
.sdd2/feature-state.json
.sdd2/gate-approvals.jsonl
.sdd2/events.jsonl
.sdd2/implementation-scope.json
.sdd2/archive-evidence.json
.sdd2/revisions/<artifact-stage>/r<revision>-<sha256>.md
```

`feature-state.json` 是当前状态的权威来源。Markdown 状态块只提供可读投影。批准和事件 JSONL 记录使用仅追加的 SHA-256 哈希链。每个活动资产修订都会复制为不可变、按内容寻址的快照。资产批准只对记录中的 Attempt、资产修订和资产 SHA-256 有效。

所有新建或修订的公开资产必须遵循 `references/language-policy.md`，并在记录前通过简体中文主体校验。

## 4. 规范状态

阶段顺序：

```text
brief-design
proposal-input
spec
design
tasks
implementation
code-review
auto-fix
unit-test-summary
archive
```

阶段状态：

```text
ready
executing
recorded
awaiting-approval
awaiting-final-approval
blocked
completed
closed-with-risk
aborted
superseded
```

只有 `completed`、`closed-with-risk`、`aborted` 和 `superseded` 是终态。`closed-with-risk` 与 `aborted` 不代表成功交付。

每个活动状态都记录 Feature/worktree 绑定、Attempt、修订、当前阶段、状态、下一必需动作、资产、批准、Phase Review、质量 Gate、失效记录和阻塞恢复条件。

## 5. 初始化与 worktree 隔离

保存 `brief-design.md` 后初始化控制状态：

```bash
python3 scripts/sdd2_control.py init \
  --feature-dir <feature-dir> \
  --feature-id <stable-feature-id> \
  --mode real
```

一个 Git worktree 只能有一个活动 SDD2 Feature。并行 Feature 必须使用不同 Git worktree。实现前捕获干净的 Git 基线和批准路径。存在预先变更文件、禁止路径、范围外路径、detached HEAD、分支漂移、锁缺失或过宽路径模式时，必须阻塞执行。

## 6. 资产记录与人工 Gate

创建或修改公开资产后调用 `record-artifact`。该动作增加资产修订、保存 SHA-256，并使受影响的下游批准和质量 Gate 失效。`init` 与 `record-artifact` 都必须先通过当前资产的简体中文主体校验。

`spec`、`design`、`tasks`、`unit-test-summary` 和 `archive` 必须经过人工批准。有效批准必须满足：

1. 来自当前 Gate 到达后的新用户消息；
2. 明确指出阶段和批准结论；
3. 记录 `source=user-message`、人工/用户角色、可用时的消息 ID、资产修订和资产哈希；
4. 不得从 `continue`、`next`、`ok`、文件、示例、旧消息、生成的评审文字或模型自评中推断。

`AI-as-human-reviewer` 在 real 模式中无效。在 demo 模式中，只有用户先用单独的当前消息明确授权 Demo/模拟并完成记录后才有效。

到达人工 Gate 后，记录资产并停止。不得生成下一资产、修改生产/测试代码、调用下一 Skill 或宣称已越过 Gate。

## 7. 精确执行流程

1. 保存 Brief Design 并初始化状态。
2. 生成并记录 `proposal-input.md`。
3. 生成并记录 `spec.md`；停止；记录明确的 Spec 批准。
4. 生成并记录 `design.md`；停止；记录明确的 Design 批准。
5. 生成并记录 `tasks.md`；停止；记录明确的 Tasks 批准。
6. 捕获实现范围，包括基线提交、分支、允许/禁止路径、必需 Phase 和测试路径模式。
7. 实现一个已批准 Phase；停止；记录明确的 Phase Review 后才能进入下一 Phase。
8. 冻结实现快照。之后任何生产代码、测试代码、配置、Spec、Design 或 Tasks 变更都会使受影响的下游结果失效。
9. 以 `SDD_TASK_CODE_REVIEW` 模式调用 `uaw-code-review`；针对冻结快照记录评审发现和 Code Review Gate。
10. 生成 `auto-fix-summary.md`。修复改变快照时，重新冻结并完整执行 Code Review。只有 Code Review 在同一快照上通过后，才能将 Auto-fix 记录为 `passed` 或 `not-required`。
11. 以 SDD 模式调用 `uaw-unit-test`。生产代码变更必须至少生成或更新一个匹配已捕获测试路径的测试源码。测试代码改变快照时，先重新冻结、完整复审并再次关闭 Auto-fix，之后才能记录 Unit Test。
12. 记录 `unit-test-summary.md` 和 Unit Test 证据；停止；记录明确的 Unit Test Summary 批准。
13. 根据 Git base/head/tree、冻结范围哈希和逐文件哈希准备不可变 Archive 证据。
14. 生成并记录 `archive.md`；执行 Archive 检查；停止；记录最终 Archive 批准。
15. 只有最终 Archive 批准才能设置 `completed` 并释放 worktree 锁。

## 8. 质量 Gate 结果

Code Review 接受 `passed`、`failed` 或 `blocked`。Auto-fix 接受 `passed`、`not-required`、`failed` 或 `blocked`。Unit Test 接受 `passed`、`failed`、`blocked` 或 `not-run`。

Archive 要求以下条件全部绑定到同一个当前快照：

- 当前 Spec、Design、Tasks 和 Unit Test Summary 均已批准；
- 所有必需 Phase Review 均已批准；
- Code Review 为 `passed`；
- Auto-fix 为 `passed` 或 `not-required`；
- Unit Test 为 `passed`；
- 九项公开资产均已记录且未变化；
- 当前不可变 Archive 证据有效；
- 不存在阻塞、范围漂移、哈希链损坏、分支不匹配或锁不匹配。

测试为 `failed`、`blocked` 或 `not-run` 时，绝不能按成功交付归档。用户明确接受风险时使用 `closed-with-risk`；用户明确终止时使用 `aborted`。

## 9. 失效矩阵

| 变更 | 失效范围 |
|---|---|
| Brief / Proposal / Spec | 所有后续批准、Phase Review 和质量 Gate |
| Design | Design/Tasks 及全部后续记录 |
| Tasks | Tasks 批准、Phase Review、范围及全部质量 Gate |
| 生产/测试/配置快照 | Code Review、Auto-fix、Unit Test、Unit Test Summary 批准和 Archive 证据 |
| Findings | Code Review 及后续 Gate |
| Auto-fix Summary | Auto-fix 及后续 Gate |
| Unit Test Summary | 当前批准和 Archive |
| Archive | 仅最终 Archive 批准 |

失效结果保留在历史记录中，但不能再授权流程前进。

## 10. 恢复、继续与重复执行

`resume` 会校验哈希、资产、锁、分支和范围，并且只返回一个 `next_required_action`。控制状态存在时，禁止根据聊天记忆或 Markdown 文字重建状态。

对于可恢复的阻塞阶段，修复记录中的原因并重复同一个必需动作。阻塞或终态 Attempt 之后需要重新执行时，`restart-attempt` 必须由新的明确用户重试/重启消息触发；它会增加 Attempt、使旧批准失效、清空质量结果和范围，并从最早需要重新批准的持久化阶段开始。

历史 Feature 样例迁移为 `historical-example` 和 `superseded`。不回填或接受其旧批准。它们只供参考，不能恢复执行，也不因当前语言规范而改写其不可变内容。

## 11. 失败规则

任何控制命令返回非零都必须立即停止。将错误记录为阻塞原因，不得手工绕过；只有状态恢复有效，或用户明确关闭/重启 Attempt 后才能继续。
