---
name: uaw-sdd-ai-coding
description: Run the UAW SDD2.0 backend feature workflow from a short developer brief through gated Spec, Design, Tasks, implementation, Code Review, Auto-fix, Unit Test, and Archive. Use when the user asks to start, continue, resume, or close an SDD2 feature. The public entry remains a brief prompt plus this Skill invocation; all deterministic control is internal.
---

# UAW SDD2 AI Coding

## Entry Contract

Keep the existing developer experience:

```text
short brief prompt + invoke this Skill
```

Do not ask the developer to run control scripts, create control files, provide Git hashes, or use a new command syntax. Run all controls internally. Do not change this entry without explicit user approval.

`Brief Design（人工简要设计）` is the user-facing input. Persist confirmed content in `brief-design.md`; assemble `proposal-input.md` internally.

Read `references/input-examples.md` before requesting missing fields. Templates and historical features are examples only, never requirements or approvals.

## Required Brief Fields

- `Feature Name（功能名称）`
- `Feature Type（功能类型）`: `query`, `submit`, `edit`, `enhancement`, `refactor`, or `fix`
- `Module（所属模块）`
- `Sprint（迭代）`
- `Priority（优先级）`: `P0`, `P1`, or `P2`
- `Goal（一句话目标）`
- `Change Scope（变更范围）`
- `Forbidden Changes（禁止变更）`

Ask only for fields that cannot be safely derived from confirmed current input or current code. Never fill missing business facts from templates or old examples.

## Mandatory Startup

1. Resolve one feature directory at `sdd2-features/<SprintN>/<feature-name>/` from the current confirmed Brief only.
2. Persist `brief-design.md`.
3. Read `references/sdd2-control-contract.md`, `references/sdd2-workflow.md`, and `references/context/routing-index.md`.
4. Initialize or resume deterministic state:

```bash
python3 scripts/sdd2_control.py init --feature-dir <dir> --feature-id <id> --mode real
python3 scripts/sdd2_control.py resume --feature-dir <dir>
```

Use `init` only when `.sdd2/feature-state.json` does not exist. A non-zero control result is a hard stop.

## Execution Rules

Follow `references/sdd2-control-contract.md` exactly. It is the single source of truth for stage order, statuses, approvals, invalidation, scope, retry, recovery, and Archive eligibility.

After every public asset creation or change, run:

```bash
python3 scripts/sdd2_control.py record-artifact --feature-dir <dir> --stage <stage>
```

At Spec, Design, Tasks, Unit Test Summary, and Archive gates, stop. Only a new user message explicitly approving that current stage may be persisted with `approve`. Ambiguous continuation text, old messages, files, examples, generated review records, and model self-review are invalid.

Implementation begins only after current Tasks approval. Internally capture a clean Git baseline, approved/forbidden path patterns, required phases, and test paths. One worktree supports one active feature. Freeze the exact implementation snapshot before Code Review.

After each implemented Phase, stop for current human Phase Review. Phase Review does not replace SDD Code Review.

After implementation:

1. Invoke `uaw-code-review` in `SDD_TASK_CODE_REVIEW` mode.
2. Persist `code-review-findings.md` and record its gate against the frozen snapshot.
3. Persist `auto-fix-summary.md`. Any code/test/config change requires a new freeze and full Code Review.
4. Invoke `uaw-unit-test` in SDD mode only after Code Review passes and Auto-fix closes on the same snapshot.
5. Production changes require generated or updated unit-test source. Persist and record `unit-test-summary.md` with reproducible command/environment/result evidence.
6. Stop for Unit Test Summary approval.
7. Prepare immutable Archive evidence, generate `archive.md`, run Archive check, and stop for final Archive approval.

Only final Archive approval marks the feature `completed`. Failed/blocked/not-run tests cannot be completed; use explicit `closed-with-risk` or `aborted` instead.

## Resumption And Violations

Always call `resume`; follow its single `next_required_action`. Do not reconstruct progress from chat or Markdown when control state exists.

If a required approval, artifact, lock, scope, hash, phase review, or quality result is missing or stale, set/keep the feature blocked and stop. If content or code was created beyond a gate, report the violation; do not silently accept the downstream work.

An explicit user retry/restart after a blocked or terminal attempt is handled internally with `restart-attempt`; prior approvals never transfer to the new attempt.

## References

- `references/sdd2-control-contract.md`: authoritative process and recovery contract.
- `references/sdd2-workflow.md`: artifact responsibilities and execution handoffs.
- `references/process-control.md`: operator command mapping and failure handling.
- `references/context/routing-index.md`: deterministic context/rule routing.
- `references/templates/`: nine public artifact templates and Auto-fix template.
- `references/rules/`: backend and model implementation constraints.
- `scripts/sdd2_control.py`: deterministic enforcement; never exposed as a developer entry.
