---
name: uaw-unit-test
description: Generate, repair, and summarize Java-focused UAW unit tests. Use when the user asks to create or review unit tests, produce Unit Test Summary, validate Java/Spring Boot test profiles, or when the SDD AI coding skill automatically triggers unit testing after Code Review and Auto-fix.
---

# UAW Unit Test

## Core Contract

This skill generates or validates UAW unit tests and produces Unit Test Summary. Java and Spring Boot are the primary target.

Read `references/input-examples.md` before requesting standalone input. The examples define the expected Java unit-test input structure.

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

## Output Requirements

Unit Test Summary must follow `references/templates/unit-test-summary-template.md`.

Required fields:

- Selected Testing Profile
- Selection rationale
- Test files added or updated
- Validation Method
- Execution Environment
- Actual Test Entry
- Test result: pass, fail, skipped, or not applicable
- warning / failure / skipped notes
- Remaining test risks

Template sections must be retained. Sections that do not apply are marked as `not applicable` with a reason.

Local `mvn` or `gradle` availability is not a prerequisite. IDE, Wrapper, Local CLI, CI, Script, Manual, and Other are valid validation methods when recorded with evidence.

## References

- `references/input-examples.md`: concise Java input example.
- `references/testing-profile-routing.md`: profile selection and validation rules.
- `references/templates/unit-test-summary-template.md`: required Unit Test Summary output template.
- `references/java/`: detailed Java test generation rules for methods, services, static methods, controllers, and ServiceStrategy.
