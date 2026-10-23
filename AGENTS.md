# AI-SDD-Prompts 工作约定

1. 新会话先完整读取 `CODEX_HANDOFF.md`，按任务读取 `docs/SDD_VERSION_POLICY.md` 和对应规则；不默认读取 SDD1.0 的 `sdd/`。
2. SDD2.0 的冻结范围、标签与校验清单以 `releases/sdd2.0/manifest.json` 为准。冻结完成后，不再修改该基线或重写标签/冻结包。
3. 用户要求 SDD2.1 小升级时，从冻结标签建立独立开发分支，保留 SDD2.0；具体需求及发布验收需在该任务确认。禁止把旧的 AI 简要设计规划自动当作 SDD2.1 任务。
4. 需求读取后由 AI 编写简要设计等大升级已交由用户指定的阿里云桌面 AWS Kiro 环境，本仓库本轮不实施。
5. 维护环境可运行 `python3 tools/freeze_sdd20.py` 核验冻结包。Python 属于维护依赖，开发者正式运行仍仅要求 Java 8+ 与 Git。
6. 修改交接前读取适用的 `HANDOFF_STANDARD.md`，保留可接续状态，将已完成任务压缩并指向记录或提交。
7. 执行体系内的人工审核、唯一下一动作、精确范围和真实测试证据约束继续有效；维护仓库的提交授权不能代替业务 Feature 的人工批准。
