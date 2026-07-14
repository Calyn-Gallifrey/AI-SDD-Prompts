# Method Unit-Test Rule

Use for a focused public/package-visible method, domain helper, mapper helper, or small collaborator whose behavior can be exercised without a Spring context.

## Required Analysis

1. Read the method and all branches, validation, defaults, exceptions, and side effects.
2. Identify observable contract from approved Spec/current callers; do not test private implementation details directly.
3. Partition inputs into valid, boundary, null/empty, invalid, and regression cases that actually apply.
4. Identify collaborators. Mock only external boundaries; use real value objects where practical.

## Test Design

| Concern | Required approach |
|---|---|
| Happy path | assert complete meaningful result, not only non-null |
| Boundary | minimum/maximum, empty, nullability, precision, ordering as applicable |
| Invalid input | assert exact exception type and important message/code when contractual |
| Branches | one case per materially different outcome |
| Side effects | verify arguments and count; assert no interaction on rejected paths |
| Regression | reproduce the changed/previously failing behavior |

Use parameterized tests when multiple cases share the same contract and improve readability. Avoid loops with opaque assertions.

## Assertions

- Assert domain fields/collections and ordering that callers depend on.
- For exceptions, use the selected framework's supported assertion mechanism.
- Use argument captors only when the collaborator input is part of behavior.
- Do not assert incidental local variable choices, exact internal call order, or logging unless they are contractual.

## Constraints

- Do not expose a private method solely for testing; exercise it through an observable owner unless Design explicitly changes the API.
- Do not start Spring for pure method behavior.
- Do not import UAW utilities unless target code and current dependencies use them.
- Keep test data minimal and named for the scenario.

## Completion Evidence

Record target symbol, changed test path, scenario mapping, selected framework profile, command/entry, and observed result in Unit Test Summary.
