# OM API 防腐层规则

## 触发条件与证据

只用于已确认的 Old Mutual（OM）外部 API 集成。确认当前 OM Client/SDK Operation、请求/响应/错误契约、认证、Timeout/Retry、共享 ACL 工具和当前模块示例。

本规则与 EPI 不同。不得因为旧示例相似，就通过 OM 类型或工具调用 EPI。

## ACL 结构

1. 业务/应用 Service 依赖内部 OM Gateway/Service Interface，不直接依赖外部 SDK Client。
2. 实现层负责 Transport 调用，并委托确定性映射/解析。
3. 外部 OM 请求、响应和结果类型不得泄露到 Domain/Controller 契约。
4. 只有当前 OM 代码确认 `RemoteResultUtil` 或同类工具能正确处理成功、错误码、null Data、Warning 和部分结果时才可使用。`Optional.empty()` 不得抹去 Provider 错误。
5. 将 OM 错误映射为内部类型化结果/异常，并安全保留 Provider Code 和 Correlation。
6. 按 Operation 定义 Timeout、Retry 和 Fallback。只重试安全、幂等调用。
7. 日志脱敏凭据、个人数据和 Provider Payload，保留已批准的 Correlation 标识。

## 映射

- 字段映射和默认值必须显式并考虑版本。
- 定义未知枚举/状态行为。
- null、空值和部分 Payload 行为遵循真实 OM 契约。
- 涉及时测试日期时间、金额精度、Locale/国家和标识符转换。

## 测试

- 请求、Header 和认证元数据映射，不使用真实密钥；
- 成功、空值和部分响应映射；
- OM 业务错误、畸形响应、Timeout 和传输失败；
- 配置时的 Retry、Fallback 和幂等行为；
- 未知/新增 Provider 值的兼容性。

## 阻塞条件

当前 OM Operation 契约、外部类型版本、错误语义、认证或 Timeout/Retry 策略不明确时必须阻塞。不得根据示意类名实现。
