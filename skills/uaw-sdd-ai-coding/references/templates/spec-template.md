# 功能级 Spec 模板

> 本文件用于定义“本次任务到底要做什么、边界是什么、如何验收、哪些不能碰”。
> 本文件是 `proposal-input.md` 进入工程链路后的第一核心产物。
> 后续 `design.md`、`tasks.md`、implementation 都必须以本文件为边界依据。
> 本文件不是设计文档，不回答详细实现方式。
> 本文件不是施工清单，不拆编码步骤。

---

# 1. 基本信息

- 功能名称：
- 功能类型：query / submit / edit / enhancement / refactor / fix
- 所属模块：
- 所在 sprint：
- 优先级：P0 / P1 / P2
- 风险等级：low / medium / high（可留空，由 AI 判断）
- 对应 proposal：`./proposal-input.md`
- spec 文件路径：`./spec.md`
- 当前状态：draft / confirmed / rejected

---

# 2. Proposal 输入摘要

## 一句话目标

-

## 业务背景 / 触发原因

-

## 提案原始范围

-

## 提案禁止变更项

-

## 提案优先级

-

---

# 3. Context Assembly（上下文装配结果）

## Base Context（默认装配）

- 当前项目目录结构
- 当前模块基础语境
- 当前代码扫描范围
- 通用开发规范
- 流程控制规则：`skills/uaw-sdd-ai-coding/references/process-control.md`

## Conditional Context（按任务命中的上下文）

- 参考资产：
- 外部依赖背景：
- 兼容性背景：
- 特殊领域知识：

## 引用文件清单

- `skills/uaw-sdd-ai-coding/references/context/...`
- `skills/uaw-sdd-ai-coding/references/rules/...`
- `user-provided-reference-docs/...`
- `sdd2-features/...`（SDD2.x 主版本线功能资产根目录）

说明：

- 若未说明引用来源，后续 AI 容易自由发挥
- enhancement / refactor 场景下，必须显式列出参考资产来源
- 禁止默认引用旧版 SDD 目录或未被用户指定的历史路径

---

# 4. 当前现状（As-Is Baseline）

## 当前 Git 实物基线

- 现有接口：
- 现有 service：
- 现有 mapper：
- 现有对象：
- 现有流程：

## 当前存在问题 / 缺口

-
-

---

# 5. 参考资产（仅 enhancement / refactor）

## 引用路径

- `sdd2-features/.../`

## 已读取

- archive.md
- spec.md
- design.md
- tasks.md（按需）

## 可复用内容

-

## 与当前代码差异

-

---

# 6. 功能目标（To-Be）

## 本次必须达成

-
-

## 本次完成后预期结果

-

## 业务价值

-

---

# 7. 变更范围（In Scope）

## 包含范围

- 新增接口
- 修改查询逻辑
- 新增对象
- 补充测试
- 调整配置（如适用）

## 明确交付物

- 接口
- 字段
- 文档
- 测试
- 脚本（如适用）

---

# 8. 非范围（Out of Scope）

本次明确不做：

- 前端改版
- 无关模块重构
- 架构升级
- 大规模历史清理
- 非需求要求的额外优化

---

# 9. 不可变边界（Constraints / Non-goals）

明确禁止：

- 不改既有 API path
- 不改稳定核心流程
- 不改无关模块
- 不破坏向后兼容（如适用）
- 不改表结构（如适用）

补充：

-

---

# 10. Domain Mapping（领域映射，按需填写）

| 业务概念 | 系统对象 | 来源 |
|---|---|---|
|  |  |  |

说明：

- 解决“业务说法”和“代码对象”错位问题
- 若任务简单且无明显领域映射成本，可写“无特殊映射”

---

# 11. 依赖识别

## 内部依赖

- Service
- Shared Util
- Common Model
- Config

## 外部依赖

- 第三方接口
- Gateway
- ACL（防腐层）
- MQ（如适用）

## 数据依赖

- 表
- 视图
- 缓存
- 文件（如适用）

---

# 12. 风险识别

## 技术风险

-

## 兼容风险

-

## 交付风险

-

## 数据风险

-

## 风险重点（供 design 引用）

-
-
-

---

# 13. 回滚策略

若上线 / 合并失败：

- 回退代码提交
- 关闭开关
- 恢复旧逻辑
- 暂停入口
- 数据回退（如适用）

---

# 14. 验收标准（Acceptance Criteria）

## 功能验收

- 输入合法时结果正确
- 输入非法时错误符合预期
- 空结果场景符合预期
- 原有功能不受影响

## 技术验收

- Code Review 已完成
- Review-driven Auto-fix 已完成或明确不需要
- Unit Test Summary 已完成
- 无严重扫描告警
- 日志 / 异常符合规范

## 业务验收

- 满足需求描述
- 字段正确
- 权限正确
- 客户可验证通过（如适用）

---

# 15. 需传递给 Design 的约束

Design 阶段必须回答：

- 类与包如何落位
- 请求链路如何设计
- 数据访问如何设计
- 外部依赖如何接入
- 异常如何处理
- 测试如何覆盖
- 性能风险如何控制（如适用）

Design 阶段不得违反：

- 本 spec 的范围定义
- 本 spec 的边界约束
- 本 spec 的验收标准

---

# 16. 流程模式约束

当前 SDD2.0 标准流程只允许 `standard` 模式。

规则：

1. 不得默认启用 Fast Lane、mini-spec、mini-tasks 或 archive-lite。
2. 不得省略 design 阶段。
3. 不得省略 spec / design / tasks / phase / archive 的人工审核节点。
4. 若未来版本需要轻量模式，必须先在体系规则中正式定义输入、产物、审核点、质量闸门和归档规则。

---

# 17. 审核记录

- 审核状态：待审核 / 已通过 / 已驳回
- 审核意见：
- 审核人：
- 审核时间：
- 修订记录：

---

# 18. Code Review 前置约束（传递给 Tasks）

Tasks 阶段必须承接以下约束：

1. 代码实现完成后必须触发 SDD 内部 Code Review。
2. Code Review 入口固定为 `Entry Mode: SDD_TASK_CODE_REVIEW`。
3. Code Review 必须读取本功能目录下的 `proposal-input.md`、`spec.md`、`design.md`、`tasks.md`。
4. SDD 内部 Code Review 不生成 HTML 报告，不创建 `./reports/code-review/YYYY-MM-DD/`。
5. Code Review 发现 P0/P1 问题时，必须先 Review-driven Auto-fix，再进入 Unit Test Generation。
6. Archive 之前必须生成并记录 `code-review-findings.md`、Auto-fix Summary、Unit Test Summary。
7. 本 spec 的范围、边界、验收标准是 Code Review 的强制判定依据。


---

# Process Status（强制｜流程闸门）

- Current Stage：
- Stage Status：draft / confirmed / executing / review / fix / unit-test / archived / blocked
- Last Completed Step：
- Next Required Step：
- Human Confirmation Required：yes / no
- Allowed Next Action：
- Forbidden Next Action：
- Updated At：

# Process Audit Trail（强制｜过程审核轨迹）

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

规则：

1. 进入下一阶段前，必须先更新当前文件的 Process Status 和 Process Audit Trail。
2. 未更新状态区块，不允许进入下一阶段。
3. 如果某阶段被跳过或不适用，必须写明原因，禁止静默跳过。
4. 生成 archive.md 前，proposal-input.md、spec.md、design.md、tasks.md 均必须处于最终可归档状态。
5. Process Status 生命周期必须遵守 `skills/uaw-sdd-ai-coding/references/process-control.md`。
