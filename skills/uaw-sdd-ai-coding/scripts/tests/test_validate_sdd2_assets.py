from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import validate_sdd2_assets as validator


CHINESE_BODY = "# 功能资产\n\n这是受控流程生成的简体中文资产，用于验证当前状态和后续动作。\n"


class ValidateSdd2AssetsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.feature = self.root / "sdd2-features/Sprint1/example"
        (self.feature / ".sdd2").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_state(self, state: dict) -> None:
        (self.feature / ".sdd2/feature-state.json").write_text(
            json.dumps(state, ensure_ascii=False), encoding="utf-8"
        )

    def test_live_demo_feature_is_not_treated_as_historical(self) -> None:
        (self.feature / "brief-design.md").write_text(CHINESE_BODY, encoding="utf-8")
        self._write_state(
            {
                "execution_mode": "demo",
                "stage_status": "awaiting-approval",
                "feature_dir": "sdd2-features/Sprint1/example",
            }
        )
        errors: list[str] = []
        warnings: list[str] = []

        with (
            patch.object(validator, "ROOT", self.root),
            patch.object(
                validator,
                "validate_state",
                return_value={"errors": [], "warnings": []},
            ),
        ):
            kind = validator.validate_feature_directory(self.feature, errors, warnings)

        self.assertEqual(kind, "live")
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_historical_feature_still_requires_quarantine_assets(self) -> None:
        (self.feature / "brief-design.md").write_text(CHINESE_BODY, encoding="utf-8")
        self._write_state(
            {
                "execution_mode": "historical-example",
                "stage_status": "superseded",
                "feature_dir": "sdd2-features/Sprint1/example",
                "approvals": {},
            }
        )
        errors: list[str] = []
        warnings: list[str] = []

        with patch.object(validator, "ROOT", self.root):
            kind = validator.validate_feature_directory(self.feature, errors, warnings)

        self.assertEqual(kind, "historical")
        self.assertTrue(any(error.startswith("FEATURE_ASSET_MISSING:") for error in errors))
        self.assertTrue(any(error.startswith("HISTORICAL_BANNER_MISSING:") for error in errors))


if __name__ == "__main__":
    unittest.main()
