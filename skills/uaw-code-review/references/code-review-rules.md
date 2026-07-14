# UAW Code Review Rules

## 1. Modes And Ownership

| Mode | Scope authority | Output | SDD gates | Fix code |
|---|---|---|---|---|
| `SDD_TASK_CODE_REVIEW` | current `.sdd2/implementation-scope.json.frozen_snapshot` | feature `code-review-findings.md` | validate current SDD state | no |
| `STANDALONE_GIT_RANGE_REVIEW` | frozen base/head commits and diff hash | HTML summary + developer reports | no | no |
| `STANDALONE_WORKTREE_SNAPSHOT_REVIEW` | frozen target/HEAD/file manifest hash | HTML summary + developer reports | no | no |

Select exactly one mode before reading implementation files. Never use a standalone report as SDD gate evidence. Never generate HTML in SDD mode.

## 2. SDD Mode Preconditions

Read the SDD2 control contract from `skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md`. Then run:

```bash
python3 skills/uaw-sdd-ai-coding/scripts/sdd2_control.py validate --feature-dir <feature-dir>
```

Review is blocked unless:

1. control validation succeeds;
2. Spec, Design, and Tasks approval records bind current revisions and hashes;
3. all phases declared in scope have current human Phase Review approvals;
4. the worktree lock, branch, base commit, and frozen snapshot are current;
5. all manifest paths are allowed and none are forbidden/out-of-scope;
6. `proposal-input.md`, `spec.md`, `design.md`, and `tasks.md` are readable;
7. the output is the current feature's `code-review-findings.md`.

Do not scan for literal unchecked boxes in Tasks. Tasks is an approved immutable plan; implementation completion is proven by Phase Review records and the frozen scope manifest.

If any precondition fails, write a blocked Findings artifact only when the output location is trustworthy; otherwise return the blocking error without writing elsewhere.

## 3. Deterministic SDD Scope

The only implementation files under review are `frozen_snapshot.files`. Record:

- feature ID and attempt;
- repository and branch;
- base commit, head commit, head tree;
- scope snapshot SHA-256;
- each path and SHA-256/deletion marker;
- current Spec/Design/Tasks revisions and hashes.

Verify every current file hash before reviewing. A hash mismatch is `blocked` and requires a new `freeze-scope`; it is not reviewed under the old scope.

Feature Markdown/control assets are context, not production implementation scope. Review those only for SDD consistency; do not count them as product code changes.

## 4. Standalone Git Range Scope

Required input: repository, base ref, target ref, output directory; developer attribution when individual reports are requested.

Before review:

1. resolve base and target to immutable commit IDs;
2. record branch/ref names only as labels;
3. capture the exact changed-file list and diff;
4. compute SHA-256 of the captured diff;
5. keep the scope fixed for the run.

If a date range is requested, resolve the included commits first and list them. Do not review commits appearing after capture. Merge semantics (`base..target` or merge-base comparison) must follow explicit user input; if absent, state and use merge-base comparison.

Uncommitted/untracked files are outside Git-range scope unless the user explicitly requests a second worktree-snapshot review.

## 5. Standalone Worktree Snapshot Scope

Required input: repository/target path and output directory.

Capture:

- repository HEAD commit/tree when available;
- exact target path;
- tracked changes, deletions, and untracked files under target;
- per-file content hashes and one canonical snapshot hash;
- capture time.

Label every report: `Scope Deviation: worktree snapshot, not Git range; not a formal merge gate.` A file change during review invalidates the snapshot and requires recapture.

## 6. Review Method

For each scoped file:

1. inspect the diff and enough surrounding current code to understand behavior;
2. trace affected callers, callees, contracts, persistence, and configuration;
3. compare against approved SDD behavior in SDD mode, or user-stated intent in standalone mode;
4. apply routed UAW rules only when their trigger conditions match;
5. verify tests cover changed behavior and failure boundaries;
6. record concrete evidence with path, symbol, and diff location.

Do not redesign requirements, expand scope, invent project conventions, or report generic style preferences without a demonstrated consequence.

## 7. Mandatory Review Categories

| Category | Required checks |
|---|---|
| Scope/traceability | every changed file authorized; every approved requirement mapped; no hidden behavior |
| Correctness | branch logic, null/empty handling, boundary values, state transitions, failure behavior |
| Compatibility | API/model/schema/config compatibility, defaults, migration and rollback |
| Security | authorization, input validation, sensitive data, injection, unsafe logging |
| Transactions/concurrency | atomicity, rollback, retries, locks, idempotency, race conditions |
| Integration | gateway/ACL mapping, timeout/error translation, contract drift |
| Persistence | query correctness, cardinality, indexes, ORM mappings, data integrity |
| Maintainability | ownership, duplication with real risk, naming consistency, unreachable/dead code |
| Observability | actionable logs/metrics/audit without leaking data |
| Tests | changed test source, happy/boundary/error/regression cases, meaningful assertions/mocks |

Each category receives `checked-pass`, `checked-finding`, or `blocked`, plus evidence. No category may remain blank or pending when the conclusion is recorded.

## 8. Severity

- `P0`: likely security/data-loss/availability incident, irreversible corruption, gate bypass, or code that cannot safely run/merge.
- `P1`: real functional defect, contract violation, serious regression, transaction/concurrency flaw, or missing test that leaves a high-risk change unverified.
- `P2`: bounded maintainability, clarity, or lower-risk correctness concern with a concrete impact.

Mark a P2 `blocking=true` only when its actual context prevents safe progression. Do not inflate severity because a rule wording uses “must”; assess consequence.

## 9. Conclusions

- `passed`: no P0, P1, or blocking P2; all categories checked with evidence.
- `failed`: at least one actionable P0/P1/blocking P2 on the current scope.
- `blocked`: scope/input/hash/context is missing, stale, or unverifiable.

In SDD mode, Code Review never grants Archive. It only authorizes the Auto-fix step. Unit Test and later approvals remain mandatory.

## 10. SDD Findings Rules

Use `templates/sdd-code-review-findings-template.md`.

1. Findings are immutable first-pass evidence after recording. Do not edit them to mark fixes complete.
2. Assign stable IDs `CR-001`, `CR-002`, and so on.
3. Every finding includes severity, blocking flag, exact path/symbol/location, violated SDD/rule evidence, consequence, and actionable fix.
4. Include all scoped files, all mandatory category results, and the exact frozen IDs/hashes.
5. Set `Unit tests required: yes` for production changes.
6. Return to `uaw-sdd-ai-coding`; fixes and dispositions are recorded only in `auto-fix-summary.md`.

## 11. Standalone Report Rules

Generate `代码评审统计报告.html` and one `{开发者姓名}_代码评审报告.html` per attributable developer. If attribution cannot be established, generate a clearly labeled unassigned report rather than guessing.

Reports include captured immutable scope, review method, findings, severity counts, tested/untested risk, and limitations. HTML must be self-contained and open locally. Code changes require a separate explicit request.

## 12. Failure Handling

- Git command/range failure: `blocked`; report exact command and error.
- Binary/generated/large file: record limitation and inspect the authoritative source when available; do not silently omit.
- Rule conflict: cite both sources and block when the conflict affects safety/correctness.
- Scope changes mid-review: discard the stale conclusion, recapture, and rerun.
- No findings: explicitly state no actionable findings and list remaining verification gaps; do not manufacture issues.
