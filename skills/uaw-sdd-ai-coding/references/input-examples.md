# Input Examples

All human input examples must use:

```text
English Field（中文字段）：example value
```

## Brief Design（人工简要设计）

Require developers to use this format when starting SDD2.0.

```text
# Brief Design（人工简要设计）

Feature Name（功能名称）：policy-info-change-workorder

Feature Type（功能类型）：enhancement

Module（所属模块）：transaction / policy

Sprint（迭代）：sprint6

Priority（优先级）：P1

Goal（一句话目标）：新增保单信息变更工单能力，支持坐席为客户提交保单信息变更申请，并返回工单号。

API（接口）：POST /api/policy/change-workorder

Request Params（入参）：
- agreementNumber：协议号，必填
- changeType：变更类型，必填
- changeItems：变更项列表，必填
- remark：备注，非必填

Response Params（出参）：
- workorderId：工单号
- status：工单状态

Business Logic（业务逻辑）：
1. 校验 agreementNumber 属于当前客户。
2. 校验 changeType 是否在允许的变更类型内。
3. 根据 changeItems 生成保单信息变更工单。
4. 保存工单主表和变更明细。
5. 返回工单号和初始状态。

Change Scope（变更范围）：
API, Service, DB / Mapper, Model, Test

Forbidden Changes（禁止变更）：
- 不改现有保单查询接口。
- 不改现有保单提交主流程。
- 不改无关 transaction 功能。
- 不引入新的外部系统调用。

Related Impact（关联逻辑与影响面）：
当前用户上下文获取、Agreement 权限校验、工单保存逻辑、工单状态初始化逻辑、单元测试与接口验证。

Confirmed Facts（已确认信息）：
- 需要新增接口。
- 需要保存工单和变更明细。
- 需要校验协议号属于当前客户。

Assumptions（推断信息）：
- 工单初始状态可能为 CREATED。
- 工单号可能由现有工单编号规则生成。
- 当前用户信息可能来自 CurrentUser 工具类。

Open Questions（待确认问题）：
- 工单表是否已有，还是需要新建。
- changeType 枚举值来源。
- changeItems 具体字段结构。
- 是否需要调用外部系统。
```

## Missing Required Fields（缺失字段补充）

When required fields are missing, ask only for the missing fields. Do not continue until they are supplied.

```text
Feature Type（功能类型）：enhancement

Module（所属模块）：transaction / policy

Priority（优先级）：P1

Forbidden Changes（禁止变更）：无
```

## Human Review（人工审核）

Use this format for spec, design, tasks, phase-review, implementation, unit-test-summary, and archive review.

```text
Review Stage（审核阶段）：spec

Review Result（审核结论）：通过

Review Comments（审核意见）：
需求范围、非范围和验收标准清晰，可以进入 design。

Required Fixes（需要修复）：无

Next Stage Allowed（是否允许进入下一阶段）：yes
```
