# agreement-information-query 功能任务编排

> 本文件承接已确认的 spec 与 design，输出 Builder / AI 可施工的阶段化执行任务。

---

## 1. 基本信息
- 功能名称：agreement-information-query
- 功能类型：query
- 所属模块：transaction
- 对应 spec：`./spec.md`
- 对应 design：`./design.md`
- tasks 文件路径：`./tasks.md`
- 当前状态：待确认

## 2. 输入文件区
### 2.1 必选输入
- `spec.md`
- `design.md`
- 当前 Git 代码扫描结果
- 已装配的 context
- 已装配的 rules

### 2.2 可选输入
- `.project-design-docs/sprint5/agreement-information-query-design.md`
- 既有 query 类功能测试结果 / 编译日志

### 2.3 输入完整性检查
开始执行前确认：
- spec 已确认
- design 已确认
- 当前代码基线已扫描
- 规则装配已完成
- 依赖与边界已明确

## 3. 本次规范装配摘要
### 3.1 已装配 context
- transaction 模块上下文
- agreement information 查询场景上下文
- 当前代码扫描结果上下文

### 3.2 已装配 rules
- 结构与落位
- 契约与接口
- 持久化与查询
- 对象模型与边界
- 转换与映射
- 身份、权限与审计
- 测试与质量门禁
- 兼容、迁移与演进

### 3.3 已装配 templates
- 当前模板：`tasks-template.md`
- 归档模板：`archive-template.md`

### 3.4 历史资产引用（如适用）
- 本次不适用

## 4. 任务分阶段执行（Phases）

### Phase 0：执行前确认
#### 目标
确认本次施工的双基线、边界和依赖已经齐备。

#### 输入
- spec
- design
- 当前代码扫描结果

#### 执行动作
- 确认 transaction 模块落位路径
- 确认 agreement-information-query 为 transaction 内增量能力
- 确认不可变边界：
  - 不改表
  - 不改 path
  - 不改 helper
  - 不改核心流程
- 确认需补齐的测试范围
- 确认可参考的既有 query 类实现样板

#### 输出物
- 执行前确认结论
- 风险提示
- 依赖清单

#### Dependencies
- spec 已确认
- design 已确认

---

### Phase 1：对象与结构落位
#### 目标
完成对象、包路径、结构落位相关工作。

#### 输入
- spec
- design
- 对象模型与边界规则
- 结构与落位规则

#### 执行动作
- 新增 `AgreementInformationQueryBO`
- 新增 `AgreementInformationQueryDTO`
- 新增 `AgreementInformationQueryVO`
- 如需要，新增 `AgreementInformationQueryEntity`
- 校验对象命名、路径与层级
- 确认 package 落位与 transaction 模块风格一致

#### 输出物
- 新增对象文件清单
- 包落位结果

#### Dependencies
- Phase 0 完成

---

### Phase 2：核心实现
#### 目标
完成 controller / service / mapper / xml / 转换等核心实现。

#### 输入
- spec
- design
- 契约与接口规则
- 持久化与查询规则
- 转换与映射规则
- 身份 / 审计规则
- 校验 / 异常规则

#### 执行动作
- 实现 `AgreementInformationQueryController`
- 实现 `AgreementInformationQueryService`
- 实现 `AgreementInformationQueryServiceImpl`
- 实现 `AgreementInformationQueryMapper`
- 实现 `AgreementInformationQueryMapper.xml`
- 补齐请求对象到业务对象、查询结果到返回对象的转换逻辑
- 保持 current user / 审计处理方式与既有规则一致
- 严格避免修改既有 helper / path / 核心流程

#### 输出物
- 核心实现文件清单
- 核心变更摘要

#### Dependencies
- Phase 1 完成

---

### Phase 3：测试与质量校验
#### 目标
补齐测试并完成质量门禁要求。

#### 输入
- spec 验收标准
- design 测试设计考量
- testing rules

#### 执行动作
- 新增 / 补充 `AgreementInformationQueryServiceTest`
- 新增 / 补充 `AgreementInformationQueryControllerTest`
- 按需补充转换逻辑测试
- 检查正常路径、空结果、参数边界、异常场景
- 检查 current user / 审计处理逻辑（如有）

#### 输出物
- 测试文件清单
- 测试执行结果
- 质量校验结果

#### Dependencies
- Phase 2 完成

---

### Phase 4：实施后自检
#### 目标
在人工审核前形成完整可审查输出。

#### 输入
- 所有实现结果
- 测试结果
- spec / design / tasks

#### 执行动作
- 检查实现是否符合 spec 目标
- 检查实现是否符合 design 设计
- 检查不可变边界是否被破坏
- 汇总变更文件清单
- 汇总编译结果、测试结果
- 汇总已知问题与风险
- 为人工审核准备交付摘要

#### 输出物
- 变更文件清单
- 变更摘要
- 编译结果
- 测试结果
- 已知问题 / 风险点

#### Dependencies
- Phase 3 完成

## 5. 明确执行顺序
必须按以下顺序执行，不得跳步：

1. Phase 0：执行前确认
2. Phase 1：对象与结构落位
3. Phase 2：核心实现
4. Phase 3：测试与质量校验
5. Phase 4：实施后自检
6. 人工审核
7. 如审核不通过，回到对应 Phase 修正
8. 审核通过后，进入 archive

## 6. Dependencies（依赖关系）

### 6.1 上游依赖
- spec 已确认
- design 已确认
- context 与 rules 已装配
- 当前代码扫描结果已生成

### 6.2 施工依赖
- package 路径明确
- 不可变边界明确
- 转换逻辑明确
- 测试范围明确

### 6.3 禁止事项
- 不得在 design 未明确时自行脑补新的落位、流程或外部调用方式
- 不得把“最小增量实现”扩成“顺手重构 transaction 模块”

## 7. 人工审核前必须输出
- 变更文件清单
- 变更摘要
- 编译结果
- 测试结果
- 已知问题 / 风险点

## 8. 审核未通过处理
- 收集问题清单
- 回到对应 Phase 修正
- 重新自检
- 再提交审核

禁止：
- 跳过问题直接归档
- 私自扩大变更范围
- 推翻已确认 spec（除非重新发起提案）

## 9. 归档前置条件
以下全部满足后才允许归档：

- spec 已确认
- design 已确认
- tasks 已执行完成
- 编译通过
- 测试通过
- 人工审核通过
- 输出 summary 已完成

## 10. 归档输出要求
生成：
- `archive.md`

至少包含：
- 最终方案
- 实施结果
- 风险与遗留项
- 关键决策
- 可复用资产
- 下一次 enhancement 阅读顺序

归档内容必须按 `archive-template.md` 生成，不得简化为几行空壳结论。