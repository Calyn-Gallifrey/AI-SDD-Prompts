# Input Templates

本文件提供 SDD2.0 人工输入结构模板，覆盖 Brief Design、缺失字段补充和人工审核输入。

## 使用规则

1. 尖括号 `<...>` 表示占位符，必须由真实需求内容替换。
2. 本文件不提供任何默认功能名、默认接口、默认字段、默认业务流程或默认输出目录。
3. `Feature Name（功能名称）`、`Module（所属模块）`、`API（接口）`、字段、业务逻辑、变更范围和过程资产目录必须来自用户已确认的 Brief Design。
4. 不得将本文件中的占位符、字段说明或模板文本复制为真实过程资产内容。
5. enhancement / refactor 场景必须以当前代码为基线描述真实增量；如果只是既有查询返回新增字段，Brief Design 必须表达为最小变更范围，不得扩展为新增工单、新增流程或无关模块改造。

## Brief Design Template（人工简要设计模板）

开发启动 SDD2.0 时使用以下结构填写 Brief Design。

```text
# Brief Design（人工简要设计）

Feature Name（功能名称）：<actual-feature-name-in-kebab-case>

Feature Type（功能类型）：<query | submit | edit | enhancement | refactor | fix>

Module（所属模块）：<actual-module-or-package>

Sprint（迭代）：<actual-sprint>

Priority（优先级）：<P0 | P1 | P2>

Goal（一句话目标）：<one-sentence-actual-goal>

API（接口）：<HTTP method and path, existing API, method, or class affected by this change>

Request Params（入参）：
- <paramName>：<description, required-or-optional, added-or-existing>

Response Params（出参）：
- <fieldName>：<description, added-or-changed-or-existing>

Business Logic（业务逻辑）：
1. <actual logic step or delta>
2. <actual logic step or delta>

Change Scope（变更范围）：
<actual scope only, such as API, Service, Mapper, Model, Test, Config, Script, Docs>

Forbidden Changes（禁止变更）：
- <out-of-scope item or constraint>

Related Impact（关联逻辑与影响面）：
<actual related logic, dependency, compatibility impact, validation impact, or none>

Confirmed Facts（已确认信息）：
- <confirmed fact from BA requirement, code inspection, or team confirmation>

Assumptions（推断信息）：
- <assumption that requires later validation>

Open Questions（待确认问题）：
- <question that must be confirmed before or during SDD review>
```

## Missing Required Fields Template（缺失字段补充模板）

缺失必填字段时，只补充缺失项；补齐前流程停留在 Brief Design 校验阶段。

```text
Feature Name（功能名称）：<actual-feature-name-in-kebab-case>

Feature Type（功能类型）：<query | submit | edit | enhancement | refactor | fix>

Module（所属模块）：<actual-module-or-package>

Sprint（迭代）：<actual-sprint>

Priority（优先级）：<P0 | P1 | P2>

Goal（一句话目标）：<one-sentence-actual-goal>

Change Scope（变更范围）：<actual-change-scope-only>

Forbidden Changes（禁止变更）：<out-of-scope items or none>
```

## Human Review Template（人工审核模板）

以下结构用于 spec、design、tasks、phase-review、implementation、unit-test-summary 和 archive 等审核输入。

```text
Review Stage（审核阶段）：<spec | design | tasks | phase-review | implementation | code-review | unit-test-summary | archive>

Review Result（审核结论）：<通过 | 有条件通过 | 驳回 | 不适用>

Review Comments（审核意见）：
<review comments based on the current asset>

Required Fixes（需要修复）：<required fixes or none>

Next Stage Allowed（是否允许进入下一阶段）：<yes | no | conditional>
```
