# Controller 单元测试规则

用于 HTTP Controller 的请求映射、校验、权限交接、序列化和异常转换。

## Test Harness 选择

根据当前项目的可执行证据选择：

- 以独立 MockMvc 测试聚焦映射/校验，并 Mock Service；
- Filter、Advice、Converter 或安全配置属于契约时，使用项目支持的 Spring MVC Slice；
- 只有 Controller 未映射 HTTP，或已批准变更仅为 Method 层且邻近测试采用该方式时，才直接测试 Method。

默认不得使用 `@SpringBootTest`。未进入已批准范围时，不得新增模块目前缺失的 Spring 测试依赖。

## 必需场景

1. 正确 Method、Path 和 Content Type；
2. 有效请求绑定和传入 Service 的参数；
3. 响应状态及关键 JSON/Body 字段；
4. 适用时的必填、格式、范围和畸形 Body 校验；
5. 权限在范围内时的认证/授权行为；
6. Service/domain 异常到 HTTP 错误的映射；
7. 已变更请求/响应字段的兼容与默认行为；
8. 来自 Spec 或 Findings 的回归场景。

## 断言

- 不得只断言 Status，同时检查契约相关 Header/Body。
- 请求被拒绝时验证 Service 未被调用。
- 请求到模型映射变化时捕获并检查 Service Input。
- 序列化行为相关时使用项目已配置 ObjectMapper/Converter。
- 不重复测试框架内部实现，不断言无意义的 JSON 格式细节。

## 安全

使用既有测试安全 Helper/配置。权限属于契约时，不得为让测试通过而绕过安全。测试数据不得包含真实 Token、凭据或个人数据。

记录 Harness/Profile 证据、测试路径、Endpoint/场景映射、执行入口、结果数量和当前范围哈希。
