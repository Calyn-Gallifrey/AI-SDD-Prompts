# MapStruct 转换规则

## 触发条件与证据

当前模块已使用 MapStruct，或已批准 Design 引入兼容依赖时使用。检查 MapStruct 版本、编译器/插件配置、Component Model、共享 `@MapperConfig`、注入策略、未映射策略和邻近 Converter。

## Component Model

- 使用 `componentModel = "spring"` 时，按模块的 Constructor/Injection 约定通过 Spring 注入生成的 Mapper；不得同时定义或使用 `Mappers.getMapper(...).INSTANCE`。
- 使用默认 Component Model 时，可按当前约定使用静态 `INSTANCE = Mappers.getMapper(...)`，但不得把它标为 Spring Component。
- 同一个 Converter 中禁止混合两种访问模式。

## 映射规则

- 字段重命名、嵌套、转换、默认值或忽略时使用显式 `@Mapping`。
- 明确定义 null 和集合行为；契约相关时不得依赖偶然的 Generator 默认值。
- 只有共享 Config/基础 Converter 真实存在且 Generic/Qualifier 契约匹配时才复用。
- 需要当前用户、时间或 Locale 时，通过显式参数或 `@Context` 传入，避免隐藏全局访问。
- 外部/持久化类型停留在其边界，Converter Method 必须明确所有权。
- Update 映射要定义 null 是覆盖还是忽略。
- 自定义 Expression/Default Method 必须确定且无副作用。

## 验证与测试

- 使用实际 Annotation Processor 编译生成源码；
- 测试重命名、嵌套、默认值、null、集合和 Update 语义；
- 按所选 Component Model 验证 Spring 注入或静态访问；
- 检查未映射 Target 的 Warning/Error，并显式处理有意忽略项。

## 阻塞条件

模块配置、Component Model、共享 Mapper Config 或映射契约无法确认时必须阻塞。不得引入第二套不兼容 MapStruct 约定。
