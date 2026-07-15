# UAW-SDD 2.0 运行时路由索引

本索引用于当前 SDD2 执行。`original/` 只保存迁移来源，不得加载为运行时指令。来源关系见 `source-provenance.json`。

## 1. 始终加载

```text
skills/uaw-sdd-ai-coding/SKILL.md
skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md
skills/uaw-sdd-ai-coding/references/language-policy.md
skills/uaw-sdd-ai-coding/references/sdd2-workflow.md
skills/uaw-sdd-ai-coding/references/process-control.md
skills/uaw-sdd-ai-coding/references/context/routing-index.md
```

请求补充缺失 Brief 字段前加载 `input-examples.md`。示例始终不具权威性。

## 2. 运行时资产

公开 Feature 资产：

```text
brief-design.md
proposal-input.md
spec.md
design.md
tasks.md
code-review-findings.md
auto-fix-summary.md
unit-test-summary.md
archive.md
```

内部控制资产：

```text
.sdd2/feature-state.json
.sdd2/gate-approvals.jsonl
.sdd2/events.jsonl
.sdd2/implementation-scope.json
.sdd2/archive-evidence.json
.sdd2/revisions/<artifact-stage>/r<revision>-<sha256>.md
```

公开入口仍是简要提示词加 Skill 调用。内部控制资产不要求开发者执行任何动作。公开资产正文必须通过简体中文主体校验。

## 3. 模板路由

| 资产 | 模板 |
|---|---|
| Proposal | `references/templates/proposal-input-internal-template.md` |
| Spec | `references/templates/spec-template.md` |
| Design | `references/templates/design-template.md` |
| Tasks | `references/templates/tasks-template.md` |
| Auto-fix | `references/templates/auto-fix-summary-template.md` |
| Archive | `references/templates/archive-template.md` |
| Code Review Findings | `skills/uaw-code-review/references/templates/sdd-code-review-findings-template.md` |
| Unit Test Summary | `skills/uaw-unit-test/references/templates/unit-test-summary-template.md` |

## 4. 后端规则路由

只加载 Brief、已批准 Design 或当前代码已确认触发条件的规则。

| 触发条件 | 运行时规则 |
|---|---|
| HTTP/API 入口或响应契约 | `references/rules/backend/backend-api.md` |
| 新建/修改数据库表或部署 DDL | `references/rules/backend/create-table.md` |
| MyBatis Mapper、查询或映射 | `references/rules/backend/mybatis-orm.md` |
| 当前认证用户 | `references/rules/backend/current-user.md` |
| EPI 集成 | `references/rules/backend/epi-gateway.md` |
| OM 外部 API 防腐层 | `references/rules/backend/om-api-acl.md` |
| MapStruct 转换 | `references/rules/backend/mapstruct-conversion.md` |
| Transaction 模块包结构 | `references/rules/backend/transaction-package-structure.md` |
| 新 Transaction Type 影响 Case Tracker | `references/rules/backend/case-tracker-compatibility.md` |

触发条件含糊，或必需外部/数据库契约无法确认时，记录待确认问题，并按影响阻塞 Design 或实现。绝不能使用代码示例补全缺口。

## 5. 模型规则路由

| 边界 | 运行时规则 |
|---|---|
| API/业务输入 | `references/rules/model/bo.md` |
| 内部/层间传输 | `references/rules/model/dto.md` |
| 持久化映射 | `references/rules/model/entity.md` |
| API/视图输出 | `references/rules/model/vo.md` |

是否需要新类型由当前模块约定决定。Design 未记录所有权或映射需求时，不得并行创建 BO/DTO/VO/Entity。

## 6. 测试规则路由

始终加载：

```text
skills/uaw-unit-test/SKILL.md
skills/uaw-unit-test/references/testing-profile-routing.md
```

然后选择一个主要目标规则：

| 目标 | 运行时规则 |
|---|---|
| Method/helper | `skills/uaw-unit-test/references/java/method-unit-test.md` |
| Service | `skills/uaw-unit-test/references/java/service-unit-test.md` |
| 静态工具/依赖 | `skills/uaw-unit-test/references/java/static-method-unit-test.md` |
| Controller | `skills/uaw-unit-test/references/java/controller-unit-test.md` |
| ServiceStrategy/选择器 | `skills/uaw-unit-test/references/java/service-strategy-unit-test.md` |

遵循 SDD 两轮测试交接：先生成测试源码，再重新冻结/复审，最后执行并总结。

## 7. Code Review 路由

SDD 调用：

```text
uaw-code-review / SDD_TASK_CODE_REVIEW
```

只加载 Code Review Skill、当前规则和 Markdown Findings 模板。HTML 模板只用于 Standalone 模式，SDD 模式不得加载。

## 8. 业务上下文路由

`transactions-dictionary.md` 是带来源标签的历史快照。只有任务匹配 Transaction 业务域时才加载。名称、包、状态和下拉值只作为候选项，必须由当前代码、配置、Schema 或当前用户输入确认后才能转为需求。

每次使用上下文时，在 Proposal/Design 中记录来源路径、来源哈希/版本、确认时间、当前确认来源和置信度。未确认的字典状态或枚举值不得授权代码或数据库变更。

## 9. Feature 类型关注点

| 类型 | 必查重点 |
|---|---|
| query | 权限、查询边界、基数、响应兼容性、脱敏 |
| submit | 校验、事务、幂等、持久化、状态转换 |
| edit | 目标身份、权限、审计、兼容性、部分失败 |
| enhancement | 当前行为/增量、兼容性、回归 |
| refactor | 行为保持、受限范围、回归 |
| fix | 复现、根因、最小修复、回归 |

Feature 类型不会自动加载业务规则。必须先确认真实范围。

## 10. 来源冲突规则

当前实现事实按以下优先级判断：

1. 当前用户已批准的需求；
2. 已捕获 Git 状态下的当前可执行代码、Schema 和配置；
3. 当前 SDD2 运行规则；
4. 带来源标签的上下文快照；
5. 示例或模板。

影响行为、范围、安全、数据或验收的冲突必须明确解决，否则阻塞流程。
