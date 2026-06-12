---
name: uaw-sdd-ai-coding
description: Run the UAW SDD2.0 AI coding workflow for backend feature delivery. Use when the user provides a human brief design, asks to start SDD, generate proposal/spec/design/tasks/archive, implement code under SDD gates, or continue a UAW SDD feature flow. This skill assembles proposal-input.md internally, enforces human review gates, and automatically invokes UAW code review and unit test skills after tasks implementation.
---

# UAW SDD AI Coding

## Core Contract

This skill runs the SDD2.0 backend feature delivery workflow from `Brief Design（人工简要设计）` to `archive.md`.

`Brief Design（人工简要设计）` is the user-facing entry. `proposal-input.md` is an internal SDD asset assembled by the skill after required brief fields are available.

Read `references/input-examples.md` before requesting human input. The file defines input structure templates for brief design and review input.

Input templates are not business requirements. Placeholder text, template field descriptions, and illustrative wording must not be copied into `brief-design.md`, `proposal-input.md`, feature directory names, API paths, field names, business logic, code, tests, or archive assets unless the user explicitly provides the same content as part of the real requirement.

## Required Brief Fields

Required fields in `Brief Design（人工简要设计）`:

- `Feature Name（功能名称）`
- `Feature Type（功能类型）`: `query`, `submit`, `edit`, `enhancement`, `refactor`, or `fix`
- `Module（所属模块）`
- `Sprint（迭代）`
- `Priority（优先级）`: `P0`, `P1`, or `P2`
- `Goal（一句话目标）`
- `Change Scope（变更范围）`
- `Forbidden Changes（禁止变更）`

If a required field is missing, request only the missing field by using the missing-field example in `references/input-examples.md`. Required fields must come from confirmed user input.

## Generalization Rules

- Feature assets must be named from the confirmed `Feature Name（功能名称）` in the current Brief Design only.
- For enhancements to existing functionality, identify the existing API, class, method, response model, mapper, or logic first, then keep the SDD scope to the confirmed delta.
- If the requirement is limited to adding one response field to an existing query, the SDD scope must not expand into a new work order, new submit flow, new table, or unrelated module unless explicitly confirmed.
- Template placeholders and historical examples are reference material only; they are never fallback values for missing requirement information.

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
10. Invoke `uaw-code-review` in `SDD_TASK_CODE_REVIEW` mode. SDD context provides Code Review inputs.
11. Apply Review-driven Auto-fix according to `code-review-findings.md`.
12. Invoke `uaw-unit-test` in SDD mode after Auto-fix. SDD context provides unit-test inputs when available.
13. Generate Unit Test Summary using `skills/uaw-unit-test/references/templates/unit-test-summary-template.md`.
14. Sync Process Status and Process Audit Trail.
15. Generate `archive.md`; wait for final human review.

## Stage Gates

- `design.md` is generated only after `spec.md` is confirmed.
- `tasks.md` is generated only after `design.md` is confirmed.
- Code implementation starts only after `tasks.md` is confirmed.
- The next tasks Phase starts only after the current Phase Review is approved.
- Archive starts only after Code Review, Auto-fix, Unit Test Summary, and final human review are complete.

## References

- `references/input-examples.md`: required human input structure templates.
- `references/sdd2-workflow.md`: SDD2.0 workflow, proposal assembly, and skill invocation contract.
- `references/process-control.md`: status, audit trail, review, validation, and archive gates.
- `references/templates/`: internal proposal/spec/design/tasks/archive templates.
- `references/context/`: routing index source material and UAW transaction dictionary.
- `references/rules/backend/`: backend implementation rules.
- `references/rules/model/`: BO/VO/DTO/Entity modeling rules.

When bundled SDD reference wording conflicts with this SDD2.0 skill contract, this file and `references/sdd2-workflow.md` take precedence. In SDD2.0, developers provide `Brief Design（人工简要设计）`; `proposal-input.md` is assembled internally.
