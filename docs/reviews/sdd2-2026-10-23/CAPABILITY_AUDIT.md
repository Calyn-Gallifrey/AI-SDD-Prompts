# 可复用能力沉淀审计

日期：2026-10-23；设备：Mac-Air。

已检索技术能力库的 QA-003、QA-005、SEC-003、SEC-006 及知识库能力库 DATA-001、QA-001。冻结清单与来源指纹沿用既有方法；知识库旧规划标注属于常规状态治理，没有新增知识维护机制。

已新增并推送两项开发能力：**ASYNC-009、QA-012**。目标文件：`/Users/chenjialin763/Documents/Codex/Config/codex-personal-config/TECHNICAL_CAPABILITIES.md`；配置仓库提交 `4948e76`，推送成功。只提交该能力库文件，未夹带其他项目或配置变更。

## ASYNC-009 Java 8 控制命令的跨进程串行化

- 分类与适用平台：并发与状态一致性；Java 8、Git worktree、文件型流程控制器。
- 问题与适用场景：多个 CLI 进程先读取同一状态，再分别追加批准和写入投影，会使同一消息多次成功，或产生丢失/不一致记录。
- 核心方案与选择依据：在 worktree 的 Git 元数据目录使用 FileChannel/FileLock；先取得 OS 锁，再加载、检查和修改状态；设置有界等待；锁文件长期存在，进程结束由 OS 释放实际锁，不以删除文件清锁。不同 worktree 使用独立锁。
- 实现索引：AI-SDD-Prompts，`skills/uaw-sdd-ai-coding/scripts/Sdd2Control.java` 的 `dispatchSerialized`；同目录 `tests/test_sdd2_control.py` 的并发重复批准测试。
- 复用方法：将全部读改写状态命令放在同一锁边界内，纯预检保持只读；加入同消息并发、进程退出释放与 worktree 隔离验证。
- 验证状态与证据：Mac-Air Java 8 实测，修复前 4 个同消息请求中 3 个成功，修复后只有 1 个成功且批准链仅 1 条。固定证据为 `sdd2.0-frozen-2026-10-23:docs/reviews/sdd2-2026-10-23/probe-results-baseline.json` 与 `probe-results.json` 的 `concurrent-approval`，以及 `verification.json`。
- 限制与代价：等待超过 30 秒拒绝；长测试会占用当前 worktree 的控制命令锁。只约束遵守该入口的 Java 命令，不构成对任意文件编辑器或同权限恶意进程的隔离。
- 来源与更新日期：SDD2.0 冻结前并发审批审计与修复；2026-10-23。

## QA-012 测试执行器来源与结果格式绑定

- 分类与适用平台：测试证据与执行边界；Java 8 CLI，可迁移到有受控工具链的自动化系统。
- 问题与适用场景：只凭可执行文件名和通用 stdout 成功摘要，会把同名假程序或另一测试框架的日志误当作真实测试通过。
- 核心方案与选择依据：系统工具须匹配当前 PATH 解析出的规范路径；仓库 Wrapper 须位于仓库内并与基线提交内容一致；执行前后核对工具哈希；按已选择 Runner 的格式解析数量，零测试或未识别结果保持 blocked。
- 实现索引：AI-SDD-Prompts，`skills/uaw-sdd-ai-coding/scripts/Sdd2Control.java` 的 `trustedTestExecutable`、`parsedTestCounts`、`cmdRunUnitTest`；同目录测试的假执行器和跨格式输出反例。
- 复用方法：先定义可信 PATH/基线工具链，再绑定实际执行路径与输出口径；验证外部同名程序在执行前被拒绝、零测试不能被伪造成功摘要提升、合法安装工具继续可用。
- 验证状态与证据：Mac-Air Java 8 下，外部假 mvn 从旧版 passed 变为执行前拒绝；Python 零测试打印 Maven 成功摘要仍保持 blocked；真实 Maven 三类 Demo 分别 3/3、14/14、23/23 通过。固定证据为 `sdd2.0-frozen-2026-10-23:docs/reviews/sdd2-2026-10-23/probe-results.json` 与 `verification.json`。
- 限制与代价：PATH 与既有 Wrapper 仍是可信前提；不证明全部依赖、插件或测试断言正确。工具链变更需另行验收，其他平台和 Runner 不继承本次 Mac-Air 结果。
- 来源与更新日期：SDD2.0 冻结前测试证明审计与修复；2026-10-23。
