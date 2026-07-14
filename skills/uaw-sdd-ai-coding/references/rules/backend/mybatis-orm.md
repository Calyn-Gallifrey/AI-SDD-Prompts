# MyBatis ORM Rule

## Trigger And Discovery

Use for MyBatis/MyBatis-Plus persistence changes. Inspect the target module's mapper interfaces, XML/resource locations, aliases/type handlers, pagination, base entities/mappers, naming strategy, and tests before Design.

The current build/resource configuration decides where XML lives. Do not assume Java package directories or `resources/mapper` without evidence.

## Mapper And XML

- Interface and XML namespace must match exactly.
- Statement IDs must match interface methods and parameter/return types.
- In UAW transaction modules that currently use XML SQL, keep SQL in XML and do not introduce `@Select/@Insert/@Update/@Delete` annotations.
- In other modules, preserve the established approach unless Design explicitly approves migration.
- Use explicit `resultMap` when names/types/nesting are non-trivial; avoid fragile positional/implicit mapping.
- Qualify ambiguous columns and alias joined columns deterministically.
- Bind values with `#{}`. Use `${}` only for a strictly allow-listed structural fragment with documented justification; never for raw user input.

## Query And Data Integrity

- Define expected cardinality. A “single” query must have a verified uniqueness guarantee or explicit multiple-row behavior.
- Avoid `SELECT *`; select owned fields to protect compatibility and performance.
- Define null/empty collection behavior for dynamic SQL. Prevent accidental full-table update/delete.
- Batch operations have bounded size and transaction behavior.
- Pagination/order is deterministic; indexes support verified filters/order where needed.
- Map enums, dates/timezones, JSON, encrypted fields, and decimals with current type handlers/conventions.
- Respect tenant/country/soft-delete/data-access predicates already required by the module.

## Models

Entities represent persistence rows; DTOs represent query/inter-layer projections. Do not leak Entity into API BO/VO. Inheritance, Lombok, table annotations, and base mapper use are conditional on current module conventions, not universal requirements.

## Tests And Validation

- parse/load mapper XML through the actual build when possible;
- test dynamic SQL branches, empty inputs, cardinality, join aliases, type handlers, and regression query behavior;
- use integration/database evidence when SQL semantics cannot be proven by a pure unit test;
- record schema/mapper/XML paths and execution evidence.

## Block Conditions

Block when table/schema, XML resource convention, cardinality, data-access predicates, or destructive-query boundary cannot be established.
