# Codex 交接

## 当前任务

完成 UAW-SDD 2.0 的弱模型流程加固，并用真实小功能 Demo 验证以下五项 P0 要求：

1. 流程不得跳步或串 Feature。
2. Spec、Design、Tasks、Phase Review、Unit Test Summary 和 Archive 的人工审核不得丢失。
3. Feature 目录不得乱生成文件、目录或提前阶段资产。
4. Code Review、Auto-fix、Unit Test 和 Archive 质量门必须绑定当前实现范围及真实证据。
5. 状态、审批、质量门、测试证据和恢复点必须一致且可追溯。

开发者入口保持不变：提交简要提示词并调用 `uaw-sdd-ai-coding`。

## 范围与约束

- 范围只包含 SDD2.0。
- `sdd/` 属于 SDD1.0，本轮未读取、未修改。
- 未新增开发者命令、表单、手工控制文件或新的调用入口；新增命令只由主 Skill 内部调用。
- 体系文件和生成资产以简体中文为主体；路径、命令、枚举、哈希和必要技术名称保留英文。
- 未更新 Word 操作指南及其生成器。
- 无关未跟踪文件 `docs/.DS_Store` 保持未暂存、未修改。
- 本轮只创建本地提交，不执行 push；用户后续手动推送。

## 本轮确认的根因

1. Unit Test Gate 可接受模型填写的 `--evidence` 文字，缺少由控制器实际执行测试并观察退出码、测试数量和范围变化的硬证据。
2. `feature-state.json` 与最新事件没有完整状态投影绑定，弱模型或中断恢复可能把状态直接改到后续阶段。
3. 状态中的普通审批、Phase Review 和质量门投影没有全部反向绑定追加式记录，删除或伪造链记录后仍可能留下看似有效的状态。
4. `resume` 即使发现验证错误也可能以成功退出码返回，弱模型容易把“返回了状态”误判为“允许继续”。
5. 旧版无状态投影事件缺少独立的上游资产、批准和质量门前置条件校验，存在伪造后续阶段或完成态的空间。
6. 畸形单元测试证据可能触发未处理异常，不能稳定进入受控阻断。

## 已实施修复

### 1. 流程和状态控制

- 每个新事件写入完整控制状态的 `state_sha256`；`resume`、控制动作、验证、Archive 和恢复操作都校验最新事件投影。
- `resume` 增加顶层 `valid`；存在任何验证错误时退出码为 1。
- 明确定义阶段、状态、唯一下一动作、阻断码和恢复动作的合法组合，非法组合返回 `INVALID_STATE_TRANSITION`。
- 按当前阶段独立校验上游公开资产、Spec/Design/Tasks 批准、Phase Review、Code Review、Auto-fix、Unit Test 和归档批准。
- 旧版无投影事件只作为兼容输入，并由独立前置条件阻止跳过 Proposal、Spec 或直接伪造 `completed`。

### 2. 人工审核链

- Spec、Design、Tasks、Unit Test Summary 和 Archive 的状态投影必须唯一匹配 `gate-approvals.jsonl` 中的追加式记录。
- 每个 Phase Review 也写入同一审批链，绑定当前 Tasks 修订号和 SHA-256。
- 删除、重复或改写审批记录会触发 `APPROVAL_CHAIN_RECORD_*`、`APPROVAL_CHAIN_BINDING_MISMATCH` 或 `PHASE_REVIEW_*`，不能继续。
- 规划 Gate 与 Phase Review 仍要求当前用户消息来源；Demo 只有在用户明确授权后才能使用 `demo-simulation`。
- 每个规划 Gate 记录后继续执行 P0 回合硬停止协议，不允许同一 assistant 回合越过人工审核生成后续资产或代码。

### 3. 文件生成和串线控制

- Feature 根目录继续使用九项公开资产封闭白名单；额外文件、临时目录、软链接、提前资产和伪内部控制文件均阻断。
- `.sdd2/unit-test-evidence.json` 只有在控制器实际执行测试并写入状态投影后才允许存在；提前伪造会触发 `UNEXPECTED_CONTROL_FILE`。
- 同一 worktree 的第二个活动或未受控 Feature 继续触发 `UNCONTROLLED_SIBLING_FEATURE`；合法并行需求必须使用独立 worktree。
- 违规路径不会被自动删除或追认为合法资产；人工移走后，`resume` 只恢复原 Gate 和原唯一动作。
- 活动流程的 `git commit`、`git commit --no-verify` 和 `git push` 继续由 Git Guard 拒绝。

### 4. 质量门和真实测试证据

- 新增内部 `run-unit-test`：直接执行受支持测试 Runner，不经过 Shell 包装，拒绝 Maven/Gradle 跳过测试参数，超时限制为 1 到 3600 秒。
- 控制器记录命令、工作目录、开始/结束时间、退出码、输出哈希、有限输出片段、测试数量、测试源码哈希、范围前后 SHA-256 和结果。
- 零测试、零通过、失败/错误、超时、启动失败或测试期间改写冻结范围均不得得到 `passed`。
- Unit Test 的 `passed`/`failed` 必须匹配控制器观察结果和 `.sdd2/unit-test-evidence.json` 的证据 SHA-256；模型自报文字不能替代。
- Unit Test Summary 与 Archive 分别绑定测试执行证据 SHA-256 和当前范围 SHA-256。
- 畸形、删除、改写或跨范围测试证据均返回确定性阻断码，不抛出未处理异常。

### 5. 唯一事实来源和中文指令

- 主 Skill、Code Review Skill、Unit Test Skill、流程契约、状态 Schema、审批 Schema、模板和路由索引已同步。
- 新增 `unit-test-evidence.schema.json`，并纳入静态验证器的必需运行文件。
- 新增可重复执行的真实小功能 Demo 脚本；脚本使用临时 Git 仓库，结束后不留下正式 Feature 资产。

## 真实小功能 Demo

永久脚本：

`skills/uaw-sdd-ai-coding/scripts/demo_sdd2_small_feature.py`

Demo 在临时 Git 仓库中新增 Java `ContactDisplayNameFormatter`：

- `null` 返回空字符串。
- 去除首尾空白。
- 连续空白合并为一个普通空格。
- 三项 JUnit 测试覆盖空值、连续空白和普通名称。

完整执行 Proposal、Spec、Design、Tasks、两个 Phase Review、实现、范围冻结、Code Review、Auto-fix、真实 Unit Test、Unit Test Summary、Archive 和最终批准。

攻击式检查结果：

- 额外文件、提前 Design 和重复 Feature：已阻断。
- 直接改写控制状态：已阻断。
- Spec 人工 Gate 前修改生产代码：已阻断。
- 删除或篡改批准链、质量门投影和测试执行证据：已阻断。
- 活动流程执行 `git commit --no-verify`：已阻断，HEAD 不变。
- 真实 Maven 测试：3/3 通过。
- 最终状态：`archive / completed`。
- 九项公开资产完整。
- Demo Git 提交数始终为基线 1，没有自动提交。
- 最新测试执行证据 SHA-256：`fd1f78192e28917d2c6876808670f931fe7ddece7b79492dc037b7a9b4734835`。

## 验证结果

- SDD2 控制器完整回归：48/48 通过。
- 真实小功能端到端 Demo：通过。
- 现有 Java Demo 回归：36/36 通过，0 failure、0 error、0 skipped。
- 静态资产验证：3 个历史 Feature、51 个语言文件、56 个运行文件、26 个来源档案；0 error、0 warning。
- 三个 Skill 的 `quick_validate.py`：全部通过。
- Python 语法编译、JSON Schema 语法和 `git diff --check`：全部通过。
- Word 操作指南、Word 生成器和 SDD1.0：无改动。

## 验收判断与安全边界

- 在现有“简要提示词 + 调用 Skill”入口和控制器必须被调用的运行边界内，本轮五项 P0 要求均有确定性规则、失败码、恢复路径、回归测试和真实 Demo 证据，操作成熟度按 5/5 验收。
- 当前运行环境没有提供由宿主签名的用户消息 ID，因此本地控制器无法从密码学上证明 `source=user-message` 文本一定来自真人。现有防线是回合硬停止、来源/角色/批准文本检查、可用时的消息 ID 去重、批准链、实现许可、代码漂移检查和 Git Guard。
- 若未来要求抵抗主动伪造用户来源的恶意执行者，需要宿主提供可信消息身份，或增加用户 nonce/手工确认入口。后一项会改变当前使用方式，必须先获得用户批准，本轮未实施。
- 对主动修改控制器、关闭 Git Hook 或完全绕过 Skill 的恶意执行者，不宣称系统级安全隔离。

## 修改文件

- `skills/uaw-sdd-ai-coding/SKILL.md`
- `skills/uaw-code-review/SKILL.md`
- `skills/uaw-unit-test/SKILL.md`
- `skills/uaw-sdd-ai-coding/references/context/routing-index.md`
- `skills/uaw-sdd-ai-coding/references/process-control.md`
- `skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md`
- `skills/uaw-sdd-ai-coding/references/sdd2-workflow.md`
- `skills/uaw-sdd-ai-coding/references/schemas/feature-state.schema.json`
- `skills/uaw-sdd-ai-coding/references/schemas/gate-approval.schema.json`
- `skills/uaw-sdd-ai-coding/references/schemas/unit-test-evidence.schema.json`
- `skills/uaw-sdd-ai-coding/references/templates/archive-template.md`
- `skills/uaw-unit-test/references/templates/unit-test-summary-template.md`
- `skills/uaw-sdd-ai-coding/scripts/sdd2_control.py`
- `skills/uaw-sdd-ai-coding/scripts/tests/test_sdd2_control.py`
- `skills/uaw-sdd-ai-coding/scripts/demo_sdd2_small_feature.py`
- `skills/uaw-sdd-ai-coding/scripts/validate_sdd2_assets.py`
- `CODEX_HANDOFF.md`

## Git 与同步

- 分支：`main`；上游：`origin/main`。
- 上游当前为 `a553b0f`。
- 已有未推送提交：`e3f385b`、`d07d6b6`。
- 本文件所在提交使用消息 `fix(sdd2): bind workflow state to observed evidence`；完成后相对 `origin/main` ahead 3。
- 用户明确要求不要 push；接手后也不要自动重试，由用户手动推送。
- 不得暂存或提交 `docs/.DS_Store`。

## 下一步 P0

用户手动推送后，在真实弱模型环境使用原入口做一次 smoke test，重点观察：

1. 每个规划 Gate 是否记录后立即结束回合。
2. 额外文件、提前资产或第二个 Feature 是否进入确定性阻断。
3. 清理违规路径后是否只恢复原 Gate 和原唯一动作。
4. Unit Test 是否只能通过控制器实际执行证据进入 passed。
5. 活动 Attempt 是否继续拒绝自动提交。
