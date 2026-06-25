# SDD Code Review Findings

> 本模板仅用于 `Entry Mode: SDD_TASK_CODE_REVIEW`。
> 本文件是 SDD 流程内 Markdown 质量闸门产物，不是 HTML 报告，不得读取或套用 HTML 报告模板。

---

# 1. 基本信息

- Entry Mode：SDD_TASK_CODE_REVIEW
- Feature Directory：
- Review Time：
- Reviewer Role：
- Review Conclusion：blocked / 拒绝通过 / 有条件通过 / 通过

# 2. 输入资产

- proposal-input.md：
- spec.md：
- design.md：
- tasks.md：
- 当前代码变更范围：

# 3. 评审范围

## 允许评审范围

-

## 禁止扩大范围

-

# 4. 必查项

- [ ] 实现符合 spec 范围和边界
- [ ] 实现符合 design 落位和流程设计
- [ ] tasks 中确认的任务均已完成
- [ ] 未出现未经批准的范围扩张
- [ ] 未创建约定之外的目录或文件
- [ ] 未绕过项目工具类、日志、异常、安全、测试规范
- [ ] 单元测试影响点已识别
- [ ] 验证方式已记录

# 5. 评审结果

- P0 Count：
- P1 Count：
- P2 Count：
- Suggestion Count：
- Review-driven Auto-fix Gate Required：yes
- Code Fix Required：yes / no
- Fix Scope：
- Files allowed to modify：
- Files forbidden to modify：
- Unit tests required：yes
- Unit test focus：
- Untracked files reviewed：
- Archive allowed：yes / no

# 6. Findings 明细

| 问题编号 | 严重程度 | 问题类型 | 文件路径 | 方法 / 类 | Diff 位置 | 关联 SDD 依据 | 问题描述 | 风险影响 | 修复建议 | 是否阻塞 Archive |
|---|---|---|---|---|---|---|---|---|---|---|
|  | P0 / P1 / P2 / Suggestion |  |  |  |  | spec / design / tasks |  |  |  | yes / no |

# 7. Auto-fix 交接

- Auto-fix Gate Required：yes
- Code Fix Required：yes / no
- Auto-fix Priority：
- 修复边界：
- 测试补充要求：
- 不修复项及原因：

# 8. Post Auto-fix Verification

- Recheck Result：passed / failed / not yet run
- Rechecked Issues：
- Remaining P0 / P1 / Blocking P2：
- Archive allowed after Auto-fix：yes / no / not yet
- Next Gate：

# 9. Unit Test 交接

- Selected Testing Profile：
- Unit Test Required：yes
- 必须覆盖场景：
- 可不覆盖场景及原因：
- 实际验证方式要求：

# 10. 结论

- 是否允许进入 Auto-fix：
- 是否允许进入 Unit Test：
- 是否允许进入 Archive：
- 备注：

---

# Template Rules

1. SDD Code Review Findings 是质量闸门产物，不是过程说明。
2. 缺少 `proposal-input.md`、`spec.md`、`design.md`、`tasks.md`、实现变更范围或未跟踪文件清单时，`Review Conclusion` 必须为 `blocked`。
3. 第 4 节必查项不得保留 `[ ]`；每项必须基于实际检查更新为已检查结果，并记录必要说明。
4. `Unit tests required` 和 `Unit Test Required` 在 SDD 模式下固定为 `yes`。
5. `Archive allowed` 只有在无 P0 / P1 / Blocking P2，且 Post Auto-fix Verification 通过后才能为 `yes`。
6. 不得用 standalone HTML 报告替代本文件。
7. Auto-fix Gate 在 SDD 模式下固定必走；没有代码修复项时，也必须输出 `auto-fix-summary.md` 并记录不需要修复的原因。
