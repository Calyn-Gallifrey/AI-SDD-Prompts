#!/usr/bin/env python3
"""在隔离 Git 仓库中预演一个真实小功能的完整 SDD2.0 流程。"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CONTROL = Path(__file__).resolve().parent / "runtime/sdd2-control.jar"
DEMO_SOURCE = ROOT / "uaw-sdd-demo"
FEATURE_RELATIVE = Path(
    "sdd2-features/DemoSprint/contact-display-name-normalization"
)


class DemoFailure(RuntimeError):
    """表示 Demo 检查没有得到预期的确定性结果。"""


def run_process(
    command: list[str],
    *,
    cwd: Path,
    expected: int = 0,
) -> subprocess.CompletedProcess[str]:
    process = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != expected:
        detail = process.stdout + process.stderr
        raise DemoFailure(
            f"命令返回码不符合预期：{command!r}，"
            f"expected={expected}, actual={process.returncode}\n{detail}"
        )
    return process


def run_control(
    repo: Path,
    *arguments: str,
    expected: int = 0,
) -> dict[str, Any]:
    process = run_process(
        ["java", "-jar", str(CONTROL), *arguments],
        cwd=repo,
        expected=expected,
    )
    try:
        return json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise DemoFailure(f"控制器没有返回有效 JSON：{process.stdout}") from exc


def git(repo: Path, *arguments: str) -> str:
    return run_process(["git", *arguments], cwd=repo).stdout.strip()


def write_asset(feature: Path, filename: str, title: str, body: str) -> None:
    (feature / filename).write_text(
        f"# {title}\n\n{body}\n",
        encoding="utf-8",
    )


def record(repo: Path, feature: Path, stage: str) -> dict[str, Any]:
    return run_control(
        repo,
        "record-artifact",
        "--feature-dir",
        str(feature),
        "--stage",
        stage,
    )


def approve_demo(
    repo: Path,
    feature: Path,
    stage: str,
    message_id: str,
) -> dict[str, Any]:
    return run_control(
        repo,
        "approve",
        "--feature-dir",
        str(feature),
        "--stage",
        stage,
        "--source",
        "demo-simulation",
        "--approver-role",
        "ai-as-human-reviewer",
        "--approval-text",
        f"Demo 模拟批准当前 {stage} 阶段",
        "--message-id",
        message_id,
    )


def main() -> int:
    if shutil.which("java") is None:
        raise DemoFailure(
            "当前环境未检测到 Java。请安装或启用 Java 8 及以上版本，"
            "并正确配置 PATH/JAVA_HOME。"
        )
    if not CONTROL.is_file():
        raise DemoFailure(f"缺少 Java 8 控制器 JAR：{CONTROL}")
    run_control(ROOT, "doctor", "--repo-root", str(ROOT))
    if shutil.which("mvn") is None:
        raise DemoFailure("当前环境未安装 Maven，无法执行真实 Java 单元测试 Demo。")
    checks: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="uaw-sdd2-demo-") as temp:
        repo = Path(temp)
        shutil.copytree(DEMO_SOURCE, repo / "uaw-sdd-demo")
        git(repo, "init", "-q")
        git(repo, "config", "user.email", "sdd2-demo@example.invalid")
        git(repo, "config", "user.name", "SDD2 Demo")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "demo baseline")
        baseline_commit_count = int(git(repo, "rev-list", "--count", "HEAD"))

        feature = repo / FEATURE_RELATIVE
        feature.mkdir(parents=True)
        write_asset(
            feature,
            "brief-design.md",
            "人工简要设计",
            (
                "在 Demo 项目中新增联系人显示名称规范化工具，去除首尾空白并合并连续空白。"
                "变更只允许落在新增工具类和对应单元测试，不修改现有接口或依赖。"
            ),
        )
        run_control(
            repo,
            "init",
            "--feature-dir",
            str(feature),
            "--feature-id",
            "contact-display-name-normalization",
            "--mode",
            "demo",
        )
        run_control(
            repo,
            "authorize-demo",
            "--feature-dir",
            str(feature),
            "--authorization-text",
            "用户明确授权运行本次完整 Demo 预演并模拟各阶段人工审核。",
            "--message-id",
            "current-user-demo-request",
        )

        write_asset(
            feature,
            "proposal-input.md",
            "内部规划输入",
            (
                "目标是新增一个无状态 Java 工具类，将空值转为空字符串，去除首尾空白，"
                "并把名称内部连续空白合并为一个普通空格。禁止修改既有业务类和构建依赖。"
            ),
        )
        record(repo, feature, "proposal-input")
        write_asset(
            feature,
            "spec.md",
            "需求规格",
            (
                "输入为空值时返回空字符串；输入包含首尾或连续空白时返回规范化名称；"
                "普通名称保持不变。验收要求真实单元测试覆盖空值、连续空白和普通输入。"
            ),
        )
        record(repo, feature, "spec")

        write_asset(
            feature,
            "design.md",
            "提前生成的设计",
            "该文件用于验证等待 Spec 审核时不能提前生成 Design，随后必须移走。",
        )
        (feature / "analysis-result.md").write_text(
            "弱模型错误生成的额外分析文件。\n",
            encoding="utf-8",
        )
        sibling = repo / "sdd2-features/DemoSprint/duplicate-contact-feature"
        sibling.mkdir(parents=True)
        write_asset(
            sibling,
            "brief-design.md",
            "错误重复功能",
            "该目录用于验证同一工作区不能串入第二个未受控 Feature。",
        )
        layout_result = run_control(
            repo,
            "resume",
            "--feature-dir",
            str(feature),
            expected=1,
        )
        layout_errors = layout_result["result"]["validation"]["errors"]
        required_layout_codes = (
            "UNEXPECTED_STAGE_ASSET:design.md",
            "UNEXPECTED_FEATURE_FILE:analysis-result.md",
            "UNCONTROLLED_SIBLING_FEATURE:",
        )
        if not all(
            any(code in error for error in layout_errors)
            for code in required_layout_codes
        ):
            raise DemoFailure(f"乱文件或串 Feature 攻击未全部阻断：{layout_errors}")
        checks.append({"检查": "乱文件、提前资产和重复 Feature", "结果": "已阻断"})
        (feature / "design.md").unlink()
        (feature / "analysis-result.md").unlink()
        shutil.rmtree(sibling)
        resumed = run_control(
            repo,
            "resume",
            "--feature-dir",
            str(feature),
        )
        if resumed["result"]["next_required_action"] != "request-spec-approval":
            raise DemoFailure("移走违规文件后没有恢复到原 Spec Gate。")

        state_path = feature / ".sdd2/feature-state.json"
        original_state = state_path.read_text(encoding="utf-8")
        tampered_state = json.loads(original_state)
        tampered_state["current_stage"] = "design"
        tampered_state["stage_status"] = "ready"
        tampered_state["next_required_action"] = "generate-design"
        state_path.write_text(
            json.dumps(tampered_state, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        tamper_result = run_control(
            repo,
            "resume",
            "--feature-dir",
            str(feature),
            expected=1,
        )
        if (
            "STATE_EVENT_PROJECTION_MISMATCH"
            not in tamper_result["result"]["validation"]["errors"]
        ):
            raise DemoFailure("状态篡改没有被事件投影哈希阻断。")
        state_path.write_text(original_state, encoding="utf-8")
        checks.append({"检查": "控制状态直接篡改", "结果": "已阻断"})

        existing_production = (
            repo
            / "uaw-sdd-demo/src/main/java/com/example/uawsdddemo/"
            "UawSddDemoApplication.java"
        )
        original_production = existing_production.read_text(encoding="utf-8")
        existing_production.write_text(
            original_production + "\n// 未经人工 Gate 的错误提前实现。\n",
            encoding="utf-8",
        )
        premature = run_control(
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
            "premature-code-approval",
            expected=2,
        )
        if "PRE_IMPLEMENTATION_CHANGE" not in premature["error"]:
            raise DemoFailure("人工 Gate 前的生产代码变更没有被阻断。")
        existing_production.write_text(original_production, encoding="utf-8")
        resumed_after_code = run_control(
            repo,
            "resume",
            "--feature-dir",
            str(feature),
        )
        if (
            resumed_after_code["result"]["next_required_action"]
            != "request-spec-approval"
        ):
            raise DemoFailure("恢复提前代码后没有返回原 Spec Gate。")
        checks.append({"检查": "人工 Gate 前提前生成生产代码", "结果": "已阻断"})

        approve_demo(repo, feature, "spec", "demo-spec-approval")
        write_asset(
            feature,
            "design.md",
            "技术设计",
            (
                "新增 final 工具类 ContactDisplayNameFormatter 和静态 normalize 方法。"
                "实现只使用 Java 标准库，测试使用项目现有 JUnit 5，不新增依赖。"
            ),
        )
        record(repo, feature, "design")
        approve_demo(repo, feature, "design", "demo-design-approval")
        write_asset(
            feature,
            "tasks.md",
            "实现任务",
            (
                "Phase1 新增名称规范化工具；Phase2 新增边界和回归测试。"
                "两个 Phase 都要等待模拟 Phase Review，之后才能冻结范围并进入代码评审。"
            ),
        )
        record(repo, feature, "tasks")
        approve_demo(repo, feature, "tasks", "demo-tasks-approval")

        phase_one = "Phase1-实现显示名称规范化"
        phase_two = "Phase2-补齐边界测试"
        scope = run_control(
            repo,
            "capture-scope",
            "--feature-dir",
            str(feature),
            "--allowed-path",
            "uaw-sdd-demo/src/main/java/com/example/uawsdddemo/util/**",
            "--allowed-path",
            "uaw-sdd-demo/src/test/java/com/example/uawsdddemo/util/**",
            "--forbidden-path",
            "uaw-sdd-demo/pom.xml",
            "--required-phase",
            phase_one,
            "--required-phase",
            phase_two,
            "--test-path",
            "uaw-sdd-demo/src/test/java/**",
        )["result"]
        if not scope.get("implementation_permit_sha256"):
            raise DemoFailure("实现许可没有绑定范围和人工 Gate。")

        production = (
            repo
            / "uaw-sdd-demo/src/main/java/com/example/uawsdddemo/util/"
            "ContactDisplayNameFormatter.java"
        )
        production.parent.mkdir(parents=True)
        production.write_text(
            "package com.example.uawsdddemo.util;\n\n"
            "public final class ContactDisplayNameFormatter {\n"
            "    private ContactDisplayNameFormatter() {\n"
            "    }\n\n"
            "    public static String normalize(String value) {\n"
            "        if (value == null) {\n"
            "            return \"\";\n"
            "        }\n"
            "        return value.trim().replaceAll(\"\\\\s+\", \" \");\n"
            "    }\n"
            "}\n",
            encoding="utf-8",
        )
        run_control(
            repo,
            "phase-review",
            "--feature-dir",
            str(feature),
            "--phase",
            phase_one,
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            f"Demo 模拟批准 {phase_one}",
            "--message-id",
            "demo-phase-one-approval",
        )

        test_source = (
            repo
            / "uaw-sdd-demo/src/test/java/com/example/uawsdddemo/util/"
            "ContactDisplayNameFormatterTest.java"
        )
        test_source.parent.mkdir(parents=True)
        test_source.write_text(
            "package com.example.uawsdddemo.util;\n\n"
            "import org.junit.jupiter.api.Test;\n\n"
            "import static org.junit.jupiter.api.Assertions.assertEquals;\n\n"
            "class ContactDisplayNameFormatterTest {\n"
            "    @Test\n"
            "    void normalizesWhitespace() {\n"
            "        assertEquals(\"Mary Ann\", "
            "ContactDisplayNameFormatter.normalize(\"  Mary   Ann  \"));\n"
            "    }\n\n"
            "    @Test\n"
            "    void convertsNullToEmptyText() {\n"
            "        assertEquals(\"\", ContactDisplayNameFormatter.normalize(null));\n"
            "    }\n\n"
            "    @Test\n"
            "    void keepsAlreadyNormalizedName() {\n"
            "        assertEquals(\"Mary Ann\", "
            "ContactDisplayNameFormatter.normalize(\"Mary Ann\"));\n"
            "    }\n"
            "}\n",
            encoding="utf-8",
        )
        run_control(
            repo,
            "phase-review",
            "--feature-dir",
            str(feature),
            "--phase",
            phase_two,
            "--source",
            "demo-simulation",
            "--approver-role",
            "ai-as-human-reviewer",
            "--approval-text",
            f"Demo 模拟批准 {phase_two}",
            "--message-id",
            "demo-phase-two-approval",
        )

        approval_records = [
            json.loads(line)
            for line in (feature / ".sdd2/gate-approvals.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        phase_stages = {
            record["stage"]
            for record in approval_records
            if record["stage"].startswith("phase-review:")
        }
        if phase_stages != {
            f"phase-review:{phase_one}",
            f"phase-review:{phase_two}",
        }:
            raise DemoFailure("Phase Review 没有完整进入仅追加批准链。")
        checks.append({"检查": "阶段 Gate 与 Phase Review 批准链", "结果": "绑定有效"})

        blocked_commit = subprocess.run(
            ["git", "commit", "--allow-empty", "--no-verify", "-m", "forbidden demo commit"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if blocked_commit.returncode == 0 or "SDD2_COMMIT_BLOCKED" not in (
            blocked_commit.stdout + blocked_commit.stderr
        ):
            raise DemoFailure("活动 Feature 没有阻止自动提交。")
        checks.append({"检查": "活动流程自动提交", "结果": "已阻断"})

        run_control(repo, "freeze-scope", "--feature-dir", str(feature))
        write_asset(
            feature,
            "code-review-findings.md",
            "代码评审发现",
            (
                "已按冻结范围检查新增工具类和三项测试，未发现阻断、严重或一般问题。"
                "实现未修改禁止路径，也没有新增依赖。"
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
            "passed",
            "--evidence",
            "完整评审当前冻结范围，未发现可执行问题。",
        )
        write_asset(
            feature,
            "auto-fix-summary.md",
            "自动修复总结",
            "当前代码评审没有可执行发现，因此无需修改代码，范围保持不变。",
        )
        record(repo, feature, "auto-fix-summary")
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
            "当前冻结范围没有需要修复的评审发现。",
        )

        execution = run_control(
            repo,
            "run-unit-test",
            "--feature-dir",
            str(feature),
            "--cwd",
            ".",
            "--",
            "mvn",
            "-f",
            "uaw-sdd-demo/pom.xml",
            "-Dtest=ContactDisplayNameFormatterTest",
            "test",
        )["result"]
        if (
            execution["outcome"] != "passed"
            or execution["test_counts"]["total"] != 3
            or execution["test_counts"]["passed"] != 3
        ):
            raise DemoFailure(f"真实 Maven 测试没有通过：{execution}")
        checks.append(
            {
                "检查": "真实 Maven 单元测试",
                "结果": "已通过",
                "通过数": execution["test_counts"]["passed"],
            }
        )

        summary_body = (
            f"控制器执行证据 SHA-256：`{execution['evidence_sha256']}`。\n\n"
            f"冻结范围 SHA-256：`{execution['scope_sha256']}`。\n\n"
            f"实际执行 {execution['test_counts']['total']} 项测试，"
            f"通过 {execution['test_counts']['passed']} 项，失败与 Error 均为零。"
        )
        write_asset(
            feature,
            "unit-test-summary.md",
            "单元测试总结",
            summary_body,
        )
        evidence_path = feature / ".sdd2/unit-test-evidence.json"
        original_evidence = evidence_path.read_text(encoding="utf-8")
        tampered_evidence = json.loads(original_evidence)
        tampered_evidence["exit_code"] = 99
        evidence_path.write_text(
            json.dumps(tampered_evidence, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        evidence_attack = run_control(
            repo,
            "record-artifact",
            "--feature-dir",
            str(feature),
            "--stage",
            "unit-test-summary",
            expected=2,
        )
        if "UNIT_TEST_EVIDENCE_HASH_MISMATCH" not in evidence_attack["error"]:
            raise DemoFailure("测试证据篡改没有阻断 Unit Test Summary。")
        evidence_path.write_text(original_evidence, encoding="utf-8")
        checks.append({"检查": "单元测试执行证据篡改", "结果": "已阻断"})

        record(repo, feature, "unit-test-summary")
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
            "控制器观察到三项测试通过、退出码为零且范围未变化。",
        )
        approve_demo(
            repo,
            feature,
            "unit-test-summary",
            "demo-unit-test-summary-approval",
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
                "联系人显示名称规范化工具及三项单元测试已经完成。"
                f"冻结范围 SHA-256 为 `{archive_evidence['scope_sha256']}`，"
                f"单元测试证据 SHA-256 为 "
                f"`{archive_evidence['unit_test_evidence_sha256']}`，"
                f"归档证据 SHA-256 为 `{archive_evidence['evidence_sha256']}`。"
            ),
        )
        record(repo, feature, "archive")
        archive_check = run_control(
            repo,
            "archive-check",
            "--feature-dir",
            str(feature),
            "--require-archive",
        )
        if not archive_check["result"]["valid"]:
            raise DemoFailure(f"Archive Gate 未通过：{archive_check}")
        approve_demo(repo, feature, "archive", "demo-archive-approval")

        validation = run_control(
            repo,
            "validate",
            "--feature-dir",
            str(feature),
        )
        if not validation["result"]["valid"]:
            raise DemoFailure(f"最终控制状态无效：{validation}")
        final_state = json.loads(state_path.read_text(encoding="utf-8"))
        final_commit_count = int(git(repo, "rev-list", "--count", "HEAD"))
        if final_commit_count != baseline_commit_count:
            raise DemoFailure("Demo 流程发生了未授权 Git 提交。")
        if final_state["stage_status"] != "completed":
            raise DemoFailure("最终状态不是 completed。")
        checks.append({"检查": "最终状态、Archive 与无自动提交", "结果": "已通过"})

        result = {
            "Demo 结论": "通过",
            "实现功能": "联系人显示名称规范化",
            "最终阶段": final_state["current_stage"],
            "最终状态": final_state["stage_status"],
            "公开资产数量": len(
                [path for path in feature.glob("*.md") if path.is_file()]
            ),
            "测试执行证据 SHA-256": execution["evidence_sha256"],
            "测试计数": execution["test_counts"],
            "Git 提交数": final_commit_count,
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
