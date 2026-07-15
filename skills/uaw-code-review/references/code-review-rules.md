# UAW 代码评审规则

## 1. 模式与所有权

| 模式 | 范围权威来源 | 输出 | SDD Gate | 是否修复代码 |
|---|---|---|---|---|
| `SDD_TASK_CODE_REVIEW` | 当前 `.sdd2/implementation-scope.json.frozen_snapshot` | Feature 的 `code-review-findings.md` | 校验当前 SDD 状态 | 否 |
| `STANDALONE_GIT_RANGE_REVIEW` | 冻结 Base/Head Commit 和 Diff Hash | HTML 汇总与开发者报告 | 否 | 否 |
| `STANDALONE_WORKTREE_SNAPSHOT_REVIEW` | 冻结目标、HEAD 和文件清单哈希 | HTML 汇总与开发者报告 | 否 | 否 |

读取实现文件前只选择一种模式。Standalone 报告不得作为 SDD Gate 证据；SDD 模式不得生成 HTML。全部人类可读输出遵循简体中文主体规范。

## 2. SDD 模式前置条件

读取 `skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md`，然后执行：

```bash
python3 skills/uaw-sdd-ai-coding/scripts/sdd2_control.py validate --feature-dir <feature-dir>
```

以下任一条件不满足时阻塞评审：

1. 控制校验成功；
2. Spec、Design 和 Tasks 批准记录绑定当前修订与哈希；
3. 范围中声明的所有 Phase 都有当前人工 Phase Review 批准；
4. worktree 锁、分支、Base Commit 和冻结快照均为当前状态；
5. 清单内全部路径均被允许，且不存在禁止或范围外路径；
6. `proposal-input.md`、`spec.md`、`design.md` 和 `tasks.md` 可读取；
7. 输出位置是当前 Feature 的 `code-review-findings.md`。

不得扫描 Tasks 中的字面未勾选框。Tasks 是已批准的不可变计划；实现完成由 Phase Review 记录和冻结范围清单证明。

前置条件失败时，只有输出位置可信才写入阻塞 Findings；否则直接返回阻塞错误，不得写入其他目录。

## 3. 确定性 SDD 范围

唯一受评审实现文件是 `frozen_snapshot.files`。记录：

- Feature ID 和 Attempt；
- 仓库与分支；
- Base Commit、Head Commit、Head Tree；
- 范围快照 SHA-256；
- 每个路径及 SHA-256/删除标记；
- 当前 Spec、Design、Tasks 修订和哈希。

评审前验证每个当前文件哈希。哈希不匹配时返回 `blocked` 并要求重新执行 `freeze-scope`，不得在旧范围上继续评审。

Feature Markdown 和控制资产是上下文，不属于生产实现范围。只检查其 SDD 一致性，不把它们计为产品代码变更。

## 4. Standalone Git Range 范围

必需输入：仓库、Base Ref、Target Ref 和输出目录；需要个人报告时还要提供可验证的开发者归属。

评审前：

1. 将 Base 和 Target 解析为不可变 Commit ID；
2. 分支/Ref 名称只作为标签记录；
3. 捕获精确变更文件清单和 Diff；
4. 计算捕获 Diff 的 SHA-256；
5. 本次执行期间保持范围固定。

用户指定日期范围时，先解析并列出包含的 Commit，不得评审捕获后出现的 Commit。Merge 语义使用用户明确指定的 `base..target` 或 Merge Base 比较；未指定时说明并采用 Merge Base 比较。

未提交和未跟踪文件不属于 Git Range，除非用户明确要求另做一次 worktree 快照评审。

## 5. Standalone Worktree 快照范围

必需输入：仓库/目标路径和输出目录。

捕获：

- 可用时的仓库 HEAD Commit/Tree；
- 精确目标路径；
- 目标下已跟踪变更、删除和未跟踪文件；
- 逐文件内容哈希和一个规范快照哈希；
- 捕获时间。

每份报告必须标注：`范围偏差：worktree 快照，不是 Git Range，不能作为正式合并 Gate。` 评审期间文件变化会使快照失效，必须重新捕获。

## 6. 评审方法

对范围内每个文件：

1. 检查 Diff 和足够的当前上下文代码，理解真实行为；
2. 追踪受影响的调用方、被调用方、契约、持久化和配置；
3. SDD 模式对照已批准行为，Standalone 模式对照用户明确意图；
4. 只有触发条件匹配时才应用路由 UAW 规则；
5. 验证测试覆盖已变更行为和失败边界；
6. 以路径、符号和 Diff 位置记录具体证据。

不得重新设计需求、扩展范围、虚构项目约定，或在无法说明实际后果时报告通用风格偏好。

## 7. 强制评审类别

| 类别 | 必查内容 |
|---|---|
| 范围/追溯 | 每个变更文件已授权；每项批准需求已映射；无隐藏行为 |
| 正确性 | 分支逻辑、null/空值、边界值、状态转换、失败行为 |
| 兼容性 | API、模型、Schema、配置兼容性，默认值、迁移和回滚 |
| 安全 | 权限、输入校验、敏感数据、注入、不安全日志 |
| 事务/并发 | 原子性、回滚、Retry、锁、幂等、竞态 |
| 集成 | Gateway/ACL 映射、Timeout、错误转换、契约漂移 |
| 持久化 | 查询正确性、基数、索引、ORM 映射、数据完整性 |
| 可维护性 | 所有权、有实际风险的重复、命名一致性、不可达/死代码 |
| 可观测性 | 可行动的日志、指标和审计，且不泄露数据 |
| 测试 | 已变更测试源码、正常/边界/错误/回归场景、有效断言和 Mock |

每类结果只能是 `checked-pass`、`checked-finding` 或 `blocked`，并附证据。记录 `passed` 或 `failed` 结论时不得留下空白或待处理项。

## 8. 严重度

- `P0`：很可能导致安全、数据丢失、可用性事故、不可逆损坏、Gate 绕过，或代码无法安全运行/合并。
- `P1`：真实功能缺陷、契约违反、严重回归、事务/并发缺陷，或缺失测试导致高风险变更未经验证。
- `P2`：范围有限的可维护性、清晰度或较低风险正确性问题，并且有具体影响。

只有上下文确实阻止安全推进时，才把 P2 标为 `blocking=true`。规则使用“必须”一词并不能自动提高严重度，应根据后果判断。

## 9. 结论

- `passed`：不存在 P0、P1 或阻塞 P2；全部类别都有检查证据。
- `failed`：当前范围至少存在一项可行动的 P0、P1 或阻塞 P2。
- `blocked`：范围、输入、哈希或上下文缺失、过期或无法验证。

SDD 模式中的 Code Review 不能授权 Archive，只能允许进入 Auto-fix。Unit Test 和后续批准仍为必需项。

## 10. SDD Findings 规则

使用 `templates/sdd-code-review-findings-template.md`。

1. Findings 记录后成为不可变首次评审证据，不得编辑以标记修复完成。
2. 分配稳定 ID：`CR-001`、`CR-002`，依次递增。
3. 每项 Finding 包含严重度、阻塞标记、精确路径/符号/位置、违反的 SDD/规则证据、后果和可执行修复。
4. 包含全部范围文件、全部强制类别结果和精确冻结 ID/哈希。
5. 生产代码变更时设置 `Unit tests required: yes`。
6. 将控制权返回 `uaw-sdd-ai-coding`；修复和处置只记录在 `auto-fix-summary.md`。

## 11. Standalone 报告规则

生成 `代码评审统计报告.html`，并为每个可归属开发者生成一份 `{开发者姓名}_代码评审报告.html`。无法确认归属时生成明确标记为“未归属”的报告，不得猜测。

报告必须包含已捕获的不可变范围、评审方法、Findings、严重度统计、已测试/未测试风险和限制。HTML 自包含并可在本地打开。修改代码需要用户另行明确要求。

## 12. 失败处理

- Git 命令/Range 失败：返回 `blocked`，报告精确命令和错误。
- 二进制、生成文件或大文件：记录限制；可用时检查权威源文件，不得静默遗漏。
- 规则冲突：引用双方来源；影响安全或正确性时阻塞。
- 评审中范围变化：废弃过期结论，重新捕获并完整重跑。
- 无 Findings：明确说明当前范围没有可行动问题，并列出剩余验证缺口；不得虚构问题。
