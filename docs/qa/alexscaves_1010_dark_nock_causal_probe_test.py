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

    def test_causal_seal_ledger_and_canonical_indexes(self):
        seal = json.loads((P / "EXACT-DARK-NOCK-CAUSAL-1.0.10.json").read_text())
        ledger = json.loads((ROOT /
            "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        key = "✅-alexs-caves-continued/enchantments/dark-nock.md"
        cert = ledger["objects"][key]
        self.assertEqual(cert["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["status"], "COMPLETE_PERK_READY")
        self.assertEqual(cert["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(set(cert["evidence"]), {
            "identity", "behavior", "parameters", "targeting",
            "costs", "integration", "validation"})
        self.assertEqual(cert["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"], "NOT_TESTED")
        self.assertEqual(seal["full_report_sha256"],
            "f19e0377f1388f81f34aea4514800d3be4a602ae07ad46dba4e8d47579f55f28")
        self.assertEqual(seal["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(seal["limits"]["mutation"], "NO_MUTATION")
        self.assertEqual(len(seal["method_sha256"]), 13)
        self.assertEqual(sum(seal["instruction_counts"].values()), 938)
        self.assertEqual(sum(seal["direct_branch_counts"].values()), 99)
        self.assertEqual(len(seal["direct_DARK_NOCK_class_token_owners"]), 2)
        self.assertEqual(len(ledger["objects"]), 205)
        card = CARD.read_text()
        self.assertIn("contrato técnico estático individual certificado",card)
        self.assertIn("938 instruções", card)
        self.assertIn("EXACT-DARK-NOCK-CAUSAL-1.0.10.json", card)
        self.assertIn("NO_MUTATION", card)
        cross = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        self.assertIn("individual_full_enchantment_dossiers=39/51",cross)
        self.assertIn("individual_partial_enchantment_dossiers=12/51",cross)
        self.assertIn("| ✅ | `alexscaves:dark_nock`",cross)
        sub = (P / "enchantments/INDEX.md").read_text()
        prov = (P / "INDEX.md").read_text()
        global_index = (ROOT / "wiki/modpack-catalog/providers/INDEX.md").read_text()
        self.assertIn("Fichas catalogadas (somente fichas detectadas): 39/51",sub)
        self.assertIn("Fichas catalogadas (somente fichas detectadas): 67/81",prov)
        self.assertIn("Fichas com contrato técnico estático certificado: 205/2393",global_index)
        self.assertIn("Providers com catálogo concluído: 4/164",global_index)

if __name__ == "__main__":
    unittest.main()
