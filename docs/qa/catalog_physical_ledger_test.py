#!/usr/bin/env python3
"""Check the pinned, documentation-only physical/semantic crosswalk.

This test does NOT assert current runtime, JAR-byte equivalence, effective
configuration, or survival acquisition. It verifies that the historical
physical-version reconciliation remains internally consistent with the
canonical counted ledger on the checked-out commit.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md"
REPORT = (
    ROOT
    / "wiki/modpack-catalog/meta/PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md"
)

LEDGER_ROW = re.compile(r"^\|\s*\[([^\]]+)\]\([^)]+\)\s*\|", re.MULTILINE)
VERSION = re.compile(r"\d+(?:\.\d+){1,3}[a-z]?", re.IGNORECASE)


def _ledger_rows(text: str) -> dict[str, str]:
    section = text.split("### Counted ledger", 1)[1].split("\n## ", 1)[0]
    result: dict[str, str] = {}
    for line in section.splitlines():
        match = LEDGER_ROW.match(line)
        if not match:
            continue
        fields = line.split("|")
        name = match.group(1)
        if name in result:
            raise AssertionError(f"Duplicate counted ledger provider: {name}")
        result[name] = fields[4].strip()  # COUNTED_* or CURRENT_PHYSICAL_ABSENT
    return result


def _table_rows(report: str, heading: str, next_heading: str) -> list[list[str]]:
    section = report.split(heading, 1)[1].split(next_heading, 1)[0]
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        parts = [field.strip() for field in line.strip("|").split("|")]
        if len(parts) >= 5 and parts[0] not in {"Counted provider", "Provider"}:
            rows.append(parts)
        elif len(parts) == 4 and parts[0] not in {"Provider"}:
            rows.append(parts)
    return rows


class PhysicalLedgerVersionReconciliationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = LEDGER.read_text(encoding="utf-8")
        cls.report = REPORT.read_text(encoding="utf-8")
        cls.counted = _ledger_rows(cls.ledger)
        cls.installed = _table_rows(
            cls.report,
            "## Exact-current physical crosswalk",
            "## Historical catalogs excluded from current physical sum",
        )
        cls.absent = _table_rows(
            cls.report,
            "## Historical catalogs excluded from current physical sum",
            "## Boundaries and remaining work",
        )

    def test_each_counted_provider_is_documented_exactly_once(self) -> None:
        installed_names = [row[0] for row in self.installed]
        absent_names = [row[0] for row in self.absent]
        combined = installed_names + absent_names
        self.assertEqual(len(combined), len(set(combined)), "Duplicate provider in crosswalk")
        self.assertEqual(set(self.counted), set(combined), "Ledger/crosswalk identities differ")
        self.assertEqual(
            {name for name, state in self.counted.items()
             if "CURRENT_PHYSICAL_ABSENT" in state},
            set(absent_names),
            "Do not silently materialize or drop historically absent providers",
        )

    def test_unique_physical_rows_and_jar_shapes(self) -> None:
        positions: list[int] = []
        jars: list[str] = []
        for row in self.installed:
            self.assertEqual(5, len(row), row)
            self.assertRegex(row[1], r"^#\d{3}$")
            position = int(row[1][1:])
            self.assertTrue(1 < position <= 587, row)
            positions.append(position)
            self.assertTrue(row[2].startswith(chr(96)) and row[2].endswith(chr(96)), row)
            filename = row[2].strip(chr(96))
            self.assertTrue(filename.endswith(".jar"), row)
            jars.append(filename)
        self.assertEqual(len(positions), len(set(positions)), "Duplicate physical index")
        self.assertEqual(len(jars), len(set(jars)), "Duplicate JAR assignment")

    def test_declared_version_consistency(self) -> None:
        for name, _position, quoted_jar, physical_version, ledger_version in self.installed:
            candidate = VERSION.search(ledger_version)
            self.assertIsNotNone(candidate, name)
            token = candidate.group()
            self.assertTrue(
                token.lower() in (physical_version + " " + quoted_jar).lower(),
                f"{name}: ledger {ledger_version!r} versus {physical_version!r}",
            )

    def test_absent_counted_contribution_is_zero(self) -> None:
        for name, _ver, row, status in self.absent:
            self.assertEqual("None", row, name)
            self.assertIn("CURRENT_PHYSICAL_ABSENT", status, name)

    def test_physical_neoforge_not_mistaken_for_compile_baseline(self) -> None:
        self.assertIn("NeoForge physical modloader is **21.1.250**", self.report)
        self.assertIn("uses **21.1.248** as its compile/dev baseline", self.report)


if __name__ == "__main__":
    unittest.main()
