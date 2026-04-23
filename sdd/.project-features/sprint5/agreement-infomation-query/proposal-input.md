# 功能提案入口

## 1. 任务基本信息
- 功能名称：agreement-information-query
- 功能类型：query
- 所属模块：transaction
- 所在 sprint：sprint5
- 当前任务状态：新任务

## 2. 任务目标
### 2.1 一句话目标
在 transaction 现有模块中新增 agreement information 查询能力，支持按指定条件查询 agreement information 列表或明细。

### 2.2 业务价值 / 触发原因
当前 transaction 模块缺少面向 agreement information 的独立查询能力，导致相关数据获取依赖存量逻辑拼接或人工定位，复用性差、可维护性差。本次任务目标是在不破坏 transaction 现有核心流程的前提下，补齐标准查询能力。

### 2.3 预期结果
完成后，transaction 模块中应具备独立的 agreement-information-query 查询接口、查询 service、查询 mapper/xml 及对应对象模型，并补齐必要测试与归档资产。

## 3. 任务识别维度
### 3.1 变更类型
- 新增

### 3.2 技术能力面
- 契约与接口（Contract & Interface）
- 持久化与查询（Persistence & Query）
- 对象模型与边界（Object Model & Boundary）
- 转换与映射（Transformation & Mapping）
- 身份 / 权限 / 审计（Identity / Auth / Audit）
- 测试与质量门禁（Testing & Quality Gates）
- 兼容 / 迁移 / 演进（Compatibility / Migration / Evolution）

### 3.3 变更范围
- 新增 agreement information 查询接口
- 新增查询入参对象
- 新增返回对象
- 新增 mapper / xml 查询逻辑
- 新增 service / controller
- 补充必要单元测试

### 3.4 禁止变更 / 不可变边界
- 不改资料表结构
- 不改既有 API path
- 不改既有 helper
- 不改 transaction 现有核心提交流程
- 不改既有对外接口契约
- 不做 agreement 独立模块化重构

## 4. AI 知识底座路径
- AI 知识底座根目录：`.project-ai/`
- 索引文件：`.project-ai/context/index.md`
- 上下文目录：`.project-ai/context/`
- 规则目录：`.project-ai/rules/`
- 模板目录：`.project-ai/templates/`

说明：
1. AI 必须先读取 `index.md`
2. 再由 `index.md` 决定装配哪些 context / rules / templates
3. 不得跳过 index 直接盲目生成 spec / design / tasks

## 5. 当前代码现状扫描范围
### 5.1 代码仓根目录
- `<repo-root>/`

### 5.2 优先扫描目录
- `<repo-root>/src/main/java/.../transaction/`
- `<repo-root>/src/main/resources/mapper/transaction/`
- `<repo-root>/src/test/java/.../transaction/`

### 5.3 扩展扫描目录（如有需要）
- `<repo-root>/src/main/java/.../agreement/`
- `<repo-root>/src/main/resources/mapper/agreement/`

### 5.4 需优先检查的存量类型
- Controller / Entry
- Service / Orchestration
- BO / DTO / VO / Entity
- Mapper / XML / Repository
- Helper / Converter / Adapter
- Enum / Constant
- Test
- 配置 / 路由 / 脚本（如适用）

说明：
- 当前 Git 代码始终为实物基线
- 若未扫描当前代码现状，不允许直接生成 design / tasks

## 6. 设计文档选择规则
### 6.1 设计文档根目录
- `.project-design-docs/`

### 6.2 已知设计文档（如有）
- `.project-design-docs/sprint5/agreement-information-query-design.md`

### 6.3 若未显式指定，按以下优先级选择
1. 与功能名称最接近的设计文档
2. 同模块下相同功能类型的最近设计文档
3. 同 sprint 下最相近功能文档
4. 若无可参考文档，明确标注“本次基于存量代码与规则推导设计”

## 7. 历史功能资产引用（仅 enhancement / refactor 必填）
### 7.1 本次是否基于历史功能继续演进
- 否

## 8. 本次功能资产输出位置
### 8.1 功能资产根目录
- `.project-features/`

### 8.2 本次输出目录
- `.project-features/sprint5/agreement-information-query/`

### 8.3 需生成文件
- `spec.md`
- `design.md`
- `tasks.md`

## 9. 本次归档要求
### 9.1 归档文件路径
- `.project-features/sprint5/agreement-information-query/archive.md`

### 9.2 归档前置条件
仅在以下条件全部满足后才允许归档：

1. `spec.md` 已确认
2. `design.md` 已确认
3. `tasks.md` 已确认
4. 代码实施已完成
5. 编译 / 测试结果已输出
6. 人工最终审核已通过

### 9.3 归档标准要求
归档文件必须满足：

1. 基于最终确认版本，不记录中途废弃方案作为最终结论
2. 与当前最终 Git 代码结果一致；若存在差异，必须明确标注
3. 能支持下一次 enhancement / refactor 在不回看完整对话的情况下继续工作
4. 保留必要的决策依据与取舍，不得只写结论
5. 不堆砌执行流水账，只保留后续复用所需信息
6. 如本次产生规则 / 索引 / 模板增量，必须在归档中记录
7. 如任务未完全完成，必须明确写出未完成项、遗留风险与后续建议

## 10. 执行要求
1. 先读取 `index.md`，再按索引装配 context / rules / templates
2. 再扫描当前 Git 代码现状
3. 再读取匹配的设计文档（如有）
4. 先生成 `spec.md`
5. `spec.md` 确认后，再生成 `design.md`
6. `design.md` 确认后，再生成 `tasks.md`
7. `tasks.md` 确认后，按 `spec.md + design.md + tasks.md` 实施代码
8. 实施完成后，必须输出：
    - 变更文件清单
    - 变更摘要
    - 编译结果
    - 测试结果
    - 已知问题 / 风险点
9. 人工审核实施结果；如未通过，必须在当前任务上下文中修正
10. 审核通过后，按归档标准生成 `archive.md`
11. 若本次任务产生通用规则增量，需同步更新 `.project-ai/context/index.md` 或对应 rules / templates