# code-review-findings.md - policy-beneficiary-email-change

## Review Metadata

Entry Mode：SDD_TASK_CODE_REVIEW

Feature Directory：`sdd2-features/sprint6/policy-beneficiary-email-change`

Review Time：2026-06-11 12:46

Review Scope：
- `proposal-input.md`
- `spec.md`
- `design.md`
- `tasks.md`
- `uaw-sdd-demo` 本次受益人邮箱变更相关代码 diff
- 新增未跟踪文件 `CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.java`

## Gate Summary

Code Review Conclusion: 有条件通过

P0 Count: 0

P1 Count: 0

P2 Count: 1

Suggestion Count: 0

Review-driven Auto-fix Required: yes

Fix Scope: 修复邮箱字段在 Controller validation 前未 trim 导致设计约束无法稳定生效的问题，并补充对应 Controller 测试。

Files allowed to modify:
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.java`
- `uaw-sdd-demo/src/test/java/com/example/uawsdddemo/controller/PolicyBeneficiaryChangeWorkOrderControllerTest.java`
- `sdd2-features/sprint6/policy-beneficiary-email-change/tasks.md`
- `sdd2-features/sprint6/policy-beneficiary-email-change/auto-fix-summary.md`
- `sdd2-features/sprint6/policy-beneficiary-email-change/unit-test-summary.md`
- `sdd2-features/sprint6/policy-beneficiary-email-change/archive.md`

Files forbidden to modify:
- `skills/**`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/controller/PolicyInfoChangeWorkOrderController.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/service/PolicyInfoChangeWorkOrderService.java`
- `uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/entity/PolicyInfoChangeWorkOrder.java`

Unit tests required: yes

Unit test focus:
- Controller 接收带前后空格和大小写混合的 beneficiaryEmail 时应能进入 service。
- 邮箱格式错误仍应被 validation 拦截。

Archive allowed: no

## Findings

### CR-P2-001

问题编号：CR-P2-001

严重程度：P2

问题类型：Validation / Normalization Order

文件路径：`uaw-sdd-demo/src/main/java/com/example/uawsdddemo/model/dto/CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.java`

方法 / 类：`CreatePolicyBeneficiaryEmailChangeWorkOrderRequest`

Diff 位置：新增 DTO 的 `beneficiaryEmail` 字段与 setter

关联 SDD 依据：`spec.md` FR-4；`design.md` 第 3 节 Service Design

问题描述：
`beneficiaryEmail` 字段使用 `@Email` 做 Controller validation，但当前 DTO setter 不做 trim。Spring MVC 会在进入 `PolicyBeneficiaryChangeWorkOrderService.createEmailChange(...)` 前执行 validation，因此输入 `"  Bob.Email@Example.COM  "` 这类可通过 service 设计归一化的值会在 Controller 层先失败，导致 design 中“先 trim 再校验并 lower-case”的路径无法稳定覆盖 API 调用场景。

风险影响：
API 层和 Service 层行为不一致。直接调用 Service 可以接受并归一化前后空格邮箱，但 HTTP 请求会被提前判定为 validation failed，和 SDD 设计中邮箱归一化的验收意图不一致。

修复建议：
在 `CreatePolicyBeneficiaryEmailChangeWorkOrderRequest.setBeneficiaryEmail(...)` 中对非 null 输入执行 trim，使 Controller validation 和 Service normalization 顺序一致；补充 Controller 测试覆盖带空格和大小写混合的邮箱输入。

是否阻塞 Archive：yes
