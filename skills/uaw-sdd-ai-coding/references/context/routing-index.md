# UAW SDD2.0 Routing Index

本文件定义 `uaw-sdd-ai-coding` 的上下文装配、知识路由和阶段交接规则。

本文件是 Skill 内部参考资料，不是 `proposal-input.md`、`spec.md`、`design.md`、`tasks.md` 或 `archive.md`。

## 1. Entry

SDD2.0 的用户入口是 `Brief Design（人工简要设计）`。

启动链路：

```text
Brief Design
→ proposal-input.md
→ spec.md
→ design.md
→ tasks.md
→ implementation by Phase
→ uaw-code-review / SDD_TASK_CODE_REVIEW
→ Review-driven Auto-fix
→ uaw-unit-test / SDD mode
→ Unit Test Summary
→ archive.md
```

`proposal-input.md` 由 Skill 根据人工简要设计自动组装，模板来源：

```text
skills/uaw-sdd-ai-coding/references/templates/proposal-input-internal-template.md
```

## 2. Skill Reference Paths

SDD 总控流程引用：

```text
skills/uaw-sdd-ai-coding/SKILL.md
skills/uaw-sdd-ai-coding/references/sdd2-workflow.md
skills/uaw-sdd-ai-coding/references/process-control.md
skills/uaw-sdd-ai-coding/references/input-examples.md
skills/uaw-sdd-ai-coding/references/context/routing-index.md
skills/uaw-sdd-ai-coding/references/context/transactions-dictionary.md
```

SDD 模板引用：

```text
skills/uaw-sdd-ai-coding/references/templates/proposal-input-internal-template.md
skills/uaw-sdd-ai-coding/references/templates/spec-template.md
skills/uaw-sdd-ai-coding/references/templates/design-template.md
skills/uaw-sdd-ai-coding/references/templates/tasks-template.md
skills/uaw-sdd-ai-coding/references/templates/archive-template.md
```

后端与模型规则引用：

```text
skills/uaw-sdd-ai-coding/references/rules/backend/
skills/uaw-sdd-ai-coding/references/rules/model/
```

代码评审 Skill 引用：

```text
skills/uaw-code-review/SKILL.md
skills/uaw-code-review/references/code-review-rules.md
skills/uaw-code-review/references/templates/sdd-code-review-findings-template.md
skills/uaw-code-review/references/templates/summary-report-template.html
skills/uaw-code-review/references/templates/personal-report-template.html
```

单元测试 Skill 引用：

```text
skills/uaw-unit-test/SKILL.md
skills/uaw-unit-test/references/testing-profile-routing.md
skills/uaw-unit-test/references/java/
```

## 3. Runtime Feature Assets

SDD2.0 运行时功能资产默认输出到当前代码工程内：

```text
sdd2-features/<SprintN>/<feature-name>/
```

功能资产目录必须包含：

```text
proposal-input.md
spec.md
design.md
tasks.md
code-review-findings.md
archive.md
```

功能资产目录必须包含或引用：

```text
Auto-fix Summary
Unit Test Summary
Process Status
Process Audit Trail
Phase Review records
```

## 4. Context Assembly

每次 SDD 任务默认装配：

- 当前代码工程目录结构。
- 当前模块基础语境。
- 当前代码扫描范围。
- `skills/uaw-sdd-ai-coding/references/process-control.md`。
- 与变更范围命中的后端规则、模型规则和业务词典。

按任务条件装配：

- enhancement / refactor 场景的历史功能资产。
- 用户提供的外部参考设计文档。
- 业务域词典和特殊集成规则。
- Code Review 和 Unit Test 的交接规则。

## 5. Routing Rules

`Feature Type（功能类型）` 决定流程重点：

| Feature Type | Routing Focus |
|---|---|
| query | API、权限、查询条件、返回模型、分页与脱敏 |
| submit | API、校验、事务、幂等、落库、状态流转 |
| edit | 数据定位、权限、变更范围、审计、历史兼容 |
| enhancement | 历史资产引用、差异说明、兼容性、回归风险 |
| refactor | 行为保持、范围控制、回归验证、禁止功能扩张 |
| fix | 缺陷复现、修复边界、回归验证、影响面控制 |

`Change Scope（变更范围）` 决定规则装配：

| Change Scope | Required References |
|---|---|
| API | `skills/uaw-sdd-ai-coding/references/rules/backend/backend-api.md` |
| Service | `skills/uaw-sdd-ai-coding/references/rules/backend/transaction-package-structure.md` |
| DB / Mapper | `skills/uaw-sdd-ai-coding/references/rules/backend/create-table.md`, `skills/uaw-sdd-ai-coding/references/rules/backend/mybatis-orm.md` |
| Model | `skills/uaw-sdd-ai-coding/references/rules/model/` |
| Test | `skills/uaw-unit-test/references/testing-profile-routing.md` |

## 6. Code Review Routing

SDD 流程内代码实现完成后，必须自动调用：

```text
uaw-code-review / SDD_TASK_CODE_REVIEW
```

SDD 模式下不要求用户填写 Code Review 输入，不读取 HTML 模板，不生成 HTML 报告，只在当前功能资产目录生成：

```text
code-review-findings.md
```

Standalone Code Review 才允许读取：

```text
skills/uaw-code-review/references/templates/summary-report-template.html
skills/uaw-code-review/references/templates/personal-report-template.html
```

## 7. Unit Test Routing

Review-driven Auto-fix 完成后，必须自动调用：

```text
uaw-unit-test / SDD mode
```

SDD 模式下不要求用户重复填写单元测试输入。测试目标、变更文件、测试框架和验证方式优先从 SDD 资产、代码变更和项目文件中自动识别。

## 8. Archive Gate

生成 `archive.md` 前必须满足：

- `spec.md`、`design.md`、`tasks.md` 已通过人工审核。
- tasks Phase Review 已完成。
- `code-review-findings.md` 已生成。
- Review-driven Auto-fix 已完成或明确不适用。
- Unit Test Summary 已完成或明确不适用原因。
- Process Status 和 Process Audit Trail 已同步。
