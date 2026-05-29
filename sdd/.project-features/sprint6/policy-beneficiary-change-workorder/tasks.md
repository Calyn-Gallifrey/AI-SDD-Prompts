# 功能级 Tasks

# 1. 基本信息

- 功能名称：policy-beneficiary-change-workorder
- 功能类型：submit
- 所属模块：policy / workorder
- 对应 spec：`./spec.md`
- 对应 design：`./design.md`
- tasks 文件路径：`./tasks.md`
- 执行模式：standard
- 当前状态：archived

# 2. 输入确认（执行前必须完成）

## 必须已确认

- [x] proposal-input.md 已存在：`./proposal-input.md`
- [x] spec.md 已确认：Codex 代理人工审核通过
- [x] design.md 已确认：Codex 代理人工审核通过

## 当前代码已扫描

- [x] 当前模块代码：已扫描 `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/`
- [x] mapper / repository：已扫描 repository 包；本次无 mapper
- [x] model 对象：已扫描 DTO / Entity / Enum 包
- [x] test 代码：已扫描 controller / service / repository 测试包
- [x] config / script：已扫描 `uaw-sdd-demo/pom.xml`

## enhancement / refactor 额外确认

- [x] 不适用：本次为新增 submit 功能
- [x] 不适用：无历史资产差异需要识别

# 3. 输入摘要（来自 spec / design）

## 功能目标

- 新增保单受益人变更工单提交接口。
- 生成待处理工单并返回脱敏受益人信息。

## 本次范围

- Controller / Service / Repository / DTO / Entity / Enum / Test。

## 不可变边界

- 不接真实数据库。
- 不改已有保单信息变更工单接口。
- 不引入前端。
- 不修改 SDD 体系文件。
- 不生成 SDD 内部 Code Review HTML 报告。

## 关键设计约束

- 响应不得返回明文 `beneficiaryIdNo`。
- 重复提交保存由 Repository 提供原子方法。
- 复用现有 `WorkOrderStatus` 和异常处理机制。

## 风险重点

- 证件号脱敏。
- 重复提交控制。
- 与现有 `policy-info-change` 接口隔离。

## 验收重点

- 创建成功返回 201。
- 非法比例返回 400。
- 重复提交返回 400。
- 必填字段缺失返回 400。
- `mvn test` 通过。

# 4. 本次规则装配结果

已命中规则：

- 包结构规则
- API 规则
- Model 规则
- Mapping 规则
- Testing 规则
- Security / Audit 规则
- SDD 内部 Code Review 规则：`SDD_TASK_CODE_REVIEW`

补充说明：

- DB / Mapper 规则不适用：本次无真实 DB。
- Integration 规则不适用：本次无外部系统。
- UAW 工具类不适用：demo 工程不存在 CurrentUser / LogUtil / MyJsonUtil 等内部工具类。
- SDD 内部 Code Review 不生成 HTML 报告，不读取 HTML 模板，不创建 `reports/code-review/YYYY-MM-DD/`。

# 5. 执行总原则

1. 严格按 spec 范围施工。
2. 严格按 design 落位施工。
3. 不改无关代码。
4. 小步修改，保持可回滚。
5. 每阶段完成后执行代理人工审核。
6. 如需突破边界，必须回到 spec / design 重审。

# 6. Phase 拆解（Standard Mode）

## Phase 1：对象层施工

### 任务内容

- 新增创建请求 DTO。
- 新增响应 DTO。
- 新增受益人变更工单 Entity。
- 新增受益人关系 Enum。

### 输出物

- `CreatePolicyBeneficiaryChangeWorkOrderRequest.java`
- `PolicyBeneficiaryChangeWorkOrderResponse.java`
- `PolicyBeneficiaryChangeWorkOrder.java`
- `BeneficiaryRelationType.java`

### 代理审核标准

- 命名规范。
- 字段完整。
- 字段来源明确。
- 与 spec 对齐。
- 响应不包含明文证件号。

### 当前执行结果

- 已完成。
- 代理审核通过。
- 响应对象仅包含 `beneficiaryIdNoMasked`，不包含明文 `beneficiaryIdNo`。

## Phase 2：数据层施工

### 任务内容

- 新增 Repository 接口。
- 新增内存 Repository 实现。
- 提供原子保存方法 `saveSubmittedIfAbsent`。

### 输出物

- `PolicyBeneficiaryChangeWorkOrderRepository.java`
- `InMemoryPolicyBeneficiaryChangeWorkOrderRepository.java`

### 代理审核标准

- 重复判断条件完整。
- 保存方法避免明显 exists + save 分离窗口。
- 命名统一。
- 不引入 DB。

### 当前执行结果

- 已完成。
- 代理审核通过。
- 内存实现使用 `synchronized saveSubmittedIfAbsent`，以当前 demo 范围避免明显 exists + save 分离窗口。

## Phase 3：业务层施工

### 任务内容

- 新增 Service。
- 实现比例校验。
- 实现重复提交异常。
- 实现实体到响应转换。
- 实现证件号脱敏。

### 输出物

- `PolicyBeneficiaryChangeWorkOrderService.java`

### 代理审核标准

- 流程符合 design。
- 敏感字段脱敏。
- 异常处理合理。
- 不污染存量逻辑。

### 当前执行结果

- 已完成。
- 代理审核通过。
- `benefitRatio` 业务兜底校验覆盖 null / 小于 1 / 大于 100。
- 重复提交通过 `BadRequestException` 返回业务 400。

## Phase 4：接口层施工

### 任务内容

- 新增 Controller。
- 新增 API path。
- 接入 Bean Validation。

### 输出物

- `PolicyBeneficiaryChangeWorkOrderController.java`

### 代理审核标准

- path 正确。
- 入参正确。
- 出参正确。
- 注解完整。
- 不影响现有接口。

### 当前执行结果

- 已完成。
- 代理审核通过。
- 新增接口为 `POST /api/work-orders/policy-beneficiary-change`。

## Phase 5：集成层施工

### 任务内容

- 不适用：本次无外部系统。

### 当前执行结果

- 不适用，已记录。

## Phase 6：测试层施工

### 任务内容

- 新增 Service 测试。
- 新增 Controller 测试。
- Review-driven Auto-fix 后补充 Repository 测试。

### 输出物

- `PolicyBeneficiaryChangeWorkOrderServiceTest.java`
- `PolicyBeneficiaryChangeWorkOrderControllerTest.java`
- `InMemoryPolicyBeneficiaryChangeWorkOrderRepositoryTest.java`

### 覆盖场景

- 正常路径。
- 受益比例非法。
- 重复提交。
- 必填字段缺失。
- 业务异常映射。
- 证件号脱敏。
- Repository business key 去重。

### 当前执行结果

- 已完成。
- 代理审核通过。
- 最终 `mvn test` 通过：19 tests, 0 failures, 0 errors。

## Phase 7：交付整理

### 变更文件清单

生产代码：

- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyBeneficiaryChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/CreatePolicyBeneficiaryChangeWorkOrderRequest.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/PolicyBeneficiaryChangeWorkOrderResponse.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/entity/PolicyBeneficiaryChangeWorkOrder.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/enums/BeneficiaryRelationType.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/PolicyBeneficiaryChangeWorkOrderRepository.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/InMemoryPolicyBeneficiaryChangeWorkOrderRepository.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyBeneficiaryChangeWorkOrderService.java`

测试代码：

- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyBeneficiaryChangeWorkOrderControllerTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/PolicyBeneficiaryChangeWorkOrderServiceTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/repository/InMemoryPolicyBeneficiaryChangeWorkOrderRepositoryTest.java`

SDD 资产：

- `developer-brief-design.md`
- `proposal-input.md`
- `spec.md`
- `design.md`
- `tasks.md`
- `archive.md`
- `sdd-process-findings.md`

### 变更摘要

- 新增受益人变更工单提交 API。
- 新增请求、响应、实体、枚举、仓储、业务服务和 Controller。
- 新增 Service / Controller / Repository 单元测试。
- 完成 SDD 内部 Code Review、Review-driven Auto-fix、Unit Test Gate 和 Archive。

### Unit Test Summary 引用

- 测试命令：`mvn test`
- 执行目录：`uaw-sdd-demo`
- 最终结果：19 tests, 0 failures, 0 errors
- 完成时间：2026-05-29 12:34:30 +0800
- 环境说明：当前 demo 工程 `pom.xml` 使用 Spring Boot 3.3.5、Java 17、JUnit4 + JUnit Vintage，并配置 `-Dnet.bytebuddy.experimental=true`。

### 已知问题

- 当前 demo 工程仍使用内存仓储，仅适合流程验证。
- 当前流程由 Codex 代理人工审核，不代表真实生产审批。
- Maven 测试可运行，但当前 `pom.xml` 的 Byte Buddy experimental 配置会带来环境可移植性和测试噪声风险。

### 风险点

- 正式内网工程接入真实 DB 后，Repository 原子保存需要用唯一索引或事务约束重新设计。
- 正式 UAW 工程接入时，应重新评审 CurrentUser、日志、审计、JSON 工具和安全规范。

### 回滚方式

- 回退新增受益人变更工单相关类和测试。
- 删除本功能目录下新增 SDD 资产。

# 7. 实施后本地检查记录

## 代码层

- [x] 新增代码均位于 `com.example.uawsdddemo` 既有包结构下。
- [x] 未修改已有 `policy-info-change` 相关代码。
- [x] 未新增第三方依赖。
- [x] 响应 DTO 不包含明文 `beneficiaryIdNo`。

## 功能层

- [x] 合法请求可创建 SUBMITTED 工单。
- [x] `benefitRatio` 非法返回 400。
- [x] 重复提交返回 400。
- [x] 必填字段缺失返回 400。

## 设计层

- [x] 实现符合 spec 范围。
- [x] 实现符合 design 类落位、数据流和异常流。
- [x] 不存在未经确认的范围扩张。

## 质量层

- [x] 已执行 SDD 内部 Code Review。
- [x] 已按 Findings 完成 Review-driven Auto-fix。
- [x] 已生成并执行单元测试。
- [x] 已记录最终测试结果。

# 8. 归档前置条件

- spec 已确认：是，Codex 代理人工审核通过。
- design 已确认：是，Codex 代理人工审核通过。
- tasks 已确认：是，Codex 代理人工审核通过。
- 代码实施已完成：是。
- Code Review 已完成：是，SDD 内部入口，不生成 HTML 报告。
- Review-driven Auto-fix 已完成或明确不需要：是，已修复 CR-BEN-001。
- Unit Test Generation 已完成：是。
- Unit Test Summary 已输出：是。
- 人工最终审核通过：是，Codex 代理人工审核通过。

# 9. 代理人工审核记录

| Time | Stage | Reviewer Role | Result | Comment |
|---|---|---|---|---|
| 2026-05-29 12:20:03 +0800 | Tasks | Codex 扮演人类审核 | 通过 | tasks 已按 design 拆分到对象、数据、业务、接口、测试层 |
| 2026-05-29 12:24:50 +0800 | Implementation | Codex 扮演人类审核 | 通过 | 各 Phase 输出物与 design 落位一致 |
| 2026-05-29 12:26:10 +0800 | Code Review | Codex 扮演人类审核 | 有 P2，允许修复后继续 | 发现 Repository 去重行为缺少直接单元测试 |
| 2026-05-29 12:34:30 +0800 | Unit Test | Codex 扮演人类审核 | 通过 | `mvn test` 通过，19 tests |
| 2026-05-29 12:34:45 +0800 | Archive | Codex 扮演人类审核 | 通过 | 归档条件满足 |

# 10. Code Review Gate

- Entry Mode：`SDD_TASK_CODE_REVIEW`
- Feature Directory：`.project-features/sprint6/policy-beneficiary-change-workorder/`
- 当前状态：已完成
- HTML 报告：未生成，符合 SDD 内部 Code Review 规则
- HTML 模板：未读取，符合 SDD 内部 Code Review 规则
- 报告目录：未创建 `reports/code-review/YYYY-MM-DD/`

## 10.1 Code Review 必查项

- [x] 实现符合 spec 范围和边界
- [x] 实现符合 design 落位和流程设计
- [x] tasks 中确认的任务均已完成
- [x] 未出现未经批准的范围扩张
- [x] 未创建约定之外的目录或文件
- [x] 未绕过项目工具类、日志、异常、安全、测试规范
- [x] P0/P1 问题均有明确修复建议
- [x] Unit Test 影响点已识别

## 10.2 Code Review Findings

| 问题编号 | 严重程度 | 文件 | 方法 / 类 | 问题摘要 | 修复建议 | 是否阻塞 |
|---|---|---|---|---|---|---|
| CR-BEN-001 | P2 | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/InMemoryPolicyBeneficiaryChangeWorkOrderRepository.java` | `saveSubmittedIfAbsent` | 核心重复提交仓储行为初版只由 Service mock 测试间接覆盖，缺少 Repository business key 直接验证 | 补充 Repository 单元测试覆盖同保单同证件号拒绝、不同保单允许 | no |

## 10.3 Code Review 结果

- Code Review 结论：通过
- P0 数量：0
- P1 数量：0
- P2 数量：1
- Suggestion 数量：0
- 是否需要 Review-driven Auto-fix：yes
- Fix Scope：补充 Repository 行为测试
- Files allowed to modify：`uaw-sdd-demo/src/test/java/com/example/uawsdddemo/repository/InMemoryPolicyBeneficiaryChangeWorkOrderRepositoryTest.java`
- Files forbidden to modify：本任务范围外历史代码、SDD 体系模板、HTML 报告模板
- Unit tests required：yes
- Archive allowed：yes，需先完成 Auto-fix 与 Unit Test Summary

# 11. Review-driven Auto-fix Gate

## 11.1 修复结果

- 修复文件清单：`uaw-sdd-demo/src/test/java/com/example/uawsdddemo/repository/InMemoryPolicyBeneficiaryChangeWorkOrderRepositoryTest.java`
- 修复问题编号：CR-BEN-001
- 未修复问题及原因：无
- 是否需要重新 Code Review：no

## 11.2 Auto-fix Summary

- Fixed Issues：CR-BEN-001
- Modified Files：无生产代码修改；新增 Repository 测试文件
- Test Files Added / Updated：`InMemoryPolicyBeneficiaryChangeWorkOrderRepositoryTest.java`
- Issues Not Fixed：无
- Reason：不适用
- Remaining Risks：真实 DB 场景仍需用唯一索引或事务重新验证并发约束

# 12. Unit Test Gate

## 12.1 测试规则来源

- Code Project Root：`uaw-sdd-demo`
- Module Root：`uaw-sdd-demo`
- Build Tool：Maven
- Spring Boot 版本：3.3.5
- Java 目标版本：17
- 测试依赖：JUnit4、JUnit Vintage、Mockito、Spring Test
- Selected Testing Profile：UAW-JUnit4
- 兼容 Profile：No-UAW-Util
- 选择依据：当前 demo 工程已有测试和新增测试均采用 JUnit4 + Mockito 风格；工程不存在 UAW 内部工具类。
- 不适用规则：UAW CurrentUser / LogUtil / MyJsonUtil / MyStringUtil / MyCollectionUtil 不适用。
- 测试框架风险：Spring Boot 3.3.5 默认更贴近 JUnit Jupiter，当前工程通过 Vintage 运行 JUnit4；`pom.xml` 中存在 Byte Buddy experimental 参数。
- 是否需要补充依赖：否。

## 12.2 Unit Test Summary

| 测试文件 | 覆盖场景 | 结果 | 备注 |
|---|---|---|---|
| `PolicyBeneficiaryChangeWorkOrderServiceTest.java` | 创建成功、比例过低、比例过高、重复提交 | 通过 | 使用 Mockito 验证 repository 调用次数 |
| `PolicyBeneficiaryChangeWorkOrderControllerTest.java` | 201 响应、必填校验、比例校验、业务异常映射、响应脱敏 | 通过 | 验证 `beneficiaryIdNo` 不存在 |
| `InMemoryPolicyBeneficiaryChangeWorkOrderRepositoryTest.java` | 同保单同证件号重复拒绝、不同保单允许 | 通过 | Review-driven Auto-fix 补充 |

## 12.3 最终测试记录

- 命令：`mvn test`
- 目录：`uaw-sdd-demo`
- 结果：BUILD SUCCESS
- 测试数：19
- Failures：0
- Errors：0
- Skipped：0
- 完成时间：2026-05-29 12:34:30 +0800

# Process Status（强制｜流程闸门）

- Current Stage：Archive
- Stage Status：archived
- Last Completed Step：archive.md 已生成并完成代理最终审核
- Next Required Step：流程复盘与问题确认
- Human Confirmation Required：no（本轮由用户授权 Codex 扮演人类审核）
- Allowed Next Action：检查归档结果，确认是否要调整 SDD 体系模板
- Forbidden Next Action：未经用户确认直接修改 SDD 体系模板
- Updated At：2026-05-29 12:34:45 +0800

# Process Audit Trail（强制｜过程审核轨迹）

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-29 12:20:03 +0800 | Tasks | 根据 spec/design 生成 Tasks | spec.md、design.md | tasks.md | 通过代理审核 | Implementation |
| 2026-05-29 12:24:50 +0800 | Implementation | 按 Phase 实现代码 | tasks.md、design.md | Controller / Service / Repository / DTO / Entity / Enum | 通过代理审核 | Code Review |
| 2026-05-29 12:26:10 +0800 | Code Review | 执行 SDD 内部代码评审 | proposal/spec/design/tasks/代码 | Code Review Findings | 发现 P2 | Auto-fix |
| 2026-05-29 12:26:25 +0800 | Auto-fix | 按 Findings 补充测试 | CR-BEN-001 | Repository 单元测试 | 已完成 | Unit Test |
| 2026-05-29 12:34:30 +0800 | Unit Test | 执行单元测试 | 新增与存量测试 | 19 tests passed | 通过 | Archive |
| 2026-05-29 12:34:45 +0800 | Archive | 生成归档与流程问题报告 | 全部 SDD 资产和代码 | archive.md、sdd-process-findings.md | 通过代理审核 | Done |
