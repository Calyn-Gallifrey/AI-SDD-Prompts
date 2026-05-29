# 功能级 Design

## 1. 设计基本信息

- 功能名称：policy-beneficiary-change-workorder
- 功能类型：submit
- 所属模块：policy / workorder
- 对应 spec：`./spec.md`
- design 文件路径：`./design.md`
- 当前状态：已确认

## 2. Spec 输入摘要

本次设计基于以下已确认内容：

- 功能目标：新增受益人变更工单提交接口。
- 变更范围：API、Service、Repository、DTO、Entity、Enum、Test。
- 不可变边界：不接 DB、不改已有接口、不生成 SDD 内部 HTML review。
- 验收标准：创建成功、比例校验、重复提交校验、证件号脱敏、测试通过。
- 风险重点：敏感字段脱敏、重复提交原子性、不破坏现有接口。

## 3. 设计目标与范围

### 3.1 设计目标

- 在现有 demo 工程中新增独立的受益人变更工单能力。
- 保持与现有保单信息变更工单相同的 Controller / Service / Repository 分层风格。
- 避免明文证件号出现在响应对象中。
- 仓储层提供原子化保存方法，避免明显并发重复提交窗口。

### 3.2 设计范围

- 包结构与落位
- 类设计
- 数据流转
- 转换逻辑
- 异常处理
- 测试设计考量

### 3.3 非设计范围

- 不设计数据库表。
- 不设计审批流程。
- 不设计查询详情接口。
- 不设计权限系统。

## 4. 既有设计文档引用

### 4.1 设计文档来源

- 无 `.project-design-docs/` 参考。
- 参考现有 `policy-info-change` demo 代码风格。

### 4.2 引用理由

- 同属 policy / workorder。
- 同为 submit 类工单创建。
- 可复用 Controller / Service / Repository 分层风格。

### 4.3 既有设计结论

- 可直接沿用的设计：独立 Controller、Service、Repository、DTO、Entity、Enum。
- 需要调整的设计：重复提交保存改为仓储层原子方法。
- 不再适用的设计：信息变更字段枚举不复用，新增受益人关系枚举。

## 5. 结构设计

### 5.1 总体结构

在 `com.example.uawsdddemo` 下新增 beneficiary-change 相关类，保持现有普通分层结构：

- controller
- service
- repository
- model.dto
- model.entity
- model.enums

### 5.2 分层设计

- Controller：新增 `PolicyBeneficiaryChangeWorkOrderController`，只处理请求入口、Bean Validation 和响应状态。
- Service：新增 `PolicyBeneficiaryChangeWorkOrderService`，处理比例校验、实体创建、保存结果映射和证件号脱敏。
- Repository：新增 `PolicyBeneficiaryChangeWorkOrderRepository`，提供 `saveSubmittedIfAbsent`。
- Entity：新增 `PolicyBeneficiaryChangeWorkOrder`。
- Enum：新增 `BeneficiaryRelationType`，复用 `WorkOrderStatus`。
- Test：新增 Service / Controller 测试。

### 5.3 结构选型理由

- 与当前 demo 工程既有结构保持一致。
- 避免把受益人变更逻辑混入保单信息变更类。
- 原子保存由 Repository 负责，更贴近重复提交控制职责。

## 6. 模块划分

| 层 / 模块 | 路径 | 说明 |
|---|---|---|
| Controller | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/` | API 入口 |
| Service | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/` | 业务逻辑 |
| Repository | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/` | 内存仓储与重复提交控制 |
| DTO | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/` | 请求响应对象 |
| Entity | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/entity/` | 工单实体 |
| Enum | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/enums/` | 受益人关系枚举 |
| Test | `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/` | 单元测试 |

## 7. 类 / 包 / 落位设计

| 类名 / 文件名 | 层级 | 路径 | 新增 / 修改 | 说明 |
|---|---|---|---|---|
| `PolicyBeneficiaryChangeWorkOrderController` | Controller | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyBeneficiaryChangeWorkOrderController.java` | 新增 | 创建接口 |
| `PolicyBeneficiaryChangeWorkOrderService` | Service | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyBeneficiaryChangeWorkOrderService.java` | 新增 | 业务校验和响应转换 |
| `PolicyBeneficiaryChangeWorkOrderRepository` | Repository | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/PolicyBeneficiaryChangeWorkOrderRepository.java` | 新增 | 仓储接口 |
| `InMemoryPolicyBeneficiaryChangeWorkOrderRepository` | Repository | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/InMemoryPolicyBeneficiaryChangeWorkOrderRepository.java` | 新增 | 内存实现 |
| `CreatePolicyBeneficiaryChangeWorkOrderRequest` | DTO | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/CreatePolicyBeneficiaryChangeWorkOrderRequest.java` | 新增 | 创建请求 |
| `PolicyBeneficiaryChangeWorkOrderResponse` | DTO | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/PolicyBeneficiaryChangeWorkOrderResponse.java` | 新增 | 创建响应 |
| `PolicyBeneficiaryChangeWorkOrder` | Entity | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/entity/PolicyBeneficiaryChangeWorkOrder.java` | 新增 | 工单实体 |
| `BeneficiaryRelationType` | Enum | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/enums/BeneficiaryRelationType.java` | 新增 | 关系枚举 |
| `PolicyBeneficiaryChangeWorkOrderServiceTest` | Test | `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/PolicyBeneficiaryChangeWorkOrderServiceTest.java` | 新增 | Service 测试 |
| `PolicyBeneficiaryChangeWorkOrderControllerTest` | Test | `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyBeneficiaryChangeWorkOrderControllerTest.java` | 新增 | Controller 测试 |

## 8. 数据流转设计

### 8.1 输入来源

- 请求入参：`CreatePolicyBeneficiaryChangeWorkOrderRequest`
- 上游接口：无
- 数据表：无
- 存量对象：`WorkOrderStatus`

### 8.2 核心流转

- Controller 接收 JSON 请求。
- Bean Validation 校验必填字段。
- Service 校验 `benefitRatio`。
- Service 构建 `PolicyBeneficiaryChangeWorkOrder`。
- Repository 执行 `saveSubmittedIfAbsent`。
- Service 将 Entity 转为 Response，并对证件号脱敏。

### 8.3 输出对象

- 返回对象：`PolicyBeneficiaryChangeWorkOrderResponse`
- 字段来源：请求字段、系统生成 ID、系统生成状态、系统生成创建时间。
- 字段映射说明：Service 手工转换。

## 9. 请求流程 / Sequence Flow

1. Controller 接收 `POST /api/work-orders/policy-beneficiary-change`。
2. Spring Validation 校验必填字段。
3. Service 校验受益比例范围。
4. Service 构造工单实体。
5. Repository 原子保存，若发现重复则返回空。
6. Service 将重复提交转为 `BadRequestException`。
7. Service 转换响应并脱敏证件号。
8. Controller 返回 201。

分支：

- 正常分支：创建成功。
- 异常分支：比例非法、重复提交。
- 空结果分支：不适用，本次不提供查询接口。
- 降级分支：无。

## 10. 外部依赖与调用方式

| 外部依赖 / 存量依赖 | 调用位置 | 调用方式 | 说明 |
|---|---|---|---|
| 无 | 无 | 无 | 本次不涉及外部系统 |

## 11. 转换逻辑设计

### 11.1 输入转换

- Request → Entity：Service 手工创建。

### 11.2 查询结果转换

- Entity → Response：Service 手工转换。
- `beneficiaryIdNo` → `beneficiaryIdNoMasked`：Service 内部脱敏。

### 11.3 mapstruct / 手工转换

- 使用 mapstruct 的场景：无。
- 使用手工转换的场景：对象少、逻辑包含脱敏，手工转换更直接。
- 不能直接复用的场景：不复用保单信息变更响应对象，避免语义混乱。

## 12. 异常处理设计

- 参数校验异常：由现有 `ApiExceptionHandler` 返回 400。
- 查询为空：不适用。
- 重复提交：Service 抛 `BadRequestException`。
- 数据转换异常：不专门捕获。
- 系统异常：沿用现有 demo 行为。

## 13. 上下文依赖 / 审计字段处理

- 当前用户信息：由请求字段 `requester` 模拟。
- 审计字段：`createdAt`。
- createdBy / updatedBy：本次不实现。

## 14. 测试设计考量

### 14.1 需覆盖的核心点

- 创建成功。
- 受益比例小于 1。
- 受益比例大于 100。
- 重复提交。
- 请求必填字段缺失。
- Controller 业务异常映射。
- 证件号脱敏。

### 14.2 测试规则选择

- 使用当前 demo 工程既有 JUnit4 + Mockito 风格。
- 不强行切换 JUnit5。
- 不引入 UAW 内部工具类。

## 15. 代理人工审核记录

| Time | Stage | Reviewer Role | Result | Comment |
|---|---|---|---|---|
| 2026-05-29 12:20:03 +0800 | Design | Codex 扮演人类审核 | 通过 | Design 承接 Spec，类落位、数据流和异常处理清晰 |

# Process Status（强制｜流程闸门）

- Current Stage：Archive
- Stage Status：archived
- Last Completed Step：archive.md 已生成并完成代理最终审核
- Next Required Step：流程复盘与问题确认
- Human Confirmation Required：no（本轮由用户授权 Codex 扮演人类审核）
- Allowed Next Action：检查归档结果，确认是否要调整 SDD 体系模板
- Forbidden Next Action：未经用户确认直接修改 SDD 体系模板
- Updated At：2026-05-29 12:34:45 +0800

# Process Audit Trail（强制｜过程审核轨迹）

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-29 12:20:03 +0800 | Design | 根据 spec 生成 Design | spec.md、当前代码扫描 | design.md | 通过代理审核 | Tasks |
| 2026-05-29 12:34:45 +0800 | Archive | 同步最终流程状态 | 全部 SDD 资产和代码 | archive.md | 通过代理审核 | Done |
