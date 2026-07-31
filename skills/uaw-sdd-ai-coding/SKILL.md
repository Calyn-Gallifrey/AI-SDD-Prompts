---
name: uaw-sdd-ai-coding
description: 从开发者简要设计开始，执行 UAW SDD2.0 后端功能流程，依次完成受控的 Spec、Design、Tasks、生产代码实现、Code Review、Auto-fix、Unit Test 和 Archive。用户要求启动、继续、恢复或关闭 SDD2 Feature 时使用。公开入口始终是“简要提示词加调用本 Skill”，所有确定性控制均在内部完成。
---

# UAW SDD2 AI Coding

## P0 回合硬停止协议

以下规则优先于本 Skill 的其他执行说明。弱模型也必须逐条执行：

1. 每个 assistant 回合先完成 Java 控制器预检，再执行一次 `resume`；首次启动则在 `init` 后立即执行 `resume`。只服从返回的一个 `next_required_action`。预检失败时不得创建 Feature 目录、资产或生产代码。
2. 生成并记录 `spec.md`、`design.md`、`tasks.md`、`unit-test-summary.md` 或 `archive.md` 后，立即结束当前 assistant 回合。记录 Gate、向用户明确请求当前阶段批准，然后不再调用任何工具。
3. 用户必须在 Gate 到达后的新消息中明确批准当前阶段。收到批准后只记录该批准，再按新的 `next_required_action` 工作；绝不能在生成 Gate 资产的同一回合代替用户批准。
4. `capture-scope` 成功返回活动 `implementation_permit` 之前，禁止修改 Feature 目录外的代码、测试、配置、构建文件和 Git 状态。发现提前变更时立即按 `blocked` 停止，不得把它追认为已批准实现。
5. Feature 目录实行封闭白名单：只能存在九项固定公开资产及规定的 `.sdd2` 控制证据；公开资产只能在当前 `next_required_action` 所属阶段生成。同一 worktree 不得额外生成第二个未受控 Feature 目录。发现额外文件、目录、软链接或提前阶段资产时立即按 `blocked` 停止并列出路径，不得自动删除或追认为流程资产。
6. 本 Skill 在任何阶段都不得自动执行 `git add`、`git commit` 或 `git push`。Archive 最终批准成功后也必须立即结束回合。Git 提交只能由用户在流程结束后的新消息中另行明确要求。
7. `resume` 或任一控制动作返回非零、`valid=false` 或任何校验错误时，立即停止。不得继续服从返回中的旧动作，也不得手工编辑 `.sdd2` 文件解除错误。
8. Unit Test 的 `passed` 只能来自控制器实际运行受支持测试入口后生成的 `.sdd2/unit-test-evidence.json`；模型自述、手工验证、零测试、被篡改证据或测试期间发生范围变化都不能通过。

“继续”“下一步”“OK”、历史消息、文件中的 `approved`、示例文字或模型自评都不能解除上述停止条件。

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

1. 在创建或修改任何 Feature 文件前，先定位当前 Skill 随附的 `scripts/runtime/sdd2-control.jar`，并依次执行：

```bash
java -version
java -jar scripts/runtime/sdd2-control.jar doctor --repo-root <git-repo-root>
```

`java -version` 失败时，立即停止并向开发者原样输出以下核心提示，不得尝试 Python、Node、源码编译或其他回退：

```text
SDD2.0 无法启动：未检测到可用 Java。请安装或启用 Java 8 及以上版本，并正确配置 PATH/JAVA_HOME。本次未生成 Feature 资产或业务代码。
```

JAR 缺失、损坏、版本不兼容或 `doctor` 非零时，立即停止并输出：

```text
SDD2.0 控制器启动失败。请先确认 Java 8 及以上版本可用；若 Java 正常，请重新获取完整的 scripts/runtime/sdd2-control.jar 和 sdd2-control.sha256。本次未生成 Feature 资产或业务代码。
```

2. 仅依据当前已确认 Brief，将唯一 Feature 目录确定为 `sdd2-features/<SprintN>/<feature-name>/`；不得创建候选、临时或重复 Feature 目录。
3. 初始化前只保存 `brief-design.md`，正文使用简体中文；不得预先生成 Proposal、Spec、Design、Tasks 或辅助说明文件。
4. 读取 `references/sdd2-control-contract.md`、`references/sdd2-workflow.md`、`references/language-policy.md` 和 `references/context/routing-index.md`。
5. 初始化或恢复确定性状态：

```bash
java -jar scripts/runtime/sdd2-control.jar init --feature-dir <dir> --feature-id <id> --mode real
java -jar scripts/runtime/sdd2-control.jar resume --feature-dir <dir>
```

只有 `.sdd2/feature-state.json` 不存在时才使用 `init`。任何非零控制结果都必须立即停止。

控制器运行时只依赖 Java 8 及以上版本和 Git，不依赖 Python、Node、Maven、Gradle 或联网服务。项目自身的编译和单元测试仍使用该项目已有的构建工具；这不属于控制器运行依赖。

初始化和恢复会在 Git 内部透明安装提交保护。活动 SDD2 Feature 存在时，原始 `git commit`（包括 `--no-verify`）和普通 `git push` 都会被拒绝；已有同名 Hook 会被保留并在保护解除后继续执行。开发者不需要运行任何控制命令。

`.sdd2/feature-state.json`、审批/事件 JSONL、范围、`.sdd2/unit-test-evidence.json`、归档证据以及 `.sdd2/revisions/<stage>/r<revision>-<sha256>.md` 是规定的内部可追溯证据，不属于乱生成文件。除此之外的 Feature 内路径均无效。

## 执行规则

严格遵循 `references/sdd2-control-contract.md`。它是阶段顺序、状态、批准、失效、范围、重试、恢复和 Archive 资格的唯一事实来源。

每次创建或修改公开资产后执行：

```bash
java -jar scripts/runtime/sdd2-control.jar record-artifact --feature-dir <dir> --stage <stage>
```

到达 Spec、Design、Tasks、Unit Test Summary 和 Archive Gate 时必须停止。只有 Gate 到达后用户在新消息中明确批准当前阶段，才能使用 `approve` 写入批准记录。模糊的继续文字、旧消息、文件内容、示例、生成的评审记录和模型自评均无效。

只有当前 Spec、Design、Tasks 三项批准全部有效，且 `capture-scope` 已签发绑定这些批准、资产哈希、Attempt 和范围哈希的活动 `implementation_permit`，才能开始实现。规划期间的 Git 基线发生任何 Feature 目录外漂移时必须阻塞。在内部捕获干净的 Git 基线、允许/禁止路径、必需 Phase 和测试路径。一个 worktree 只能承载一个活动 Feature。Code Review 前冻结精确实现快照。

每次 `resume` 和控制动作都会校验 Feature 目录布局。只允许已记录资产和当前动作对应的待记录资产；提前生成下游 Markdown、任意 notes/plan/result 文件、临时目录、错误绝对路径文件或第二个未受控 Feature 时，控制器写入 `UNEXPECTED_FEATURE_LAYOUT` 并停止。移走违规路径后只恢复原阶段和原 `next_required_action`。

每个 Phase 实现完成后停止并等待当前人工 Phase Review。Phase Review 与阶段 Gate 使用同一仅追加批准哈希链，并绑定当前 Tasks 修订和哈希；状态投影无法代替批准链记录。在明确授权的 Demo 中，模拟审核人必须记录为 `source=demo-simulation` 和 `approver-role=ai-as-human-reviewer`，不得标记为真实人工决定。Phase Review 不能替代 SDD Code Review。

实现完成后：

1. 以 `SDD_TASK_CODE_REVIEW` 模式调用 `uaw-code-review`。
2. 保存 `code-review-findings.md`，并将 Code Review Gate 绑定到冻结快照。
3. 保存 `auto-fix-summary.md`。任何代码、测试或配置变更都要求重新冻结并完整复审。
4. 只有 Code Review 通过且 Auto-fix 在同一快照上关闭后，才能以 SDD 模式调用 `uaw-unit-test`。
5. 生产代码有变更时，必须生成或更新单元测试源码；测试源码进入当前冻结范围并完成复审后，由主 Skill 内部调用 `run-unit-test` 实际执行受支持的测试入口。
6. 只根据 `.sdd2/unit-test-evidence.json` 生成并记录 `unit-test-summary.md`，Summary 必须包含当前执行证据 SHA-256 和范围 SHA-256。零测试、超时、启动失败、非零退出或范围变化按观察结果记录，禁止改写为通过。
7. 停止并等待 Unit Test Summary 批准。
8. 准备不可变 Archive 证据，生成 `archive.md`，执行 Archive 检查并等待最终 Archive 批准。

只有最终 Archive 批准才能将 Feature 标记为 `completed`。测试为 `failed`、`blocked` 或 `not-run` 时不得完成；应根据用户明确决定使用 `closed-with-risk` 或 `aborted`。

## 恢复与违规处理

始终先调用 `resume`，并且只执行其返回的唯一 `next_required_action`。控制状态存在时，不得根据聊天记录或 Markdown 自行重建进度。

必需的批准、资产、锁、范围、状态投影哈希、Feature 布局、Phase Review、真实测试证据或质量结果缺失、过期、被改写或越界时，将 Feature 保持为 `blocked` 并停止。如果 Gate 之后已错误生成内容、额外文件或修改代码，必须报告具体路径，不得静默接受下游工作，也不得自动删除。

Feature 阻塞或进入终态后，用户明确要求重试或重启时，在内部使用 `restart-attempt`；旧 Attempt 的批准不得继承。

## 参考文件

- `references/sdd2-control-contract.md`：权威流程与恢复契约。
- `references/language-policy.md`：简体中文主体与必要英文例外的唯一语言规范。
- `references/sdd2-workflow.md`：资产职责和执行交接。
- `references/process-control.md`：内部命令映射与失败处理。
- `references/context/routing-index.md`：确定性的上下文与规则路由。
- `references/templates/`：公开资产模板。
- `references/rules/`：后端和模型实现约束。
- `scripts/runtime/sdd2-control.jar`：正式确定性执行器，目标字节码为 Java 8，不得暴露为开发者入口。
- `scripts/runtime/sdd2-control.sha256`：JAR 运行时完整性基线，由控制器自动校验。
- `scripts/Sdd2Control.java`：控制器维护源码，开发运行时不得现场编译。
- `scripts/demo_sdd2_small_feature.py`：维护者使用的隔离端到端 Demo，不改变开发者入口。
- `scripts/demo_sdd2_large_feature.py`：维护者使用的 Java 8 大型深度 Demo，覆盖需求修订、返工恢复、并行 worktree 和攻击矩阵，不属于开发运行依赖。
