# SDD2.0 Artifact And Handoff Workflow

`sdd2-control-contract.md` owns all state, approval, invalidation, recovery, and Archive semantics. This file defines only artifact responsibilities and Skill handoffs.

## Entry And Workspace

The developer supplies a short Brief Design and invokes `uaw-sdd-ai-coding`. The Skill persists the Brief and performs all internal control operations. No new developer command or form is introduced.

Feature directory:

```text
sdd2-features/<SprintN>/<feature-name>/
```

`<feature-name>` comes only from the current confirmed Brief. Keep all SDD2 minor revisions under `sdd2-features`; a new root requires an explicit major-version migration decision.

## Artifact Map

| Artifact | Purpose | Input | Output / Consumer | Completion Condition |
|---|---|---|---|---|
| `brief-design.md` | Persist current human brief | Current user message | Proposal assembly | All required fields confirmed |
| `proposal-input.md` | Normalize internal planning input | Brief + targeted code/context discovery | Spec generation | Source facts and open questions identified |
| `spec.md` | Define behavior and acceptance | Proposal + current behavior | Human Spec review, Design | Recorded and explicitly approved |
| `design.md` | Define technical delta and constraints | Approved Spec + current code + routed rules | Human Design review, Tasks | Recorded and explicitly approved |
| `tasks.md` | Define bounded phases and files | Approved Design | Human Tasks review, implementation scope | Recorded and explicitly approved |
| `code-review-findings.md` | Immutable first-pass review findings | Frozen scope + approved SDD assets | Auto-fix | Gate recorded for same scope |
| `auto-fix-summary.md` | Map each finding to fix/disposition | Findings + code changes | Re-review, Unit Test | Gate closed on same reviewed scope |
| `unit-test-summary.md` | Record test-source changes and results | Reviewed scope + test execution | Human Unit Test Summary review | Unit Test passed and summary approved |
| `archive.md` | Final traceable delivery record | All current artifacts + Archive evidence | Final human review | Archive check passes and final approval recorded |

`proposal-input.md` is internal. Reference examples and templates are not business requirements.

## Proposal Mapping

| Brief field | Proposal field |
|---|---|
| Feature Name | 功能名称 |
| Feature Type | 功能类型 |
| Module | 所属模块 |
| Goal | 一句话目标 |
| Change Scope | 变更范围 |
| Forbidden Changes | 禁止变更 |
| Priority | 优先级 |
| Sprint | sprint |
| Open Questions | 风险提醒 / 待确认 |

For `enhancement`, `refactor`, and `fix`, inspect current code first and describe only the confirmed delta. Prior Feature assets may be used only when explicitly named or when current code cannot establish behavior; label them as historical context.

## Handoff Sequence

```text
Brief -> Proposal -> Spec approval -> Design approval -> Tasks approval
-> phased implementation + Phase Reviews
-> uaw-code-review / SDD_TASK_CODE_REVIEW
-> Auto-fix + full re-review when scope changes
-> uaw-unit-test / SDD mode
-> Unit Test Summary approval
-> Archive evidence -> Archive approval -> completed
```

### Code Review Handoff

Provide:

- feature directory and state path;
- approved Spec, Design, and Tasks revisions/hashes;
- Git repository, branch, base commit, frozen snapshot hash, exact changed-file manifest;
- Code Review output path.

The Code Review Skill must use this fixed scope. It must not infer scope from `git status`, upstream drift, or the feature asset directory alone.

### Unit Test Handoff

Provide:

- the same current frozen scope;
- Design test strategy and Tasks test phase;
- immutable Code Review findings and Auto-fix summary;
- detected project test stack and routed testing profile;
- target test source paths and required execution evidence.

The Unit Test Skill generates or updates test code before the summary. If target code, framework, or executable test entry cannot be established, record `blocked`; do not substitute prose or manual checks for unit-test source.

## Change Handling

A user requirement change is not an informal edit. Update the earliest affected artifact, record it, allow deterministic invalidation, and repeat every downstream approval/gate that became stale. If the request identifies a different feature, create a separate feature/worktree rather than retargeting active state.

## Non-Goals

Fast Lane, mini-spec, mini-tasks, archive-lite, and alternate public entry modes are outside SDD2.0. They require a separately approved process version.
