# 功能级 Design

## 1. 设计基本信息

- 功能名称：policy-info-change-workorder
- 功能类型：submit
- 所属模块：policy / workorder
- 对应 spec：`./spec.md`
- design 文件路径：`./design.md`
- 当前状态：已确认（模拟确认）

## 2. Spec 输入摘要

本次设计基于以下已确认内容：

- 功能目标：新增保单信息变更工单创建与查询能力，并跑通 SDD 闭环。
- 变更范围：Spring Boot 工程、API、Service、Repository、Model、Test、Maven 配置。
- 不可变边界：不接真实数据库、不引入公司内网依赖、不生成 SDD Code Review HTML 报告。
- 验收标准：接口可用、核心校验生效、`mvn test` 通过、SDD 流程资产完整。
- 风险重点：环境预检、目录根定位、模拟确认与真实确认区分。

## 3. 设计目标与范围

### 3.1 设计目标

- 建立一个能被 Maven 直接测试的 Spring Boot 示例工程。
- 用最小业务闭环表达保单信息变更工单的提交、查询、校验和异常处理。
- 将真实构建失败和修复过程纳入 SDD Review / Auto-fix / Unit Test 记录。

### 3.2 设计范围

- 包结构与落位。
- 类设计。
- 数据流转。
- 异常处理。
- 测试设计。
- Maven 测试运行配置。

### 3.3 非设计范围

- 不设计真实数据库表。
- 不设计审批流。
- 不设计权限、租户、审计上下文。
- 不设计外部保单系统集成。

## 4. 既有设计文档引用

### 4.1 设计文档来源

- 未引用 `.project-design-docs/`：当前仓库未提供与本模拟功能直接匹配的设计文档。

### 4.2 引用理由

- 不适用。

### 4.3 既有设计结论

- 可直接沿用的设计：无。
- 需要调整的设计：无。
- 不再适用的设计：无。

## 5. 结构设计

### 5.1 总体结构

在 `uaw-sdd-demo/` 下创建独立 Spring Boot Maven 工程，包名为 `com.example.uawsdddemo`。功能按 Controller、Service、Repository、Model、Exception Handler 分层。

### 5.2 分层设计

- Controller：接收创建和查询请求，负责参数校验入口。
- Service：负责业务校验、重复提交判断、实体创建和响应转换。
- Repository：定义工单保存、按 ID 查询、待处理重复判断接口；本次以内存实现落地。
- DTO / Entity / Enum：表达请求、响应、工单实体、变更字段枚举、状态枚举。
- Exception Handler：统一处理参数错误、业务错误、未找到错误。
- Test：服务层测试和接口层 MockMvc 测试。

### 5.3 结构选型理由

- 分层足够表达常见后端 AI Coding 任务的主要落点。
- 内存仓储可以避免数据库建表和环境依赖干扰，聚焦 SDD 流程验证。
- 测试覆盖服务层和接口层，能暴露构建环境、Mock、校验、异常处理等 SDD 实操问题。

## 6. 模块划分

| 层 / 模块 | 路径 | 说明 |
|---|---|---|
| Maven 工程 | `uaw-sdd-demo/` | 独立 Spring Boot 示例工程 |
| Controller | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/` | API 入口 |
| Service | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/` | 业务编排 |
| Repository | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/` | 数据访问抽象与内存实现 |
| Model | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/` | DTO / Entity / Enum |
| Exception | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/exception/` | 业务异常 |
| Handler | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/handler/` | 统一异常响应 |
| Test | `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/` | 单元测试 |

## 7. 类 / 包 / 落位设计

| 类名 / 文件名 | 层级 | 路径 | 新增 / 修改 | 说明 |
|---|---|---|---|---|
| `UawSddDemoApplication` | Bootstrap | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/UawSddDemoApplication.java` | 新增 | Spring Boot 启动类 |
| `PolicyInfoChangeWorkOrderController` | Controller | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderController.java` | 新增 | 创建与查询接口 |
| `PolicyInfoChangeWorkOrderService` | Service | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java` | 新增 | 业务校验和响应转换 |
| `PolicyInfoChangeWorkOrderRepository` | Repository | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/PolicyInfoChangeWorkOrderRepository.java` | 新增 | 仓储接口 |
| `InMemoryPolicyInfoChangeWorkOrderRepository` | Repository | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/InMemoryPolicyInfoChangeWorkOrderRepository.java` | 新增 | 内存仓储实现 |
| `CreatePolicyInfoChangeWorkOrderRequest` | DTO | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/CreatePolicyInfoChangeWorkOrderRequest.java` | 新增 | 创建请求 |
| `PolicyInfoChangeWorkOrderResponse` | DTO | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/PolicyInfoChangeWorkOrderResponse.java` | 新增 | 工单响应 |
| `PolicyInfoChangeWorkOrder` | Entity | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/entity/PolicyInfoChangeWorkOrder.java` | 新增 | 工单实体 |
| `ChangeFieldType` | Enum | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/enums/ChangeFieldType.java` | 新增 | 可变更字段 |
| `WorkOrderStatus` | Enum | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/enums/WorkOrderStatus.java` | 新增 | 工单状态 |
| `BadRequestException` | Exception | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/exception/BadRequestException.java` | 新增 | 业务参数错误 |
| `NotFoundException` | Exception | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/exception/NotFoundException.java` | 新增 | 查询未命中 |
| `ApiExceptionHandler` | Handler | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/handler/ApiExceptionHandler.java` | 新增 | 统一错误响应 |
| `PolicyInfoChangeWorkOrderServiceTest` | Test | `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderServiceTest.java` | 新增 | 服务层测试 |
| `PolicyInfoChangeWorkOrderControllerTest` | Test | `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderControllerTest.java` | 新增 | 接口层测试 |

## 8. 数据流转设计

### 8.1 输入来源

- 请求入参：`CreatePolicyInfoChangeWorkOrderRequest`
- 上游接口：无
- 数据表：无
- 存量对象：无

### 8.2 核心流转

- Controller 接收 JSON 请求并触发 Bean Validation。
- Controller 调用 Service 创建工单。
- Service 校验 `oldValue` 与 `newValue` 是否一致。
- Service 构造 `PolicyInfoChangeWorkOrder`，默认状态为 `SUBMITTED`。
- Service 调用 Repository 判断是否存在待处理重复工单。
- Repository 使用 `ConcurrentHashMap` 保存和查询。
- Service 将 Entity 转换为 Response。
- Controller 返回响应。

### 8.3 输出对象

- 返回对象：`PolicyInfoChangeWorkOrderResponse`
- 字段来源：请求字段、系统生成 ID、系统生成状态、系统生成创建时间。
- 字段映射说明：Service 内部手工转换。

## 9. 请求流程 / Sequence Flow

1. `POST /api/work-orders/policy-info-change` 接收创建请求。
2. Bean Validation 校验必填字段。
3. Service 校验新旧值差异。
4. Service 构造待处理工单。
5. Repository 检查重复待处理工单。
6. Repository 保存工单。
7. Service 返回响应。
8. `GET /api/work-orders/policy-info-change/{workOrderId}` 按 ID 查询并返回响应。

分支说明：

- 正常分支：创建成功返回 201，查询成功返回 200。
- 异常分支：新旧值一致或重复提交返回 400。
- 空结果分支：查询不到工单返回 404。
- 降级分支：无。

## 10. 外部依赖与调用方式

| 外部依赖 / 存量依赖 | 调用位置 | 调用方式 | 说明 |
|---|---|---|---|
| 无 | 无 | 无 | 本次不涉及外部系统 |

## 11. 转换逻辑设计

### 11.1 输入转换

- Request → Entity：Service 手工创建 Entity。
- BO → DTO：不适用。

### 11.2 查询结果转换

- Entity → Response：Service 内部 `toResponse` 手工转换。

### 11.3 mapstruct / 手工转换

- 使用 mapstruct 的场景：无。
- 使用手工转换的场景：当前对象数量少，手工转换更直接。
- 不能直接复用的场景：无存量 converter 可复用。

## 12. 异常处理设计

- 参数校验异常：`MethodArgumentNotValidException` 转换为 400，message 为 `request validation failed`。
- 查询为空：Service 抛出 `NotFoundException`，统一转换为 404。
- 外部接口异常：不适用。
- 数据转换异常：不做专门处理，保持默认系统异常。
- 系统异常：本次不实现全局兜底，避免示例工程过度扩展。

## 13. 上下文依赖 / 审计字段处理

- 当前用户信息：由请求字段 `requester` 模拟提供。
- 上下文字段：无 tenant / channel。
- 审计字段：`createdAt`。
- createdBy / updatedBy：不实现，原因是本次不接入真实用户上下文。

## 14. 测试设计考量

### 14.1 需覆盖的核心点

- 正常创建。
- 新旧值一致。
- 重复待处理工单。
- 查询存在工单。
- 查询不存在工单。
- 请求参数校验失败。
- Controller 异常映射。

### 14.2 测试实现

- 使用 JUnit4 + Mockito，原因是当前 UAW testing 规则偏向 JUnit4 命名和 Mock 风格。
- 使用 MockMvc standalone 验证 Controller。
- 使用 Mockito Mock Repository 验证 Service。

### 14.3 已知测试环境风险

- Maven 当前使用 Java 26，Spring Boot 3.3.5 管理的 Byte Buddy 版本默认不支持 Java 26 class file。
- 需要在 Surefire 中配置 `-Dnet.bytebuddy.experimental=true`，或将 Maven 运行 JDK 固定为 Java 17。

# Process Status

- Current Stage：Archive
- Stage Status：archived
- Last Completed Step：Design 已确认并被 Tasks / Implementation 使用
- Next Required Step：无，已归档
- Human Confirmation Required：no
- Allowed Next Action：作为后续同类模拟设计参考
- Forbidden Next Action：不得作为真实生产架构设计直接套用
- Updated At：2026-05-28 17:06:26 +0800

# Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-28 16:40:00 +0800 | Design | 基于 spec 设计工程结构与功能分层 | spec.md、代码工程目标 | design.md | 通过，模拟确认 | Tasks |
| 2026-05-28 17:06:26 +0800 | Design | 回写测试环境风险和内存仓储边界 | 首次测试失败、最终实现 | design.md | 通过，进入归档 | Archive |
