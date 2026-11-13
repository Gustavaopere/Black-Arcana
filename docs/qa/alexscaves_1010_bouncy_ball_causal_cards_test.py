#!/usr/bin/env python3
"""Bouncy Ball individual static contract, causal seal and ledger assertions."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
META = ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
KEY = "✅-alexs-caves-continued/enchantments/bouncy-ball.md"
CARD = PROVIDER / "enchantments/bouncy-ball.md"

class BouncyBallCardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads((PROVIDER / "EXACT-BOUNCY-BALL-CAUSAL-1.0.10.json").read_text())
        cls.parent = json.loads((PROVIDER / "EXACT-BOUNCY-BALL-1.0.10.json").read_text())
        cls.state = json.loads((PROVIDER / "EXACT-GUMBALL-STATE-1.0.10.json").read_text())
        cls.ledger = json.loads(META.read_text())
        cls.card = CARD.read_text()
        cls.cross = (PROVIDER / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()

    def test_exact_parent_and_state_artifact(self):
        self.assertEqual(self.seal["artifact"], self.parent["artifact"])
        self.assertEqual(self.seal["artifact"], self.state["artifact"])
        self.assertEqual(self.seal["artifact"]["sha1"],
                         "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570")
        self.assertEqual(self.seal["artifact"]["size_bytes"], 75279314)

    def test_class_method_census_and_full_direct_branches(self):
        self.assertEqual([x["declared_method_count"] for x in self.seal["classes"]],
                         [25, 28, 36])
        self.assertEqual([x["name"] for x in self.seal["selected_consumers"]],
                         [x["method"]["name"] for x in self.parent["selected_consumers"]])
        counts = {x["name"]:x["conditional_and_goto_branches"]
                  for x in self.seal["selected_consumers"]}
        self.assertEqual([counts[x] for x in
                          ("acInventoryTick","bounceFromDirection","shootGumball")],
                         [40,22,12])
        for child in self.seal["selected_consumers"]:
            prior=next(p["method"] for p in self.parent["selected_consumers"]
                       if p["method"]["name"]==child["name"])
            self.assertEqual(child["parsed_method_sha256"],prior["parsed_method_sha256"])

    def test_native_direction_switch_is_not_silently_omitted(self):
        bounce=next(x for x in self.seal["selected_consumers"]
                    if x["name"]=="bounceFromDirection")
        self.assertEqual(bounce["verified_switch_tables"],[{
            "offset":355,"opcode":"tableswitch","cases":[
                {"case":"1","target":380},
                {"case":"2","target":392},
                {"case":"3","target":404},
                {"case":"default","target":413},
            ]}])
        self.assertEqual(self.seal["limits"]["direct_switch_case_destinations"],
                         "VERIFIED_EXACT_JAVAP")

    def test_own_nbt_not_reload_proof(self):
        own=self.seal["gumball_own_nbt"]
        self.assertFalse(own["bounce_state_in_own_overrides"])
        self.assertEqual(own["inherited_engine_persistence"],"NOT_VERIFIED")
        self.assertEqual(own["write_method_sha256"],
                         "71d94d6babff7eb6ec1b9ff66f035c970ed9cfd4bf428cfbde1e6dfc9e7a52cf")
        self.assertEqual(own["read_method_sha256"],
                         "6ab17f1d19425646dc4e5bf69274f479ff3634b7f552c005af6041c408c765e5")

    def test_certificate_has_seven_evidence_axes_and_no_mutation(self):
        cert=self.ledger["objects"][KEY]
        self.assertEqual(cert["status"],"COMPLETE_PERK_READY")
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(set(cert["evidence"]),
                         {"identity","behavior","parameters","targeting",
                          "costs","integration","validation"})
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(self.seal["limits"]["mutation"],"NO_MUTATION")

    def test_card_and_crosswalk_are_consistent_with_ledger(self):
        for token in ("M=4+2×L","74 desvios","tableswitch @355",
                      "NO_MUTATION","NOT_VERIFIED","NOT_TESTED",
                      "EXACT-BOUNCY-BALL-CAUSAL-1.0.10.json"):
            self.assertIn(token,self.card)
        number=sum(k.startswith("✅-alexs-caves-continued/enchantments/")
                   for k in self.ledger["objects"])
        self.assertIn(f"individual_full_enchantment_dossiers={number}/51",self.cross)
        self.assertIn(f"individual_partial_enchantment_dossiers={51-number}/51",self.cross)
        self.assertIn("| ✅ | "+chr(96)+"alexscaves:bouncy_ball",self.cross)

if __name__=="__main__":
    unittest.main()
