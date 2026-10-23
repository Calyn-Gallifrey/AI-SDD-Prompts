# UAW-SDD 2.0 控制契约

本文件是 SDD2 阶段状态、批准、失效、实现范围、恢复和 Archive 资格的唯一事实来源。三项 Skill 可以摘要引用本契约，但不得重新定义。

## 1. 稳定的用户入口

公开入口保持不变：

```text
short brief prompt + invoke this Skill
```

开发者不运行控制命令，也不维护控制文件。`uaw-sdd-ai-coding` 在内部调用随 Skill 分发的 `scripts/runtime/sdd2-control.jar`。未来如需改变公开入口，必须先获得用户明确批准再实施。

## 2. 权威来源与优先级

1. `SKILL.md` 定义用户意图路由和不变入口。
2. 本文件定义流程语义。
3. `scripts/runtime/sdd2-control.jar` 确定性执行本契约；该 JAR 使用 Java 8 目标字节码和 Java 8 标准库。
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
.sdd2/unit-test-evidence.json
.sdd2/archive-evidence.json
.sdd2/revisions/<artifact-stage>/r<revision>-<sha256>.md
```

`feature-state.json` 是当前状态的权威来源，但它不能脱离控制证据单独授权流程前进。Markdown 状态块只提供可读投影。批准和事件 JSONL 记录使用仅追加的 SHA-256 哈希链；每个新事件还绑定事件发生后的完整控制状态投影 SHA-256。状态与最新事件投影不一致时立即停止。每个活动资产修订都会复制为不可变、按内容寻址的快照。阶段批准和 Phase Review 都写入批准链，只对记录中的 Attempt、阶段、资产修订和资产 SHA-256 有效。

Feature 目录是封闭资产空间。除上述九项公开资产和内部控制路径外，不允许出现其他文件、目录、软链接、候选输出、临时说明或错误拼接路径。公开资产只能在已记录状态或当前 `next_required_action` 对应阶段存在；例如等待 Spec 批准时出现 `design.md` 或 `tasks.md` 属于违规。`.sdd2/revisions/` 下只有阶段已经记录、修订号不超过当前修订且文件内容 SHA-256 与文件名一致的快照才是规定审计证据；提前伪造的范围、归档或修订文件仍属于违规。

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

活动 Attempt 还必须记录：

- 初始化时 Feature 目录外工作区的规划基线；
- 是否已经进入过实现；
- 绑定当前 Spec、Design、Tasks 批准和实现范围的 `implementation_permit`；
- 已失效实现许可的历史记录。
- 绑定当前冻结范围、真实测试命令、观察结果和证据哈希的 `unit_test_execution`。

## 5. 初始化与 worktree 隔离

任何 Feature 文件写入前，主 Skill 必须先检查 `java -version`，再执行只读的 `java -jar scripts/runtime/sdd2-control.jar doctor --repo-root <git-repo-root>`。控制器在每次命令启动时自动核对同目录 `sdd2-control.sha256`。任一步非零、Java 不可用、JAR 或校验文件缺失/损坏、哈希不匹配或版本不兼容时，必须在创建 Feature 目录、资产或业务代码前停止，并用简体中文提示安装或启用 Java 8 及以上版本、配置 `PATH/JAVA_HOME`，或重新获取完整 JAR 和校验文件。

正式控制器运行时只依赖 Java 8 及以上版本和 Git。不得回退调用 Python 控制器，不得要求开发机安装 Python、Node、Maven、Gradle、额外服务或联网下载控制器依赖。业务项目已有的构建工具只用于编译和测试该项目，不属于 SDD2 控制器依赖。

保存 `brief-design.md` 后初始化控制状态：

```bash
java -jar scripts/runtime/sdd2-control.jar init \
  --feature-dir <feature-dir> \
  --feature-id <stable-feature-id> \
  --mode real
```

一个 Git worktree 只能有一个活动 SDD2 Feature。并行 Feature 必须使用不同 Git worktree。初始化前，目标 Feature 目录只能包含当前 `brief-design.md`；同一 worktree 内如存在另一个未终止或尚未初始化的变更 Feature 目录，`init` 必须拒绝启动。实现前捕获干净的 Git 基线和批准路径。存在预先变更文件、禁止路径、范围外路径、detached HEAD、分支漂移、锁缺失或过宽路径模式时，必须阻塞执行。

`init` 必须保存 Feature 目录外的规划期 Git 快照。首次实现许可签发前，分支、HEAD 或任一代码、测试、配置、构建及其他 Feature 外文件发生变化，都记录为 `PREMATURE_IMPLEMENTATION_CHANGE` 并进入 `blocked`。只有恢复到原规划基线后，`resume` 才能返回原人工 Gate。

`init` 和活动 Feature 的 `resume` 必须透明安装 Git Guard。控制器在 Git 内部的 `sdd2-git-guard/` 保存分发脚本及原 `core.hooksPath` 路由，通过仓库或 worktree 专用配置启用；既有 Hook 保持原文件名、位置、解释器、参数和标准输入，其他 Git Hook 也继续转发。Guard 通过 `prepare-commit-msg` 拒绝活动 Attempt 下的所有提交，因此 `git commit --no-verify` 也不能绕过；普通 `git push` 由 `pre-push` 同步拒绝。活动锁按 worktree 隔离，不能阻止其他已结束或未启动流程的 worktree 正常提交。旧版 `.sdd2-original` 备份在新分发路由生效后恢复原位。

`init` 必须在写入前检查必需参数与模式；初始化写入失败时，仅回滚该次新建的内部控制文件和归属锁，保留 `brief-design.md`。旧运行包留下的未完成初始化，只有锁的仓库、路径、功能标识一致，且内部内容仅包含可验证的初始 Brief 快照、没有状态/批准/事件或其他内容时，才允许在重试 `init` 时恢复。存在未知内容或审批证据时保留现场并停止。

同一 worktree 的控制命令通过 Git 内部 `sdd2-command.lock` 上的操作系统文件锁串行执行，取得锁后才读取并校验当前状态。锁文件存在不代表命令仍活动；进程退出由操作系统释放锁。等待超过 30 秒返回 `SDD2_COMMAND_BUSY`；`doctor` 保持只读，不创建该文件。

## 6. 资产记录与人工 Gate

创建或修改公开资产后调用 `record-artifact`。该动作增加资产修订、保存 SHA-256，并使受影响的下游批准和质量 Gate 失效。`init` 与 `record-artifact` 都必须先通过当前资产的简体中文主体校验。

`spec`、`design`、`tasks`、`unit-test-summary` 和 `archive` 必须经过人工批准。有效批准必须满足：

1. 来自当前 Gate 到达后的新用户消息；
2. 明确指出阶段和批准结论；
3. 记录 `source=user-message`、人工/用户角色、可用时的消息 ID、资产修订和资产哈希；
4. 不得从 `continue`、`next`、`ok`、文件、示例、旧消息、生成的评审文字或模型自评中推断。

否定、附条件、疑问及未决表达均拒绝，例如“请不要批准 spec”“如果接口确认再批准 spec”“不同意终止”“不要重试”。批准解析采取保守策略，误拒绝时请用户重新给出简短、明确的当前阶段决定，不得由模型改写原话。

控制器核验来源字段、修订和历史的一致性，不独立认证聊天平台发件人或 assistant 回合。`source=user-message` 等命令参数必须来自真实上下文；本地哈希链不能替代可信消息来源、人工审查或业务正确性判断。

每项 Phase Review 遵循相同来源要求，并作为 `phase-review:<phase-id>` 写入同一批准链，绑定当前 Tasks 修订与哈希。状态中的 `approved` 字段只有在能反向找到唯一匹配批准链记录时才有效。

`AI-as-human-reviewer` 在 real 模式中无效。在 demo 模式中，只有用户先用单独的当前消息明确授权 Demo/模拟并完成记录后才有效。

到达人工 Gate 后，记录资产并停止。不得生成下一资产、修改生产/测试代码、调用下一 Skill 或宣称已越过 Gate。

“停止”是 assistant 回合边界：生成并记录 Gate 资产后，只能输出当前阶段、资产修订/哈希、所需人工动作和阻塞影响，然后立即结束当前回合。此后不得再调用任何工具。生成 Gate 资产的同一回合永远不能执行 `approve`。

## 7. 精确执行流程

1. 保存 Brief Design 并初始化状态。
2. 生成并记录 `proposal-input.md`。
3. 生成并记录 `spec.md`；停止；记录明确的 Spec 批准。
4. 生成并记录 `design.md`；停止；记录明确的 Design 批准。
5. 生成并记录 `tasks.md`；停止；记录明确的 Tasks 批准。
6. 捕获实现范围，包括基线提交、分支、允许/禁止路径、必需 Phase 和测试路径模式；校验三项当前批准后，签发绑定 Attempt、Spec/Design/Tasks 修订与哈希、批准 ID 和范围契约哈希的 `implementation_permit`。
7. 实现一个已批准 Phase；停止；记录明确的 Phase Review 后才能进入下一 Phase。
8. 冻结实现快照。之后任何生产代码、测试代码、配置、Spec、Design 或 Tasks 变更都会使受影响的下游结果失效。
9. 以 `SDD_TASK_CODE_REVIEW` 模式调用 `uaw-code-review`；针对冻结快照记录评审发现和 Code Review Gate。
10. 生成 `auto-fix-summary.md`。修复改变快照时，重新冻结并完整执行 Code Review。只有 Code Review 在同一快照上通过后，才能将 Auto-fix 记录为 `passed` 或 `not-required`。
11. 以 SDD 模式调用 `uaw-unit-test`。生产代码变更必须至少生成或更新一个匹配已捕获测试路径的测试源码。测试代码改变快照时，先重新冻结、完整复审并再次关闭 Auto-fix。随后由控制器使用受支持测试 Runner 实际执行测试，生成 `.sdd2/unit-test-evidence.json`。
12. 只根据当前执行证据记录 `unit-test-summary.md`；Summary 必须包含执行证据 SHA-256 和范围 SHA-256。记录确定性 Unit Test 结果；停止；记录明确的 Unit Test Summary 批准。
13. 根据 Git base/head/tree、冻结范围哈希和逐文件哈希准备不可变 Archive 证据。
14. 生成并记录 `archive.md`；执行 Archive 检查；停止；记录最终 Archive 批准。
15. 只有最终 Archive 批准才能设置 `completed` 并释放 worktree 锁；批准成功后立即结束回合，不执行任何 Git 提交或推送。

生产代码、测试、配置或构建文件只能在活动 `implementation_permit` 校验成功后修改。后续实现、冻结、Code Review、Auto-fix、Unit Test 和 Archive 动作都必须重新校验该许可；许可缺失、失效、哈希不匹配或批准不再有效时立即停止。

范围模式必须包含实际路径或名称约束；`?*`、`*/*`、`*/**`、仅字符类/通配符、父级穿越和绝对路径均拒绝。冻结文件记录同时包含内容哈希和 Git 等价执行模式，执行权限变化会使快照失效；实现文件的符号链接与非普通文件拒绝进入范围。

## 8. 质量 Gate 结果

Code Review 接受 `passed`、`failed` 或 `blocked`。Auto-fix 接受 `passed`、`not-required`、`failed` 或 `blocked`。Unit Test 接受 `passed`、`failed`、`blocked` 或 `not-run`。

Unit Test 的 `passed` 还必须同时满足：

- 控制器实际启动受支持测试 Runner，未通过 Shell 包装或跳过测试参数；
- 观察到至少一项测试通过，失败与 Error 为零，退出码为零；
- 执行前后实现范围 SHA-256 相同；
- `.sdd2/unit-test-evidence.json` 内容哈希有效，状态、Gate、Summary 和 Archive 证据均绑定同一证据 SHA-256。

模型自述、手工验证、零测试、超时、启动失败、证据改写或测试期间范围变化都不能得到 `passed`。

系统测试工具必须与当前 PATH 上已安装的同名工具一致；显式路径不一致时拒绝。仓库 Wrapper 必须位于仓库内，并与基线提交中的文件内容一致；改动 Wrapper 的维护工作需先独立验收，或改用已安装工具。仅伪造同名可执行文件不能获得测试证明。执行记录保存实际命令，执行前后核对工具文件哈希；测试数量只按所选 Runner 的格式解析，不能用另一种 Runner 的日志伪造结果。PATH 与基线工具链属于可信环境前提；该检查不证明测试断言质量。

Archive 要求以下条件全部绑定到同一个当前快照：

- 当前 Spec、Design、Tasks 和 Unit Test Summary 均已批准；
- 所有必需 Phase Review 均已批准；
- Code Review 为 `passed`；
- Auto-fix 为 `passed` 或 `not-required`；
- Unit Test 为 `passed`；
- Unit Test Gate 和 Archive 证据绑定同一真实测试执行证据 SHA-256；
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
| Unit Test 执行证据 | Unit Test Gate、Unit Test Summary 批准和 Archive |
| Archive | 仅最终 Archive 批准 |

失效结果保留在历史记录中，但不能再授权流程前进。

## 10. 恢复、继续与重复执行

`resume` 会校验状态事件投影、批准链、哈希、资产、锁、分支、范围和测试执行证据，并且只返回一个 `next_required_action`。存在任何校验错误时返回非零并硬停止；不得继续执行返回中的旧动作。控制状态存在时，禁止根据聊天记忆或 Markdown 文字重建状态。

已进入终态但释放锁失败时，`resume` 在校验状态与历史后重试释放本功能的残留锁；对已关闭状态重复相同结果的 `close` 也可重试释放。恢复不新增批准、不修改终态或修订，不解除其他功能的锁；历史损坏时不清理。规划阶段终止无需补造实现范围文件。

从 `2.0-java8.2` 的活动冻结快照接续时，新构建纳入执行模式，原快照可能报告 `IMPLEMENTATION_SCOPE_DRIFT`；通过 `freeze-scope` 重新冻结后，必须重新执行代码评审及受影响的测试/归档步骤，不重写原人工批准链。已归档历史记录保留原状，必要时使用对应历史运行包只读复核。

`resume` 还必须检查规划基线和实现许可。规划期出现提前实现时保存原 Gate 恢复点并进入 `blocked`；变更恢复后只回到原 Gate，不得把提前代码视为已完成阶段。

`resume` 和所有控制动作还必须校验 Feature 生成边界。额外文件、目录、软链接、提前阶段资产或未受控兄弟 Feature 触发 `UNEXPECTED_FEATURE_LAYOUT`，并保存原阶段、状态、原阻塞信息和唯一下一动作。违规路径移走后才能恢复；控制器不得自动删除，也不得将其补登记为合法资产。Archive 检查必须在布局错误为零时才可通过。

对于可恢复的阻塞阶段，修复记录中的原因并重复同一个必需动作。阻塞或终态 Attempt 之后需要重新执行时，`restart-attempt` 必须由新的明确用户重试/重启消息触发；它会增加 Attempt、使旧批准失效、清空质量结果和范围，并从最早需要重新批准的持久化阶段开始。

历史 Feature 样例迁移为 `historical-example` 和 `superseded`。不回填或接受其旧批准。它们只供参考，不能恢复执行，也不因当前语言规范而改写其不可变内容。

## 11. Git 提交与推送规则

自动提交不是 SDD2 流程节点。本 Skill 不得执行 `git add`、`git commit` 或 `git push`，也不得因代码生成、测试通过、Archive 完成或上层通用工作流规则而推断提交授权。

活动 Attempt 的 Git Guard 是第二道确定性防线。它只在 worktree 的活动锁存在时拒绝操作，流程完成或明确关闭并释放锁后恢复原有 Git 行为。流程结束后的提交仍需用户在新的明确消息中另行要求；不得复用 Brief、阶段批准或 Archive 批准作为提交授权。

## 12. 失败规则

任何控制命令返回非零都必须立即停止。将错误记录为阻塞原因，不得手工绕过；只有状态恢复有效，或用户明确关闭/重启 Attempt 后才能继续。

`FEATURE_GENERATION_BOUNDARY_REJECTED` 表示初始化前已出现额外文件、错误 Feature 路径或未受控兄弟 Feature。`UNEXPECTED_FEATURE_LAYOUT` 表示活动流程中检测到白名单外路径或提前阶段资产。两者都必须报告完整相对路径；先由人确认后移走或删除，再执行 `resume`，不得自动清理。

`STATE_EVENT_PROJECTION_MISMATCH` 或批准链绑定错误表示控制状态被改写、丢失或无法追溯，必须停止并保留证据。`UNIT_TEST_EXECUTION_*`、`UNIT_TEST_EVIDENCE_*` 或 `UNIT_TEST_SCOPE_CHANGED` 表示测试未被真实观察、证据无效或测试过程改变范围，必须从当前有效范围恢复并重走必要质量 Gate。
