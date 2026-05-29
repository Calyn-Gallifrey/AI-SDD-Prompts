# SDD 体系试跑问题报告

## 结论

本次 Spring Boot + Maven 示例工程已跑通 SDD 标准链路，但这套 SDD 体系在正式投入公司内网 AI Coding 前仍有两个 P0 问题必须先修：缺少“代码工程根目录”字段，缺少“环境预检闸门”。这两个问题会直接导致 AI 扫描错工程、测试在不同机器上结果不一致，进而让后续 spec / design / tasks / review 的可信度下降。

## 核心结果

### 已确认

- 已创建 Spring Boot Maven 工程：`uaw-sdd-demo/`。
- 已实现保单信息变更工单创建与查询能力。
- 已生成 SDD 标准资产：`proposal-input.md`、`spec.md`、`design.md`、`tasks.md`、`archive.md`。
- 已执行 SDD 内部 Code Review，没有生成 HTML 报告，也没有创建 `reports/code-review/YYYY-MM-DD/`。
- 首次 `mvn test` 失败，失败原因为 Maven 实际使用 Java 26，Byte Buddy 默认不支持 Java 26 class file 70。
- Auto-fix 后再次执行 `mvn test` 成功：Tests run: 9, Failures: 0, Errors: 0, Skipped: 0。

### 推断

- 如果公司内网开发机、CI、Maven 工具链未统一 JDK，则同一 SDD 任务可能在不同环境得到不同测试结论。
- 如果真实业务仓库里 SDD 资产目录与代码目录分离，当前模板容易让 AI 把 `sdd/` 当作代码工程根目录。
- 当前 testing 规则对 UAW 存量工程友好，但对 Spring Boot 3 默认 JUnit5 项目不够稳。

### 待确认

- 公司内网目标 JDK 版本。
- Maven 是否强制使用同一 JDK。
- 内网 Maven 仓库是否允许拉取 Spring Boot 3.3.5、JUnit Vintage、Mockito、Byte Buddy 相关依赖。
- UAW 真实工程是否仍统一使用 JUnit4，还是存在 JUnit5 / Spring Boot 3 混合项目。

## 依据与判断

| 编号 | 严重程度 | 问题 | 依据 | 影响 |
|---|---|---|---|---|
| SDD-001 | P0 | 模板缺少“代码工程根目录 / 模块根目录”字段 | 本次 SDD 资产在 `sdd/`，代码工程在 `uaw-sdd-demo/`；只能在 proposal 补充信息里手写 | AI 可能扫描错目录，导致 spec / design / tasks 基线失真 |
| SDD-002 | P0 | 缺少环境预检闸门 | `java -version` 与 `mvn -version` 使用的 JDK 不一致；首次 `mvn test` 因 Java 26 / Byte Buddy 失败 | 正式内网使用时，构建失败会被误判成代码问题，或在不同机器结果不一致 |
| SDD-003 | P1 | 测试规则缺少技术栈 profile | 为贴合当前 testing 规则，本次引入 JUnit Vintage 并写 JUnit4 测试；Spring Boot 3 默认更偏 JUnit5 | 新老工程混用时，AI 容易强套测试风格 |
| SDD-004 | P1 | 人工确认与模拟确认没有正式区分 | 模板只定义人工确认，本次只能写“模拟确认”防止伪造审批 | 试跑、CI 自动化、真实人工审批之间的证据边界不清 |
| SDD-005 | P1 | 首次失败和 Auto-fix 证据不是一等结构 | tasks / archive 可记录 Unit Test Summary，但没有专门字段要求记录“首次失败 → 修复 → 重跑” | AI 可能只保留最终 pass，丢失关键问题证据 |
| SDD-006 | P1 | Archive 模板结构有阅读顺序问题 | `5.archive-template.md` 中最终结论出现在 Code Review 归档证据和 Process Status 之前，且后段再次出现流程状态 | 后续人员阅读时容易错过质量证据 |
| SDD-007 | P2 | 样板资产缺少统一索引和有效性状态 | 旧版 `agreement-information-query` 需要手动标注旧版样板；新样板、真实试跑、旧样板未统一分类 | 后续 AI 可能误用旧资产 |
| SDD-008 | P2 | 内网依赖缓存策略未进入 SDD 输入 | 本次首次 Maven 运行需要解析外部依赖；公司内网可能无法联网 | 真实使用时任务可能卡在依赖下载，而不是编码问题 |

## 风险与待确认点

- P0 风险：如果不加代码工程根目录字段，SDD 在多模块、多 repo、资产目录分离场景下不稳定。
- P0 风险：如果不加环境预检，测试失败原因会混入业务缺陷、依赖缺陷、JDK 缺陷，影响 AI 自动修复判断。
- P1 风险：如果 testing 规则继续单一化，后续真实项目会出现“为了符合规则而改测试栈”的反向适配。
- P1 风险：如果没有模拟模式，试跑资产可能被误读为真实人工审批通过。

## 下一步建议

### P0

1. 在 `proposal-input-template.md`、`spec-template.md`、`tasks-template.md` 中新增 `Code Project Root` / `Module Root` / `Build Command` 字段，并要求进入 spec 前先扫描该目录。
2. 在 `1.index.md` 和 `tasks-template.md` 增加 Environment Preflight Gate，至少记录 `java -version`、`mvn -version`、`JAVA_HOME`、`mvn test -DskipTests` 或等价轻量检查、依赖仓库可用性。

### P1

1. 把 testing 规则拆成 profile：UAW-JUnit4、SpringBoot-JUnit5、Legacy-Mockito、No-UAW-Util，生成测试前先选择 profile。
2. 增加 `Run Mode`：production / dry-run / simulation，并把人工确认字段改成可表达 `human-confirmed`、`user-authorized-simulation`、`ci-auto`。
3. 在 tasks / archive 中增加 Build/Test Attempt 表，强制记录首次失败、修复动作、重跑结果，避免只留下最终通过结论。
4. 调整 archive 模板顺序，把 Code Review Evidence、Auto-fix、Unit Test Summary 放到最终结论之前，并避免重复 Process Status。

### P2

1. 建立 `.project-features/README` 或资产索引，标注 old-sample / sample / real-run / deprecated。
2. 增加内网依赖缓存说明：Maven mirror、私服地址、离线依赖策略、首次依赖解析失败时的处理方式。
3. 增加真实业务二次试跑：选择一个已有 UAW 服务模块，用同样流程验证 SDD 是否仍存在规则过拟合。
