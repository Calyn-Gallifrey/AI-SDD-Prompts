# 功能级 Tasks 模板

> 本文件承接已确认的 `spec.md + design.md`，用于输出可直接执行的实施任务。
> 本文件定义实施顺序、交付物、自检要求和归档条件。
> 需求范围以 `spec.md` 为准。
> 技术方案以 `design.md` 为准。

---

# 1. 基本信息

- 功能名称：
- 功能类型：query / submit / edit / enhancement / refactor / fix
- 所属模块：
- 对应 spec：`./spec.md`
- 对应 design：`./design.md`
- tasks 文件路径：`./tasks.md`
- 执行模式：standard
- 当前状态：draft / confirmed / executing / review / fix / unit-test / archived / blocked

---

# 2. 输入确认（执行前必须完成）

## 必须已确认

- [ ] proposal-input.md 已存在
- [ ] spec.md 已确认
- [ ] design.md 已确认

## 当前代码已扫描

- [ ] 当前模块代码
- [ ] mapper / repository
- [ ] model 对象
- [ ] test 代码
- [ ] config / script（如适用）

## enhancement / refactor 额外确认

- [ ] 已扫描当前代码工程中的既有实现
- [ ] 如用户提供或当前任务依赖参考资产，已读取相关参考资产
- [ ] 已识别参考资产与当前 Git 实物基线差异

---

# 3. 输入摘要（来自 spec / design）

## 功能目标

-

## 本次范围

-

## 不可变边界

-

## 关键设计约束

-

## 风险重点

-

## 验收重点

-

---

# 4. 本次规则装配结果

已命中规则：

- 流程控制规则
- 包结构规则
- API 规则
- DB / Mapper 规则
- Model 规则
- Mapping 规则
- Testing 规则
- Integration 规则（如适用）
- Security / Audit 规则（如适用）

补充说明：

-

---

# 5. 执行总原则（固定）

1. 严格按 spec 范围施工
2. 严格按 design 落位施工
3. 不改无关代码
4. 小步修改，保持可回滚
5. 每阶段完成后必须自检并完成 Phase Review
6. 如需突破边界，必须回到 spec / design 重审
7. 当前 Git 代码与文档冲突时，以代码为准并记录差异
8. 若 design 未明确某类对象、流程或调用方式，必须先回到 design 澄清，不得补写未经确认的实施内容

---


## 5.1 检查项执行标记规则（强制）

Tasks 文件中的所有检查项都必须经过实际检查，不得保留未检查状态。

### 标记规则

- `[✓]`：已检查，且发现问题 / 不满足 / 有阻塞。
- `[x]`：已检查，且无问题 / 已满足 / 可通过。
- `[ ]`：仅允许作为模板初始占位。实际生成或更新 `tasks.md` 后，禁止继续保留 `[ ]`。

### 执行要求

1. 所有 `[ ]` 检查项必须逐项检查后改为 `[✓]` 或 `[x]`。
2. 发现问题时必须打 `[✓]`，并在该检查项后补充问题说明、影响范围和下一步处理动作。
3. 未发现问题时必须打 `[x]`，表示该项已检查且无问题。
4. 不得批量默认打 `[x]`，每一项都必须基于实际检查结果。
5. 不得用“已检查”“无异常”等泛泛文字替代 `[✓] / [x]` 标记。
6. 如果某检查项不适用，必须写成 `[x] 不适用：原因...`，不得留空。
7. 若存在任何 `[✓]` 项，必须在“执行结论 / 阻塞项 / 下一步动作”中同步记录。
8. 若进入 Code Review、Review-driven Auto-fix、Unit Test 或 Archive 前仍存在 `[ ]`，必须停止流程并先完成检查项更新。

### 示例

```markdown
- [✓] design.md 已确认
  问题：design.md 仍处于 draft 状态，未满足进入 tasks 执行条件。
  下一步：等待人工确认 design.md。

- [x] 当前模块代码
  已检查，当前模块代码可作为实施基线。

- [x] config / script（如适用）
  不适用：本次变更不涉及配置或脚本。
```

## 5.2 Phase Review 记录规则（强制）

每个实际执行的 Phase 完成后，必须记录人工审核结果。Phase Review 不替代 SDD 内部 Code Review。

### Phase Review 总表

| Phase | Reviewer Role | Review Time | Result | Findings | Required Action | Next Phase Allowed |
|---|---|---|---|---|---|---|
| Phase 1：对象层施工 |  |  | 通过 / 有条件通过 / 驳回 / 不适用 |  |  | yes / no |
| Phase 2：数据层施工 |  |  | 通过 / 有条件通过 / 驳回 / 不适用 |  |  | yes / no |
| Phase 3：业务层施工 |  |  | 通过 / 有条件通过 / 驳回 / 不适用 |  |  | yes / no |
| Phase 4：接口层施工 |  |  | 通过 / 有条件通过 / 驳回 / 不适用 |  |  | yes / no |
| Phase 5：集成层施工 |  |  | 通过 / 有条件通过 / 驳回 / 不适用 |  |  | yes / no |
| Phase 6：测试层施工 |  |  | 通过 / 有条件通过 / 驳回 / 不适用 |  |  | yes / no |
| Phase 7：交付整理 |  |  | 通过 / 有条件通过 / 驳回 / 不适用 |  |  | yes / no |

规则：

1. 每个实际执行的 Phase 都必须有审核记录。
2. 不适用的 Phase 必须记录不适用原因。
3. `Next Phase Allowed` 为 `no` 时，禁止进入下一 Phase。
4. 有条件通过必须写明条件、修复范围和验证方式。
5. 驳回必须回到对应 Phase 修复，并追加新的 Phase Review 记录。
6. 如果由 AI 代理人工审核，必须如实记录审核角色，不得记录为真实人员审批。

# 6. Phase 拆解（Standard Mode）

## Phase 1：对象层施工

### 任务内容

- 新增 / 修改 DTO
- 新增 / 修改 VO
- 新增 / 修改 BO
- 新增 / 修改 Entity
- 新增 / 修改 Enum / Constant（如需）

### 输出物

- model 类文件

### 检查项

- 命名规范
- 字段完整
- 字段来源明确
- 与 spec 对齐
- 无重复对象

### 可跳过条件

- 若 design 已明确本次无需新增 / 修改对象层，可跳过
- 跳过时必须写明原因，不得静默省略

---

## Phase 2：数据层施工

### 任务内容

- 新增 / 修改 Mapper / Repository
- 新增 / 修改 XML / SQL
- 新增 QueryParam / 条件对象

### 输出物

- 数据访问层代码

### 检查项

- SQL 正确
- 条件完整
- 返回字段正确
- 无明显性能问题
- 命名统一

### 可跳过条件

- 若 design 已明确本次不涉及 DB / Mapper 改动，可跳过
- 跳过时必须写明原因，不得静默省略

---

## Phase 3：业务层施工

### 任务内容

- 新增 / 修改 Service
- 新增 / 修改 Impl
- 新增 / 修改业务逻辑
- Strategy / Support（如需）

### 输出物

- service 层代码

### 检查项

- 流程符合 design
- 边界清晰
- 异常处理合理
- 不污染存量逻辑

### 可跳过条件

- 仅在 design 明确无业务层变更时允许跳过
- 跳过时必须写明原因

---

## Phase 4：接口层施工

### 任务内容

- 新增 / 修改 Controller
- 新增 / 修改 API path
- Request / Response
- 参数校验

### 输出物

- controller 层代码

### 检查项

- path 正确
- 入参正确
- 出参正确
- 错误码统一
- 注解完整（如适用）

### 可跳过条件

- 若 design 已明确本次无接口层变化，可跳过
- 跳过时必须写明原因

---

## Phase 5：集成层施工（如适用）

### 任务内容

涉及外部系统 / 网关 / ACL 时执行：

- 第三方接口接入
- 网关调用
- fallback / retry
- traceId 透传

### 输出物

- integration 代码

### 检查项

- timeout
- retry
- 错误映射
- 日志完整

### 可跳过条件

- 若 design 已明确本次无外部依赖改动，可跳过
- 跳过时必须写明原因

---

## Phase 6：测试层施工

### 任务内容

补充：

- Unit Test
- Integration Test（如适用）
- Converter / Util Test（如适用）

### 输出物

- 测试代码

### 覆盖场景

- 正常路径
- 异常路径
- 边界输入
- 空结果
- 权限 / 上下文场景
- 回归场景

---

## Phase 7：交付整理

### 必须输出

#### 变更文件清单

-

#### 变更摘要

-

#### Unit Test Summary 引用

- pass / fail / not applicable
- 说明：正式测试结论以第 17.3 节 Unit Test Summary 为准。

#### 已知问题

-

#### 风险点

-

#### 回滚方式（如适用）

-

---

# 7. 流程模式约束

当前 SDD2.0 标准流程只允许 `standard` 模式。

规则：

1. 不得默认启用 Fast Lane、mini-spec、mini-tasks 或 archive-lite。
2. tasks 必须承接已确认的 `spec.md` 和 `design.md`。
3. 不得从 proposal-input 或 spec 直接进入代码实现。
4. 若未来版本需要轻量模式，必须先在体系规则中正式定义输入、产物、审核点、质量闸门和归档规则。

---

# 8. Dependencies（依赖关系）

默认顺序：

对象层
→ 数据层
→ 业务层
→ 接口层
→ 集成层（如有）
→ 测试层
→ 交付整理

允许特例：

- 纯 SQL 修复：从数据层开始
- 纯接口字段调整：从接口层开始
- 纯测试补齐：从测试层开始

---

# 9. 实施后本地检查记录（必须更新，不作为强制闸门替代）

## 代码层

- [ ] 本地验证记录已补充（如适用；不得替代 Code Review / Unit Test Summary）
- [ ] import 干净
- [ ] 无明显 warning
- [ ] 命名规范

## 功能层

- [ ] 满足 spec
- [ ] 原功能未破坏
- [ ] 边界未突破

## 设计层

- [ ] 与 design 一致
- [ ] 无私自扩展实现

## 质量层

- [ ] Unit Test Summary 已输出或明确不适用原因
- [ ] 无明显回归问题

---

# 10. 审核未通过处理

1. 收集问题清单
2. 回到对应 Phase 修正
3. 重新自检
4. 再提交审核

禁止：

- 跳过问题直接归档
- 私自扩大范围
- 推翻已确认 spec（除非重新提案）

---

# 11. 归档前置条件

以下全部满足后才允许归档：

- [ ] spec 已确认
- [ ] design 已确认
- [ ] tasks 已执行完成
- [ ] 代码实施已完成
- [ ] Code Review 已完成
- [ ] Review-driven Auto-fix 已完成，或明确记录不需要修复
- [ ] Unit Test Generation 已完成，或明确记录不适用原因
- [ ] Unit Test Summary 已输出
- [ ] 人工最终审核通过

---

# 12. 归档输出要求

生成：

- `archive.md`

至少包含：

- 最终方案
- 实施结果
- 风险与遗留项
- 关键决策
- 可复用资产
- 下一次 enhancement 阅读顺序

归档内容必须基于 `archive-template.md`，并完整保留必填结论、依据和风险项。

---

# 13. 状态流转

draft
→ executing
→ code-review
→ auto-fix（如需）
→ unit-test
→ approved
→ archived

---

# 14. 执行结论

- 当前状态：
- 阻塞项：
- 下一步动作：
- 备注：

---

# 15. Code Review Gate（强制）

代码实现完成后，必须进入 Code Review Gate。

## 15.1 入口模式

SDD 流程内必须使用 `SDD_TASK_CODE_REVIEW`。

该入口由 SDD 流程内部调用，Entry Mode、Feature Directory 和 SDD Artifacts 由流程上下文提供。流程上下文必须能够等价提供以下信息：

```text
Entry Mode: SDD_TASK_CODE_REVIEW
Feature Directory: sdd2-features/<SprintN>/<feature-name>/
SDD Artifacts:
- ./proposal-input.md
- ./spec.md
- ./design.md
- ./tasks.md
```

## 15.2 SDD 内部 Code Review 输出规则

SDD 内部 Code Review 是流程质量闸门，输出形式为 Markdown Findings。

必须遵守：

1. 不生成 `代码评审统计报告.html`。
2. 不生成 `{开发者姓名}_代码评审报告.html`。
3. 不读取 `skills/uaw-code-review/references/templates/summary-report-template.html`。
4. 不读取 `skills/uaw-code-review/references/templates/personal-report-template.html`。
5. 不创建 `./reports/code-review/YYYY-MM-DD/` 目录。
6. 必须在当前功能目录输出 `code-review-findings.md`。
7. 必须基于 Findings 进入 Review-driven Auto-fix。

## 15.3 Code Review 必查项

- [ ] 实现符合 spec 范围和边界
- [ ] 实现符合 design 落位和流程设计
- [ ] tasks 中确认的任务均已完成
- [ ] 未出现未经批准的范围扩张
- [ ] 未创建约定之外的目录或文件
- [ ] 未绕过项目工具类、日志、异常、安全、测试规范
- [ ] P0/P1 问题均有明确修复建议
- [ ] Unit Test 影响点已识别

## 15.4 Code Review Findings 产物

- Findings 文件：`./code-review-findings.md`
- Findings 模板：`skills/uaw-code-review/references/templates/sdd-code-review-findings-template.md`
- 引用位置：`tasks.md`、`archive.md`
- 产物类型：SDD 内部 Markdown 质量闸门产物
- HTML 报告：不生成
- Standalone 报告替代：不得使用

`code-review-findings.md` 必须至少包含：

- Code Review Conclusion
- P0 / P1 / P2 / Suggestion 数量
- Review-driven Auto-fix Required
- Fix Scope
- Files allowed to modify
- Files forbidden to modify
- Untracked files reviewed
- Unit tests required
- Archive allowed
- Findings 明细

## 15.5 Code Review Findings 明细

| 问题编号 | 严重程度 | 文件 | 方法 / 类 | 问题摘要 | 修复建议 | 是否阻塞 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## 15.6 Code Review 结果

- Code Review 结论：拒绝通过 / 有条件通过 / 通过
- P0 数量：
- P1 数量：
- P2 数量：
- Suggestion 数量：
- 是否需要 Review-driven Auto-fix：yes / no
- Fix Scope：
- Files allowed to modify：
- Files forbidden to modify：
- Unit tests required：yes / no
- Archive allowed：yes / no

规则：

1. 存在 P0：拒绝通过，必须先 Auto-fix，禁止进入 Archive。
2. 存在 P1：有条件通过，必须完成修复计划后才能 Archive。
3. 无 P0/P1：允许进入 Unit Test Generation。
4. Archive 必须等待 Code Review、Auto-fix、Unit Test Summary 全部完成。

# 16. Review-driven Auto-fix Gate（强制）

Code Review 后必须执行本 Gate。

## 16.1 触发条件

- 存在 P0 / P1：必须修复
- 存在影响验收的 P2：建议修复
- 无需修复：必须记录原因

## 16.2 修复边界

允许修改：

- Code Review 明确指出的问题文件
- 为修复问题必须同步调整的测试文件
- 已在 spec/design/tasks 确认范围内的相关文件

禁止修改：

- 未被 Code Review 指出的问题区域
- spec/design/tasks 未批准的额外范围
- 与本任务无关的历史代码

## 16.3 修复结果

- 修复文件清单：
- 修复问题编号：
- 未修复问题及原因：
- 是否需要重新 Code Review：yes / no

## 16.4 Auto-fix 后复核

Auto-fix 完成后，必须执行一次轻量复核，确认 `code-review-findings.md` 中所有阻塞 Archive 的问题都已经处理。

复核规则：

1. 必须区分 Code Review 原始结论与 Auto-fix 后最终闸门结论。
2. 不得把修复前的 `Archive allowed: no` 直接作为 Archive 阻断依据继续保留到最终状态。
3. 必须在 `code-review-findings.md` 或 `auto-fix-summary.md` 中记录 `Post Auto-fix Verification`。
4. 存在未修复 P0 / P1 时，禁止进入 Unit Test 和 Archive。
5. 存在未修复且影响验收的 P2 时，禁止 Archive，必须说明处理策略。
6. 复核通过后，才能进入 Unit Test Gate。

`Post Auto-fix Verification` 至少包含：

- Recheck Result：passed / failed
- Rechecked Issues：
- Remaining P0 / P1 / Blocking P2：
- Archive allowed after Auto-fix：yes / no
- Next Gate：

---

# 17. Unit Test Gate（强制）

Review-driven Auto-fix 完成后，必须进入 Unit Test Gate。

## 17.1 测试规则来源

必须读取并遵守：

`skills/uaw-unit-test/references/java/`

必须先读取：

`skills/uaw-unit-test/references/testing-profile-routing.md`

生成 Unit Test Summary 前必须读取：

`skills/uaw-unit-test/references/templates/unit-test-summary-template.md`

并记录：

- Selected Testing Profile：
- 选择依据：
- 不适用规则：
- 测试框架风险：
- 是否需要补充依赖：

## 17.2 单元测试要求

- [ ] 核心业务路径已覆盖
- [ ] 异常路径已覆盖
- [ ] 边界条件已覆盖
- [ ] Code Review 修复点已覆盖
- [ ] 测试命名、Mock、断言符合 testing 规则

如单元测试不适用，必须写明：

- 不适用原因：
- 替代验证方式：
- 是否影响 archive：

## 17.3 Unit Test Summary

必须按 `skills/uaw-unit-test/references/templates/unit-test-summary-template.md` 生成或更新 `unit-test-summary.md`。

- Validation Method：IDE / Wrapper / Local CLI / CI / Script / Manual / Other
- Execution Environment：本机 / CI / 开发容器 / IDE / 其他
- Build Tool 或测试执行器：
- 实际执行入口：命令 / IDE 配置名 / CI Job / 脚本路径 / 手工验证说明
- 新增测试文件：
- 修改测试文件：
- 覆盖场景：
- 未覆盖场景及原因：
- warning / failure / skipped 说明：
- 测试结论：pass / fail / not applicable

规则：

1. 不强制要求本机安装 `mvn` 或其他命令行工具。
2. 可以记录 IDE 内置 Maven / Gradle、Wrapper、CI、脚本或手工验证结果。
3. 如无法执行自动化测试，必须写明原因、替代验证方式和是否影响 Archive。

---

# 18. Archive Gate（强制）

以下全部满足后才允许生成 `archive.md`：

- [ ] spec.md 最终状态已更新
- [ ] design.md 最终状态已更新
- [ ] tasks.md 最终状态已更新
- [ ] proposal-input.md 最终状态已更新
- [ ] code-review-findings.md 已生成
- [ ] Code Review 已完成
- [ ] Review-driven Auto-fix 已完成或明确不需要
- [ ] Unit Test Summary 已完成或明确不适用原因

禁止在 Code Review 或 Unit Test 之前生成 archive。


---

# Process Status（强制｜流程闸门）

- Current Stage：
- Stage Status：draft / confirmed / executing / review / fix / unit-test / archived / blocked
- Last Completed Step：
- Next Required Step：
- Human Confirmation Required：yes / no
- Allowed Next Action：
- Forbidden Next Action：
- Updated At：

# Process Audit Trail（强制｜过程审核轨迹）

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

规则：

1. 进入下一阶段前，必须先更新当前文件的 Process Status 和 Process Audit Trail。
2. 未更新状态区块时，不得进入下一阶段。
3. 如果某阶段被跳过或不适用，必须写明原因，禁止静默跳过。
4. 生成 archive.md 前，proposal-input.md、spec.md、design.md、tasks.md 均必须处于最终可归档状态。
5. Process Status 生命周期、Phase Review 和验证方式记录必须遵守 `skills/uaw-sdd-ai-coding/references/process-control.md`。
