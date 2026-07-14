# DTO Model Rule

## Ownership

A DTO transports data between application/integration layers or represents a query projection. Do not create one when an existing owned type already matches the contract.

## Naming And Placement

- New UAW transaction types use exact suffix `DTO` when current module follows it.
- Preserve established module convention for existing/public types; avoid mass renaming.
- Place beside the owning application/integration boundary, not in a generic global package by default.

## Structure

- DTOs do not expose persistence Entities, API BOs, or API VOs as fields.
- Nested owned data may use another DTO or an appropriate immutable/value type. Java standard value types, enums, money/date types, and collections are allowed when their semantics are defined; “non-primitive must be DTO” is not a valid universal rule.
- Keep transport fields focused; avoid business behavior and persistence annotations.
- API schema/validation annotations appear only when the DTO is actually an API boundary and current convention permits it.
- Define null/default, collection mutability, enum/unknown-value, date/timezone, and precision behavior.
- Use Lombok/serialization interfaces according to current module compatibility.

## Mapping And Tests

Use explicit mapping for renamed/transformed fields. Test null/default/nested/collection and provider/persistence projection mappings that changed. Prevent sensitive/unneeded fields from crossing boundaries.

## Block Conditions

Block when DTO owner, source/target contract, field semantics, or target package/style cannot be established.
