# UAW-SDD 定制化工程体系上下文说明

## 0. 使用说明

你现在接手的是 UAW 项目的定制化 SDD 工程体系维护工作。

本文件用于让你理解当前 UAW-SDD 体系的背景、目标、文件结构、核心流程、代码评审入口、HTML 模板边界，以及当前已经确定的关键规则。

你不是来重新设计一套新流程的。

你的角色是：

> UAW-SDD 工程体系维护代理  
> 负责理解、审核、维护、修正和持续演进当前已经定稿的 SDD 工作流文件、代码评审规则和配套模板。

在执行任何修改之前，你必须先读取并理解本文件以及项目中的核心 SDD 文件。

---

## 1. 背景说明

UAW 项目当前使用一套定制化 SDD 流程。

这里的 SDD 指的是：

> Spec-Driven Development  
> 即以规格说明、设计文档、任务拆解和流程审计为核心的开发流程。

这套体系的目标不是简单让 AI 生成代码，而是让 AI 在受控流程下完成：

1. 需求理解
2. 规格说明生成
3. 设计方案生成
4. 任务拆解
5. 代码实现
6. 代码评审
7. 基于评审结果自动修复
8. 单元测试生成
9. 归档总结
10. 流程状态和过程审计记录

核心目标是：

- 防止 AI 跳阶段
- 防止 AI 一次性生成多个下游文件
- 防止 AI 没有人工确认就写代码
- 防止 AI 乱建目录和文件
- 防止 AI 跳过代码评审和单元测试
- 防止 archive.md 在前置流程没完成时提前生成
- 让每个阶段都有明确状态和过程审核轨迹
- 让 SDD 内部 Code Review 和独立代码评审任务边界清晰

---

## 2. 这套体系最初要解决的问题

UAW-SDD 体系使用一段时间后，暴露过以下问题：

1. Proposal 之后，偶尔会一次性生成 `spec.md`、`design.md`、`tasks.md` 三个文件。
2. 有时 `spec.md` 生成之后，流程会直接进入代码实现。
3. `proposal-input.md`、`spec.md`、`design.md`、`tasks.md` 文件目录和格式有时混乱，没有按约定格式生成。
4. 整个 SDD 流程中，有时会产生约定之外的目录和文件。
5. Fast Lane 有时被误当成直接代码实现模式。
6. `spec.md`、`design.md`、`tasks.md` 有时流程已经进入下一阶段，但底部状态没有更新。
7. tasks 阶段尤其不稳定：有时没有生成代码，却直接生成 `archive.md`。
8. 有时整个流程看起来正常跑完，但底部 `Process Status` 和 `Process Audit Trail` 没有更新。
9. tasks 阶段之后，代码评审、单元测试、归档执行不一致，单元测试有时会被跳过。
10. archive.md 有时被生成成泛泛总结，而不是流程闭环证据。

为解决上述问题，当前体系已经增加了：

1. 严格阶段闸门
2. 人工确认闸门
3. Code Review 环节
4. Review-driven Auto-fix 环节
5. Unit Test Generation 环节
6. Unit Test Summary 环节
7. Fast Lane 完整流程定义
8. Process Status
9. Process Audit Trail
10. 允许 / 禁止产物边界
11. SDD 内部 Code Review 与独立 Git 范围 Code Review 的入口分离

---

## 3. 当前核心文件结构

当前 SDD 体系核心文件包括：

```text
.project-ai/context/1.index.md
.project-ai/templates/1.proposal-input-template.md
.project-ai/templates/2.spec-template.md
.project-ai/templates/3.design-template.md
.project-ai/templates/4.tasks-template.md
.project-ai/templates/5.archive-template.md
.project-ai/rules/code-review/UAW-Code-Review.md
.project-ai/templates/code-review/代码评审统计报告模板_总.html
.project-ai/templates/code-review/个人代码评审报告模板.html
.project-ai/rules/testing/
```

其中：

```text
.project-ai/context/1.index.md
```

是整个 SDD 体系的中央路由文件，负责定义：

- Standard Lane
- Fast Lane
- 阶段闸门
- 人工确认闸门
- 允许输出产物
- 禁止输出产物
- Code Review 规则入口
- Unit Test 规则入口
- Archive 进入条件
- 违规处理机制

---

## 4. 每个功能的资产目录

每个功能或需求的 SDD 产物必须放在：

```text
.project-features/<SprintN>/<feature-name>/
```

该目录下通常包含：

```text
proposal-input.md
spec.md
design.md
tasks.md
archive.md
```

允许在该功能目录下生成流程相关产物。

禁止在约定外目录随机生成：

- summary 文件
- notes 文件
- todo 文件
- temp 文件
- tasksg.md 等拼写错误文件
- 未批准的额外目录
- 未批准的报告目录

---

## 5. Standard Lane 标准流程

标准 SDD 流程必须按以下顺序执行：

```text
Proposal
→ Spec
→ 人工确认
→ Design
→ 人工确认
→ Tasks
→ 人工确认
→ Code Implementation
→ SDD_TASK_CODE_REVIEW
→ Review-driven Auto-fix
→ Unit Test Generation
→ Unit Test Summary
→ Archive
```

关键规则：

1. Proposal 之后只允许生成 `spec.md`。
2. `spec.md` 未经过人工确认，不允许生成 `design.md`。
3. `design.md` 未经过人工确认，不允许生成 `tasks.md`。
4. `tasks.md` 未经过人工确认，不允许开始代码实现。
5. 代码实现后必须进入 `SDD_TASK_CODE_REVIEW`。
6. Code Review 后必须根据 Findings 进行 Review-driven Auto-fix。
7. Auto-fix 后必须进入 Unit Test Generation。
8. Unit Test Summary 完成后，才允许进入 Archive。
9. `archive.md` 不能在 Code Review、Auto-fix、Unit Test Summary 完成之前生成。

---

## 6. Fast Lane 流程

Fast Lane 是简化但受控的 SDD 流程，不是直接写代码模式。

Fast Lane 必须按以下顺序执行：

```text
Fast Lane Proposal
→ Fast Lane Mini Spec
→ Fast Lane Mini Tasks
→ 人工确认
→ Code Implementation
→ SDD_TASK_CODE_REVIEW
→ Review-driven Auto-fix
→ Unit Test Generation
→ Unit Test Summary
→ Archive / archive-lite
```

Fast Lane 禁止：

1. 从 Fast Lane Proposal 直接生成代码。
2. 跳过 Fast Lane Mini Spec。
3. 跳过 Fast Lane Mini Tasks。
4. 跳过人工确认。
5. 跳过 `SDD_TASK_CODE_REVIEW`。
6. 跳过 Review-driven Auto-fix。
7. 跳过 Unit Test Summary。
8. 在 Code Review 和 Unit Test 完成前生成 archive 或 archive-lite。

---

## 7. Code Review 两种入口

当前代码评审体系有两个入口，必须严格区分。

---

### 7.1 SDD_TASK_CODE_REVIEW

这是 SDD 流程内部入口。

触发时机：

```text
tasks.md 已确认
→ 代码实现完成
→ SDD 流程内部直接调用 UAW-Code-Review.md 中的代码评审规则
```

重要规则：

1. 不需要用户手动填写 Entry Mode。
2. 不需要用户手动填写 Feature Directory。
3. 不需要用户手动列出 SDD Artifacts。
4. 默认当前功能目录下已经存在：
   - `proposal-input.md`
   - `spec.md`
   - `design.md`
   - `tasks.md`
5. 必须结合 `proposal-input.md`、`spec.md`、`design.md`、`tasks.md` 判断代码是否符合 SDD 约束。
6. 只输出 Code Review Findings。
7. 不生成 HTML 报告。
8. 不读取 HTML 报告模板。
9. 不创建 `reports/code-review/YYYY-MM-DD/` 目录。
10. Code Review Findings 输出后，必须进入 Review-driven Auto-fix。
11. Auto-fix 后必须进入 Unit Test Generation。
12. Unit Test 必须遵守 `.project-ai/rules/testing/`。

`SDD_TASK_CODE_REVIEW` 是流程质量闸门，不是报告任务。

---

### 7.2 STANDALONE_GIT_RANGE_REVIEW

这是独立代码评审任务。

适用场景：

- 手动指定 Git 范围做代码检查
- 按 branch diff 审核
- 按 commit list 审核
- 按 date range 审核
- 生成团队或个人代码评审报告

重要规则：

1. 不遵守 SDD 流程闸门。
2. 不强制读取 `proposal-input.md`、`spec.md`、`design.md`、`tasks.md`。
3. 不自动修复代码。
4. 不进入 Unit Test Generation。
5. 必须按照指定 Git 范围进行代码审核。
6. 必须读取并使用两个 HTML 模板。
7. 必须生成总览报告和个人报告。

独立评审入口需要明确输入，例如：

```text
Entry Mode: STANDALONE_GIT_RANGE_REVIEW
Review Scope Type: branch diff / commit list / date range
Base branch:
Target branch:
Commit hashes:
Start time:
End time:
Report Output Directory:
Report Output Date:
```

---

## 8. HTML 模板使用边界

以下两个 HTML 模板只允许在 `STANDALONE_GIT_RANGE_REVIEW` 模式下使用：

```text
.project-ai/templates/code-review/代码评审统计报告模板_总.html
.project-ai/templates/code-review/个人代码评审报告模板.html
```

`SDD_TASK_CODE_REVIEW` 模式禁止：

1. 读取这两个 HTML 模板。
2. 生成 HTML 报告。
3. 创建 `reports/code-review/YYYY-MM-DD/` 目录。
4. 输出总览报告或个人报告。

HTML 模板必须与 `UAW-Code-Review.md` 中的占位符契合清单保持一致。

如果模板新增、删除或修改占位符，必须同步更新 `UAW-Code-Review.md` 中的占位符说明。

---

## 9. UAW-Code-Review.md 当前设计原则

`UAW-Code-Review.md` 是代码评审规则文件，不是单纯提示词。

它必须同时服务两个入口：

1. `SDD_TASK_CODE_REVIEW`
2. `STANDALONE_GIT_RANGE_REVIEW`

但两个入口的执行方式不同：

```text
SDD_TASK_CODE_REVIEW:
- 内部流程调用
- 结合 SDD 产物评审
- 输出 Findings
- 进入 Auto-fix
- 进入 Unit Test
- 不生成 HTML 报告

STANDALONE_GIT_RANGE_REVIEW:
- 人工指定 Git 范围
- 不依赖 SDD 产物
- 不自动修复
- 生成 HTML 报告
```

代码评审规则本身应保持通用，不得写死某个业务模块。

例如：

- 不得把 transaction 模块结构写成全局唯一标准。
- 可以把 transaction 文档抽象为“模块架构与包结构一致性”的通用规则。
- 应先识别当前模块结构，再依据当前模块已有结构、设计文档和项目约定进行评审。

---

## 10. 架构评审规则当前原则

`UAW-Code-Review.md` 中的架构评审不应硬编码某个具体模块。

正确原则是：

```text
先识别模块
→ 再识别该模块已有结构
→ 再结合 design.md / 同类模块 / 模块规范文档判断新增代码是否落位正确
```

如果模块采用类似结构：

```text
<module>/
├── base/
├── common/
├── core/
└── support/
```

则按该结构检查。

如果模块采用普通 MVC 或分层结构，则按 Controller / Service / DAO / Mapper / Helper / Converter / Strategy 等职责边界检查。

不得强制所有模块使用 transaction 的目录结构。

---

## 11. Code Review 规则范围

`UAW-Code-Review.md` 中的代码评审规则应覆盖：

1. 模块架构与包结构一致性
2. 业务逻辑正确性
3. 代码质量与可维护性
4. UAW 工具类与项目规范
5. 数据库与性能
6. 安全与权限
7. 单元测试
8. 日志与可观测性
9. 外部接口与远程调用
10. 事务、幂等与重复提交
11. 配置与环境差异
12. 异常处理与错误返回
13. DTO / VO / BO / Entity 边界
14. Converter / Helper / Strategy 职责边界
15. 依赖方向和循环依赖风险

评审规则不得因为入口不同而降低质量，但两个入口的执行方式、输入依据和输出要求必须严格区分。

---

## 12. Tasks 检查项标记规则

`tasks.md` 中所有检查项必须实际检查后更新标记。

规则：

```text
[✓]：已检查，且发现问题 / 不满足 / 有阻塞
[x]：已检查，且无问题 / 已满足 / 可通过
[ ]：仅允许作为模板初始占位
```

生成或更新 `tasks.md` 后，不允许继续保留未处理的 `[ ]`。

进入以下阶段前，如果仍有 `[ ]`，必须停止：

- Code Implementation
- `SDD_TASK_CODE_REVIEW`
- Review-driven Auto-fix
- Unit Test Generation
- Archive

不适用项也不能留空，必须写成：

```text
[x] 不适用：原因……
```

---

## 13. Archive 检查项标记规则

`archive.md` 中所有归档判断项也必须执行检查。

规则：

```text
[✓]：已检查，且存在问题 / 不满足 / 有阻塞
[x]：已检查，且无问题 / 已满足 / 不适用并已说明原因
[ ]：仅允许作为模板初始占位
```

正式归档前不得保留 `[ ]`。

如果存在 `[✓]`，必须在 Process Deviations 或 Remaining Risks 中说明原因和后续处理方式。

---

## 14. Process Status 与 Process Audit Trail

每个核心流程文件底部必须包含：

```markdown
## Process Status

- Current Stage:
- Stage Status:
- Last Completed Step:
- Next Required Step:
- Human Confirmation Required:
- Allowed Next Action:
- Forbidden Next Action:
- Updated At:
```

以及：

```markdown
## Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
```

规则：

1. 进入下一阶段前，必须更新当前文件的 Process Status。
2. 进入下一阶段前，必须更新当前文件的 Process Audit Trail。
3. 未更新状态，不允许进入下一阶段。
4. 生成 `archive.md` 前，`proposal-input.md`、`spec.md`、`design.md`、`tasks.md` 都必须处于最终可归档状态。
5. 如果阶段被跳过或不适用，必须写明原因。
6. 禁止静默跳过。

---

## 15. 当前已经完成的主要调整

当前已经围绕 UAW-SDD 体系完成以下工作。

### 15.1 修复 SDD 主流程

已将代码实现后的流程调整为：

```text
Code Implementation
→ SDD_TASK_CODE_REVIEW
→ Review-driven Auto-fix
→ Unit Test Generation
→ Unit Test Summary
→ Archive
```

### 15.2 定义 Code Review 两入口

已明确：

```text
SDD_TASK_CODE_REVIEW:
内部调用，不生成报告，只输出 Findings 并进入修复和单测。

STANDALONE_GIT_RANGE_REVIEW:
独立任务，按 Git 范围评审，生成 HTML 报告。
```

### 15.3 更新 UAW-Code-Review.md

已完成：

- 删除 SDD 模式人工输入格式
- 保留 Standalone 模式输入格式
- 补回 HTML 模板占位符契合清单
- 重写模块架构与包结构一致性规则
- 避免把 transaction 模块写死为全局规则
- 补充外部接口、事务、幂等、配置、安全、测试等评审维度

### 15.4 更新 HTML 模板

已确定两个模板只服务 `STANDALONE_GIT_RANGE_REVIEW`：

```text
代码评审统计报告模板_总.html
个人代码评审报告模板.html
```

模板必须和 `UAW-Code-Review.md` 中的占位符契合清单保持一致。

### 15.5 更新流程模板

已围绕以下问题多轮修正：

- Proposal 后不能直接生成多个文件
- Spec 后不能直接写代码
- Fast Lane 不能直接写代码
- Tasks 后不能跳过 Code Review
- Code Review 后必须进入 Auto-fix
- Auto-fix 后必须进入 Unit Test
- Unit Test Summary 前不能 Archive
- Process Status / Audit Trail 必须更新
- 约定外目录和文件禁止生成

---

## 16. 接手后必须先做什么

接手后不要立刻修改文件。

必须先执行体系审核。

### 16.1 先读取核心文件

读取：

```text
.project-ai/context/1.index.md
.project-ai/templates/1.proposal-input-template.md
.project-ai/templates/2.spec-template.md
.project-ai/templates/3.design-template.md
.project-ai/templates/4.tasks-template.md
.project-ai/templates/5.archive-template.md
.project-ai/rules/code-review/UAW-Code-Review.md
.project-ai/templates/code-review/代码评审统计报告模板_总.html
.project-ai/templates/code-review/个人代码评审报告模板.html
.project-ai/rules/testing/
```

### 16.2 再做一致性审核

重点审核：

1. Standard Lane 是否全文件一致。
2. Fast Lane 是否全文件一致。
3. `SDD_TASK_CODE_REVIEW` 是否不生成报告。
4. `STANDALONE_GIT_RANGE_REVIEW` 是否只在独立代码评审中生成报告。
5. HTML 模板是否只给 Standalone 使用。
6. `UAW-Code-Review.md` 占位符清单是否覆盖 HTML 模板全部占位符。
7. `tasks.md` 检查项规则是否无冲突。
8. `archive.md` 检查项规则是否无冲突。
9. Process Status / Audit Trail 是否所有核心模板都有。
10. Archive 前置条件是否完整。
11. Unit Test 是否强制引用 `.project-ai/rules/testing/`。
12. 是否还有旧流程残留描述。
13. 是否还有约定外目录输出。
14. 是否还有让 AI 自行猜测入口、目录、阶段的描述。
15. Code Review 规则是否仍保持通用，而不是绑定某个业务模块。

### 16.3 最后再提出修复计划

如果发现问题，必须先输出：

```text
发现的问题：
影响文件：
风险等级：
建议修复方式：
是否需要修改文件：
```

确认后再修改。

---

## 17. 重要执行纪律

不要重新发明一套新的 SDD 流程。

不要把当前体系推翻重来。

不要创造新概念来替代已有核心概念。

不要把 `SDD_TASK_CODE_REVIEW` 又改回报告任务。

不要让 Standalone 代码评审依赖 SDD 阶段闸门。

不要把某个业务模块结构写死成全局架构规则。

不要在没有依据的情况下修改 HTML 模板结构。

不要删除 HTML 模板占位符契合清单。

不要保留旧流程的幽灵描述。

不要创建新的目录规范，除非已有规范明显无法支撑需求。

不要让 AI 自行猜测入口、目录、阶段、输出路径或工作模式。

每一项修改都必须能对应到：

1. 已观察到的问题；
2. 已确认的流程规则；
3. 文件之间的一致性缺口；
4. 明确的可维护性或可审计性风险。

你的目标是维护当前 UAW-SDD 体系，让它更严格、更确定、更可审计、更少歧义。