# 功能提案入口

# 1. 任务基本信息

## 功能名称

- policy-info-change-workorder

## 功能类型

- submit

## 所属模块

- policy / workorder

## 一句话目标

- 新增保单信息变更工单的创建与查询能力，用于验证 UAW-SDD 从提案到归档的完整闭环。

# 2. 变更识别信息

## 变更范围

- API
- Service
- Repository
- Model（DTO / Entity / Enum）
- Test
- Config

## 禁止变更

- 不接入真实数据库。
- 不改动既有 SDD 核心模板以外的历史业务资产。
- 不引入前端页面。
- 不引入公司内网专有依赖。
- 不把本次 SDD 内部 Code Review 生成 HTML 报告。

## 优先级

- P1

# 3. 历史功能引用

## 历史功能目录

- 不适用：本次为新增模拟功能，不基于存量功能 enhancement / refactor。

# 4. 输出信息

## sprint

- sprint6

## 输出目录

- `.project-features/sprint6/policy-info-change-workorder/`

# 5. 补充信息

## 指定参考设计文档

- 未指定。

## 代码工程根目录

- `uaw-sdd-demo/`

说明：现有 proposal 模板没有“代码工程根目录”字段。本次因 SDD 资产位于 `sdd/`，代码工程位于仓库根目录下的 `uaw-sdd-demo/`，因此在补充信息中显式记录，避免扫描范围误判。

## 风险提醒

- 本地 `java -version` 与 `mvn -version` 实际使用 JDK 不一致，可能影响 Mockito / Byte Buddy 等测试工具运行。
- 本次为内网 AI Coding 投入前的体系试跑，流程问题需要比业务功能本身更优先暴露。

# 6. AI 知识底座路径

- AI 知识底座根目录：`.project-ai/`
- 索引文件：`.project-ai/context/1.index.md`
- 上下文目录：`.project-ai/context/`
- 规则目录：`.project-ai/rules/`
- 模板目录：`.project-ai/templates/`

# 7. 当前代码扫描要求

## 默认扫描范围

- SDD 资产根目录：`sdd/`
- 代码工程根目录：`uaw-sdd-demo/`
- 当前模块代码目录：`uaw-sdd-demo/src/main/java/com/example/uawsdddemo/`
- 当前模块测试目录：`uaw-sdd-demo/src/test/java/com/example/uawsdddemo/`

## 需优先检查的存量类型

- Controller / Entry
- Service
- DTO / Entity / Enum
- Repository
- Test
- Maven 配置

# 8. 归档要求

## 归档文件路径

- `.project-features/sprint6/policy-info-change-workorder/archive.md`

## 必须归档的信息

- proposal / spec / design / tasks
- Code Review Findings
- Review-driven Auto-fix Summary
- Unit Test Summary
- SDD 体系问题报告

# Process Status

- Current Stage：Archive
- Stage Status：archived
- Last Completed Step：Proposal 已作为本次模拟 SDD 流程入口使用
- Next Required Step：无，已进入归档
- Human Confirmation Required：no
- Allowed Next Action：作为后续复盘输入读取
- Forbidden Next Action：不得把本文件当作真实生产需求审批记录
- Updated At：2026-05-28 17:06:26 +0800

# Process Audit Trail

| Time | Stage | Action | Input | Output | Result | Next Gate |
|---|---|---|---|---|---|---|
| 2026-05-28 16:30:00 +0800 | Proposal | 用户授权创建 Spring Boot 工程并模拟新增保单信息变更工单 | 用户请求 | proposal-input.md | 通过，进入 Spec | Spec |
| 2026-05-28 17:06:26 +0800 | Proposal | 补充代码工程根目录和风险提醒 | SDD 资产目录与代码目录现状 | proposal-input.md | 通过，作为试跑入口归档 | Spec |
