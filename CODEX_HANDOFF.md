# Codex 交接

## 当前任务

修复 UAW-SDD 2.0 在弱模型上的 P0 流程漏洞：Spec、Design 或 Tasks 未经当前人工确认时，模型仍可能提前生成生产代码，并在生成后自动提交。

开发者入口保持不变：提交简要提示词并调用 `uaw-sdd-ai-coding`。

## 范围与约束

- 范围只包含 SDD2.0。
- `sdd/` 属于 SDD1.0，本轮未读取、未修改。
- 未新增开发者命令、参数、表单或手工控制文件。
- 运行规则、指南和新建或修订的公开资产以简体中文为主体；机器契约、路径、命令和必要技术英文保持精确。
- 无关未跟踪文件 `docs/.DS_Store` 保持未暂存、未修改。

## 根因

1. 原 Skill 虽规定人工 Gate，但没有“记录 Gate 资产后立即结束 assistant 回合”的最高优先级协议，弱模型可能在同一回合继续执行。
2. 控制器只会拒绝越序的控制命令，没有在规划期保存 Feature 外 Git 基线；模型直接写代码后，后续审批可能继续被记录。
3. 实现入口只依赖 Tasks 状态和范围文件，没有独立许可同时绑定当前 Spec、Design、Tasks 的批准、修订、哈希、Attempt 与范围契约。
4. SDD2 没有 Git 层提交保护，弱模型可在流程进行中执行 `git commit`，包括 `--no-verify`。

## 已实施修复

### 1. 回合硬停止

- `skills/uaw-sdd-ai-coding/SKILL.md` 新增最高优先级 `P0 回合硬停止协议`。
- 每个 assistant 回合先执行 `resume`，只服从一个 `next_required_action`。
- 记录 Spec、Design、Tasks、Unit Test Summary 或 Archive 后，立即请求当前阶段批准并结束回合，不再调用工具。
- 只有 Gate 到达后的新用户消息可以批准当前阶段。
- Skill 在任何阶段都不得自动执行 `git add`、`git commit` 或 `git push`；Archive 批准也不构成 Git 授权。

### 2. 规划期基线与可恢复阻塞

- `init` 保存 Feature 目录外的分支、HEAD、tree、变更路径及文件哈希。
- 实现许可签发前，任何代码、测试、配置、构建文件或 Git HEAD 漂移都会写入 `PREMATURE_IMPLEMENTATION_CHANGE`，保存原 Gate 恢复点并进入 `blocked`。
- 提前变更撤销后，`resume` 精确恢复到原来的 Gate、状态和唯一下一动作；不得通过补写 Tasks 或手工改状态追认。

### 3. 批准绑定实现许可

- `capture-scope` 只有在当前 Spec、Design、Tasks 三项批准全部有效后才签发 `implementation_permit`。
- 许可绑定 Feature、Attempt、三项资产 revision/hash、三项 approval ID、范围契约哈希和许可自身哈希。
- 实现、Phase Review、Freeze、Review、Auto-fix、Unit Test 与 Archive 都会复核许可。
- 规划资产修订会撤销许可、删除旧范围，并强制重新批准和捕获。

### 4. Git Guard

- `init` 和活动 Feature 的 `resume` 透明安装 `prepare-commit-msg` 与 `pre-push` Guard。
- 活动锁存在时，所有普通提交以及 `git commit --no-verify` 都被拒绝；普通 `git push` 被拒绝。
- Guard 遵循仓库 `core.hooksPath`，已有同名 Hook 保存为 `.sdd2-original`，锁释放后继续执行原 Hook。
- Guard 不改变公开入口，也不要求开发者安装或运行额外命令。

## 修改文件

- `skills/uaw-sdd-ai-coding/SKILL.md`
- `skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md`
- `skills/uaw-sdd-ai-coding/references/process-control.md`
- `skills/uaw-sdd-ai-coding/references/sdd2-workflow.md`
- `skills/uaw-sdd-ai-coding/references/context/routing-index.md`
- `skills/uaw-sdd-ai-coding/references/schemas/feature-state.schema.json`
- `skills/uaw-sdd-ai-coding/references/schemas/implementation-scope.schema.json`
- `skills/uaw-sdd-ai-coding/scripts/sdd2_control.py`
- `skills/uaw-sdd-ai-coding/scripts/validate_sdd2_assets.py`
- `skills/uaw-sdd-ai-coding/scripts/tests/test_sdd2_control.py`
- `skills/uaw-sdd-ai-coding/scripts/tests/test_validate_sdd2_assets.py`
- `docs/generate_sdd2_guide.py`
- `docs/UAW-SDD2.0 Skill化方案说明与操作指南.docx`
- `CODEX_HANDOFF.md`

## 攻击式完整 Demo

新增永久回归用例 `test_weak_model_bypass_demo_recovers_and_archives`，在同一临时 Git Feature 中执行：

1. 生成并记录 Proposal 与 Spec。
2. 在 Spec 批准前修改生产代码。
3. Spec 批准被拒绝，状态写为 `blocked / PREMATURE_IMPLEMENTATION_CHANGE`。
4. 暂存代码并执行 `git commit --no-verify`，提交被 `SDD2_COMMIT_BLOCKED` 拒绝，HEAD 不变。
5. 恢复生产代码并执行 `resume`，精确回到 `spec / awaiting-approval / request-spec-approval`。
6. 依次完成 Spec、Design、Tasks 当前人工批准并签发实现许可。
7. 完成实现、Phase Review、范围冻结、Code Review、Auto-fix、Unit Test Summary、Archive 和最终批准。
8. 最终 `validate.valid=true`，活动 Feature 锁释放。

该 Demo 单独执行通过，并随全量回归再次通过。

## 验证结果

- Python 语法编译：通过。
- SDD2 控制与验证器单元测试：30/30 通过。
- 关键新增覆盖：提前代码漂移、原 Gate 恢复、实现许可签发与篡改、`--no-verify` 提交阻断、推送阻断、默认 Hook 兼容、自定义 `core.hooksPath` 兼容、完整成功路径。
- 静态资产与语言验证：54 个运行文件、51 个人类可读文件、3 个历史 Feature、26 个来源档案；0 error、0 warning。
- 三个 Skill 的 `quick_validate.py`：全部通过。
- 操作指南：重新生成，共 16 页；逐页检查无截断、重叠、缺字和编号续接错误。
- Git whitespace：`git diff --check` 通过。

## 验收判断与边界

- 本轮 P0 漏洞在 SDD2 仓库可控边界内关闭：规划 Gate 有明确停轮规则，提前实现不可被后续控制追认，实施必须持有批准绑定许可，活动 Attempt 不能自动提交或普通推送。
- 仓库控制器不能从 Git 内部证明聊天平台 UI 的真实用户身份；有平台 message ID 时应记录，平台未提供时仍依赖 Skill 的新消息硬停止协议。文档不得把模型传入的身份字段描述为平台级身份认证。
- 对主动关闭 Hook、改写控制器或完全绕过 Skill 初始化的恶意执行者，不宣称安全隔离；本次目标是约束实际调用 Skill 的弱模型错误行为。

## Git 与同步

- 分支：`main`；上游：`origin/main`。
- 本轮开始时已同步并确认 `main` 与 `origin/main` 一致，起始提交为 `a553b0f`。
- 本文件与 P0 修复使用同一提交。接手时先用上游对比确认同步状态；若本地 ahead，则直接重试 `git push origin main`。
- 不得暂存或提交 `docs/.DS_Store`。

## 下一步 P0

发布后在真实弱模型环境用“简要提示词 + 调用 Skill”再观察一轮，重点确认每个规划 Gate 都在记录资产后结束回合，并收集平台是否提供稳定 message ID。当前仓库内没有未完成的 P0 代码或文档修复。
