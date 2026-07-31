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
| 执行并固化真实单元测试 | `python3 "$CONTROL" run-unit-test --feature-dir <dir> --cwd <repo-relative-dir> -- <recognized-test-command-and-args>` |
| 记录质量 Gate | `python3 "$CONTROL" quality-gate --feature-dir <dir> --gate <code-review|auto-fix|unit-test> --result <result> --evidence <reproducible-evidence>` |
| 准备不可变 Archive 证据 | `python3 "$CONTROL" prepare-archive --feature-dir <dir>` |
| 检查 Archive 资格 | `python3 "$CONTROL" archive-check --feature-dir <dir> --require-archive` |
| 校验全部控制 | `python3 "$CONTROL" validate --feature-dir <dir>` |
| 显式关闭失败流程 | `python3 "$CONTROL" close --feature-dir <dir> --result <closed-with-risk|aborted> --approval-text <exact-message>` |
| 显式开始新 Attempt | `python3 "$CONTROL" restart-attempt --feature-dir <dir> --approval-text <exact-message>` |

按需重复 `--allowed-path`、`--forbidden-path`、`--required-phase` 和 `--test-path`。路径模式必须足够窄；`*`、`**`、仓库根目录和绝对路径均会被拒绝。

只有已批准 Tasks 不包含生产代码变更时，才能使用 `--non-production-change`。理由必须记录在 Design 和 Tasks 中。不得用它绕过测试源码要求。

`init` 会保存规划期 Git 基线并安装 Git Guard；活动 Feature 的 `resume` 会复核并补装 Guard。`capture-scope` 成功结果必须同时包含 `implementation_permit_sha256`，状态中的 `implementation_permit.status` 必须为 `active`。缺少这两个结果时禁止任何实现编辑。

`run-unit-test` 只接受明确的测试 Runner，不通过 Shell 包装执行任意命令，也拒绝跳过测试参数。控制器亲自观察退出码和测试数量，将命令、输出哈希、有限输出片段、测试计数、当前范围和已变更测试源码写入 `.sdd2/unit-test-evidence.json`。Unit Test 的 `passed` 必须绑定该文件的 SHA-256；单独提供 `--evidence` 文字不能替代。

## 每回合分派

每个 assistant 回合只按以下顺序分派：

1. 首次启动执行 `init` 后调用 `resume`；已有状态直接调用 `resume`。
2. 读取唯一的 `next_required_action`。
3. 若动作是 `request-*-approval`，且当前用户新消息不是该阶段的明确批准，只输出审批请求并结束回合。
4. 若本回合刚记录 Spec、Design、Tasks、Unit Test Summary 或 Archive，输出审批请求并结束回合；不再调用工具。
5. 若动作是 `capture-implementation-scope`，只有命令成功并返回活动实现许可后才允许编辑 Feature 目录外文件。
6. 若状态为 `blocked` 或控制命令非零，报告阻塞并结束回合。

禁止把一个回合中的多条后续动作预先串联执行。

## 批准处理

不得在生成 Gate 资产的同一个 assistant turn 中执行 `approve`。等待用户新消息，并原样传入批准文字，不得改写。平台提供稳定消息 ID 时必须记录；否则保留时间戳、原始文字、资产修订、资产哈希和批准哈希链证据。

仅在用户明确授权的 Demo 中：

1. 使用 `--mode demo` 初始化；
2. 使用 `authorize-demo` 保存用户单独提供的当前授权；
3. 使用 `source=demo-simulation` 和 `approver-role=ai-as-human-reviewer`；
4. 将每项输出标为模拟证据，而非人工批准。

`phase-review` 同样必须保留上述 Demo 来源；不得把 AI 模拟的 Phase Review 记录为 `user-message/human`。所有真实或模拟 Phase Review 都写入与阶段 Gate 相同的仅追加批准哈希链，并绑定当前 Tasks 修订和哈希。

## 错误处理

退出码含义：

- `0`：动作成功，并返回当前结构化结果。
- `1`：校验/检查已完成，但发现阻塞错误。
- `2`：命令或状态转换被拒绝。

退出码为 `1` 或 `2`、`valid=false` 或返回任何校验错误时立即停止。保留返回错误；人类可读资产中的状态只能作为 `.sdd2/feature-state.json` 的投影；当前状态本身还必须匹配最新事件的状态投影哈希。按照后续有效 `resume.next_required_action` 恢复。禁止手工编辑控制 JSON/JSONL。

`PRE_IMPLEMENTATION_CHANGE` 表示实现许可签发前发生了 Feature 目录外变更。控制器会保存原 Gate 恢复点并进入 `blocked`。必须撤销或移走提前代码、测试、配置、构建变更及提前 Git 提交，再调用 `resume`；不得通过补写 Tasks、手工编辑状态或重新捕获范围来追认。

`IMPLEMENTATION_PERMIT_*` 表示批准、资产、Attempt、范围或许可哈希不一致。立即停止并从最早失效资产重新审批；不得继续实现或复用旧快照。

`FEATURE_GENERATION_BOUNDARY_REJECTED` 表示 `init` 前目标 Feature 不只包含 `brief-design.md`，或同一 worktree 已出现另一个未受控 Feature。`UNEXPECTED_FEATURE_LAYOUT` 表示活动 Feature 中出现白名单外文件/目录/软链接、提前阶段资产或未受控兄弟 Feature。报告所有相对路径并停止；不得自动删除。用户或维护者确认并移走违规路径后调用 `resume`，控制器只恢复原状态和原动作。

`SCOPE_MANIFEST_INVALID` 表示既有范围控制文件缺字段、格式损坏或无法复核。必须作为可报告的控制错误停止，不得抛出未处理异常，也不得重新解释为当前实现许可。

`STATE_EVENT_PROJECTION_MISMATCH`、`APPROVAL_CHAIN_*` 或 `PHASE_REVIEW_*` 表示当前状态与仅追加证据不一致。不得从 Markdown、聊天记录或状态文件中的孤立字段推断已批准，必须保留证据并停止。

`UNIT_TEST_EXECUTION_*` 或 `UNIT_TEST_EVIDENCE_*` 表示真实测试未执行、未观察到测试、结果不匹配或证据被改写。`UNIT_TEST_SCOPE_CHANGED` 表示测试过程改变了冻结范围，必须先恢复或批准该变化，再重新冻结、完整 Code Review、关闭 Auto-fix 并重跑测试。

## Git 写操作

本 Skill 不执行 `git add`、`git commit` 或 `git push`。活动锁存在时，内部 `prepare-commit-msg` Guard 会阻止所有提交，包括带 `--no-verify` 的提交；`pre-push` Guard 会阻止普通推送。Guard 遵循仓库当前的 `core.hooksPath`，保留既有同名 Hook，流程释放活动锁后自动放行并继续执行原 Hook。

Archive 批准不是 Git 授权。完成 Archive 后立即结束当前回合；只有用户在后续新消息中明确要求，才可由 SDD2 之外的 Git 工作流处理提交。

## 恢复规则

- 锁缺失或不匹配：只有没有其他 Feature 占用 worktree 时，`resume` 才可重新获取；否则使用另一个 worktree。
- 范围漂移：冻结新快照，然后按失效结果重新执行 Code Review、Auto-fix 关闭、Unit Test、Unit Test Summary 批准和 Archive 证据。
- 资产漂移：记录已变更资产，再重复所有失效的下游动作。
- 哈希链损坏：停止并保留证据，不得自动修复或重写历史。
- 测试失败/阻塞：在当前范围修复并重跑，或由用户明确接受风险/终止；绝不能完成 Archive。
- 测试为零：结果保持 `blocked`；修正精确测试选择器并重新执行，不能把退出码零解释为通过。
- 测试证据损坏：停止并保留现状，不能手工重写证据哈希；从当前复审后的范围重新执行测试。
- 会话中断：调用 `resume`，不得从聊天记录推断状态。
- 重复执行：只有用户发送新的明确重试/重启消息后才能使用 `restart-attempt`。
- 乱生成文件：保留错误清单并进入 `UNEXPECTED_FEATURE_LAYOUT`；只移走白名单外路径，九项公开资产及 `.sdd2` 规定证据不得误删。

## 历史样例

使用一次 `migrate-legacy` 隔离控制器引入前的样例。该动作把既有资产记录为历史内容，不伪造批准，将状态设为 `superseded`，并禁止恢复或继续。历史资产保持原哈希，不执行语言回写。

## 维护验证

维护者可运行 `python3 skills/uaw-sdd-ai-coding/scripts/demo_sdd2_small_feature.py`。脚本在临时 Git 仓库中实现一个小型 Java 功能，执行真实 Maven 测试，走完全部 Gate，并验证乱文件、重复 Feature、状态篡改、批准链、自动提交和测试证据篡改均被控制器阻断。临时仓库结束后自动清理，不在正式 Feature 目录留下演练资产。
