# UAW-SDD 2.0 Demo 预演验证报告

- 日期：2026-07-15
- 范围：仅 SDD2.0 runtime、三个 Skill 的协作合同、控制脚本、Demo Feature 流程和简体中文主体规则
- 入口约束：保持“简要提示词 + 调用 `uaw-sdd-ai-coding`”不变
- 演练方式：独立 Git worktree、`execution_mode=demo`、合成 Feature、故障注入、最终不合并业务 Demo 代码

## 1. 最终结论

**预演开始时的版本不是真正的 5/5。** 真实走流程时发现 3 个控制缺陷，其中 2 个会破坏审批/复审可信度或令流程无法闭环。

**3 个缺陷修复后，当前 `main` 在本次定义的仓库控制验收矩阵内达到 5/5。** 完整 Demo 已从 Brief 走到 Archive，并验证了失败、返工、重新冻结、完整复审、测试阻塞、跨会话恢复、终态不可变和锁释放。

这里的 5/5 表示：入口不变、关键状态可执行、异常路径可恢复、证据可追溯、终态不可绕过。它不表示任一单独 AI Reviewer 永远不会漏检；本次恰好证明 Code Review 会漏检，而 Unit Test 能作为独立防线拦截。

## 2. 入口与隔离结果

| 检查项 | 结果 | 证据 |
|---|---|---|
| 开发者入口 | 未改变 | `entry_contract.user_entry=brief-prompt-and-skill-call` |
| 开发者新增操作 | 无 | 控制命令仍由 Skill 内部执行 |
| Demo 授权 | 使用用户原文单独记录 | `做一次demo预演，验证一下整个体系是否真的达到5/5` |
| Demo 审批身份 | `demo-simulation / ai-as-human-reviewer` | Spec、Design、Tasks、Phase、Summary、Archive 证据 |
| 业务 Demo 代码 | 未合并到 `main` | 只存在于临时 worktree |
| 主分支正式改动 | 仅 SDD2 控制修复、测试、报告和 handoff | Git 变更清单 |

## 3. 预演 Feature

- Feature：`demo-policy-info-summary-masking`
- 类型：enhancement
- 模块：`uaw-sdd-demo/policy-info`
- 合成目标：GET `changeSummary` 对手机号旧值和新值做遮蔽；短值完全遮蔽；null 保持；非手机号和 POST 行为不变
- 允许变更：一个 Service 文件和其既有 Service Test
- 禁止变更：Controller、DTO/Entity、Repository、POM、其他模块
- 测试栈：Java 17、Maven、JUnit4、Mockito

## 4. 端到端流程结果

```text
Brief
  -> init/resume
  -> Proposal r1-r3
  -> Spec r1-r2 + Demo approval
  -> Design r1-r2 + Demo approval
  -> Tasks r1 + Demo approval
  -> clean scope capture
  -> Phase1 + Demo Phase Review
  -> freeze code revision 1
  -> Code Review failed (CR-001)
  -> Auto-fix + refreeze code revision 2
  -> full Code Review r2 passed
  -> Auto-fix r1 passed
  -> Unit Test source expansion
  -> refreeze code revision 3
  -> full Code Review r3 + Auto-fix r2 passed
  -> intentional invalid test selector -> Unit Test blocked
  -> valid test run exposed UT-001 -> Unit Test blocked
  -> fix + refreeze code revision 4
  -> full Code Review r4 + Auto-fix r3 passed
  -> 7/7 Unit Tests passed
  -> Unit Test Summary r3 + Demo approval
  -> immutable Archive evidence
  -> Archive check passed
  -> Archive r1 + Demo approval
  -> completed / resume valid / terminal immutable / lock released
```

## 5. 异常场景矩阵

| 场景 | 预期 | 实际结果 | 结论 |
|---|---|---|---|
| Demo 未授权时 AI 模拟批准 Spec | 拒绝 | 退出码 2，状态未前进 | 通过 |
| 用户原文“做一次demo预演”授权 | 应接受 | 初始版本错误拒绝 | 缺陷 D-01，已修复 |
| Scope Capture 前先改代码 | 拒绝脏基线 | 精确指出 Service 文件 | 通过 |
| Proposal 基线 revision 变化 | 旧 Spec/Design 审批失效 | 两个审批标记 `invalidated` | 通过 |
| Demo Phase Review | 必须标记模拟来源/角色 | 初始命令硬写 `user-message/human` | 缺陷 D-02，已修复 |
| 实现只遮蔽旧手机号 | Code Review 失败 | CR-001 P1，Gate=`failed` | 通过 |
| Auto-fix 改代码后沿用旧 Review | 禁止 | Scope 变化令旧 Gate 失效 | 通过 |
| 新 Scope 记录 Findings r2 | 必须允许完整复审 | 初始版本报 `Unknown workflow stage` | 缺陷 D-03，已修复 |
| Unit Test 阶段新增测试源 | Review/Auto-fix 失效 | 两个 Gate 同时失效并回到 Code Review | 通过 |
| 无效 Maven 测试选择器 | Unit Test 失败并阻止 Archive | `UNIT_TEST_FAILED`；Archive Check 拒绝 | 通过 |
| 有效测试发现短值泄露 | 生产缺陷不能归档 | 7 个测试中 1 个失败；记录 UT-001 | 通过 |
| 修复 UT-001 后不重新复审 | 禁止 | Review、Auto-fix、Unit Test 全失效 | 通过 |
| 最终窄测试 | 全部通过 | 7 run / 7 passed / 0 failed/errors/skipped | 通过 |
| 未批准 Unit Test Summary | 不得准备成功 Archive | 需当前 Summary Demo approval | 通过 |
| Archive 证据与当前 Scope 不一致 | 拒绝 | 当前证据 hash/manifest 精确匹配后才通过 | 通过 |
| 完成后再次写入 | 拒绝 | 退出码 2：terminal attempt immutable | 通过 |
| 新会话恢复 | 返回唯一终态 | `archive/completed/none`，0 error/warning | 通过 |
| 完成后工作树锁 | 自动释放 | `sdd2-active-feature.json` 不存在 | 通过 |

## 6. 发现并修复的问题

### D-01：自然中文 Demo 授权被误拒绝

- 严重度：P1
- 复现：`authorize-demo --authorization-text '做一次demo预演，验证一下整个体系是否真的达到5/5'`
- 原因：动作词仅覆盖“请/运行/进行”等，不覆盖“做”；Demo 词也未覆盖“预演”。
- 风险：用户保持现有短提示词入口时，合法 Demo 请求无法启动。
- 修复：新增明确 Demo 词、动作词和否定词集合；接受“做一次/预演”，拒绝“不要/不做/取消/停止”等否定请求。
- 测试：自然中文原文通过；`不要进行 demo 演练` 被拒绝。

### D-02：Demo Phase Review 被伪记为真人审批

- 严重度：P0
- 复现：原 `phase-review` 无 `source` 和 `approver-role` 参数，内部固定写入 `user-message/human`。
- 原因：阶段审批复用了真实模式的硬编码字段，没有实现 Demo provenance 合同。
- 风险：AI 模拟审批在审计记录中表现为真人审批，破坏 Gate 证据真实性。
- 修复：Phase Review 必须显式传入来源和角色；Demo 要求 `demo-simulation / ai-as-human-reviewer`；增加 message ID 重放检查；同步 Skill 和 process-control。
- 入口影响：无。该命令属于 Skill 内部控制接口，开发者入口未改变。

### D-03：质量产物无法在新 Scope 上记录后续 revision

- 严重度：P0
- 复现：Auto-fix 后 refreeze，再记录 `code-review-findings.md` r2。
- 原因：`record-artifact` 把产物键 `code-review-findings`/`auto-fix-summary` 直接传给只认识流程阶段的失效函数。
- 实际错误：`Unknown workflow stage: code-review-findings`。
- 风险：规则要求“任何代码/测试变化后完整复审”，但控制器自身令第二轮 Findings/Auto-fix 无法落盘，流程永久卡死。
- 修复：新增产物键到流程阶段的唯一映射：`code-review-findings -> code-review`、`auto-fix-summary -> auto-fix`。
- 测试：连续三个 Scope 上记录 Findings r1/r2/r3，并记录 Auto-fix r1/r2，revision 与失效状态正确。

## 7. 最终证据

| 证据 | 结果 |
|---|---|
| SDD2 控制回归测试 | 20/20 通过，其中 4 项覆盖简体中文、必要英文和繁体拒绝边界 |
| 静态资产与语言验证 | 53 个 runtime 文件、51 个人类可读文件、3 个历史 Feature、26 个来源档案；0 error、0 warning |
| 控制脚本 Python 编译 | 通过 |
| Demo 最终 Unit Test | 7/7 通过，Java 17，Maven/Surefire |
| 最终 Scope | code revision 4，2 个允许文件，0 violation |
| Code Review | Findings r4，passed，绑定最终 Scope |
| Auto-fix | Summary r3，passed，绑定最终 Scope |
| Unit Test | Summary r3，passed + 当前 Demo approval |
| Archive Check | valid=true，0 error |
| 最终 validate | valid=true，0 error，0 warning |
| 最终 resume | `archive / completed / none` |
| 终态写保护 | 非零退出，拒绝修改 |
| Feature lock | 完成后已释放 |
| Git whitespace | `git diff --check` 通过 |

## 8. 成熟度评分

| 维度 | 预演前真实评分 | 修复后评分 | 依据 |
|---|---:|---:|---|
| 入口与授权 | 4/5 | 5/5 | 原入口不变；自然中文 Demo 请求和否定请求均有测试 |
| Gate 与审批真实性 | 3/5 | 5/5 | 所有 Demo Gate 含正确来源/角色，真实/模拟不混淆 |
| 状态、revision 与恢复 | 4/5 | 5/5 | 需求 revision、Scope revision、失败 Summary 和终态恢复全部实跑 |
| Scope 与失效链 | 5/5 | 5/5 | 脏基线、测试源变更、代码修复均触发正确失效 |
| Review/Auto-fix 闭环 | 3/5 | 5/5 | 后续 Findings/Auto-fix revision 可记录并绑定当前 Scope |
| Unit Test 与 Archive | 5/5 | 5/5 | 选择器失败和真实断言失败均阻止 Archive，最终证据闭环 |
| 审计与跨会话 | 5/5 | 5/5 | hash、revision、resume、terminal immutability、lock release 全验证 |
| 语言与资产一致性 | 未纳入 | 5/5 | 运行规则和新建/修订资产以简体中文为主体；必要英文受控保留；控制器硬阻塞不合规输入和资产 |

**最终成熟度：5/5，仅限上述已执行的仓库控制验收边界。**

## 9. 剩余边界

1. 单个 AI Code Review 仍可能漏检。本次短值缺陷就是由 Unit Test 而不是 r3 Review 发现；因此 5/5 的依据是多 Gate 防御和失败恢复，不是单节点完美。
2. 本次运行的是合成 Java Service Feature 和窄测试类，不替代每个真实业务仓库自己的构建、集成测试、权限和环境验证。
3. 宿主不提供可独立查询的 message ID 时，仓库只能证明记录内容、来源字段、时间、revision/hash 和哈希链，不能独立证明外部 UI 账户身份。

## 10. 验收判断

当前版本满足本轮目标：

- 保持已上线的开发者入口不变；
- 不要求开发者直接操作控制脚本或 `.sdd2/`；
- Demo 与真实人工审批不混淆；
- 任何代码/测试 Scope 变化都会使下游证据失效；
- Review/Auto-fix 可跨多个 Scope revision 闭环；
- Unit Test 失败无法 Archive；
- 完成态可恢复、不可修改、释放锁；
- 三项 Skill 及其人类可读运行文件以简体中文为主体，新建或修订的公开资产受语言闸门约束；
- 所有本次发现的控制缺陷均已有回归测试。

因此，可以把当前 SDD2.0 标记为“5/5（本次仓库控制验收矩阵内）”。

## 11. 简体中文主体补充验证

2026-07-15 在不改变开发者入口的前提下，新增并验证以下语言合同：

1. `skills/uaw-sdd-ai-coding/references/language-policy.md` 是人类可读文件和生成资产语言规则的唯一来源。
2. 三项 Skill 的说明、规则、模板、示例和代理元数据均以简体中文为主体。
3. `init` 会在获取 Feature 锁之前校验 `brief-design.md`；`record-artifact` 会在计算哈希和写入状态之前校验九项公开资产。失败时返回非零并保持当前状态。
4. 文件名、路径、命令、代码标识符、Schema 键、状态枚举、哈希、技术缩写和外部契约原值可保留必要英文，不要求开发者翻译机器契约。
5. 三个 `execution_mode=historical-example` Feature 是不可变审计样例，为保持既有哈希和迁移证据不回写翻译；它们仍不能作为当前需求、审批或 Gate 证据。
6. `original/` 是保留原文和来源哈希的导入档案，不是当前运行规则；活跃 Skill 不得直接加载，派生运行规则必须在 `references/` 中以简体中文表达。

正反向验证覆盖：简体中文正文通过、含必要技术英文通过、英文主导 Brief 拒绝、英文主导过程资产拒绝、繁体正文拒绝。该加固没有增加开发者命令、表单或手工维护步骤。
