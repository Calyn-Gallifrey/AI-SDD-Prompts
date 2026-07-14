# Static Method Unit-Test Rule

Use for deterministic static utilities or code that must call a static boundary already present in the approved design.

## Pure Static Utility

Call the public static method directly. Cover valid, boundary, null/empty, invalid, and regression inputs that apply. Assert complete outputs and exception contracts. No mocking is needed for deterministic pure functions.

## Static Dependency

Prefer testing through the owning public behavior. Use scoped static mocking only when:

- current dependencies already support it;
- refactoring the static boundary is outside approved scope;
- the static call is a real external/non-deterministic boundary;
- the mock is closed deterministically in the test scope.

Do not add Mockito-inline or another engine solely for convenience without approved Design/Tasks and a new scope review.

## Required Checks

- static state does not leak between tests;
- locale/timezone/clock/random inputs are controlled when behavior depends on them;
- concurrency assumptions are identified for mutable static state;
- exceptions and fallback values are asserted;
- interactions are verified only when observable behavior depends on them.

## Anti-Patterns

- mocking the static method under test;
- leaving a static mock open across tests;
- relying on test execution order;
- changing global process state without restoration;
- asserting internal helper calls instead of output.

Record selected profile/modifier, static-mocking capability evidence, changed test file, execution command, and observed result.
