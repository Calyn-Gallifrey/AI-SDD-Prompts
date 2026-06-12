# SDD2.0 Workflow

## Entry Change

SDD2.0 starts from `Brief Design（人工简要设计）`.

`proposal-input.md` is generated internally after parsing the brief design and collecting missing required fields.

## Generalization Contract

1. SDD2.0 system files define workflow, gates, templates, routing, and engineering constraints; they do not define default business features.
2. Input templates and reference examples are never requirements. They must not be copied into feature names, output directories, API paths, field names, business logic, implementation code, tests, or archive content unless the same values are explicitly provided by the user as current requirement content.
3. Missing requirement information must be requested from the user or recorded as an open question. It must not be filled from examples, historical demo assets, or unrelated reference cases.
4. For enhancement and refactor work, the current codebase is the primary baseline. The generated SDD assets must describe the confirmed delta against existing behavior.
5. If the confirmed requirement is a minimal change to an existing query, such as adding a response field, the SDD scope must remain minimal and must not create a new submit flow, work order process, table, or module unless explicitly confirmed.

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

Reference assets are optional context, not required brief-design fields.

For `enhancement` or `refactor`, use the current codebase as the primary baseline. Only use prior SDD feature assets when the user explicitly provides them, names a previous feature, or the current codebase is insufficient to identify the existing behavior. If prior assets may be needed, scan the configured feature workspace before asking the user to provide a path.

## Feature Workspace Root

SDD2.x feature assets use one stable workspace root:

```text
sdd2-features/<SprintN>/<feature-name>/
```

Rules:

1. `sdd2-features` represents the SDD major version line, not the exact minor version.
2. `sdd2.1-features`, `sdd2.2-features`, and other minor-version roots are not used.
3. If SDD2.1 changes rules, keep writing feature assets under `sdd2-features` and record the executed Skill version inside the generated assets.
4. A new root for a future major version requires an explicit migration decision, not an automatic naming change.
5. `<feature-name>` must come from the confirmed current Brief Design. It must not be copied from input templates, reference examples, previous demo features, or historical process assets.
6. If `Feature Name（功能名称）` is missing or too generic, request confirmation before creating the feature asset directory.

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

In SDD mode, Code Review input is provided by SDD context, including feature directory, SDD artifacts, implementation scope, and expected output.

After Code Review and Auto-fix are complete, automatically invoke `uaw-unit-test` in SDD mode.

In SDD mode, unit-test inputs are derived from code changes, design, tasks, findings, and Auto-fix Summary.

## Required Output Assets

The feature asset directory must contain:

```text
brief-design.md
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

`brief-design.md` is the persisted user entry input. If the brief design came only from chat, capture the confirmed brief design into `brief-design.md` before assembling `proposal-input.md`.

## SDD2.0 Overrides

If bundled SDD reference content states that developers fill `proposal-input.md`, the SDD2.0 workflow contract takes precedence. In SDD2.0, developers provide `Brief Design（人工简要设计）`; the skill assembles `proposal-input.md`.

If bundled SDD reference content contain Code Review or Unit Test implementation details, keep the workflow gate in this skill but delegate execution to `uaw-code-review` and `uaw-unit-test`.

Fast Lane, mini-spec, mini-tasks, and archive-lite are outside the active SDD2.0 standard flow. They are only available when a later approved SDD version defines them explicitly.
