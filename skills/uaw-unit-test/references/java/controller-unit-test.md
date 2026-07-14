# Controller Unit-Test Rule

Use for HTTP controller request mapping, validation, authorization handoff, serialization, and exception translation.

## Harness Selection

Choose from current executable project evidence:

- standalone MockMvc for focused mapping/validation with mocked service;
- supported Spring MVC slice when filters, advice, converters, or security configuration are part of the contract;
- direct method testing only when the controller is not HTTP-mapped or the approved change is purely method-level and nearby tests use it.

Do not use `@SpringBootTest` by default. Do not add a Spring test dependency that the module lacks without approved scope.

## Required Scenarios

1. correct method/path/content type;
2. valid request binding and service arguments;
3. response status and important JSON/body fields;
4. required-field, format, range, and malformed-body validation as applicable;
5. authorization/authentication behavior when in scope;
6. service/domain exception to HTTP error mapping;
7. compatibility/default behavior for changed request/response fields;
8. regression scenario from Spec or findings.

## Assertions

- Assert status plus contract-relevant headers/body, not status alone.
- Verify service is not called on rejected requests.
- Capture service input when request-to-model mapping changed.
- Use the project's configured object mapper/converters when serialization behavior matters.
- Do not duplicate framework internals or assert incidental JSON formatting.

## Security

Use established test security helpers/configuration. Never bypass security merely to make the test pass when authorization is in contract. Do not embed real tokens, credentials, or personal data.

Record harness/profile evidence, test paths, endpoint/scenario mapping, execution entry, result counts, and current scope hash.
