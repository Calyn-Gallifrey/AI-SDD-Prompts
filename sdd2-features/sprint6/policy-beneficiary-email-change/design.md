# design.md - policy-beneficiary-email-change

## 1. Design Summary

在现有 `PolicyBeneficiaryChangeWorkOrderController`、`PolicyBeneficiaryChangeWorkOrderService`、`PolicyBeneficiaryChangeWorkOrder` 上做小范围增强，新增邮箱变更入口。为避免影响现有受益人变更 API，请求 DTO 单独新增，实体和响应 DTO 增加可选邮箱字段。

## 2. API Design

### 2.1 Endpoint

```http
POST /api/work-orders/policy-beneficiary-change/email
Content-Type: application/json
```

### 2.2 Request

新增 DTO：`CreatePolicyBeneficiaryEmailChangeWorkOrderRequest`

| Field | Type | Validation | Description |
|---|---|---|---|
| policyNo | String | @NotBlank | 保单号 |
| beneficiaryName | String | @NotBlank | 受益人姓名 |
| beneficiaryIdNo | String | @NotBlank | 受益人证件号 |
| beneficiaryEmail | String | @NotBlank @Email | 受益人新邮箱 |
| requester | String | @NotBlank | 提交人 |

### 2.3 Response

复用并扩展 `PolicyBeneficiaryChangeWorkOrderResponse`：

| Field | Description |
|---|---|
| workOrderId | 工单号 |
| policyNo | 保单号 |
| beneficiaryName | 受益人姓名 |
| beneficiaryIdNoMasked | 脱敏证件号 |
| beneficiaryEmail | 归一化后的受益人新邮箱 |
| requester | 提交人 |
| status | 工单状态 |
| createdAt | 创建时间 |

## 3. Service Design

新增方法：

```java
PolicyBeneficiaryChangeWorkOrderResponse createEmailChange(
        CreatePolicyBeneficiaryEmailChangeWorkOrderRequest request)
```

处理流程：

1. 对 beneficiaryEmail 执行 trim。
2. 使用 service 层正则做邮箱格式校验，避免绕过 Controller Validation 直接调用 service 时漏校验。
3. 归一化为 lower-case。
4. 调用 `PolicyBeneficiaryChangeWorkOrder.submittedEmailChange(...)` 创建实体。
5. 调用 `repository.saveSubmittedIfAbsent(...)` 复用重复提交控制。
6. 转换为 response。

## 4. Model Design

### 4.1 Entity

`PolicyBeneficiaryChangeWorkOrder` 新增字段：

```java
private final String beneficiaryEmail;
```

新增工厂方法：

```java
submittedEmailChange(policyNo, beneficiaryName, beneficiaryIdNo, beneficiaryEmail, requester)
```

现有 `submitted(...)` 工厂方法保持原语义，邮箱字段传 `null`。

### 4.2 DTO

- 新增 `CreatePolicyBeneficiaryEmailChangeWorkOrderRequest`。
- `PolicyBeneficiaryChangeWorkOrderResponse` 增加 `beneficiaryEmail`。

## 5. Repository Design

复用 `saveSubmittedIfAbsent`。重复判断仍基于：

```text
policyNo + beneficiaryIdNo + status SUBMITTED
```

本次不新增 repository 接口方法。

## 6. Test Design

选择测试 Profile：`Legacy-Mockito`

选择依据：
- `pom.xml` 使用 Spring Boot 3.3.5、Java 17。
- 已有测试大量使用 JUnit4、MockitoJUnitRunner。
- 当前 Maven Surefire 已配置 `-Dnet.bytebuddy.experimental=true` 支持当前 Java 运行环境。

测试覆盖：

- Service 成功创建邮箱变更工单，返回小写邮箱。
- Service 对空邮箱、非法邮箱返回 `BadRequestException`。
- Controller 成功请求返回 HTTP 201。
- Controller validation 对非法邮箱返回 HTTP 400。
- Repository 对同一 policyNo + beneficiaryIdNo 的邮箱变更重复提交返回 empty。

## 7. Human Review

| Review Stage | Reviewer Role | Review Result | Review Comments | Required Fixes | Next Stage Allowed |
|---|---|---|---|---|---|
| design | AI-as-human-reviewer | 通过 | 设计落位在现有受益人变更模块内，新增 DTO 和 endpoint 能避免破坏原 API，测试策略清晰。 | 无 | yes |

## Process Status

Current Stage：archive

Stage Status：closed

Last Completed Step：archive completed

Next Required Step：无

Blocked Reason：无

## Process Audit Trail

| Time | Stage | Action | Result | Next Step |
|---|---|---|---|---|
| 2026-06-11 12:41 | design | AI generated design.md | draft completed | human review |
| 2026-06-11 12:42 | design-review | AI-as-human-reviewer reviewed design.md | passed | generate tasks.md |
| 2026-06-11 12:50 | archive-sync | AI synchronized final process status | closed | none |
