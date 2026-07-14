# ServiceStrategy Unit-Test Rule

Use for strategy implementations, selectors, chains, or routers where behavior depends on applicability, priority, or strategy-specific execution.

## Strategy Implementation

Test:

1. applicability predicate for matching, non-matching, null/invalid, and boundary inputs;
2. successful strategy behavior and collaborator mapping;
3. dependency empty/error behavior;
4. side effects and no-interaction rejection paths;
5. regression cases tied to the changed strategy.

## Selector Or Chain

Test:

- exactly one expected strategy is selected for each supported category;
- no-match behavior is explicit;
- overlapping matches follow approved priority or fail explicitly;
- ordering is deterministic when order matters;
- disabled/unsupported strategies do not execute;
- selected-strategy exceptions propagate/map as designed.

Use real lightweight strategy instances when practical. Mock strategies when verifying selection/dispatch independent of their internal logic.

## Data Matrix

Create a scenario matrix from approved business categories rather than one test per incidental enum value:

| Input category | Expected applicable strategies | Selected strategy | Expected outcome |
|---|---|---|---|
|  |  |  |  |

Every supported category, gap, and intentional overlap must be represented.

## Constraints

- Do not duplicate selection logic in test helpers.
- Do not rely on unordered collection iteration.
- Do not mock the selector under test.
- Do not load Spring only to obtain a list that can be constructed directly, unless container ordering/qualifiers are the behavior under test.

Record strategy matrix coverage, changed test path/hash, profile, exact execution entry, result counts, and scope SHA-256.
