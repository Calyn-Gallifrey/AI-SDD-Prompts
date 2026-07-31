# Codex 交接

## 当前任务

修复 UAW-SDD 2.0 在弱模型上的第二个 P0 流程漏洞：模型会在 Feature 目录中提前或随意生成 Markdown、临时目录、错误路径文件和重复 Feature，导致流程资产与 Git 变更不可控。

开发者入口保持不变：提交简要提示词并调用 `uaw-sdd-ai-coding`。

## 范围与约束

- 范围只包含 SDD2.0。
- `sdd/` 属于 SDD1.0，本轮未读取、未修改。
- 未新增开发者命令、参数、表单或手工控制文件。
- 运行规则和新建或修订的公开资产以简体中文为主体；机器契约、路径、命令和必要技术英文保持精确。
- 按用户最新要求，本轮不更新 Word 操作指南及其生成器。
- 无关未跟踪文件 `docs/.DS_Store` 保持未暂存、未修改。
- 本轮只创建本地提交，不执行 push；用户后续手动推送。

## 根因

1. 原控制器只校验九项公开资产的阶段顺序，没有把 Feature 目录定义为封闭文件空间。
2. `init` 允许目标 Feature 在 Brief 之外预存辅助文件，也没有拒绝同一需求生成的第二个未受控 Feature。
3. 活动流程的 `resume`、审批、范围和质量动作没有统一校验额外文件、目录、软链接和提前阶段资产。
4. 名称看起来合法的 `.sdd2/implementation-scope.json`、归档证据或修订快照会被直接接受；缺字段的伪范围文件甚至可能触发未处理 `KeyError`。
5. 布局违规没有保存原阶段、原阻塞状态和唯一下一动作，清理后无法确定性恢复。

## 已实施修复

### 1. Feature 封闭白名单

- Feature 根目录只允许九项固定公开资产。
- 公开资产只能在已经记录或当前 `next_required_action` 对应的阶段存在。
- 初始化前目标目录只能包含 `brief-design.md`。
- 额外 notes/plan/result 文件、临时目录、嵌套错误路径、软链接和提前生成的 Design/Tasks 等资产均触发 `UNEXPECTED_FEATURE_LAYOUT`。

### 2. 内部证据真实性

- `.sdd2/feature-state.json`、审批/事件 JSONL、范围、归档证据和修订快照仍是规定控制资产，不被误判为普通乱文件。
- `implementation-scope.json` 只在活动实现许可存在时允许。
- `archive-evidence.json` 只在归档证据已由状态机进入对应动作后允许。
- 修订快照必须属于已记录阶段，修订号不得超过当前修订，内容 SHA-256 必须与文件名一致，同一阶段和修订不得重复。
- 缺字段或损坏的范围文件返回 `SCOPE_MANIFEST_INVALID`，不再抛出未处理异常，也不能被解释为实现许可。

### 3. 重复 Feature 控制

- `init` 和活动流程会检查同一 worktree 的其他变更 Feature 根目录。
- 未初始化或非终态的兄弟 Feature 触发 `UNCONTROLLED_SIBLING_FEATURE:<relative-path>`。
- 合法并行需求仍必须使用独立 Git worktree；开发者入口不变。

### 4. 可恢复阻断

- 布局违规保存原阶段、原 `stage_status`、原 `next_required_action` 和此前阻塞信息。
- 状态写为 `blocked / UNEXPECTED_FEATURE_LAYOUT`，并列出全部相对路径。
- 控制器不自动删除、不补登记、不把违规文件追认为合法资产。
- 人工确认并移走违规路径后，`resume` 精确恢复原状态和原动作。
- `restart-attempt` 与成功 Archive 都要求布局错误为零。

### 5. 既有 P0 防线保持有效

- Spec、Design、Tasks、Unit Test Summary 和 Archive Gate 后强制结束 assistant 回合。
- 实现许可前的 Feature 外代码漂移继续触发 `PREMATURE_IMPLEMENTATION_CHANGE`。
- 实现仍要求当前 Spec、Design、Tasks 批准绑定的 `implementation_permit`。
- 活动 Attempt 的 `git commit`、`git commit --no-verify` 和普通 `git push` 继续由 Git Guard 拒绝。

## 修改文件

- `skills/uaw-sdd-ai-coding/SKILL.md`
- `skills/uaw-sdd-ai-coding/references/context/routing-index.md`
- `skills/uaw-sdd-ai-coding/references/process-control.md`
- `skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md`
- `skills/uaw-sdd-ai-coding/references/sdd2-workflow.md`
- `skills/uaw-sdd-ai-coding/scripts/sdd2_control.py`
- `skills/uaw-sdd-ai-coding/scripts/tests/test_sdd2_control.py`
- `skills/uaw-sdd-ai-coding/scripts/validate_sdd2_assets.py`
- `CODEX_HANDOFF.md`

## 攻击式完整 Demo

永久回归用例 `test_weak_model_bypass_demo_recovers_and_archives` 在同一临时 Git Feature 中执行：

1. 生成并记录 Proposal 与 Spec，停在 Spec 人工 Gate。
2. 弱模型额外生成 `analysis-result.md` 和第二个 Feature 目录，并直接尝试批准 Spec，不先调用 `resume`。
3. 控制动作拒绝继续，状态写为 `blocked / UNEXPECTED_FEATURE_LAYOUT`，同时报告两个违规相对路径。
4. 移走违规路径后执行 `resume`，精确恢复 `spec / awaiting-approval / request-spec-approval`。
5. 再模拟提前修改生产代码，Spec 批准被 `PREMATURE_IMPLEMENTATION_CHANGE` 拒绝。
6. 暂存代码并执行 `git commit --no-verify`，提交被 `SDD2_COMMIT_BLOCKED` 拒绝，HEAD 不变。
7. 恢复生产代码后完成 Spec、Design、Tasks 批准、实现许可、Phase Review、范围冻结、完整 Code Review、Auto-fix、Unit Test Summary 和 Archive。
8. 最终 `validate.valid=true`，活动 Feature 锁释放。

另有独立测试覆盖初始化前额外文件、提前公开资产、真实当前资产、实现后重复 Feature、伪范围文件、伪修订快照和损坏范围文件。

## 验证结果

- Python 语法编译：通过。
- SDD2 控制器与静态验证器单元测试：38/38 通过。
- 完整弱模型攻击 Demo：通过。
- 静态资产与语言验证：54 个运行文件、51 个人类可读文件、3 个历史 Feature、26 个来源档案；0 error、0 warning。
- 三个 Skill 的 `quick_validate.py`：全部通过。
- Git whitespace：`git diff --check` 通过。
- Word 操作指南及生成器：本轮无改动、未纳入提交。

## 验收判断与边界

- 截图所反映的 Feature 流程资产乱生成问题已在仓库可控边界内关闭：额外路径、提前资产、重复 Feature 和伪内部证据都不能推进控制状态。
- 截图中的九项公开资产、`.sdd2` 状态/审批/事件文件和真实 `r<revision>-<sha256>.md` 快照是可追溯证据，不应为减少 IDE 变更数量而删除。
- 生产代码、测试和配置文件仍由已批准 Tasks、实现许可、允许/禁止路径、Phase Review、冻结范围和完整复审控制；本轮没有把生产代码范围改成固定文件名清单。
- 对主动改写控制器、关闭 Hook 或完全绕过 Skill 初始化的恶意执行者，不宣称系统级安全隔离；目标是约束实际调用 Skill 的弱模型错误行为。

## Git 与同步

- 分支：`main`；上游：`origin/main`。
- 上游当前为 `a553b0f`；上一项 P0 修复提交 `e3f385b` 尚未推送。
- 本轮文件边界修复在 `e3f385b` 之后创建本地提交；提交后预计相对 `origin/main` ahead 2。
- 用户明确要求本轮不要 push；接手后也不要自动重试 push，由用户手动推送。
- 不得暂存或提交 `docs/.DS_Store`。

## 下一步 P0

用户手动推送后，在真实弱模型环境用“简要提示词 + 调用 Skill”验证一次，重点观察：

1. 每个规划 Gate 是否在记录资产后停止。
2. 额外文件或第二个 Feature 是否立即进入 `UNEXPECTED_FEATURE_LAYOUT`。
3. 清理违规路径后是否只恢复原 Gate 和原唯一动作。
4. 活动 Attempt 是否继续拒绝自动提交。
