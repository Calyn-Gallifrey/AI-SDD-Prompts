# design.md - i-need-document-workorder

## 1. Design Summary

新增独立的 I need document 工单模块，落位在现有 demo 的 `controller`、`service`、`repository`、`model` 分层下。该功能不修改既有保单信息变更或受益人变更工单。下游平台提交在 demo 中通过 `INeedDocumentDownstreamClient` 模拟。

## 2. API Design

### 2.1 Endpoint

```http
POST /api/work-orders/i-need-document
Content-Type: application/json
```

### 2.2 Request

DTO：`CreateINeedDocumentWorkOrderRequest`

| Field | Type | Validation | Description |
|---|---|---|---|
| policyNo | String | @NotBlank | 保单号 |
| customerName | String | @NotBlank | 客户姓名 |
| requestType | INeedDocumentRequestType | @NotNull | QUERY_DOCUMENT / SEND_DOCUMENT |
| documentTypes | List<String> | @NotEmpty | 文档类型列表 |
| deliveryEmail | String | @Email | SEND_DOCUMENT 时必填 |
| requester | String | @NotBlank | 坐席 |

### 2.3 Response

DTO：`INeedDocumentWorkOrderResponse`

| Field | Description |
|---|---|
| workOrderId | UAW 工单号 |
| policyNo | 保单号 |
| customerName | 客户姓名 |
| requestType | 请求类型 |
| documentTypes | 归一化后的文档类型列表 |
| deliveryEmail | 归一化后的发送邮箱 |
| downstreamSubmissionId | 下游提交号 |
| status | 工单状态 |
| createdAt | 创建时间 |

## 3. Model Design

### 3.1 Enum

`INeedDocumentRequestType`：
- `QUERY_DOCUMENT`
- `SEND_DOCUMENT`

### 3.2 Entity

`INeedDocumentWorkOrder` 字段：
- workOrderId
- policyNo
- customerName
- requestType
- documentTypes
- deliveryEmail
- requester
- downstreamSubmissionId
- status
- createdAt

工厂方法：

```java
submitted(policyNo, customerName, requestType, documentTypes, deliveryEmail, requester, downstreamSubmissionId)
```

## 4. Service Design

新增 `INeedDocumentWorkOrderService#create(CreateINeedDocumentWorkOrderRequest request)`。

处理流程：
1. 归一化并校验 `documentTypes`，去除每个文档类型前后空格，不允许空白项。
2. `requestType=SEND_DOCUMENT` 时校验 `deliveryEmail` 必填，并执行 trim + lower-case。
3. `requestType=QUERY_DOCUMENT` 时将空白 `deliveryEmail` 归一化为 `null`。
4. 调用 `INeedDocumentDownstreamClient.submit(...)` 获取下游提交号。
5. 创建 `INeedDocumentWorkOrder`，状态为 `SUBMITTED`。
6. 调用 repository 保存。
7. 转换为 response 返回。

## 5. Downstream Client Design

接口：`INeedDocumentDownstreamClient`

```java
String submit(INeedDocumentWorkOrderSubmission submission)
```

demo 实现：`InMemoryINeedDocumentDownstreamClient`

规则：
- 不发起真实 HTTP 调用。
- 返回 `DOC-` 前缀的随机提交号。

## 6. Repository Design

接口：`INeedDocumentWorkOrderRepository`

方法：
- `INeedDocumentWorkOrder save(INeedDocumentWorkOrder workOrder)`
- `Optional<INeedDocumentWorkOrder> findById(String workOrderId)`

demo 实现：`InMemoryINeedDocumentWorkOrderRepository`

## 7. Test Design

Testing Profile：`Legacy-Mockito`

选择依据：
- 既有 demo 测试以 JUnit4 `@RunWith(MockitoJUnitRunner.class)` 和 Mockito 为主。
- `pom.xml` 通过 JUnit Vintage 支持 JUnit4 测试执行。
- 当前 demo 未引入 UAW 单元测试工具类，按 No-UAW-Util 处理。

不适用规则：
- UAW 测试工具类规则不适用。
- JUnit5-only 规则不适用。

测试框架风险：
- JUnit Vintage 可支撑当前测试，但真实项目应统一测试框架策略。
- 新 JDK 下 Mockito / Byte Buddy 可能出现兼容 warning，需要在 Unit Test Summary 中记录。

是否需要补充依赖：no

覆盖：
- Service 成功提交 QUERY_DOCUMENT 工单。
- Service 成功提交 SEND_DOCUMENT 工单并归一化邮箱。
- Service 拦截 SEND_DOCUMENT 缺少邮箱。
- Service 拦截空白文档类型。
- Controller 成功请求返回 HTTP 201。
- Controller validation 对缺少必填字段返回 HTTP 400。
- Repository 保存和查询。

## 8. Human Review

| Review Stage | Reviewer Role | Review Result | Review Comments | Required Fixes | Next Stage Allowed |
|---|---|---|---|---|---|
| design | AI-as-human-reviewer | 通过 | 设计保持独立模块边界，demo 下游 client 明确不接真实外部系统，测试策略清晰。 | 无 | yes |

## Process Status

Current Stage：archive

Stage Status：archived

Last Completed Step：archive completed

Next Required Step：无

Blocked Reason：无

## Process Audit Trail

| Time | Stage | Action | Result | Next Step |
|---|---|---|---|---|
| 2026-06-11 14:37 | design | AI generated design.md | draft completed | human review |
| 2026-06-11 14:38 | design-review | AI-as-human-reviewer reviewed design.md | passed | generate tasks.md |
| 2026-06-11 14:43 | archive-sync | AI synchronized final process status | archived | none |
