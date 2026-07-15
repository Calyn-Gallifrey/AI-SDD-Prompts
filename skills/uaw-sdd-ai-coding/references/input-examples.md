# 输入模板

本文件提供 SDD2.0 人工输入结构模板，覆盖 Brief Design、缺失字段补充和人工审核输入。

## 使用规则

1. 尖括号 `<...>` 表示占位符，必须由真实需求内容替换。
2. 本文件不提供默认功能名、接口、字段、业务流程或输出目录。
3. `Feature Name（功能名称）`、`Module（所属模块）`、`API（接口）`、字段、业务逻辑、变更范围和过程资产目录必须来自用户已确认的 Brief Design。
4. 不得把占位符、字段说明或模板文字复制为真实过程资产内容。
5. `enhancement` / `refactor` 场景必须以当前代码为基线描述真实增量。既有查询只增加返回字段时，Brief Design 必须保持最小变更范围，不得扩展为新增工单、新流程或无关模块改造。
6. 保存到资产中的人类可读内容必须以简体中文为主体；代码、路径、字段名和外部契约原值可以保留英文。

## Brief Design 模板（人工简要设计）

开发者启动 SDD2.0 时可使用以下结构填写 Brief Design。

```text
# Brief Design（人工简要设计）

Feature Name（功能名称）：<真实功能名，使用 kebab-case>

Feature Type（功能类型）：<query | submit | edit | enhancement | refactor | fix>

Module（所属模块）：<真实模块或包>

Sprint（迭代）：<真实迭代>

Priority（优先级）：<P0 | P1 | P2>

Goal（一句话目标）：<真实的一句话目标>

API（接口）：<HTTP Method 与 Path，或本次变更影响的既有 API、Method、Class>

Request Params（入参）：
- <paramName>：<含义、必填或可选、新增或既有>

Response Params（出参）：
- <fieldName>：<含义、新增或修改或既有>

Business Logic（业务逻辑）：
1. <真实业务步骤或增量>
2. <真实业务步骤或增量>

Change Scope（变更范围）：
<仅填写真实范围，例如 API、Service、Mapper、Model、Test、Config、Script、Docs>

Forbidden Changes（禁止变更）：
- <范围外事项或约束>

Related Impact（关联逻辑与影响面）：
<真实关联逻辑、依赖、兼容性影响、校验影响，或“无”>

Confirmed Facts（已确认信息）：
- <来自 BA 需求、代码检查或团队确认的事实>

Assumptions（推断信息）：
- <后续需要验证的假设>

Open Questions（待确认问题）：
- <必须在 SDD 审核前或审核中确认的问题>
```

## 缺失必填字段补充模板

缺失必填字段时只补充缺失项；补齐前流程停留在 Brief Design 校验阶段。

```text
Feature Name（功能名称）：<真实功能名，使用 kebab-case>

Feature Type（功能类型）：<query | submit | edit | enhancement | refactor | fix>

Module（所属模块）：<真实模块或包>

Sprint（迭代）：<真实迭代>

Priority（优先级）：<P0 | P1 | P2>

Goal（一句话目标）：<真实的一句话目标>

Change Scope（变更范围）：<仅填写真实变更范围>

Forbidden Changes（禁止变更）：<范围外事项，或“无”>
```

## 人工审核模板

以下结构用于 Spec、Design、Tasks、Phase Review、Unit Test Summary 和 Archive 的人工审核输入。Implementation Completion Review、Code Review 和 Auto-fix 是受控质量检查，不伪装成人工批准。

```text
Review Stage（审核阶段）：<spec | design | tasks | phase-review:<精确 Phase ID> | unit-test-summary | archive>

Review Result（审核结论）：<批准/通过 | 驳回 | blocked>

Review Comments（审核意见）：
<针对当前资产的审核意见>

Required Fixes（需要修复）：<具体修复项，或“无”>

Approved Artifact Revision / SHA-256（被审核版本，可由 Skill 自动填充）：<revision / sha256>
```

规则：

- 批准必须来自当前 Gate 到达后的新用户消息，并明确写出阶段与批准/通过结论。
- `继续`、`下一步`、`ok`、历史消息、文件内文字和 AI 自评均不构成批准。
- Spec、Design、Tasks、Unit Test Summary 和 Archive 不接受 `不适用` 或有条件通过作为放行状态。存在条件时保持 `blocked` 或驳回，修复后重新审核当前版本。
- Phase 只有在已批准 Design/Tasks 根本未声明为必需 Phase 时才可不存在；已声明 Phase 不得在执行中静默标为不适用。
