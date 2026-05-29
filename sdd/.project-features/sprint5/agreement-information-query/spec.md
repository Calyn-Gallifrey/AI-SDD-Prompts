# agreement-information-query 功能规格

> 旧版样板说明：本文件生成于 2026-05-28 UAW-SDD 体系更新前，仅作为历史功能资产和旧版 query 类案例参考。
> 它不完整体现新版强制闭环，包括 Process Status / Process Audit Trail、`SDD_TASK_CODE_REVIEW`、Review-driven Auto-fix 和 Unit Test Summary。
> 新功能不得直接照搬本文件作为新版流程样板，应以 `.project-ai/context/1.index.md` 和当前模板为准。

> 本文件是 agreement-information-query 功能的正式规格文件。  
> 本文件负责定义：目标、边界、双基线、规则装配结果、验收标准，以及 design 必须承接的约束。

---

## 1. 基本信息
- 功能名称：agreement-information-query
- 功能类型：query
- 所属模块：transaction
- 所在 sprint：sprint5
- 当前状态：待确认
- spec 文件路径：`./spec.md`

## 2. 任务来源 / Proposal 输入摘要
### 2.1 原始提案摘要
- 功能目标：在 transaction 现有模块中新增 agreement information 查询能力，支持按指定条件查询 agreement information 列表或明细结果
- 变更范围：
  - 新增 agreement information 查询接口
  - 新增查询入参对象
  - 新增返回对象
  - 新增 mapper / xml 查询逻辑
  - 新增 service / controller
  - 补充必要单元测试
- 禁止变更：
  - 不改资料表结构
  - 不改既有 API path
  - 不改既有 helper
  - 不改 transaction 现有核心提交流程
  - 不改既有对外接口契约
  - 不做 agreement 独立模块化重构
- 输出位置：`.project-features/sprint5/agreement-information-query/`

### 2.2 Proposal 文件引用
- 当前提案文件路径：`./proposal-input.md`
- 是否基于历史功能继续演进：否

## 3. Context Assembly（上下文装配）
### 3.1 Base Context
- UAW 既定目录结构
- transaction 模块现有语义与分层约定
- `.project-ai/context/1.index.md` 所定义的装配逻辑
- 当前 Git 代码扫描范围
- `.project-design-docs` 中相近功能设计文档（如存在）

### 3.2 Conditional Context
- 模块上下文：transaction
- 领域上下文：agreement information 查询
- 兼容性上下文：不得破坏 transaction 既有核心流程
- enhancement / refactor 特殊上下文：本次不适用

### 3.3 上下文装配结论
- 本次任务是 transaction 模块内的增量查询能力建设
- 本次任务必须优先沿用 transaction 现有模块结构和 query 类功能风格
- agreement information 当前作为 transaction 模块中的一个查询能力处理，而非独立子域

## 4. Rules Assembly（规则装配）
### 4.1 结构与落位
- transaction 模块包结构规则
- 类与文件落位规则

### 4.2 契约与接口
- 后端 API 接口编写规则
- 请求 / 响应契约规则

### 4.3 持久化与查询
- MyBatis ORM 规则
- Mapper / XML 查询规则

### 4.4 对象模型与边界
- BO / DTO / VO / Entity 生成规则
- 对象边界分层规则

### 4.5 转换与映射
- MapStruct / 映射规则
- 字段与对象转换规则

### 4.6 身份、权限与审计
- current user 获取规则
- 审计字段处理规则

### 4.7 外部依赖与防腐层
- 本次默认不涉及新增 OM / EPI 集成
- 如实现中发现需调用存量外部依赖，必须沿用既有防腐层规则

### 4.8 校验、异常与错误语义
- 参数校验规则
- 空结果 / 异常语义规则

### 4.9 可观测性与运维友好性
- 基本日志与排障信息输出规则

### 4.10 测试与质量门禁
- service 单测规则
- controller 单测规则
- 必要时的 converter / static 测试规则

### 4.11 兼容、迁移与演进
- 保持 transaction 核心流程兼容
- 为后续 enhancement / refactor 预留归档资产

## 5. 历史功能资产引用（enhancement / refactor 必填）
本次任务为新任务，不基于历史功能资产继续演进。  
本节不适用。

## 6. 双基线定义
### 6.1 知识基线
来源：
- 已装配 context
- 已装配 rules
- transaction 模块既有约定
- 既有 query 类功能设计风格

结论：
- agreement-information-query 必须作为 transaction 模块内的增量查询能力落地
- 本次任务必须遵守“最小侵入、最小改动、复用现有结构”的原则
- 不允许借本次任务顺手推进大规模模块重构

### 6.2 当前 Git 代码基线
扫描范围：
- `<repo-root>/src/main/java/.../transaction/`
- `<repo-root>/src/main/resources/mapper/transaction/`
- `<repo-root>/src/test/java/.../transaction/`

扫描结果（待实际仓库确认）：
- 现有 transaction 模块已有 query 类 controller / service / mapper / xml 结构
- 现有 helper / converter / enum 可供复用
- 现有测试结构可作为本次测试落位参考
- 现有 API path 与 transaction 核心流程不得破坏

### 6.3 双基线差异
- 当前无明确知识基线与实物基线冲突信息
- 若后续扫描发现差异，以当前 Git 代码为准，并在 design 中明确标注调整策略

## 7. 功能目标
- 在 transaction 模块中新增 agreement information 查询能力
- 提供标准化查询接口，支持列表或明细结果返回
- 沿用现有 transaction 模块的分层、对象命名与查询实现风格
- 保持现有核心流程与对外契约稳定

## 8. 存量现状
### 8.1 业务存量
- transaction 模块已有既定查询类能力
- 系统中存在 agreement information 相关数据来源
- 当前缺少独立的 agreement information 查询能力出口

### 8.2 代码存量
- 已存在 transaction 模块 package 结构
- 已存在 query 类 controller / service / mapper / xml 实现样板
- 已存在 current user / 审计字段处理方式
- 已存在测试目录与测试风格

## 9. 本次变更范围
### 9.1 新增内容
- 新增 agreement-information-query 接口
- 新增 BO / DTO / VO
- 新增 service / controller
- 新增 mapper / xml 查询逻辑
- 新增必要单元测试

### 9.2 修改内容
- 如需接入现有 transaction 查询流程，只允许做最小必要修改

### 9.3 复用内容
- 复用 transaction 模块现有分层
- 复用现有 API 设计风格
- 复用现有 mapper / xml 风格
- 复用 current user 与审计处理方式

### 9.4 不在本次范围内的内容
- agreement 独立模块化
- 数据表结构调整
- 既有 helper / path / 核心流程重构
- 对外接口契约变更

## 10. Non-goals / 不可变边界
- 不改资料表结构
- 不改既有 API path
- 不改既有 helper
- 不改 transaction 核心提交流程
- 不改既有对外接口契约
- 不借本次任务推进 agreement 子域拆分

## 11. Domain Mapping / 字段来源与领域映射

| 字段 / 领域对象 | 来源（表 / 接口 / 存量类） | 目标对象 | 备注 |
|---|---|---|---|
| agreement 基础信息 | agreement 相关表 / 存量查询结果 | AgreementInformationQueryVO | 需以实际表结构和 mapper 结果为准 |
| 查询条件 | 请求入参 | AgreementInformationQueryBO / DTO | 由 controller / service 接收并下传 |
| 审计 / 操作者相关信息 | current user / 审计字段 | service / query 上下文 | 仅按既有规则补充，不新增新机制 |

## 12. 验收标准（AC）
### 12.1 正常路径
- 可通过新增接口发起 agreement information 查询
- 返回结构符合既定 VO 规范
- 查询逻辑可在 transaction 模块内正常运行

### 12.2 边界场景
- 查询条件为空或部分缺失时，行为符合既有接口约定
- 无结果时返回语义清晰，不抛出不必要异常

### 12.3 异常场景
- 参数非法时有明确校验结果
- 查询过程异常时有明确错误语义和日志记录

### 12.4 兼容场景
- 不影响 transaction 现有核心提交流程
- 不影响既有 query 类能力
- 不破坏既有 API path 和既有 helper 依赖

## 13. 风险识别
### 13.1 技术风险
- 当前若 agreement information 查询需跨多表或复杂条件，Mapper / XML 复杂度可能上升
- 若存量 query 样板并不能完全覆盖 agreement 场景，需谨慎扩展

### 13.2 兼容风险
- 若误改 transaction 核心 helper、既有 path 或核心提交流程，会带来不必要连带影响
- 若查询复用了不合适的存量对象，可能导致字段语义混乱

### 13.3 交付风险
- 若当前仓库中实际代码结构与预想不一致，design 阶段需及时修正落位方案
- 若测试覆盖不足，容易在 query 边界场景出问题

### 13.4 风险重点（供 design 引用）
- 严禁突破“不改表 / 不改 path / 不改 helper / 不改核心流程”的边界
- 需显式设计 mapper / xml 查询与对象转换，避免实现时临时拼接
- 需补齐最小必要测试，避免把 query 做成只能跑通 happy path 的半成品

## 14. 回滚策略
若实施失败或验收不通过：
- 回退本次新增 controller / service / mapper / xml / object / test 文件
- 恢复到无 agreement-information-query 能力的 transaction 模块状态
- 不触碰既有核心流程与对外接口，保证回滚成本最小

## 15. 需传递给 Design 的约束
Design 阶段必须回答：

- 类与包如何落位
- 请求链路如何设计
- 数据访问如何设计
- 外部依赖如何接入（若后续发现存在）
- 异常如何处理
- 测试如何覆盖
- performance / mapper 复杂度风险如何控制

Design 阶段不得违反：

- 本 spec 的范围定义
- 本 spec 的边界约束
- 本 spec 的验收标准

## 16. 审核记录
- 审核状态：待审核
- 审核意见：
- 审核人：
- 审核时间：
- 修订记录：
  - v1：基于 proposal 生成初版 spec
