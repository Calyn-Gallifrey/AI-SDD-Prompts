# 单元测试总结（Unit Test Summary）

> 本审计记录在单元测试源码生成或更新后创建。SDD 模式中，它必须绑定到 Code Review 已通过且 Auto-fix 已关闭的同一冻结范围。正文必须以简体中文为主体。

## 1. 基本信息与范围

- Feature ID/Standalone Task ID：
- 模式：`SDD` / `standalone`
- Attempt：
- 范围 SHA-256：
- Base Commit：
- Head Commit/Tree：
- 代码修订：
- Summary 修订/SHA-256：

## 2. Profile 证据

- 主要 Profile：`JUNIT5_MOCKITO` / `JUNIT4_MOCKITO` / `EXISTING_CUSTOM` / `BLOCKED_UNKNOWN`
- 修饰项：
- 目标规则：
- 构建/模块证据：
- JUnit/Mockito/断言库证据：
- 邻近测试约定证据：
- 选择理由：
- 依赖变更：`none` / 精确的已批准变更

## 3. 测试源码变更

| 测试文件 | SHA-256 | 新增/更新 | 生产目标 | 覆盖的需求/Findings |
|---|---|---|---|---|
|  |  |  |  |  |

SDD 结果为 `passed` 时，至少一个当前已变更测试源码必须匹配已捕获测试路径。

## 4. 场景覆盖

| 测试 Method/参数集 | 场景类型 | Given（前提） | 预期断言/交互 | 需求/Finding |
|---|---|---|---|---|
|  | `happy` / `boundary` / `error` / `regression` |  |  |  |

## 5. 执行证据

- 验证方式：`Wrapper` / `Local CLI` / `IDE` / `CI` / `Script`
- 执行环境：
- JDK：
- 精确测试入口/命令/Job/配置：
- 开始/结束时间：
- 退出码/观察结果：
- 执行测试数：
- 通过数：
- 失败数：
- Error 数：
- 跳过数：
- 相关输出/证据位置：
- Warning：

没有实际观察到的执行证据时不得记录 `passed`。手工验证只能放在补充证据中，不能通过本 Gate。

## 6. 失败或阻塞详情

| 失败/阻塞 | 测试/符号 | 根因证据 | 生产缺陷/测试缺陷/环境问题 | 恢复方式 |
|---|---|---|---|---|
|  |  |  |  |  |

## 7. Code Review 与 Auto-fix 绑定

- Code Review Findings SHA-256：
- Code Review 结果/范围 SHA-256：`passed` /
- Auto-fix Summary SHA-256：
- Auto-fix 结果/范围 SHA-256：`passed` 或 `not-required` /
- 测试源码变化后的完整复审是否完成：`yes` / `no`

## 8. 剩余测试风险

| 风险 | 原因 | 影响 | 是否阻塞 | 后续动作 |
|---|---|---|---|---|
|  |  |  | `yes` / `no` |  |

## 9. Gate 结论

- Unit Test 结果：`passed` / `failed` / `blocked` / `not-run`
- 是否具备 Archive 资格：仅 `passed` 时为 `yes`，其他情况为 `no`
- 证据摘要：

## 10. 人工 Summary Gate（仅 SDD）

- 状态权威文件：`./.sdd2/feature-state.json`
- 当前阶段：`unit-test-summary`
- 阶段状态：`awaiting-approval`
- 下一必需动作：`request-unit-test-summary-approval`
- 批准证据写入：`./.sdd2/gate-approvals.jsonl`

记录本 Summary 和确定性 Unit Test 结果后停止。准备 Archive 前必须收到用户对当前 Summary 修订的新的明确批准。
