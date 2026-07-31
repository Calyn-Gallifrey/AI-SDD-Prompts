# Codex 交接

## 当前任务

将 UAW-SDD 2.0 正式运行时从 Python 切换为 Java 8 兼容控制器，同时保持开发者公开入口不变：

```text
简要提示词 + 调用 uaw-sdd-ai-coding Skill
```

目标是让只有 Java 8 和 Git、没有 Python/Node/额外服务的内网开发机仍能完整执行 SDD2.0，并继续满足以下 P0 要求：

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

## 当前验证结果

- Java 正式控制器原有流程/攻击回归：48/48 通过。
- Java 8 字节码、只读 `doctor`、JAR 校验失败中文恢复：3/3 通过。
- Python/Java 双向状态与审批链兼容：单项回归通过。
- 合并后的 52 项全套控制器回归：52/52 通过。
- 旧 Python 参考控制器原有回归：48/48 通过。
- 真实小功能完整 Demo：通过。
- Demo 功能：联系人显示名称规范化；真实 Maven 测试 3/3 通过。
- Demo 攻击检查：乱文件、提前资产、重复 Feature、状态篡改、提前生产代码、审批链篡改、测试证据篡改和活动自动提交均被阻断。
- Demo 最终状态：`archive / completed`；九项公开资产完整；Git 提交数始终为基线 1。
- 最新 Demo 测试执行证据 SHA-256：`bcaeea6e966e9a36d6f3cf09c0e5ddb501a585a921938678555fb6eb613f2ed8`。
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
- `uaw-sdd-demo/`
- `CODEX_HANDOFF.md`

## Git 与下一步

- Git 根目录：`AI-SDD-Prompts/`。
- 分支：`main`，相对 `origin/main` 存在未推送提交。
- Java 8 环境验收前的控制器提交为 `b32791b`。
- 不得暂存 `docs/.DS_Store`。
- 不执行 push。
- 后续内网部署验收继续使用原入口：简要提示词加 `uaw-sdd-ai-coding` Skill，不要求开发者手工运行控制命令。
