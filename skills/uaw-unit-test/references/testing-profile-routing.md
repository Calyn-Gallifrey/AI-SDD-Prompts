# Java Testing Profile Routing

## 1. Evidence Before Selection

Inspect the target module's build files, dependency tree/configuration, test plugin, Java toolchain, and nearby executable tests. Record exact paths and versions when available.

Do not select from Spring Boot version alone. The actual JUnit engine, runner/extension, Mockito support, and test task configuration determine executability.

## 2. Primary Framework Profile

Select exactly one:

### `JUNIT5_MOCKITO`

Use when JUnit Jupiter is configured and nearby tests execute on it.

- `org.junit.jupiter.api.Test`
- `@ExtendWith(MockitoExtension.class)` when Mockito injection is useful
- Jupiter assertions or the project's existing assertion library
- no Vintage/JUnit4 dependency addition

### `JUNIT4_MOCKITO`

Use when the module runs JUnit4 and nearby tests use it.

- `org.junit.Test`
- `@RunWith(MockitoJUnitRunner.class)` or the established rule/runner style
- JUnit4-compatible assertions
- do not migrate the module during feature test work

### `EXISTING_CUSTOM`

Use when the module has a custom base class, runner, extension, test harness, or mixed platform that is demonstrably required. Cite one or more executable nearby tests and preserve only necessary conventions.

### `BLOCKED_UNKNOWN`

Use when no executable test engine can be established. Do not guess imports or add dependencies. Return the missing evidence and recovery action.

## 3. Compatibility Modifiers

Modifiers do not replace the primary profile:

- `LEGACY_JDK_MOCKITO`: record JDK/Mockito/Byte Buddy compatibility. Reuse existing JVM flags only when already configured; do not introduce `net.bytebuddy.experimental` as a silent workaround.
- `NO_UAW_UTIL`: target code does not use or project lacks UAW utilities. Do not import invented helpers.
- `SPRING_SLICE`: existing controller/data slice tests and dependencies justify a Spring test slice.
- `PURE_MOCKITO`: no Spring context is needed; preferred for service/method/strategy tests.
- `STATIC_MOCKING_AVAILABLE`: current dependencies already support scoped static mocking.

## 4. Target Rule Routing

| Target | Rule |
|---|---|
| Method/domain helper | `java/method-unit-test.md` |
| Service/application component | `java/service-unit-test.md` |
| Static utility behavior | `java/static-method-unit-test.md` |
| HTTP controller | `java/controller-unit-test.md` |
| ServiceStrategy/strategy selection | `java/service-strategy-unit-test.md` |

For mixed targets, use one primary rule and cite additional rule sections only for actual boundaries.

## 5. Execution Entry Selection

Prefer in order when available and appropriate:

1. repository wrapper command scoped to module/test;
2. established project script;
3. installed Maven/Gradle command matching project config;
4. reproducible IDE configuration or CI job when the agent cannot run locally.

An IDE/CI result must include configuration/job identity and observed result. A suggested future command is `not-run`, not `passed`. Manual checks cannot pass the SDD unit-test gate.

## 6. Dependency Rule

Do not add a test dependency unless existing approved Design/Tasks require it and no current supported test mechanism can cover the target. Any dependency change is implementation scope, requires a new freeze, full Code Review, and explicit evidence.

## 7. Result Normalization

- `passed`: relevant tests executed successfully; exit/result and counts recorded.
- `failed`: tests executed and failed.
- `blocked`: missing target/framework/environment evidence prevents safe generation or execution.
- `not-run`: tests were generated but not executed; never Archive-eligible.

Skipped tests are counts/risks, not a gate status. If a required scenario is skipped, use `failed` or `blocked` based on cause.
