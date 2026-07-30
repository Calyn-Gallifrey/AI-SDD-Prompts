from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "sdd2_control.py"
PUBLIC_ASSET_NAMES = {
    "brief-design.md",
    "proposal-input.md",
    "spec.md",
    "design.md",
    "tasks.md",
    "code-review-findings.md",
    "auto-fix-summary.md",
    "unit-test-summary.md",
    "archive.md",
}
VALID_CHINESE_BODY = "\n\n本资产用于控制流程测试，正文采用简体中文并记录当前阶段的真实信息。\n"


class Sdd2ControlTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self._git("init", "-q")
        self._git("config", "user.email", "sdd2-test@example.invalid")
        self._git("config", "user.name", "SDD2 Test")
        (self.repo / "app/src/main/java").mkdir(parents=True)
        (self.repo / "app/src/main/java/App.java").write_text("class App {}\n", encoding="utf-8")
        (self.repo / "README.md").write_text("test\n", encoding="utf-8")
        self._git("add", ".")
        self._git("commit", "-qm", "baseline")
        self.feature = self.repo / "sdd2-features/Sprint1/example"
        self.feature.mkdir(parents=True)
        self._write("brief-design.md", "# Brief\n")
        self._run("init", "--feature-dir", str(self.feature), "--feature-id", "example")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _git(self, *args: str) -> str:
        process = subprocess.run(
            ["git", *args], cwd=self.repo, text=True, capture_output=True, check=True
        )
        return process.stdout.strip()

    def _write(self, name: str, content: str) -> None:
        path = self.feature / name
        if name in PUBLIC_ASSET_NAMES:
            content += VALID_CHINESE_BODY
        path.write_text(content, encoding="utf-8")

    def _run(self, *args: str, expected: int = 0) -> dict:
        process = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, expected, process.stdout + process.stderr)
        return json.loads(process.stdout)

    def _record(self, stage: str, filename: str, content: str) -> None:
        self._write(filename, content)
        self._run("record-artifact", "--feature-dir", str(self.feature), "--stage", stage)

    def _approve(self, stage: str) -> None:
        self._run(
            "approve",
            "--feature-dir",
            str(self.feature),
            "--stage",
            stage,
            "--source",
            "user-message",
            "--approver-role",
            "human",
            "--approval-text",
            f"批准 {stage}",
            "--message-id",
            f"message-{stage}",
        )

    def _reach_tasks_approval(self) -> None:
        self._record("proposal-input", "proposal-input.md", "# Proposal\n")
        self._record("spec", "spec.md", "# Spec\n")
        self._approve("spec")
        self._record("design", "design.md", "# Design\n")
        self._approve("design")
        self._record("tasks", "tasks.md", "# Tasks\n")
        self._approve("tasks")

    def _capture_scope(self) -> None:
        self._run(
            "capture-scope",
            "--feature-dir",
            str(self.feature),
            "--allowed-path",
            "app/**",
            "--forbidden-path",
            "app/secrets/**",
            "--required-phase",
            "Phase1",
            "--test-path",
            "app/src/test/**",
        )

    def _complete_implementation_and_archive(self) -> None:
        (self.repo / "app/src/main/java/App.java").write_text(
            "class App { int value = 1; }\n", encoding="utf-8"
        )
        test = self.repo / "app/src/test/java/AppTest.java"
        test.parent.mkdir(parents=True)
        test.write_text("class AppTest {}\n", encoding="utf-8")
        self._run(
            "phase-review", "--feature-dir", str(self.feature), "--phase", "Phase1",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "批准 Phase1", "--message-id", "phase-1"
        )
        self._run("freeze-scope", "--feature-dir", str(self.feature))
        self._record("code-review-findings", "code-review-findings.md", "# Findings\nPassed\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "code-review",
            "--result", "passed", "--evidence", "all required checks completed"
        )
        self._record("auto-fix-summary", "auto-fix-summary.md", "# Auto-fix\nNot required\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "auto-fix",
            "--result", "not-required", "--evidence", "no actionable finding"
        )
        self._record("unit-test-summary", "unit-test-summary.md", "# Unit Test\nPassed\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "unit-test",
            "--result", "passed", "--evidence", "test command exit code 0; 1 test passed"
        )
        self._approve("unit-test-summary")
        evidence = self._run("prepare-archive", "--feature-dir", str(self.feature))["result"]
        self._record(
            "archive", "archive.md", f"# Archive\nEvidence: {evidence['evidence_sha256']}\n"
        )
        self.assertTrue(
            self._run(
                "archive-check", "--feature-dir", str(self.feature), "--require-archive"
            )["result"]["valid"]
        )
        self._approve("archive")
        result = self._run("validate", "--feature-dir", str(self.feature))
        self.assertTrue(result["result"]["valid"])
        git_dir = Path(self._git("rev-parse", "--git-dir"))
        if not git_dir.is_absolute():
            git_dir = self.repo / git_dir
        self.assertFalse((git_dir / "sdd2-active-feature.json").exists())

    def _start_demo_feature(self) -> None:
        self._run(
            "close", "--feature-dir", str(self.feature), "--result", "aborted",
            "--approval-text", "同意终止并关闭", "--message-id", "close-before-demo",
        )
        shutil.rmtree(self.feature)
        self.feature = self.repo / "sdd2-features/Sprint1/demo"
        self.feature.mkdir(parents=True)
        self._write("brief-design.md", "# Demo Brief\n")
        self._run(
            "init", "--feature-dir", str(self.feature), "--feature-id", "demo", "--mode", "demo",
        )

    def test_full_success_flow_releases_lock(self) -> None:
        self._reach_tasks_approval()
        self._capture_scope()
        self._complete_implementation_and_archive()

    def test_ambiguous_and_self_approval_are_rejected(self) -> None:
        self._record("proposal-input", "proposal-input.md", "# Proposal\n")
        self._record("spec", "spec.md", "# Spec\n")
        ambiguous = self._run(
            "approve", "--feature-dir", str(self.feature), "--stage", "spec",
            "--source", "user-message", "--approver-role", "human", "--approval-text", "ok",
            expected=2,
        )
        self.assertIn("ambiguous", ambiguous["error"])
        simulated = self._run(
            "approve", "--feature-dir", str(self.feature), "--stage", "spec",
            "--source", "demo-simulation", "--approver-role", "ai-as-human-reviewer",
            "--approval-text", "approved spec", expected=2,
        )
        self.assertIn("demo authorization", simulated["error"])

    def test_natural_chinese_demo_authorization_and_negation(self) -> None:
        self._start_demo_feature()
        rejected = self._run(
            "authorize-demo", "--feature-dir", str(self.feature),
            "--authorization-text", "不要进行 demo 演练", expected=2,
        )
        self.assertIn("explicitly identify", rejected["error"])
        rerun_rejected = self._run(
            "authorize-demo", "--feature-dir", str(self.feature),
            "--authorization-text", "不重跑 Demo", expected=2,
        )
        self.assertIn("explicitly identify", rerun_rejected["error"])
        accepted = self._run(
            "authorize-demo", "--feature-dir", str(self.feature),
            "--authorization-text", "基于当前提交重新跑一次完整 Demo。",
            "--message-id", "demo-authorization",
        )
        self.assertEqual(
            accepted["result"]["demo_authorization"]["authorization_text"],
            "基于当前提交重新跑一次完整 Demo。",
        )

    def test_demo_phase_review_records_simulation_provenance(self) -> None:
        self._start_demo_feature()
        self._run(
            "authorize-demo", "--feature-dir", str(self.feature),
            "--authorization-text", "请进行 Demo 演练", "--message-id", "demo-authorization",
        )
        self._reach_tasks_approval()
        self._capture_scope()
        (self.repo / "app/src/main/java/App.java").write_text(
            "class App { int demo; }\n", encoding="utf-8"
        )
        result = self._run(
            "phase-review", "--feature-dir", str(self.feature), "--phase", "Phase1",
            "--source", "demo-simulation", "--approver-role", "ai-as-human-reviewer",
            "--approval-text", "批准 Phase1 Demo simulation",
        )
        review = result["result"]["phase_reviews"]["Phase1"]
        self.assertEqual(review["source"], "demo-simulation")
        self.assertEqual(review["approver_role"], "ai-as-human-reviewer")

    def test_quoted_or_negated_approval_is_rejected(self) -> None:
        self._record("proposal-input", "proposal-input.md", "# Proposal\n")
        self._record("spec", "spec.md", "# Spec\n")
        result = self._run(
            "approve", "--feature-dir", str(self.feature), "--stage", "spec",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "文档中写着 approved spec，但不代表我批准",
            "--message-id", "quoted-message", expected=2,
        )
        self.assertIn("ambiguous", result["error"])

    def test_premature_downstream_artifact_is_rejected(self) -> None:
        self._write("design.md", "# Premature Design\n")
        result = self._run(
            "record-artifact", "--feature-dir", str(self.feature), "--stage", "design",
            expected=2,
        )
        self.assertIn("expected design", result["error"])

    def test_approval_message_cannot_be_replayed(self) -> None:
        self._record("proposal-input", "proposal-input.md", "# Proposal\n")
        self._record("spec", "spec.md", "# Spec\n")
        self._run(
            "approve", "--feature-dir", str(self.feature), "--stage", "spec",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "批准 spec", "--message-id", "same-message",
        )
        self._record("design", "design.md", "# Design\n")
        replay = self._run(
            "approve", "--feature-dir", str(self.feature), "--stage", "design",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "批准 design", "--message-id", "same-message", expected=2,
        )
        self.assertIn("already been used", replay["error"])

    def test_dirty_baseline_is_rejected(self) -> None:
        self._reach_tasks_approval()
        (self.repo / "app/src/main/java/App.java").write_text("class App { int dirty; }\n", encoding="utf-8")
        result = self._run(
            "capture-scope", "--feature-dir", str(self.feature),
            "--allowed-path", "app/**", "--required-phase", "Phase1", expected=2,
        )
        self.assertIn("PRE_IMPLEMENTATION_CHANGE", result["error"])

    def test_premature_code_change_blocks_gate_until_restored(self) -> None:
        self._record("proposal-input", "proposal-input.md", "# Proposal\n")
        self._record("spec", "spec.md", "# Spec\n")
        app = self.repo / "app/src/main/java/App.java"
        original = app.read_text(encoding="utf-8")
        app.write_text("class App { int premature; }\n", encoding="utf-8")

        blocked = self._run(
            "approve", "--feature-dir", str(self.feature), "--stage", "spec",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "批准 spec", "--message-id", "premature-spec-approval",
            expected=2,
        )
        self.assertIn("PRE_IMPLEMENTATION_CHANGE", blocked["error"])
        state = json.loads((self.feature / ".sdd2/feature-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["stage_status"], "blocked")
        self.assertEqual(state["blocked"]["code"], "PREMATURE_IMPLEMENTATION_CHANGE")

        app.write_text(original, encoding="utf-8")
        resumed = self._run("resume", "--feature-dir", str(self.feature))
        self.assertEqual(resumed["result"]["current_stage"], "spec")
        self.assertEqual(resumed["result"]["stage_status"], "awaiting-approval")
        self.assertEqual(resumed["result"]["next_required_action"], "request-spec-approval")

    def test_weak_model_bypass_demo_recovers_and_archives(self) -> None:
        self._record("proposal-input", "proposal-input.md", "# Proposal\n")
        self._record("spec", "spec.md", "# Spec\n")
        app = self.repo / "app/src/main/java/App.java"
        original = app.read_text(encoding="utf-8")
        app.write_text("class App { int premature; }\n", encoding="utf-8")
        self._git("add", "app/src/main/java/App.java")

        blocked_approval = self._run(
            "approve", "--feature-dir", str(self.feature), "--stage", "spec",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "批准 spec", "--message-id", "premature-spec-approval",
            expected=2,
        )
        self.assertIn("PRE_IMPLEMENTATION_CHANGE", blocked_approval["error"])

        blocked_commit = subprocess.run(
            ["git", "commit", "--no-verify", "-m", "premature"],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(blocked_commit.returncode, 0)
        self.assertIn("SDD2_COMMIT_BLOCKED", blocked_commit.stdout + blocked_commit.stderr)
        self.assertEqual(self._git("rev-list", "--count", "HEAD"), "1")

        app.write_text(original, encoding="utf-8")
        self._git("add", "app/src/main/java/App.java")
        resumed = self._run("resume", "--feature-dir", str(self.feature))
        self.assertEqual(resumed["result"]["current_stage"], "spec")
        self.assertEqual(resumed["result"]["stage_status"], "awaiting-approval")
        self.assertEqual(resumed["result"]["next_required_action"], "request-spec-approval")

        self._approve("spec")
        self._record("design", "design.md", "# Design\n")
        self._approve("design")
        self._record("tasks", "tasks.md", "# Tasks\n")
        self._approve("tasks")
        self._capture_scope()
        self._complete_implementation_and_archive()

    def test_capture_scope_issues_approval_bound_implementation_permit(self) -> None:
        self._reach_tasks_approval()
        scope = self._run(
            "capture-scope", "--feature-dir", str(self.feature),
            "--allowed-path", "app/**", "--required-phase", "Phase1",
            "--test-path", "app/src/test/**",
        )["result"]
        state = json.loads((self.feature / ".sdd2/feature-state.json").read_text(encoding="utf-8"))
        permit = state["implementation_permit"]

        self.assertEqual(permit["status"], "active")
        self.assertEqual(permit["attempt"], state["attempt"])
        self.assertEqual(scope["implementation_permit_sha256"], permit["permit_sha256"])
        for stage in ("spec", "design", "tasks"):
            self.assertEqual(
                permit["approved_artifacts"][stage]["sha256"],
                state["artifacts"][stage]["sha256"],
            )
            self.assertEqual(
                permit["approved_artifacts"][stage]["approval_id"],
                state["approvals"][stage]["approval_id"],
            )

    def test_tampered_implementation_permit_blocks_implementation_action(self) -> None:
        self._reach_tasks_approval()
        self._capture_scope()
        state_path = self.feature / ".sdd2/feature-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["implementation_permit"]["permit_sha256"] = "0" * 64
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        blocked = self._run(
            "phase-review", "--feature-dir", str(self.feature), "--phase", "Phase1",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "批准 Phase1", "--message-id", "tampered-permit",
            expected=2,
        )
        self.assertIn("IMPLEMENTATION_PERMIT", blocked["error"])

    def test_active_feature_blocks_commit_even_with_no_verify(self) -> None:
        (self.repo / "README.md").write_text("premature commit\n", encoding="utf-8")
        self._git("add", "README.md")
        process = subprocess.run(
            ["git", "commit", "--no-verify", "-m", "premature"],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("SDD2_COMMIT_BLOCKED", process.stdout + process.stderr)
        self.assertEqual(self._git("rev-list", "--count", "HEAD"), "1")

    def test_active_feature_blocks_push(self) -> None:
        remote = self.repo / "remote.git"
        subprocess.run(
            ["git", "init", "--bare", "-q", str(remote)],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=True,
        )
        self._git("remote", "add", "origin", str(remote))

        process = subprocess.run(
            ["git", "push", "origin", "HEAD:refs/heads/main"],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("SDD2_COMMIT_BLOCKED", process.stdout + process.stderr)

        remote_ref = subprocess.run(
            ["git", "--git-dir", str(remote), "show-ref", "--verify", "refs/heads/main"],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(remote_ref.returncode, 0)

    def test_git_guard_preserves_existing_hook_and_releases_after_close(self) -> None:
        self._run(
            "close", "--feature-dir", str(self.feature), "--result", "aborted",
            "--approval-text", "同意终止并关闭", "--message-id", "close-before-hook-test",
        )
        hooks = Path(self._git("rev-parse", "--git-path", "hooks"))
        if not hooks.is_absolute():
            hooks = self.repo / hooks
        hook = hooks / "prepare-commit-msg"
        backup = hooks / "prepare-commit-msg.sdd2-original"
        hook.unlink()
        backup.unlink(missing_ok=True)
        hook.write_text(
            "#!/bin/sh\n"
            "touch \"$(git rev-parse --git-dir)/existing-hook-ran\"\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)

        self.feature = self.repo / "sdd2-features/Sprint1/hook-compatible"
        self.feature.mkdir(parents=True)
        self._write("brief-design.md", "# Hook 兼容性验证\n")
        self._run(
            "init", "--feature-dir", str(self.feature), "--feature-id", "hook-compatible",
        )
        self.assertTrue(backup.is_file())

        blocked = subprocess.run(
            ["git", "commit", "--allow-empty", "--no-verify", "-m", "blocked"],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(blocked.returncode, 0)
        self.assertFalse((self.repo / ".git/existing-hook-ran").exists())

        self._run(
            "close", "--feature-dir", str(self.feature), "--result", "aborted",
            "--approval-text", "同意终止并关闭", "--message-id", "close-hook-compatible",
        )
        self._git("commit", "--allow-empty", "--no-verify", "-m", "allowed after close")
        self.assertTrue((self.repo / ".git/existing-hook-ran").is_file())

    def test_git_guard_supports_custom_hooks_path(self) -> None:
        self._run(
            "close", "--feature-dir", str(self.feature), "--result", "aborted",
            "--approval-text", "同意终止并关闭", "--message-id", "close-before-custom-hooks",
        )
        custom_hooks = self.repo / ".custom-hooks"
        custom_hooks.mkdir()
        existing = custom_hooks / "prepare-commit-msg"
        existing.write_text(
            "#!/bin/sh\n"
            "touch \"$(git rev-parse --git-dir)/custom-hook-ran\"\n",
            encoding="utf-8",
        )
        existing.chmod(0o755)
        self._git("config", "core.hooksPath", ".custom-hooks")

        self.feature = self.repo / "sdd2-features/Sprint1/custom-hooks"
        self.feature.mkdir(parents=True)
        self._write("brief-design.md", "# 自定义 Hook 路径验证\n")
        self._run(
            "init", "--feature-dir", str(self.feature), "--feature-id", "custom-hooks",
        )
        self.assertIn("UAW-SDD2 GIT GUARD", existing.read_text(encoding="utf-8"))
        self.assertTrue((custom_hooks / "prepare-commit-msg.sdd2-original").is_file())

        blocked = subprocess.run(
            ["git", "commit", "--allow-empty", "--no-verify", "-m", "blocked"],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("SDD2_COMMIT_BLOCKED", blocked.stdout + blocked.stderr)
        self.assertFalse((self.repo / ".git/custom-hook-ran").exists())

        self._run(
            "close", "--feature-dir", str(self.feature), "--result", "aborted",
            "--approval-text", "同意终止并关闭", "--message-id", "close-custom-hooks",
        )
        self._git("commit", "--allow-empty", "--no-verify", "-m", "allowed after close")
        self.assertTrue((self.repo / ".git/custom-hook-ran").is_file())

    def test_phase_order_and_parallel_feature_lock_are_enforced(self) -> None:
        self._reach_tasks_approval()
        self._run(
            "capture-scope", "--feature-dir", str(self.feature),
            "--allowed-path", "app/**", "--required-phase", "Phase1",
            "--required-phase", "Phase2", "--test-path", "app/src/test/**",
        )
        order = self._run(
            "phase-review", "--feature-dir", str(self.feature), "--phase", "Phase2",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "批准 Phase2", expected=2,
        )
        self.assertIn("order violation", order["error"])

        second = self.repo / "sdd2-features/Sprint1/second"
        second.mkdir(parents=True)
        (second / "brief-design.md").write_text(
            "# 人工简要设计\n\n这是第二个功能，用于验证同一工作区的并行锁。\n",
            encoding="utf-8",
        )
        locked = self._run(
            "init", "--feature-dir", str(second), "--feature-id", "second", expected=2,
        )
        self.assertIn("locked by another", locked["error"])

    def test_requirement_revision_invalidates_downstream_approvals(self) -> None:
        self._reach_tasks_approval()
        self._record("spec", "spec.md", "# Spec revision 2\n")
        state = json.loads((self.feature / ".sdd2/feature-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["current_stage"], "spec")
        self.assertEqual(state["stage_status"], "awaiting-approval")
        for stage in ("spec", "design", "tasks"):
            self.assertEqual(state["approvals"][stage]["status"], "invalidated")

    def test_hash_chain_corruption_blocks_mutation(self) -> None:
        self._reach_tasks_approval()
        approvals = self.feature / ".sdd2/gate-approvals.jsonl"
        approvals.write_text(
            approvals.read_text(encoding="utf-8").replace('"result":"approved"', '"result":"tampered"', 1),
            encoding="utf-8",
        )
        validation = self._run("validate", "--feature-dir", str(self.feature), expected=1)
        self.assertTrue(any("hash mismatch" in error for error in validation["result"]["errors"]))
        self._write("spec.md", "# Changed after corruption\n")
        blocked = self._run(
            "record-artifact", "--feature-dir", str(self.feature), "--stage", "spec", expected=2,
        )
        self.assertIn("hash mismatch", blocked["error"])

    def test_terminal_attempt_requires_explicit_restart(self) -> None:
        closed = self._run(
            "close", "--feature-dir", str(self.feature), "--result", "aborted",
            "--approval-text", "同意终止并关闭", "--message-id", "abort-message",
        )
        self.assertEqual(closed["result"]["stage_status"], "aborted")
        restarted = self._run(
            "restart-attempt", "--feature-dir", str(self.feature),
            "--approval-text", "同意重新开始重试", "--message-id", "restart-message",
        )
        self.assertEqual(restarted["result"]["attempt"], 2)
        self.assertEqual(restarted["result"]["current_stage"], "proposal-input")

    def test_historical_example_cannot_resume_progression(self) -> None:
        historical = self.repo / "sdd2-features/Sprint0/historical"
        historical.mkdir(parents=True)
        for name in (
            "brief-design.md", "proposal-input.md", "spec.md", "design.md", "tasks.md",
            "code-review-findings.md", "auto-fix-summary.md", "unit-test-summary.md", "archive.md",
        ):
            (historical / name).write_text(f"# {name}\n", encoding="utf-8")
        self._run(
            "migrate-legacy", "--feature-dir", str(historical), "--feature-id", "historical",
        )
        validation = self._run("validate", "--feature-dir", str(historical))
        self.assertIn(
            "HISTORICAL_EXAMPLE_NOT_VALID_GATE_EVIDENCE",
            validation["result"]["warnings"],
        )
        blocked = self._run(
            "record-artifact", "--feature-dir", str(historical), "--stage", "archive", expected=2,
        )
        self.assertIn("Historical examples are immutable", blocked["error"])

    def test_scope_change_invalidates_review(self) -> None:
        self._reach_tasks_approval()
        self._capture_scope()
        (self.repo / "app/src/main/java/App.java").write_text("class App { int one; }\n", encoding="utf-8")
        test = self.repo / "app/src/test/java/AppTest.java"
        test.parent.mkdir(parents=True)
        test.write_text("class AppTest {}\n", encoding="utf-8")
        self._run(
            "phase-review", "--feature-dir", str(self.feature), "--phase", "Phase1",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "通过 Phase1"
        )
        self._run("freeze-scope", "--feature-dir", str(self.feature))
        self._record("code-review-findings", "code-review-findings.md", "# Findings\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "code-review",
            "--result", "passed", "--evidence", "reviewed snapshot"
        )
        (self.repo / "app/src/main/java/App.java").write_text("class App { int two; }\n", encoding="utf-8")
        drift = self._run("validate", "--feature-dir", str(self.feature), expected=1)
        self.assertIn("IMPLEMENTATION_SCOPE_DRIFT", drift["result"]["errors"])
        self._run("freeze-scope", "--feature-dir", str(self.feature))
        state = json.loads((self.feature / ".sdd2/feature-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["quality_gates"]["code-review"]["status"], "invalidated")

        self._write("code-review-findings.md", "# Findings revision 2\n")
        review_revision_2 = self._run(
            "record-artifact", "--feature-dir", str(self.feature),
            "--stage", "code-review-findings",
        )
        self.assertEqual(
            review_revision_2["result"]["artifacts"]["code-review-findings"]["revision"], 2
        )
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "code-review",
            "--result", "passed", "--evidence", "full review of revision 2 scope",
        )
        self._record("auto-fix-summary", "auto-fix-summary.md", "# Auto-fix revision 1\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "auto-fix",
            "--result", "not-required", "--evidence", "no finding on revision 2 scope",
        )

        (self.repo / "app/src/main/java/App.java").write_text(
            "class App { int three; }\n", encoding="utf-8"
        )
        self._run("freeze-scope", "--feature-dir", str(self.feature))
        self._write("code-review-findings.md", "# Findings revision 3\n")
        self._run(
            "record-artifact", "--feature-dir", str(self.feature),
            "--stage", "code-review-findings",
        )
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "code-review",
            "--result", "passed", "--evidence", "full review of revision 3 scope",
        )
        self._write("auto-fix-summary.md", "# Auto-fix revision 2\n")
        auto_fix_revision_2 = self._run(
            "record-artifact", "--feature-dir", str(self.feature),
            "--stage", "auto-fix-summary",
        )
        self.assertEqual(
            auto_fix_revision_2["result"]["artifacts"]["auto-fix-summary"]["revision"], 2
        )

    def test_unit_test_gate_requires_changed_test_source(self) -> None:
        self._reach_tasks_approval()
        self._capture_scope()
        (self.repo / "app/src/main/java/App.java").write_text("class App { int value; }\n", encoding="utf-8")
        self._run(
            "phase-review", "--feature-dir", str(self.feature), "--phase", "Phase1",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "批准 Phase1"
        )
        self._run("freeze-scope", "--feature-dir", str(self.feature))
        self._record("code-review-findings", "code-review-findings.md", "# Findings\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "code-review",
            "--result", "passed", "--evidence", "reviewed"
        )
        self._record("auto-fix-summary", "auto-fix-summary.md", "# Auto-fix\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "auto-fix",
            "--result", "not-required", "--evidence", "none"
        )
        self._record("unit-test-summary", "unit-test-summary.md", "# Unit Test\n")
        result = self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "unit-test",
            "--result", "passed", "--evidence", "manual assertion", expected=2,
        )
        self.assertIn("changed test source", result["error"])

    def test_failed_test_cannot_archive_and_can_close_with_risk(self) -> None:
        self._reach_tasks_approval()
        self._capture_scope()
        (self.repo / "app/src/main/java/App.java").write_text("class App { int value; }\n", encoding="utf-8")
        test = self.repo / "app/src/test/java/AppTest.java"
        test.parent.mkdir(parents=True)
        test.write_text("class AppTest {}\n", encoding="utf-8")
        self._run(
            "phase-review", "--feature-dir", str(self.feature), "--phase", "Phase1",
            "--source", "user-message", "--approver-role", "human",
            "--approval-text", "批准 Phase1"
        )
        self._run("freeze-scope", "--feature-dir", str(self.feature))
        self._record("code-review-findings", "code-review-findings.md", "# Findings\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "code-review",
            "--result", "passed", "--evidence", "reviewed"
        )
        self._record("auto-fix-summary", "auto-fix-summary.md", "# Auto-fix\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "auto-fix",
            "--result", "not-required", "--evidence", "none"
        )
        self._record("unit-test-summary", "unit-test-summary.md", "# Unit Test\nFailed\n")
        self._run(
            "quality-gate", "--feature-dir", str(self.feature), "--gate", "unit-test",
            "--result", "failed", "--evidence", "test command exit code 1"
        )
        archive = self._run("archive-check", "--feature-dir", str(self.feature), expected=1)
        self.assertIn("QUALITY_GATE_NOT_PASSED:unit-test", archive["result"]["errors"])
        closed = self._run(
            "close", "--feature-dir", str(self.feature), "--result", "closed-with-risk",
            "--approval-text", "同意风险并关闭"
        )
        self.assertEqual(closed["result"]["stage_status"], "closed-with-risk")

    def test_init_rejects_english_only_brief(self) -> None:
        self._run(
            "close", "--feature-dir", str(self.feature), "--result", "aborted",
            "--approval-text", "同意终止当前功能", "--message-id", "close-before-language-test",
        )
        english_feature = self.repo / "sdd2-features/Sprint1/english-brief"
        english_feature.mkdir(parents=True)
        (english_feature / "brief-design.md").write_text(
            "# Brief Design\n\nAdd a new response field to the existing policy information API.\n",
            encoding="utf-8",
        )
        result = self._run(
            "init", "--feature-dir", str(english_feature), "--feature-id", "english-brief",
            expected=2,
        )
        self.assertIn("ARTIFACT_LANGUAGE_NOT_SIMPLIFIED_CHINESE", result["error"])
        self.assertFalse((english_feature / ".sdd2/feature-state.json").exists())
        self.assertFalse((self.repo / ".git/sdd2-active-feature.json").exists())

    def test_record_artifact_rejects_english_only_body(self) -> None:
        (self.feature / "proposal-input.md").write_text(
            "# Proposal Input\n\nThis document defines the feature scope, behavior, risks, and acceptance outcomes.\n",
            encoding="utf-8",
        )
        result = self._run(
            "record-artifact", "--feature-dir", str(self.feature), "--stage", "proposal-input",
            expected=2,
        )
        self.assertIn("ARTIFACT_LANGUAGE_NOT_SIMPLIFIED_CHINESE", result["error"])
        state = json.loads((self.feature / ".sdd2/feature-state.json").read_text(encoding="utf-8"))
        self.assertNotIn("proposal-input", state["artifacts"])
        self.assertFalse((self.feature / ".sdd2/revisions/proposal-input").exists())

    def test_record_artifact_accepts_chinese_body_with_technical_terms(self) -> None:
        (self.feature / "proposal-input.md").write_text(
            "# Proposal 输入\n\n本功能在现有 PolicyInfoController 中新增 `summary` 字段，"
            "保持 HTTP API、DTO 和兼容行为不变，并补充对应 JUnit 测试。\n",
            encoding="utf-8",
        )
        result = self._run(
            "record-artifact", "--feature-dir", str(self.feature), "--stage", "proposal-input",
        )
        self.assertEqual(result["result"]["current_stage"], "spec")

    def test_record_artifact_rejects_traditional_chinese_body(self) -> None:
        (self.feature / "proposal-input.md").write_text(
            "# Proposal 輸入\n\n這個功能將更新現有 API，並記錄完整的測試與驗證結果。\n",
            encoding="utf-8",
        )
        result = self._run(
            "record-artifact", "--feature-dir", str(self.feature), "--stage", "proposal-input",
            expected=2,
        )
        self.assertIn("TRADITIONAL_CHINESE_DETECTED", result["error"])
        state = json.loads((self.feature / ".sdd2/feature-state.json").read_text(encoding="utf-8"))
        self.assertNotIn("proposal-input", state["artifacts"])
        self.assertFalse((self.feature / ".sdd2/revisions/proposal-input").exists())


if __name__ == "__main__":
    unittest.main()
