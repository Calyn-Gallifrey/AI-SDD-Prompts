# Backend API Rule

## Trigger And Evidence

Use for a new/changed HTTP or service API. Before Design, inspect the current controller/service, response/error wrapper, validation, authorization, logging, package layout, and nearby tests in the target module. User-approved API contract and current module code take precedence over examples.

## Responsibilities

| Layer | Owns | Must not own |
|---|---|---|
| Controller/entry | routing, binding, validation trigger, authorization handoff, response/error integration | business orchestration, persistence |
| Service/application | business orchestration, transaction/idempotency boundary, gateway/repository calls | HTTP serialization details |
| Strategy, if justified | one explicit variation selected deterministically | hidden global routing or duplicate keys |
| Mapper/converter | explicit model mapping and defaults | remote/persistence calls |
| Repository/gateway | persistence/external boundary | API response construction |

Create only layers/models needed for the approved delta. Reuse existing public API and symbols for enhancement work unless a breaking change is explicitly approved.

## Contract Rules

- Request/response types, wrapper, annotations, error mapping, and route style follow current target-module conventions.
- Use BO/DTO/VO/Entity only at their owned boundaries; see model rules.
- Validate at the boundary and enforce business invariants in the owning service/domain component.
- Define null/empty/default and compatibility behavior for every changed field.
- Authorization is explicit and deny-by-default for missing/invalid identity.
- Do not log complete request/response objects when they may contain sensitive or high-volume data.

## Strategy Registry Safety

When current architecture builds a strategy map:

```java
Object previous = strategyMap.putIfAbsent(key, strategy);
if (previous != null) {
    throw new IllegalStateException("Duplicate strategy key: " + key);
}
```

`putIfAbsent` keeps the previous value; never log that the new value overwrote it. Duplicate behavior (fail fast or explicitly approved deterministic priority) must be designed and tested. Do not silently skip missing/blank keys.

## Transactions, Errors, And Observability

- Put transaction ownership on the application/service operation according to current framework convention.
- Specify idempotency and partial-failure behavior for write APIs.
- Map internal/external exceptions through the existing error contract; do not leak stack traces or provider payloads.
- Log stable identifiers, outcome, latency, and actionable error context. Redact secrets and personal data.

## Required Tests

- successful request/response contract;
- validation and authorization rejection;
- service/gateway error mapping;
- boundary/default/compatibility behavior;
- idempotency/duplicate strategy behavior when applicable;
- regression for the approved change.

## Block Conditions

Block Design/implementation when route ownership, contract fields, authorization rule, transaction behavior, or response/error convention cannot be established safely.
