# 静态 Method 单元测试规则

用于确定性静态工具，或必须调用已批准 Design 中既有静态边界的代码。

## 纯静态工具

直接调用 Public Static Method。覆盖实际适用的有效、边界、null/空值、无效和回归输入，并断言完整输出与异常契约。确定性纯函数不需要 Mock。

## 静态依赖

优先通过所属 Public 行为测试。只有同时满足以下条件时才使用有作用域的 Static Mock：

- 当前依赖已支持；
- Refactor 静态边界不在已批准范围内；
- 静态调用是真实的外部或非确定性边界；
- Mock 能在测试作用域中确定性关闭。

未经已批准 Design/Tasks 和新范围评审，不得只为方便而新增 Mockito-inline 或其他 Engine。

## 必查项

- 静态状态不会在测试之间泄露；
- 行为依赖 Locale、Timezone、Clock 或 Random 时受到控制；
- 可变静态状态的并发假设已识别；
- 已断言异常和 Fallback 值；
- 只有可观察行为依赖交互时才验证调用。

## 反模式

- Mock 被测静态 Method；
- 跨测试保持 Static Mock 未关闭；
- 依赖测试执行顺序；
- 修改全局进程状态后不恢复；
- 断言内部 Helper 调用而不是输出。

记录所选 Profile/修饰项、Static Mock 能力证据、已变更测试文件、执行命令和观察结果。
