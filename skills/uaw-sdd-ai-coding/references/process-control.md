# SDD2.0 内部操作控制

`sdd2-control-contract.md` 是权威来源。本文件只把正常流程动作映射到内部确定性 CLI。这些命令由 Skill 执行，不由开发者执行。

Skill 执行期间设置一次：

```bash
CONTROL=skills/uaw-sdd-ai-coding/scripts/sdd2_control.py
```

## 命令映射

| 流程动作 | 内部命令 |
|---|---|
| Brief 保存后初始化 | `python3 "$CONTROL" init --feature-dir <dir> --feature-id <id> --mode real` |
| 恢复/当前状态检查 | `python3 "$CONTROL" resume --feature-dir <dir>` |
| 记录已变更公开资产 | `python3 "$CONTROL" record-artifact --feature-dir <dir> --stage <stage>` |
| 保存当前明确批准 | `python3 "$CONTROL" approve --feature-dir <dir> --stage <stage> --source user-message --approver-role human --approval-text <exact-message> --message-id <id-if-available>` |
| 捕获干净实现范围 | `python3 "$CONTROL" capture-scope --feature-dir <dir> --allowed-path <pattern> --forbidden-path <pattern> --required-phase <phase> --test-path <pattern>` |
| 记录 Phase Review | `python3 "$CONTROL" phase-review --feature-dir <dir> --phase <phase> --source <user-message|demo-simulation> --approver-role <human|ai-as-human-reviewer> --approval-text <exact-message> --message-id <id-if-available>` |
| 冻结当前代码/测试范围 | `python3 "$CONTROL" freeze-scope --feature-dir <dir>` |
| 记录质量 Gate | `python3 "$CONTROL" quality-gate --feature-dir <dir> --gate <code-review|auto-fix|unit-test> --result <result> --evidence <reproducible-evidence>` |
| 准备不可变 Archive 证据 | `python3 "$CONTROL" prepare-archive --feature-dir <dir>` |
| 检查 Archive 资格 | `python3 "$CONTROL" archive-check --feature-dir <dir> --require-archive` |
| 校验全部控制 | `python3 "$CONTROL" validate --feature-dir <dir>` |
| 显式关闭失败流程 | `python3 "$CONTROL" close --feature-dir <dir> --result <closed-with-risk|aborted> --approval-text <exact-message>` |
| 显式开始新 Attempt | `python3 "$CONTROL" restart-attempt --feature-dir <dir> --approval-text <exact-message>` |

按需重复 `--allowed-path`、`--forbidden-path`、`--required-phase` 和 `--test-path`。路径模式必须足够窄；`*`、`**`、仓库根目录和绝对路径均会被拒绝。

只有已批准 Tasks 不包含生产代码变更时，才能使用 `--non-production-change`。理由必须记录在 Design 和 Tasks 中。不得用它绕过测试源码要求。

## 批准处理

不得在生成 Gate 资产的同一个 assistant turn 中执行 `approve`。等待用户新消息，并原样传入批准文字，不得改写。平台提供稳定消息 ID 时必须记录；否则保留时间戳、原始文字、资产修订、资产哈希和批准哈希链证据。

仅在用户明确授权的 Demo 中：

1. 使用 `--mode demo` 初始化；
2. 使用 `authorize-demo` 保存用户单独提供的当前授权；
3. 使用 `source=demo-simulation` 和 `approver-role=ai-as-human-reviewer`；
4. 将每项输出标为模拟证据，而非人工批准。

`phase-review` 同样必须保留上述 Demo 来源；不得把 AI 模拟的 Phase Review 记录为 `user-message/human`。

## 错误处理

退出码含义：

- `0`：动作成功，并返回当前结构化结果。
- `1`：校验/检查已完成，但发现阻塞错误。
- `2`：命令或状态转换被拒绝。

退出码为 `1` 或 `2` 时立即停止。保留返回错误；人类可读资产中的状态只能作为 `.sdd2/feature-state.json` 的投影；按照 `resume.next_required_action` 恢复。禁止手工编辑控制 JSON/JSONL。

## 恢复规则

- 锁缺失或不匹配：只有没有其他 Feature 占用 worktree 时，`resume` 才可重新获取；否则使用另一个 worktree。
- 范围漂移：冻结新快照，然后按失效结果重新执行 Code Review、Auto-fix 关闭、Unit Test、Unit Test Summary 批准和 Archive 证据。
- 资产漂移：记录已变更资产，再重复所有失效的下游动作。
- 哈希链损坏：停止并保留证据，不得自动修复或重写历史。
- 测试失败/阻塞：在当前范围修复并重跑，或由用户明确接受风险/终止；绝不能完成 Archive。
- 会话中断：调用 `resume`，不得从聊天记录推断状态。
- 重复执行：只有用户发送新的明确重试/重启消息后才能使用 `restart-attempt`。

## 历史样例

使用一次 `migrate-legacy` 隔离控制器引入前的样例。该动作把既有资产记录为历史内容，不伪造批准，将状态设为 `superseded`，并禁止恢复或继续。历史资产保持原哈希，不执行语言回写。
