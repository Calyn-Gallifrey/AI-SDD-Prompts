# UAW SDD Demo

Spring Boot + Maven demo project for validating the UAW-SDD workflow.

## Requirements

- Java 17+ for compilation
- Maven 3.9+

The `maven-surefire-plugin` configuration enables dynamic agent loading and Byte Buddy experimental mode so Mockito-based tests can run on newer local JDKs while compiling with Java 17 target compatibility. Newer JDKs may still print Byte Buddy `sun.misc.Unsafe` compatibility warnings; they do not fail the current test suite.

## Run Tests

```bash
mvn test
```

## Start App

```bash
mvn spring-boot:run
```

## APIs

Create a policy info change work order:

```http
POST /api/work-orders/policy-info-change
Content-Type: application/json

{
  "policyNo": "P-10001",
  "changeFieldType": "HOLDER_PHONE",
  "oldValue": "13800000000",
  "newValue": "13900000000",
  "requester": "alice"
}
```

Get a policy info change work order:

```http
GET /api/work-orders/policy-info-change/{workOrderId}
```

The response includes `changeSummary`, a read-only summary derived from `changeFieldType`, `oldValue`, and `newValue`.

Create a policy beneficiary change work order:

```http
POST /api/work-orders/policy-beneficiary-change
Content-Type: application/json

{
  "policyNo": "P-20001",
  "beneficiaryName": "Bob",
  "beneficiaryIdNo": "1234567890",
  "beneficiaryRelation": "CHILD",
  "benefitRatio": 50,
  "requester": "alice"
}
```

Create a policy beneficiary email change work order:

```http
POST /api/work-orders/policy-beneficiary-change/email
Content-Type: application/json

{
  "policyNo": "P-20001",
  "beneficiaryName": "Bob",
  "beneficiaryIdNo": "1234567890",
  "beneficiaryEmail": "bob@example.com",
  "requester": "alice"
}
```

Create an I need document work order:

```http
POST /api/work-orders/i-need-document
Content-Type: application/json

{
  "policyNo": "P-30001",
  "customerName": "Mary",
  "requestType": "SEND_DOCUMENT",
  "documentTypes": ["policy schedule", "statement"],
  "deliveryEmail": "customer@example.com",
  "requester": "agent01"
}
```
