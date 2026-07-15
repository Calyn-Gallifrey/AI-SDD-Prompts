# 后端 API 规则

## 触发条件与证据

新建或修改 HTTP/Service API 时使用。Design 前检查目标模块当前 Controller/Service、响应与错误包装、校验、权限、日志、包结构和邻近测试。用户已批准 API 契约与当前模块代码优先于示例。

## 职责

| 层 | 负责内容 | 不得负责 |
|---|---|---|
| Controller/入口 | 路由、绑定、触发校验、权限交接、响应/错误集成 | 业务编排、持久化 |
| Service/应用层 | 业务编排、事务/幂等边界、Gateway/Repository 调用 | HTTP 序列化细节 |
| Strategy（确有必要时） | 由确定性规则选择的单一明确变化 | 隐式全局路由或重复 Key |
| Mapper/Converter | 显式模型映射和默认值 | 远程或持久化调用 |
| Repository/Gateway | 持久化或外部系统边界 | API 响应构造 |

只为已批准增量创建必需的层和模型。增强场景优先复用现有公开 API 与符号，除非破坏性变更已获明确批准。

## 契约规则

- 请求/响应类型、包装器、注解、错误映射和路由风格遵循目标模块当前约定。
- BO/DTO/VO/Entity 只用于其拥有的边界，具体见模型规则。
- 在入口边界校验输入，在所属 Service/domain 组件中执行业务不变量。
- 每个变更字段都要定义 null、空值、默认值和兼容行为。
- 权限必须显式处理，身份缺失或无效时默认拒绝。
- 请求/响应可能含敏感或高容量数据时，不得完整记录对象。

## Strategy 注册安全

当前架构构建 Strategy Map 时：

```java
Object previous = strategyMap.putIfAbsent(key, strategy);
if (previous != null) {
    throw new IllegalStateException("Duplicate strategy key: " + key);
}
```

`putIfAbsent` 会保留旧值，日志不得声称新值已覆盖旧值。重复 Key 的行为必须在 Design 中确定并测试，可以快速失败，也可以使用已批准的确定性优先级。不得静默跳过缺失或空白 Key。

## 事务、错误与可观测性

- 按当前框架约定，把事务所有权放在应用/Service 操作上。
- 写 API 必须定义幂等和部分失败行为。
- 通过既有错误契约映射内部/外部异常，不得泄露堆栈或 Provider Payload。
- 日志记录稳定标识、结果、耗时和可行动错误上下文，同时脱敏密码和个人数据。

## 必需测试

- 成功请求/响应契约；
- 校验与权限拒绝；
- Service/Gateway 错误映射；
- 边界、默认值和兼容行为；
- 适用时的幂等与重复 Strategy 行为；
- 已批准变更的回归场景。

## 阻塞条件

路由所有权、契约字段、权限规则、事务行为或响应/错误约定无法安全确认时，阻塞 Design 或实现。
