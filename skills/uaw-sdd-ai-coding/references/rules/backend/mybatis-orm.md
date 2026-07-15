# MyBatis ORM 规则

## 触发条件与发现

修改 MyBatis/MyBatis-Plus 持久化代码时使用。Design 前检查目标模块的 Mapper Interface、XML/资源位置、别名/TypeHandler、分页、基础 Entity/Mapper、命名策略和测试。

XML 位置由当前构建和资源配置决定。没有证据时不得假定 Java 包目录或 `resources/mapper`。

## Mapper 与 XML

- Interface 和 XML Namespace 必须完全一致。
- Statement ID 必须匹配 Interface Method 及其参数/返回类型。
- 当前使用 XML SQL 的 UAW Transaction 模块继续把 SQL 放在 XML 中，不得引入 `@Select/@Insert/@Update/@Delete`。
- 其他模块保留既有方式，除非 Design 明确批准迁移。
- 名称、类型或嵌套结构复杂时使用显式 `resultMap`，避免脆弱的位置或隐式映射。
- 对歧义列增加限定，并为 Join 列使用确定性别名。
- 值绑定使用 `#{}`。`${}` 只能用于严格白名单控制且理由已记录的结构片段，绝不能接收原始用户输入。

## 查询与数据完整性

- 定义预期基数。“单条”查询必须有已确认唯一性保证，或明确多行处理行为。
- 避免 `SELECT *`，只查询归属字段以保护兼容性和性能。
- 为动态 SQL 定义 null/空集合行为，防止意外全表更新或删除。
- 批处理必须限制大小并定义事务行为。
- 分页和排序必须确定；需要时用索引支持已确认的筛选和排序。
- 枚举、日期时区、JSON、加密字段和小数按当前 TypeHandler/约定映射。
- 保留模块已有的租户、国家、软删除和数据访问条件。

## 模型

Entity 表示持久化行，DTO 表示查询或层间投影。不得把 Entity 泄露给 API BO/VO。继承、Lombok、表注解和基础 Mapper 均取决于当前模块约定，不是通用要求。

## 测试与验证

- 尽可能通过实际构建解析/加载 Mapper XML；
- 测试动态 SQL 分支、空输入、基数、Join 别名、TypeHandler 和回归查询行为；
- 纯单元测试无法证明 SQL 语义时，使用集成/数据库证据；
- 记录 Schema、Mapper、XML 路径和执行证据。

## 阻塞条件

表/Schema、XML 资源约定、基数、数据访问条件或破坏性查询边界无法确认时必须阻塞。
