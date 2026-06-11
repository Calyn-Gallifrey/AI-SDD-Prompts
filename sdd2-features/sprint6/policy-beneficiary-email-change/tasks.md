# tasks.md - policy-beneficiary-email-change

## 1. Task Plan

| Phase | Goal | Status |
|---|---|---|
| Phase 1 | 生成 SDD2.0 proposal/spec/design/tasks 并完成人工审核 | confirmed |
| Phase 2 | 实现受益人邮箱变更 API、Service、Model、Repository 复用 | completed |
| Phase 3 | 增加 Service、Controller、Repository 单元测试 | completed |
| Phase 4 | 运行 SDD 内部 Code Review、Auto-fix、Unit Test Summary、Archive | completed |

## 2. Implementation Checklist

### Phase 2 - Code Implementation

- [x] 新增 `CreatePolicyBeneficiaryEmailChangeWorkOrderRequest`。
- [x] 扩展 `PolicyBeneficiaryChangeWorkOrder` 保存 `beneficiaryEmail`。
- [x] 扩展 `PolicyBeneficiaryChangeWorkOrderResponse` 返回 `beneficiaryEmail`。
- [x] 在 `PolicyBeneficiaryChangeWorkOrderService` 增加 `createEmailChange`。
- [x] 在 `PolicyBeneficiaryChangeWorkOrderController` 增加 `POST /email`。
- [x] 更新 README API 示例。

### Phase 3 - Unit Test Implementation

- [x] Service 成功和异常测试。
- [x] Controller 成功和 validation 测试。
- [x] Repository 重复提交测试。

### Phase 4 - SDD Quality Gates

- [x] 生成 `code-review-findings.md`。
- [x] 输出 Auto-fix Summary。
- [x] 生成 Unit Test Summary。
- [x] Archive 前状态同步。

## 3. Files Allowed to Modify

- `uaw-sdd-demo/README.md`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyBeneficiaryChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/PolicyBeneficiaryChangeWorkOrderResponse.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/entity/PolicyBeneficiaryChangeWorkOrder.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyBeneficiaryChangeWorkOrderService.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyBeneficiaryChangeWorkOrderControllerTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/repository/InMemoryPolicyBeneficiaryChangeWorkOrderRepositoryTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/PolicyBeneficiaryChangeWorkOrderServiceTest.java`

## 4. Files Forbidden to Modify

- `skills/**`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/entity/PolicyInfoChangeWorkOrder.java`

## 5. Phase Review

| Phase | Reviewer Role | Review Time | Result | Findings | Required Action | Next Phase Allowed |
|---|---|---|---|---|---|---|
| Phase 1 | AI-as-human-reviewer | 2026-06-11 12:42 | 通过 | SDD 过程文件已按顺序生成，spec/design/tasks 均已审核。 | 无 | yes |
| Phase 2 | AI-as-human-reviewer | 2026-06-11 12:46 | 通过 | 实现文件均在允许范围内，新增接口未改变既有受益人变更接口语义。 | 无 | yes |
| Phase 3 | AI-as-human-reviewer | 2026-06-11 12:46 | 通过 | Service、Controller、Repository 测试覆盖成功、validation、业务异常和重复提交边界。 | 无 | yes |
| Phase 4 | AI-as-human-reviewer | 2026-06-11 12:50 | 通过 | Code Review 发现 1 个 P2 并完成自动修复；Unit Test Summary 通过；Archive 已完成。 | 无 | yes |

## 6. Human Review

| Review Stage | Reviewer Role | Review Result | Review Comments | Required Fixes | Next Stage Allowed |
|---|---|---|---|---|---|
| tasks | AI-as-human-reviewer | 通过 | 任务拆分、允许修改范围、禁止修改范围和测试目标清晰，可以进入实现。 | 无 | yes |

## 7. Review-driven Auto-fix Summary

Auto-fix Summary：`auto-fix-summary.md`

- Fixed Issues：`CR-P2-001`
- Modified Files：`CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.java`、`PolicyBeneficiaryChangeWorkOrderControllerTest.java`
- Test Files Added / Updated：`PolicyBeneficiaryChangeWorkOrderControllerTest.java`
- Issues Not Fixed：无
- Remaining Risks：真实 UAW 并发提交和工单类型并行策略需业务确认。

## 8. Unit Test Summary

Unit Test Summary：`unit-test-summary.md`

- Entry Mode：SDD_UNIT_TEST
- Actual Test Entry：`mvn test`
- Result：SUCCESS
- Tests run：27
- Failures：0
- Errors：0
- Skipped：0

## Process Status

Current Stage：archive

Stage Status：closed

Last Completed Step：archive completed

Next Required Step：无

Blocked Reason：无

## Process Audit Trail

| Time | Stage | Action | Result | Next Step |
|---|---|---|---|---|
| 2026-06-11 12:42 | tasks | AI generated tasks.md | draft completed | human review |
| 2026-06-11 12:43 | tasks-review | AI-as-human-reviewer reviewed tasks.md | passed | implement Phase 2 |
| 2026-06-11 12:46 | implementation | AI implemented Phase 2 code changes | completed | phase review |
| 2026-06-11 12:46 | unit-test-implementation | AI implemented Phase 3 tests | completed | code review |
| 2026-06-11 12:46 | code-review | SDD_TASK_CODE_REVIEW generated code-review-findings.md | one P2 found | auto-fix |
| 2026-06-11 12:47 | auto-fix | AI fixed CR-P2-001 | completed | unit test |
| 2026-06-11 12:49 | unit-test | mvn test | passed, 27 tests | archive |
| 2026-06-11 12:50 | archive | AI generated archive.md | completed | closed |
