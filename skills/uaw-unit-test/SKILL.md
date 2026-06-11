---
name: uaw-unit-test
description: Generate, repair, and summarize Java-focused UAW unit tests. Use when the user asks to create or review unit tests, produce Unit Test Summary, validate Java/Spring Boot test profiles, or when the SDD AI coding skill automatically triggers unit testing after Code Review and Auto-fix.
---

# UAW Unit Test

## Core Contract

Use this skill to generate or validate UAW unit tests and produce Unit Test Summary. Java and Spring Boot are the primary target.

Always read `references/input-examples.md` before requesting standalone input. All user-facing input examples must use `English Field（中文字段）：示例值`.

Always read `references/templates/unit-test-summary-template.md` before producing or updating Unit Test Summary.

## Input Policy

Keep standalone user input minimal. Ask the user only for information that cannot be reliably scanned from the project.

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

When invoked by `uaw-sdd-ai-coding`, do not ask the user to repeat unit-test inputs. Derive target files, test scope, and validation expectations from `proposal-input.md`, `spec.md`, `design.md`, `tasks.md`, `code-review-findings.md`, Auto-fix Summary, and current code changes.

## Output Requirements

Always output or update Unit Test Summary by following `references/templates/unit-test-summary-template.md`.

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

Do not omit template sections. If a section is not applicable, mark it as `not applicable` and explain why.

Do not force local `mvn` or `gradle` availability as a prerequisite. IDE, Wrapper, Local CLI, CI, Script, Manual, and Other are all valid validation methods when recorded honestly.

## References

- `references/input-examples.md`: concise Java input example.
- `references/testing-profile-routing.md`: profile selection and validation rules.
- `references/templates/unit-test-summary-template.md`: required Unit Test Summary output template.
- `references/java/`: detailed Java test generation rules for methods, services, static methods, controllers, and ServiceStrategy.
