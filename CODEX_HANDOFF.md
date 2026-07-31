# Codex 交接

## 当前任务

在真实 Java 8 环境中使用大型多文件功能深度验证 UAW-SDD 2.0 全流程，同时保持开发者公开入口不变：

```text
简要提示词 + 调用 uaw-sdd-ai-coding Skill
```

本轮大型 Demo 覆盖需求修订、生产实现、Code Review 返工、Unit Test 两轮交接、真实测试失败恢复和 Archive，并继续验证以下 P0 要求：

1. 流程不得跳步或串 Feature。
2. Spec、Design、Tasks、Phase Review、Unit Test Summary 和 Archive 的人工审核不得丢失。
3. Feature 目录不得乱生成文件、目录或提前阶段资产。
4. Code Review、Auto-fix、Unit Test 和 Archive 必须绑定当前范围及真实证据。
5. 状态、审批、质量门、测试证据和恢复点必须一致且可追溯。
6. 活动流程不得自动提交或推送。

## 范围与约束

- 范围仅包含 SDD2.0。
- `sdd/` 属于 SDD1.0，本轮未读取、未修改。
- 开发者入口、Brief 字段和调用方式均未改变。
- 正式运行文件和生成资产继续以简体中文为主体。
- 未更新 Word 操作指南及其生成器。
- `docs/.DS_Store` 是无关未跟踪文件，保持未暂存、未修改。
- 本轮只创建本地提交，不执行 push；用户后续手动推送。

## 已实施修复

### 1. Java 8 正式控制器

- 新增 `skills/uaw-sdd-ai-coding/scripts/Sdd2Control.java`。
- 使用 Java 8 标准库实现原控制器全部 15 个流程命令，并新增只读 `doctor`。
- 新增预编译 `scripts/runtime/sdd2-control.jar`，编译参数为 `javac --release 8`。
- JAR 主类字节码为 class major 52，运行依赖经 `jdeps` 检查仅为 JDK 标准库。
- 新增 `scripts/runtime/sdd2-control.sha256`；每次控制命令启动前自动校验自身 JAR，缺失或不匹配时拒绝执行。
- 新增维护构建脚本 `scripts/build_sdd2_java8.sh`；开发机不需要 `javac`、Maven 或现场编译。
- 旧 `sdd2_control.py` 仅保留为维护回归和迁移对照，正式 Skill 与子 Skill 不再引用或调用。

### 2. 运行环境预检与中文恢复提示

- 创建任何 Feature 目录或资产前，主 Skill 必须先执行 `java -version`，再执行 JAR `doctor`。
- Java 不存在时，必须提示安装或启用 Java 8 及以上版本并配置 `PATH/JAVA_HOME`，同时明确本次未生成 Feature 资产或业务代码。
- JAR/校验文件缺失、损坏、版本不兼容或 `doctor` 非零时，必须提示重新获取完整运行包并停止。
- 禁止回退到 Python、Node、源码运行、现场编译、Maven 或联网下载控制器依赖。
- `doctor` 不创建目录、不写 Feature 文件、不安装 Git Hook。
- 即使弱模型跳过 `doctor`，任意 JAR 命令仍会先执行完整性自检。

### 3. 状态机与旧资产兼容

- Java 控制器保留既有阶段、唯一 `next_required_action`、回合硬停止、人工 Gate、实现许可、范围冻结、哈希链、测试证据、Archive 和 Git Guard 语义。
- 命令参数使用白名单；未知参数、缺失值、给布尔标志传值、非法枚举和多余位置参数均拒绝执行。
- 路径统一解析为真实路径，避免 macOS `/var` 与 `/private/var` 导致 Feature 边界误判。
- JSON 整数保持整数类型，确保事件/审批哈希与旧 Python 状态完全兼容。
- 已验证 Java 创建的状态可由旧参考实现恢复，旧参考实现生成到 Spec 批准后的状态也可由 Java JAR 恢复并继续记录 Design。

### 4. Java 8 Demo 基线

- `uaw-sdd-demo` 从 Spring Boot 3 / Java 17 调整为 Spring Boot 2.7 / Java 8。
- Validation 包从 `jakarta.validation` 调整为 Java 8 兼容的 `javax.validation`。
- 移除 `List.copyOf`，改为 Java 8 可用且保持 null 拒绝、不可变返回语义的防御性拷贝。
- 静态验证器新增 Java 8 后置 API 扫描，阻止常见 Java 9+ API 回归。
- Demo 项目生产类和正式控制器均确认生成 class major 52。

### 5. 大型深度 Demo

- 新增 `scripts/demo_sdd2_large_feature.py`，只在临时 Git 仓库和临时 linked worktree 中运行。
- Demo 功能为“批量保单联系方式变更预检与幂等计划生成”，包含六个生产类、两个测试类和三个生产实现 Phase。
- 覆盖不同 worktree 并行隔离、同 worktree 串 Feature、需求修订失效、批准消息防重放、过宽范围、实现许可篡改、范围外修改、commit/push Guard、Code Review 失败返工、Unit Test 两轮交接、真实测试失败返工、测试/Archive 证据篡改和最终锁释放。
- 测试源码严格在首次 Code Review 与 Auto-fix 关闭后生成；测试变化后重新冻结并完整复审，符合 `uaw-unit-test` 两轮交接契约。

### 6. Demo 模式模糊批准修复

- 大型 Demo 发现：已授权 `demo-simulation` 曾跳过 `explicitApproval`，会把仅含 `ok` 的文本错误记录为当前阶段批准。
- Java 正式控制器与 Python 维护参考实现已统一修复：所有批准来源都必须先明确识别当前阶段和批准结论；Demo 授权不再降低批准语义。
- 新增回归，确认模糊 Demo 批准返回非零、状态保持当前 Gate 且批准链不新增记录。
- 正式控制器版本更新为 `2.0-java8.2`。

## 当前验证结果

- Java 8 正式控制器扩展回归：53/53 通过。
- Python 维护参考实现同套回归：53 项通过，三个 Java 专属检查按设计跳过。
- Python/Java 双向状态与审批链兼容：通过。
- 真实小功能完整 Demo：通过。
- Demo 功能：联系人显示名称规范化；真实 Maven 测试 3/3 通过。
- Demo 攻击检查：乱文件、提前资产、重复 Feature、状态篡改、提前生产代码、审批链篡改、测试证据篡改和活动自动提交均被阻断。
- Demo 最终状态：`archive / completed`；九项公开资产完整；Git 提交数始终为基线 1。
- 最新小 Demo 测试执行证据 SHA-256：`34c6b2834647a72e6ef23f871768e7f2debbb01b42a010d07244210630bcd5ad`。
- 大型深度 Demo：19/19 检查点通过，最终 `archive / completed`。
- 大型 Demo 首次真实测试：14 项中 13 项通过、1 项失败，Archive 被阻断。
- 大型 Demo 修复后真实测试：14/14 通过，0 failure、0 error、0 skipped。
- 大型 Demo 最终证据：四次冻结代码修订、九项公开资产、十九份不可变资产快照、十一条批准链记录、五十五条事件链记录，Git 提交数保持基线 1。
- 最新大型 Demo 测试执行证据 SHA-256：`706495bb3ab6bb06d36db59ddf5eaaaaead5cd24967a5c5e61a49d2c9a66552d`。
- 最新大型 Demo Archive 证据 SHA-256：`0e6af1624f15ad4bde316a873c087f4fdaec101d802549d9554aa7ee6cc8bb35`。
- Java Demo 项目完整回归：36/36 通过，0 failure、0 error、0 skipped。
- 静态资产验证：0 error、0 warning。
- 三个 Skill 的 `quick_validate.py`：全部通过。
- `git diff --check`：通过。

## Java 8 实机环境验收

2026-07-31 已在本机安装的 Amazon Corretto `1.8.0_502` 上完成环境验收，结论为通过：

1. 显式设置 Java 8 `JAVA_HOME` 和 `PATH` 后，控制器 `doctor` 返回 `java_specification_version=1.8`、JAR 完整性通过、`wrote_feature_files=false`。
2. Java 8 下完整控制器回归 `52/52` 通过，覆盖阶段 Gate、人工批准链、实现许可、范围冻结、乱文件、串 Feature、状态/证据篡改、质量门和自动提交阻断。
3. Java 8 下真实小功能完整 Demo 通过，最终状态为 `archive / completed`，九项公开资产完整，真实 Maven 测试 `3/3` 通过，Git 提交数保持基线 1。
4. 本次 Demo 测试执行证据 SHA-256 为 `ba9668579844f569dfac9f460a26192bffc100adc3d1ce8176f3ceea23e95028`。
5. `uaw-sdd-demo` 使用 Maven 3.9.16 和 Corretto 8 完整执行 `36/36` 项测试，0 failure、0 error、0 skipped；代表性生产类为 class major 52。
6. 在子进程 `PATH` 中只提供 Java 8 和 Git、不提供 Python、Node 或 Maven 时，控制器 `doctor` 仍通过。
7. 最终控制器 JAR 版本为 `2.0-java8.2`，SHA-256 为 `dedc3bac2981886296a84bb163576d861b167cc77f590ae524f17b58d928c407`，主类为 class major 52，`jdeps` 仅依赖 `java.base`。

Python 仅用于仓库维护者的测试和 Demo 编排，不属于开发者正式运行路径。Maven 仅用于本次 Demo 项目自身的编译和测试，也不属于控制器依赖。

## 主要修改文件

- `skills/uaw-sdd-ai-coding/SKILL.md`
- `skills/uaw-sdd-ai-coding/references/process-control.md`
- `skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md`
- `skills/uaw-code-review/references/code-review-rules.md`
- `skills/uaw-sdd-ai-coding/scripts/Sdd2Control.java`
- `skills/uaw-sdd-ai-coding/scripts/runtime/sdd2-control.jar`
- `skills/uaw-sdd-ai-coding/scripts/runtime/sdd2-control.sha256`
- `skills/uaw-sdd-ai-coding/scripts/build_sdd2_java8.sh`
- `skills/uaw-sdd-ai-coding/scripts/java8/MANIFEST.MF`
- `skills/uaw-sdd-ai-coding/scripts/tests/test_sdd2_control.py`
- `skills/uaw-sdd-ai-coding/scripts/validate_sdd2_assets.py`
- `skills/uaw-sdd-ai-coding/scripts/demo_sdd2_small_feature.py`
- `skills/uaw-sdd-ai-coding/scripts/demo_sdd2_large_feature.py`
- `uaw-sdd-demo/`
- `CODEX_HANDOFF.md`

## Git 与下一步

- Git 根目录：`AI-SDD-Prompts/`。
- 分支：`main`，相对 `origin/main` 存在未推送提交。
- Java 8 环境验收前的控制器提交为 `b32791b`。
- 不得暂存 `docs/.DS_Store`。
- 不执行 push。
- 本轮大型 Demo、P0 修复和交接结果只创建本地提交，不执行 push。
- 内网开发继续使用原入口：简要提示词加 `uaw-sdd-ai-coding` Skill，不要求开发者手工运行控制命令。
