# Transaction 模块包结构规则

## 触发条件与基线

修改 UAW Transaction 模块时使用。先检查真实模块根目录和最近的现有 Feature 包。当前包结构与构建配置具备权威性；历史完整目录树不能作为创建空目录的指令。

## 所有权

以下层级仅在当前存在或确有需要时使用：

| 区域 | 职责 |
|---|---|
| `base` | 广泛共享且稳定的 Transaction 抽象/契约 |
| `common` | 有多个真实使用方的共享 Transaction 行为 |
| `core/<feature>` | Feature 自有 Controller、Service、Strategy、Model 和持久化代码 |
| `support` | 基础设施 Adapter/工具，不放 Feature 业务逻辑 |
| `task` | 仅用于已批准 Task Feature 的定时/异步入口及支持代码 |

Feature 专有新代码应放在最近的当前 `core/<feature>` 约定下。没有多个具体使用方和已批准所有权决定时，不得提升到 `common/base/support`。

## 包与类规则

- 包名使用小写，并与源码目录一致。
- Service 实现统一遵循当前模块的 `service.impl` 或同等约定；没有证据时不得混用 `implementation`、Service 根目录类和 `impl`。
- 只创建包含已批准文件的包。
- `package-info.java` 遵循当前模块实践，既不是通用必需项，也不是通用禁止项。
- Design/Tasks 中不得包含操作系统专用目录命令，只记录仓库路径和正常文件操作。
- 后缀 `Controller`、`Service`、`ServiceImpl`、`Strategy`、`Mapper`、`Entity`、`BO`、`DTO`、`VO`、`Converter`、`Helper` 必须对应真实职责。

## 依赖方向

- 入口/Controller -> 应用/Service -> Domain/Strategy -> Gateway/Repository 边界；
- 基础设施实现可依赖外部/持久化库，但对外暴露内部契约；
- 下层/共享层不得依赖 Feature Controller 或响应模型；
- 避免循环和跨 Feature 内部依赖，只有已批准时才引入显式共享契约。

## 变更控制

增强或修复应修改现有符号，不得创建平行包树。包移动或重命名属于 Refactor，Design 必须覆盖兼容性、Import、配置、资源更新和回归范围。

## 验证

- 检查 Package Declaration 和资源扫描；
- 检查使用到的 Spring、MyBatis、MapStruct 组件发现；
- 检查依赖方向和重复所有权；
- 编译并测试受影响模块。

## 阻塞条件

真实模块根目录、最近既有模式、所有权或扫描/资源约定不明确时必须阻塞。
