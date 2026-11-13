#!/usr/bin/env python3
"""Ensure Bonking's exact causal manifesto remains partial-only."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL=PROVIDER/"EXACT-BONKING-CAUSAL-1.0.10.json"
PREV=PROVIDER/"EXACT-BONKING-1.0.10.json"
CARD=PROVIDER/"enchantments/bonking.md"
CROSS=PROVIDER/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md"
LEDGER=ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(SEAL.read_text(encoding="utf8"))
        cls.parent=json.loads(PREV.read_text(encoding="utf8"))
    def test_legacy_binary_identity_and_21_branches(self):
        self.assertEqual(self.data["artifact"],self.parent["artifact"])
        method=self.data["method"]
        self.assertEqual(method["instruction_count"],229)
        self.assertEqual(method["parsed_method_sha256"],
                         self.parent["death_consumer"]["parsed_method_sha256"])
        self.assertEqual(len(method["all_branch_edges"]),21)
        self.assertEqual(method["exception_table"]["declared_exception_handlers"],0)
    def test_preconditions_rng_and_loot_chance_loops(self):
        method=self.data["method"]
        e={x["offset"]:x for x in method["all_branch_edges"]}
        for offset in (97,110,127,157,173,194,214):
            self.assertEqual(e[offset]["target"],432)
        self.assertEqual(e[363]["target"],316)
        self.assertTrue(e[363]["back_edge"])
        self.assertEqual(e[429]["target"],390)
        self.assertTrue(e[429]["back_edge"])
        pins={x["offset"]:x for x in method["selected_bonking_pivots"]}
        self.assertIn("0.33",pins[191]["symbol"])
        self.assertIn("ac_dropCustomDeathLoot",pins[372]["symbol"])
        self.assertIn("ac_setDropChance",pins[421]["symbol"])
        self.assertEqual(pins[354]["opcode"],"fconst_0")
    def test_mixin_declared_not_execution_proof(self):
        configs=self.data["mixin_declarations"]
        self.assertEqual(len(configs),1)
        self.assertEqual(configs[0]["path"],"alexscaves.mixins.json")
        self.assertIn("mixins",configs[0]["entries_in"])
        self.assertEqual(len(self.data["loot_bridge"]),3)
    def test_historical_partial_and_current_static_certificate_never_mutate(self):
        key="✅-alexs-caves-continued/enchantments/bonking.md"
        cert=json.loads(LEDGER.read_text(encoding="utf8"))["objects"][key]
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(cert["evidence"]),
                         {"identity","behavior","parameters","targeting",
                          "costs","integration","validation"})
        self.assertEqual(self.data["limits"]["static_certification"],"PARTIAL")
        self.assertEqual(self.data["limits"]["mutation"],"NO_MUTATION")
        self.assertEqual(self.data["limits"]["physical_qa"],"NOT_TESTED")
        self.assertEqual(self.data["limits"]["safe_mutating_hook"],"NOT_VERIFIED")
        self.assertIn("EXACT-BONKING-CAUSAL-1.0.10.json",CARD.read_text(encoding="utf8"))
        self.assertIn("EXACT-BONKING-CONTRACT-1.0.10.json",CARD.read_text(encoding="utf8"))
        self.assertIn("| ✅ | `alexscaves:bonking`",CROSS.read_text(encoding="utf8"))
if __name__=="__main__":
    unittest.main()
