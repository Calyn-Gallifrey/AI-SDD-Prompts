#!/usr/bin/env python3
"""在隔离 Git 仓库中深度预演一个多文件、多返工的大型 SDD2.0 功能。"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from textwrap import dedent
from typing import Any

from demo_sdd2_small_feature import (
    CONTROL,
    DEMO_SOURCE,
    ROOT,
    DemoFailure,
    approve_demo,
    git,
    record,
    run_control,
    run_process,
    write_asset,
)


FEATURE_RELATIVE = Path(
    "sdd2-features/DeepDemoSprint/policy-contact-change-batch-planning"
)
MAIN_PACKAGE = Path(
    "uaw-sdd-demo/src/main/java/com/example/uawsdddemo/batchcontact"
)
TEST_PACKAGE = Path(
    "uaw-sdd-demo/src/test/java/com/example/uawsdddemo/batchcontact"
)
PHASE_MODEL = "Phase1-建立批量变更领域模型"
PHASE_VALIDATION = "Phase2-实现联系方式校验"
PHASE_PLANNING = "Phase3-实现幂等批次计划"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DemoFailure(message)


def result_text(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, sort_keys=True)


def expect_control_failure(
    repo: Path,
    *arguments: str,
    expected: int = 2,
    contains: tuple[str, ...] = (),
) -> dict[str, Any]:
    result = run_control(repo, *arguments, expected=expected)
    rendered = result_text(result)
    if contains and not all(fragment in rendered for fragment in contains):
        raise DemoFailure(
            f"控制器失败内容不符合预期：arguments={arguments!r}, result={rendered}"
        )
    return result


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_source(repo: Path, relative: Path, content: str) -> Path:
    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).lstrip(), encoding="utf-8")
    return path


def phase_review(
    repo: Path,
    feature: Path,
    phase: str,
    message_id: str,
) -> dict[str, Any]:
    return run_control(
        repo,
        "phase-review",
        "--feature-dir",
        str(feature),
        "--phase",
        phase,
        "--source",
        "demo-simulation",
        "--approver-role",
        "ai-as-human-reviewer",
        "--approval-text",
        f"Demo 模拟批准 {phase} 阶段",
        "--message-id",
        message_id,
    )


def resume_action(repo: Path, feature: Path) -> str:
    return run_control(
        repo,
        "resume",
        "--feature-dir",
        str(feature),
    )["result"]["next_required_action"]


def git_path(repo: Path, name: str) -> Path:
    value = Path(git(repo, "rev-parse", "--git-path", name))
    return value if value.is_absolute() else repo / value


def request_source() -> str:
    return """
        package com.example.uawsdddemo.batchcontact;

        public final class PolicyContactChangeRequest {
            private final String requestId;
            private final String policyNo;
            private final String email;
            private final String mobile;

            public PolicyContactChangeRequest(
                    String requestId,
                    String policyNo,
                    String email,
                    String mobile) {
                this.requestId = requestId;
                this.policyNo = policyNo;
                this.email = email;
                this.mobile = mobile;
            }

            public String getRequestId() {
                return requestId;
            }

            public String getPolicyNo() {
                return policyNo;
            }

            public String getEmail() {
                return email;
            }

            public String getMobile() {
                return mobile;
            }
        }
    """


def validation_issue_source() -> str:
    return """
        package com.example.uawsdddemo.batchcontact;

        public final class ValidationIssue {
            private final String code;
            private final String field;
            private final String message;

            public ValidationIssue(String code, String field, String message) {
                this.code = code;
                this.field = field;
                this.message = message;
            }

            public String getCode() {
                return code;
            }

            public String getField() {
                return field;
            }

            public String getMessage() {
                return message;
            }
        }
    """


def rejection_source() -> str:
    return """
        package com.example.uawsdddemo.batchcontact;

        import java.util.ArrayList;
        import java.util.Collections;
        import java.util.List;

        public final class ContactChangeRejection {
            private final String requestId;
            private final List<ValidationIssue> issues;

            public ContactChangeRejection(
                    String requestId,
                    List<ValidationIssue> issues) {
                this.requestId = requestId;
                this.issues = Collections.unmodifiableList(
                    new ArrayList<ValidationIssue>(issues)
                );
            }

            public String getRequestId() {
                return requestId;
            }

            public List<ValidationIssue> getIssues() {
                return issues;
            }
        }
    """


def validator_source(*, fixed_blank_email: bool) -> str:
    email_condition = "!email.isEmpty()" if fixed_blank_email else (
        "request.getEmail() != null"
    )
    return f"""
        package com.example.uawsdddemo.batchcontact;

        import java.util.ArrayList;
        import java.util.Collections;
        import java.util.List;
        import java.util.regex.Pattern;

        public final class PolicyContactChangeValidator {{
            private static final Pattern EMAIL = Pattern.compile(
                "^[^@\\\\s]+@[^@\\\\s]+\\\\.[^@\\\\s]+$"
            );
            private static final Pattern MOBILE = Pattern.compile("^\\\\d{{8,15}}$");

            public List<ValidationIssue> validate(PolicyContactChangeRequest request) {{
                if (request == null) {{
                    return Collections.singletonList(
                        new ValidationIssue(
                            "REQUEST_REQUIRED",
                            "request",
                            "request must not be null"
                        )
                    );
                }}
                List<ValidationIssue> issues = new ArrayList<ValidationIssue>();
                String requestId = trim(request.getRequestId());
                String policyNo = trim(request.getPolicyNo());
                String email = trim(request.getEmail());
                String mobile = trim(request.getMobile());

                if (requestId.isEmpty()) {{
                    issues.add(new ValidationIssue(
                        "REQUEST_ID_REQUIRED",
                        "requestId",
                        "requestId must not be blank"
                    ));
                }}
                if (policyNo.isEmpty()) {{
                    issues.add(new ValidationIssue(
                        "POLICY_NO_REQUIRED",
                        "policyNo",
                        "policyNo must not be blank"
                    ));
                }}
                if (email.isEmpty() && mobile.isEmpty()) {{
                    issues.add(new ValidationIssue(
                        "CONTACT_REQUIRED",
                        "contact",
                        "email or mobile is required"
                    ));
                }}
                if ({email_condition} && !EMAIL.matcher(email).matches()) {{
                    issues.add(new ValidationIssue(
                        "EMAIL_INVALID",
                        "email",
                        "email format is invalid"
                    ));
                }}
                if (!mobile.isEmpty() && !MOBILE.matcher(mobile).matches()) {{
                    issues.add(new ValidationIssue(
                        "MOBILE_INVALID",
                        "mobile",
                        "mobile format is invalid"
                    ));
                }}
                return Collections.unmodifiableList(issues);
            }}

            private static String trim(String value) {{
                return value == null ? "" : value.trim();
            }}
        }}
    """


def batch_plan_source() -> str:
    return """
        package com.example.uawsdddemo.batchcontact;

        import java.util.ArrayList;
        import java.util.Collections;
        import java.util.List;

        public final class PolicyContactChangeBatchPlan {
            private final List<PolicyContactChangeRequest> accepted;
            private final List<ContactChangeRejection> rejected;
            private final int duplicateCount;

            public PolicyContactChangeBatchPlan(
                    List<PolicyContactChangeRequest> accepted,
                    List<ContactChangeRejection> rejected,
                    int duplicateCount) {
                this.accepted = Collections.unmodifiableList(
                    new ArrayList<PolicyContactChangeRequest>(accepted)
                );
                this.rejected = Collections.unmodifiableList(
                    new ArrayList<ContactChangeRejection>(rejected)
                );
                this.duplicateCount = duplicateCount;
            }

            public List<PolicyContactChangeRequest> getAccepted() {
                return accepted;
            }

            public List<ContactChangeRejection> getRejected() {
                return rejected;
            }

            public int getDuplicateCount() {
                return duplicateCount;
            }
        }
    """


def planner_source(*, fixed_conflict: bool) -> str:
    if fixed_conflict:
        duplicate_handling = """
                PolicyContactChangeRequest existing = seen.get(request.getRequestId());
                if (existing != null) {
                    if (samePayload(existing, request)) {
                        duplicateCount++;
                    } else {
                        List<ValidationIssue> conflict =
                            new ArrayList<ValidationIssue>();
                        conflict.add(new ValidationIssue(
                            "DUPLICATE_CONFLICT",
                            "requestId",
                            "same requestId carries a different payload"
                        ));
                        rejected.add(new ContactChangeRejection(
                            request.getRequestId(),
                            conflict
                        ));
                    }
                    continue;
                }
        """
        helper = """
            private static boolean samePayload(
                    PolicyContactChangeRequest first,
                    PolicyContactChangeRequest second) {
                return normalized(first.getPolicyNo()).equals(
                        normalized(second.getPolicyNo()))
                    && normalized(first.getEmail()).equals(
                        normalized(second.getEmail()))
                    && normalized(first.getMobile()).equals(
                        normalized(second.getMobile()));
            }

            private static String normalized(String value) {
                return value == null ? "" : value.trim();
            }
        """
    else:
        duplicate_handling = """
                PolicyContactChangeRequest existing = seen.get(request.getRequestId());
                if (existing != null) {
                    duplicateCount++;
                    continue;
                }
        """
        helper = ""
    return f"""
        package com.example.uawsdddemo.batchcontact;

        import java.util.ArrayList;
        import java.util.LinkedHashMap;
        import java.util.List;
        import java.util.Map;
        import java.util.Objects;

        public final class PolicyContactChangeBatchPlanner {{
            private static final int MAX_BATCH_SIZE = 100;
            private final PolicyContactChangeValidator validator;

            public PolicyContactChangeBatchPlanner(
                    PolicyContactChangeValidator validator) {{
                this.validator = Objects.requireNonNull(validator, "validator");
            }}

            public PolicyContactChangeBatchPlan plan(
                    List<PolicyContactChangeRequest> requests) {{
                Objects.requireNonNull(requests, "requests");
                if (requests.size() > MAX_BATCH_SIZE) {{
                    throw new IllegalArgumentException(
                        "batch size must not exceed " + MAX_BATCH_SIZE
                    );
                }}

                List<PolicyContactChangeRequest> accepted =
                    new ArrayList<PolicyContactChangeRequest>();
                List<ContactChangeRejection> rejected =
                    new ArrayList<ContactChangeRejection>();
                Map<String, PolicyContactChangeRequest> seen =
                    new LinkedHashMap<String, PolicyContactChangeRequest>();
                int duplicateCount = 0;

                for (PolicyContactChangeRequest request : requests) {{
                    List<ValidationIssue> issues = validator.validate(request);
                    if (!issues.isEmpty()) {{
                        rejected.add(new ContactChangeRejection(
                            request == null ? null : request.getRequestId(),
                            issues
                        ));
                        continue;
                    }}
                    {dedent(duplicate_handling).strip()}
                    seen.put(request.getRequestId(), request);
                    accepted.add(request);
                }}
                return new PolicyContactChangeBatchPlan(
                    accepted,
                    rejected,
                    duplicateCount
                );
            }}

            {dedent(helper).strip()}
        }}
    """


def validator_test_source() -> str:
    return """
        package com.example.uawsdddemo.batchcontact;

        import org.junit.jupiter.api.Test;

        import java.util.ArrayList;
        import java.util.List;

        import static org.junit.jupiter.api.Assertions.assertEquals;
        import static org.junit.jupiter.api.Assertions.assertTrue;

        class PolicyContactChangeValidatorTest {
            private final PolicyContactChangeValidator validator =
                new PolicyContactChangeValidator();

            @Test
            void acceptsValidEmailAndMobile() {
                PolicyContactChangeRequest request = request(
                    "REQ-1",
                    "POL-1",
                    "customer@example.com",
                    "91234567"
                );
                assertTrue(validator.validate(request).isEmpty());
            }

            @Test
            void rejectsMissingRequest() {
                assertEquals(
                    "REQUEST_REQUIRED",
                    validator.validate(null).get(0).getCode()
                );
            }

            @Test
            void reportsMissingRequiredIdentityFields() {
                List<String> codes = codes(validator.validate(
                    request(" ", "", "customer@example.com", null)
                ));
                assertTrue(codes.contains("REQUEST_ID_REQUIRED"));
                assertTrue(codes.contains("POLICY_NO_REQUIRED"));
            }

            @Test
            void requiresAtLeastOneContactChannel() {
                List<String> codes = codes(validator.validate(
                    request("REQ-2", "POL-2", null, " ")
                ));
                assertTrue(codes.contains("CONTACT_REQUIRED"));
            }

            @Test
            void rejectsMalformedEmail() {
                List<String> codes = codes(validator.validate(
                    request("REQ-3", "POL-3", "invalid-email", null)
                ));
                assertTrue(codes.contains("EMAIL_INVALID"));
            }

            @Test
            void rejectsMalformedMobile() {
                List<String> codes = codes(validator.validate(
                    request("REQ-4", "POL-4", null, "12AB")
                ));
                assertTrue(codes.contains("MOBILE_INVALID"));
            }

            @Test
            void acceptsBlankEmailWhenValidMobileProvided() {
                PolicyContactChangeRequest request = request(
                    "REQ-5",
                    "POL-5",
                    "   ",
                    "91234567"
                );
                assertTrue(validator.validate(request).isEmpty());
            }

            private static PolicyContactChangeRequest request(
                    String requestId,
                    String policyNo,
                    String email,
                    String mobile) {
                return new PolicyContactChangeRequest(
                    requestId,
                    policyNo,
                    email,
                    mobile
                );
            }

            private static List<String> codes(List<ValidationIssue> issues) {
                List<String> result = new ArrayList<String>();
                for (ValidationIssue issue : issues) {
                    result.add(issue.getCode());
                }
                return result;
            }
        }
    """


def planner_test_source() -> str:
    return """
        package com.example.uawsdddemo.batchcontact;

        import org.junit.jupiter.api.Test;

        import java.util.ArrayList;
        import java.util.Arrays;
        import java.util.Collections;
        import java.util.List;

        import static org.junit.jupiter.api.Assertions.assertEquals;
        import static org.junit.jupiter.api.Assertions.assertThrows;

        class PolicyContactChangeBatchPlannerTest {
            private final PolicyContactChangeBatchPlanner planner =
                new PolicyContactChangeBatchPlanner(
                    new PolicyContactChangeValidator()
                );

            @Test
            void keepsAcceptedOrder() {
                PolicyContactChangeBatchPlan plan = planner.plan(Arrays.asList(
                    request("REQ-1", "POL-1", "one@example.com", null),
                    request("REQ-2", "POL-2", null, "91234567")
                ));
                assertEquals("REQ-1", plan.getAccepted().get(0).getRequestId());
                assertEquals("REQ-2", plan.getAccepted().get(1).getRequestId());
            }

            @Test
            void countsIdenticalDuplicate() {
                PolicyContactChangeRequest first =
                    request("REQ-3", "POL-3", "same@example.com", null);
                PolicyContactChangeRequest duplicate =
                    request("REQ-3", "POL-3", " same@example.com ", null);
                PolicyContactChangeBatchPlan plan = planner.plan(
                    Arrays.asList(first, duplicate)
                );
                assertEquals(1, plan.getAccepted().size());
                assertEquals(1, plan.getDuplicateCount());
                assertEquals(0, plan.getRejected().size());
            }

            @Test
            void rejectsConflictingDuplicateRequestId() {
                PolicyContactChangeBatchPlan plan = planner.plan(Arrays.asList(
                    request("REQ-4", "POL-4", "first@example.com", null),
                    request("REQ-4", "POL-4", "second@example.com", null)
                ));
                assertEquals(1, plan.getAccepted().size());
                assertEquals(1, plan.getRejected().size());
                assertEquals(
                    "DUPLICATE_CONFLICT",
                    plan.getRejected().get(0).getIssues().get(0).getCode()
                );
            }

            @Test
            void separatesInvalidRequests() {
                PolicyContactChangeBatchPlan plan = planner.plan(Arrays.asList(
                    request("REQ-5", "POL-5", "bad-email", null),
                    request("REQ-6", "POL-6", "valid@example.com", null)
                ));
                assertEquals(1, plan.getAccepted().size());
                assertEquals(1, plan.getRejected().size());
                assertEquals("REQ-5", plan.getRejected().get(0).getRequestId());
            }

            @Test
            void rejectsBatchAboveLimit() {
                List<PolicyContactChangeRequest> requests =
                    new ArrayList<PolicyContactChangeRequest>();
                for (int index = 0; index < 101; index++) {
                    requests.add(request(
                        "REQ-" + index,
                        "POL-" + index,
                        "customer" + index + "@example.com",
                        null
                    ));
                }
                assertThrows(
                    IllegalArgumentException.class,
                    () -> planner.plan(requests)
                );
            }

            @Test
            void returnsImmutableCollections() {
                PolicyContactChangeBatchPlan plan = planner.plan(
                    Collections.singletonList(
                        request("REQ-7", "POL-7", null, "91234567")
                    )
                );
                assertThrows(
                    UnsupportedOperationException.class,
                    () -> plan.getAccepted().clear()
                );
                assertThrows(
                    UnsupportedOperationException.class,
                    () -> plan.getRejected().clear()
                );
            }

            @Test
            void handlesMixedBatchDeterministically() {
                PolicyContactChangeRequest acceptedEmail =
                    request("REQ-8", "POL-8", "mix@example.com", null);
                PolicyContactChangeRequest identicalDuplicate =
                    request("REQ-8", "POL-8", "mix@example.com", null);
                PolicyContactChangeRequest invalid =
                    request("REQ-9", "POL-9", "invalid", null);
                PolicyContactChangeRequest acceptedMobile =
                    request("REQ-10", "POL-10", null, "91234567");
                PolicyContactChangeRequest conflictingDuplicate =
                    request("REQ-10", "POL-10", null, "99887766");

                PolicyContactChangeBatchPlan plan = planner.plan(Arrays.asList(
                    acceptedEmail,
                    identicalDuplicate,
                    invalid,
                    acceptedMobile,
                    conflictingDuplicate
                ));

                assertEquals(2, plan.getAccepted().size());
                assertEquals(2, plan.getRejected().size());
                assertEquals(1, plan.getDuplicateCount());
            }

            private static PolicyContactChangeRequest request(
                    String requestId,
                    String policyNo,
                    String email,
                    String mobile) {
                return new PolicyContactChangeRequest(
                    requestId,
                    policyNo,
                    email,
                    mobile
                );
            }
        }
    """


def write_model_phase(repo: Path) -> list[Path]:
    return [
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactChangeRequest.java",
            request_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "ValidationIssue.java",
            validation_issue_source(),
        ),
    ]


def write_validation_phase(repo: Path) -> list[Path]:
    return [
        write_source(
            repo,
            MAIN_PACKAGE / "ContactChangeRejection.java",
            rejection_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactChangeValidator.java",
            validator_source(fixed_blank_email=False),
        ),
    ]


def write_planning_phase(repo: Path) -> list[Path]:
    return [
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactChangeBatchPlan.java",
            batch_plan_source(),
        ),
        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactChangeBatchPlanner.java",
            planner_source(fixed_conflict=False),
        ),
    ]


def write_test_phase(repo: Path) -> list[Path]:
    return [
        write_source(
            repo,
            TEST_PACKAGE / "PolicyContactChangeValidatorTest.java",
            validator_test_source(),
        ),
        write_source(
            repo,
            TEST_PACKAGE / "PolicyContactChangeBatchPlannerTest.java",
            planner_test_source(),
        ),
    ]


def run_feature_tests(repo: Path, feature: Path) -> dict[str, Any]:
    return run_control(
        repo,
        "run-unit-test",
        "--feature-dir",
        str(feature),
        "--cwd",
        ".",
        "--timeout-seconds",
        "600",
        "--",
        "mvn",
        "-f",
        "uaw-sdd-demo/pom.xml",
        "-Dtest=PolicyContactChangeValidatorTest,PolicyContactChangeBatchPlannerTest",
        "test",
    )["result"]


def write_unit_summary(
    feature: Path,
    execution: dict[str, Any],
    *,
    conclusion: str,
) -> None:
    counts = execution["test_counts"]
    write_asset(
        feature,
        "unit-test-summary.md",
        "单元测试总结",
        (
            f"控制器执行证据 SHA-256：`{execution['evidence_sha256']}`。\n\n"
            f"冻结范围 SHA-256：`{execution['scope_sha256']}`。\n\n"
            f"实际执行 {counts['total']} 项测试，通过 {counts['passed']} 项，"
            f"失败 {counts['failed']} 项，Error {counts['errors']} 项。"
            f"结论：{conclusion}。"
        ),
    )


def main() -> int:
    if shutil.which("java") is None:
        raise DemoFailure(
            "当前环境未检测到 Java。请安装或启用 Java 8 及以上版本，"
            "并正确配置 PATH/JAVA_HOME。"
        )
    if not CONTROL.is_file():
        raise DemoFailure(f"缺少 Java 8 控制器 JAR：{CONTROL}")
    doctor = run_control(
        ROOT,
        "doctor",
        "--repo-root",
        str(ROOT),
    )["result"]
    if doctor["java_specification_version"] != "1.8":
        raise DemoFailure(
            "大型环境验收必须由真实 Java 8 运行；"
            f"当前版本为 {doctor['java_specification_version']}。"
        )
    if shutil.which("mvn") is None:
        raise DemoFailure("当前环境未安装 Maven，无法执行真实 Java 测试。")

    checks: list[dict[str, Any]] = [
        {
            "检查": "Java 8 实机预检",
            "结果": "已通过",
            "版本": doctor["java_specification_version"],
        }
    ]

    with tempfile.TemporaryDirectory(prefix="uaw-sdd2-large-demo-") as temp:
        workspace = Path(temp)
        repo = workspace / "main"
        parallel_repo = workspace / "parallel"
        remote = workspace / "remote.git"
        shutil.copytree(DEMO_SOURCE, repo / "uaw-sdd-demo")
        git(repo, "init", "-q")
        git(repo, "config", "user.email", "sdd2-large-demo@example.invalid")
        git(repo, "config", "user.name", "SDD2 Large Demo")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "large demo baseline")
        baseline_commit_count = int(git(repo, "rev-list", "--count", "HEAD"))
        run_process(
            ["git", "init", "--bare", "-q", str(remote)],
            cwd=workspace,
        )
        git(repo, "remote", "add", "origin", str(remote))
        git(
            repo,
            "worktree",
            "add",
            "-q",
            "-b",
            "large-demo-parallel",
            str(parallel_repo),
            "HEAD",
        )

        feature = repo / FEATURE_RELATIVE
        feature.mkdir(parents=True)
        write_asset(
            feature,
            "brief-design.md",
            "人工简要设计",
            (
                "新增批量保单联系方式变更预检与幂等计划能力。"
                "输入包含请求号、保单号、邮箱和手机号；系统需要校验字段、"
                "保持有效请求顺序、识别相同重复请求并拒绝同请求号冲突载荷。"
                "单批最多一百条。变更只能新增独立 batchcontact 包及对应测试，"
                "不得修改现有接口、构建文件、依赖或其他业务模块。"
            ),
        )
        initial = run_control(
            repo,
            "init",
            "--feature-dir",
            str(feature),
            "--feature-id",
            "policy-contact-change-batch-planning",
            "--mode",
            "demo",
        )["result"]
        require(
            initial["next_required_action"] == "assemble-proposal-input",
            "初始化后没有停在 Proposal 输入动作。",
        )

        expect_control_failure(
            repo,
            "resume",
            "--feature-dir",
            str(feature),
            "--unexpected",
            contains=("Unknown argument",),
        )
        checks.append({"检查": "未知控制参数", "结果": "已拒绝且状态未前进"})

        parallel_feature = (
            parallel_repo
            / "sdd2-features/DeepDemoSprint/parallel-worktree-smoke"
        )
        parallel_feature.mkdir(parents=True)
        write_asset(
            parallel_feature,
            "brief-design.md",
            "并行工作树验证",
            "在独立 Git worktree 中启动第二个受控功能，用于验证隔离锁不会串线。",
        )
        parallel_state = run_control(
            parallel_repo,
            "init",
            "--feature-dir",
            str(parallel_feature),
            "--feature-id",
            "parallel-worktree-smoke",
            "--mode",
            "demo",
        )["result"]
        require(
            parallel_state["next_required_action"] == "assemble-proposal-input",
            "独立 worktree 没有获得自己的流程状态。",
        )
        require(
            resume_action(repo, feature) == "assemble-proposal-input",
            "并行 worktree 影响了主 Feature 的下一动作。",
        )
        run_control(
            parallel_repo,
            "close",
            "--feature-dir",
            str(parallel_feature),
            "--result",
            "aborted",
            "--approval-text",
            "用户同意终止并关闭并行 worktree 验证功能",
            "--message-id",
            "large-parallel-close",
        )
        require(
            not git_path(
                parallel_repo,
                "sdd2-active-feature.json",
            ).exists(),
            "关闭并行 Feature 后锁没有释放。",
        )
        checks.append({"检查": "不同 worktree 并行隔离", "结果": "状态与锁均独立"})

        sibling = (
            repo
            / "sdd2-features/DeepDemoSprint/uncontrolled-sibling"
        )
        sibling.mkdir(parents=True)
        write_asset(
            sibling,
            "brief-design.md",
            "错误兄弟功能",
            "该目录用于验证同一 worktree 不能串入第二个未受控 Feature。",
        )
        sibling_block = expect_control_failure(
            repo,
            "resume",
            "--feature-dir",
            str(feature),
            expected=1,
            contains=("UNCONTROLLED_SIBLING_FEATURE",),
        )
        require(
            not sibling_block["result"]["valid"],
            "兄弟 Feature 攻击没有让恢复校验失败。",
        )
        shutil.rmtree(sibling)
        require(
            resume_action(repo, feature) == "assemble-proposal-input",
            "移走兄弟 Feature 后没有恢复原 Proposal 动作。",
        )
        checks.append({"检查": "同一 worktree 串 Feature", "结果": "已阻断并恢复"})

        blocked_commit = subprocess.run(
            [
                "git",
                "commit",
                "--allow-empty",
                "--no-verify",
                "-m",
                "forbidden large demo commit",
            ],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(
            blocked_commit.returncode != 0
            and "SDD2_COMMIT_BLOCKED"
            in blocked_commit.stdout + blocked_commit.stderr,
            "活动 Feature 没有阻止 git commit --no-verify。",
        )
        blocked_push = subprocess.run(
            ["git", "push", "origin", "HEAD:refs/heads/main"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(
            blocked_push.returncode != 0
            and "SDD2_COMMIT_BLOCKED"
            in blocked_push.stdout + blocked_push.stderr,
            "活动 Feature 没有阻止 git push。",
        )
        checks.append({"检查": "活动流程提交与推送", "结果": "双重 Git Guard 已阻断"})

        write_asset(
            feature,
            "proposal-input.md",
            "内部规划输入",
            (
                "该功能新增独立 Java 8 包，不修改既有接口。"
                "已确认输入字段、幂等键、顺序、冲突拒绝和最大批次边界；"
                "测试必须覆盖有效、无效、重复、冲突、混合批次及不可变返回。"
            ),
        )
        record(repo, feature, "proposal-input")
        write_asset(
            feature,
            "spec.md",
            "需求规格第一版",
            (
                "校验请求号、保单号以及邮箱或手机号；有效请求保持输入顺序。"
                "同请求号只处理一次，非法请求进入拒绝列表。"
                "验收要求通过真实 Java 单元测试并且不修改现有业务文件。"
            ),
        )
        record(repo, feature, "spec")

        expect_control_failure(
            repo,
            "approve",
            "--feature-dir",
            str(feature),
            "--stage",
            "spec",
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            "Demo 模拟批准当前 spec 阶段",
            "--message-id",
            "large-before-demo-authorization",
            contains=("demo authorization",),
        )
        run_control(
            repo,
            "authorize-demo",
            "--feature-dir",
            str(feature),
            "--authorization-text",
            "用户明确授权运行本次大型完整 Demo，并模拟各阶段人工审核。",
            "--message-id",
            "current-user-large-demo-request",
        )
        expect_control_failure(
            repo,
            "approve",
            "--feature-dir",
            str(feature),
            "--stage",
            "spec",
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            "ok",
            "--message-id",
            "large-ambiguous-spec",
            contains=("ambiguous",),
        )
        checks.append({"检查": "未授权模拟与模糊批准", "结果": "均已拒绝"})

        write_asset(
            feature,
            "design.md",
            "错误提前设计",
            "该资产用于验证等待 Spec 批准时禁止提前生成下游设计。",
        )
        (feature / "analysis-notes").mkdir()
        (feature / "analysis-notes/guess.md").write_text(
            "弱模型自行生成的候选分析文件。\n",
            encoding="utf-8",
        )
        layout = expect_control_failure(
            repo,
            "resume",
            "--feature-dir",
            str(feature),
            expected=1,
            contains=(
                "UNEXPECTED_STAGE_ASSET:design.md",
                "UNEXPECTED_FEATURE_DIRECTORY:analysis-notes",
            ),
        )
        require(
            layout["result"]["next_required_action"]
            == "remove-unexpected-feature-paths-before-current-action",
            "布局错误没有进入唯一恢复动作。",
        )
        (feature / "design.md").unlink()
        shutil.rmtree(feature / "analysis-notes")
        require(
            resume_action(repo, feature) == "request-spec-approval",
            "清理违规路径后没有恢复 Spec Gate。",
        )
        checks.append({"检查": "提前资产与额外目录", "结果": "已阻断并恢复原 Gate"})

        git(repo, "checkout", "-qb", "unauthorized-branch-change")
        branch_drift = expect_control_failure(
            repo,
            "resume",
            "--feature-dir",
            str(feature),
            expected=1,
            contains=("PRE_IMPLEMENTATION_BRANCH_CHANGE",),
        )
        require(
            branch_drift["result"]["stage_status"] == "blocked",
            "分支漂移没有进入 blocked。",
        )
        git(repo, "checkout", "-q", "main")
        require(
            resume_action(repo, feature) == "request-spec-approval",
            "恢复原分支后没有返回 Spec Gate。",
        )
        checks.append({"检查": "规划期分支漂移", "结果": "已阻断并恢复"})

        approve_demo(repo, feature, "spec", "large-spec-v1")
        write_asset(
            feature,
            "design.md",
            "技术设计第一版",
            (
                "使用不可变请求、校验问题、拒绝项、批次计划、校验器和计划器六个类。"
                "使用 LinkedHashMap 保持顺序，使用请求号做幂等去重，"
                "全部实现兼容 Java 8 且不新增依赖。"
            ),
        )
        record(repo, feature, "design")
        approve_demo(repo, feature, "design", "large-design-v1")
        write_asset(
            feature,
            "tasks.md",
            "实现任务第一版",
            (
                "Phase1 建立领域模型；Phase2 实现校验；"
                "Phase3 实现批次计划；Phase4 编写完整测试。"
                "每个 Phase 完成后必须独立审核，全部批准后才能冻结范围。"
            ),
        )
        record(repo, feature, "tasks")
        approve_demo(repo, feature, "tasks", "large-tasks-v1")

        expect_control_failure(
            repo,
            "capture-scope",
            "--feature-dir",
            str(feature),
            "--allowed-path",
            "**",
            "--required-phase",
            PHASE_MODEL,
            "--test-path",
            "uaw-sdd-demo/src/test/**",
            contains=("Unsafe or overly broad scope pattern",),
        )
        checks.append({"检查": "过宽实现范围", "结果": "已拒绝"})

        write_asset(
            feature,
            "spec.md",
            "需求规格第二版",
            (
                "校验请求号、保单号以及邮箱或手机号；空邮箱在有效手机号存在时允许。"
                "有效请求保持输入顺序；完全相同的请求号与载荷计为重复，"
                "同请求号不同载荷必须进入冲突拒绝列表。单批最多一百条。"
                "验收覆盖有效、无效、重复、冲突、混合批次和不可变返回。"
            ),
        )
        spec_revision = record(repo, feature, "spec")["result"]
        require(
            spec_revision["artifacts"]["spec"]["revision"] == 2,
            "Spec 修订号没有增加到 2。",
        )
        revised_state = read_json(feature / ".sdd2/feature-state.json")
        for stage in ("spec", "design", "tasks"):
            require(
                revised_state["approvals"][stage]["status"] == "invalidated",
                f"需求修订后 {stage} 批准没有失效。",
            )
        expect_control_failure(
            repo,
            "capture-scope",
            "--feature-dir",
            str(feature),
            "--allowed-path",
            "uaw-sdd-demo/src/main/java/**",
            "--required-phase",
            PHASE_MODEL,
            contains=("only allowed immediately",),
        )
        approve_demo(repo, feature, "spec", "large-spec-v2")
        write_asset(
            feature,
            "design.md",
            "技术设计第二版",
            (
                "六个 Java 8 类继续保持不可变边界。校验器先标准化可选联系方式，"
                "计划器以 LinkedHashMap 保存首个有效请求；相同载荷计数，"
                "冲突载荷生成 DUPLICATE_CONFLICT。批次入口强制最多一百条。"
            ),
        )
        design_revision = record(repo, feature, "design")["result"]
        require(
            design_revision["artifacts"]["design"]["revision"] == 2,
            "Design 修订号没有增加到 2。",
        )
        expect_control_failure(
            repo,
            "approve",
            "--feature-dir",
            str(feature),
            "--stage",
            "design",
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            "Demo 模拟批准当前 design 阶段",
            "--message-id",
            "large-spec-v2",
            contains=("already been used",),
        )
        approve_demo(repo, feature, "design", "large-design-v2")
        write_asset(
            feature,
            "tasks.md",
            "实现任务第二版",
            (
                f"{PHASE_MODEL}；{PHASE_VALIDATION}；{PHASE_PLANNING}；"
                "每个阶段只修改声明范围内生产文件，"
                "每项 Phase Review 绑定当前 Tasks 第二版。"
                "生产实现完成并关闭首次 Code Review 与 Auto-fix 后，"
                "再由 Unit Test Skill 第一轮生成测试源码，重新冻结并完整复审。"
            ),
        )
        tasks_revision = record(repo, feature, "tasks")["result"]
        require(
            tasks_revision["artifacts"]["tasks"]["revision"] == 2,
            "Tasks 修订号没有增加到 2。",
        )
        approve_demo(repo, feature, "tasks", "large-tasks-v2")
        checks.append(
            {
                "检查": "需求修订与下游失效",
                "结果": "Spec/Design/Tasks 已全部重审",
            }
        )

        scope = run_control(
            repo,
            "capture-scope",
            "--feature-dir",
            str(feature),
            "--allowed-path",
            f"{MAIN_PACKAGE.as_posix()}/**",
            "--allowed-path",
            f"{TEST_PACKAGE.as_posix()}/**",
            "--forbidden-path",
            "uaw-sdd-demo/pom.xml",
            "--forbidden-path",
            "uaw-sdd-demo/README.md",
            "--required-phase",
            PHASE_MODEL,
            "--required-phase",
            PHASE_VALIDATION,
            "--required-phase",
            PHASE_PLANNING,
            "--test-path",
            f"{TEST_PACKAGE.as_posix()}/**",
        )["result"]
        require(
            bool(scope.get("implementation_permit_sha256")),
            "实现范围没有签发哈希绑定许可。",
        )
        permitted_state = read_json(feature / ".sdd2/feature-state.json")
        for stage in ("spec", "design", "tasks"):
            require(
                permitted_state["implementation_permit"]["approved_artifacts"][
                    stage
                ]["revision"]
                == 2,
                f"实现许可没有绑定 {stage} 第二版。",
            )

        scope_path = feature / ".sdd2/implementation-scope.json"
        original_scope = scope_path.read_text(encoding="utf-8")
        tampered_scope = json.loads(original_scope)
        tampered_scope["implementation_permit_sha256"] = "0" * 64
        scope_path.write_text(
            json.dumps(tampered_scope, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        expect_control_failure(
            repo,
            "phase-review",
            "--feature-dir",
            str(feature),
            "--phase",
            PHASE_MODEL,
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            f"Demo 模拟批准 {PHASE_MODEL} 阶段",
            "--message-id",
            "large-tampered-permit",
            contains=("IMPLEMENTATION_PERMIT",),
        )
        scope_path.write_text(original_scope, encoding="utf-8")
        checks.append({"检查": "实现许可篡改", "结果": "已阻断"})

        expect_control_failure(
            repo,
            "phase-review",
            "--feature-dir",
            str(feature),
            "--phase",
            PHASE_VALIDATION,
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            f"Demo 模拟批准 {PHASE_VALIDATION} 阶段",
            "--message-id",
            "large-phase-order-attack",
            contains=("order violation",),
        )

        production_files = write_model_phase(repo)
        phase_review(repo, feature, PHASE_MODEL, "large-phase-model")
        production_files.extend(write_validation_phase(repo))
        expect_control_failure(
            repo,
            "phase-review",
            "--feature-dir",
            str(feature),
            "--phase",
            PHASE_VALIDATION,
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            f"Demo 模拟批准 {PHASE_VALIDATION} 阶段",
            "--message-id",
            "large-phase-model",
            contains=("already been used",),
        )
        phase_review(
            repo,
            feature,
            PHASE_VALIDATION,
            "large-phase-validation",
        )
        production_files.extend(write_planning_phase(repo))
        phase_review(
            repo,
            feature,
            PHASE_PLANNING,
            "large-phase-planning",
        )
        checks.append(
            {
                "检查": "三阶段顺序与批准消息防重放",
                "结果": "顺序错误及消息复用均已拒绝",
            }
        )

        readme = repo / "uaw-sdd-demo/README.md"
        original_readme = readme.read_text(encoding="utf-8")
        readme.write_text(
            original_readme + "\n大型 Demo 错误范围外修改。\n",
            encoding="utf-8",
        )
        expect_control_failure(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
            contains=("FORBIDDEN_PATH:uaw-sdd-demo/README.md",),
        )
        blocked_state = read_json(feature / ".sdd2/feature-state.json")
        require(
            blocked_state["blocked"]["code"] == "IMPLEMENTATION_SCOPE_VIOLATION",
            "范围外修改没有记录确定性阻塞码。",
        )
        readme.write_text(original_readme, encoding="utf-8")
        first_snapshot = run_control(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
        )["result"]
        require(
            first_snapshot["code_revision"] == 1,
            "恢复范围后首次冻结修订不是 1。",
        )
        checks.append({"检查": "范围外文件修改", "结果": "已阻断、记录并恢复"})

        write_asset(
            feature,
            "code-review-findings.md",
            "代码评审发现第一版",
            (
                "P1：计划器把同请求号不同载荷错误计为普通重复，"
                "会静默丢弃冲突变更。必须区分完全相同载荷与冲突载荷，"
                "后者写入 DUPLICATE_CONFLICT 拒绝项。其余范围未发现阻断问题。"
            ),
        )
        record(repo, feature, "code-review-findings")
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "code-review",
            "--result",
            "failed",
            "--evidence",
            "逐文件复核冻结快照，定位到冲突请求被静默去重的可复现缺陷。",
        )
        write_asset(
            feature,
            "auto-fix-summary.md",
            "自动修复总结第一版",
            "首次评审问题尚未修复，当前总结不得关闭 Auto-fix Gate。",
        )
        record(repo, feature, "auto-fix-summary")
        expect_control_failure(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "auto-fix",
            "--result",
            "passed",
            "--evidence",
            "错误声称已经修复。",
            contains=("requires Code Review passed",),
        )

        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactChangeBatchPlanner.java",
            planner_source(fixed_conflict=True),
        )
        second_snapshot = run_control(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
        )["result"]
        require(
            second_snapshot["code_revision"] == 2,
            "修复评审问题后没有形成第二个冻结范围。",
        )
        write_asset(
            feature,
            "code-review-findings.md",
            "代码评审发现第二版",
            (
                "已完整复审第二个冻结快照。冲突请求现在生成明确拒绝项，"
                "相同载荷仍只计一次且保持首个请求顺序。"
                "未发现新的阻断、严重或一般问题。"
            ),
        )
        findings_v2 = record(
            repo,
            feature,
            "code-review-findings",
        )["result"]
        require(
            findings_v2["artifacts"]["code-review-findings"]["revision"] == 2,
            "第二轮代码评审资产修订不正确。",
        )
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "code-review",
            "--result",
            "passed",
            "--evidence",
            "第二轮逐文件复审覆盖全部六个生产类，冲突缺陷已关闭。",
        )
        write_asset(
            feature,
            "auto-fix-summary.md",
            "自动修复总结第二版",
            (
                "已将普通重复与冲突载荷分支分离；冲突请求生成 "
                "DUPLICATE_CONFLICT，随后重新冻结并完成全量复审。"
            ),
        )
        auto_fix_v2 = record(repo, feature, "auto-fix-summary")["result"]
        require(
            auto_fix_v2["artifacts"]["auto-fix-summary"]["revision"] == 2,
            "第二版 Auto-fix Summary 修订不正确。",
        )
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "auto-fix",
            "--result",
            "passed",
            "--evidence",
            "评审发现已修复，第二个冻结范围的 Code Review 已通过。",
        )
        checks.append(
            {
                "检查": "Code Review 失败、修复与完整复审",
                "结果": "首轮失败未放行，第二轮闭环通过",
            }
        )

        require(
            resume_action(repo, feature) == "generate-or-update-test-source",
            "首次 Review 与 Auto-fix 关闭后没有进入 Unit Test 源码生成动作。",
        )
        test_files = write_test_phase(repo)
        third_snapshot = run_control(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
        )["result"]
        require(
            third_snapshot["code_revision"] == 3,
            "测试源码生成后没有形成第三个冻结范围。",
        )
        write_asset(
            feature,
            "code-review-findings.md",
            "代码评审发现第三版",
            (
                "Unit Test Skill 第一轮新增两个测试类后，已重新检查六个生产类"
                "和两个测试类。测试覆盖有效、无效、重复、冲突、批次上限、"
                "不可变返回与混合批次，当前冻结范围未发现可执行评审问题。"
            ),
        )
        findings_v3 = record(
            repo,
            feature,
            "code-review-findings",
        )["result"]
        require(
            findings_v3["artifacts"]["code-review-findings"]["revision"] == 3,
            "测试生成后的第三轮代码评审资产修订不正确。",
        )
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "code-review",
            "--result",
            "passed",
            "--evidence",
            "第三轮完整复审绑定新增测试源码后的冻结范围，生产与测试文件均已覆盖。",
        )
        write_asset(
            feature,
            "auto-fix-summary.md",
            "自动修复总结第三版",
            (
                "测试源码生成使旧范围失效，已重新冻结并完成第三轮完整评审。"
                "本轮没有新增评审发现，因此无需额外自动修复。"
            ),
        )
        auto_fix_v3 = record(repo, feature, "auto-fix-summary")["result"]
        require(
            auto_fix_v3["artifacts"]["auto-fix-summary"]["revision"] == 3,
            "测试生成后的第三版 Auto-fix Summary 修订不正确。",
        )
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "auto-fix",
            "--result",
            "not-required",
            "--evidence",
            "测试源码后的第三个冻结范围已通过完整评审且没有可执行发现。",
        )
        checks.append(
            {
                "检查": "Unit Test Skill 两轮交接",
                "结果": "先生成测试，再冻结、复审并关闭 Auto-fix",
            }
        )

        expect_control_failure(
            repo,
            "run-unit-test",
            "--feature-dir",
            str(feature),
            "--cwd",
            ".",
            "--",
            "sh",
            "-c",
            "mvn test",
            contains=("Unsupported or non-test command",),
        )
        failed_execution = run_feature_tests(repo, feature)
        require(
            failed_execution["outcome"] == "failed",
            f"首次真实测试没有按设计暴露缺陷：{failed_execution}",
        )
        require(
            failed_execution["test_counts"]["total"] == 14
            and failed_execution["test_counts"]["failed"] == 1,
            f"首次真实测试计数不符合预期：{failed_execution['test_counts']}",
        )
        write_unit_summary(
            feature,
            failed_execution,
            conclusion="空邮箱与有效手机号组合场景失败，禁止归档",
        )
        record(repo, feature, "unit-test-summary")
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "unit-test",
            "--result",
            "failed",
            "--evidence",
            "控制器实际执行十四项测试，其中空邮箱边界断言失败一项。",
        )
        archive_before_fix = run_control(
            repo,
            "archive-check",
            "--feature-dir",
            str(feature),
            "--require-archive",
            expected=1,
        )
        require(
            any(
                "QUALITY_GATE_NOT_PASSED:unit-test" in error
                for error in archive_before_fix["result"]["errors"]
            ),
            "真实测试失败后 Archive 没有被质量 Gate 阻断。",
        )
        checks.append(
            {
                "检查": "真实测试失败与提前 Archive",
                "结果": "十四项中一项失败，Archive 已阻断",
            }
        )

        write_source(
            repo,
            MAIN_PACKAGE / "PolicyContactChangeValidator.java",
            validator_source(fixed_blank_email=True),
        )
        fourth_snapshot = run_control(
            repo,
            "freeze-scope",
            "--feature-dir",
            str(feature),
        )["result"]
        require(
            fourth_snapshot["code_revision"] == 4,
            "测试失败修复后没有形成第四个冻结范围。",
        )
        write_asset(
            feature,
            "code-review-findings.md",
            "代码评审发现第四版",
            (
                "真实测试发现空邮箱边界后，校验器改为仅在标准化邮箱非空时检查格式。"
                "已重新检查全部当前生产与测试变更，手机号单独存在时行为符合 Spec 第二版，"
                "未发现剩余可执行问题。"
            ),
        )
        findings_v4 = record(
            repo,
            feature,
            "code-review-findings",
        )["result"]
        require(
            findings_v4["artifacts"]["code-review-findings"]["revision"] == 4,
            "第四轮代码评审资产修订不正确。",
        )
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "code-review",
            "--result",
            "passed",
            "--evidence",
            "第四轮全量复审绑定测试失败后的新冻结范围，空邮箱修复符合当前 Spec。",
        )
        write_asset(
            feature,
            "auto-fix-summary.md",
            "自动修复总结第四版",
            (
                "根据真实测试失败证据修复空邮箱判断，重新冻结范围并完成第四轮代码评审。"
                "冲突去重修复保持有效，没有修改禁止路径或新增依赖。"
            ),
        )
        auto_fix_v4 = record(repo, feature, "auto-fix-summary")["result"]
        require(
            auto_fix_v4["artifacts"]["auto-fix-summary"]["revision"] == 4,
            "第四版 Auto-fix Summary 修订不正确。",
        )
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "auto-fix",
            "--result",
            "passed",
            "--evidence",
            "测试发现已修复，第四个冻结范围已通过完整代码评审。",
        )

        passed_execution = run_feature_tests(repo, feature)
        require(
            passed_execution["outcome"] == "passed",
            f"修复后真实测试没有通过：{passed_execution}",
        )
        require(
            passed_execution["test_counts"]["total"] == 14
            and passed_execution["test_counts"]["passed"] == 14
            and passed_execution["test_counts"]["failed"] == 0
            and passed_execution["test_counts"]["errors"] == 0,
            f"修复后测试计数不符合预期：{passed_execution['test_counts']}",
        )
        write_unit_summary(
            feature,
            passed_execution,
            conclusion="十四项真实测试全部通过",
        )
        evidence_path = feature / ".sdd2/unit-test-evidence.json"
        original_evidence = evidence_path.read_text(encoding="utf-8")
        tampered_evidence = json.loads(original_evidence)
        tampered_evidence["exit_code"] = 99
        evidence_path.write_text(
            json.dumps(tampered_evidence, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        expect_control_failure(
            repo,
            "record-artifact",
            "--feature-dir",
            str(feature),
            "--stage",
            "unit-test-summary",
            contains=("UNIT_TEST_EVIDENCE_HASH_MISMATCH",),
        )
        evidence_path.write_text(original_evidence, encoding="utf-8")
        unit_summary_v2 = record(
            repo,
            feature,
            "unit-test-summary",
        )["result"]
        require(
            unit_summary_v2["artifacts"]["unit-test-summary"]["revision"] == 2,
            "成功测试后的 Summary 没有形成第二版。",
        )
        run_control(
            repo,
            "quality-gate",
            "--feature-dir",
            str(feature),
            "--gate",
            "unit-test",
            "--result",
            "passed",
            "--evidence",
            "控制器实际执行十四项测试，十四项通过，失败与 Error 均为零。",
        )
        approve_demo(
            repo,
            feature,
            "unit-test-summary",
            "large-unit-test-summary-v2",
        )
        checks.append(
            {
                "检查": "测试失败修复、复审与证据防篡改",
                "结果": "第四轮范围十四项全部通过，篡改已拒绝",
            }
        )

        archive_evidence = run_control(
            repo,
            "prepare-archive",
            "--feature-dir",
            str(feature),
        )["result"]
        write_asset(
            feature,
            "archive.md",
            "归档总结",
            (
                "批量保单联系方式变更预检与幂等计划功能已完成。"
                "共新增六个生产类和两个测试类，经历一次需求修订、"
                "一次代码评审返工和一次真实测试返工。"
                f"最终范围 SHA-256：`{archive_evidence['scope_sha256']}`；"
                f"测试证据 SHA-256："
                f"`{archive_evidence['unit_test_evidence_sha256']}`；"
                f"归档证据 SHA-256：`{archive_evidence['evidence_sha256']}`。"
            ),
        )
        archive_path = feature / ".sdd2/archive-evidence.json"
        original_archive_evidence = archive_path.read_text(encoding="utf-8")
        tampered_archive = json.loads(original_archive_evidence)
        tampered_archive["evidence_sha256"] = "f" * 64
        archive_path.write_text(
            json.dumps(tampered_archive, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        expect_control_failure(
            repo,
            "record-artifact",
            "--feature-dir",
            str(feature),
            "--stage",
            "archive",
            contains=("ARCHIVE_EVIDENCE_HASH_MISMATCH",),
        )
        archive_path.write_text(original_archive_evidence, encoding="utf-8")
        record(repo, feature, "archive")
        archive_check = run_control(
            repo,
            "archive-check",
            "--feature-dir",
            str(feature),
            "--require-archive",
        )
        require(
            archive_check["result"]["valid"],
            f"最终 Archive 检查失败：{archive_check}",
        )
        approve_demo(repo, feature, "archive", "large-archive-approval")
        checks.append({"检查": "Archive 证据篡改与最终归档", "结果": "篡改拒绝，恢复后通过"})

        validation = run_control(
            repo,
            "validate",
            "--feature-dir",
            str(feature),
        )
        require(
            validation["result"]["valid"],
            f"最终控制状态无效：{validation}",
        )
        final_state = read_json(feature / ".sdd2/feature-state.json")
        final_commit_count = int(git(repo, "rev-list", "--count", "HEAD"))
        require(
            final_commit_count == baseline_commit_count == 1,
            "大型 Demo 发生了未授权 Git 提交。",
        )
        require(
            final_state["current_stage"] == "archive"
            and final_state["stage_status"] == "completed",
            "大型 Demo 最终状态不是 archive/completed。",
        )
        require(
            not git_path(repo, "sdd2-active-feature.json").exists(),
            "最终 Archive 批准后主 worktree 锁没有释放。",
        )
        public_assets = sorted(
            path.name for path in feature.glob("*.md") if path.is_file()
        )
        require(
            len(public_assets) == 9,
            f"最终公开资产数量不是九项：{public_assets}",
        )
        approval_records = read_jsonl(
            feature / ".sdd2/gate-approvals.jsonl"
        )
        event_records = read_jsonl(feature / ".sdd2/events.jsonl")
        revision_files = sorted(
            (feature / ".sdd2/revisions").glob("*/*.md")
        )
        phase_approvals = [
            record
            for record in approval_records
            if record["stage"].startswith("phase-review:")
        ]
        require(
            len(phase_approvals) == 3,
            "三项生产 Phase Review 没有完整进入追加批准链。",
        )
        require(
            len(revision_files) == 19,
            f"资产修订快照数量不符合预期：{len(revision_files)}",
        )
        remote_ref = subprocess.run(
            [
                "git",
                "--git-dir",
                str(remote),
                "show-ref",
                "--verify",
                "refs/heads/main",
            ],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(
            remote_ref.returncode != 0,
            "被阻断的 push 仍向远端写入了分支。",
        )
        checks.append(
            {
                "检查": "最终状态、资产、哈希链、锁与 Git",
                "结果": "全部一致且无自动提交推送",
            }
        )

        result = {
            "Demo 结论": "通过",
            "实现功能": "批量保单联系方式变更预检与幂等计划生成",
            "Java 运行版本": doctor["java_specification_version"],
            "最终阶段": final_state["current_stage"],
            "最终状态": final_state["stage_status"],
            "生产文件数量": len(production_files),
            "测试文件数量": len(test_files),
            "最终测试计数": passed_execution["test_counts"],
            "首次失败测试计数": failed_execution["test_counts"],
            "公开资产数量": len(public_assets),
            "不可变修订快照数量": len(revision_files),
            "批准链记录数量": len(approval_records),
            "事件链记录数量": len(event_records),
            "冻结代码修订数量": fourth_snapshot["code_revision"],
            "最终测试证据 SHA-256": passed_execution["evidence_sha256"],
            "最终归档证据 SHA-256": archive_evidence["evidence_sha256"],
            "Git 提交数": final_commit_count,
            "深度检查点数量": len(checks),
            "检查点": checks,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DemoFailure as exc:
        print(
            json.dumps(
                {"Demo 结论": "失败", "错误": str(exc)},
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
