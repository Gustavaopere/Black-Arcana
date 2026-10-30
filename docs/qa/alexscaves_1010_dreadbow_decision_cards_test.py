#!/usr/bin/env python3
"""Crosscheck exact JVM Dreadbow decision anchors against the Dark Arrow card."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
SNAPSHOT = DIR / "EXACT-DREADBOW-DECISIONS-1.0.10.json"
CARD = DIR / "dark-arrow.md"

class DreadbowDecisionCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj = json.loads(SNAPSHOT.read_text(encoding="utf8"))
        cls.release = cls.obj["methods"]["releaseUsing"]
        cls.tick = cls.obj["methods"]["onUseTick"]
        cls.card = CARD.read_text(encoding="utf8")
    def slot(self, n, off):
        rows = [x for x in self.release["integer_slot_8_and_10_windows"]
                if x["slot"] == n and x["offset"] == off]
        self.assertEqual(len(rows), 1)
        return rows[0]["window"]
    def test_scope_and_fail_closed(self):
        self.assertEqual(self.obj["scope"],
                         "EXACT_1010_DREADBOW_SELECTED_CONTROL_DECISION_ANCHORS_ONLY")
        self.assertEqual(self.release["instruction_count"], 391)
        self.assertEqual(self.tick["instruction_count"], 175)
        self.assertFalse(self.obj["limits"]["complete_perk_ready"])
        self.assertFalse(self.obj["limits"]["provider_universe_closed"])
        self.assertEqual(self.obj["limits"]["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(self.obj["limits"]["physical_qa"], "NOT_TESTED")
    def test_precise_volley_is_source_of_local_eight(self):
        win = self.slot(8,57)
        self.assertTrue(any("PRECISE_VOLLEY" in x["symbol"] for x in win))
        self.assertTrue(any("ACCompat.enchantLevel" in x["symbol"] for x in win))
        self.assertTrue(any(x["opcode"] == "istore" and x["operand"] == "8"
                            for x in win))
    def test_twilight_and_perfect_shot_counter_are_source_of_local_ten(self):
        win = self.slot(10,108)
        self.assertTrue(any("TWILIGHT_PERFECTION" in x["symbol"] for x in win))
        self.assertTrue(any("getPerfectShotTicks" in x["symbol"] for x in win))
        self.assertTrue(any(x["opcode"] == "istore" and x["operand"] == "10"
                            for x in win))
    def test_exact_dark_arrow_factory_and_setters(self):
        self.assertEqual([x["offset"] for x in self.release["direct_dark_arrow_sites"]],
                         [383,402,409])
        self.assertEqual([x["offset"] for x in self.tick["direct_dark_arrow_sites"]],
                         [188,196])
    def test_card_records_pins_and_no_false_perk_certification(self):
        for tok in ("PRECISE_VOLLEY","TWILIGHT_PERFECTION","getPerfectShotTicks",
                    self.obj["class_sha256"],
                    "STATIC_TECHNICAL_CATALOG_ONLY","NOT_VERIFIED","NOT_TESTED","NO_MUTATION"):
            self.assertIn(tok,self.card)
        self.assertIn("EXACT-DREADBOW-DECISIONS-1.0.10.json", self.card)

if __name__ == "__main__":
    unittest.main()
