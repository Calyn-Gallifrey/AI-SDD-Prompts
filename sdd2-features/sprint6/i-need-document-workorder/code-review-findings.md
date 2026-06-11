# code-review-findings.md - i-need-document-workorder

## Review Metadata

Entry Mode：SDD_TASK_CODE_REVIEW

Feature Directory：`sdd2-features/sprint6/i-need-document-workorder`

Review Time：2026-06-11 14:41

Reviewer Role：AI code review agent

Review Scope：
- `brief-design.md`
- `proposal-input.md`
- `spec.md`
- `design.md`
- `tasks.md`
- `uaw-sdd-demo` 本次新增 I need document 代码和测试
- 新增未跟踪 Java 文件

## Gate Summary

Code Review Conclusion: 有条件通过

P0 Count: 0

P1 Count: 0

P2 Count: 1

Suggestion Count: 0

Review-driven Auto-fix Required: yes

Fix Scope: 增加 Service 层 requestType 必填校验，并补充对应 Service 单元测试。

Files allowed to modify:
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/INeedDocumentWorkOrderService.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/service/INeedDocumentWorkOrderServiceTest.java`
- `sdd2-features/sprint6/i-need-document-workorder/tasks.md`
- `sdd2-features/sprint6/i-need-document-workorder/auto-fix-summary.md`
- `sdd2-features/sprint6/i-need-document-workorder/unit-test-summary.md`
- `sdd2-features/sprint6/i-need-document-workorder/archive.md`

Files forbidden to modify:
- `skills/**`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyBeneficiaryChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyBeneficiaryChangeWorkOrderService.java`

Unit tests required: yes

Unit test focus:
- Service 直接调用时 `requestType=null` 必须返回 `BadRequestException`。
- 该异常路径不得调用 downstream client，也不得保存 repository。

Untracked files reviewed: yes

Archive allowed: no

## Findings

### CR-P2-001

问题编号：CR-P2-001

严重程度：P2

问题类型：Service Validation Gap

文件路径：`uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/INeedDocumentWorkOrderService.java`

方法 / 类：`INeedDocumentWorkOrderService#create`

Diff 位置：新增 Service 方法

关联 SDD 依据：`spec.md` FR-1 / FR-2 / FR-3；`design.md` 第 4 节 Service Design

问题描述：
`requestType` 是 I need document 工单核心业务字段，DTO 层有 `@NotNull`，但 Service 层没有做直接调用保护。若绕过 Controller 直接调用 `INeedDocumentWorkOrderService#create(...)` 且 `requestType=null`，当前实现会继续构造 downstream submission 和 work order，导致向下游提交请求类型为空的工单。

风险影响：
真实服务中 Service 可能被其他应用层、任务或测试直接调用。缺少 Service 层核心字段校验会导致无效工单进入下游平台，影响下游分类处理和后续审计。

修复建议：
在 Service 层增加 `requestType` 非空校验，异常信息使用 `requestType is required`；补充 Service 单元测试验证不会调用 downstream client 和 repository。

是否阻塞 Archive：yes

## Post Auto-fix Verification

Recheck Time：2026-06-11 14:42

Recheck Result：passed

Rechecked Issues：
- `CR-P2-001` fixed. `INeedDocumentWorkOrderService#create(...)` now validates `requestType` before downstream submission and repository save.

Remaining P0 / P1 / Blocking P2：0

Archive allowed after Auto-fix：yes

Next Gate：Unit Test Summary
