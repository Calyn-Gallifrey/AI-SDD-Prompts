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

## Hard Gate Protocol

The hard gate protocol is an execution blocker. It takes precedence over the workflow list, templates, examples, and any model-generated plan.

When a hard gate is reached, the assistant must stop after producing the current allowed artifact and must not generate downstream artifacts, edit code, run code implementation, invoke downstream skills, or create archive content until a valid human approval is received.

Valid human approval must be a new user message after the gate is reached, explicitly approving the current stage. Existing files, prior demo records, historical approvals, generated Review Record sections, inferred approval, or model self-review are not valid approval sources.

In real SDD execution, the assistant must not approve on behalf of the human reviewer. `AI-as-human-reviewer` is allowed only when the user explicitly asks to run a demo, validation drill, or simulation where AI must play the reviewer role.

Hard gates:

- After generating `spec.md`, stop and wait for explicit human spec approval. Do not generate `design.md`.
- After generating `design.md`, stop and wait for explicit human design approval. Do not generate `tasks.md`.
- After generating `tasks.md`, stop and wait for explicit human tasks approval. Do not edit or generate implementation code.
- After each tasks Phase implementation, stop and wait for explicit Phase Review approval. Do not continue to the next Phase.
- After implementation is complete, run only the required SDD Code Review sequence. Do not skip `code-review-findings.md`.
- After Code Review, complete required Auto-fix before Unit Test. Do not skip Review-driven Auto-fix when findings require it.
- After Unit Test Summary is generated, stop and wait for explicit Unit Test Summary approval before Archive.
- After `archive.md` is generated, stop and wait for final human archive approval.

Ambiguous user replies such as "continue", "next", "ok", or "go on" are not valid approvals unless they clearly name the current stage and approve it. If approval is ambiguous, ask for stage-specific approval and do not proceed.

If downstream content or code is generated before the required approval, stop immediately, report the gate violation, and wait for user direction. Do not continue from the invalid state silently.

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
12. Invoke `uaw-unit-test` in SDD mode after Auto-fix. SDD context must provide unit-test inputs from the approved SDD assets, implementation diff, Code Review Findings, and Auto-fix Summary.
13. Invoke `uaw-unit-test` to generate or update unit test code, then generate Unit Test Summary using `skills/uaw-unit-test/references/templates/unit-test-summary-template.md`.
14. Sync Process Status and Process Audit Trail.
15. Generate `archive.md`; wait for final human review.

## Stage Gates

- `design.md` is generated only after `spec.md` is confirmed.
- `tasks.md` is generated only after `design.md` is confirmed.
- Code implementation starts only after `tasks.md` is confirmed.
- The next tasks Phase starts only after the current Phase Review is approved.
- Archive starts only after Code Review, Auto-fix, unit test code generation, Unit Test Summary, and explicit Unit Test Summary approval are complete.
- The flow is not complete until `archive.md` is generated and explicitly approved by the final human archive review.

## References

- `references/input-examples.md`: required human input structure templates.
- `references/sdd2-workflow.md`: SDD2.0 workflow, proposal assembly, and skill invocation contract.
- `references/process-control.md`: status, audit trail, review, validation, and archive gates.
- `references/templates/`: internal proposal/spec/design/tasks/archive templates.
- `references/context/`: routing index source material and UAW transaction dictionary.
- `references/rules/backend/`: backend implementation rules.
- `references/rules/model/`: BO/VO/DTO/Entity modeling rules.

When bundled SDD reference wording conflicts with this SDD2.0 skill contract, this file and `references/sdd2-workflow.md` take precedence. In SDD2.0, developers provide `Brief Design（人工简要设计）`; `proposal-input.md` is assembled internally.
