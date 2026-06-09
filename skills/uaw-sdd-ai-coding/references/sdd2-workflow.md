# SDD2.0 Workflow

## Entry Change

SDD2.0 starts from `Brief Design（人工简要设计）`.

Do not ask developers to fill `proposal-input.md`. Generate `proposal-input.md` internally after parsing the brief design and collecting missing required fields.

## Proposal Assembly

Map the brief design to proposal fields:

| Brief Design field | proposal-input field |
|---|---|
| Feature Name（功能名称） | 功能名称 |
| Feature Type（功能类型） | 功能类型 |
| Module（所属模块） | 所属模块 |
| Goal（一句话目标） | 一句话目标 |
| Change Scope（变更范围） | 变更范围 |
| Forbidden Changes（禁止变更） | 禁止变更 |
| Priority（优先级） | 优先级 |
| Sprint（迭代） | sprint |
| Open Questions（待确认问题） | 风险提醒 / 待确认 |

If `Feature Type（功能类型）` is `enhancement` or `refactor`, require historical feature asset path when the task depends on previous SDD assets. If the user does not know it, scan likely `sdd2-features/` directories before asking.

## Stage Flow

Run the flow in this exact order:

```text
Brief Design
→ proposal-input.md
→ spec.md
→ human spec review
→ design.md
→ human design review
→ tasks.md
→ human tasks review
→ implementation by Phase
→ Phase Review
→ uaw-code-review in SDD_TASK_CODE_REVIEW mode
→ Review-driven Auto-fix
→ uaw-unit-test in SDD mode
→ Unit Test Summary
→ Archive status sync
→ archive.md
→ final human archive review
```

## Automatic Skill Calls

After code implementation is complete, automatically invoke `uaw-code-review` in `SDD_TASK_CODE_REVIEW` mode.

Do not ask the user for Code Review input in SDD mode. The SDD context provides the feature directory, SDD artifacts, implementation scope, and expected output.

After Code Review and Auto-fix are complete, automatically invoke `uaw-unit-test` in SDD mode.

Do not ask the user to repeat unit-test inputs in SDD mode. Derive test targets from code changes, design, tasks, findings, and Auto-fix Summary.

## Required Output Assets

The feature asset directory must contain:

```text
proposal-input.md
spec.md
design.md
tasks.md
code-review-findings.md
archive.md
```

It must also contain or reference:

```text
Auto-fix Summary
Unit Test Summary
Process Status
Process Audit Trail
Phase Review records
```

## SDD2.0 Overrides

If bundled SDD reference content say that developers fill `proposal-input.md`, treat that as outdated. In SDD2.0, developers provide `Brief Design（人工简要设计）`; the skill assembles `proposal-input.md`.

If bundled SDD reference content contain Code Review or Unit Test implementation details, keep the workflow gate in this skill but delegate execution to `uaw-code-review` and `uaw-unit-test`.
