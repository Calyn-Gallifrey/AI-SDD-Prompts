# 功能提案入口

## 1. 业务任务信息
功能名称：agreement-info-query  
功能类型：query  
所属模块：transaction  
变更目标：在 transaction 现有模块中新增 agreement information 查询接口，用于按指定条件查询 agreement information 列表或明细。  
技术面：API / ORM / mapstruct / current user / test  
变更范围：
- 新增 agreement-info-query 查询接口
- 新增查询入参对象
- 新增返回对象
- 新增 mapper / xml 查询逻辑
- 新增 service / controller
- 补充必要单元测试

禁止变更：
- 不改资料表结构
- 不改既有 API path
- 不改既有 helper
- 不改 transaction 现有核心提交流程

## 2. AI 知识底座路径
AI知识底座根目录：`.project-ai/`  
索引文件：`.project-ai/context/index.md`  
上下文目录：`.project-ai/context/`  
规则目录：`.project-ai/rules/`  
模板目录：`.project-ai/templates/`

## 3. 现状扫描范围
代码仓根目录：`<repo-root>/`

优先扫描目录：
- `<repo-root>/src/main/java/.../transaction/`
- `<repo-root>/src/main/resources/mapper/transaction/`
- `<repo-root>/src/test/java/.../transaction/`

扩展扫描目录（如有需要）：
- `<repo-root>/src/main/java/.../agreement/`
- `<repo-root>/src/main/resources/mapper/agreement/`

需优先检查的存量类型：
- Controller
- Service
- BO / DTO / VO / Entity
- Mapper / XML
- Helper / Converter
- Enum / 常量
- 单元测试

## 4. 设计文档选择规则
设计文档根目录：`.project-design-docs/`

如已知，请直接指定设计文档路径：
- `.project-design-docs/sprint5/agreement-info-query-design.md`

若未指定，按以下优先级选择：
1. 与功能名称最接近的设计文档
2. 同模块下相同功能类型的最近设计文档
3. 同 sprint 下最相近功能文档
4. 若无可参考文档，标注“本次基于存量代码与规则推导设计”

## 5. 历史功能资产引用（仅 enhancement / refactor 必填）
本次任务是否基于历史功能继续演进：否

## 6. 本次功能资产输出位置
功能资产根目录：`.project-features/`  
本次输出目录：`.project-features/sprint5/agreement-info-query/`

需生成文件：
- `spec.md`
- `design.md`
- `tasks.md`

## 7. 本次归档要求
本次任务完成并通过最终人工审核后，需生成归档文件：
- `.project-features/sprint5/agreement-info-query/archive.md`

归档前置条件：
1. `spec.md` 已确认
2. `design.md` 已确认
3. `tasks.md` 已确认
4. 代码实施已完成
5. 编译 / 测试结果已输出
6. 人工最终审核已通过

归档内容至少包括：
- 本次任务基本信息
- 最终采用的 spec / design / tasks 路径
- 最终实施结果摘要
- 变更文件清单
- 关键决策与取舍
- 未解决问题 / 后续风险
- 是否新增 / 修正了 rules / index / templates
- 下一次增强需求应优先阅读哪些文件


## 8. 执行要求
1. 先读索引文件，再按索引装配 context / rules / templates
2. 再扫描指定代码范围
3. 再读取匹配的设计文档
4. 先生成 `spec.md`
5. `spec.md` 确认后，再生成 `design.md`
6. `design.md` 确认后，再生成 `tasks.md`
7. `tasks.md` 确认后，按 `spec.md + design.md + tasks.md` 实施代码
8. 人工审核通过后，再执行归档
9. 如本次产生通用规则增量，需同步更新 `.project-ai/context/index.md` 或对应 rules / templates  