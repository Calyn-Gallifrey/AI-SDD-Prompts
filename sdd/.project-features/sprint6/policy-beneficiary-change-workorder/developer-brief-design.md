# 开发个人简要设计

## 1. BA 需求理解

新增一个“保单受益人变更工单”提交能力。用户提交保单号、受益人信息和受益比例后，系统生成一张待处理工单。该需求用于验证真实迭代中“开发先写简要设计，再交给内网 AI 生成 proposal 并启动 SDD”的完整链路。

## 2. API 设计

### 新增接口

- Method：`POST`
- Path：`/api/work-orders/policy-beneficiary-change`
- Content-Type：`application/json`

### 请求入参

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| policyNo | String | 是 | 保单号 |
| beneficiaryName | String | 是 | 受益人姓名 |
| beneficiaryIdNo | String | 是 | 受益人证件号 |
| beneficiaryRelation | Enum | 是 | 受益人与投保人关系：SPOUSE / CHILD / PARENT / OTHER |
| benefitRatio | Integer | 是 | 受益比例，范围 1-100 |
| requester | String | 是 | 提交人 |

### 响应出参

| 字段 | 类型 | 说明 |
|---|---|---|
| workOrderId | String | 工单号 |
| policyNo | String | 保单号 |
| beneficiaryName | String | 受益人姓名 |
| beneficiaryIdNoMasked | String | 脱敏后的证件号 |
| beneficiaryRelation | Enum | 受益人与投保人关系 |
| benefitRatio | Integer | 受益比例 |
| requester | String | 提交人 |
| status | Enum | 工单状态，默认 SUBMITTED |
| createdAt | Instant | 创建时间 |

## 3. 业务逻辑

1. Controller 接收请求并做 Bean Validation。
2. Service 校验 `benefitRatio` 必须在 1-100 范围内。
3. Service 构建受益人变更工单实体，默认状态为 `SUBMITTED`。
4. Repository 保存工单前检查重复提交。
5. 重复提交判断口径：同一保单号 + 同一受益人证件号 + `SUBMITTED` 状态。
6. 若重复，返回 400：`submitted duplicate policy beneficiary change work order exists`。
7. 保存成功后返回响应，证件号只返回脱敏值。

## 4. 映射逻辑

- `CreatePolicyBeneficiaryChangeWorkOrderRequest` → `PolicyBeneficiaryChangeWorkOrder`
- `PolicyBeneficiaryChangeWorkOrder` → `PolicyBeneficiaryChangeWorkOrderResponse`
- 证件号脱敏规则：长度小于等于 4 时全部返回 `****`；长度大于 4 时仅保留后 4 位。

## 5. 牵连改动

- 新增 Controller。
- 新增 Service。
- 新增 Repository 接口与内存实现。
- 新增 DTO / Entity / Enum。
- 复用现有 `WorkOrderStatus`、`BadRequestException`、`NotFoundException`、`ApiExceptionHandler`。
- 新增 Service 单元测试。
- 新增 Controller 单元测试。

## 6. 禁止变更

- 不接真实数据库。
- 不改已有保单信息变更工单接口。
- 不引入前端。
- 不修改 SDD 体系文件。
- 不生成 SDD 内部 Code Review HTML 报告。

## 7. 开发个人风险判断

- 证件号属于敏感信息，响应必须脱敏。
- 内存仓储只用于流程验证，不具备生产持久化能力。
- 重复提交检查需要尽量做成仓储层原子操作，避免明显并发窗口。

## 8. 代理人工审核记录

- 审核人角色：Codex 扮演开发 / Reviewer
- 审核结论：通过，允许进入 proposal 生成
- 审核时间：2026-05-29 12:20:03 +0800
- 备注：本审核用于 SDD 流程完整性模拟，不代表真实生产审批。
