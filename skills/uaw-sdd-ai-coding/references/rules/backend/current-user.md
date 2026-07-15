# 当前用户规则

## 触发条件与发现

行为需要认证用户或 Agent 身份时使用。选择方式前检查当前模块的安全/上下文 API 及邻近用法。`UserContext.getUserId()`、`getCurrentUser()` 等名称只有被当前依赖和代码确认后才可使用。

## 规则

1. 明确所需身份：User ID、Adviser ID、Subject、Role、租户/国家或 System Actor。
2. 身份缺失或匿名时，遵循已批准的明确安全行为；不得回退为空字符串、任意默认值、请求传入身份或虚构 System User。
3. Service/应用层负责涉及权限的身份决定。可行时，Helper/Converter 通过显式参数接收所需身份。
4. MapStruct Converter 可使用上下文参数 `@Context` 或显式映射参数。只有这是模块既有且可测试的约定时，才允许静态访问或 Expression。
5. 不得把请求/用户上下文缓存在静态字段或 Singleton 可变状态中。
6. 不得记录 Token、完整用户对象、Role/Claim Payload 或个人数据。确有需要时只记录已批准的稳定标识。
7. 后台/异步执行必须显式传递已批准身份上下文，或使用已设计的 System Actor；不得假定请求 ThreadLocal 可用。

## 测试

- 已认证身份正确映射并授权；
- 身份缺失/匿名时按 Design 拒绝或处理；
- 适用时拒绝错误 Role、租户或国家；
- Converter/Service 接收到预期身份；
- 异步/后台行为不会错误复用其他请求上下文。

使用现有测试支持模拟当前上下文边界。不得为了简化测试而新增生产回退逻辑。

## 阻塞条件

当前身份 API、所需身份含义、用户缺失行为或异步传递要求不明确时必须阻塞。
