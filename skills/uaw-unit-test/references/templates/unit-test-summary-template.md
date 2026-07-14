# Unit Test Summary

> Audit record created after unit-test source generation/update. In SDD mode, it must bind to the same frozen scope as passed Code Review and closed Auto-fix.

## 1. Identity And Scope

- Feature ID / standalone task ID:
- Mode: SDD / standalone
- Attempt:
- Scope SHA-256:
- Base Commit:
- Head Commit / Tree:
- Code Revision:
- Summary Revision / SHA-256:

## 2. Profile Evidence

- Primary Profile: JUNIT5_MOCKITO / JUNIT4_MOCKITO / EXISTING_CUSTOM / BLOCKED_UNKNOWN
- Modifiers:
- Target Rule:
- Build/module evidence:
- JUnit/Mockito/assertion evidence:
- Nearby test convention evidence:
- Selection rationale:
- Dependency changes: none / exact approved change

## 3. Test Source Changes

| Test file | SHA-256 | Added/updated | Production target | Requirements/findings covered |
|---|---|---|---|---|
|  |  |  |  |  |

A passed SDD result requires at least one current changed test source matching captured test paths.

## 4. Scenario Coverage

| Test method / parameter set | Scenario type | Given | Expected assertions/interactions | Requirement / finding |
|---|---|---|---|---|
|  | happy / boundary / error / regression |  |  |  |

## 5. Execution Evidence

- Validation Method: Wrapper / Local CLI / IDE / CI / Script
- Execution Environment:
- JDK:
- Exact Test Entry / Command / Job / Configuration:
- Started/Finished At:
- Exit Code / Observed Result:
- Tests Run:
- Passed:
- Failed:
- Errors:
- Skipped:
- Relevant output/evidence location:
- Warnings:

Do not record `passed` without observed execution evidence. Manual validation belongs in supplemental evidence and cannot pass this gate.

## 6. Failure Or Block Detail

| Failure/block | Test/symbol | Root cause evidence | Production defect vs test defect vs environment | Recovery |
|---|---|---|---|---|
|  |  |  |  |  |

## 7. Review And Auto-fix Binding

- Code Review Findings SHA-256:
- Code Review Result / Scope SHA-256: passed /
- Auto-fix Summary SHA-256:
- Auto-fix Result / Scope SHA-256: passed or not-required /
- Post-test-source full re-review completed: yes / no

## 8. Remaining Test Risk

| Risk | Reason | Impact | Blocking | Follow-up |
|---|---|---|---|---|
|  |  |  | yes / no |  |

## 9. Gate Conclusion

- Unit Test Result: passed / failed / blocked / not-run
- Archive Eligible From Unit Test: yes only when passed; otherwise no
- Evidence Summary:

## 10. Human Summary Gate (SDD Only)

- State Authority: `./.sdd2/feature-state.json`
- Current Stage: unit-test-summary
- Stage Status: awaiting-approval
- Next Required Action: request-unit-test-summary-approval
- Approval Evidence Destination: `./.sdd2/gate-approvals.jsonl`

Stop after recording this summary and deterministic Unit Test result. Archive preparation requires a new explicit human approval of this current summary revision.
