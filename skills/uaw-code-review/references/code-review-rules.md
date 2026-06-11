# UAW-Code-Review.md

> 本文件定义 UAW 项目的代码评审规则。
> 本文件支持三个入口。不同入口的输入依据、执行流程、输出内容和后续动作不同，禁止混用。
>
> - `SDD_TASK_CODE_REVIEW`：SDD 流程内入口。用于 `tasks.md` 完成代码实现后，执行代码审核，输出 `code-review-findings.md`，并进入 Review-driven Auto-fix 与 Unit Test。**不生成 HTML 报告，不读取 HTML 模板。**
> - `STANDALONE_GIT_RANGE_REVIEW`：独立 Git 范围评审入口。用于人工指定 branch / commit / date range 做独立代码检查与审核。**不遵守 SDD 阶段闸门，不自动修复代码，必须按 HTML 模板生成报告。**
> - `STANDALONE_WORKTREE_SNAPSHOT_REVIEW`：独立工作区快照评审入口。仅用于未提交的新工程、临时 demo、迁移前代码盘点等无法提供 Git range 的场景。**必须显式记录 Target Path 与 Scope Deviation，必须生成 HTML 报告，但不得作为正式合并闸门。**

> 如果用户要求“评审整个工程 / 目录 / 未提交 demo”，不得静默伪装成 `STANDALONE_GIT_RANGE_REVIEW`。必须改用 `STANDALONE_WORKTREE_SNAPSHOT_REVIEW`，并在报告中标明“非 Git range，只代表当前工作区快照”。

---

# 1. 角色定位

你是 UAW 项目的 AI 代码评审代理。

你的任务不是重新设计需求，不是随意重构项目，也不是扩大实现范围。你的任务是根据调用上下文执行代码检查与审核，并按对应入口要求输出可追溯结果。

入口由调用上下文确定：

1. 当本文件被 SDD 流程中的 `tasks.md` 在代码实现后调用时，默认进入 `SDD_TASK_CODE_REVIEW` 模式。该模式不需要用户额外提供输入格式，当前功能目录、SDD 产物和实现范围由 SDD 流程上下文提供。
2. 当用户单独发起代码评审任务，并显式指定 Git 范围时，进入 `STANDALONE_GIT_RANGE_REVIEW` 模式。该模式必须提供独立评审输入参数。
3. 当用户单独发起代码评审任务，只指定工程目录 / 模块目录 / 未提交工作区时，进入 `STANDALONE_WORKTREE_SNAPSHOT_REVIEW` 模式。该模式必须记录目标路径和范围偏差。

如果当前调用既不是 SDD 流程上下文，也没有提供独立 Git 范围或工作区快照范围，必须停止并要求补充评审范围，不得自行猜测。

---

# 2. 三个入口的强制区别

| 项目 | SDD_TASK_CODE_REVIEW | STANDALONE_GIT_RANGE_REVIEW | STANDALONE_WORKTREE_SNAPSHOT_REVIEW |
|---|---|---|---|
| 使用场景 | SDD 的 tasks 生成代码后自动触发 | 人工指定 Git 范围单独评审 | 人工指定未提交工程目录 / 模块目录快照 |
| 是否遵守 SDD 体系 | 是 | 否 | 否 |
| 是否读取 proposal/spec/design/tasks | 必须读取 | 不需要，除非用户明确要求 | 不需要，除非用户明确要求 |
| 是否执行 SDD 阶段闸门 | 必须执行 | 不执行 | 不执行 |
| 是否生成 HTML 报告 | 不生成 | 必须生成 | 必须生成 |
| 是否读取 HTML 模板 | 不读取 | 必须读取 | 必须读取 |
| 是否创建 reports/code-review 目录 | 不创建 | 按用户指定目录生成 | 按用户指定目录生成 |
| 输出目标 | `code-review-findings.md` → Auto-fix → Unit Test | 总览报告 + 个人报告 | 总览报告 + 个人报告 + Scope Deviation |
| 是否自动修复代码 | 必须根据 Findings 修复 | 不默认修复，只输出审核报告 | 不默认修复，只输出审核报告 |
| 是否归档到 archive | 作为 SDD 后续流程输入 | 不参与 SDD archive | 不参与 SDD archive，不得作为正式合并闸门 |

禁止：

1. 把 SDD 模式当成独立报告模式。
2. 把独立 Git 范围评审或工作区快照评审当成 SDD 流程阶段。
3. 在 SDD 模式下生成 HTML 报告。
4. 在 SDD 模式下读取 HTML 模板。
5. 在独立模式下强制读取 SDD 产物或执行 SDD 阶段闸门。
6. 用 Standalone 报告替代 SDD 内部 `code-review-findings.md`。
7. 把未提交目录快照静默伪装为 Git range。

---

# 3. SDD_TASK_CODE_REVIEW 模式

## 3.1 调用方式

`SDD_TASK_CODE_REVIEW` 不是人工单独启动的输入模式，而是 SDD 流程内部的代码评审规则调用。

当 `tasks.md` 中的代码实现阶段完成后，SDD 流程直接调用本文件中的评审规则执行代码审核。

该模式下：

1. 不要求用户填写 `Entry Mode`。
2. 不要求用户填写 Feature Directory。
3. 不要求用户重复列出 SDD Artifacts。
4. 默认当前工作目录就是对应功能资产目录。
5. 默认 `proposal-input.md`、`spec.md`、`design.md`、`tasks.md` 与当前任务处于同一功能目录。
6. 评审结果必须写入当前功能目录的 `code-review-findings.md`，并进入 Review-driven Auto-fix 和 Unit Test。
7. 禁止生成 HTML 报告，禁止读取 HTML 模板，禁止创建报告目录。

## 3.2 前置条件

必须确认：

1. `proposal-input.md` 存在。
2. `spec.md` 已确认。
3. `design.md` 已确认。
4. `tasks.md` 已确认。
5. 代码实现已完成。
6. 当前任务尚未 archive。
7. `tasks.md` 中所有检查项已按规则更新为 `[✓]` 或 `[x]`，不得遗留 `[ ]`。

如任一条件不满足，必须停止并输出阻塞原因。

## 3.3 必须读取内容

必须读取：

```text
./proposal-input.md
./spec.md
./design.md
./tasks.md
skills/uaw-sdd-ai-coding/references/context/routing-index.md
skills/uaw-sdd-ai-coding/references/process-control.md
skills/uaw-sdd-ai-coding/references/rules/
skills/uaw-unit-test/references/java/
```

不得读取 HTML 模板：

```text
skills/uaw-code-review/references/templates/summary-report-template.html
skills/uaw-code-review/references/templates/personal-report-template.html
```

## 3.4 评审范围确定

SDD 模式不要求人工指定 branch / commit / date range。

必须基于以下信息确定本次实现变更范围：

1. `tasks.md` 中声明的实施任务与允许修改范围。
2. 当前工作区变更文件。
3. 当前分支相对上游分支的 Git Diff。
4. 任务实施摘要或变更文件清单。

如果无法确定本次实现范围，必须停止并要求补充变更文件清单或 Git Diff 范围。

## 3.5 SDD 模式必查项

必须检查：

1. 实现是否符合 `spec.md` 的范围、边界、验收标准。
2. 实现是否符合 `design.md` 的包、类、流程、异常、数据流转设计。
3. 实现是否完成 `tasks.md` 的所有确认任务。
4. 是否出现未批准的范围扩张。
5. 是否创建约定之外的目录或文件。
6. 是否违反模块包结构、依赖方向、工具类、日志、异常、安全、权限、数据访问规范。
7. 是否遗漏必要单元测试。
8. 是否存在 P0 / P1 / P2 / Suggestion 问题。

## 3.6 SDD 模式输出

SDD 模式不得生成 HTML 报告。

必须在当前功能目录生成：

```text
./code-review-findings.md
```

`code-review-findings.md` 必须包含以下内容，作为后续 Review-driven Auto-fix 输入：

```text
Code Review Conclusion: 拒绝通过 / 有条件通过 / 通过
P0 Count:
P1 Count:
P2 Count:
Suggestion Count:
Review-driven Auto-fix Required: yes / no
Fix Scope:
Files allowed to modify:
Files forbidden to modify:
Unit tests required: yes / no
Unit test focus:
Archive allowed: yes / no
```

规则：

1. `code-review-findings.md` 是 SDD 内部 Markdown 质量闸门产物。
2. `code-review-findings.md` 不得使用 HTML 报告模板。
3. `code-review-findings.md` 不得放入 `reports/code-review/YYYY-MM-DD/` 目录。
4. `tasks.md` 和 `archive.md` 必须引用该文件。

## 3.7 Code Review Findings 格式

```text
问题编号：
严重程度：P0 / P1 / P2 / Suggestion
问题类型：
文件路径：
方法 / 类：
Diff 位置：
关联 SDD 依据：spec / design / tasks 中的对应章节
问题描述：
风险影响：
修复建议：
是否阻塞 Archive：yes / no
```

## 3.8 SDD 模式自动修复规则

Code Review 完成后必须进入 Review-driven Auto-fix。

规则：

1. 存在 P0：必须修复，禁止进入 Unit Test 和 Archive。
2. 存在 P1：必须给出修复计划并优先修复，修复完成前禁止 Archive。
3. P2 可按影响决定是否本轮修复，但必须记录处理策略。
4. Suggestion 可不修复，但必须记录理由。
5. 修复范围只能限于 Findings 指出的文件和为修复所需的测试文件。
6. 禁止借修复扩大需求范围。
7. 修复后必须输出 Auto-fix Summary。
8. Auto-fix 后必须进入 Unit Test Generation / Unit Test Summary。
9. Auto-fix Summary 必须回写到 `tasks.md` 和 `archive.md`，并与 `code-review-findings.md` 的问题编号一致。
10. Auto-fix 后必须执行一次轻量复核，明确区分修复前 Code Review 闸门结论与修复后最终 Archive 闸门结论。
11. 复核结果必须记录为 `Post Auto-fix Verification`，写入 `code-review-findings.md` 或 `auto-fix-summary.md`。
12. 存在未修复 P0 / P1，或仍影响验收的 P2 时，禁止进入 Archive。

`Post Auto-fix Verification` 必须包含：

```text
Post Auto-fix Verification:
- Recheck Result: passed / failed
- Rechecked Issues:
- Remaining P0 / P1 / Blocking P2:
- Archive allowed after Auto-fix: yes / no
- Next Gate:
```

## 3.9 Auto-fix Summary 格式

```text
Auto-fix Summary:
- Fixed Issues:
- Modified Files:
- Test Files Added / Updated:
- Issues Not Fixed:
- Reason:
- Remaining Risks:
```

---

# 4. STANDALONE_GIT_RANGE_REVIEW 模式

## 4.1 输入格式

`STANDALONE_GIT_RANGE_REVIEW` 是人工单独启动的代码评审任务，必须显式提供以下输入。

```text
Entry Mode: STANDALONE_GIT_RANGE_REVIEW
Review Scope Type: branch diff / commit list / date range
Report Output Directory: <指定报告输出目录>
Report Output Date: YYYY-MM-DD
```

该模式是独立代码检查与审核任务，不属于 SDD 流程。

规则：

1. 不要求读取 `proposal-input.md`、`spec.md`、`design.md`、`tasks.md`。
2. 不执行 SDD 阶段闸门。
3. 不检查 SDD 流程状态。
4. 不要求 Auto-fix。
5. Standalone 模式不得自动修改代码，除非用户另行明确要求。
6. 必须按指定 Git 范围做代码检查与审核。
7. 必须按 HTML 模板生成总览报告和个人报告。

## 4.2 HTML 模板固定路径

必须读取：

```text
skills/uaw-code-review/references/templates/summary-report-template.html
skills/uaw-code-review/references/templates/personal-report-template.html
```

这两个模板仅允许在 `STANDALONE_GIT_RANGE_REVIEW` 或 `STANDALONE_WORKTREE_SNAPSHOT_REVIEW` 模式下使用。

禁止使用：

```text
.gemini/
Desktop/
临时目录/
```

## 4.3 报告输出

独立模式必须根据用户指定的 `Report Output Directory` 输出报告。

Standalone 模式不属于 SDD 流程，不得默认创建 SDD feature directory；只有用户明确指定时，才允许输出到 `sdd2-features/.../reports/code-review/...`。

推荐路径：

```text
reports/code-review/YYYY-MM-DD/
```

说明：`sdd2-features` 是 SDD2.x 主版本线默认功能资产根目录，小版本升级不得自动改成 `sdd2.1-features` 等新目录。Standalone code review 默认不依赖该目录。

如用户指定其他内网目录，也可使用，但必须明确记录。

输出文件：

```text
代码评审统计报告.html
{开发者姓名}_代码评审报告.html
```

## 4.3.1 Worktree Snapshot 输入格式

`STANDALONE_WORKTREE_SNAPSHOT_REVIEW` 仅用于无法提供 Git range 的临时场景。该模式必须显式提供以下输入：

```text
Entry Mode: STANDALONE_WORKTREE_SNAPSHOT_REVIEW
Review Scope Type: worktree snapshot
Target Path: <工程目录或模块目录>
Include Untracked Files: yes / no
Baseline: none / current HEAD / specified ref
Report Output Directory: <指定报告输出目录>
Report Output Date: YYYY-MM-DD
Formal Merge Gate: no
```

规则：

1. 必须读取 `Target Path` 下的源代码、测试代码、构建配置和 README / 文档。
2. 必须排除 `target/`、`build/`、`.idea/`、`.DS_Store`、生成报告目录和其他构建产物。
3. 必须在 HTML 报告首页标明 `Scope Deviation: worktree snapshot, not Git range`。
4. 必须将文件数、总代码行数、未跟踪文件列表作为统计依据。
5. 不得输出“提交统计”为真实 Git 提交；若无提交，提交数必须写 0 或 N/A。
6. 不得将该报告作为正式合并闸门；正式合并前必须重新执行 `STANDALONE_GIT_RANGE_REVIEW`。
7. 如果用户要求该模式自动修复代码，必须另起任务并明确修复范围；本模式默认只评审不修复。

## 4.4 branch diff 输入示例

```text
Entry Mode: STANDALONE_GIT_RANGE_REVIEW
Review Scope Type: branch diff
Base branch: origin/develop
Target branch: HEAD
Exclude merge commits: yes
Exclude generated files: yes
Report Output Directory: reports/code-review/2026-06-09/
Report Output Date: 2026-05-27
```

命令：

```bash
git fetch origin
git diff --stat <base-branch>...<target-branch>
git diff --name-only <base-branch>...<target-branch>
git diff --unified=80 --find-renames <base-branch>...<target-branch>
git log --no-merges <base-branch>...<target-branch> --pretty=format:"%H|%an|%ae|%ad|%s"
```

## 4.5 commit list 输入示例

```text
Entry Mode: STANDALONE_GIT_RANGE_REVIEW
Review Scope Type: commit list
Commit hashes:
- abc123
- def456
Exclude generated files: yes
Report Output Directory: reports/code-review/2026-06-09/
Report Output Date: 2026-05-27
```

命令：

```bash
git show --stat <commit-hash>
git show --name-only <commit-hash>
git show --unified=80 --find-renames <commit-hash>
```

## 4.6 date range 输入示例

```text
Entry Mode: STANDALONE_GIT_RANGE_REVIEW
Review Scope Type: date range
Start time: 2026-05-27 00:00:00
End time: 2026-05-27 23:59:59
Target branch: develop
Exclude merge commits: yes
Exclude generated files: yes
Report Output Directory: reports/code-review/2026-06-09/
Report Output Date: 2026-05-27
```

命令：

```bash
git log --no-merges --since="<start-time>" --until="<end-time>" --pretty=format:"%H|%an|%ae|%ad|%s"
git show --stat <commit-hash>
git show --name-only <commit-hash>
git show --unified=80 --find-renames <commit-hash>
```

---

# 5. 通用 Diff 分析边界

1. 问题判定必须基于本次 Git Diff 中新增或修改的代码行。
2. 可以读取相关上下文文件，例如同一类、接口、DTO、VO、PO、RO、Mapper、Repository、测试文件和配置文件。
3. 读取上下文只是为了理解本次变更，不得把未修改的历史代码直接当成本次问题输出。
4. 如果问题来自历史代码，但本次变更触发、放大或依赖了该问题，必须标记为“历史问题，本次变更相关”。
5. 自动生成文件、格式化调整、版本号调整、纯注释调整必须单独标记，避免误判。
6. 不得为了凑问题数量制造低价值问题。

---

# 6. 异常提交检测

## 6.1 Standalone 模式

满足以下任一条件，标记为异常提交：

1. 单次提交总变更行数 > 500 行。
2. 单次提交涉及文件数 > 20 个。
3. 同一开发者 30 分钟内提交次数 > 5 次。
4. 单次提交包含大量自动生成文件、格式化文件或批量迁移文件。
5. 单次提交同时修改多个无明显关联的业务模块。

异常提交不直接进入逐行详细评审，必须在报告中单独说明原因、影响和拆分建议。

## 6.2 SDD 模式

SDD 模式下如发现类似异常，只作为 Code Review Finding 记录，不生成异常提交报告。

---

# 7. 评审维度

本章定义通用代码评审维度。

不同入口的执行方式不同：

- `SDD_TASK_CODE_REVIEW`：结合 SDD 产物判断实现是否符合已确认的范围、设计、任务和允许修改边界，并输出 `code-review-findings.md`，随后进入 Review-driven Auto-fix 和 Unit Test。
- `STANDALONE_GIT_RANGE_REVIEW`：仅基于用户指定的 Git 范围执行，不强制读取 SDD 产物，不自动修复代码，必须按 HTML 模板生成报告。
- `STANDALONE_WORKTREE_SNAPSHOT_REVIEW`：仅基于用户指定的工作区目录快照执行，不强制读取 SDD 产物，不自动修复代码，必须按 HTML 模板生成报告，并标明不是正式 Git range。

三个入口可以共用评审维度，但不得混用执行流程、输入依据和输出要求。

## 7.1 模块架构与包结构一致性

评审目标：检查新增或修改代码是否符合当前功能模块的既有包结构、职责边界和依赖方向。

本规则不得把某一个业务模块的目录结构硬编码为全项目唯一标准。评审时必须先识别当前变更所属模块，再基于该模块已有结构、相关设计文档、模块规范文档和项目约定进行判断。

### 7.1.1 模块结构识别规则

评审前必须先判断本次变更属于哪类模块结构：

1. 如果变更位于已有业务模块下，必须优先遵守该模块当前已存在的目录结构和命名方式。
2. 如果存在对应的模块结构规范文档，必须读取并作为评审依据。
3. 如果 `design.md` 明确规定了新增类、包、层级或落位，必须优先以 `design.md` 为准。
4. 如果是独立 Git 范围评审或工作区快照评审且没有 SDD 产物，则以当前代码仓库中同类模块的既有结构为主要依据。
5. 不得仅凭通用分层模型强行要求所有模块都使用同一种目录结构。

### 7.1.2 通用模块分层检查

如果某个业务模块采用类似以下结构：

```text
<module>/
├── base/       # 基础能力：常量、基础模型、基础接口、基础控制器
├── common/     # 公共能力：跨业务场景复用逻辑
├── core/       # 核心业务：具体业务域、工单类型、交易类型或功能模块
└── support/    # 支撑能力：工具、缓存、校验、通用技术支撑
```

则必须按以下规则检查。

#### base 层

`base/` 应仅承载模块级基础能力，包括：模块常量、基础路径、基础标签、基础模型、基础接口、抽象控制器或抽象服务。

禁止：写具体业务流程、访问数据库、调用外部系统、放置仅服务单一业务场景的代码。

#### common 层

`common/` 应承载跨业务场景复用能力，包括：跨模块复用查询、通用业务处理、公共协议处理、公共 ID 生成、可被多个 core 子模块复用的服务。

禁止：放置只属于单个具体业务模块的私有逻辑、承担具体业务模块主流程、依赖某个 core 子模块的私有实现、与 core 子模块形成循环依赖。

#### core 层

`core/` 应承载具体业务模块。常见结构包括：

```text
core/<business-module>/
├── controller/
├── dao/
│   ├── entity/
│   └── mapper/
├── enums/
├── pojo/
│   ├── bo/
│   ├── dto/
│   └── vo/
└── service/
    ├── converter/
    ├── helper/
    ├── impl/
    └── strategy/
```

检查重点：

1. 每个具体业务域是否有独立目录。
2. 新增类是否落在正确业务子模块。
3. Controller 是否只处理入口适配、参数校验和响应返回。
4. Service 是否承载业务流程、事务控制和业务编排。
5. DAO / Mapper 是否只处理数据访问。
6. Entity 是否只表达数据库表结构或持久化对象。
7. Helper 是否封装复杂但可复用的业务辅助逻辑。
8. Converter 是否只处理 BO / DTO / VO / Entity 转换。
9. Strategy 是否只承载不同业务场景下的策略差异。

禁止：

1. Controller 中写复杂业务流程。
2. Controller 直接访问 DAO / Mapper。
3. Service 直接拼接 SQL。
4. DAO / Mapper 承担业务决策。
5. Helper 变成无边界的杂物类。
6. Converter 中混入业务规则。
7. Strategy 中复制大量公共逻辑。
8. 将新业务代码放入错误业务子模块。
9. 为了新增一个小功能创建过度复杂的包结构。

#### support 层

`support/` 应承载模块支撑能力，包括工具类、缓存能力、重复提交校验、通用校验能力、技术支撑组件。

禁止：写具体业务流程、依赖 core 的具体业务实现、放置只服务单一业务模块的私有逻辑、重复创建项目已有工具类能力。

### 7.1.3 通用 MVC / 分层职责检查

如果当前模块不是 `base/common/core/support` 结构，而是普通分层结构，也必须检查以下职责边界。

#### Controller 层

允许：接收请求、参数校验、调用 Service、返回响应结果。

禁止：写复杂业务逻辑、直接访问数据库、直接调用 Mapper、拼接 SQL、处理复杂状态流转。

#### Service 层

允许：实现业务流程、做事务控制、调用 DAO / Repository / Mapper 封装、使用 Helper 处理复杂逻辑、使用 Converter 做对象转换、使用 Strategy 处理差异化业务场景。

禁止：堆积过长方法、混入 Controller 入参适配逻辑、直接返回数据库 Entity 给外部接口、复制多个业务场景的重复逻辑。

#### DAO / Mapper 层

允许：数据库访问、Entity 映射、Mapper 接口定义、SQL 查询与更新。

禁止：承担业务决策、处理状态流转规则、返回不适合上层使用的底层异常、直接拼接不安全 SQL。

#### Helper 层

允许：封装复杂业务辅助逻辑、提供可复用业务方法、降低 Service 方法复杂度。

禁止：变成万能工具类、持有过多跨模块依赖、隐藏核心业务主流程。

#### Converter 层

允许：BO / DTO / VO / Entity 之间转换、使用 MapStruct 或项目既有转换规范。

禁止：写业务判断、调用外部服务、访问数据库、修改业务状态。

#### Strategy 层

允许：实现不同场景下的业务差异，按类型、状态、业务种类、工单类型分发处理。

禁止：每个 Strategy 复制大量相同逻辑、Strategy 之间互相调用形成混乱依赖、把主流程全部拆散导致不可读。

### 7.1.4 包命名与文件完整性检查

必须检查：

1. 包名是否全小写。
2. 包名是否能表达职责。
3. Java package 声明是否与目录结构一致。
4. 新增目录是否包含必要的 `package-info.java`。
5. 类名是否符合角色后缀，例如 `Controller`、`Service`、`ServiceImpl`、`Mapper`、`Helper`、`Converter`、`Strategy`、`BO`、`DTO`、`VO`、`Entity`、`Constants`、`Util`。
6. 是否存在拼写错误、缩写混乱或同一概念多种命名。
7. 是否为了一个小功能创建过多空包或空类。

### 7.1.5 依赖方向检查

必须检查：

1. 上层可以依赖下层，下层不得依赖上层。
2. 具体业务模块可以依赖公共能力，公共能力不得依赖具体业务模块。
3. 支撑能力不得依赖具体业务模块。
4. 不得形成循环依赖。
5. 不得通过工具类、静态方法、Spring Bean 注入绕过分层边界。

常见违规：

- `common` 依赖具体业务模块。
- `support` 依赖具体业务 Service。
- DAO 调用 Service。
- Converter 调用 Service 或 Mapper。
- Helper 跨多个业务模块直接操作对方内部实现。
- Controller 直接调用 Mapper。

### 7.1.6 新增业务模块检查

如果本次变更新增业务模块，必须检查：

1. 是否创建在正确的业务父目录下。
2. 是否遵守同类业务模块的既有结构。
3. 是否创建必要子包。
4. 是否创建必要的 `package-info.java`。
5. 是否按职责创建 Controller / Service / DAO / POJO / Helper / Converter / Strategy。
6. 是否避免创建当前功能不需要的空目录和空类。
7. 是否在 `design.md` 中有明确落位依据。
8. 是否没有破坏已有模块结构一致性。

### 7.1.7 SDD 模式额外检查

当入口为 `SDD_TASK_CODE_REVIEW` 时，架构一致性还必须检查：

1. 新增类是否符合 `design.md` 的设计落位。
2. 实际包结构是否与 `tasks.md` 中的文件计划一致。
3. 是否创建了 `design.md` 或 `tasks.md` 未批准的目录。
4. 是否修改了 `tasks.md` 未允许修改的文件。
5. 是否出现范围扩张。
6. 是否需要将偏差记录到 `tasks.md` 和 `archive.md`。

### 7.1.8 Standalone 模式额外检查

当入口为 `STANDALONE_GIT_RANGE_REVIEW` 时，架构一致性不强制读取 SDD 产物，但必须检查：

1. 本次 Git Diff 是否符合当前模块已有结构。
2. 是否与同类模块的组织方式保持一致。
3. 新增包和类是否职责清晰。
4. 是否存在明显违反模块边界的问题。
5. 是否需要在 HTML 报告中列为架构风险。

## 7.2 业务逻辑正确性

重点检查：

1. 状态流转是否合法。
2. 权限 / 数据范围是否正确。
3. 边界条件是否处理。
4. 外部系统返回是否处理完整。
5. 是否符合 spec 验收标准。
6. 是否存在重复提交、重复处理或重复状态变更风险。
7. 是否存在失败重试导致的副作用。
8. 是否存在错误默认值或漏处理分支。

## 7.3 代码质量与可维护性

重点检查：

1. 命名清晰。
2. 方法不过长。
3. 类职责单一。
4. 无重复代码。
5. 无魔法值。
6. 无过度设计。
7. 无无意义封装。
8. 复杂条件是否可读。
9. 是否有明确异常处理。
10. 是否便于单元测试。

## 7.4 UAW 工具类与项目规范

优先检查是否使用：

```text
CurrentUser
LogUtil
MyDateUtil
DatePattern
MyStringUtil
MyObjectUtil
MyJsonUtil
MyCollectionUtil
Preconditions
```

禁止：

1. 使用 `System.out.println` 或 `System.err.println`。
2. 重复造项目已有工具方法。
3. 绕过项目已有用户上下文、日期、日志、JSON、集合、字符串处理规范。

## 7.5 日志与可观测性

检查：

1. 日志级别是否合理。
2. 是否使用占位符。
3. 是否记录关键业务上下文。
4. 是否避免输出敏感信息。
5. 异常日志是否有足够排查信息。
6. 外部接口调用是否有必要日志。
7. 状态变更是否有必要日志。
8. 是否存在无意义日志或刷屏日志。

## 7.6 数据库与 SQL

检查：

1. SQL 注入风险。
2. `SELECT *`。
3. N+1 查询。
4. 分页缺失。
5. 大 offset 或内存分页。
6. 索引失效。
7. 事务边界不清。
8. 批量操作性能风险。
9. 全表扫描风险。
10. Mapper / Entity / DTO 边界混乱。

## 7.7 安全与权限

检查：

1. 密码、Token、密钥、连接串泄露。
2. 日志敏感信息。
3. 返回敏感字段。
4. 硬编码权限。
5. 输入校验缺失。
6. SQL 注入。
7. XSS 风险。
8. 越权访问。
9. 数据权限遗漏。
10. 不安全加密或脱敏不足。

发现敏感信息必须标记 P0，并在输出中脱敏。

## 7.8 单元测试

必须读取并遵守：

```text
skills/uaw-unit-test/references/java/
skills/uaw-unit-test/references/testing-profile-routing.md
```

检查：

1. 是否先识别 Testing Profile。
2. 是否覆盖正常路径。
3. 是否覆盖异常路径。
4. 是否覆盖边界条件。
5. 是否覆盖状态流转。
6. 是否覆盖 Review 修复点。
7. 是否存在无断言测试。
8. 是否存在只追求覆盖率、不验证业务结果的测试。
9. Mock 是否合理。
10. 测试命名是否清晰。
11. 不适用单元测试时是否说明原因。
12. 是否强行引入不必要的 JUnit Vintage / UAW 工具类依赖。

## 7.9 外部接口与远程调用

检查：

1. 外部接口调用是否封装在合适层级。
2. 是否避免 Controller 直接调用外部接口。
3. 是否处理外部接口超时、失败、空响应、异常响应。
4. 是否对返回码、业务状态码、错误信息做明确处理。
5. 是否记录必要调用日志。
6. 是否避免记录敏感请求和响应。
7. 是否有重试、降级或失败处理策略。
8. 是否避免在循环中频繁调用远程接口。
9. 是否没有把外部系统 DTO 直接泄露到本系统外部响应。
10. 是否有必要的单元测试或 Mock 测试。

## 7.10 事务、幂等与重复提交

检查：

1. 涉及数据写入的业务流程是否有清晰事务边界。
2. 多表写入是否存在部分成功风险。
3. 状态更新是否具备前置状态校验。
4. 重复提交是否可能导致重复记录、重复交易或重复状态变更。
5. 是否使用项目已有重复提交校验能力。
6. 是否存在并发更新覆盖风险。
7. 是否需要乐观锁、唯一索引或业务幂等键。
8. 失败重试是否会导致重复执行。
9. 外部接口回调或异步任务是否具备幂等处理。
10. 单元测试是否覆盖重复提交、并发或状态重复流转场景。

## 7.11 配置、环境与兼容性

检查：

1. 是否硬编码环境地址、租户、开关、密钥或配置。
2. 是否兼容 SIT / UAT / PROD 等不同环境。
3. 配置默认值是否安全。
4. 是否存在配置缺失导致启动失败或运行时异常。
5. 是否破坏已有接口兼容性。
6. 是否新增依赖但未说明影响。
7. 是否修改公共配置导致其他模块受影响。

## 7.12 异常处理与错误返回

检查：

1. 异常是否被吞掉。
2. 是否将底层异常直接暴露给外部。
3. 是否提供业务可读错误信息。
4. 是否区分业务异常与系统异常。
5. 是否有必要日志。
6. 是否导致事务或状态不一致。
7. 是否出现 catch 后只打印日志但继续执行。
8. 是否存在空 catch。

---

# 8. 严重程度

## P0：必须立即修复

生产事故、数据错乱、安全泄露、权限绕过、核心流程不可用、SQL 注入、敏感信息泄露、严重事务一致性问题、状态流转错误、重复交易或重复关键业务处理。

## P1：本次建议修复

边界场景异常、重要业务逻辑漏处理、性能风险、核心业务缺测试、架构职责混乱、错误处理不完整、幂等缺失、外部接口失败处理不完整。

## P2：后续优化

命名、局部重复、日志上下文不足、轻微魔法值、方法可拆分、非核心路径测试不足、局部包结构可读性一般。

## Suggestion：建议项

风格优化、长期演进建议、不影响当前功能与安全。

---

# 9. 评分体系

综合评分总分 100 分：

| 维度 | 分值 |
|---|---:|
| 架构一致性与包结构 | 15 |
| 业务逻辑正确性 | 15 |
| 代码质量与可维护性 | 15 |
| UAW 工具类与项目规范 | 10 |
| 数据库与性能 | 10 |
| 安全与权限 | 10 |
| 单元测试 | 10 |
| 日志与可观测性 | 5 |
| 外部接口与配置风险 | 5 |
| 事务、幂等与重复提交 | 5 |

扣分必须能对应具体问题，不能只给分不解释。

---

# 10. 三选一结论

```text
拒绝通过：存在 P0 问题，必须修复后重新评审。
有条件通过：不存在 P0，但存在 P1，需要明确修复计划。
通过：不存在 P0/P1，仅存在 P2 或 Suggestion，或无明显问题。
```

SDD 模式中，该结论用于决定是否进入 Auto-fix / Unit Test / Archive。

Standalone 模式中，该结论用于 HTML 报告。

---

# 11. STANDALONE HTML 报告要求

本章仅适用于：

```text
Entry Mode: STANDALONE_GIT_RANGE_REVIEW
Entry Mode: STANDALONE_WORKTREE_SNAPSHOT_REVIEW
```

## 11.1 HTML 模板使用边界

以下两个 HTML 模板仅允许在 `STANDALONE_GIT_RANGE_REVIEW` 或 `STANDALONE_WORKTREE_SNAPSHOT_REVIEW` 模式下读取和使用：

```text
skills/uaw-code-review/references/templates/summary-report-template.html
skills/uaw-code-review/references/templates/personal-report-template.html
```

`SDD_TASK_CODE_REVIEW` 模式禁止读取上述模板，禁止生成 HTML 报告，禁止创建报告目录。

## 11.2 总览报告

必须基于：

```text
skills/uaw-code-review/references/templates/summary-report-template.html
```

输出：

```text
代码评审统计报告.html
```

总览报告必须包含：

1. 评审范围。
2. Git 命令记录。
3. 提交统计。
4. 开发者统计。
5. 异常提交。
6. 问题分布。
7. 团队评分。
8. 架构一致性与包结构评分。
9. 业务逻辑评分。
10. 代码质量评分。
11. 单元测试评分。
12. 外部接口与配置风险。
13. 事务、幂等与重复提交风险。
14. 关键发现。
15. 高风险文件。
16. 行动计划。
17. 最终结论。

## 11.3 个人报告

必须基于：

```text
skills/uaw-code-review/references/templates/personal-report-template.html
```

输出：

```text
{开发者姓名}_代码评审报告.html
```

个人报告必须包含：开发者信息、提交概览、问题统计、详细问题清单、代码对比、架构与包结构评审、业务逻辑评审、测试评审、外部接口与配置评审、事务幂等评审、亮点总结、修复优先级、三选一结论。

## 11.4 模板占位符覆盖要求

生成报告前必须填充模板中的所有占位符。缺少数据时必须写明“无 / 不适用 / 未发现”，不得保留原始 `{{placeholder}}`。

具体占位符必须按 `11.6 HTML 模板占位符契合清单` 执行。

## 11.5 报告生成自检

生成报告前必须确认：

1. 已读取指定 Git 范围或工作区快照范围。
2. 已读取两个 HTML 模板。
3. 已填充模板中的关键占位符。
4. 已输出总览报告。
5. 已按提交人输出个人报告。
6. 报告路径符合输入指定目录。
7. 不包含未脱敏敏感信息。
8. 模板中明确标记为 Standalone HTML Review only，不得允许 `SDD_TASK_CODE_REVIEW` 使用。


## 11.6 HTML 模板占位符契合清单（强制）

本节仅适用于 `STANDALONE_GIT_RANGE_REVIEW` 或 `STANDALONE_WORKTREE_SNAPSHOT_REVIEW`。

生成报告前，必须逐项填充下列占位符。任何占位符缺少数据时，必须填入 `无`、`不适用` 或 `未发现`，不得让 `{{placeholder}}` 原样保留在最终 HTML 报告中。

SDD_TASK_CODE_REVIEW 模式禁止执行本节，禁止读取 HTML 模板，禁止生成 HTML 报告。

### 11.6.1 总览报告模板占位符

| 占位符 | 填充要求 |
|---|---|
| `{{reviewDate}}` | 评审日期，格式 YYYY-MM-DD |
| `{{scopeDeviation}}` | 范围偏差说明；Git range 模式填“Scope: Git range”，worktree snapshot 填“Scope Deviation: worktree snapshot, not Git range; Formal Merge Gate: no” |
| `{{baseRef}}` | branch diff 模式的 Base branch；worktree snapshot 填写“none / current HEAD / specified ref” |
| `{{headRef}}` | branch diff 模式的 Target branch / HEAD；worktree snapshot 填写“working tree: <Target Path>” |
| `{{finalDecision}}` | 最终结论：拒绝通过 / 有条件通过 / 通过 |
| `{{totalCommits}}` | 本次评审范围内提交总数；worktree snapshot 无提交时填 0 / N/A |
| `{{excludeMerge}}` | 是否排除 merge commit：是 / 否 |
| `{{developerCount}}` | 涉及开发者数量 |
| `{{abnormalCommits}}` | 异常提交数量 |
| `{{changedFiles}}` | 变更文件总数 |
| `{{insertions}}` | 新增行数 |
| `{{deletions}}` | 删除行数 |
| `{{teamScore}}` | 团队综合评分 |
| `{{architectureScore}}` | 架构一致性与包结构得分 |
| `{{architectureDeductionReason}}` | 架构一致性与包结构扣分原因；无则填“无” |
| `{{architecturePercent}}` | 该维度得分占比或扣分占比 |
| `{{businessScore}}` | 业务逻辑正确性得分 |
| `{{businessDeductionReason}}` | 业务逻辑扣分原因；无则填“无” |
| `{{businessPercent}}` | 该维度得分占比或扣分占比 |
| `{{qualityScore}}` | 代码质量与可维护性得分 |
| `{{qualityDeductionReason}}` | 代码质量扣分原因；无则填“无” |
| `{{qualityPercent}}` | 该维度得分占比或扣分占比 |
| `{{uawStandardScore}}` | UAW 工具类与项目规范得分 |
| `{{uawStandardDeductionReason}}` | UAW 规范扣分原因；无则填“无” |
| `{{uawStandardPercent}}` | 该维度得分占比或扣分占比 |
| `{{databaseScore}}` | 数据库与性能得分 |
| `{{databaseDeductionReason}}` | 数据库与性能扣分原因；无则填“无” |
| `{{databasePercent}}` | 该维度得分占比或扣分占比 |
| `{{securityScore}}` | 安全与权限得分 |
| `{{securityDeductionReason}}` | 安全与权限扣分原因；无则填“无” |
| `{{securityPercent}}` | 该维度得分占比或扣分占比 |
| `{{testScore}}` | 单元测试得分 |
| `{{testDeductionReason}}` | 单元测试扣分原因；无则填“无” |
| `{{testPercent}}` | 该维度得分占比或扣分占比 |
| `{{loggingScore}}` | 日志与可观测性得分 |
| `{{loggingDeductionReason}}` | 日志与可观测性扣分原因；无则填“无” |
| `{{loggingPercent}}` | 该维度得分占比或扣分占比 |
| `{{integrationConfigScore}}` | 外部接口与配置风险得分 |
| `{{integrationConfigDeductionReason}}` | 外部接口与配置风险扣分原因；无则填“无” |
| `{{integrationConfigPercent}}` | 该维度得分占比或扣分占比 |
| `{{idempotencyScore}}` | 事务、幂等与重复提交得分 |
| `{{idempotencyDeductionReason}}` | 事务、幂等与重复提交扣分原因；无则填“无” |
| `{{idempotencyPercent}}` | 该维度得分占比或扣分占比 |
| `{{developerName}}` | 开发者姓名 |
| `{{developerCommits}}` | 该开发者提交数 |
| `{{developerFiles}}` | 该开发者变更文件数 |
| `{{developerInsertions}}` | 该开发者新增行数 |
| `{{developerDeletions}}` | 该开发者删除行数 |
| `{{developerAbnormalCommits}}` | 该开发者异常提交数 |
| `{{p0Count}}` | P0 问题数量 |
| `{{p1Count}}` | P1 问题数量 |
| `{{p2Count}}` | P2 问题数量 |
| `{{developerScore}}` | 开发者综合评分 |
| `{{developerDecisionClass}}` | 结论样式：pass / warn / fail |
| `{{developerDecision}}` | 开发者结论：拒绝通过 / 有条件通过 / 通过 |
| `{{commitHash}}` | 提交 Hash |
| `{{author}}` | 提交作者 |
| `{{commitMessage}}` | 提交信息 |
| `{{filesChanged}}` | 提交涉及文件数 |
| `{{totalChangedLines}}` | 提交总变更行数 |
| `{{abnormalReason}}` | 异常提交原因；无则填“无” |
| `{{abnormalSuggestion}}` | 异常提交处理建议；无则填“无” |
| `{{criticalFindingTitle}}` | P0 或最高风险发现标题；无则填“未发现 P0” |
| `{{criticalFindingDescription}}` | P0 或最高风险发现描述；无则填“无” |
| `{{majorFindingTitle}}` | P1 主要问题标题；无则填“未发现 P1” |
| `{{majorFindingDescription}}` | P1 主要问题描述；无则填“无” |
| `{{minorFindingTitle}}` | P2 一般问题标题；无则填“未发现 P2” |
| `{{minorFindingDescription}}` | P2 一般问题描述；无则填“无” |
| `{{totalP0}}` | 团队 P0 总数 |
| `{{totalP1}}` | 团队 P1 总数 |
| `{{totalP2}}` | 团队 P2 总数 |
| `{{totalSuggestion}}` | Suggestion 总数 |
| `{{architectureFinding}}` | 模块架构与包结构专项发现；无则填“无” |
| `{{architectureImpact}}` | 模块架构与包结构影响；无则填“无” |
| `{{architectureAction}}` | 模块架构与包结构建议动作；无则填“无” |
| `{{integrationConfigFinding}}` | 外部接口与配置专项发现；无则填“无” |
| `{{integrationConfigImpact}}` | 外部接口与配置影响；无则填“无” |
| `{{integrationConfigAction}}` | 外部接口与配置建议动作；无则填“无” |
| `{{idempotencyFinding}}` | 事务、幂等与重复提交专项发现；无则填“无” |
| `{{idempotencyImpact}}` | 事务、幂等与重复提交影响；无则填“无” |
| `{{idempotencyAction}}` | 事务、幂等与重复提交建议动作；无则填“无” |
| `{{riskFilePath}}` | 高风险文件路径；无则填“无” |
| `{{riskType}}` | 高风险文件风险类型；无则填“无” |
| `{{riskIssueCount}}` | 高风险文件问题数量；无则填“0” |
| `{{riskSuggestion}}` | 高风险文件处理建议；无则填“无” |
| `{{p0Action}}` | P0 行动计划；无则填“无” |
| `{{p0Owner}}` | P0 负责人；无则填“无” |
| `{{p0Due}}` | P0 建议完成时间；无则填“无” |
| `{{p1Action}}` | P1 行动计划；无则填“无” |
| `{{p1Owner}}` | P1 负责人；无则填“无” |
| `{{p1Due}}` | P1 建议完成时间；无则填“无” |
| `{{p2Action}}` | P2 行动计划；无则填“无” |
| `{{p2Owner}}` | P2 负责人；无则填“无” |
| `{{p2Due}}` | P2 建议完成时间；无则填“无” |
| `{{gitCommands}}` | 本次实际执行的 Git / 文件扫描 / 测试命令记录 |
| `{{generatedAt}}` | 报告生成时间 |

### 11.6.2 个人报告模板占位符

| 占位符 | 填充要求 |
|---|---|
| `{{developerName}}` | 开发者姓名 |
| `{{scopeDeviation}}` | 范围偏差说明；Git range 模式填“Scope: Git range”，worktree snapshot 填“Scope Deviation: worktree snapshot, not Git range; Formal Merge Gate: no” |
| `{{reviewDate}}` | 评审日期，格式 YYYY-MM-DD |
| `{{overallScore}}` | 个人综合评分 |
| `{{finalDecision}}` | 最终结论：拒绝通过 / 有条件通过 / 通过 |
| `{{commitCount}}` | 该开发者提交数量 |
| `{{changedFiles}}` | 变更文件总数 |
| `{{insertions}}` | 新增行数 |
| `{{deletions}}` | 删除行数 |
| `{{commitHash}}` | 提交 Hash |
| `{{commitMessage}}` | 提交信息 |
| `{{filesChanged}}` | 提交涉及文件数 |
| `{{commitStatusClass}}` | 提交状态样式：pass / warn / fail |
| `{{commitStatus}}` | 提交状态：正常 / 异常 / 需关注 |
| `{{architectureScore}}` | 架构一致性与包结构得分 |
| `{{architectureReview}}` | 架构一致性与包结构评审摘要 |
| `{{businessScore}}` | 业务逻辑正确性得分 |
| `{{businessReview}}` | 业务逻辑正确性评审摘要 |
| `{{qualityScore}}` | 代码质量与可维护性得分 |
| `{{qualityReview}}` | 代码质量与可维护性评审摘要 |
| `{{uawStandardScore}}` | UAW 工具类与项目规范得分 |
| `{{uawStandardReview}}` | UAW 工具类与项目规范评审摘要 |
| `{{databaseScore}}` | 数据库与性能得分 |
| `{{databaseReview}}` | 数据库与性能评审摘要 |
| `{{securityScore}}` | 安全与权限得分 |
| `{{securityReview}}` | 安全与权限评审摘要 |
| `{{testScore}}` | 单元测试得分 |
| `{{testReview}}` | 单元测试评审摘要 |
| `{{loggingScore}}` | 日志与可观测性得分 |
| `{{loggingReview}}` | 日志与可观测性评审摘要 |
| `{{integrationConfigScore}}` | 外部接口与配置风险得分 |
| `{{integrationConfigReview}}` | 外部接口与配置风险评审摘要 |
| `{{idempotencyScore}}` | 事务、幂等与重复提交得分 |
| `{{idempotencyReview}}` | 事务、幂等与重复提交评审摘要 |
| `{{p0Count}}` | P0 问题数量 |
| `{{p1Count}}` | P1 问题数量 |
| `{{p2Count}}` | P2 问题数量 |
| `{{suggestionCount}}` | Suggestion 数量 |
| `{{issueNo}}` | 问题编号 |
| `{{issueTitle}}` | 问题标题 |
| `{{severityClass}}` | 严重程度样式：pass / warn / fail |
| `{{severity}}` | 严重程度：P0 / P1 / P2 / Suggestion |
| `{{filePath}}` | 问题所在文件路径 |
| `{{location}}` | 类 / 方法 / 行号 / Diff 位置 |
| `{{issueDescription}}` | 问题描述 |
| `{{impactDescription}}` | 风险影响 |
| `{{fixSuggestion}}` | 修复建议 |
| `{{beforeCode}}` | 优化前代码，来自本次 Diff 或相关上下文；无则填“不适用” |
| `{{afterCode}}` | 优化后代码建议；无则填“不适用” |
| `{{moduleStructureResult}}` | 模块结构识别结论 |
| `{{moduleStructureReview}}` | 模块结构识别说明 |
| `{{responsibilityResult}}` | 职责边界结论 |
| `{{responsibilityReview}}` | 职责边界说明 |
| `{{dependencyResult}}` | 依赖方向结论 |
| `{{dependencyReview}}` | 依赖方向说明 |
| `{{placementResult}}` | 新增包 / 类落位结论 |
| `{{placementReview}}` | 新增包 / 类落位说明 |
| `{{unitTestRequired}}` | 是否需要单元测试：是 / 否 / 不适用 |
| `{{testScenario}}` | 建议或已覆盖测试场景 |
| `{{testGap}}` | 测试缺口；无则填“无” |
| `{{testSuggestion}}` | 测试建议；无则填“无” |
| `{{externalCallResult}}` | 外部接口与远程调用检查结果 |
| `{{externalCallRisk}}` | 外部接口与远程调用风险 |
| `{{externalCallSuggestion}}` | 外部接口与远程调用建议 |
| `{{configResult}}` | 配置与环境兼容检查结果 |
| `{{configRisk}}` | 配置与环境兼容风险 |
| `{{configSuggestion}}` | 配置与环境兼容建议 |
| `{{idempotencyResult}}` | 事务、幂等、重复提交检查结果 |
| `{{idempotencyRisk}}` | 事务、幂等、重复提交风险 |
| `{{idempotencySuggestion}}` | 事务、幂等、重复提交建议 |
| `{{highlightOne}}` | 具体亮点 1；无则填“无” |
| `{{highlightTwo}}` | 具体亮点 2；无则填“无” |
| `{{p0Action}}` | P0 行动计划；无则填“无” |
| `{{p1Action}}` | P1 行动计划；无则填“无” |
| `{{p2Action}}` | P2 行动计划；无则填“无” |
| `{{generatedAt}}` | 报告生成时间 |

### 11.6.3 占位符最终自检

生成 HTML 报告后，必须执行最终自检：

1. 总览报告中不得残留任何 `{{...}}`。
2. 个人报告中不得残留任何 `{{...}}`。
3. 所有评分维度必须与第 9 章评分体系一致。
4. 所有严重程度必须符合第 8 章定义。
5. 所有问题必须能追溯到 Git Diff、文件路径、提交、工作区快照或明确工程风险。
6. 模板中的 Standalone HTML Review 标记不得删除，也不得允许 `SDD_TASK_CODE_REVIEW` 使用。

---

# 12. 重要执行纪律

1. 不要创造性扩展代码评审流程。
2. 不要发明新的 UAW 代码评审体系。
3. 不要混用三个入口模式。
4. SDD 模式不要生成 HTML 报告。
5. SDD 模式不要读取 HTML 模板。
6. SDD 模式必须直接进入 Review-driven Auto-fix。
7. Standalone 模式不要执行 SDD 阶段闸门。
8. Standalone 模式必须按两个 HTML 模板生成报告。
9. Worktree Snapshot 模式必须标明 Scope Deviation，且不得作为正式合并闸门。
10. 不要把历史代码问题强行算作本次变更问题。
11. 不要为了输出“完整报告”制造低价值问题。
12. 不要把某一个模块案例硬编码成全项目架构规则。
13. 每个架构问题必须基于当前模块已有结构、设计约束或明确项目规范。

每一项问题、评分和结论都必须能对应到 Git Diff、SDD 产物、项目规则或明确工程风险。
