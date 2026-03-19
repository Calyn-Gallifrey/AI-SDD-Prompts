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

---

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

---

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

---

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

---

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

---

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

### 6.3 下游依赖
- 实施结果需提供给人工审核
- 审核通过后才允许归档
- 若有规则增量，需回写 `.project-ai`

---

## 7. 实施后自检要求
在人工审核前，必须完成以下自检：
- 是否遵循已装配规则
- 是否与 spec 目标一致
- 是否与 design 设计一致
- 是否修改了禁止变更区域
- 是否补齐必要测试
- 是否输出完整变更摘要
- 是否标明已知问题与风险
- 是否具备归档前置条件

---

## 8. 人工审核前输出要求
提交给人工审核前，必须输出：

1. 变更文件清单
2. 变更摘要
3. 编译结果
4. 测试结果
5. 已知问题 / 风险点
6. 是否需要继续修正的建议

---

## 9. 交付物清单
本次 tasks 执行完成后，至少应交付：

- `spec.md`
- `design.md`
- `tasks.md`
- 已修改 / 新增代码
- 测试代码
- 实施后自检结果
- 提交人工审核的输出摘要
- 审核通过后生成的 `archive.md`

---

## 10. 归档前置条件
只有满足以下条件，才允许进入 archive：

1. `spec.md` 已确认
2. `design.md` 已确认
3. `tasks.md` 已确认
4. 代码实施已完成
5. 编译 / 测试结果已输出
6. 人工最终审核已通过
7. 已形成变更文件清单与实施摘要
8. 已知问题 / 风险点已明确记录

---

## 11. 与 `archive-template.md` 的衔接
在满足归档前置条件后，tasks 的执行结果必须能直接供 `archive-template.md` 使用，包括：

- 本次最终采用的 spec / design / tasks 路径
- 最终实施结果摘要
- 变更文件清单
- 关键决策与取舍
- 编译 / 测试结果
- 遗留事项与后续建议
- 是否回写 rules / index / templates

---

## 12. 审核记录
- tasks 审核状态：待审核
- 审核结论：
- 审核人：
- 审核时间：