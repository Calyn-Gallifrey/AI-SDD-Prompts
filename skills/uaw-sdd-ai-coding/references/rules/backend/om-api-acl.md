# OM API Anti-Corruption Layer Rule

## Trigger And Evidence

Use only for a confirmed Old Mutual (OM) external API integration. Identify the current OM client/SDK operation, request/response/error contract, authentication, timeouts/retries, shared ACL utilities, and a current module example.

This rule is distinct from EPI. Do not route an EPI call through OM types/utilities merely because the old examples looked similar.

## ACL Structure

1. Business/application services depend on an internal OM gateway/service interface, not an external SDK client.
2. The implementation owns transport invocation and delegates deterministic mapping/parsing.
3. External OM request/response/result types do not escape into domain/controller contracts.
4. Use an existing `RemoteResultUtil` or equivalent only if current OM code confirms its contract handles success, error code, null data, warnings, and partial results correctly. `Optional.empty()` must not erase a provider error.
5. Map OM errors to internal typed outcomes/exceptions with provider code/correlation retained safely.
6. Define timeout/retry/fallback per operation. Retry only safe/idempotent calls.
7. Redact credentials and personal/provider payload data in logs; preserve approved correlation identifiers.

## Mapping

- Field mapping and defaults are explicit and version-aware.
- Unknown enum/status behavior is defined.
- Null/empty/partial payload behavior follows the actual OM contract.
- Date/time, money/precision, locale/country, and identifier conversion are tested where present.

## Tests

- request/header/auth metadata mapping without real secrets;
- successful and empty/partial response mapping;
- OM business error, malformed response, timeout, and transport failure;
- retry/fallback and idempotency behavior when configured;
- compatibility for unknown/new provider values.

## Block Conditions

Block when the current OM operation contract, external type version, error semantics, auth, or timeout/retry policy is unknown. Do not implement from illustrative class names.
