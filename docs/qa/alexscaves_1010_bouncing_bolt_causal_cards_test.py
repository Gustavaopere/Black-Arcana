#!/usr/bin/env python3
"""Bouncing Bolt static-only provenance/ledger regression."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL=P/"EXACT-BOUNCING-BOLT-CAUSAL-1.0.10.json"
PARENT=P/"EXACT-BOUNCING-BOLT-1.0.10.json"
LEDGER=ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
CARD=P/"enchantments/bouncing-bolt.md"
CROSS=P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md"
class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SEAL.read_text(encoding="utf8"))
        cls.parent=json.loads(PARENT.read_text(encoding="utf8"))
        cls.ledger=json.loads(LEDGER.read_text(encoding="utf8"))
    def test_exact_two_class_28_method_census(self):
        d=self.d
        self.assertEqual(d["artifact"],self.parent["artifact"])
        self.assertEqual([x["declared_method_count"] for x in d["classes"]],[7,21])
        self.assertEqual({x["name"]:len(x["all_branch_edges"]) for x in d["consumers"]},
                         {"use":17,"damageMobs":14,"onRicochetHit":13})
        for m in d["consumers"]:
            self.assertEqual(m["parsed_method_sha256"],next(
                x["method"]["parsed_method_sha256"] for x in self.parent["consumers"]
                if x["method"]["name"]==m["name"]))
    def test_flag_consumed_and_child_is_conditional(self):
        c={x["name"]:x for x in self.d["consumers"]}
        pin=lambda name,off:next(x for x in c[name]["verified_pivots"] if x["offset"]==off)
        self.assertIn("ricochet",pin("use",311)["symbol"])
        self.assertIn("ricochet",pin("damageMobs",233)["symbol"])
        self.assertIn("onRicochetHit",pin("damageMobs",239)["symbol"])
        self.assertIn("getEntitiesOfClass",pin("onRicochetHit",32)["symbol"])
        self.assertIn("addFreshEntity",pin("onRicochetHit",266)["symbol"])
        self.assertEqual(pin("onRicochetHit",156)["operand"],"270")
        self.assertEqual(pin("onRicochetHit",163)["operand"],"270")
        ctor=next(x for x in self.d["classes"][1]["methods"]
                  if x["name"]=="WaterBoltEntity" and "EntityType;" in x["descriptor"])
        self.assertTrue(any("ricochet" in x["symbol"] for x in ctor["relevant_symbolic_refs"]))
    def test_scoped_certificate_not_runtime_authorization(self):
        cert=self.ledger["objects"]["✅-alexs-caves-continued/enchantments/bouncing-bolt.md"]
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["status"],"COMPLETE_PERK_READY")
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(cert["evidence"]),
                         {"identity","behavior","parameters","targeting",
                          "costs","integration","validation"})
        self.assertEqual(self.d["limits"]["mutation"],"NO_MUTATION")
        self.assertEqual(self.d["limits"]["certification"],"STATIC_TECHNICAL_CATALOG_ONLY")
    def test_dossier_crosswalk_and_limits(self):
        card=CARD.read_text(encoding="utf8")
        cross=CROSS.read_text(encoding="utf8")
        for t in ("NO_MUTATION","NOT_VERIFIED","NOT_TESTED","32D","3D",
                  "ricochet=false","EXACT-BOUNCING-BOLT-CAUSAL-1.0.10.json"):
            self.assertIn(t,card)
        self.assertIn("individual_full_enchantment_dossiers=34/51",cross)
        self.assertIn("individual_partial_enchantment_dossiers=17/51",cross)
        self.assertIn("| ✅ | `alexscaves:bouncing_bolt`",cross)
if __name__=="__main__":
    unittest.main()
