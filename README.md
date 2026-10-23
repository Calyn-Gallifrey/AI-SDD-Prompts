# UAW SDD2.0

当前固定版：`sdd2.0-frozen-2026-10-23`，控制器构建 `2.0-java8.3`。

- [冻结版使用说明与技能包](releases/sdd2.0/README.md)
- [完整审计、修复及验收结果](docs/reviews/sdd2-2026-10-23/AUDIT.md)
- [版本安排与冻结规则](docs/SDD_VERSION_POLICY.md)
- [会话交接](CODEX_HANDOFF.md)

开发入口保持“简要提示词 + 调用 uaw-sdd-ai-coding Skill”。完整 skills 包随附 Java 8 兼容 JAR，控制器运行只需 Java 8+ 和 Git；业务测试使用项目自身工具。

SDD2.0 冻结后不再修改；SDD2.1 仅做用户明确的小升级。读取需求后由 AI 编写简要设计等大升级转阿里云桌面 AWS Kiro；本轮未对该环境做现场验收。

旧 Word 操作指南、旧生成器与 Python 控制器属于历史参考，不作为当前运行入口。运行以固定版 Skill、控制合同及预编译 JAR 为准。
