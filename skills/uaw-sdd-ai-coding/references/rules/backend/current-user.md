# Current User Rule

## Trigger And Discovery

Use when behavior needs the authenticated user/agent identity. Inspect the current module's security/context API and nearby use before choosing a method. Names such as `UserContext.getUserId()` or `getCurrentUser()` are valid only when current dependencies/code confirm them.

## Rules

1. Define which identity is required: user ID, adviser ID, subject, roles, tenant/country, or system actor.
2. Missing/anonymous context follows an explicit approved security behavior; never fall back to an empty string, arbitrary default, request-supplied identity, or fabricated system user.
3. Service/application code owns authorization-sensitive identity decisions. Helpers/converters should receive the required identity as an explicit argument when practical.
4. A MapStruct converter may use a context parameter (`@Context`) or explicit mapping parameter. Static access/expression is allowed only when it is the established, testable module convention.
5. Do not cache request/user context in static fields or singleton mutable state.
6. Do not log tokens, full user objects, roles/claims payloads, or personal data. Log only approved stable identifiers when needed.
7. Background/async execution must explicitly propagate an approved identity context or use a designed system actor; request thread-local context must not be assumed.

## Tests

- authenticated identity maps/authorizes correctly;
- missing/anonymous identity is denied or handled exactly as designed;
- wrong role/tenant/country is rejected when applicable;
- converter/service receives the intended identity;
- async/background behavior does not accidentally reuse another request's context.

Mock the current context boundary using existing test support. Do not add production fallback logic merely to simplify tests.

## Block Conditions

Block when the current identity API, required identity meaning, missing-user behavior, or async propagation requirement is unknown.
