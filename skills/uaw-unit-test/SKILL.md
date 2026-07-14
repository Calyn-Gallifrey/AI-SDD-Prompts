---
name: uaw-unit-test
description: Generate, update, execute, and summarize Java-focused UAW unit tests. Use for direct unit-test work or SDD2 test generation after Code Review. In SDD mode it uses a two-pass handoff so changed test source is frozen and fully reviewed before execution and Unit Test Summary.
---

# UAW Unit Test

## Core Contract

Generate or update real unit-test source for every accessible production change with an identifiable target. A prose plan, review note, manual check, or `unit-test-summary.md` alone is never test implementation.

Read `references/testing-profile-routing.md`, the selected target rule under `references/java/`, and `references/templates/unit-test-summary-template.md`.

Do not add/upgrade test dependencies merely to fit a preferred style. Current build dependencies and nearby executable tests are the primary convention. If project files, target code, framework, or a runnable entry cannot be established, return `blocked` with exact recovery information.

## SDD Mode: Two Passes

### Pass 1: Generate Test Source

Inputs from `uaw-sdd-ai-coding`:

- current feature/state and frozen implementation scope;
- approved Spec, Design, and Tasks;
- immutable Code Review findings and Auto-fix summary;
- exact production symbols and captured test path patterns.

Create/update tests under approved paths and return changed test paths plus selected profile evidence. Do not create Unit Test Summary yet.

Test-source changes invalidate the old scope. Return control so `uaw-sdd-ai-coding` can freeze the new production+test snapshot, rerun full Code Review, and close Auto-fix on that same snapshot.

### Pass 2: Execute And Summarize

Run only after Code Review is `passed` and Auto-fix is `passed`/`not-required` on the current frozen scope. Verify at least one changed test source matches the captured test path patterns.

Execute the narrow relevant unit tests using an actual project-supported entry. Produce `unit-test-summary.md` with command/environment, exit code, counts, failures/skips, test-source hashes, and current scope SHA-256. Return control for the deterministic Unit Test gate and human Unit Test Summary approval.

`passed` requires an executed test entry with exit code/result proving success. IDE/CI/Wrapper/local CLI/project script are valid when evidence is reproducible. Manual validation may supplement unit tests but cannot produce a passed SDD Unit Test Gate.

## Standalone Mode

Read `references/input-examples.md`. Required user inputs are only facts that cannot be discovered safely: project root, target when ambiguous, and preferred validation environment when multiple unavailable-to-agent choices remain.

Generate/update test source first. Execute when possible. A standalone summary may be `not-run` with a precise reason and command for later execution, but must not be represented as passed.

## Required Discovery

Record evidence for:

- build tool/wrapper and module;
- Java, Spring Boot when present, JUnit platform, Mockito, assertion libraries;
- Surefire/Gradle test configuration and JDK compatibility;
- nearby executable test style;
- target dependencies and mock boundaries;
- UAW utility availability only when target code uses it.

## Outputs

- one or more added/updated unit-test source paths;
- selected testing profile and target-specific rule;
- executable test evidence or a blocked/not-run result;
- `unit-test-summary.md` only after source generation.

Never use `none` for test-source changes in a successful SDD flow. Failed, blocked, or not-run SDD tests forbid successful Archive.

## References

- `references/testing-profile-routing.md`: evidence-based framework/profile selection.
- `references/java/`: target-specific generation rules.
- `references/templates/unit-test-summary-template.md`: summary and gate evidence.
- `references/input-examples.md`: standalone input examples only.
