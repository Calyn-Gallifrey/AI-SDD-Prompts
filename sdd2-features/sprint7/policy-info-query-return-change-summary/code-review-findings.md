# code-review-findings.md - policy-info-query-return-change-summary

> HISTORICAL EXAMPLE ONLY (quarantined 2026-07-14): this file predates deterministic SDD2 control. Approval, reviewer, status, and business text below is legacy illustration, not valid gate evidence or reusable requirement input.

## 1. 基本信息

- Entry Mode：SDD_TASK_CODE_REVIEW
- Feature Directory：`sdd2-features/sprint7/policy-info-query-return-change-summary`
- Review Time：2026-06-17 14:15 CST
- Reviewer Role：AI-as-code-reviewer
- Review Conclusion：通过

## 2. 输入资产

- `brief-design.md`：已读取
- `proposal-input.md`：已读取
- `spec.md`：已读取
- `design.md`：已读取
- `tasks.md`：已读取
- 当前代码变更范围：
  - `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/PolicyInfoChangeWorkOrderResponse.java`
  - `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java`
  - `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderServiceTest.java`
  - `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderControllerTest.java`
  - `uaw-sdd-demo/README.md`

## 3. 评审范围

### 允许评审范围

- 既有 `GET /api/work-orders/policy-info-change/{workOrderId}` 查询响应新增 `changeSummary`。
- 与新增响应字段直接相关的 DTO、service mapping、controller serialization test、service unit test、README。

### 禁止扩大范围

- 新增 API。
- 新增工单类型。
- 新增 repository 方法、持久化字段、数据库表或外部系统调用。
- 修改 `POST /api/work-orders/policy-info-change` 的请求语义或响应边界。
- 修改受益人变更或 I need document 功能。

## 4. 必查项

- [x] 实现符合 spec 范围和边界
- [x] 实现符合 design 落位和流程设计
- [x] tasks 中确认的任务均已完成
- [x] 未创建约定之外的目录或文件
- [x] 未绕过项目异常、安全或测试规范
- [x] 单元测试影响点已识别
- [x] 验证方式已记录
- [x] 未出现未经批准的范围扩张

## 5. 评审结果

- P0 Count：0
- P1 Count：1
- P2 Count：0
- Suggestion Count：0
- Review-driven Auto-fix Required：completed
- Fix Scope：限制 `changeSummary` 只在 GET 查询响应中返回
- Files allowed to modify：
  - `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/PolicyInfoChangeWorkOrderResponse.java`
  - `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java`
  - `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderServiceTest.java`
  - `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderControllerTest.java`
  - `sdd2-features/sprint7/policy-info-query-return-change-summary/design.md`
  - `sdd2-features/sprint7/policy-info-query-return-change-summary/tasks.md`
- Files forbidden to modify：受益人变更、I need document、repository、entity、pom.xml
- Unit tests required：yes
- Unit test focus：GET 返回 `changeSummary`；POST 创建响应不返回 `changeSummary`
- Untracked files reviewed：current feature asset directory files
- Archive allowed：yes

## 6. Findings 明细

| 问题编号 | 严重程度 | 问题类型 | 文件路径 | 方法 / 类 | Diff 位置 | 关联 SDD 依据 | 问题描述 | 风险影响 | 修复建议 | 是否阻塞 Archive |
|---|---|---|---|---|---|---|---|---|---|---|
| CR-P1-001 | P1 | Scope Deviation | `PolicyInfoChangeWorkOrderService.java` / `PolicyInfoChangeWorkOrderResponse.java` | `create` / shared response DTO | `toResponse` always sets `changeSummary` | `brief-design.md` / `spec.md` / `design.md` | 当前实现通过共享响应 DTO 和统一 mapping 让 `POST /api/work-orders/policy-info-change` 创建响应也返回 `changeSummary`，超出了本次“增强既有 GET 查询响应”的确认范围。 | 调用方可能观察到未经确认的 POST 响应变化，违背最小增强原则。 | 将 `changeSummary` 限制在 GET 查询响应；POST 创建响应不返回该字段，并补充测试保护。 | yes |

## 7. Auto-fix 交接

- Auto-fix Required：yes
- Auto-fix Priority：P1
- 修复边界：只调整 policy-info-change 查询响应相关 DTO 序列化、service mapping 和测试
- 测试补充要求：
  - Controller create response must not include `changeSummary`
  - Controller get response must include `changeSummary`
  - Service create response keeps `changeSummary` unset
  - Service get response returns expected `changeSummary`
- 不修复项及原因：无

## 8. Post Auto-fix Verification

- Recheck Result：passed
- Rechecked Issues：CR-P1-001 fixed
- Remaining P0 / P1 / Blocking P2：none
- Archive allowed after Auto-fix：yes
- Next Gate：Unit Test Summary

## 9. Unit Test 交接

- Selected Testing Profile：UAW-JUnit4
- Unit Test Required：yes
- 必须覆盖场景：
  - GET 查询返回 `changeSummary`
  - POST 创建响应不返回 `changeSummary`
  - Service query mapping 正确派生字段
- 可不覆盖场景及原因：真实数据库字段与外部系统不适用，本 demo 使用内存 repository
- 实际验证方式要求：Local CLI `mvn test`

## 10. 结论

- 是否允许进入 Auto-fix：yes
- 是否允许进入 Unit Test：yes
- 是否允许进入 Archive：yes, after Unit Test Summary passed
- 备注：CR-P1-001 已修复，GET 查询返回 `changeSummary`，POST 创建响应不返回 `changeSummary`。
