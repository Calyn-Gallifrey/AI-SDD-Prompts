# EPI Gateway 集成规则

## 边界

只用于已确认的 EPI 集成。本规则不是 OM ACL 规则。除非当前 EPI 实现明确共用，否则不得把 OM Client 类型、包名、Parser、结果包装或错误语义复制到 EPI 代码。

## 必需契约证据

Design 前确认：

- 当前 EPI Client/SDK/Transport 及所属模块；
- Operation、Endpoint/Topic、请求/响应 Schema 和版本；
- 认证、Header 和 Correlation 要求；
- Timeout、Retry、Rate Limit、幂等和可用性语义；
- EPI 成功、错误和部分结果契约；
- 已批准的敏感数据处理和可观测性；
- 可用时的一个当前 EPI 集成示例。

无法获得真实 EPI 契约时必须阻塞，不得根据占位符生成 Client。

## 设计

1. 将 EPI 专有类型封装在集成边界拥有的 Gateway/Adapter 后面。
2. 显式把内部请求模型映射为 EPI 请求类型；EPI 响应/错误必须先映射为内部 DTO/domain 错误，再返回业务 Service。
3. 不得通过 Controller 或 Domain API 暴露 EPI SDK/结果类型。
4. 根据真实 EPI 契约定义 null、空值和部分响应行为。
5. Retry 只适用于文档确认安全且幂等的操作，并避免重试风暴。
6. 使用既有基础设施传递或生成 Correlation ID，脱敏凭据和个人数据。
7. Fallback/Circuit Breaker 行为必须显式且可观测，禁止静默把失败转换为空成功。

## 测试

- 精确的请求和 Header 映射；
- 成功响应映射；
- EPI 业务错误和传输超时映射；
- null、畸形和部分响应；
- 配置时的 Retry/幂等行为；
- 可测试范围内的安全日志和 Correlation 行为。

## 评审证据

记录 EPI 契约/来源版本、Adapter 符号、Timeout/Retry 配置、错误映射表和测试。任何契约假设都保留为待确认问题；影响行为时阻塞实现。
