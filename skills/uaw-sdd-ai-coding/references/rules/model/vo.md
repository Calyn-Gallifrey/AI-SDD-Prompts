# VO Model Rule

## Ownership

A VO represents the API/view output contract. Create one only when the response boundary needs an owned shape distinct from current compatible output.

## Naming And Placement

- New UAW response types use exact suffix `VO` when the target module follows it.
- Preserve established public type names and package conventions unless a breaking migration is explicitly approved.
- Place under the feature's current response/VO package.

## Structure

- Include only approved client-visible fields; never expose Entity or external provider types.
- Nested output uses VO/value types appropriate to the response contract.
- Define null/default, empty collection, ordering, enum/unknown-value, date/timezone, precision, masking, and backward compatibility.
- Extend a base VO only when its public fields/serialization contract apply. Inheritance must not accidentally expose irrelevant fields.
- `Serializable`, Lombok, API-schema annotations, and custom `toString` follow current target-module/framework conventions rather than universal requirements.
- Sensitive fields are omitted or masked per approved contract; never leak them through `toString`/logs.

## Mapping And Tests

Use explicit mapping from internal DTO/domain types for renamed/defaulted/masked fields. Test serialization contract, added-field compatibility/default, nested/collection behavior, ordering, masking, and null handling.

## Block Conditions

Block when response ownership, client compatibility, field semantics, masking, or current serialization convention is unknown.
