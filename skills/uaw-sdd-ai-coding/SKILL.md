---
name: uaw-sdd-ai-coding
description: Run the UAW SDD2.0 AI coding workflow for backend feature delivery. Use when the user provides a human brief design, asks to start SDD, generate proposal/spec/design/tasks/archive, implement code under SDD gates, or continue a UAW SDD feature flow. This skill assembles proposal-input.md internally, enforces human review gates, and automatically invokes UAW code review and unit test skills after tasks implementation.
---

# UAW SDD AI Coding

## Core Contract

Use this skill to run SDD2.0 from a human brief design through archive.

The user-facing entry is `Brief Design（人工简要设计）`. Do not ask the user to manually fill `proposal-input.md`. Parse the brief design, ask for missing required fields in the chat window, then assemble `proposal-input.md` as the internal SDD entry asset.

Always read `references/input-examples.md` before requesting human input. All user-facing input examples must use `English Field（中文字段）：示例值`.

## Required Brief Fields

Extract these fields from the human brief design:

- `Feature Name（功能名称）`
- `Feature Type（功能类型）`: `query`, `submit`, `edit`, `enhancement`, `refactor`, or `fix`
- `Module（所属模块）`
- `Sprint（迭代）`
- `Priority（优先级）`: `P0`, `P1`, or `P2`
- `Goal（一句话目标）`
- `Change Scope（变更范围）`
- `Forbidden Changes（禁止变更）`

If any required field is missing, stop and ask only for the missing fields using the missing-field example in `references/input-examples.md`. Do not infer or fabricate required fields.

## Workflow

1. Read `references/input-examples.md`.
2. Parse the human brief design and collect missing required fields.
3. Assemble `proposal-input.md` using `references/templates/proposal-input-internal-template.md`.
4. Read `references/sdd2-workflow.md` and `references/process-control.md`.
5. Load current code, context, backend/model rules, and templates as needed.
6. Generate `spec.md`; wait for human review.
7. After confirmed `spec.md`, generate `design.md`; wait for human review.
8. After confirmed `design.md`, generate `tasks.md`; wait for human review.
9. After confirmed `tasks.md`, implement code by tasks Phase and record Phase Review.
10. Automatically invoke `uaw-code-review` in `SDD_TASK_CODE_REVIEW` mode. Do not ask the user for Code Review input in SDD mode.
11. Apply Review-driven Auto-fix according to `code-review-findings.md`.
12. Automatically invoke `uaw-unit-test` in SDD mode after Auto-fix. Do not ask the user to repeat unit-test inputs when SDD context is available.
13. Generate Unit Test Summary.
14. Sync Process Status and Process Audit Trail.
15. Generate `archive.md`; wait for final human review.

## Stage Gates

- Do not generate `design.md` before `spec.md` is confirmed.
- Do not generate `tasks.md` before `design.md` is confirmed.
- Do not implement code before `tasks.md` is confirmed.
- Do not enter the next tasks Phase when the current Phase Review is rejected.
- Do not archive before Code Review, Auto-fix, Unit Test Summary, and final human review are complete.

## References

- `references/input-examples.md`: required human input examples.
- `references/sdd2-workflow.md`: SDD2.0 workflow, proposal assembly, and skill invocation contract.
- `references/process-control.md`: status, audit trail, review, validation, and archive gates.
- `references/templates/`: internal proposal/spec/design/tasks/archive templates.
- `references/context/`: routing index source material and UAW transaction dictionary.
- `references/rules/backend/`: backend implementation rules.
- `references/rules/model/`: BO/VO/DTO/Entity modeling rules.

SDD2.0 rules in this `SKILL.md` and `references/sdd2-workflow.md` override bundled SDD reference material when wording conflicts, especially any wording that says developers manually fill `proposal-input.md`.
