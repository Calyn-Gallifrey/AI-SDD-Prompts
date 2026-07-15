# Case Tracker 兼容规则

## 触发条件

只有已批准变更新增、重命名或下线 Transaction Type，且当前代码确认 Case Tracker 依赖该类型时才加载。

## 必需当前证据

Design 前确认并记录：

- 当前 Transaction Type Enum/配置符号和文件；
- 当前 Case Tracker 查询/选择路径；
- 当前字典表/Schema 和迁移约定；
- 来自已批准需求的精确持久化 Transaction Type、Code 和 Display Value；
- 现有唯一性、语言、国家、状态和排序语义；
- 发布与回滚机制。

`TransactionTypeConfigEnum`、`iic_crm_base_data` 等历史名称只能作为发现线索。当前代码/Schema 未确认时，不得根据这些名称生成编辑或 SQL。

## 设计规则

1. 定义唯一规范 Transaction 标识，并显式映射 Enum/配置、持久化 Code、Display Text 和 Case Tracker 行为。
2. 除非迁移已批准，否则保留现有标识；修改 Display Name 不得静默改变持久化 Code。
3. 使用项目既有迁移路径。Skill 不得执行数据库变更。
4. 迁移必须确定且按当前项目约定可安全重复执行，避免无条件删除后重插导致本地化或用户维护数据丢失。
5. 定义 Code 已存在但值不同时的冲突行为。
6. 只有当前 Schema 和需求确认时，才加入语言、国家、状态和顺序字段。
7. 定义回滚/禁用行为，以及对现有 Transaction 的兼容性。

## 必需测试

- 新类型映射到预期 Case Tracker 路径；
- 现有 Transaction Type 保持不变；
- 明确定义未知/禁用类型行为；
- 处理重复或配置冲突；
- 持久化/显示映射使用已批准值；
- 无法执行数据库测试时记录迁移验证。

## 阻塞条件

当前 Enum/配置所有者、表/Schema、规范 Code 或 Case Tracker 行为无法确认时必须阻塞。不得使用历史示例补全缺口。
