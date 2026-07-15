# UAW SDD Demo

本项目是用于验证 UAW-SDD 流程的 Spring Boot + Maven Demo。

## 环境要求

- 使用 Java 17 或更高版本编译
- Maven 3.9 或更高版本

`maven-surefire-plugin` 已启用动态 Agent 加载和 Byte Buddy 实验模式，使基于 Mockito 的测试可以在较新的本地 JDK 上运行，同时保持 Java 17 目标兼容性。较新 JDK 仍可能输出 Byte Buddy 关于 `sun.misc.Unsafe` 的兼容性 Warning，但不会导致当前测试失败。

## 运行测试

```bash
mvn test
```

## 启动应用

```bash
mvn spring-boot:run
```

## API 示例

### 创建保单信息变更工单

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

### 查询保单信息变更工单

```http
GET /api/work-orders/policy-info-change/{workOrderId}
```

响应包含只读字段 `changeSummary`，其值根据 `changeFieldType`、`oldValue` 和 `newValue` 生成。

### 创建保单受益人变更工单

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

### 创建保单受益人邮箱变更工单

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

### 创建资料申请工单

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
