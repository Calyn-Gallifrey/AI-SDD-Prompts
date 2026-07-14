# Entity Model Rule

## Ownership

An Entity represents persistence state for a verified table/query contract. It must not be used as controller request/response or external integration contract.

## Naming And Placement

- New UAW persistence types use suffix `Entity` when the target module does; preserve established existing conventions where table-named entities differ.
- Place under the owning persistence package determined from current mapper configuration.
- Extend `BaseEntity`, `BaseTransactionEntity`, or another base only when it exists and its columns/annotations match the table. Do not duplicate inherited columns.

## Mapping

- Table/column annotations and MyBatis-Plus vs XML mapping follow the detected persistence stack.
- Define primary-key generation, null/default, optimistic lock, soft delete, tenant/country, audit fields, enum/type handlers, JSON, dates/timezones, money/precision, and sensitive storage from current schema.
- Do not add API schema or Bean Validation annotations unless the Entity truly owns that boundary (normally it does not).
- Avoid broad `equals/hashCode/toString` over mutable relations, large fields, or sensitive values. Lombok is conditional on current safe conventions.
- Relationships/nested objects require an explicit query/result mapping; they are not implicit table columns.

## Compatibility

Entity changes must align with approved schema rollout. A field added to code before/after DDL needs backward-compatible behavior and deployment order. Do not assume column existence from an API request.

## Tests And Validation

- mapper/XML loading and field mapping;
- key/default/type-handler/soft-delete behavior where changed;
- query projection and cardinality;
- sensitive-data persistence/redaction;
- compatibility with rollout order.

## Block Conditions

Block when table schema, key/defaults, base entity semantics, mapping technology, or sensitive-data policy is unknown.
