#!/usr/bin/env python3
"""Static integrity checks for the UAW-SDD 2.0 Skill package."""

from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from sdd2_control import ControlError, simplified_chinese_body_issues, validate_state


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "skills"
FEATURES = ROOT / "sdd2-features"

PUBLIC_ASSETS = {
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

REQUIRED_RUNTIME = {
    "skills/uaw-sdd-ai-coding/references/sdd2-control-contract.md",
    "skills/uaw-sdd-ai-coding/references/language-policy.md",
    "skills/uaw-sdd-ai-coding/references/schemas/feature-state.schema.json",
    "skills/uaw-sdd-ai-coding/references/schemas/gate-approval.schema.json",
    "skills/uaw-sdd-ai-coding/references/schemas/implementation-scope.schema.json",
    "skills/uaw-sdd-ai-coding/references/templates/auto-fix-summary-template.md",
    "skills/uaw-sdd-ai-coding/references/rules/backend/case-tracker-compatibility.md",
}

LANGUAGE_RELAXED_RUNTIME = {
    "skills/uaw-sdd-ai-coding/references/context/transactions-dictionary.md",
}

REQUIRED_SUPPLEMENTAL_LANGUAGE_FILES = {
    "CODEX_HANDOFF.md",
    "docs/UAW-SDD2.0 Skill化方案说明与操作指南.docx",
    "uaw-sdd-demo/README.md",
}

ALLOWED_ORIGINAL_REFERENCES = {
    "skills/uaw-sdd-ai-coding/references/language-policy.md",
    "skills/uaw-sdd-ai-coding/references/context/routing-index.md",
    "skills/uaw-sdd-ai-coding/references/context/transactions-dictionary.md",
    "skills/uaw-sdd-ai-coding/references/context/source-provenance.json",
}

LIVE_EXECUTION_MODES = {"standard", "demo"}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"INVALID_JSON:{relative(path)}:{exc}")
        return None


def read_docx_text(path: Path) -> str:
    text_parts: list[str] = []
    word_namespace = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    paragraph_tag = f"{{{word_namespace}}}p"
    style_tag = f"{{{word_namespace}}}pStyle"
    text_tag = f"{{{word_namespace}}}t"
    value_attribute = f"{{{word_namespace}}}val"
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if not name.startswith("word/") or not name.endswith(".xml"):
                continue
            root = ElementTree.fromstring(archive.read(name))
            for paragraph in root.iter(paragraph_tag):
                style = paragraph.find(f"./{{{word_namespace}}}pPr/{style_tag}")
                if style is not None and style.get(value_attribute) == "CodeBlock":
                    continue
                paragraph_text = "".join(node.text or "" for node in paragraph.iter(text_tag))
                if paragraph_text:
                    text_parts.append(paragraph_text)
    return "\n".join(text_parts)


def validate_feature_directory(
    feature_dir: Path,
    errors: list[str],
    warnings: list[str],
) -> str:
    """Validate one Feature according to its persisted execution mode."""
    feature_rel = relative(feature_dir)
    state_path = feature_dir / ".sdd2/feature-state.json"
    state = read_json(state_path, errors) if state_path.is_file() else None
    execution_mode = state.get("execution_mode") if isinstance(state, dict) else None

    if execution_mode in LIVE_EXECUTION_MODES:
        if Path(state.get("feature_dir", "")).is_absolute():
            errors.append(f"NONPORTABLE_FEATURE_PATH:{relative(state_path)}")
        for artifact in sorted(feature_dir.glob("*.md")):
            if artifact.name not in PUBLIC_ASSETS:
                continue
            minimum_han = 8 if artifact.name == "brief-design.md" else 16
            content = artifact.read_text(encoding="utf-8")
            for issue in simplified_chinese_body_issues(content, minimum_han=minimum_han):
                errors.append(f"LANGUAGE_POLICY_VIOLATION:{relative(artifact)}:{issue}")
        try:
            result = validate_state(feature_dir, state)
        except (ControlError, KeyError, OSError, json.JSONDecodeError) as exc:
            errors.append(f"LIVE_FEATURE_VALIDATION_FAILED:{feature_rel}:{exc}")
        else:
            for issue in result["errors"]:
                errors.append(f"LIVE_FEATURE_INVALID:{feature_rel}:{issue}")
            for issue in result["warnings"]:
                warnings.append(f"LIVE_FEATURE_WARNING:{feature_rel}:{issue}")
        return "live"

    present = {path.name for path in feature_dir.glob("*.md")}
    for missing in sorted(PUBLIC_ASSETS - present):
        errors.append(f"FEATURE_ASSET_MISSING:{feature_rel}:{missing}")
    for artifact in sorted(feature_dir.glob("*.md")):
        content = artifact.read_text(encoding="utf-8")
        if "HISTORICAL EXAMPLE ONLY" not in content[:800]:
            errors.append(f"HISTORICAL_BANNER_MISSING:{relative(artifact)}")
        if "AI-as-human-reviewer" in content:
            errors.append(f"LEGACY_SELF_APPROVAL_NOT_QUARANTINED:{relative(artifact)}")
    if not isinstance(state, dict):
        errors.append(f"HISTORICAL_STATE_MISSING:{feature_rel}")
    else:
        if execution_mode != "historical-example" or state.get("stage_status") != "superseded":
            errors.append(f"HISTORICAL_STATE_NOT_QUARANTINED:{feature_rel}")
        if state.get("approvals"):
            errors.append(f"HISTORICAL_APPROVAL_BACKFILLED:{feature_rel}")
        if Path(state.get("feature_dir", "")).is_absolute():
            errors.append(f"NONPORTABLE_FEATURE_PATH:{relative(state_path)}")
    return "historical"


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    language_checked_files = 0

    for item in sorted(REQUIRED_RUNTIME):
        if not (ROOT / item).is_file():
            errors.append(f"MISSING_RUNTIME_ASSET:{item}")

    for schema in sorted((SKILLS / "uaw-sdd-ai-coding/references/schemas").glob("*.json")):
        value = read_json(schema, errors)
        if isinstance(value, dict) and value.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"INVALID_SCHEMA_DIALECT:{relative(schema)}")

    provenance_path = SKILLS / "uaw-sdd-ai-coding/references/context/source-provenance.json"
    provenance = read_json(provenance_path, errors)
    if isinstance(provenance, dict):
        entries = provenance.get("entries", [])
        sources = {entry.get("source") for entry in entries if isinstance(entry, dict)}
        actual_sources = {relative(path) for path in (ROOT / "original").rglob("*") if path.is_file()}
        for missing in sorted(actual_sources - sources):
            errors.append(f"PROVENANCE_SOURCE_UNMAPPED:{missing}")
        for extra in sorted(sources - actual_sources):
            errors.append(f"PROVENANCE_SOURCE_MISSING:{extra}")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("INVALID_PROVENANCE_ENTRY")
                continue
            for target in entry.get("runtime_targets", []):
                if not (ROOT / target).is_file():
                    errors.append(f"PROVENANCE_TARGET_MISSING:{target}")

    runtime_files = [path for path in SKILLS.rglob("*") if path.is_file() and path.suffix in {".md", ".html", ".yaml", ".json", ".py"}]
    for path in runtime_files:
        if path.resolve() == Path(__file__).resolve():
            continue
        content = path.read_text(encoding="utf-8")
        rel = relative(path)
        if path.suffix in {".md", ".html"} or path.name == "openai.yaml":
            language_checked_files += 1
            language_issues = simplified_chinese_body_issues(
                content,
                minimum_han=12,
                enforce_dominance=rel not in LANGUAGE_RELAXED_RUNTIME,
            )
            for issue in language_issues:
                errors.append(f"LANGUAGE_POLICY_VIOLATION:{rel}:{issue}")
        if "UAW-Code-Review.md" in content:
            errors.append(f"STALE_REFERENCE:{rel}:UAW-Code-Review.md")
        if "[✓]" in content:
            errors.append(f"NONSTANDARD_CHECKBOX:{rel}")
        if "original/" in content and rel not in ALLOWED_ORIGINAL_REFERENCES:
            errors.append(f"ORIGINAL_USED_AS_RUNTIME:{rel}")
        for match in re.findall(r"skills/[A-Za-z0-9_.\-/]+", content):
            candidate = match.rstrip(".,:;`)'\"")
            if "/<" in candidate or candidate.endswith("/"):
                continue
            if not (ROOT / candidate).exists():
                errors.append(f"BROKEN_SKILL_REFERENCE:{rel}:{candidate}")

    supplemental_language_files = {
        ROOT / item for item in REQUIRED_SUPPLEMENTAL_LANGUAGE_FILES
    }
    supplemental_language_files.update(ROOT.glob("*.md"))
    supplemental_language_files.update(
        path for path in (ROOT / "docs").rglob("*") if path.is_file() and path.suffix in {".md", ".html", ".docx"}
    )
    supplemental_language_files.update(
        path for path in (ROOT / "uaw-sdd-demo").glob("*.md") if path.is_file()
    )
    for path in sorted(supplemental_language_files):
        item = relative(path)
        path = ROOT / item
        if not path.is_file():
            errors.append(f"MISSING_LANGUAGE_ASSET:{item}")
            continue
        try:
            content = read_docx_text(path) if path.suffix == ".docx" else path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
            errors.append(f"INVALID_LANGUAGE_ASSET:{item}:{exc}")
            continue
        language_checked_files += 1
        for issue in simplified_chinese_body_issues(content, minimum_han=16):
            errors.append(f"LANGUAGE_POLICY_VIOLATION:{item}:{issue}")

    epi = SKILLS / "uaw-sdd-ai-coding/references/rules/backend/epi-gateway.md"
    om = SKILLS / "uaw-sdd-ai-coding/references/rules/backend/om-api-acl.md"
    if epi.read_bytes() == om.read_bytes():
        errors.append("EPI_RULE_DUPLICATES_OM_RULE")

    entry_marker = "short brief prompt + invoke this Skill"
    if entry_marker not in (SKILLS / "uaw-sdd-ai-coding/SKILL.md").read_text(encoding="utf-8"):
        errors.append("PUBLIC_ENTRY_CONTRACT_MISSING")

    feature_dirs = sorted({path.parent for path in FEATURES.rglob("brief-design.md")})
    historical_feature_count = 0
    live_feature_count = 0
    if not feature_dirs:
        warnings.append("NO_SDD2_FEATURES")
    for feature_dir in feature_dirs:
        feature_kind = validate_feature_directory(feature_dir, errors, warnings)
        if feature_kind == "live":
            live_feature_count += 1
        else:
            historical_feature_count += 1

    control_contract = (SKILLS / "uaw-sdd-ai-coding/references/sdd2-control-contract.md").read_text(encoding="utf-8")
    for asset in sorted(PUBLIC_ASSETS):
        if asset not in control_contract:
            errors.append(f"CONTROL_CONTRACT_ASSET_MISSING:{asset}")

    payload = {
        "valid": not errors,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "checked_runtime_files": len(runtime_files),
        "checked_language_files": language_checked_files,
        "checked_historical_features": historical_feature_count,
        "checked_live_features": live_feature_count,
        "checked_source_archive_files": sum(1 for path in (ROOT / "original").rglob("*") if path.is_file()),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
