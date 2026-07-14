# Transaction Module Package Rule

## Trigger And Baseline

Use for changes inside the UAW transaction module. Inspect the actual module root and nearest existing feature package first. Current package layout and build configuration are authoritative; historical full trees are not instructions to create unused directories.

## Ownership

Typical layers, only when present/needed:

| Area | Responsibility |
|---|---|
| `base` | stable transaction abstractions/contracts shared broadly |
| `common` | genuinely shared transaction behavior with multiple consumers |
| `core/<feature>` | feature-owned controller/service/strategy/model/persistence code |
| `support` | infrastructure adapters/utilities, not feature business logic |
| `task` | scheduled/async task entry and support only for approved task features |

New feature-specific code belongs under the nearest current `core/<feature>` convention. Do not promote code to `common/base/support` without multiple concrete consumers and an approved ownership decision.

## Package And Class Rules

- Package names are lowercase and mirror source directories.
- Service implementations use the current module's `service.impl`/equivalent convention consistently; do not alternate `implementation`, root service classes, and `impl` without evidence.
- Create only packages containing approved files.
- `package-info.java` follows current module practice. It is neither universally required nor universally forbidden.
- Do not include OS-specific directory commands in Design/Tasks; use repository paths and normal file operations.
- Suffixes (`Controller`, `Service`, `ServiceImpl`, `Strategy`, `Mapper`, `Entity`, `BO`, `DTO`, `VO`, `Converter`, `Helper`) reflect actual responsibility.

## Dependency Direction

- entry/controller -> application/service -> domain/strategy -> gateway/repository boundary;
- infrastructure implementations may depend on external/persistence libraries but expose internal contracts;
- lower/shared layers must not depend on feature controllers or response models;
- avoid cycles and cross-feature internals; use an explicit shared contract only when approved.

## Change Control

Enhancement/fix work should modify existing symbols rather than create a parallel package tree. A package move/rename is a refactor requiring compatibility, import/config/resource updates, and regression scope in Design.

## Validation

- verify package declarations and resource scanning;
- verify Spring/MyBatis/MapStruct component discovery where used;
- check dependency direction and no duplicate ownership;
- compile/test the affected module.

## Block Conditions

Block when the real module root, nearest existing pattern, ownership, or scanning/resource convention is unknown.
