---
name: uaw-unit-test
description: Generate, repair, and summarize Java-focused UAW unit test code. Use when the user asks to create, update, or review unit tests, produce Unit Test Summary, validate Java/Spring Boot test profiles, or when the SDD AI coding skill automatically triggers unit testing after Code Review and Auto-fix.
---

# UAW Unit Test

## Core Contract

This skill generates or updates UAW unit test source code and produces Unit Test Summary. Java and Spring Boot are the primary target.

Every invocation must result in newly created or updated unit test code when project files are accessible and a test target can be identified. Producing only analysis, review comments, validation notes, or Unit Test Summary is not sufficient.

Unit Test Summary is an audit artifact after test code generation. It must not replace unit test source code.

Do not mark unit test code generation as not applicable. If the project cannot be read, the test target cannot be identified, or the test framework cannot be determined with available evidence, stop in `blocked` status and request the missing information. A blocked result must not be treated as a successful Unit Test Gate.

Read `references/input-examples.md` before requesting standalone input. The file defines the expected Java unit-test input structure.

Input templates are not default test targets. Placeholder paths, test class names, commands, and validation entries must be replaced by project-scanned or user-confirmed values.

Read `references/templates/unit-test-summary-template.md` before producing or updating Unit Test Summary.

## Input Policy

Standalone input is limited to information that cannot be reliably scanned from project files.

Required standalone inputs:

- `Project Root（项目根目录）`
- `Test Target（测试目标）`
- `Validation Method（验证方式）`
- `Actual Test Entry（实际执行入口）`

Automatically scan and record:

- Build Tool: Maven, Gradle, Maven Wrapper, or Gradle Wrapper
- Java Version
- Spring Boot Version
- Test Framework: JUnit4, JUnit5, Legacy-Mockito, or No-UAW-Util
- Changed Files
- Existing Test Style
- Whether UAW utility classes exist

## SDD Mode

When invoked by `uaw-sdd-ai-coding`, unit-test inputs are derived from `proposal-input.md`, `spec.md`, `design.md`, `tasks.md`, `code-review-findings.md`, Auto-fix Summary, and current code changes.

SDD mode must generate or update unit test code for the implemented change before producing `unit-test-summary.md`. If no matching test file exists, create a new test file following the selected testing profile and the existing project test layout. If a matching test file exists, update it to cover the current change.

## Output Requirements

Unit Test Summary must follow `references/templates/unit-test-summary-template.md`.

Required fields:

- Selected Testing Profile
- Selection rationale
- Test files added or updated
- Validation Method
- Execution Environment
- Actual Test Entry
- Test result: pass, fail, skipped, not run, or blocked
- warning / failure / skipped notes
- Remaining test risks

Template sections must be retained. Sections that do not apply are marked as `not applicable` with a reason.

`Test files added or updated` must contain at least one real unit test source file path. `none` is allowed only when the skill is blocked before code generation, and the Unit Test Gate result must then be `blocked`.

Local `mvn` or `gradle` availability is not a prerequisite. IDE, Wrapper, Local CLI, CI, Script, Manual, and Other are valid validation methods when recorded with evidence.

## References

- `references/input-examples.md`: concise Java input structure template.
- `references/testing-profile-routing.md`: profile selection and validation rules.
- `references/templates/unit-test-summary-template.md`: required Unit Test Summary output template.
- `references/java/`: detailed Java test generation rules for methods, services, static methods, controllers, and ServiceStrategy.
