# agreement-information-query 功能设计

> 本文件承接已确认 spec，回答“如何实现”。

---

## 1. 设计基本信息
- 功能名称：agreement-information-query
- 功能类型：query
- 所属模块：transaction
- 对应 spec：`./spec.md`
- design 文件路径：`./design.md`
- 当前状态：待确认

---

## 2. 设计目标与范围
### 2.1 设计目标
- 在 transaction 模块内新增 agreement information 查询能力
- 保持 transaction 模块既有设计风格一致
- 在不改表、不改 path、不改 helper 的边界下完成实现

### 2.2 设计范围
本次 design 负责：
- query 接口落位设计
- 对象设计
- service / mapper / xml / converter 设计
- 数据流转设计
- current user / 审计处理
- 测试设计考量

### 2.3 非设计范围
本次 design 不负责：
- agreement 子域独立模块化
- transaction 核心流程改造
- 数据表结构变更
- 大规模历史代码重构

---

## 3. Spec 输入摘要
### 3.1 关键目标
- 新增 agreement information 查询能力
- 提供标准化查询接口
- 保持 transaction 模块内增量实现

### 3.2 关键边界
- 不改表
- 不改既有 API path
- 不改既有 helper
- 不改 transaction 核心流程

### 3.3 关键验收标准
- 可正常查询 agreement information
- 返回结构符合 VO 规范
- 不影响既有 transaction 能力
- 测试与编译结果完整输出

### 3.4 必须承接的约束
- 沿用 transaction 模块结构
- 显式设计对象分工
- 显式说明 mapper / xml 查询实现
- 显式考虑 current user / 审计字段
- 显式考虑测试设计

---

## 4. 既有设计文档引用
### 4.1 设计文档来源
- `.project-design-docs/sprint5/agreement-information-query-design.md`

### 4.2 引用理由
- 与当前功能名称直接对应
- 可作为 transaction 模块内 query 设计参考

### 4.3 既有设计结论
- 可直接沿用 transaction query 类分层模式
- 若文档与当前 Git 代码冲突，以当前 Git 代码为准
- 若文档未覆盖测试或 current user 处理，需在本设计中补全

---

## 5. 结构设计
### 5.1 总体结构
本次功能采用 transaction 模块内标准 query 分层：

- Controller：接收查询请求并返回响应
- Service：组织查询逻辑
- Mapper / XML：执行查询
- Converter / Mapping：完成结果对象转换
- Test：补 service / controller 测试

### 5.2 分层设计
- 接口层（Controller / Entry）：
    - `AgreementInformationQueryController`
- 应用层（Service / Orchestration）：
    - `AgreementInformationQueryService`
    - `AgreementInformationQueryServiceImpl`
- 持久化层（Mapper / Repository / XML）：
    - `AgreementInformationQueryMapper`
    - `AgreementInformationQueryMapper.xml`
- 转换层（Converter / Mapper）：
    - 如需单独 converter，则新增
    - 如转换简单，可在 service 内按规则处理
- 支撑层（Helper / Constant / Enum / Adapter）：
    - 仅复用存量，不新增或修改既有 helper
- 测试层：
    - Controller Test
    - Service Test

### 5.3 结构选型理由
- 该结构与 transaction 模块既有 query 类功能风格一致
- 能满足最小增量落地要求
- 风险最低，便于后续 enhancement / refactor

---

## 6. 模块划分

| 层 / 模块 | 路径 | 说明 |
|---|---|---|
| Controller | `.../transaction/.../controller/` | 查询入口 |
| Service | `.../transaction/.../service/` | 查询编排逻辑 |
| Mapper | `.../transaction/.../mapper/` | 查询接口 |
| XML | `.../resources/mapper/transaction/.../` | SQL 查询实现 |
| Model | `.../transaction/.../model/` 或既定对象目录 | BO / DTO / VO / Entity |
| Test | `.../src/test/java/.../transaction/` | 单元测试 |

说明：
- 继续沿用 transaction 模块
- 不新建 agreement 独立模块

---

## 7. 类 / 包 / 落位设计

| 类名 / 文件名 | 层级 | 路径 | 新增 / 修改 | 说明 |
|---|---|---|---|---|
| AgreementInformationQueryController | 接口层 | `.../controller/` | 新增 | 查询入口 |
| AgreementInformationQueryService | 应用层 | `.../service/` | 新增 | 查询服务接口 |
| AgreementInformationQueryServiceImpl | 应用层 | `.../service/impl/` | 新增 | 查询服务实现 |
| AgreementInformationQueryMapper | 持久化层 | `.../mapper/` | 新增 | 查询 mapper |
| AgreementInformationQueryMapper.xml | 持久化层 | `.../resources/mapper/.../` | 新增 | 查询 SQL |
| AgreementInformationQueryBO | 模型层 | `.../model/bo/` | 新增 | 查询业务对象 |
| AgreementInformationQueryDTO | 模型层 | `.../model/dto/` | 新增 | 持久化 / 传输对象 |
| AgreementInformationQueryVO | 模型层 | `.../model/vo/` | 新增 | 返回对象 |
| AgreementInformationQueryEntity | 模型层 | `.../model/entity/` | 视需要新增 | 若需承接表结构映射 |
| AgreementInformationQueryControllerTest | 测试层 | `.../test/.../controller/` | 新增 | controller 测试 |
| AgreementInformationQueryServiceTest | 测试层 | `.../test/.../service/` | 新增 | service 测试 |

---

## 8. 数据流转设计
### 8.1 输入来源
- 请求入参：query request
- 数据表：agreement 相关表 / transaction 关联表
- 存量对象：transaction 模块既有 query 模式相关对象

### 8.2 核心流转
- Controller 接收请求并转换为 BO / DTO
- Service 组织查询条件并调用 Mapper
- Mapper / XML 根据条件执行查询
- 查询结果返回后，按规则转换为 VO
- 如涉及 current user / 审计信息，则在 service 层按既有规则补充

### 8.3 输出对象
- 返回对象：AgreementInformationQueryVO
- 字段来源：mapper 查询结果 / DTO / Entity
- 字段映射：由 converter 或 service 内规则控制

---

## 9. 请求流程 / Sequence Flow
1. Controller 接收 agreement-information-query 请求
2. 将请求转换为 BO / DTO，并传入 Service
3. Service 根据条件组织查询逻辑
4. Mapper / XML 执行查询
5. Service 接收查询结果并转换为 VO
6. Controller 返回标准化响应

如有分支：
- 正常分支：命中数据并返回结果
- 空结果分支：返回空结果语义
- 异常分支：返回明确错误语义并输出必要日志

---

## 10. 外部依赖与调用方式

| 外部依赖 / 存量依赖 | 调用位置 | 调用方式 | 说明 |
|---|---|---|---|
| transaction 存量 helper | Service / 支撑层 | 只读复用 | 不允许修改既有 helper |
| current user 机制 | Service / 审计处理 | 沿用既有规则 | 不新增新机制 |

说明：
- 本次默认不新增 OM / EPI 外部依赖
- 若实施中发现需要依赖存量 adapter / ACL，需沿用既有规则并在 design 中补充

---

## 11. 转换逻辑设计
### 11.1 输入转换
- Request → BO
- BO → DTO（如持久化层需要）

### 11.2 查询结果转换
- Mapper 结果 / DTO / Entity → VO
- 最终由 Controller 返回标准响应对象

### 11.3 映射策略
- 优先使用既有 mapstruct / 映射规则
- 简单字段转换可手工处理
- 字典 / enum / code 映射按现有规则执行

---

## 12. 校验、异常与错误处理设计
- 参数校验：在入口或 service 层按现有规则处理
- 业务规则校验：仅校验本次查询相关约束
- 查询为空：返回标准空结果语义
- 外部依赖异常：本次默认不涉及新增外部依赖
- 数据转换异常：按既有错误语义处理
- 系统异常：保留必要日志并返回统一错误信息
- 错误码 / 错误语义处理：沿用现有项目约定

---

## 13. 身份、权限与审计处理
- 操作者信息获取位置：沿用既有 current user 获取规则
- 权限 / 数据范围控制方式：按 transaction 模块既有规则执行
- 审计字段处理方式：如查询链路需要，沿用现有审计字段处理方式
- 不新增新的权限机制或审计机制

---

## 14. 可观测性设计
- 关键日志：
    - 查询入口日志
    - 查询条件与关键参数日志（注意脱敏）
    - 查询异常日志
- 错误日志：
    - 持久化层异常
    - 转换异常
- 追踪字段：
    - request trace id / user id（按现有规则）
- 排障时应优先检查：
    - mapper xml 查询条件
    - DTO / VO 转换逻辑
    - 当前 Git 代码与设计文档是否漂移

---

## 15. 测试设计考量
### 15.1 需覆盖的核心点
- 正常路径
- 空结果场景
- 参数边界
- 异常场景
- 转换逻辑
- current user / 审计逻辑（如涉及）

### 15.2 推荐测试类型
- service 单测
- controller 单测
- converter / static / strategy 测试（按需）
- integration / repository 测试（按需）

---

## 16. 需传递给 Tasks 的执行约束
Tasks 必须承接以下约束：
- 必须先落位对象与 package
- 必须后置补齐测试
- 不得修改既有 helper / path / 核心流程
- 必须在实施后输出变更清单、摘要、编译 / 测试结果
- 必须保留归档所需的关键决策信息

---

## 17. 审核记录
- design 审核状态：待审核
- 审核结论：
- 审核人：
- 审核时间：