# Database Table And DDL Rule

## Trigger And Required Inputs

Use for approved schema/table/index changes. Confirm database engine/version, owning module, current migration/deployment convention, table purpose, columns/types/null/defaults, keys/indexes, retention, sensitive-data handling, rollout, and rollback. Do not infer schema from model examples.

## Naming And Structure

- Follow the current database/project convention. Use `iic_crm_<business_entity>` only when current UAW schema confirms that prefix.
- Every column has a clear purpose and compatible type/length/precision.
- Primary/unique/foreign key behavior is explicit.
- Indexes map to verified query predicates/order and data cardinality; avoid redundant indexes.
- Timestamps/audit/soft-delete/tenant/country fields follow current schema, not a generic template.
- Sensitive values use the approved encryption/tokenization mechanism. Searchable sensitive data requires an approved non-reversible lookup representation and access controls.

## Migration Safety

- Use the repository's existing versioned migration/DDL path; do not execute SQL against an environment.
- No destructive `DROP`, broad `DELETE`, column narrowing, or irreversible rewrite without explicit approved migration and rollback/data-recovery plan.
- Define lock/downtime and backward-compatible rollout for large/live tables.
- Make rerun/idempotency behavior consistent with the current migration tool.
- Include verification queries or schema checks that are safe and read-only.

## Allowed File Scope

The approved Tasks may allow both:

1. the exact migration/DDL directory (often `db/**`, when current project confirms it); and
2. the exact existing deployment descriptor path.

This rule does not restrict edits to `db/**` while simultaneously requiring a descriptor elsewhere. Both paths must be explicit in implementation scope. If the descriptor is missing/unparseable, block; do not create a replacement unless Design explicitly approves its format/location.

When the descriptor is JSON/YAML/XML, use a parser/serializer or established project tool. Preserve unrelated entries and formatting as far as the tool allows. Never update a deployment environment not approved by the feature.

## Required Evidence

- schema source and database version;
- DDL/migration file path and checksum;
- deployment descriptor path/change, if required;
- compatibility/rollback analysis;
- sensitive-data decision;
- query/index rationale;
- static parse/lint or approved migration validation result.

## Block Conditions

Block when engine, current migration convention, destructive impact, sensitive-data policy, deployment target, or required field semantics are unknown.
