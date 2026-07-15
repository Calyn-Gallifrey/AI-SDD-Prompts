# ServiceStrategy 单元测试规则

用于行为取决于适用条件、优先级或 Strategy 专有执行的 Strategy 实现、Selector、Chain 或 Router。

## Strategy 实现

测试：

1. 匹配、不匹配、null/无效和边界输入的适用性判断；
2. 成功 Strategy 行为及协作者映射；
3. 依赖空值/错误行为；
4. 副作用和拒绝路径无交互；
5. 与已变更 Strategy 关联的回归场景。

## Selector 或 Chain

测试：

- 每个支持类别只选择一个预期 Strategy；
- 明确定义无匹配行为；
- 多重匹配按已批准优先级执行，或明确失败；
- 顺序相关时保持确定性；
- 禁用/不支持的 Strategy 不执行；
- 被选 Strategy 的异常按 Design 传播或映射。

实际可行时使用轻量真实 Strategy。需要独立验证选择/分派而不依赖内部逻辑时 Mock Strategy。

## 数据矩阵

根据已批准业务类别创建场景矩阵，不要为偶然的每个 Enum 值机械创建一个测试：

| 输入类别 | 预期适用 Strategy | 被选 Strategy | 预期结果 |
|---|---|---|---|
|  |  |  |  |

每个支持类别、缺口和有意重叠都必须覆盖。

## 约束

- 不得在 Test Helper 中复制选择逻辑。
- 不得依赖无序集合迭代。
- 不得 Mock 被测 Selector。
- 只有容器排序/Qualifier 本身属于被测行为时，才为获取可直接构造的列表加载 Spring。

记录 Strategy 矩阵覆盖、已变更测试路径/哈希、Profile、精确执行入口、结果数量和范围 SHA-256。
