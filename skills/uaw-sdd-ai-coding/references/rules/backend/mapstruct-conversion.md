# MapStruct Conversion Rule

## Trigger And Evidence

Use when current module already uses MapStruct or approved Design introduces it with compatible dependencies. Inspect MapStruct version, compiler/plugin configuration, component model, shared `@MapperConfig`, injection strategy, unmapped policy, and nearby converters.

## Component Model

- With `componentModel = "spring"`, inject the generated mapper through Spring using the module's constructor/injection convention. Do not also define/use `Mappers.getMapper(...).INSTANCE`.
- With the default component model, a static `INSTANCE = Mappers.getMapper(...)` may follow current convention. Do not annotate it as a Spring component.
- Never mix both access modes in one converter.

## Mapping Rules

- Use explicit `@Mapping` for renamed, nested, transformed, defaulted, or ignored fields.
- Define null-value and collection behavior; do not rely on an accidental generator default when contract matters.
- Reuse shared config/base converter only when it exists and its generic/qualifier contract matches.
- Pass current user/time/locale through explicit parameters or `@Context` when needed; avoid hidden global access.
- Keep external/persistence types at their boundaries; converter methods must make ownership clear.
- For updates, define whether null overwrites or is ignored.
- Custom expressions/default methods remain deterministic and side-effect free.

## Validation And Tests

- compile generated sources with the actual annotation processor;
- test renamed/nested/default/null/collection behavior and update semantics;
- verify Spring injection or static access according to the selected component model;
- review unmapped target warnings/errors and explicitly resolve intentional ignores.

## Block Conditions

Block when module configuration, component model, shared mapper config, or mapping contract cannot be established. Do not add a second incompatible MapStruct convention.
