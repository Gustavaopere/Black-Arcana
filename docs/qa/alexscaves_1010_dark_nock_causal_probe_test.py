#!/usr/bin/env python3
"""Negative and arithmetic gates for the SHA-exact Dark Nock probe."""
import copy
import json
import unittest
from pathlib import Path

from alexscaves_1010_dark_nock_causal_probe import (
    EXPECTED, PIVOTS, check_pivots, canonical_anchors, first_valid,
    power, require, strict_pairs
)

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
CARD = P / "enchantments/dark-nock.md"
MANIFEST = P / "EXACT-DREADBOW-CONTRACTS-1.0.10.json"


class DarkNockCausalProbeTests(unittest.TestCase):
    def test_nominal_ticks_without_ascribing_new_spell(self):
        self.assertEqual([40 - 8 * x for x in range(4)], [40, 32, 24, 16])
        self.assertEqual([first_valid(40 - 8 * x) for x in range(4)],
                         [6, 5, 4, 3])
        for maximum in (40, 32, 24, 16):
            self.assertEqual(power(maximum, maximum), 1)
            self.assertLessEqual(power(maximum // 2, maximum), 1)
        with self.assertRaisesRegex(ValueError, "denominator"):
            power(2, 0)
        with self.assertRaisesRegex(ValueError, "denominator"):
            power(2, -8)

    def test_explicit_dark_nock_method_coverage(self):
        self.assertEqual(len(EXPECTED), len(set(EXPECTED)))
        for name in ("getMaxLoadTime", "getPowerForTime",
                     "getPullingAmount", "releaseUsing", "acInventoryTick",
                     "onUseTick", "getUseDuration"):
            self.assertIn(name, EXPECTED)
        self.assertIn(17, PIVOTS["getMaxLoadTime"])
        self.assertEqual(PIVOTS["getMaxLoadTime"][23], ("imul", ""))

    def test_direct_branch_rejects_missing_destination(self):
        method = {"instructions": [
            {"offset": 0, "opcode": "ifeq", "operand": "10", "symbol": ""},
            {"offset": 3, "opcode": "return", "operand": "", "symbol": ""},
        ]}
        with self.assertRaisesRegex(ValueError, "branch destination"):
            check_pivots(method, {})

    def test_pivot_detects_opcode_or_symbol_drift(self):
        method = {"instructions": [
            {"offset": 1, "opcode": "getstatic", "operand": "#2",
             "symbol": "Field X.DARK_NOCK:ResourceKey"},
            {"offset": 4, "opcode": "return", "operand": "", "symbol": ""},
        ]}
        check_pivots(method, {1: ("getstatic", "DARK_NOCK")})
        bad = copy.deepcopy(method)
        bad["instructions"][0]["symbol"] = "Field X.OTHER"
        with self.assertRaisesRegex(ValueError, "pivot drift"):
            check_pivots(bad, {1: ("getstatic", "DARK_NOCK")})
        with self.assertRaisesRegex(ValueError, "pivot drift"):
            check_pivots(method, {1: ("invokestatic", "DARK_NOCK")})

    def test_exact_previous_anchor_rejects_truncation(self):
        method = {"header": "testMethod()", "instructions": [
            {"offset": 1, "opcode": "getstatic", "operand": "#2",
             "symbol": "Field X.DARK_NOCK:ResourceKey"},
        ]}
        anchor = copy.deepcopy(method["instructions"])
        self.assertEqual(canonical_anchors(method, anchor), 1)
        anchor[0]["symbol"] = "WRONG"
        with self.assertRaisesRegex(ValueError, "anchor drift"):
            canonical_anchors(method, anchor)

    def test_json_duplicate_keys_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            json.loads('{"max_level": 3, "max_level": 100}',
                       object_pairs_hook=strict_pairs)

    def test_existing_card_and_binary_manifest_are_aligned(self):
        m = json.loads(MANIFEST.read_text(encoding="utf8"),
                       object_pairs_hook=strict_pairs)
        item = ("com/github/alexmodguy/alexscaves/server/item/"
                "DreadbowItem.class")
        records = m["classes"][item]["methods"]
        self.assertTrue(set(EXPECTED).issubset({x["name"] for x in records}))
        self.assertEqual(m["artifact_sha256"],
            "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(m["resources"]["data/alexscaves/enchantment/dark_nock.json"],
            "569cb5857db11189b2eb8a1163d53a440587ab02e2f14bc8296aaaf91dcd8033")
        card = CARD.read_text(encoding="utf8")
        for token in ("40−8", "Relentless", "getPowerForTime",
                      "getMaxLoadTime", "NO_MUTATION", "NOT_TESTED",
                      "NOT_VERIFIED", "⚠️"):
            self.assertIn(token, card)

if __name__ == "__main__":
    unittest.main()
