# Feature 归档（Archive）

> 只有当前质量 Gate 全部通过且 Unit Test Summary 已被明确批准后，才能生成成功交付候选。最终完成状态只在当前 Archive 获批后存在于控制状态中。正文必须以简体中文为主体。

## 1. 基本信息

- Feature ID：
- 功能名称：
- 所属模块：
- 迭代：
- Attempt：
- Archive 修订/SHA-256：
- 生成时间：
- 候选结果：最终 Archive 批准后为 `completed`

## 2. 交付总结

- 原始目标：
- 已交付行为：
- 保持不变的行为：
- 最终范围：
- 明确非目标：

## 3. 不可变实现证据

来源：`./.sdd2/archive-evidence.json`

- Git 分支：
- Git Base Commit：
- Git Head Commit：
- Git Head Tree：
- 冻结范围 SHA-256：
- Archive 证据 SHA-256：

### 变更文件清单

| 文件 | 最终 SHA-256 | 用途 | 需求/任务 |
|---|---|---|---|
|  |  |  |  |

以上值必须与当前 Archive 证据完全一致；任何不匹配都会阻塞最终批准。

## 4. 资产与批准链

| 资产 | 修订 | SHA-256 | 批准 ID/记录哈希 | 状态 |
|---|---|---|---|---|
| `brief-design.md` |  |  | 不适用 | `current` |
| `proposal-input.md` |  |  | 不适用 | `current` |
| `spec.md` |  |  |  | `approved-current` |
| `design.md` |  |  |  | `approved-current` |
| `tasks.md` |  |  |  | `approved-current` |
| `code-review-findings.md` |  |  | 质量 Gate | `passed-current-scope` |
| `auto-fix-summary.md` |  |  | 质量 Gate | `passed/not-required-current-scope` |
| `unit-test-summary.md` |  |  |  | `approved-current` |
| `archive.md` |  |  | 等待最终批准 | `awaiting-final-approval` |

## 5. 需求可追溯性

| 需求/验收项 | Design | Task/Phase | 生产符号 | 测试源码/用例 | 结果 |
|---|---|---|---|---|---|
| FR-01 / AC-01 |  |  |  |  | `passed` |

## 6. Phase Review 总结

| Phase | 批准消息 ID | 批准时间 | Tasks 修订/哈希 | 结果 |
|---|---|---|---|---|
|  |  |  |  | `approved-current` |

## 7. Code Review

- 范围 SHA-256：
- Findings SHA-256：
- 结论：`passed`
- P0/P1/阻塞 P2 数量：
- 证据：

## 8. Auto-fix

- Summary SHA-256：
- 结果：`passed` / `not-required`
- 范围是否变化：`yes` / `no`
- 变化时的完整复审证据：
- 剩余已接受的非阻塞风险：

## 9. Unit Test

- Summary SHA-256：
- 新增/更新的测试源码文件：
- 测试 Profile/框架：
- 执行方式/环境：
- 精确命令/入口：
- 退出码/结果：
- 通过/失败/跳过数量：
- 范围 SHA-256：
- Gate 结果：`passed`

`failed`、`blocked` 或 `not-run` 不满足成功 Archive 条件。必须由用户明确决定将 Attempt 关闭为 `closed-with-risk` 或 `aborted`。

## 10. 验证总结

| 验证项 | 方法 | 环境 | 结果 | 证据 |
|---|---|---|---|---|
| 构建/静态检查 |  |  | `passed` |  |
| 单元测试 |  |  | `passed` |  |
| 其他已批准验证 |  |  | `passed` / 有理由的 `not-applicable` |  |

## 11. 偏差、风险与技术债

| ID | 类型 | 描述 | 影响 | 所有者 | 后续引用 | 是否阻塞 |
|---|---|---|---|---|---|---|
|  | `deviation` / `risk` / `debt` |  |  |  |  | `no` |

任何阻塞项都会阻止 Archive 批准。

## 12. 知识与规则反馈

| 候选更新 | 证据 | 目标运行文件 | 动作 | 所有者 |
|---|---|---|---|---|
|  |  |  | `updated` / `follow-up` / `none` |  |

未经审核，不得把项目专有事实写入通用规则。

## 13. 恢复与读取顺序

未来接手时按以下顺序读取：

1. `.sdd2/feature-state.json`
2. `.sdd2/archive-evidence.json`
3. `spec.md`
4. `design.md`
5. `tasks.md`
6. `code-review-findings.md`
7. `auto-fix-summary.md`
8. `unit-test-summary.md`
9. 当前 Archive

恢复流程不依赖聊天记录。

## 14. 最终 Archive Gate

- 前置检查结果：`passed`
- 状态权威文件：`./.sdd2/feature-state.json`
- 当前阶段：`archive`
- 阶段状态：`awaiting-final-approval`
- 下一必需动作：`request-archive-approval`
- 必需审核人：当前人工审核人
- 批准证据写入：`./.sdd2/gate-approvals.jsonl`

生成、记录并检查本文件后停止。只有用户在新消息中明确批准当前 Archive 修订，才能把控制状态设为 `completed`。批准后不得仅为写入 `completed` 而修改本文件；批准记录和控制状态才是权威来源。
