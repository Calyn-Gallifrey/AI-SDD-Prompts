# UAW-SDD 2.0 Control Contract

This file is the single source of truth for SDD2 stage state, approvals, invalidation, implementation scope, recovery, and Archive eligibility. The three Skills may summarize this contract, but must not redefine it.

## 1. Stable User Entry

The public entry remains unchanged:

```text
developer brief prompt + invoke uaw-sdd-ai-coding
```

The developer does not run control commands or maintain control files. `uaw-sdd-ai-coding` runs `scripts/sdd2_control.py` internally. A future change to the public entry requires explicit user approval before implementation.

## 2. Authorities And Precedence

1. `SKILL.md` defines user intent routing and the unchanged entry.
2. This file defines process semantics.
3. `scripts/sdd2_control.py` deterministically enforces this contract.
4. JSON Schemas under `references/schemas/` define persisted record shapes.
5. Stage templates define human-readable artifact content.
6. Engineering rules define production implementation constraints.
7. Examples are non-authoritative and never constitute approval or requirements.

If a lower item conflicts with a higher item, stop as `blocked`, report the conflict, and do not guess.

## 3. Feature Assets And Control Files

The nine public assets remain fixed:

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

Internal control data is stored under the same feature directory:

```text
.sdd2/feature-state.json
.sdd2/gate-approvals.jsonl
.sdd2/events.jsonl
.sdd2/implementation-scope.json
.sdd2/archive-evidence.json
.sdd2/revisions/<artifact-stage>/r<revision>-<sha256>.md
```

`feature-state.json` is the current-state authority. Markdown status blocks are readable projections only. Approval and event JSONL records are append-only SHA-256 hash chains. Each active artifact revision is copied to an immutable content-addressed snapshot. An artifact approval is valid only for the recorded attempt, artifact revision, and artifact SHA-256.

## 4. Canonical State

Stages, in order:

```text
brief-design
proposal-input
spec
design
tasks
implementation
code-review
auto-fix
unit-test-summary
archive
```

Stage statuses:

```text
ready
executing
recorded
awaiting-approval
awaiting-final-approval
blocked
completed
closed-with-risk
aborted
superseded
```

Only `completed`, `closed-with-risk`, `aborted`, and `superseded` are terminal. `closed-with-risk` and `aborted` are not successful delivery.

Every active state records the feature/worktree binding, attempt, revision, current stage, status, next required action, artifacts, approvals, phase reviews, quality gates, invalidations, and any blocked recovery condition.

## 5. Initialization And Worktree Isolation

After persisting `brief-design.md`, initialize control state:

```bash
python3 scripts/sdd2_control.py init \
  --feature-dir <feature-dir> \
  --feature-id <stable-feature-id> \
  --mode real
```

One Git worktree may have only one active SDD2 feature. Parallel features require separate Git worktrees. Before implementation, capture a clean Git baseline and approved paths. Pre-existing changed files, forbidden paths, out-of-scope paths, detached HEAD, branch drift, missing lock, or an overly broad path pattern block execution.

## 6. Artifact Recording And Human Gates

After creating or changing a public artifact, call `record-artifact`. This increments its revision, stores its SHA-256, and invalidates affected downstream approvals and quality gates.

Human approval is required for `spec`, `design`, `tasks`, `unit-test-summary`, and `archive`. A valid approval:

1. comes from a new user message after the current gate is reached;
2. explicitly identifies the stage and approval result;
3. is recorded with `source=user-message`, a human/user role, message ID when available, artifact revision, and artifact hash;
4. is never inferred from `continue`, `next`, `ok`, files, examples, old messages, generated review text, or model self-review.

`AI-as-human-reviewer` is invalid in real mode. In demo mode it is valid only after a separate current user message explicitly authorizes a demo/simulation and that authorization is persisted first.

At a human gate, stop after recording the artifact. Do not generate the next artifact, edit production/test code, invoke the next Skill, or claim progress beyond the gate.

## 7. Exact Execution Flow

1. Persist Brief Design and initialize state.
2. Generate and record `proposal-input.md`.
3. Generate and record `spec.md`; stop; record explicit Spec approval.
4. Generate and record `design.md`; stop; record explicit Design approval.
5. Generate and record `tasks.md`; stop; record explicit Tasks approval.
6. Capture implementation scope with base commit, branch, allowed/forbidden paths, required phases, and test path patterns.
7. Implement one approved phase; stop; record explicit Phase Review before the next phase.
8. Freeze the implementation snapshot. Any later production code, test code, configuration, Spec, Design, or Tasks change invalidates affected downstream results.
9. Invoke `uaw-code-review` in `SDD_TASK_CODE_REVIEW` mode; record findings and the Code Review gate against the frozen snapshot.
10. Produce `auto-fix-summary.md`. If fixes change the snapshot, freeze again and rerun full Code Review. Record Auto-fix as `passed` or `not-required` only after Code Review passes on the same snapshot.
11. Invoke `uaw-unit-test` in SDD mode. Production changes require at least one generated or updated test source matching the captured test paths. If test code changes the snapshot, freeze again, rerun Code Review, and close Auto-fix again before recording Unit Test.
12. Record `unit-test-summary.md` and Unit Test evidence; stop; record explicit Unit Test Summary approval.
13. Prepare immutable Archive evidence from Git base/head/tree, frozen scope hash, and per-file hashes.
14. Generate and record `archive.md`; run Archive check; stop; record final Archive approval.
15. Only final Archive approval sets `completed` and releases the worktree lock.

## 8. Quality Gate Results

Code Review accepts `passed`, `failed`, or `blocked`. Auto-fix accepts `passed`, `not-required`, `failed`, or `blocked`. Unit Test accepts `passed`, `failed`, `blocked`, or `not-run`.

Archive requires all of the following on the same current snapshot:

- current Spec, Design, Tasks, and Unit Test Summary approvals;
- all required Phase Reviews approved;
- Code Review `passed`;
- Auto-fix `passed` or `not-required`;
- Unit Test `passed`;
- all nine public artifacts recorded and unchanged;
- current immutable Archive evidence;
- no blocked condition, scope drift, hash-chain corruption, branch mismatch, or lock mismatch.

Failed, blocked, or not-run tests can never be archived as successful delivery. With explicit human risk acceptance, use `closed-with-risk`; with explicit termination, use `aborted`.

## 9. Invalidation Matrix

| Change | Invalidates |
|---|---|
| Brief/proposal/spec | all later approvals, phase reviews, and quality gates |
| Design | Design/Tasks and all later records |
| Tasks | Tasks approval, phase reviews, scope, and all quality gates |
| Production/test/config snapshot | Code Review, Auto-fix, Unit Test, Unit Test Summary approval, Archive evidence |
| Findings | Code Review and later gates |
| Auto-fix Summary | Auto-fix and later gates |
| Unit Test Summary | its approval and Archive |
| Archive | final Archive approval only |

An invalidated result remains in history but cannot authorize progress.

## 10. Recovery, Resume, And Repetition

`resume` validates hashes, artifacts, lock, branch, and scope, then returns exactly one `next_required_action`. Never reconstruct state from chat memory or Markdown prose when control state exists.

For a recoverable blocked stage, fix the recorded cause and rerun the same required action. For a new execution after a blocked or terminal attempt, `restart-attempt` requires a new explicit user retry/restart message, increments the attempt, invalidates prior approvals, clears quality results and scope, and restarts at the earliest persisted stage requiring fresh approval.

Historical feature examples are migrated as `historical-example` and `superseded`. Their old approvals are not backfilled or accepted. They are reference-only and cannot resume.

## 11. Failure Rule

Any control command returning non-zero is a hard stop. Record the error as the blocking reason, do not work around it manually, and do not proceed until the state is valid or the user explicitly closes/restarts the attempt.
