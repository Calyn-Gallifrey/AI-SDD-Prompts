# Java 测试 Profile 路由

## 1. 选择前的证据

检查目标模块的构建文件、依赖树/配置、测试插件、Java Toolchain 和邻近可执行测试。可用时记录精确路径和版本。

不得只根据 Spring Boot 版本选择。实际 JUnit Engine、Runner/Extension、Mockito 支持和 Test Task 配置共同决定能否执行。

## 2. 主要框架 Profile

只选择一个：

### `JUNIT5_MOCKITO`

JUnit Jupiter 已配置且邻近测试在其上可执行时使用。

- `org.junit.jupiter.api.Test`
- Mockito 注入有价值时使用 `@ExtendWith(MockitoExtension.class)`
- 使用 Jupiter Assertion 或项目既有断言库
- 不新增 Vintage/JUnit4 依赖

### `JUNIT4_MOCKITO`

模块运行 JUnit4 且邻近测试使用它时使用。

- `org.junit.Test`
- `@RunWith(MockitoJUnitRunner.class)` 或既有 Rule/Runner 风格
- 与 JUnit4 兼容的 Assertion
- Feature 测试工作中不得顺带迁移模块

### `EXISTING_CUSTOM`

模块存在已证明必需的自定义 Base Class、Runner、Extension、Test Harness 或混合 Platform 时使用。引用一个或多个可执行的邻近测试，只保留必需约定。

### `BLOCKED_UNKNOWN`

无法确认可执行 Test Engine 时使用。不得猜测 Import 或新增依赖。返回缺失证据和恢复动作。

## 3. 兼容性修饰项

修饰项不能替代主要 Profile：

- `LEGACY_JDK_MOCKITO`：记录 JDK、Mockito、Byte Buddy 兼容性。只有项目已经配置时才复用 JVM Flag，不得静默引入 `net.bytebuddy.experimental`。
- `NO_UAW_UTIL`：目标代码未使用或项目不存在 UAW Utility，不得导入虚构 Helper。
- `SPRING_SLICE`：既有 Controller/Data Slice 测试和依赖能够证明 Spring Slice 合理。
- `PURE_MOCKITO`：不需要 Spring Context，Service/Method/Strategy 测试优先采用。
- `STATIC_MOCKING_AVAILABLE`：当前依赖已经支持有作用域的静态 Mock。

## 4. 目标规则路由

| 目标 | 规则 |
|---|---|
| Method/Domain Helper | `java/method-unit-test.md` |
| Service/应用组件 | `java/service-unit-test.md` |
| 静态工具行为 | `java/static-method-unit-test.md` |
| HTTP Controller | `java/controller-unit-test.md` |
| ServiceStrategy/Strategy 选择 | `java/service-strategy-unit-test.md` |

混合目标选择一个主要规则，只有确实涉及额外边界时才引用其他规则章节。

## 5. 执行入口选择

可用且合适时按以下顺序优先：

1. 限定到模块/测试的仓库 Wrapper 命令；
2. 项目既有脚本；
3. 与项目配置匹配的本机 Maven/Gradle 命令；
4. Agent 无法本地执行时，使用可复现 IDE 配置或 CI Job。

IDE/CI 结果必须包含配置/Job 标识和观察结果。建议的未来命令只能记为 `not-run`，不能记为 `passed`。手工检查不能通过 SDD Unit Test Gate。

## 6. 依赖规则

只有现有已批准 Design/Tasks 要求，并且当前支持的测试机制都无法覆盖目标时，才允许新增测试依赖。任何依赖变更都属于实现范围，要求重新冻结、完整 Code Review 和明确证据。

## 7. 结果规范化

- `passed`：相关测试已成功执行，且已记录退出码/结果和数量。
- `failed`：测试已执行并失败。
- `blocked`：缺失目标、框架或环境证据，无法安全生成或执行。
- `not-run`：测试已生成但未执行，永远不具备 Archive 资格。

跳过测试只作为数量和风险记录，不是 Gate 状态。必需场景被跳过时，根据原因使用 `failed` 或 `blocked`。
