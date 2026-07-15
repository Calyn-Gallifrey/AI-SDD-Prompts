# Codex 交接

## 当前任务

在不改变已上线开发者入口的前提下，将 UAW-SDD 2.0 的体系文件和新生成资产统一为简体中文主体，并以自动校验和完整回归维持 5/5 的仓库控制成熟度。

开发者入口保持为：提交简要提示词并调用 `uaw-sdd-ai-coding`。

## 范围与约束

- 范围仅限 SDD2.0。
- `sdd/` 属于 SDD1.0，继续排除且未修改。
- 开发者不需要运行控制脚本、维护 `.sdd2/`、提供 Git 哈希或填写新增表单。
- `original/` 是保留原文和来源哈希的导入档案，不是当前运行规则；活跃 Skill 不得直接加载。
- 三个 `execution_mode=historical-example` Feature 是不可变历史证据，不回写翻译，也不能作为当前审批或 Gate 证据。
- 无关未跟踪文件 `docs/.DS_Store` 保持未暂存、未修改。

## 当前状态

- Demo 预演发现的 3 个控制缺陷已在先前提交中关闭，并具备回归覆盖。
- 简体中文主体规则、三项 Skill 翻译、模板翻译和资产语言闸门已完成。
- 当前结论：在已执行的 SDD2 仓库控制与语言验收矩阵内达到 5/5。
- SDD2 实现和文档工作已完成；剩余外部阻塞仅为本机 GitHub HTTPS 身份验证。

## 本轮语言加固

1. 新增 `skills/uaw-sdd-ai-coding/references/language-policy.md`，作为人类可读文件和生成资产语言规则的唯一来源。
2. 三项 Skill 的说明、运行规则、模板、示例和代理元数据改为简体中文主体。
3. `init` 在获取 Feature 锁之前校验 `brief-design.md`；`record-artifact` 在写入 revision/hash 之前校验九项公开资产。
4. 英文主导正文和繁体正文会被非零退出硬阻塞；文件名、路径、命令、代码标识符、Schema 键、状态枚举、哈希、技术缩写和外部契约原值可精确保留。
5. 静态验证同时覆盖 46 个 Skill 人类可读运行文件，以及 handoff、两份正式报告、Demo README 和生成的 DOCX。
6. DOCX 指南已加入语言合同、验收项和历史边界并重新生成。

## 长期产物

- 唯一语言规则：`skills/uaw-sdd-ai-coding/references/language-policy.md`
- 控制合同：`skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md`
- Demo 预演报告：`docs/reviews/UAW-SDD2.0-demo-rehearsal-2026-07-15.md`
- 全盘审查与整改报告：`docs/reviews/UAW-SDD2.0-full-audit-2026-07-14.md`
- 操作指南：`docs/UAW-SDD2.0 Skill化方案说明与操作指南.docx`
- 先前 Demo 控制修复提交：
  - `e5829b9 fix(sdd2): preserve demo approval provenance`
  - `4218185 fix(sdd2): close demo rehearsal control gaps`

## 验证结果

- SDD2 控制回归：20/20 通过。
- 静态资产与语言验证：53 个 runtime 文件、51 个人类可读文件、3 个历史 Feature、26 个来源档案；0 error、0 warning。
- 三项 Skill 快速结构验证：全部 valid。
- 三个历史 Feature 控制校验：3/3 通过，仅返回预期的 `HISTORICAL_EXAMPLE_NOT_VALID_GATE_EVIDENCE`。
- Python 编译、JSON 解析：通过。
- Demo Maven 回归：36/36 通过，0 failure、0 error、0 skipped。
- DOCX 结构：124 个段落、29 个表格、4 张内嵌图、4747 个汉字；语言合同和来源档案边界内容存在。
- DOCX 视觉：macOS Quick Look 确认中文字形正常；LibreOffice 渲染 12 页，版式无遮挡、裁切和表格溢出。当前主机 LibreOffice 的 CJK 字体回退异常，因此不以它证明中文字形。
- 四张生成图：逐张视觉检查通过；标题、说明和动作文字以简体中文为主体，只保留 Skill 名、阶段枚举、文件名及 Git/Scope/Hash 等必要英文标识。
- 排除路径检查：`sdd/` 下无变更。
- Git whitespace：`git diff --check` 通过。

## 平台边界

宿主提供稳定 message ID 时，审批会绑定该 ID 并防止重放。宿主无法提供可独立查询的 message ID 时，仓库可以证明已记录的来源/角色、精确文本或摘要、时间、attempt、stage、revision/hash 和哈希链，但不超出证据声称能够独立证明外部 UI 账户身份。

## Git 与同步

- 分支：`main`；上游：`origin/main`。
- 本轮语言加固将与本 handoff 一起提交；提交后本地预计相对上游 ahead 6、behind 0。
- 本机仍缺少可用的 GitHub HTTPS 凭据，推送预计继续返回：

```text
fatal: could not read Username for 'https://github.com': Device not configured
```

- 恢复方式：为当前 `origin` 配置 Git 身份验证后运行 `git push origin main`。

## 下一步 P0

为 Git 配置身份验证并推送 `main`。保持 `docs/.DS_Store` 未暂存；当前没有其他 SDD2 代码、文档或语言整改待办。
