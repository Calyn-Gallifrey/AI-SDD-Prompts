# 功能提案入口

## 1. 业务任务信息
功能名称：
功能类型：query / submit / edit / enhancement / refactor
所属模块：
变更目标：
技术面：API / ORM / mapstruct / current user / test / OM / EPI
变更范围：
禁止变更：

## 2. AI 知识底座路径
AI知识底座根目录：`.project-ai/`
索引文件：`.project-ai/context/index.md`
上下文目录：`.project-ai/context/`
规则目录：`.project-ai/rules/`
模板目录：`.project-ai/templates/`

## 3. 现状扫描范围
代码仓根目录：`<repo-root>/`

优先扫描目录：
- ``
- ``
- ``

扩展扫描目录（如有需要）：
- ``
- ``

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
- ``

若未指定，按以下优先级选择：
1. 与功能名称最接近的设计文档
2. 同模块下相同功能类型的最近设计文档
3. 同 sprint 下最相近功能文档
4. 若无可参考文档，标注“本次基于存量代码与规则推导设计”

## 5. 历史功能资产引用（仅 enhancement / refactor 必填）
本次任务是否基于历史功能继续演进：是 / 否

如是，请填写：
历史功能目录：`.project-features/.../`
优先读取：
- `archive.md`

补充读取（按需）：
- `spec.md`
- `design.md`
- `tasks.md`

说明：
- 先读 `archive.md`，了解上次最终方案、关键决策、边界与风险
- 再按需读 `spec.md`、`design.md`
- 当前 Git 代码始终为实物基线，如历史资产与当前代码冲突，以当前 Git 代码为准，并在新一轮 spec 中明确标注差异

## 6. 本次功能资产输出位置
功能资产根目录：`.project-features/`
本次输出目录：`.project-features/<sprint>/<feature-name>/`

需生成文件：
- `spec.md`
- `design.md`
- `tasks.md`

## 7. 本次归档要求
本次任务完成并通过最终人工审核后，需生成归档文件：
- `.project-features/<sprint>/<feature-name>/archive.md`

归档前置条件：
1. `spec.md` 已确认
2. `design.md` 已确认
3. `tasks.md` 已确认
4. 代码实施已完成
5. 编译 / 测试结果已输出
6. 人工最终审核已通过

归档标准要求：
1. 归档内容必须基于“最终确认版本”，不得记录中途废弃方案作为最终结论
2. 归档内容必须与当前最终 Git 代码结果一致；若存在差异，必须在归档中明确标注
3. 归档必须能让下一次 enhancement / refactor 在不回看完整对话的情况下，快速理解本次任务的：
   - 目标
   - 边界
   - 最终方案
   - 关键决策
   - 风险
   - 推荐阅读顺序
4. 归档不得只写结论，必须保留必要的决策依据与取舍说明
5. 归档不得堆砌执行过程流水账，只保留对后续复用有价值的信息
6. 若本次任务形成新的通用规则、索引增量或模板修正，必须在归档中明确记录
7. 若本次任务未完全完成，必须在归档中明确标注“未完成项 / 遗留风险 / 后续建议”，不得伪装为完整闭环
8. 归档完成后，应可作为下一次增强提案的优先输入资产

## 8. 执行要求
1. 先读索引文件，再按索引装配 context / rules / templates
2. 再扫描指定代码范围
3. 再读取匹配的设计文档
4. 先生成 `spec.md`
5. `spec.md` 确认后，再生成 `design.md`
6. `design.md` 确认后，再生成 `tasks.md`
7. `tasks.md` 确认后，按 `spec.md + design.md + tasks.md` 实施代码
8. 代码实施完成后，需输出：
   - 变更文件清单
   - 变更摘要
   - 编译结果
   - 测试结果
   - 已知问题 / 风险点
9. 人工审核实施结果；如未通过，需基于当前任务上下文继续修正，不得直接跳过审查进入归档
10. 仅在以下条件全部满足后，才允许执行归档：
    - `spec.md` 已确认
    - `design.md` 已确认
    - `tasks.md` 已确认
    - 代码实施已完成
    - 编译 / 测试结果已输出
    - 人工最终审核已通过
11. 执行归档时，需按归档标准生成 `archive.md`，不得仅生成空壳文件或简略结论
12. 如本次任务产生通用规则增量，需同步更新 `.project-ai/context/index.md` 或对应 rules / templates
13. 若本次任务后续可能继续 enhancement / refactor，需在 `archive.md` 中明确写出下一次任务的推荐阅读顺序