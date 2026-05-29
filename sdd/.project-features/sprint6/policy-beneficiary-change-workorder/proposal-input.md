# 功能提案入口

> 来源：`developer-brief-design.md`

# 1. 任务基本信息（必须填写）

## 功能名称（必须填）

- policy-beneficiary-change-workorder

## 功能类型（必须填）

- submit

## 所属模块（必须填）

- policy / workorder

## 一句话目标（必须填）

- 新增保单受益人变更工单提交接口，生成待处理工单并返回脱敏受益人信息。

# 2. 变更识别信息（必须填写）

## 变更范围（必须填）

- API
- Service
- Repository
- Model（DTO / Entity / Enum）
- Test

## 禁止变更（必须填）

- 不接真实数据库。
- 不改已有保单信息变更工单接口。
- 不引入前端。
- 不修改 SDD 体系文件。
- 不生成 SDD 内部 Code Review HTML 报告。

## 优先级（必须填）

- P1

# 3. 历史功能引用（有则必填）

## 历史功能目录（条件必填）

- 不适用：本次为新增 submit 功能，不属于 enhancement / refactor。

# 4. 输出信息（建议填写）

## sprint（必填）

- sprint6

## 输出目录（可选）

- `.project-features/sprint6/policy-beneficiary-change-workorder/`

# 5. 补充信息（可选）

## 指定参考设计文档（可选）

- 未指定。

## 风险提醒（可选）

- 受益人证件号属于敏感信息，响应必须脱敏。
- 当前 demo 工程使用内存仓储，仅用于 SDD 流程验证，不作为生产持久化方案。
- 需避免在 SDD 内部 Code Review 阶段生成 HTML 报告。

# 6. AI 知识底座路径（固定｜无需修改）

- AI 知识底座根目录：`.project-ai/`
- 索引文件：`.project-ai/context/1.index.md`
- 上下文目录：`.project-ai/context/`
- 规则目录：`.project-ai/rules/`
- 模板目录：`.project-ai/templates/`

# 7. 当前代码扫描要求（固定｜无需修改）

## 默认扫描范围

- 当前仓库：`/Users/chenjialin763/Documents/code/AI/AI-SDD-Prompts`
- 当前代码工程：`uaw-sdd-demo/`
- 当前模块代码目录：`uaw-sdd-demo/src/main/java/com/example/uawsdddemo/`
- 当前模块测试目录：`uaw-sdd-demo/src/test/java/com/example/uawsdddemo/`
- 当前模块 repository：`uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/`
- 当前模块对象模型目录：`uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/`

## 需优先检查的存量类型

- Controller / Entry
- Service / Orchestration
- DTO / Entity / Enum
- Repository
- Test
- Maven 配置

# 8. 代理人工审核记录

| Time | Stage | Reviewer Role | Result | Comment |
|---|---|---|---|---|
| 2026-05-29 12:20:03 +0800 | Proposal | Codex 扮演人类审核 | 通过 | proposal 已覆盖简要设计中的目标、范围和禁止变更 |

# Process Status（强制｜流程闸门）

- Current Stage：Archive
- Stage Status：archived
- Last Completed Step：archive.md 已生成并完成代理最终审核
- Next Required Step：流程复盘与问题确认
- Human Confirmation Required：no（本轮由用户授权 Codex 扮演人类审核）
- Allowed Next Action：检查归档结果，确认是否要调整 SDD 体系模板
- Forbidden Next Action：未经用户确认直接修改 SDD 体系模板
- Updated At：2026-05-29 12:34:45 +0800

# Process Audit Trail（强制｜过程审核轨迹）

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-29 12:20:03 +0800 | Brief Design | 开发个人简要设计生成 | 用户描述的真实使用方式 | developer-brief-design.md | 通过代理审核 | Proposal |
| 2026-05-29 12:20:03 +0800 | Proposal | 按 proposal 模板生成提案 | developer-brief-design.md | proposal-input.md | 通过代理审核 | Spec |
| 2026-05-29 12:34:45 +0800 | Archive | 同步最终流程状态 | 全部 SDD 资产和代码 | archive.md | 通过代理审核 | Done |
