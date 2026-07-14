# Case Tracker Compatibility Rule

## Trigger

Load only when an approved change adds/renames/retires a transaction type and current code shows Case Tracker depends on that type.

## Required Current Evidence

Before Design, identify and record:

- current transaction-type enum/config symbol and file;
- current Case Tracker lookup/selection path;
- current dictionary table/schema and migration convention;
- exact persisted transaction type/code/display values from approved requirements;
- existing uniqueness, language, country, status, and ordering semantics;
- rollout and rollback mechanism.

Historical names such as `TransactionTypeConfigEnum` or `iic_crm_base_data` are discovery hints only. If current code/schema does not confirm them, do not generate edits or SQL from those names.

## Design Rules

1. Define one canonical transaction identifier and map enum/config, persisted code, display text, and Case Tracker behavior explicitly.
2. Preserve existing identifiers unless migration is approved; display-name changes must not silently change persisted codes.
3. Use the project's existing migration path. Do not execute database changes from the Skill.
4. Migration must be deterministic and safe to rerun according to current project convention; avoid unconditional delete/reinsert that can destroy localized or user-managed data.
5. Define conflict behavior when the code already exists with different values.
6. Include language/country/status/order only when confirmed by current schema and requirement.
7. Include rollback/disable behavior and compatibility for existing transactions.

## Required Tests

- new type maps to the expected Case Tracker path;
- existing transaction types remain unchanged;
- unknown/disabled type behavior is explicit;
- duplicate/config conflict is handled;
- persistence/display mapping uses approved values;
- migration validation is recorded where executable database tests are unavailable.

## Block Conditions

Block when the current enum/config owner, table/schema, canonical code, or Case Tracker behavior cannot be established. Do not fill these gaps from the historical source example.
