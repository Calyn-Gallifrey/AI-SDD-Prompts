#!/usr/bin/env python3
"""Deterministic process control for UAW-SDD 2.0.

The user-facing entry remains a brief prompt plus a Skill invocation. The Skill
calls this CLI internally to persist state, approvals, scope, and gate evidence.
Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "2.0.0"
CONTROL_DIR = ".sdd2"
STATE_FILE = "feature-state.json"
APPROVAL_FILE = "gate-approvals.jsonl"
EVENT_FILE = "events.jsonl"
SCOPE_FILE = "implementation-scope.json"
ARCHIVE_EVIDENCE_FILE = "archive-evidence.json"
REVISION_DIR = "revisions"

ARTIFACT_FILES = {
    "brief-design": "brief-design.md",
    "proposal-input": "proposal-input.md",
    "spec": "spec.md",
    "design": "design.md",
    "tasks": "tasks.md",
    "code-review-findings": "code-review-findings.md",
    "auto-fix-summary": "auto-fix-summary.md",
    "unit-test-summary": "unit-test-summary.md",
    "archive": "archive.md",
}

STAGE_ORDER = [
    "brief-design",
    "proposal-input",
    "spec",
    "design",
    "tasks",
    "implementation",
    "code-review",
    "auto-fix",
    "unit-test-summary",
    "archive",
]

APPROVAL_STAGES = {"spec", "design", "tasks", "unit-test-summary", "archive"}
QUALITY_GATES = {"code-review", "auto-fix", "unit-test"}
TERMINAL_STATUSES = {"completed", "closed-with-risk", "aborted", "superseded"}
PASS_WORDS = ("批准", "通过", "同意", "approve", "approved", "accept")
STAGE_WORDS = {
    "spec": ("spec", "需求规格", "需求"),
    "design": ("design", "设计"),
    "tasks": ("tasks", "任务"),
    "unit-test-summary": ("unit test summary", "unit-test-summary", "单元测试总结", "测试总结"),
    "archive": ("archive", "归档"),
}
APPROVAL_PATTERN = re.compile(r"(?:批准|通过|同意|\bapprove(?:d)?\b|\baccept(?:ed)?\b)", re.IGNORECASE)
APPROVAL_REJECTION_TERMS = (
    "不批准",
    "未批准",
    "不同意",
    "不通过",
    "未通过",
    "驳回",
    "不代表",
    "不是批准",
    "not approve",
    "not approved",
    "do not approve",
    "disapprove",
    "reject",
)
APPROVAL_META_TERMS = (
    "文档中",
    "文件中",
    "示例",
    "历史",
    "引用",
    "document says",
    "file says",
    "example",
    "historical",
    "quoted",
)
DEMO_TERMS = ("demo", "simulation", "simulate", "模拟", "演练", "预演")
DEMO_ACTION_TERMS = (
    "批准", "同意", "授权", "请", "运行", "进行", "做", "开始",
    "approve", "authorize", "run", "start",
)
DEMO_REJECTION_TERMS = APPROVAL_REJECTION_TERMS + (
    "不要", "不做", "不用", "无需", "不需要", "别做", "别运行", "别进行",
    "取消", "停止", "do not", "don't", "dont", "no demo", "without demo", "cancel", "stop",
)

DEFAULT_TEST_PATHS = (
    "**/src/test/**",
    "**/test/**",
    "**/tests/**",
    "**/*Test.java",
    "**/*Tests.java",
    "**/*Spec.java",
)


class ControlError(RuntimeError):
    """A deterministic control failure that must block workflow progress."""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    if not path.is_file():
        raise ControlError(f"Required file does not exist: {path}")
    return sha256_bytes(path.read_bytes())


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def atomic_write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(value)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ControlError(f"Missing control file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ControlError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ControlError(f"Expected JSON object in {path}")
    return value


def run_git(repo_root: Path, *args: str, check: bool = True) -> str:
    process = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if check and process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip()
        raise ControlError(f"Git command failed ({' '.join(args)}): {detail}")
    return process.stdout.strip()


def git_root(path: Path) -> Path:
    root = run_git(path, "rev-parse", "--show-toplevel")
    return Path(root).resolve()


def git_path(repo_root: Path, name: str) -> Path:
    value = run_git(repo_root, "rev-parse", "--git-path", name)
    path = Path(value)
    return path if path.is_absolute() else (repo_root / path).resolve()


def repository_id(repo_root: Path) -> str:
    roots = sorted(run_git(repo_root, "rev-list", "--max-parents=0", "HEAD").splitlines())
    if not roots:
        raise ControlError("Cannot identify Git repository root commit")
    return sha256_bytes(canonical_json({"root_commits": roots}).encode("utf-8"))


def state_repo_root(feature_dir: Path, state: dict[str, Any]) -> Path:
    repo_root = git_root(feature_dir)
    expected = state.get("workspace_binding", {}).get("repository_id")
    if expected and expected != repository_id(repo_root):
        raise ControlError("Feature state belongs to a different Git repository")
    return repo_root


def scope_repo_root(feature_dir: Path, scope: dict[str, Any]) -> Path:
    repo_root = git_root(feature_dir)
    expected = scope.get("repository_id")
    if expected and expected != repository_id(repo_root):
        raise ControlError("Implementation scope belongs to a different Git repository")
    return repo_root


def feature_paths(feature_dir: Path) -> dict[str, Path]:
    control = feature_dir / CONTROL_DIR
    return {
        "control": control,
        "state": control / STATE_FILE,
        "approvals": control / APPROVAL_FILE,
        "events": control / EVENT_FILE,
        "scope": control / SCOPE_FILE,
        "archive_evidence": control / ARCHIVE_EVIDENCE_FILE,
        "revisions": control / REVISION_DIR,
    }


def normalize_feature_dir(value: str | Path) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_dir():
        raise ControlError(f"Feature directory does not exist: {path}")
    return path


def load_state(feature_dir: Path) -> dict[str, Any]:
    state = read_json(feature_paths(feature_dir)["state"])
    if state.get("schema_version") != SCHEMA_VERSION:
        raise ControlError(
            f"Unsupported state schema: {state.get('schema_version')!r}; expected {SCHEMA_VERSION}"
        )
    repo_root = git_root(feature_dir)
    expected = feature_dir.relative_to(repo_root).as_posix()
    if state.get("feature_dir") != expected:
        raise ControlError(
            f"Feature directory binding mismatch: state={state.get('feature_dir')!r}, actual={expected!r}"
        )
    state_repo_root(feature_dir, state)
    return state


def save_state(feature_dir: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    atomic_write_json(feature_paths(feature_dir)["state"], state)


def persist_artifact_snapshot(
    feature_dir: Path,
    stage: str,
    revision: int,
    digest: str,
) -> str:
    source = feature_dir / ARTIFACT_FILES[stage]
    destination = feature_paths(feature_dir)["revisions"] / stage / f"r{revision:04d}-{digest}.md"
    content = source.read_bytes()
    if sha256_bytes(content) != digest:
        raise ControlError(f"Artifact changed while snapshotting: {source}")
    if destination.exists():
        if sha256_file(destination) != digest:
            raise ControlError(f"Immutable artifact snapshot collision: {destination}")
    else:
        atomic_write_bytes(destination, content)
    return destination.relative_to(feature_dir).as_posix()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ControlError(f"Invalid JSONL at {path}:{number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ControlError(f"Expected JSON object at {path}:{number}")
        records.append(value)
    return records


def validate_hash_chain(path: Path, hash_field: str) -> list[str]:
    errors: list[str] = []
    previous = None
    for index, record in enumerate(read_jsonl(path), 1):
        actual = record.get(hash_field)
        body = dict(record)
        body.pop(hash_field, None)
        expected = sha256_bytes(canonical_json(body).encode("utf-8"))
        if actual != expected:
            errors.append(f"{path.name}:{index} hash mismatch")
        if body.get("previous_hash") != previous:
            errors.append(f"{path.name}:{index} previous_hash mismatch")
        previous = actual
    return errors


def append_chained_record(path: Path, record: dict[str, Any], hash_field: str) -> dict[str, Any]:
    existing = read_jsonl(path)
    record = dict(record)
    record["previous_hash"] = existing[-1].get(hash_field) if existing else None
    record[hash_field] = sha256_bytes(canonical_json(record).encode("utf-8"))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(record) + "\n")
    return record


def append_event(feature_dir: Path, state: dict[str, Any], event_type: str, payload: dict[str, Any]) -> None:
    append_chained_record(
        feature_paths(feature_dir)["events"],
        {
            "event_id": str(uuid.uuid4()),
            "timestamp": utc_now(),
            "event_type": event_type,
            "feature_id": state["feature_id"],
            "attempt": state["attempt"],
            "revision": state["revision"],
            "payload": payload,
        },
        "event_hash",
    )


def lock_path(repo_root: Path) -> Path:
    return git_path(repo_root, "sdd2-active-feature.json")


def acquire_lock(repo_root: Path, feature_dir: Path, feature_id: str) -> None:
    path = lock_path(repo_root)
    feature_repo_path = feature_dir.relative_to(repo_root).as_posix()
    if path.exists():
        current = read_json(path)
        if current.get("feature_dir") != feature_repo_path:
            raise ControlError(
                "This Git worktree is locked by another SDD2 feature: "
                f"{current.get('feature_id')} at {current.get('feature_dir')}. "
                "Use a separate Git worktree for parallel features."
            )
        return
    atomic_write_json(
        path,
        {
            "schema_version": SCHEMA_VERSION,
            "feature_id": feature_id,
            "feature_dir": feature_repo_path,
            "repository_id": repository_id(repo_root),
            "acquired_at": utc_now(),
        },
    )


def release_lock(repo_root: Path, feature_dir: Path, feature_id: str) -> None:
    path = lock_path(repo_root)
    if not path.exists():
        return
    current = read_json(path)
    feature_repo_path = feature_dir.relative_to(repo_root).as_posix()
    if current.get("feature_dir") != feature_repo_path or current.get("feature_id") != feature_id:
        raise ControlError("Cannot release a worktree lock owned by another SDD2 feature")
    path.unlink()


def verify_lock(feature_dir: Path, state: dict[str, Any]) -> list[str]:
    if state.get("execution_mode") == "historical-example" or state.get("stage_status") in TERMINAL_STATUSES:
        return []
    repo_root = state_repo_root(feature_dir, state)
    path = lock_path(repo_root)
    if not path.exists():
        return ["FEATURE_LOCK_MISSING"]
    current = read_json(path)
    if current.get("feature_dir") != state["feature_dir"]:
        return ["FEATURE_LOCK_MISMATCH"]
    if current.get("feature_id") != state["feature_id"]:
        return ["FEATURE_LOCK_ID_MISMATCH"]
    if current.get("repository_id") != repository_id(repo_root):
        return ["FEATURE_LOCK_REPOSITORY_MISMATCH"]
    return []


def artifact_key_for_stage(stage: str) -> str:
    if stage not in ARTIFACT_FILES:
        raise ControlError(f"Unknown artifact stage: {stage}")
    return stage


def stage_index(stage: str) -> int:
    normalized = "unit-test-summary" if stage == "unit-test" else stage
    try:
        return STAGE_ORDER.index(normalized)
    except ValueError as exc:
        raise ControlError(f"Unknown workflow stage: {stage}") from exc


def invalidate_from(
    state: dict[str, Any],
    changed_stage: str,
    reason: str,
) -> list[str]:
    changed_index = stage_index(changed_stage)
    invalidated: list[str] = []
    for stage, approval in state.get("approvals", {}).items():
        if approval.get("status") == "approved" and stage_index(stage) >= changed_index:
            approval["status"] = "invalidated"
            approval["invalidated_reason"] = reason
            invalidated.append(f"approval:{stage}")
    gate_stage = {"code-review": "code-review", "auto-fix": "auto-fix", "unit-test": "unit-test-summary"}
    for gate, result in state.get("quality_gates", {}).items():
        if result.get("status") not in {"invalidated", "not-recorded"} and stage_index(gate_stage[gate]) >= changed_index:
            result["status"] = "invalidated"
            result["invalidated_reason"] = reason
            invalidated.append(f"quality:{gate}")
    for phase, review in state.get("phase_reviews", {}).items():
        if changed_index <= stage_index("tasks") and review.get("status") == "approved":
            review["status"] = "invalidated"
            review["invalidated_reason"] = reason
            invalidated.append(f"phase:{phase}")
    if invalidated:
        state.setdefault("invalidations", []).append(
            {
                "timestamp": utc_now(),
                "changed_stage": changed_stage,
                "reason": reason,
                "invalidated": invalidated,
            }
        )
    return invalidated


def direct_approval(text: str, stage_terms: Iterable[str]) -> bool:
    lowered = text.strip().lower()
    if any(term in lowered for term in APPROVAL_REJECTION_TERMS + APPROVAL_META_TERMS):
        return False
    return bool(APPROVAL_PATTERN.search(lowered)) and any(term.lower() in lowered for term in stage_terms)


def explicit_approval(stage: str, text: str) -> bool:
    return direct_approval(text, STAGE_WORDS[stage])


def unique_in_order(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def current_artifact_hash(feature_dir: Path, stage: str) -> str:
    filename = ARTIFACT_FILES[artifact_key_for_stage(stage)]
    return sha256_file(feature_dir / filename)


def artifact_drift(feature_dir: Path, state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for stage, record in state.get("artifacts", {}).items():
        path = feature_dir / record["path"]
        if not path.is_file():
            errors.append(f"ARTIFACT_MISSING:{stage}:{record['path']}")
            continue
        actual = sha256_file(path)
        if actual != record.get("sha256"):
            errors.append(f"ARTIFACT_DRIFT:{stage}:{record['path']}")
        snapshot_path = record.get("snapshot_path")
        if not snapshot_path:
            if state.get("execution_mode") != "historical-example":
                errors.append(f"ARTIFACT_SNAPSHOT_MISSING:{stage}")
            continue
        snapshot = feature_dir / snapshot_path
        if not snapshot.is_file():
            errors.append(f"ARTIFACT_SNAPSHOT_FILE_MISSING:{stage}:{snapshot_path}")
        elif sha256_file(snapshot) != record.get("sha256"):
            errors.append(f"ARTIFACT_SNAPSHOT_DRIFT:{stage}:{snapshot_path}")
    return errors


def changed_paths(repo_root: Path, base_commit: str) -> list[str]:
    tracked = run_git(repo_root, "diff", "--name-only", "-z", base_commit)
    untracked = run_git(repo_root, "ls-files", "--others", "--exclude-standard", "-z")
    paths = {value for value in tracked.split("\0") if value}
    paths.update(value for value in untracked.split("\0") if value)
    return sorted(paths)


def path_matches(path: str, patterns: Iterable[str]) -> bool:
    return any(path == pattern or fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def reject_unsafe_patterns(patterns: Iterable[str]) -> None:
    unsafe = {"", ".", "./", "*", "**", "**/*", "/"}
    bad = [pattern for pattern in patterns if pattern.strip() in unsafe or Path(pattern).is_absolute()]
    if bad:
        raise ControlError(f"Unsafe or overly broad scope pattern(s): {', '.join(bad)}")


def snapshot_for_scope(repo_root: Path, scope: dict[str, Any]) -> dict[str, Any]:
    base_commit = scope["base_commit"]
    feature_prefix = scope["feature_repo_path"].rstrip("/") + "/"
    files: list[dict[str, str]] = []
    violations: list[str] = []
    current_branch = run_git(repo_root, "branch", "--show-current")
    if current_branch != scope["branch"]:
        violations.append(f"BRANCH_MISMATCH:{current_branch or '<detached>'}")
    for relative in changed_paths(repo_root, base_commit):
        if relative == scope["feature_repo_path"] or relative.startswith(feature_prefix):
            continue
        if path_matches(relative, scope.get("forbidden_paths", [])):
            violations.append(f"FORBIDDEN_PATH:{relative}")
            continue
        if not path_matches(relative, scope["allowed_paths"]):
            violations.append(f"OUT_OF_SCOPE:{relative}")
            continue
        path = repo_root / relative
        digest = sha256_file(path) if path.is_file() else "<deleted>"
        files.append({"path": relative, "sha256": digest})
    payload = {
        "base_commit": base_commit,
        "branch": scope["branch"],
        "head_commit": run_git(repo_root, "rev-parse", "HEAD"),
        "head_tree": run_git(repo_root, "rev-parse", "HEAD^{tree}"),
        "files": files,
    }
    return {
        "captured_at": utc_now(),
        "files": files,
        "head_commit": payload["head_commit"],
        "head_tree": payload["head_tree"],
        "snapshot_sha256": sha256_bytes(canonical_json(payload).encode("utf-8")),
        "violations": violations,
    }


def changed_test_paths(scope: dict[str, Any], snapshot: dict[str, Any]) -> list[str]:
    patterns = scope.get("test_path_patterns") or list(DEFAULT_TEST_PATHS)
    return sorted(
        item["path"] for item in snapshot.get("files", []) if path_matches(item["path"], patterns)
    )


def load_scope(feature_dir: Path) -> dict[str, Any]:
    return read_json(feature_paths(feature_dir)["scope"])


def scope_drift(feature_dir: Path, state: dict[str, Any]) -> list[str]:
    scope_path = feature_paths(feature_dir)["scope"]
    if not scope_path.exists():
        if stage_index(state["current_stage"]) >= stage_index("implementation"):
            return ["SCOPE_MANIFEST_MISSING"]
        return []
    scope = load_scope(feature_dir)
    snapshot = snapshot_for_scope(scope_repo_root(feature_dir, scope), scope)
    if snapshot["violations"]:
        return snapshot["violations"]
    frozen = scope.get("frozen_snapshot")
    if frozen and frozen.get("snapshot_sha256") != snapshot["snapshot_sha256"]:
        return ["IMPLEMENTATION_SCOPE_DRIFT"]
    return []


def approval_errors(feature_dir: Path, state: dict[str, Any], stage: str) -> list[str]:
    approval = state.get("approvals", {}).get(stage)
    artifact = state.get("artifacts", {}).get(stage)
    if not approval or approval.get("status") != "approved":
        return [f"APPROVAL_MISSING_OR_INVALID:{stage}"]
    if not artifact:
        return [f"APPROVED_ARTIFACT_MISSING:{stage}"]
    errors = []
    if approval.get("attempt") != state.get("attempt"):
        errors.append(f"APPROVAL_ATTEMPT_MISMATCH:{stage}")
    if approval.get("artifact_sha256") != artifact.get("sha256"):
        errors.append(f"APPROVAL_HASH_MISMATCH:{stage}")
    if approval.get("artifact_revision") != artifact.get("revision"):
        errors.append(f"APPROVAL_REVISION_MISMATCH:{stage}")
    actual = current_artifact_hash(feature_dir, stage)
    if actual != approval.get("artifact_sha256"):
        errors.append(f"APPROVAL_ARTIFACT_DRIFT:{stage}")
    return errors


def quality_gate_errors(feature_dir: Path, state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scope = load_scope(feature_dir)
    current = snapshot_for_scope(scope_repo_root(feature_dir, scope), scope)
    if current["violations"]:
        errors.extend(current["violations"])
        return errors
    current_sha = current["snapshot_sha256"]
    accepted = {
        "code-review": {"passed"},
        "auto-fix": {"passed", "not-required"},
        "unit-test": {"passed"},
    }
    for gate, allowed in accepted.items():
        record = state.get("quality_gates", {}).get(gate)
        if not record or record.get("status") not in allowed:
            errors.append(f"QUALITY_GATE_NOT_PASSED:{gate}")
            continue
        if record.get("scope_sha256") != current_sha:
            errors.append(f"QUALITY_GATE_SCOPE_MISMATCH:{gate}")
        artifact_stage = {
            "code-review": "code-review-findings",
            "auto-fix": "auto-fix-summary",
            "unit-test": "unit-test-summary",
        }[gate]
        artifact = state.get("artifacts", {}).get(artifact_stage)
        if not artifact or record.get("artifact_sha256") != artifact.get("sha256"):
            errors.append(f"QUALITY_GATE_ARTIFACT_MISMATCH:{gate}")
        elif artifact.get("scope_sha256") != current_sha:
            errors.append(f"QUALITY_GATE_ARTIFACT_SCOPE_MISMATCH:{gate}")
    return errors


def archive_evidence_errors(feature_dir: Path, state: dict[str, Any]) -> list[str]:
    path = feature_paths(feature_dir)["archive_evidence"]
    if not path.is_file():
        return ["ARCHIVE_EVIDENCE_MISSING"]
    evidence = read_json(path)
    scope = load_scope(feature_dir)
    frozen = scope.get("frozen_snapshot") or {}
    errors: list[str] = []
    expected = {
        "feature_id": state["feature_id"],
        "attempt": state["attempt"],
        "base_commit": scope.get("base_commit"),
        "head_commit": frozen.get("head_commit"),
        "head_tree": frozen.get("head_tree"),
        "scope_sha256": frozen.get("snapshot_sha256"),
    }
    for key, value in expected.items():
        if evidence.get(key) != value:
            errors.append(f"ARCHIVE_EVIDENCE_MISMATCH:{key}")
    if evidence.get("files") != frozen.get("files"):
        errors.append("ARCHIVE_EVIDENCE_MISMATCH:files")
    if evidence.get("evidence_sha256") != sha256_bytes(
        canonical_json({key: value for key, value in evidence.items() if key != "evidence_sha256"}).encode("utf-8")
    ):
        errors.append("ARCHIVE_EVIDENCE_HASH_MISMATCH")
    return errors


def archive_errors(feature_dir: Path, state: dict[str, Any], require_archive: bool) -> list[str]:
    errors: list[str] = []
    errors.extend(verify_lock(feature_dir, state))
    errors.extend(validate_hash_chain(feature_paths(feature_dir)["events"], "event_hash"))
    errors.extend(validate_hash_chain(feature_paths(feature_dir)["approvals"], "record_hash"))
    errors.extend(artifact_drift(feature_dir, state))
    for stage in ("spec", "design", "tasks", "unit-test-summary"):
        errors.extend(approval_errors(feature_dir, state, stage))
    for phase in state.get("required_phases", []):
        record = state.get("phase_reviews", {}).get(phase)
        if not record or record.get("status") != "approved":
            errors.append(f"PHASE_REVIEW_NOT_APPROVED:{phase}")
    if not feature_paths(feature_dir)["scope"].exists():
        errors.append("SCOPE_MANIFEST_MISSING")
    else:
        errors.extend(quality_gate_errors(feature_dir, state))
        errors.extend(archive_evidence_errors(feature_dir, state))
    required = list(ARTIFACT_FILES)
    if not require_archive:
        required.remove("archive")
    for stage in required:
        if stage not in state.get("artifacts", {}):
            errors.append(f"ARTIFACT_NOT_RECORDED:{stage}")
    if state.get("blocked"):
        errors.append("FEATURE_BLOCKED")
    return sorted(set(errors))


def validate_state(feature_dir: Path, state: dict[str, Any]) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required = {
        "schema_version",
        "feature_id",
        "feature_dir",
        "execution_mode",
        "entry_contract",
        "revision",
        "attempt",
        "current_stage",
        "stage_status",
        "artifacts",
        "approvals",
        "quality_gates",
        "phase_reviews",
        "next_required_action",
    }
    missing = sorted(required - set(state))
    errors.extend(f"STATE_FIELD_MISSING:{name}" for name in missing)
    if state.get("entry_contract", {}).get("user_entry") != "brief-prompt-and-skill-call":
        errors.append("USER_ENTRY_CONTRACT_CHANGED")
    if state.get("entry_contract", {}).get("developer_action_required") is not False:
        errors.append("USER_ENTRY_REQUIRES_NEW_ACTION")
    if state.get("current_stage") not in STAGE_ORDER:
        errors.append("INVALID_CURRENT_STAGE")
    errors.extend(verify_lock(feature_dir, state))
    errors.extend(artifact_drift(feature_dir, state))
    errors.extend(validate_hash_chain(feature_paths(feature_dir)["events"], "event_hash"))
    errors.extend(validate_hash_chain(feature_paths(feature_dir)["approvals"], "record_hash"))
    if state.get("execution_mode") != "historical-example":
        errors.extend(scope_drift(feature_dir, state))
    else:
        warnings.append("HISTORICAL_EXAMPLE_NOT_VALID_GATE_EVIDENCE")
    return {"errors": sorted(set(errors)), "warnings": sorted(set(warnings))}


def assert_control_integrity(
    feature_dir: Path,
    state: dict[str, Any],
    *,
    ignore_artifact_stage: str | None = None,
    allow_scope_drift: bool = False,
) -> None:
    errors: list[str] = []
    errors.extend(verify_lock(feature_dir, state))
    errors.extend(validate_hash_chain(feature_paths(feature_dir)["events"], "event_hash"))
    errors.extend(validate_hash_chain(feature_paths(feature_dir)["approvals"], "record_hash"))
    for error in artifact_drift(feature_dir, state):
        if ignore_artifact_stage and error.startswith((f"ARTIFACT_DRIFT:{ignore_artifact_stage}:", f"ARTIFACT_MISSING:{ignore_artifact_stage}:")):
            continue
        errors.append(error)
    if not allow_scope_drift and state.get("execution_mode") != "historical-example":
        errors.extend(scope_drift(feature_dir, state))
    if errors:
        raise ControlError("Control integrity check failed: " + ", ".join(sorted(set(errors))))


def assert_history_and_lock(feature_dir: Path, state: dict[str, Any]) -> None:
    errors = verify_lock(feature_dir, state)
    errors.extend(validate_hash_chain(feature_paths(feature_dir)["events"], "event_hash"))
    errors.extend(validate_hash_chain(feature_paths(feature_dir)["approvals"], "record_hash"))
    if errors:
        raise ControlError("Control history check failed: " + ", ".join(sorted(set(errors))))


def assert_artifact_entry(
    feature_dir: Path,
    state: dict[str, Any],
    stage: str,
    previous: dict[str, Any] | None,
) -> None:
    revisable_planning = {"brief-design", "proposal-input", "spec", "design", "tasks"}
    if previous and stage in revisable_planning:
        return
    expected_stage = {
        "proposal-input": "proposal-input",
        "spec": "spec",
        "design": "design",
        "tasks": "tasks",
        "code-review-findings": "code-review",
        "auto-fix-summary": "auto-fix",
        "unit-test-summary": "unit-test-summary",
        "archive": "archive",
    }.get(stage)
    if expected_stage and state.get("current_stage") != expected_stage:
        raise ControlError(
            f"Cannot record {stage} while current_stage={state.get('current_stage')}; expected {expected_stage}"
        )
    if stage == "proposal-input" and "brief-design" not in state["artifacts"]:
        raise ControlError("proposal-input requires recorded brief-design")
    if stage == "spec" and "proposal-input" not in state["artifacts"]:
        raise ControlError("spec requires recorded proposal-input")
    if stage == "design":
        errors = approval_errors(feature_dir, state, "spec")
        if errors:
            raise ControlError("design requires current Spec approval: " + ", ".join(errors))
    if stage == "tasks":
        errors = approval_errors(feature_dir, state, "design")
        if errors:
            raise ControlError("tasks requires current Design approval: " + ", ".join(errors))
    if stage == "code-review-findings":
        errors = approval_errors(feature_dir, state, "tasks")
        for phase in state.get("required_phases", []):
            review = state.get("phase_reviews", {}).get(phase)
            if not review or review.get("status") != "approved":
                errors.append(f"PHASE_REVIEW_NOT_APPROVED:{phase}")
        require_current_scope(feature_dir, state)
        if errors:
            raise ControlError("Code Review findings entry blocked: " + ", ".join(errors))
    if stage == "auto-fix-summary":
        review = state.get("quality_gates", {}).get("code-review")
        if not review or review.get("status") not in {"passed", "failed"}:
            raise ControlError("Auto-fix summary requires a completed Code Review result")
    if stage == "unit-test-summary":
        errors = quality_gate_errors(feature_dir, state)
        errors = [error for error in errors if error != "QUALITY_GATE_NOT_PASSED:unit-test"]
        if errors:
            raise ControlError("Unit Test Summary entry blocked: " + ", ".join(errors))
    if stage == "archive":
        errors = archive_evidence_errors(feature_dir, state)
        if errors:
            raise ControlError("Archive entry blocked: " + ", ".join(errors))


def cmd_init(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    paths = feature_paths(feature_dir)
    if paths["state"].exists():
        raise ControlError(f"Feature is already initialized: {paths['state']}")
    brief = feature_dir / ARTIFACT_FILES["brief-design"]
    if not brief.is_file():
        raise ControlError("brief-design.md must be persisted before SDD2 initialization")
    repo_root = git_root(feature_dir)
    feature_repo_path = feature_dir.relative_to(repo_root).as_posix()
    branch = run_git(repo_root, "branch", "--show-current")
    if not branch:
        raise ControlError("Detached HEAD is not allowed for an active SDD2 feature")
    acquire_lock(repo_root, feature_dir, args.feature_id)
    brief_digest = sha256_file(brief)
    brief_snapshot = persist_artifact_snapshot(feature_dir, "brief-design", 1, brief_digest)
    state: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": args.feature_id,
        "feature_dir": feature_repo_path,
        "feature_repo_path": feature_repo_path,
        "execution_mode": args.mode,
        "entry_contract": {
            "user_entry": "brief-prompt-and-skill-call",
            "developer_action_required": False,
            "version": 1,
        },
        "workspace_binding": {
            "repo_root": ".",
            "worktree": ".",
            "repository_id": repository_id(repo_root),
            "branch": branch,
        },
        "revision": 1,
        "attempt": 1,
        "current_stage": "proposal-input",
        "stage_status": "ready",
        "last_completed_stage": "brief-design",
        "next_required_action": "assemble-proposal-input",
        "blocked": None,
        "artifacts": {
            "brief-design": {
                "path": ARTIFACT_FILES["brief-design"],
                "revision": 1,
                "sha256": brief_digest,
                "snapshot_path": brief_snapshot,
                "status": "recorded",
                "recorded_at": utc_now(),
            }
        },
        "approvals": {},
        "quality_gates": {},
        "required_phases": [],
        "phase_reviews": {},
        "invalidations": [],
        "demo_authorization": None,
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    paths["control"].mkdir(parents=True, exist_ok=True)
    paths["approvals"].touch()
    paths["events"].touch()
    save_state(feature_dir, state)
    append_event(feature_dir, state, "feature-initialized", {"mode": args.mode})
    return state


def cmd_migrate_legacy(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    paths = feature_paths(feature_dir)
    if paths["state"].exists():
        raise ControlError("Legacy feature already has control state")
    repo_root = git_root(feature_dir)
    artifacts: dict[str, Any] = {}
    for stage, filename in ARTIFACT_FILES.items():
        path = feature_dir / filename
        if path.is_file():
            digest = sha256_file(path)
            artifacts[stage] = {
                "path": filename,
                "revision": 1,
                "sha256": digest,
                "snapshot_path": persist_artifact_snapshot(feature_dir, stage, 1, digest),
                "status": "historical-record",
                "recorded_at": utc_now(),
            }
    state = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": args.feature_id,
        "feature_dir": feature_dir.relative_to(repo_root).as_posix(),
        "feature_repo_path": feature_dir.relative_to(repo_root).as_posix(),
        "execution_mode": "historical-example",
        "entry_contract": {
            "user_entry": "brief-prompt-and-skill-call",
            "developer_action_required": False,
            "version": 1,
        },
        "workspace_binding": {
            "repo_root": ".",
            "worktree": ".",
            "repository_id": repository_id(repo_root),
            "branch": run_git(repo_root, "branch", "--show-current"),
        },
        "revision": 1,
        "attempt": 1,
        "current_stage": "archive",
        "stage_status": "superseded",
        "last_completed_stage": None,
        "next_required_action": "none-historical-example",
        "blocked": {
            "code": "LEGACY_APPROVAL_EVIDENCE_UNVERIFIED",
            "reason": "Historical AI review records are not valid human approvals.",
            "recovery": "Run a new SDD2 attempt from a current brief; do not resume this example.",
        },
        "artifacts": artifacts,
        "approvals": {},
        "quality_gates": {},
        "required_phases": [],
        "phase_reviews": {},
        "invalidations": [],
        "demo_authorization": None,
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    paths["control"].mkdir(parents=True, exist_ok=True)
    paths["approvals"].touch()
    paths["events"].touch()
    save_state(feature_dir, state)
    append_event(feature_dir, state, "legacy-example-quarantined", {"reason": state["blocked"]["code"]})
    return state


def cmd_authorize_demo(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    if state["execution_mode"] != "demo":
        raise ControlError("Demo authorization is only valid when execution_mode=demo")
    assert_control_integrity(feature_dir, state)
    lowered = args.authorization_text.lower()
    if (
        not any(term in lowered for term in DEMO_TERMS)
        or any(term in lowered for term in DEMO_REJECTION_TERMS)
        or not any(term in lowered for term in DEMO_ACTION_TERMS)
    ):
        raise ControlError("Demo authorization text must explicitly identify a demo/simulation")
    state["demo_authorization"] = {
        "source": "user-message",
        "message_id": args.message_id,
        "authorization_text": args.authorization_text,
        "authorized_at": utc_now(),
    }
    state["revision"] += 1
    append_event(feature_dir, state, "demo-authorized", dict(state["demo_authorization"]))
    save_state(feature_dir, state)
    return state


def cmd_record_artifact(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    if state["execution_mode"] == "historical-example":
        raise ControlError("Historical examples are immutable and cannot progress")
    stage = artifact_key_for_stage(args.stage)
    if state["stage_status"] in TERMINAL_STATUSES:
        raise ControlError("Terminal SDD2 attempts are immutable; restart a new attempt explicitly")
    assert_control_integrity(
        feature_dir,
        state,
        ignore_artifact_stage=stage,
        allow_scope_drift=True,
    )
    path = feature_dir / ARTIFACT_FILES[stage]
    digest = sha256_file(path)
    previous = state["artifacts"].get(stage)
    scope_sha256: str | None = None
    if stage in {"code-review-findings", "auto-fix-summary", "unit-test-summary", "archive"}:
        _, current_snapshot = require_current_scope(feature_dir, state)
        scope_sha256 = current_snapshot["snapshot_sha256"]
    if previous and previous.get("sha256") == digest:
        if scope_sha256 and previous.get("scope_sha256") != scope_sha256:
            raise ControlError(
                f"{stage} still describes an older implementation scope; update the artifact for the current scope"
            )
        return state
    assert_artifact_entry(feature_dir, state, stage, previous)
    revision = (previous or {}).get("revision", 0) + 1
    snapshot_path = persist_artifact_snapshot(feature_dir, stage, revision, digest)
    state["revision"] += 1
    invalidated: list[str] = []
    if previous:
        invalidated = invalidate_from(
            state,
            stage,
            f"{stage} changed from revision {previous['revision']} to {revision}",
        )
    artifact_record: dict[str, Any] = {
        "path": ARTIFACT_FILES[stage],
        "revision": revision,
        "sha256": digest,
        "snapshot_path": snapshot_path,
        "status": "recorded",
        "recorded_at": utc_now(),
    }
    if scope_sha256:
        artifact_record["scope_sha256"] = scope_sha256
    state["artifacts"][stage] = artifact_record
    next_actions = {
        "brief-design": ("proposal-input", "ready", "assemble-proposal-input"),
        "proposal-input": ("spec", "ready", "generate-spec"),
        "spec": ("spec", "awaiting-approval", "request-spec-approval"),
        "design": ("design", "awaiting-approval", "request-design-approval"),
        "tasks": ("tasks", "awaiting-approval", "request-tasks-approval"),
        "code-review-findings": ("code-review", "recorded", "record-code-review-gate"),
        "auto-fix-summary": ("auto-fix", "recorded", "record-auto-fix-gate"),
        "unit-test-summary": ("unit-test-summary", "recorded", "record-unit-test-gate"),
        "archive": ("archive", "awaiting-final-approval", "request-archive-approval"),
    }
    current, status, action = next_actions[stage]
    state["current_stage"] = current
    state["stage_status"] = status
    state["next_required_action"] = action
    append_event(
        feature_dir,
        state,
        "artifact-recorded",
        {"stage": stage, "artifact_revision": revision, "sha256": digest, "invalidated": invalidated},
    )
    save_state(feature_dir, state)
    return state


def cmd_approve(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    assert_control_integrity(feature_dir, state)
    stage = args.stage
    if stage not in APPROVAL_STAGES:
        raise ControlError(f"Stage does not accept approval: {stage}")
    if stage not in state["artifacts"]:
        raise ControlError(f"Cannot approve missing artifact: {ARTIFACT_FILES[stage]}")
    expected_status = "awaiting-final-approval" if stage == "archive" else "awaiting-approval"
    if state.get("current_stage") != stage or state.get("stage_status") != expected_status:
        raise ControlError(
            f"Approval is not current: expected {stage}/{expected_status}, "
            f"found {state.get('current_stage')}/{state.get('stage_status')}"
        )
    if args.message_id and any(
        record.get("message_id") == args.message_id
        for record in read_jsonl(feature_paths(feature_dir)["approvals"])
    ):
        raise ControlError("This user message ID has already been used for an SDD2 approval")
    if current_artifact_hash(feature_dir, stage) != state["artifacts"][stage]["sha256"]:
        raise ControlError(f"Artifact drift detected before approval: {stage}")
    if args.source == "user-message":
        if args.approver_role not in {"human", "user"}:
            raise ControlError("A real user-message approval must use approver_role=human or user")
        if not explicit_approval(stage, args.approval_text):
            raise ControlError(f"Approval text is ambiguous or does not identify the {stage} stage")
    elif args.source == "demo-simulation":
        if state["execution_mode"] != "demo" or not state.get("demo_authorization"):
            raise ControlError("AI demo approval requires prior explicit user demo authorization")
        if args.approver_role != "ai-as-human-reviewer":
            raise ControlError("Demo simulation must identify approver_role=ai-as-human-reviewer")
    else:
        raise ControlError(f"Unsupported approval source: {args.source}")
    if stage == "archive":
        pre_errors = archive_errors(feature_dir, state, require_archive=True)
        pre_errors = [error for error in pre_errors if error != "APPROVAL_MISSING_OR_INVALID:archive"]
        if pre_errors:
            raise ControlError("Archive cannot be approved: " + ", ".join(pre_errors))
    if stage == "unit-test-summary":
        unit_gate = state.get("quality_gates", {}).get("unit-test")
        artifact = state["artifacts"]["unit-test-summary"]
        if (
            not unit_gate
            or unit_gate.get("status") != "passed"
            or unit_gate.get("artifact_sha256") != artifact.get("sha256")
            or unit_gate.get("scope_sha256") != artifact.get("scope_sha256")
        ):
            raise ControlError("Unit Test Summary approval requires a passed Unit Test gate on this artifact and scope")
    artifact = state["artifacts"][stage]
    approval = append_chained_record(
        feature_paths(feature_dir)["approvals"],
        {
            "approval_id": str(uuid.uuid4()),
            "timestamp": utc_now(),
            "feature_id": state["feature_id"],
            "attempt": state["attempt"],
            "stage": stage,
            "result": "approved",
            "source": args.source,
            "approver_role": args.approver_role,
            "message_id": args.message_id,
            "approval_text": args.approval_text,
            "artifact_path": artifact["path"],
            "artifact_revision": artifact["revision"],
            "artifact_sha256": artifact["sha256"],
        },
        "record_hash",
    )
    state["approvals"][stage] = {
        "approval_id": approval["approval_id"],
        "status": "approved",
        "attempt": state["attempt"],
        "artifact_revision": artifact["revision"],
        "artifact_sha256": artifact["sha256"],
        "record_hash": approval["record_hash"],
        "approved_at": approval["timestamp"],
    }
    transitions = {
        "spec": ("design", "ready", "generate-design"),
        "design": ("tasks", "ready", "generate-tasks"),
        "tasks": ("implementation", "ready", "capture-implementation-scope"),
        "unit-test-summary": ("archive", "ready", "run-archive-check"),
        "archive": ("archive", "completed", "none"),
    }
    state["current_stage"], state["stage_status"], state["next_required_action"] = transitions[stage]
    state["last_completed_stage"] = stage
    state["revision"] += 1
    append_event(
        feature_dir,
        state,
        "stage-approved",
        {"stage": stage, "approval_id": approval["approval_id"], "artifact_sha256": artifact["sha256"]},
    )
    save_state(feature_dir, state)
    if stage == "archive":
        release_lock(
            state_repo_root(feature_dir, state),
            feature_dir,
            state["feature_id"],
        )
    return state


def cmd_capture_scope(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    assert_control_integrity(feature_dir, state, allow_scope_drift=True)
    if state.get("current_stage") != "implementation" or state.get("stage_status") != "ready":
        raise ControlError("Implementation scope capture is only allowed immediately after current Tasks approval")
    errors = approval_errors(feature_dir, state, "tasks")
    if errors:
        raise ControlError("Tasks approval is required before implementation: " + ", ".join(errors))
    reject_unsafe_patterns(args.allowed_path)
    reject_unsafe_patterns(args.forbidden_path)
    reject_unsafe_patterns(args.test_path)
    if not args.required_phase:
        raise ControlError("Implementation scope requires at least one approved phase")
    repo_root = state_repo_root(feature_dir, state)
    branch = run_git(repo_root, "branch", "--show-current")
    if branch != state["workspace_binding"]["branch"]:
        raise ControlError("Git branch changed since feature initialization")
    base_commit = args.base_commit or run_git(repo_root, "rev-parse", "HEAD")
    run_git(repo_root, "cat-file", "-e", f"{base_commit}^{{commit}}")
    scope = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": state["feature_id"],
        "attempt": state["attempt"],
        "repo_root": ".",
        "repository_id": repository_id(repo_root),
        "feature_repo_path": state["feature_repo_path"],
        "branch": branch,
        "base_commit": base_commit,
        "allowed_paths": sorted(set(args.allowed_path)),
        "forbidden_paths": sorted(set(args.forbidden_path)),
        "required_phases": unique_in_order(args.required_phase),
        "production_change": not args.non_production_change,
        "test_path_patterns": sorted(set(args.test_path or DEFAULT_TEST_PATHS)),
        "captured_at": utc_now(),
        "code_revision": 0,
        "frozen_snapshot": None,
    }
    initial = snapshot_for_scope(repo_root, scope)
    if initial["violations"]:
        raise ControlError("Pre-existing scope violations: " + ", ".join(initial["violations"]))
    if initial["files"]:
        dirty = ", ".join(item["path"] for item in initial["files"][:10])
        raise ControlError(
            "Implementation scope must start from a clean baseline; pre-existing changes found: " + dirty
        )
    scope["initial_snapshot"] = initial
    atomic_write_json(feature_paths(feature_dir)["scope"], scope)
    state["required_phases"] = scope["required_phases"]
    state["current_stage"] = "implementation"
    state["stage_status"] = "executing"
    state["next_required_action"] = "implement-next-approved-phase"
    state["revision"] += 1
    append_event(
        feature_dir,
        state,
        "implementation-scope-captured",
        {"base_commit": base_commit, "allowed_paths": scope["allowed_paths"], "required_phases": scope["required_phases"]},
    )
    save_state(feature_dir, state)
    return scope


def cmd_phase_review(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    assert_control_integrity(feature_dir, state, allow_scope_drift=True)
    if state.get("current_stage") != "implementation":
        raise ControlError("Phase Review is only valid during implementation")
    if args.phase not in state.get("required_phases", []):
        raise ControlError(f"Phase is not declared in implementation scope: {args.phase}")
    next_phase = next(
        (
            phase
            for phase in state.get("required_phases", [])
            if state.get("phase_reviews", {}).get(phase, {}).get("status") != "approved"
        ),
        None,
    )
    if next_phase != args.phase:
        raise ControlError(f"Phase Review order violation: expected {next_phase!r}, received {args.phase!r}")
    if not direct_approval(args.approval_text, (args.phase, "phase review", "阶段")):
        raise ControlError("Phase approval must identify the phase and explicit approval result")
    if args.message_id and any(
        record.get("message_id") == args.message_id
        for record in read_jsonl(feature_paths(feature_dir)["approvals"])
    ):
        raise ControlError("This user message ID has already been used for an SDD2 approval")
    if args.message_id and any(
        review.get("message_id") == args.message_id
        for review in state.get("phase_reviews", {}).values()
    ):
        raise ControlError("This user message ID has already been used for an SDD2 approval")
    if args.source == "user-message":
        if args.approver_role not in {"human", "user"}:
            raise ControlError("A real user-message Phase Review must use approver_role=human or user")
    elif args.source == "demo-simulation":
        if state["execution_mode"] != "demo" or not state.get("demo_authorization"):
            raise ControlError("AI demo Phase Review requires prior explicit user demo authorization")
        if args.approver_role != "ai-as-human-reviewer":
            raise ControlError("Demo simulation must identify approver_role=ai-as-human-reviewer")
    else:
        raise ControlError(f"Unsupported Phase Review source: {args.source}")
    state["phase_reviews"][args.phase] = {
        "status": "approved",
        "source": args.source,
        "approver_role": args.approver_role,
        "message_id": args.message_id,
        "approval_text": args.approval_text,
        "approved_at": utc_now(),
        "tasks_revision": state["artifacts"]["tasks"]["revision"],
        "tasks_sha256": state["artifacts"]["tasks"]["sha256"],
    }
    state["revision"] += 1
    remaining = [
        phase
        for phase in state.get("required_phases", [])
        if state.get("phase_reviews", {}).get(phase, {}).get("status") != "approved"
    ]
    state["stage_status"] = "executing"
    state["next_required_action"] = (
        f"implement-phase:{remaining[0]}" if remaining else "freeze-implementation-scope"
    )
    append_event(
        feature_dir,
        state,
        "phase-approved",
        {"phase": args.phase, "source": args.source, "approver_role": args.approver_role},
    )
    save_state(feature_dir, state)
    return state


def cmd_freeze_scope(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    assert_control_integrity(feature_dir, state, allow_scope_drift=True)
    if state.get("current_stage") not in {"implementation", "code-review", "auto-fix", "unit-test-summary"}:
        raise ControlError(f"Scope freeze is not valid from current stage {state.get('current_stage')}")
    for phase in state.get("required_phases", []):
        review = state.get("phase_reviews", {}).get(phase)
        if not review or review.get("status") != "approved":
            raise ControlError(f"Scope freeze requires current Phase Review approval: {phase}")
    scope = load_scope(feature_dir)
    snapshot = snapshot_for_scope(scope_repo_root(feature_dir, scope), scope)
    if snapshot["violations"]:
        state["blocked"] = {
            "code": "IMPLEMENTATION_SCOPE_VIOLATION",
            "reason": ", ".join(snapshot["violations"]),
            "recovery": "Return to tasks scope approval or remove unrelated changes.",
        }
        state["stage_status"] = "blocked"
        state["next_required_action"] = "resolve-scope-violation"
        save_state(feature_dir, state)
        raise ControlError("Implementation scope violation: " + ", ".join(snapshot["violations"]))
    previous = scope.get("frozen_snapshot")
    if not previous or previous.get("snapshot_sha256") != snapshot["snapshot_sha256"]:
        scope["code_revision"] += 1
        invalidated = invalidate_from(state, "code-review", "Implementation snapshot changed")
        feature_paths(feature_dir)["archive_evidence"].unlink(missing_ok=True)
    else:
        invalidated = []
    snapshot["code_revision"] = scope["code_revision"]
    scope["frozen_snapshot"] = snapshot
    atomic_write_json(feature_paths(feature_dir)["scope"], scope)
    state["blocked"] = None
    state["current_stage"] = "code-review"
    state["stage_status"] = "ready"
    state["next_required_action"] = "run-code-review"
    state["revision"] += 1
    append_event(
        feature_dir,
        state,
        "implementation-scope-frozen",
        {"scope_sha256": snapshot["snapshot_sha256"], "code_revision": scope["code_revision"], "invalidated": invalidated},
    )
    save_state(feature_dir, state)
    return snapshot


def require_current_scope(feature_dir: Path, state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    scope = load_scope(feature_dir)
    snapshot = snapshot_for_scope(scope_repo_root(feature_dir, scope), scope)
    if snapshot["violations"]:
        raise ControlError("Scope violation: " + ", ".join(snapshot["violations"]))
    frozen = scope.get("frozen_snapshot")
    if not frozen or frozen.get("snapshot_sha256") != snapshot["snapshot_sha256"]:
        raise ControlError("Implementation scope changed; run freeze-scope and re-enter Code Review")
    return scope, snapshot


def cmd_quality_gate(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    assert_control_integrity(feature_dir, state)
    gate = args.gate
    expected_stage = {"code-review": "code-review", "auto-fix": "auto-fix", "unit-test": "unit-test-summary"}[gate]
    if state.get("current_stage") != expected_stage:
        raise ControlError(
            f"{gate} gate is not current: expected stage {expected_stage}, found {state.get('current_stage')}"
        )
    if state.get("stage_status") != "recorded":
        raise ControlError(f"{gate} gate requires its current artifact to be recorded first")
    scope, snapshot = require_current_scope(feature_dir, state)
    current_sha = snapshot["snapshot_sha256"]
    if gate == "code-review":
        for stage in ("spec", "design", "tasks"):
            errors = approval_errors(feature_dir, state, stage)
            if errors:
                raise ControlError("Code Review blocked: " + ", ".join(errors))
        for phase in state.get("required_phases", []):
            review = state.get("phase_reviews", {}).get(phase)
            if not review or review.get("status") != "approved":
                raise ControlError(f"Code Review blocked by missing Phase Review: {phase}")
        if "code-review-findings" not in state["artifacts"]:
            raise ControlError("code-review-findings.md must be recorded before the Code Review gate")
        allowed = {"passed", "failed", "blocked"}
    elif gate == "auto-fix":
        review = state.get("quality_gates", {}).get("code-review")
        if not review or review.get("status") != "passed" or review.get("scope_sha256") != current_sha:
            raise ControlError("Auto-fix requires Code Review passed on the current scope")
        if "auto-fix-summary" not in state["artifacts"]:
            raise ControlError("auto-fix-summary.md must be recorded before the Auto-fix gate")
        allowed = {"passed", "not-required", "failed", "blocked"}
    else:
        review = state.get("quality_gates", {}).get("code-review")
        auto_fix = state.get("quality_gates", {}).get("auto-fix")
        if not review or review.get("status") != "passed" or review.get("scope_sha256") != current_sha:
            raise ControlError("Unit Test requires Code Review passed on the current scope")
        if not auto_fix or auto_fix.get("status") not in {"passed", "not-required"} or auto_fix.get("scope_sha256") != current_sha:
            raise ControlError("Unit Test requires Auto-fix closed on the current scope")
        if "unit-test-summary" not in state["artifacts"]:
            raise ControlError("unit-test-summary.md must be recorded before the Unit Test gate")
        if scope.get("production_change", True) and not changed_test_paths(scope, snapshot):
            raise ControlError(
                "Unit Test requires at least one changed test source matching the captured test path patterns"
            )
        allowed = {"passed", "failed", "blocked", "not-run"}
    if args.result not in allowed:
        raise ControlError(f"Invalid {gate} result: {args.result}; expected one of {sorted(allowed)}")
    if not args.evidence.strip():
        raise ControlError(f"{gate} requires non-empty reproducible evidence")
    record = {
        "status": args.result,
        "recorded_at": utc_now(),
        "scope_sha256": current_sha,
        "code_revision": scope["code_revision"],
        "evidence": args.evidence,
    }
    artifact_stage = {
        "code-review": "code-review-findings",
        "auto-fix": "auto-fix-summary",
        "unit-test": "unit-test-summary",
    }[gate]
    record["artifact_sha256"] = state["artifacts"][artifact_stage]["sha256"]
    if gate == "unit-test":
        record["changed_test_paths"] = changed_test_paths(scope, snapshot)
    state["quality_gates"][gate] = record
    if gate == "code-review":
        if args.result == "blocked":
            state["stage_status"] = "blocked"
            state["blocked"] = {
                "code": "CODE_REVIEW_BLOCKED",
                "reason": args.evidence,
                "recovery": "Resolve review input/scope evidence and rerun Code Review.",
            }
            state["next_required_action"] = "resolve-code-review"
        else:
            state["blocked"] = None
            state["current_stage"] = "auto-fix"
            state["stage_status"] = "ready"
            state["next_required_action"] = (
                "apply-review-findings" if args.result == "failed" else "record-auto-fix-not-required-or-current-fixes"
            )
    elif gate == "auto-fix":
        if args.result in {"failed", "blocked"}:
            state["stage_status"] = "blocked"
            state["blocked"] = {
                "code": f"AUTO_FIX_{args.result.upper()}",
                "reason": args.evidence,
                "recovery": "Resolve Auto-fix evidence or implementation and rerun from the current frozen scope.",
            }
            state["next_required_action"] = "resolve-auto-fix"
        else:
            state["blocked"] = None
            state["current_stage"] = "unit-test-summary"
            state["stage_status"] = "ready"
            state["next_required_action"] = "generate-or-update-test-source"
    elif args.result != "passed":
        state["stage_status"] = "blocked"
        state["blocked"] = {
            "code": f"UNIT_TEST_{args.result.upper().replace('-', '_')}",
            "reason": args.evidence,
            "recovery": "Fix/generate tests and implementation as needed, then refreeze, re-review, and rerun tests.",
        }
        state["next_required_action"] = "resolve-unit-test"
    else:
        state["blocked"] = None
        state["current_stage"] = "unit-test-summary"
        state["stage_status"] = "awaiting-approval"
        state["next_required_action"] = "request-unit-test-summary-approval"
    state["revision"] += 1
    append_event(feature_dir, state, "quality-gate-recorded", {"gate": gate, **record})
    save_state(feature_dir, state)
    return state


def cmd_validate(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    result = validate_state(feature_dir, state)
    if args.next_stage:
        if args.next_stage in APPROVAL_STAGES and args.next_stage != "archive":
            previous = {
                "design": "spec",
                "tasks": "design",
                "unit-test-summary": "tasks",
            }.get(args.next_stage)
            if previous:
                result["errors"].extend(approval_errors(feature_dir, state, previous))
        if args.next_stage == "archive":
            result["errors"].extend(archive_errors(feature_dir, state, require_archive=False))
    result["errors"] = sorted(set(result["errors"]))
    result["valid"] = not result["errors"]
    return result


def cmd_archive_check(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    errors = archive_errors(feature_dir, state, require_archive=args.require_archive)
    return {"valid": not errors, "errors": errors}


def cmd_prepare_archive(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    assert_control_integrity(feature_dir, state)
    if state.get("current_stage") != "archive" or state.get("stage_status") != "ready":
        raise ControlError("Archive evidence is only prepared after current Unit Test Summary approval")
    errors = approval_errors(feature_dir, state, "unit-test-summary")
    if feature_paths(feature_dir)["scope"].exists():
        errors.extend(quality_gate_errors(feature_dir, state))
    else:
        errors.append("SCOPE_MANIFEST_MISSING")
    if errors:
        raise ControlError("Archive evidence cannot be prepared: " + ", ".join(sorted(set(errors))))
    scope = load_scope(feature_dir)
    frozen = scope.get("frozen_snapshot")
    if not frozen:
        raise ControlError("Archive evidence requires a frozen implementation scope")
    evidence: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": state["feature_id"],
        "attempt": state["attempt"],
        "branch": scope["branch"],
        "base_commit": scope["base_commit"],
        "head_commit": frozen["head_commit"],
        "head_tree": frozen["head_tree"],
        "scope_sha256": frozen["snapshot_sha256"],
        "files": frozen["files"],
    }
    existing_path = feature_paths(feature_dir)["archive_evidence"]
    if existing_path.is_file():
        existing = read_json(existing_path)
        comparable = {key: value for key, value in existing.items() if key not in {"generated_at", "evidence_sha256"}}
        if comparable == evidence:
            if state.get("next_required_action") == "generate-archive-from-evidence":
                return existing
            evidence = existing
    if "evidence_sha256" not in evidence:
        evidence["generated_at"] = utc_now()
        evidence["evidence_sha256"] = sha256_bytes(canonical_json(evidence).encode("utf-8"))
        atomic_write_json(feature_paths(feature_dir)["archive_evidence"], evidence)
    state["revision"] += 1
    state["current_stage"] = "archive"
    state["stage_status"] = "ready"
    state["next_required_action"] = "generate-archive-from-evidence"
    append_event(
        feature_dir,
        state,
        "archive-evidence-prepared",
        {"evidence_sha256": evidence["evidence_sha256"], "scope_sha256": evidence["scope_sha256"]},
    )
    save_state(feature_dir, state)
    return evidence


def cmd_resume(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    if state["execution_mode"] != "historical-example" and state["stage_status"] not in TERMINAL_STATUSES:
        acquire_lock(
            state_repo_root(feature_dir, state),
            feature_dir,
            state["feature_id"],
        )
    validation = validate_state(feature_dir, state)
    return {
        "feature_id": state["feature_id"],
        "execution_mode": state["execution_mode"],
        "current_stage": state["current_stage"],
        "stage_status": state["stage_status"],
        "next_required_action": state["next_required_action"],
        "blocked": state.get("blocked"),
        "revision": state["revision"],
        "attempt": state["attempt"],
        "validation": validation,
    }


def cmd_close(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    assert_history_and_lock(feature_dir, state)
    if state.get("stage_status") in TERMINAL_STATUSES:
        raise ControlError("Terminal attempts are immutable; use restart-attempt for new work")
    lowered = args.approval_text.lower()
    if not any(term in lowered for term in ("风险", "risk", "终止", "abort", "关闭", "close")):
        raise ControlError("Closure approval must explicitly mention risk acceptance or abort/close")
    if args.result == "closed-with-risk" and not state.get("blocked"):
        raise ControlError("closed-with-risk is only valid for a recorded blocked/failed workflow")
    state["current_stage"] = "archive"
    state["stage_status"] = args.result
    state["next_required_action"] = "none"
    state["revision"] += 1
    append_event(
        feature_dir,
        state,
        "workflow-closed",
        {
            "result": args.result,
            "source": "user-message",
            "message_id": args.message_id,
            "approval_text": args.approval_text,
        },
    )
    save_state(feature_dir, state)
    release_lock(
        state_repo_root(feature_dir, state),
        feature_dir,
        state["feature_id"],
    )
    return state


def cmd_restart_attempt(args: argparse.Namespace) -> dict[str, Any]:
    feature_dir = normalize_feature_dir(args.feature_dir)
    state = load_state(feature_dir)
    assert_history_and_lock(feature_dir, state)
    if state["execution_mode"] == "historical-example":
        raise ControlError("Historical examples cannot start a new attempt")
    if state["stage_status"] != "blocked" and state["stage_status"] not in TERMINAL_STATUSES:
        raise ControlError("A new attempt is only allowed after a blocked or terminal attempt")
    lowered = args.approval_text.lower()
    if not any(term in lowered for term in ("重试", "重新开始", "retry", "restart")):
        raise ControlError("New-attempt approval must explicitly request retry or restart")
    acquire_lock(
        state_repo_root(feature_dir, state),
        feature_dir,
        state["feature_id"],
    )
    old_attempt = state["attempt"]
    state["attempt"] += 1
    state["revision"] += 1
    for approval in state.get("approvals", {}).values():
        approval["status"] = "invalidated"
        approval["invalidated_reason"] = f"Attempt {old_attempt} ended; fresh approval is required"
    state["quality_gates"] = {}
    state["phase_reviews"] = {}
    state["required_phases"] = []
    state["blocked"] = None
    state["last_completed_stage"] = "brief-design"
    if "spec" in state["artifacts"]:
        state["current_stage"] = "spec"
        state["stage_status"] = "awaiting-approval"
        state["next_required_action"] = "request-spec-approval"
    elif "proposal-input" in state["artifacts"]:
        state["current_stage"] = "spec"
        state["stage_status"] = "ready"
        state["next_required_action"] = "generate-spec"
    else:
        state["current_stage"] = "proposal-input"
        state["stage_status"] = "ready"
        state["next_required_action"] = "assemble-proposal-input"
    for key in ("scope", "archive_evidence"):
        feature_paths(feature_dir)[key].unlink(missing_ok=True)
    append_event(
        feature_dir,
        state,
        "attempt-restarted",
        {
            "previous_attempt": old_attempt,
            "source": "user-message",
            "message_id": args.message_id,
            "approval_text": args.approval_text,
        },
    )
    save_state(feature_dir, state)
    return state


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Initialize active SDD2 state after brief-design.md is persisted")
    init.add_argument("--feature-dir", required=True)
    init.add_argument("--feature-id", required=True)
    init.add_argument("--mode", choices=["real", "demo"], default="real")
    init.set_defaults(handler=cmd_init)

    legacy = sub.add_parser("migrate-legacy", help="Quarantine a historical sample without backfilling approval evidence")
    legacy.add_argument("--feature-dir", required=True)
    legacy.add_argument("--feature-id", required=True)
    legacy.set_defaults(handler=cmd_migrate_legacy)

    demo = sub.add_parser("authorize-demo", help="Record explicit user authorization before simulated AI approvals")
    demo.add_argument("--feature-dir", required=True)
    demo.add_argument("--authorization-text", required=True)
    demo.add_argument("--message-id")
    demo.set_defaults(handler=cmd_authorize_demo)

    artifact = sub.add_parser("record-artifact", help="Hash and version a generated or updated core artifact")
    artifact.add_argument("--feature-dir", required=True)
    artifact.add_argument("--stage", required=True, choices=sorted(ARTIFACT_FILES))
    artifact.set_defaults(handler=cmd_record_artifact)

    approve = sub.add_parser("approve", help="Persist a stage approval bound to the current artifact revision")
    approve.add_argument("--feature-dir", required=True)
    approve.add_argument("--stage", required=True, choices=sorted(APPROVAL_STAGES))
    approve.add_argument("--source", required=True, choices=["user-message", "demo-simulation"])
    approve.add_argument("--approver-role", required=True)
    approve.add_argument("--approval-text", required=True)
    approve.add_argument("--message-id")
    approve.set_defaults(handler=cmd_approve)

    scope = sub.add_parser("capture-scope", help="Bind implementation to a Git baseline and approved path manifest")
    scope.add_argument("--feature-dir", required=True)
    scope.add_argument("--base-commit")
    scope.add_argument("--allowed-path", action="append", required=True)
    scope.add_argument("--forbidden-path", action="append", default=[])
    scope.add_argument("--required-phase", action="append", default=[])
    scope.add_argument("--test-path", action="append", default=[])
    scope.add_argument("--non-production-change", action="store_true")
    scope.set_defaults(handler=cmd_capture_scope)

    phase = sub.add_parser("phase-review", help="Record explicit human approval for one declared implementation phase")
    phase.add_argument("--feature-dir", required=True)
    phase.add_argument("--phase", required=True)
    phase.add_argument("--source", required=True, choices=["user-message", "demo-simulation"])
    phase.add_argument("--approver-role", required=True)
    phase.add_argument("--approval-text", required=True)
    phase.add_argument("--message-id")
    phase.set_defaults(handler=cmd_phase_review)

    freeze = sub.add_parser("freeze-scope", help="Freeze the current implementation snapshot before quality review")
    freeze.add_argument("--feature-dir", required=True)
    freeze.set_defaults(handler=cmd_freeze_scope)

    gate = sub.add_parser("quality-gate", help="Record Code Review, Auto-fix, or Unit Test against a frozen scope")
    gate.add_argument("--feature-dir", required=True)
    gate.add_argument("--gate", required=True, choices=sorted(QUALITY_GATES))
    gate.add_argument("--result", required=True)
    gate.add_argument("--evidence", required=True)
    gate.set_defaults(handler=cmd_quality_gate)

    validate = sub.add_parser("validate", help="Validate state, hash chains, artifacts, lock, and scope")
    validate.add_argument("--feature-dir", required=True)
    validate.add_argument("--next-stage", choices=STAGE_ORDER)
    validate.set_defaults(handler=cmd_validate)

    archive = sub.add_parser("archive-check", help="Validate Archive prerequisites")
    archive.add_argument("--feature-dir", required=True)
    archive.add_argument("--require-archive", action="store_true")
    archive.set_defaults(handler=cmd_archive_check)

    prepare_archive = sub.add_parser("prepare-archive", help="Persist immutable Git and scope evidence for Archive")
    prepare_archive.add_argument("--feature-dir", required=True)
    prepare_archive.set_defaults(handler=cmd_prepare_archive)

    resume = sub.add_parser("resume", help="Return the only valid resume point for a feature")
    resume.add_argument("--feature-dir", required=True)
    resume.set_defaults(handler=cmd_resume)

    close = sub.add_parser("close", help="Close a failed workflow without marking successful delivery")
    close.add_argument("--feature-dir", required=True)
    close.add_argument("--result", required=True, choices=["closed-with-risk", "aborted"])
    close.add_argument("--approval-text", required=True)
    close.add_argument("--message-id")
    close.set_defaults(handler=cmd_close)

    restart = sub.add_parser("restart-attempt", help="Start a fresh attempt after explicit user retry approval")
    restart.add_argument("--feature-dir", required=True)
    restart.add_argument("--approval-text", required=True)
    restart.add_argument("--message-id")
    restart.set_defaults(handler=cmd_restart_attempt)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
    except ControlError as exc:
        print(canonical_json({"ok": False, "error": str(exc)}))
        return 2
    ok = result.get("valid", True) if isinstance(result, dict) else True
    print(json.dumps({"ok": ok, "result": result}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
