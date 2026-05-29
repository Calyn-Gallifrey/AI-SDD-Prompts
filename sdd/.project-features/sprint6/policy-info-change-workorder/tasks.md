# 功能级 Tasks

# 1. 基本信息

- 功能名称：policy-info-change-workorder
- 功能类型：submit
- 所属模块：policy / workorder
- 对应 spec：`./spec.md`
- 对应 design：`./design.md`
- tasks 文件路径：`./tasks.md`
- 执行模式：standard
- 当前状态：done

# 2. 输入确认（执行前必须完成）

## 必须已确认

- [x] proposal-input.md 已存在：`./proposal-input.md`
- [x] spec.md 已确认：本次为用户授权模拟确认
- [x] design.md 已确认：本次为用户授权模拟确认

## 当前代码已扫描

- [x] 当前模块代码：已扫描 `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/`
- [x] mapper / repository：已扫描 repository 包；本次无 mapper
- [x] model 对象：已扫描 DTO / Entity / Enum
- [x] test 代码：已扫描 service test 与 controller test
- [x] config / script：已扫描 `uaw-sdd-demo/pom.xml`

## enhancement / refactor 额外确认

- [x] 不适用：本次为新增模拟功能，无历史 archive.md
- [x] 不适用：本次无历史资产与当前 Git 差异

# 3. 输入摘要（来自 spec / design）

## 功能目标

- 新建 Spring Boot Maven 工程。
- 新增保单信息变更工单创建与查询能力。
- 跑通 SDD 标准链路并暴露体系问题。

## 本次范围

- API、Service、Repository、Model、Test、Maven 配置、SDD 试跑文档。

## 不可变边界

- 不接真实数据库。
- 不接公司内网专有依赖。
- 不生成 SDD 内部 Code Review HTML 报告。
- 不伪造正式人工确认。

## 关键设计约束

- 使用独立工程 `uaw-sdd-demo/`。
- Repository 使用内存实现。
- 测试使用 JUnit4 + Mockito 以贴近当前 UAW testing 规则。

## 风险重点

- Maven 实际运行 JDK 与业务工程声明 JDK 不一致。
- SDD 模板缺少代码工程根目录字段。
- 模拟确认没有专用状态。

## 验收重点

- `mvn test` 最终通过。
- Code Review Findings、Auto-fix、Unit Test Summary、Archive 均完成。
- SDD 体系问题被独立记录。

# 4. 本次规则装配结果

已命中规则：

- [x] 包结构规则：使用 `com.example.uawsdddemo` 分层包结构
- [x] API 规则：REST Controller + Bean Validation
- [x] DB / Mapper 规则：本次无 DB / Mapper，使用 Repository 抽象
- [x] Model 规则：DTO / Entity / Enum 分离
- [x] Mapping 规则：Service 内手工转换
- [x] Testing 规则：JUnit4 + Mockito + MockMvc
- [x] Integration 规则：不适用，无外部集成
- [x] Security / Audit 规则：不适用，本次用 `requester` 和 `createdAt` 模拟

补充说明：

- 本次触发了 testing 规则与 Spring Boot 3 默认 JUnit5 风格之间的适配问题，已记录到 `sdd-system-findings.md`。

# 5. 执行总原则

1. 严格按 spec 范围施工。
2. 严格按 design 落位施工。
3. 不改无关代码。
4. 小步修改，保持可回滚。
5. 每阶段完成后自检。
6. 如需突破边界，回到 spec / design 重审。
7. 当前 Git 代码与文档冲突时，以代码为准并记录差异。

# 6. Phase 拆解（Standard Mode）

## Phase 1：对象层施工

### 任务内容

- 新增创建请求 DTO。
- 新增响应 DTO。
- 新增工单实体。
- 新增变更字段枚举。
- 新增工单状态枚举。

### 输出物

- `CreatePolicyInfoChangeWorkOrderRequest.java`
- `PolicyInfoChangeWorkOrderResponse.java`
- `PolicyInfoChangeWorkOrder.java`
- `ChangeFieldType.java`
- `WorkOrderStatus.java`

### 检查项

- [x] 命名规范：类名与功能语义一致
- [x] 字段完整：覆盖 policyNo、changeFieldType、oldValue、newValue、requester、status、createdAt
- [x] 字段来源明确：请求字段与系统生成字段已区分
- [x] 与 spec 对齐：仅实现创建和查询所需字段
- [x] 无重复对象：无存量对象可复用

## Phase 2：数据层施工

### 任务内容

- 新增 Repository 接口。
- 新增内存 Repository 实现。

### 输出物

- `PolicyInfoChangeWorkOrderRepository.java`
- `InMemoryPolicyInfoChangeWorkOrderRepository.java`

### 检查项

- [x] SQL 正确：不适用，本次无 SQL
- [x] 条件完整：重复判断覆盖 policyNo、changeFieldType、newValue、SUBMITTED 状态
- [x] 返回字段正确：保存与查询返回完整实体
- [x] 无明显性能问题：模拟场景可接受，生产场景需改为 DB 查询
- [x] 命名统一：Repository 命名与实体一致

## Phase 3：业务层施工

### 任务内容

- 新增 Service。
- 实现新旧值校验。
- 实现重复提交校验。
- 实现查询不存在异常。
- 实现 Entity 到 Response 转换。

### 输出物

- `PolicyInfoChangeWorkOrderService.java`

### 检查项

- [x] 流程符合 design：Controller → Service → Repository → Response
- [x] 边界清晰：业务校验在 Service
- [x] 异常处理合理：BadRequest / NotFound 分别抛出
- [x] 不污染存量逻辑：本次为独立工程，无存量逻辑

## Phase 4：接口层施工

### 任务内容

- 新增 Controller。
- 新增创建接口。
- 新增查询接口。
- 新增统一异常处理。

### 输出物

- `PolicyInfoChangeWorkOrderController.java`
- `ApiExceptionHandler.java`
- `BadRequestException.java`
- `NotFoundException.java`

### 检查项

- [x] path 正确：`/api/work-orders/policy-info-change`
- [x] 入参正确：创建请求使用 `@Valid @RequestBody`
- [x] 出参正确：返回工单响应对象
- [x] 错误码统一：400 / 404 已覆盖
- [x] 注解完整：`@RestController`、`@RequestMapping`、`@PostMapping`、`@GetMapping`

## Phase 5：集成层施工

### 任务内容

- 不适用：本次无外部系统 / 网关 / ACL。

### 输出物

- 无。

### 检查项

- [x] timeout：不适用，无外部调用
- [x] retry：不适用，无外部调用
- [x] 错误映射：不适用，无外部调用
- [x] 日志完整：不适用，本次不做集成日志

## Phase 6：测试层施工

### 任务内容

- 新增 Service 单元测试。
- 新增 Controller 单元测试。
- 为 Spring Boot 3 + JUnit4 增加 Vintage 依赖。
- 为当前 Java 26 Maven 运行环境增加 Surefire Byte Buddy 参数。

### 输出物

- `PolicyInfoChangeWorkOrderServiceTest.java`
- `PolicyInfoChangeWorkOrderControllerTest.java`
- `pom.xml`

### 覆盖场景

- [x] 正常路径：创建成功、查询成功
- [x] 异常路径：新旧值一致、重复待处理工单、查询不存在
- [x] 边界输入：必填字段为空
- [x] 空结果：查询 missing 返回 NotFound
- [x] 权限 / 上下文场景：不适用，本次无权限上下文
- [x] 回归场景：Code Review 修复后重新执行全部测试

## Phase 7：交付整理

### 变更文件清单

- `uaw-sdd-demo/pom.xml`
- `uaw-sdd-demo/.gitignore`
- `uaw-sdd-demo/README.md`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/**`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/**`
- `sdd/.project-features/sprint6/policy-info-change-workorder/**`

### 变更摘要

- 创建 Spring Boot Maven 示例工程。
- 实现保单信息变更工单创建与查询。
- 增加测试并修复本地 Maven Java 26 下 Mockito / Byte Buddy 测试失败问题。
- 生成本次 SDD 标准流程资产。

#### Unit Test Summary 引用

- pass
- 正式测试结论见本文件第 17.3 节。

#### 已知问题

- [✓] Maven 使用 Java 26 导致首次测试失败；已通过 Surefire 参数修复，并记录为 SDD 环境预检缺失问题。
- [✓] 内存 Repository 不能用于生产；本次仅作为 SDD 流程验证。

#### 风险点

- SDD 体系投入内网使用前，需要明确目标 JDK、Maven、测试框架和依赖缓存策略。

#### 回滚方式

- 删除或忽略 `uaw-sdd-demo/` 与本 feature 目录即可回滚本次模拟资产。

# 9. 实施后本地检查记录

## 代码层

- [x] 本地验证记录已补充：见第 17.3 节
- [x] import 干净：编译通过
- [x] 无明显 warning：测试通过，Java 26 动态 agent warning 已记录为环境兼容提示
- [x] 命名规范：类名、方法名、测试名与功能语义一致

## 功能层

- [x] 满足 spec：创建、查询、校验、重复判断均已实现
- [x] 原功能未破坏：本次独立工程，无存量业务功能
- [x] 边界未突破：未接 DB、未接外部系统、未生成 HTML Review 报告

## 设计层

- [x] 与 design 一致：按 Controller / Service / Repository / Model / Test 分层落位
- [x] 无私自扩展实现：未实现审批流、权限、前端

## 质量层

- [x] Unit Test Summary 已输出：9 tests pass
- [x] 无明显回归问题：独立工程全量测试通过

# 10. 审核未通过处理

- 首次测试未通过，原因不是业务断言失败，而是 Mockito / Byte Buddy 与 Maven Java 26 不兼容。
- 已进入 Review-driven Auto-fix，修复 `pom.xml`。
- 修复后重新执行 `mvn test`，测试通过。

# 11. 归档前置条件

- [x] spec 已确认：模拟确认
- [x] design 已确认：模拟确认
- [x] tasks 已执行完成
- [x] 代码实施已完成
- [x] Code Review 已完成
- [x] Review-driven Auto-fix 已完成
- [x] Unit Test Generation 已完成
- [x] Unit Test Summary 已输出
- [x] 人工最终审核通过：不适用，本次为用户授权模拟试跑，未伪造真实人工审批

# 12. 归档输出要求

生成：

- `archive.md`
- `sdd-system-findings.md`

# 13. 状态流转

draft → executing → code-review → auto-fix → unit-test → approved（模拟）→ archived

# 14. 执行结论

- 当前状态：done
- 阻塞项：无
- 下一步动作：根据 `sdd-system-findings.md` 修订 SDD 体系
- 备注：本次通过真实测试失败暴露出环境预检缺口

# 15. Code Review Gate（强制）

## 15.1 入口模式

Entry Mode：`SDD_TASK_CODE_REVIEW`

Feature Directory：`.project-features/sprint6/policy-info-change-workorder/`

SDD Artifacts：

- `./proposal-input.md`
- `./spec.md`
- `./design.md`
- `./tasks.md`

## 15.2 SDD 内部 Code Review 输出规则

- [x] 未生成 `代码评审统计报告.html`
- [x] 未生成个人代码评审报告
- [x] 未读取 Code Review HTML 模板
- [x] 未创建 `reports/code-review/YYYY-MM-DD/` 目录
- [x] 已直接输出 Code Review Findings
- [x] 已基于 Findings 执行 Review-driven Auto-fix

## 15.3 Code Review 必查项

- [x] 实现符合 spec 范围和边界
- [x] 实现符合 design 落位和流程设计
- [x] tasks 中确认的任务均已完成
- [x] 未出现未经批准的范围扩张
- [x] 未创建约定之外的报告目录
- [✓] 测试工具链存在环境兼容问题：Maven 实际使用 Java 26，Mockito / Byte Buddy 首次运行失败
- [x] P0/P1 问题均有明确修复建议
- [x] Unit Test 影响点已识别

## 15.4 Code Review Findings

| 问题编号 | 严重程度 | 文件 | 方法 / 类 | 问题摘要 | 修复建议 | 是否阻塞 |
|---|---|---|---|---|---|---|
| CR-001 | P1 | `uaw-sdd-demo/pom.xml` | Maven Surefire | 首次 `mvn test` 在 Java 26 下因 Byte Buddy 不支持 class file 70 导致 Mockito mock 失败 | 固定 Maven JDK 为 17，或在 Surefire 增加 `-Dnet.bytebuddy.experimental=true`；本次采用后者保证当前环境可复现通过 | 是，已修复 |
| CR-002 | P2 | `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/InMemoryPolicyInfoChangeWorkOrderRepository.java` | Repository | 使用内存仓储仅适合流程验证，不具备生产持久化能力 | 保持本次边界不变；如进入真实业务，需设计 DB 表、唯一约束和事务 | 否 |
| CR-003 | Suggestion | SDD testing 规则 | 流程规则 | 当前 SDD testing 规则偏 UAW 存量工程和 JUnit4，对 Spring Boot 3 默认 JUnit5 项目适配不足 | 增加项目技术栈 profile，允许按工程选择 JUnit4 / JUnit5 / UAW 工具类规则 | 否 |

## 15.5 Code Review 结果

- Code Review 结论：有条件通过
- P0 数量：0
- P1 数量：1
- P2 数量：1
- Suggestion 数量：1
- 是否需要 Review-driven Auto-fix：yes
- Fix Scope：Maven 测试运行配置
- Files allowed to modify：`uaw-sdd-demo/pom.xml`
- Files forbidden to modify：业务实现、无关 SDD 模板、HTML Code Review 模板
- Unit tests required：yes
- Archive allowed：yes，Auto-fix 和 Unit Test Summary 完成后允许

# 16. Review-driven Auto-fix Gate（强制）

## 16.1 触发条件

- 存在 P1：CR-001 必须修复。

## 16.2 修复边界

允许修改：

- `uaw-sdd-demo/pom.xml`

禁止修改：

- 无关历史代码。
- 未被 Code Review 指出的区域。
- SDD HTML Code Review 模板。

## 16.3 修复结果

- 修复文件清单：`uaw-sdd-demo/pom.xml`
- 修复问题编号：CR-001
- 修复方式：增加 `maven-surefire-plugin` 配置，设置 `-Dnet.bytebuddy.experimental=true`
- 未修复问题及原因：CR-002 不修复，因内存仓储符合本次模拟边界；CR-003 属 SDD 体系后续优化项
- 是否需要重新 Code Review：no，本次修复范围单一且测试已覆盖

# 17. Unit Test Gate（强制）

## 17.1 测试规则来源

- `.project-ai/rules/testing/`
- 实际执行时按当前工程能力适配 JUnit4 + Mockito。

## 17.2 单元测试要求

- [x] 核心业务路径已覆盖
- [x] 异常路径已覆盖
- [x] 边界条件已覆盖
- [x] Code Review 修复点已覆盖：Auto-fix 后全量测试通过
- [x] 测试命名、Mock、断言符合当前 SDD testing 规则的主要约束

## 17.3 Unit Test Summary

- 新增测试文件：
  - `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderServiceTest.java`
  - `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderControllerTest.java`
- 修改测试文件：无
- 覆盖场景：
  - 创建成功
  - 新旧值一致
  - 重复待处理工单
  - 查询成功
  - 查询不存在
  - 请求参数校验失败
  - Controller 业务异常映射
- 未覆盖场景及原因：
  - 真实 DB 持久化：本次不接数据库
  - 权限与审计上下文：本次不接用户上下文
  - 外部保单系统联动：本次无外部依赖
- 首次测试结果：fail，`PolicyInfoChangeWorkOrderControllerTest` 4 errors，原因为 Java 26 / Byte Buddy / Mockito 兼容问题
- Auto-fix 后测试命令：`mvn test`
- Auto-fix 后测试结论：pass
- 通过结果：Tests run: 9, Failures: 0, Errors: 0, Skipped: 0
- 完成时间：2026-05-28 17:14:43 +0800

# 18. Archive Gate（强制）

- [x] spec.md 最终状态已更新
- [x] design.md 最终状态已更新
- [x] tasks.md 最终状态已更新
- [x] Code Review 已完成
- [x] Review-driven Auto-fix 已完成
- [x] Unit Test Summary 已完成

# Process Status（强制｜流程闸门）

- Current Stage：Archive
- Stage Status：archived
- Last Completed Step：Unit Test Summary
- Next Required Step：无，已归档
- Human Confirmation Required：no
- Allowed Next Action：读取 archive.md 与 sdd-system-findings.md
- Forbidden Next Action：不得跳过体系问题修订直接推广到公司内网
- Updated At：2026-05-28 17:14:56 +0800

# Process Audit Trail（强制｜过程审核轨迹）

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-28 16:45:00 +0800 | Tasks | 拆解施工任务 | spec.md、design.md | tasks.md | 通过，进入实现 | Implementation |
| 2026-05-28 16:55:00 +0800 | Implementation | 创建 Spring Boot 工程并实现功能 | tasks.md | `uaw-sdd-demo/` | 完成 | Code Review |
| 2026-05-28 17:00:00 +0800 | Code Review | 执行 SDD_TASK_CODE_REVIEW | 实现代码、SDD 资产 | Findings | 发现 CR-001 P1 | Auto-fix |
| 2026-05-28 17:03:00 +0800 | Auto-fix | 修复 Maven 测试运行配置 | CR-001 | `pom.xml` | 完成 | Unit Test |
| 2026-05-28 17:14:43 +0800 | Unit Test | 执行 `mvn test` | Auto-fix 后代码 | Surefire 结果 | 9 tests pass | Archive |
| 2026-05-28 17:14:56 +0800 | Archive | 更新流程状态 | 测试结果、Findings | tasks.md | 完成 | None |
