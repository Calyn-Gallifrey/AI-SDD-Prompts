# SDD Process Control Rules

> 本文件定义 UAW-SDD 功能流程的状态、审核、验证和归档控制规则。
> 所有 SDD 功能资产必须遵守本文件；若模板与本文件冲突，以本文件为准，并同步修正模板。

---

# 1. Process Status 生命周期

## 1.1 状态含义

- `draft`：文件已创建但尚未完成。
- `confirmed`：当前阶段已通过人工确认，可进入下一阶段。
- `executing`：当前阶段正在实施。
- `review`：当前阶段正在审核。
- `fix`：根据审核问题修复中。
- `unit-test`：测试生成或测试验证中。
- `archived`：功能流程已完成归档。
- `blocked`：当前阶段阻塞，必须先处理阻塞原因。

## 1.2 阶段状态更新规则

每个核心 SDD 资产文件必须包含 `Process Status` 与 `Process Audit Trail`：

- `proposal-input.md`
- `spec.md`
- `design.md`
- `tasks.md`
- `archive.md`

规则：

1. 进入下一阶段前，当前阶段文件必须更新为可进入下一阶段的状态。
2. 每次阶段确认、驳回、跳过、不适用、修复、测试、归档，都必须追加 `Process Audit Trail`。
3. `Process Status` 只记录当前文件在整条流程中的最新有效状态。
4. `Process Audit Trail` 记录关键阶段流转，不记录无价值流水账。
5. 如果某阶段被跳过或不适用，必须写明原因和批准角色。

## 1.3 Process Status 字段口径

`Process Status` 必须至少包含以下字段：

- Current Stage
- Stage Status
- Last Completed Step
- Next Required Step
- Blocked Reason

可按流程需要补充以下字段：

- Human Confirmation Required
- Allowed Next Action
- Forbidden Next Action
- Updated At

规则：

1. 核心判断以必填字段和 `Process Audit Trail` 为准。
2. 模板可以提供扩展字段，但扩展字段缺失不单独构成流程阻塞。
3. `archive.md` 建议保留扩展字段，用于明确归档后的允许动作和禁止动作。
4. 如果 `Stage Status=blocked`，`Blocked Reason` 必须写明阻塞原因、责任角色和恢复条件。

## 1.4 Archive 前状态同步

生成 `archive.md` 前，必须完成状态同步：

1. `proposal-input.md`、`spec.md`、`design.md`、`tasks.md` 均不得停留在旧阶段待办状态。
2. 上述文件的 `Process Status` 必须更新到最终可归档状态。
3. 上述文件的 `Process Audit Trail` 必须追加 Archive 同步记录。
4. `archive.md` 必须记录状态同步结果。
5. 未完成状态同步时，禁止标记 Archive 完成。

---

# 2. 人工审核规则

## 2.1 审核节点

标准流程必须包含以下人工审核节点：

1. spec 审核
2. design 审核
3. tasks 审核
4. tasks 中每个执行 Phase 审核
5. 实施结果审核
6. SDD 内部 Code Review
7. Unit Test Summary 审核
8. Archive 审核

规则：

1. 未通过人工审核的阶段不得进入下一阶段。
2. 如果由 AI 代理人工审核，必须在功能资产中标明审核角色，不得伪装为真实人员审批。
3. 审核结论必须是：通过 / 有条件通过 / 驳回 / 不适用。
4. 有条件通过必须记录条件、修复范围和后续验证方式。

## 2.2 Phase Review

`tasks.md` 中每个执行 Phase 完成后，必须记录 Phase Review。

必须记录：

| Phase | Reviewer Role | Review Time | Result | Findings | Required Action | Next Phase Allowed |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

规则：

1. 每个实际执行的 Phase 都必须有审核记录。
2. 被跳过的 Phase 必须记录“不适用原因”。
3. Phase Review 未通过时，不得进入下一 Phase。
4. Phase Review 中发现的问题必须回到对应 Phase 修复。
5. Phase Review 不替代 SDD 内部 Code Review。

---

# 3. 验证方式记录

SDD 不强制绑定单一验证命令或单一执行环境。

允许的验证方式包括：

- IDE 内置 Maven / Gradle
- Maven Wrapper / Gradle Wrapper
- 本机 Maven / Gradle
- CI Pipeline
- 项目脚本
- 手工接口验证
- 其他经团队确认的验证方式

必须记录：

- Validation Method：IDE / Wrapper / Local CLI / CI / Script / Manual / Other
- Execution Environment：本机 / CI / 开发容器 / IDE / 其他
- Build Tool 或测试执行器
- 实际执行入口：命令、IDE 配置名、CI Job、脚本路径或手工验证说明
- 测试结果：pass / fail / not applicable
- 测试数量或覆盖场景
- warning / failure / skipped 说明

规则：

1. 不得把本机是否安装 `mvn` 作为 SDD 流程前置条件。
2. 如当前环境无法执行命令，允许记录 IDE / CI / Wrapper / 手工验证作为实际验证方式。
3. 无法自动验证时，必须说明原因、替代验证方式和归档影响。
4. 验证记录不得替代 Code Review 和 Unit Test Summary。

---

# 4. SDD 内部 Code Review Findings 产物

SDD 内部 Code Review 必须输出 Markdown Findings 产物，不生成 HTML 报告。

固定文件：

```text
./code-review-findings.md
```

规则：

1. `code-review-findings.md` 必须生成在当前功能资产目录。
2. `code-review-findings.md` 只用于 SDD 内部质量闸门，不得作为独立 HTML 评审报告。
3. `code-review-findings.md` 必须被 `tasks.md` 和 `archive.md` 引用。
4. Findings 完成后必须进入 Review-driven Auto-fix。
5. Auto-fix 完成后必须进入 Unit Test Generation / Unit Test Summary。
6. 独立 Git 范围评审和独立工作区快照评审仍按 `UAW-Code-Review.md` 的 standalone 规则生成 HTML 报告。

---

# 5. 禁止事项

1. 禁止从 proposal 直接生成代码。
2. 禁止跳过人工审核节点。
3. 禁止跳过 Phase Review。
4. 禁止跳过 SDD 内部 Code Review。
5. 禁止在 Code Review / Auto-fix / Unit Test Summary 完成前生成 Archive。
6. 禁止只扫描 SDD 资产目录而不扫描当前代码现状。
7. 禁止把本地命令可用性作为唯一验证前置条件。
8. 禁止在 SDD 内部 Code Review 中生成 HTML 报告。
