#!/usr/bin/env python3
"""Static integrity checks for the UAW-SDD 2.0 Skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


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
    "skills/uaw-sdd-ai-coding/references/schemas/feature-state.schema.json",
    "skills/uaw-sdd-ai-coding/references/schemas/gate-approval.schema.json",
    "skills/uaw-sdd-ai-coding/references/schemas/implementation-scope.schema.json",
    "skills/uaw-sdd-ai-coding/references/templates/auto-fix-summary-template.md",
    "skills/uaw-sdd-ai-coding/references/rules/backend/case-tracker-compatibility.md",
}

ALLOWED_ORIGINAL_REFERENCES = {
    "skills/uaw-sdd-ai-coding/references/context/routing-index.md",
    "skills/uaw-sdd-ai-coding/references/context/transactions-dictionary.md",
    "skills/uaw-sdd-ai-coding/references/context/source-provenance.json",
}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"INVALID_JSON:{relative(path)}:{exc}")
        return None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

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

    epi = SKILLS / "uaw-sdd-ai-coding/references/rules/backend/epi-gateway.md"
    om = SKILLS / "uaw-sdd-ai-coding/references/rules/backend/om-api-acl.md"
    if epi.read_bytes() == om.read_bytes():
        errors.append("EPI_RULE_DUPLICATES_OM_RULE")

    entry_marker = "short brief prompt + invoke this Skill"
    if entry_marker not in (SKILLS / "uaw-sdd-ai-coding/SKILL.md").read_text(encoding="utf-8"):
        errors.append("PUBLIC_ENTRY_CONTRACT_MISSING")

    feature_dirs = sorted({path.parent for path in FEATURES.rglob("brief-design.md")})
    if not feature_dirs:
        warnings.append("NO_HISTORICAL_FEATURE_EXAMPLES")
    for feature_dir in feature_dirs:
        present = {path.name for path in feature_dir.glob("*.md")}
        for missing in sorted(PUBLIC_ASSETS - present):
            errors.append(f"FEATURE_ASSET_MISSING:{relative(feature_dir)}:{missing}")
        for artifact in sorted(feature_dir.glob("*.md")):
            content = artifact.read_text(encoding="utf-8")
            if "HISTORICAL EXAMPLE ONLY" not in content[:800]:
                errors.append(f"HISTORICAL_BANNER_MISSING:{relative(artifact)}")
            if "AI-as-human-reviewer" in content:
                errors.append(f"LEGACY_SELF_APPROVAL_NOT_QUARANTINED:{relative(artifact)}")
        state_path = feature_dir / ".sdd2/feature-state.json"
        state = read_json(state_path, errors) if state_path.is_file() else None
        if not isinstance(state, dict):
            errors.append(f"HISTORICAL_STATE_MISSING:{relative(feature_dir)}")
        else:
            if state.get("execution_mode") != "historical-example" or state.get("stage_status") != "superseded":
                errors.append(f"HISTORICAL_STATE_NOT_QUARANTINED:{relative(feature_dir)}")
            if state.get("approvals"):
                errors.append(f"HISTORICAL_APPROVAL_BACKFILLED:{relative(feature_dir)}")
            if Path(state.get("feature_dir", "")).is_absolute():
                errors.append(f"NONPORTABLE_FEATURE_PATH:{relative(state_path)}")

    control_contract = (SKILLS / "uaw-sdd-ai-coding/references/sdd2-control-contract.md").read_text(encoding="utf-8")
    for asset in sorted(PUBLIC_ASSETS):
        if asset not in control_contract:
            errors.append(f"CONTROL_CONTRACT_ASSET_MISSING:{asset}")

    payload = {
        "valid": not errors,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "checked_runtime_files": len(runtime_files),
        "checked_historical_features": len(feature_dirs),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
