# SDD2.0 资产与交接流程

`sdd2-control-contract.md` 负责全部状态、批准、失效、恢复和 Archive 语义。本文件只定义资产职责和 Skill 交接。

## 入口与工作区

开发者提交简短的 Brief Design 并调用 `uaw-sdd-ai-coding`。Skill 保存 Brief 并完成全部内部控制操作，不引入新的开发者命令或表单。

Feature 目录：

```text
sdd2-features/<SprintN>/<feature-name>/
```

`<feature-name>` 只能来自当前已确认 Brief。SDD2 的小版本继续使用 `sdd2-features`；新建根目录必须先明确批准主版本迁移决策。

所有人类可读资产遵循 `language-policy.md`，以简体中文为主体。

初始化前，唯一 Feature 目录只能包含 `brief-design.md`。初始化后只能逐阶段生成本文件列出的九项公开资产；`.sdd2` 下的状态、审批、事件、范围、真实测试执行证据、归档证据和修订快照由控制器生成。其他说明文件、候选输出、临时目录、软链接、错误绝对路径文件和重复 Feature 目录均不属于流程资产。

## 资产映射

| 资产 | 职责 | 输入 | 输出/使用方 | 完成条件 |
|---|---|---|---|---|
| `brief-design.md` | 保存当前人工简要设计 | 当前用户消息 | Proposal 组装 | 全部必填字段已确认且中文主体校验通过 |
| `proposal-input.md` | 规范化内部规划输入 | Brief 与定向代码/上下文发现 | Spec 生成 | 来源事实和待确认问题已识别 |
| `spec.md` | 定义行为与验收边界 | Proposal 与当前行为 | 人工 Spec 审核、Design | 已记录并明确批准 |
| `design.md` | 定义技术增量与约束 | 已批准 Spec、当前代码、路由规则 | 人工 Design 审核、Tasks | 已记录并明确批准 |
| `tasks.md` | 定义受限 Phase 和文件 | 已批准 Design | 人工 Tasks 审核、实现范围 | 已记录并明确批准 |
| `code-review-findings.md` | 保存不可变的首次评审发现 | 冻结范围与已批准 SDD 资产 | Auto-fix | 针对同一范围记录 Gate |
| `auto-fix-summary.md` | 映射每项发现的修复/处置 | Findings 与代码变更 | 复审、Unit Test | Gate 在同一已评审范围上关闭 |
| `unit-test-summary.md` | 记录测试源码变更和控制器观察结果 | 已评审范围与 `.sdd2/unit-test-evidence.json` | 人工 Unit Test Summary 审核 | 真实执行 Gate 通过且 Summary 已批准 |
| `archive.md` | 最终可追溯交付记录 | 全部当前资产与 Archive 证据 | 最终人工审核 | Archive 检查通过且最终批准已记录 |

`proposal-input.md` 是内部资产。参考示例和模板不是业务需求。

## Proposal 字段映射

| Brief 字段 | Proposal 字段 |
|---|---|
| Feature Name | 功能名称 |
| Feature Type | 功能类型 |
| Module | 所属模块 |
| Goal | 一句话目标 |
| Change Scope | 变更范围 |
| Forbidden Changes | 禁止变更 |
| Priority | 优先级 |
| Sprint | 迭代 |
| Open Questions | 风险与待确认问题 |

对于 `enhancement`、`refactor` 和 `fix`，先检查当前代码，只描述已确认增量。只有用户明确指定，或当前代码无法确定行为时，才能使用旧 Feature 资产，并标记为历史上下文。

## 交接顺序

```text
Brief -> Proposal -> Spec 批准 -> Design 批准 -> Tasks 批准
-> 实现许可 -> 分 Phase 实现 + Phase Review
-> uaw-code-review / SDD_TASK_CODE_REVIEW
-> Auto-fix + 范围变化时完整复审
-> uaw-unit-test / SDD mode
-> 控制器真实执行测试并固化证据
-> Unit Test Summary 批准
-> Archive 证据 -> Archive 批准 -> completed
```

Spec、Design、Tasks 的每个箭头都跨越独立 assistant 回合：生成并记录当前 Gate 资产后必须结束回合，等待用户新消息批准。Tasks 批准后仍不能直接写代码；只有内部捕获范围并签发活动 `implementation_permit` 后才能进入实现。

实现许可绑定当前 Attempt、三项资产修订/哈希、三项人工批准 ID、Git 基线和范围契约哈希。任一绑定变化都会拒绝后续实现与质量动作。

### Code Review 交接

提供：

- Feature 目录和状态文件路径；
- 已批准 Spec、Design 和 Tasks 的修订/哈希；
- Git 仓库、分支、基线提交、冻结快照哈希和精确变更文件清单；
- Code Review 输出路径。

Code Review Skill 必须使用固定范围，不得根据 `git status`、上游漂移或仅凭 Feature 资产目录推断范围。

### Unit Test 交接

提供：

- 同一个当前冻结范围；
- Design 测试策略和 Tasks 测试 Phase；
- 不可变 Code Review Findings 和 Auto-fix Summary；
- 已识别的项目测试栈和路由测试配置；
- 目标测试源码路径和必需执行证据。

Unit Test Skill 必须先生成或更新测试代码；该变化进入冻结范围并完成复审后，由控制器实际执行受支持测试入口并生成 `.sdd2/unit-test-evidence.json`，最后才根据该证据生成 Summary。无法确认目标代码、测试框架或可执行测试入口时记录 `blocked`；不得用文字计划、手工检查、零测试或模型自述代替单元测试源码和真实执行证据。

## 变更处理

用户需求变化不是非正式编辑。更新最早受影响的资产并记录，让控制器确定性失效下游结果，再重复所有已过期的批准和 Gate。请求实际属于另一个 Feature 时，新建独立 Feature/worktree，不得重定向活动状态。

公开资产必须按当前 `next_required_action` 逐个生成。提前生成 Design、Tasks 或其他下游资产，或在同一 worktree 创建第二个未受控 Feature，都会进入 `UNEXPECTED_FEATURE_LAYOUT`。控制器列出具体路径并保留原恢复点，不自动删除；违规路径移走后 `resume` 返回原动作。

首次实现许可签发前，Feature 目录外出现代码、测试、配置、构建或 Git HEAD 变化时，流程立即阻塞并保存原人工 Gate。恢复到规划基线后才能回到原 Gate；提前实现不能通过补文档获得追认。

Git 提交和推送不属于本流程的产物或阶段。活动 Feature 的 Guard 阻止提交/推送；Archive 最终批准后 Skill 结束回合，不自动执行 Git 命令。

## 非目标

Fast Lane、mini-spec、mini-tasks、archive-lite 和其他公开入口模式不属于 SDD2.0。它们需要单独批准的流程版本。
