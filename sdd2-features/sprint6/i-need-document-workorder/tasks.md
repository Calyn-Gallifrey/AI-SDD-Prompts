# tasks.md - i-need-document-workorder

## 1. Task Plan

| Phase | Goal | Status |
|---|---|---|
| Phase 1 | 生成 SDD2.0 proposal/spec/design/tasks 并完成人工审核 | confirmed |
| Phase 2 | 实现 I need document API、Service、Model、Repository、Downstream Client | completed |
| Phase 3 | 增加 Service、Controller、Repository 单元测试 | completed |
| Phase 4 | 运行 SDD 内部 Code Review、Auto-fix、Unit Test Summary、Archive | completed |

## 2. Implementation Checklist

### Phase 2 - Code Implementation

- [x] 新增 `INeedDocumentRequestType`。
- [x] 新增 `CreateINeedDocumentWorkOrderRequest`。
- [x] 新增 `INeedDocumentWorkOrderResponse`。
- [x] 新增 `INeedDocumentWorkOrder`。
- [x] 新增 `INeedDocumentWorkOrderRepository` 与 in-memory 实现。
- [x] 新增 `INeedDocumentDownstreamClient`、`INeedDocumentWorkOrderSubmission` 与 in-memory 实现。
- [x] 新增 `INeedDocumentWorkOrderService`。
- [x] 新增 `INeedDocumentWorkOrderController`。
- [x] 更新 README API 示例。

### Phase 3 - Unit Test Implementation

- [x] Service 成功和异常测试。
- [x] Controller 成功和 validation 测试。
- [x] Repository 保存和查询测试。

### Phase 4 - SDD Quality Gates

- [x] 生成 `code-review-findings.md`。
- [x] 输出 Auto-fix Summary。
- [x] 生成 Unit Test Summary。
- [x] Archive 前状态同步。

## 3. Files Allowed to Modify

- `uaw-sdd-demo/README.md`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/INeedDocumentWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/CreateINeedDocumentWorkOrderRequest.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/INeedDocumentWorkOrderResponse.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/entity/INeedDocumentWorkOrder.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/enums/INeedDocumentRequestType.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/INeedDocumentWorkOrderRepository.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/repository/InMemoryINeedDocumentWorkOrderRepository.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/client/INeedDocumentDownstreamClient.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/client/INeedDocumentWorkOrderSubmission.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/client/InMemoryINeedDocumentDownstreamClient.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/INeedDocumentWorkOrderService.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/INeedDocumentWorkOrderControllerTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/repository/InMemoryINeedDocumentWorkOrderRepositoryTest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/INeedDocumentWorkOrderServiceTest.java`

## 4. Files Forbidden to Modify

- `skills/**`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyBeneficiaryChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyBeneficiaryChangeWorkOrderService.java`

## 5. Phase Review

| Phase | Reviewer Role | Review Time | Result | Findings | Required Action | Next Phase Allowed |
|---|---|---|---|---|---|---|
| Phase 1 | AI-as-human-reviewer | 2026-06-11 14:38 | 通过 | SDD 过程文件已按顺序生成，brief-design/proposal/spec/design/tasks 均已审核。 | 无 | yes |
| Phase 2 | AI-as-human-reviewer | 2026-06-11 14:40 | 通过 | 新增文件均在允许范围内，未改动现有工单接口。 | 无 | yes |
| Phase 3 | AI-as-human-reviewer | 2026-06-11 14:40 | 通过 | Service、Controller、Repository 测试覆盖成功、validation 和业务异常路径。 | 无 | yes |
| Phase 4 | AI-as-human-reviewer | 2026-06-11 14:43 | 通过 | Code Review 发现 1 个 P2 并完成自动修复；Unit Test Summary 通过；Archive 已完成。 | 无 | yes |

## 6. Human Review

| Review Stage | Reviewer Role | Review Result | Review Comments | Required Fixes | Next Stage Allowed |
|---|---|---|---|---|---|
| tasks | AI-as-human-reviewer | 通过 | 任务拆分、允许修改范围、禁止修改范围和测试目标清晰，可以进入实现。 | 无 | yes |

## 7. Review-driven Auto-fix Summary

Auto-fix Summary：`auto-fix-summary.md`

- Fixed Issues：`CR-P2-001`
- Modified Files：`INeedDocumentWorkOrderService.java`、`INeedDocumentWorkOrderServiceTest.java`
- Test Files Added / Updated：`INeedDocumentWorkOrderServiceTest.java`
- Issues Not Fixed：无
- Remaining Risks：真实下游平台协议、保单归属校验和客户身份校验需真实项目补齐。

## 8. Unit Test Summary

Unit Test Summary：`unit-test-summary.md`

- Entry Mode：SDD_UNIT_TEST
- Actual Test Entry：`mvn test`
- Result：SUCCESS
- Tests run：36
- Failures：0
- Errors：0
- Skipped：0

## Process Status

Current Stage：archive

Stage Status：archived

Last Completed Step：archive completed

Next Required Step：无

Blocked Reason：无

## Process Audit Trail

| Time | Stage | Action | Result | Next Step |
|---|---|---|---|---|
| 2026-06-11 14:38 | tasks | AI generated tasks.md | draft completed | human review |
| 2026-06-11 14:39 | tasks-review | AI-as-human-reviewer reviewed tasks.md | passed | implement Phase 2 |
| 2026-06-11 14:40 | implementation | AI implemented Phase 2 code changes | completed | phase review |
| 2026-06-11 14:40 | unit-test-implementation | AI implemented Phase 3 tests | completed | code review |
| 2026-06-11 14:41 | code-review | SDD_TASK_CODE_REVIEW generated code-review-findings.md | one P2 found | auto-fix |
| 2026-06-11 14:41 | auto-fix | AI fixed CR-P2-001 | completed | unit test |
| 2026-06-11 14:42 | unit-test | mvn test | passed, 36 tests | archive |
| 2026-06-11 14:43 | archive | AI generated archive.md | completed | archived |
