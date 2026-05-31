#!/usr/bin/env python3
"""Tests for brain audit validation rules."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import audit_brain  # noqa: E402


VALID_HEADER = "# Test\n> Owner: Owner | Pillar: All | Status: Active | Last Audit: 2026-05-31\n"
VALID_CONTRACT = """## AI Integration

| Decision | AI role | Human owner | Evidence inputs | Pass/fail criteria | Trace | Exception trigger | Flow metric |
|----------|---------|-------------|-----------------|--------------------|-------|-------------------|-------------|
| Is the file ready? | validate | Owner | Source data | Passes audit | Audit output | Audit error blocks commit | Error count |
"""


class AuditBrainTests(unittest.TestCase):
    def setUp(self) -> None:
        self._original_root = audit_brain.ROOT
        self._tmp = tempfile.TemporaryDirectory()
        audit_brain.ROOT = Path(self._tmp.name)

    def tearDown(self) -> None:
        audit_brain.ROOT = self._original_root
        self._tmp.cleanup()

    def write_core_file(self, body: str) -> None:
        path = audit_brain.ROOT / "03_ai_native_transformation" / "test.md"
        path.parent.mkdir(parents=True)
        path.write_text(body)

    def test_missing_ai_decision_contract_fails(self) -> None:
        self.write_core_file(
            VALID_HEADER
            + "\n## Purpose\n\nMetric and escalation trigger are present.\n\n"
            + "## AI Integration\n\nUse AI to summarize metrics.\n"
        )
        errors: list[str] = []
        warnings: list[str] = []

        audit_brain.check_governance(errors, warnings)

        self.assertIn(
            "03_ai_native_transformation/test.md: missing AI Decision Contract table in ## AI Integration",
            errors,
        )

    def test_backticked_ai_integration_text_does_not_count_as_heading(self) -> None:
        self.write_core_file(
            VALID_HEADER
            + "\n## Purpose\n\nMetric and escalation trigger are present.\n\n"
            + "This file mentions `## AI Integration` but has no real section.\n"
        )
        errors: list[str] = []
        warnings: list[str] = []

        audit_brain.check_governance(errors, warnings)

        self.assertIn("03_ai_native_transformation/test.md: missing ## AI Integration", errors)

    def test_valid_ai_decision_contract_passes(self) -> None:
        self.write_core_file(
            VALID_HEADER
            + "\n## Purpose\n\nMeasurable outcome and escalation trigger are present.\n\n"
            + VALID_CONTRACT
        )
        errors: list[str] = []
        warnings: list[str] = []

        audit_brain.check_governance(errors, warnings)

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
