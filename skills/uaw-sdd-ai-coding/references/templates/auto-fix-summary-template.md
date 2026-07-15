# 评审驱动的 Auto-fix 总结

> 记录每项评审发现的处置和修复，不得重写原始 Code Review Findings。正文必须以简体中文为主体。

## 1. 基本信息与范围

- Feature ID：
- Attempt：
- Code Review Findings 修订/SHA-256：
- 已评审范围 SHA-256：
- Auto-fix 前代码修订：
- Auto-fix 后代码修订：
- Auto-fix 结果：`passed` / `not-required` / `failed` / `blocked`

## 2. Findings 处置

| Finding ID | 严重度 | 原始位置 | 处置 | 变更文件/符号 | 修复说明 | 验证 | 剩余风险 |
|---|---|---|---|---|---|---|---|
| CR-001 | P0/P1/P2 |  | `fixed` / `accepted-risk` / `rejected-with-evidence` / `blocked` |  |  |  |  |

不得在 `code-review-findings.md` 中删除、改写或标记已解决。本表是唯一处置记录。

## 3. 范围变更

- 生产/测试/配置是否变更：`yes` / `no`
- 新冻结范围 SHA-256：
- 是否要求完整重跑 Code Review：`yes` / `no`
- 完整重跑结果/证据：

任何代码、测试、配置、Design 或 Tasks 变更都要求重新冻结并完整执行 Code Review。定向 Spot Check 不能替代完整复审。

## 4. 无需修复路径

仅当结果为 `not-required` 时填写：

- 各严重度 Findings 数量：
- 无需修改代码的原因：
- Code Review 已在当前范围通过的证据：

## 5. 验证

| 检查项 | 方法/命令 | 环境 | 退出码/结果 | 证据 |
|---|---|---|---|---|
| 构建/静态检查 |  |  |  |  |
| Finding 定向验证 |  |  |  |  |

## 6. 剩余事项

| ID | 所有者 | 未解决原因 | 是否阻塞 | 下一必需动作 |
|---|---|---|---|---|
|  |  |  | `yes` / `no` |  |

进入 Unit Test 前必须关闭 P0、P1 和明确阻塞的 P2。风险接受不能在缺少当前人工决定和正确流程状态时，把失败 Code Review 转为通过。

## 7. Unit Test 交接

- 当前范围 SHA-256：
- 已变更生产符号：
- 必需测试目标/场景：
- 修复引入的回归风险：
- 是否允许 Unit Test：`yes` / `no`

## 8. 控制状态投影

- 状态权威文件：`./.sdd2/feature-state.json`
- Attempt：
- 控制修订：
- 当前阶段：`auto-fix`
- 阶段状态：
- 下一必需动作：
- 资产修订/SHA-256：

本资产是质量 Gate 记录，不是人工阶段批准。
