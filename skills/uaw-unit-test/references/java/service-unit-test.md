# Service Unit-Test Rule

Use for application/domain services and orchestration components. Default to a real service instance with mocked external collaborators; do not load Spring unless current architecture makes a pure unit test impossible and an approved Spring profile exists.

## Fixture

- Select JUnit/Mockito annotations from the routed primary profile.
- Construct/inject the service through its real constructor or established test convention.
- Mock repositories, gateways, remote clients, clocks, user/security providers, and message publishers at their boundaries.
- Use real BO/DTO/VO/entity values where they improve behavioral confidence.

## Required Scenarios

1. successful orchestration and returned/changed domain values;
2. validation rejection with no forbidden downstream interaction;
3. dependency empty/not-found behavior;
4. dependency exception/error translation;
5. important conditional branch, compatibility default, or idempotency behavior;
6. changed regression path from Spec/Code Review.

## Verification

- Assert returned value or propagated domain exception.
- Capture and assert repository/gateway command values when mapping matters.
- Verify side-effect count and absence on rejection paths.
- Avoid `verifyNoMoreInteractions` unless extra calls would be a contractual defect.
- Do not claim to unit-test transaction rollback. Verify service behavior; transaction semantics need appropriate integration evidence if required.

## Anti-Patterns

- Mocking the service under test.
- Deep stubs that hide an unstable design.
- `@SpringBootTest` for logic that needs only Mockito.
- Assertions limited to `notNull` or “no exception”.
- Reproducing production algorithms inside expected-value calculations.
- Adding sleep/time dependence instead of injecting/controlling time.

## Completion Evidence

Map each test to requirement/finding and record test source hash, mock boundaries, exact execution entry, counts, failures/skips, and scope SHA-256.
