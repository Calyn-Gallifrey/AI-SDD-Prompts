# BO Model Rule

## Ownership

A BO represents API/application business input. Create one only when it owns a real input boundary distinct from an existing compatible type.

## Naming And Placement

- New UAW transaction types use the exact uppercase suffix `BO` (for example, `SubmitRequestBO`) when the target module follows that convention.
- Preserve an established target-module convention when different; record the decision in Design. Do not rename existing public types merely to normalize suffix case.
- Place it in the feature's existing BO/request package, not a hard-coded package copied from an example.

## Structure

- Fields are private by default. Use protected base fields only when a current, justified inheritance hierarchy requires subclass access.
- Extend an existing base BO only when its fields/validation/serialization semantics apply. Do not inherit for naming consistency alone.
- Use Bean Validation/current module annotations at the input boundary; define groups only when the API lifecycle needs them.
- Nested business inputs use owned BO/value types. Do not embed persistence Entity or API output VO.
- Define null/default/collection/date/enum behavior from the approved contract.
- Use Lombok, API-schema annotations, serialization IDs, and custom `toString` only according to current module/tool versions.

## Security And Logging

Do not include secrets, tokens, full identifiers, banking/contact data, or other sensitive values in generated `toString`/logs. A generic reflection helper is not automatically safe; exclude/redact fields or omit logging.

## Mapping And Tests

Map BO explicitly to internal DTO/command when ownership differs. Test request validation, boundary/default behavior, nested mapping, and sensitive-data redaction where relevant.

## Block Conditions

Block when request ownership, field contract, validation, sensitive-data classification, or target package convention is unknown.
