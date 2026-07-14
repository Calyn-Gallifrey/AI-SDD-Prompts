# EPI Gateway Integration Rule

## Boundary

Use only for a confirmed EPI integration. This is not an OM ACL rule. Do not copy OM client types, package names, parser utilities, result wrappers, or error semantics into EPI code unless current EPI implementation explicitly shares them.

## Required Contract Evidence

Before Design, identify:

- current EPI client/SDK/transport and owning module;
- operation, endpoint/topic, request/response schema, and version;
- authentication/headers/correlation requirements;
- timeout, retry, rate-limit, idempotency, and availability semantics;
- EPI success/error/partial-result contract;
- approved sensitive-data handling and observability;
- one current EPI integration example when available.

If the actual EPI contract is unavailable, block. Do not generate a client from placeholders.

## Design

1. Put EPI-specific types behind a gateway/adapter owned by the integration boundary.
2. Map internal request models to EPI request types explicitly; map EPI responses/errors to internal DTO/domain errors before returning to business services.
3. Do not expose EPI SDK/result classes through controller or domain APIs.
4. Define null/empty/partial response behavior from the real EPI contract.
5. Retries apply only to documented safe/idempotent operations and must avoid retry storms.
6. Propagate/generate correlation IDs using existing infrastructure; redact credentials and personal data.
7. Keep fallback/circuit-breaker behavior explicit and observable; no silent empty-success conversion.

## Tests

- exact request/header mapping;
- successful response mapping;
- EPI business error and transport timeout mapping;
- null/malformed/partial response behavior;
- retry/idempotency behavior when configured;
- sensitive-data-safe logging and correlation behavior where testable.

## Review Evidence

Record the EPI contract/source version, adapter symbols, timeout/retry config, mapped error table, and tests. Any contract assumption remains an open question and blocks implementation where it affects behavior.
