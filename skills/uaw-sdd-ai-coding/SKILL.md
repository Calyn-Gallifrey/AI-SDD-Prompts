---
name: uaw-sdd-ai-coding
description: 从开发者简要设计开始，执行 UAW SDD2.0 后端功能流程，依次完成受控的 Spec、Design、Tasks、生产代码实现、Code Review、Auto-fix、Unit Test 和 Archive。用户要求启动、继续、恢复或关闭 SDD2 Feature 时使用。公开入口始终是“简要提示词加调用本 Skill”，所有确定性控制均在内部完成。
---

# UAW SDD2 AI Coding

## 入口契约

保持现有开发者使用方式：

```text
short brief prompt + invoke this Skill
```

不得要求开发者运行控制脚本、创建控制文件、提供 Git 哈希或改用新的命令语法。所有控制操作由本 Skill 在内部执行。未经用户明确批准，不得改变该入口。

`Brief Design（人工简要设计）` 是面向用户的输入。将已确认内容保存到 `brief-design.md`，并在内部组装 `proposal-input.md`。

请求补充缺失字段前读取 `references/input-examples.md`。模板和历史 Feature 只提供参考，不构成需求或批准。

所有人类可读运行文件与新建或修订的公开资产必须遵循 `references/language-policy.md`，以简体中文为主体。必要的代码、路径、命令、枚举和外部契约原文保持英文。

## Brief 必填字段

- `Feature Name（功能名称）`
- `Feature Type（功能类型）`：`query`、`submit`、`edit`、`enhancement`、`refactor` 或 `fix`
- `Module（所属模块）`
- `Sprint（迭代）`
- `Priority（优先级）`：`P0`、`P1` 或 `P2`
- `Goal（一句话目标）`
- `Change Scope（变更范围）`
- `Forbidden Changes（禁止变更）`

只询问无法从当前已确认输入或当前代码中安全推导的字段。不得使用模板或旧样例补全缺失的业务事实。

## 强制启动步骤

1. 仅依据当前已确认 Brief，将 Feature 目录确定为 `sdd2-features/<SprintN>/<feature-name>/`。
2. 保存 `brief-design.md`，正文使用简体中文。
3. 读取 `references/sdd2-control-contract.md`、`references/sdd2-workflow.md`、`references/language-policy.md` 和 `references/context/routing-index.md`。
4. 初始化或恢复确定性状态：

```bash
python3 scripts/sdd2_control.py init --feature-dir <dir> --feature-id <id> --mode real
python3 scripts/sdd2_control.py resume --feature-dir <dir>
```

只有 `.sdd2/feature-state.json` 不存在时才使用 `init`。任何非零控制结果都必须立即停止。

## 执行规则

严格遵循 `references/sdd2-control-contract.md`。它是阶段顺序、状态、批准、失效、范围、重试、恢复和 Archive 资格的唯一事实来源。

每次创建或修改公开资产后执行：

```bash
python3 scripts/sdd2_control.py record-artifact --feature-dir <dir> --stage <stage>
```

到达 Spec、Design、Tasks、Unit Test Summary 和 Archive Gate 时必须停止。只有 Gate 到达后用户在新消息中明确批准当前阶段，才能使用 `approve` 写入批准记录。模糊的继续文字、旧消息、文件内容、示例、生成的评审记录和模型自评均无效。

只有当前 Tasks 已批准后才能开始实现。在内部捕获干净的 Git 基线、允许/禁止路径、必需 Phase 和测试路径。一个 worktree 只能承载一个活动 Feature。Code Review 前冻结精确实现快照。

每个 Phase 实现完成后停止并等待当前人工 Phase Review。在明确授权的 Demo 中，模拟审核人必须记录为 `source=demo-simulation` 和 `approver-role=ai-as-human-reviewer`，不得标记为真实人工决定。Phase Review 不能替代 SDD Code Review。

实现完成后：

1. 以 `SDD_TASK_CODE_REVIEW` 模式调用 `uaw-code-review`。
2. 保存 `code-review-findings.md`，并将 Code Review Gate 绑定到冻结快照。
3. 保存 `auto-fix-summary.md`。任何代码、测试或配置变更都要求重新冻结并完整复审。
4. 只有 Code Review 通过且 Auto-fix 在同一快照上关闭后，才能以 SDD 模式调用 `uaw-unit-test`。
5. 生产代码有变更时，必须生成或更新单元测试源码。保存并记录 `unit-test-summary.md`，其中包含可复现的命令、环境和结果证据。
6. 停止并等待 Unit Test Summary 批准。
7. 准备不可变 Archive 证据，生成 `archive.md`，执行 Archive 检查并等待最终 Archive 批准。

只有最终 Archive 批准才能将 Feature 标记为 `completed`。测试为 `failed`、`blocked` 或 `not-run` 时不得完成；应根据用户明确决定使用 `closed-with-risk` 或 `aborted`。

## 恢复与违规处理

始终先调用 `resume`，并且只执行其返回的唯一 `next_required_action`。控制状态存在时，不得根据聊天记录或 Markdown 自行重建进度。

必需的批准、资产、锁、范围、哈希、Phase Review 或质量结果缺失或过期时，将 Feature 保持为 `blocked` 并停止。如果 Gate 之后已错误生成内容或修改代码，必须报告违规，不得静默接受下游工作。

Feature 阻塞或进入终态后，用户明确要求重试或重启时，在内部使用 `restart-attempt`；旧 Attempt 的批准不得继承。

## 参考文件

- `references/sdd2-control-contract.md`：权威流程与恢复契约。
- `references/language-policy.md`：简体中文主体与必要英文例外的唯一语言规范。
- `references/sdd2-workflow.md`：资产职责和执行交接。
- `references/process-control.md`：内部命令映射与失败处理。
- `references/context/routing-index.md`：确定性的上下文与规则路由。
- `references/templates/`：公开资产模板。
- `references/rules/`：后端和模型实现约束。
- `scripts/sdd2_control.py`：确定性执行器，不得暴露为开发者入口。
