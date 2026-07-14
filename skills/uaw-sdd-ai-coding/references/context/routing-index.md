# UAW-SDD 2.0 Runtime Routing Index

This index routes current SDD2 execution. `original/` is migration provenance only and must not be loaded as runtime instruction. See `source-provenance.json`.

## 1. Always Load

```text
skills/uaw-sdd-ai-coding/SKILL.md
skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md
skills/uaw-sdd-ai-coding/references/sdd2-workflow.md
skills/uaw-sdd-ai-coding/references/process-control.md
skills/uaw-sdd-ai-coding/references/context/routing-index.md
```

Load `input-examples.md` before requesting missing Brief fields. Examples remain non-authoritative.

## 2. Runtime Assets

Public feature assets:

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

Internal control assets:

```text
.sdd2/feature-state.json
.sdd2/gate-approvals.jsonl
.sdd2/events.jsonl
.sdd2/implementation-scope.json
.sdd2/archive-evidence.json
.sdd2/revisions/<artifact-stage>/r<revision>-<sha256>.md
```

The public entry remains a brief prompt plus Skill invocation. Internal control assets require no developer action.

## 3. Template Routing

| Artifact | Template |
|---|---|
| Proposal | `references/templates/proposal-input-internal-template.md` |
| Spec | `references/templates/spec-template.md` |
| Design | `references/templates/design-template.md` |
| Tasks | `references/templates/tasks-template.md` |
| Auto-fix | `references/templates/auto-fix-summary-template.md` |
| Archive | `references/templates/archive-template.md` |
| Code Review Findings | `skills/uaw-code-review/references/templates/sdd-code-review-findings-template.md` |
| Unit Test Summary | `skills/uaw-unit-test/references/templates/unit-test-summary-template.md` |

## 4. Backend Rule Routing

Load only rules whose trigger is confirmed by Brief/approved Design/current code.

| Trigger | Runtime rule |
|---|---|
| HTTP/API entry or response contract | `references/rules/backend/backend-api.md` |
| New/changed database table or deployment DDL | `references/rules/backend/create-table.md` |
| MyBatis mapper/query/mapping | `references/rules/backend/mybatis-orm.md` |
| Current authenticated user | `references/rules/backend/current-user.md` |
| EPI integration | `references/rules/backend/epi-gateway.md` |
| OM external API anti-corruption layer | `references/rules/backend/om-api-acl.md` |
| MapStruct conversion | `references/rules/backend/mapstruct-conversion.md` |
| Transaction module package/layout | `references/rules/backend/transaction-package-structure.md` |
| New transaction type affecting Case Tracker | `references/rules/backend/case-tracker-compatibility.md` |

If a trigger is ambiguous or the required external/database contract cannot be established, record an open question and block Design/implementation as appropriate. Never fill the gap from a code example.

## 5. Model Rule Routing

| Boundary | Runtime rule |
|---|---|
| API/business input | `references/rules/model/bo.md` |
| Internal/inter-layer transfer | `references/rules/model/dto.md` |
| Persistence mapping | `references/rules/model/entity.md` |
| API/view output | `references/rules/model/vo.md` |

Current module conventions decide whether a new type is actually needed. Do not create parallel BO/DTO/VO/Entity models without an ownership/mapping need recorded in Design.

## 6. Test Rule Routing

Always load:

```text
skills/uaw-unit-test/SKILL.md
skills/uaw-unit-test/references/testing-profile-routing.md
```

Then load one primary target rule:

| Target | Runtime rule |
|---|---|
| Method/helper | `skills/uaw-unit-test/references/java/method-unit-test.md` |
| Service | `skills/uaw-unit-test/references/java/service-unit-test.md` |
| Static utility/dependency | `skills/uaw-unit-test/references/java/static-method-unit-test.md` |
| Controller | `skills/uaw-unit-test/references/java/controller-unit-test.md` |
| ServiceStrategy/selector | `skills/uaw-unit-test/references/java/service-strategy-unit-test.md` |

Use the SDD two-pass test handoff: generate test source, refreeze/re-review, then execute and summarize.

## 7. Code Review Routing

SDD invokes:

```text
uaw-code-review / SDD_TASK_CODE_REVIEW
```

Load only the Code Review Skill, current rules, and Markdown findings template. HTML templates are standalone-only and must not be loaded in SDD mode.

## 8. Business Context Routing

`transactions-dictionary.md` is a provenance-labeled historical snapshot. Load it only for a matching transaction-domain task. Treat names/packages/status/dropdowns as candidates that require confirmation from current code/config/schema or current user input before becoming requirements.

Record each context use in Proposal/Design with source path, source hash/version, verified-at time, confirming current source, and confidence. Unconfirmed dictionary status or enum values cannot authorize code/database changes.

## 9. Feature-Type Focus

| Type | Required focus |
|---|---|
| query | authorization, query bounds, cardinality, response compatibility, masking |
| submit | validation, transaction, idempotency, persistence, state transition |
| edit | target identity, authorization, audit, compatibility, partial failure |
| enhancement | current behavior/delta, compatibility, regression |
| refactor | behavior preservation, bounded scope, regression |
| fix | reproduction, root cause, minimal correction, regression |

Feature type does not auto-load a business rule. Confirm actual scope first.

## 10. Source Conflict Rule

For current implementation facts, use this precedence:

1. approved current user requirement;
2. current executable code/schema/config at captured Git state;
3. current SDD2 runtime rule;
4. provenance-labeled context snapshot;
5. example/template.

A conflict affecting behavior, scope, security, data, or acceptance blocks progression and must be resolved explicitly.
