# Service 单元测试规则

用于应用/Domain Service 和编排组件。默认使用真实 Service 实例并 Mock 外部协作者；只有当前架构使纯单元测试不可行且存在已批准 Spring Profile 时，才加载 Spring。

## Fixture

- 根据路由主要 Profile 选择 JUnit/Mockito 注解。
- 通过真实 Constructor 或既有测试约定构造/注入 Service。
- 在边界 Mock Repository、Gateway、Remote Client、Clock、用户/安全 Provider 和 Message Publisher。
- BO/DTO/VO/Entity 使用真实值能提高行为可信度时，优先使用真实对象。

## 必需场景

1. 成功编排及返回/变更的 Domain 值；
2. 校验拒绝，且没有禁止的下游交互；
3. 依赖空值/Not Found 行为；
4. 依赖异常/错误转换；
5. 重要条件分支、兼容默认值或幂等行为；
6. Spec/Code Review 中的已变更回归路径。

## 验证

- 断言返回值或传播的 Domain 异常。
- 映射相关时捕获并断言 Repository/Gateway Command 值。
- 验证副作用次数及拒绝路径无副作用。
- 只有额外调用属于契约缺陷时才使用 `verifyNoMoreInteractions`。
- 不得声称单元测试能验证事务回滚。测试 Service 行为；需要时用适当集成证据验证事务语义。

## 反模式

- Mock 被测 Service。
- 使用隐藏不稳定设计的 Deep Stub。
- 只需 Mockito 的逻辑使用 `@SpringBootTest`。
- 断言只包含 `notNull` 或“不抛异常”。
- 在期望值计算中复制生产算法。
- 使用 Sleep/真实时间依赖，不注入或控制时间。

## 完成证据

把每项测试映射到需求/Finding，并记录测试源码哈希、Mock 边界、精确执行入口、数量、失败/跳过和范围 SHA-256。
