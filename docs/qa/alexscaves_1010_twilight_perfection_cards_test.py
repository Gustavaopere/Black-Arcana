#!/usr/bin/env python3
"""Crosscheck the 51st publisher enchantment's static certificate and boundaries."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PROV=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
CARD=PROV/"enchantments/twilight-perfection.md"
SEAL=PROV/"EXACT-TWILIGHT-PERFECTION-CONTRACT-1.0.10.json"
LEDGER=ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
CROSS=PROV/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md"

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SEAL.read_text(encoding="utf8"))
        cls.ledger=json.loads(LEDGER.read_text(encoding="utf8"))
        cls.card=CARD.read_text(encoding="utf8")
        cls.cross=CROSS.read_text(encoding="utf8")

    def test_publisher_and_five_class_hashes(self):
        d=self.d
        self.assertEqual(d["enchantment_id"],"alexscaves:twilight_perfection")
        self.assertEqual(d["resource"]["size_bytes"],367)
        self.assertEqual(d["resource"]["json"]["max_level"],3)
        self.assertEqual(d["resource"]["json"]["weight"],2)
        self.assertEqual(d["artifact"]["size_bytes"],75279314)
        self.assertEqual(len(d["class_hashes"]),5)
        self.assertIn("alexscaves:twilight_perfection",d["neighbor_exclusion"]["exclusive_set"])

    def test_nine_unique_methods_and_server_boundary(self):
        methods=self.d["evidence"]
        self.assertEqual(len(methods),9)
        self.assertEqual(len({(x["method"],x["descriptor"]) for x in methods}),9)
        self.assertTrue(all(len(x["parent_method_anchors_sha256"])==64 and
                            x["verified_pivots"]==len(x["pivots"]) for x in methods))
        self.assertEqual(self.d["limits"]["safe_mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(self.d["limits"]["mutation"],"NO_MUTATION")
        self.assertEqual(self.d["limits"]["client_to_server_tag_authority"],"NOT_VERIFIED")

    def test_static_certificate_has_seven_axes(self):
        key="✅-alexs-caves-continued/enchantments/twilight-perfection.md"
        cert=self.ledger["objects"][key]
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(cert["evidence"]),
                         {"identity","behavior","parameters","targeting",
                          "costs","integration","validation"})

    def test_complete_individual_card_and_family_accounting(self):
        for phrase in ("TWILIGHT_PERFECTION","PerfectShotTicks","4+3",
                       "acInventoryTick","releaseUsing","setPerfectShot",
                       "ACCompat.hurt","UpdateItemTagMessage",
                       "128F","42F","NO_MUTATION","NOT_TESTED","NOT_VERIFIED"):
            self.assertIn(phrase,self.card)
        self.assertIn("individual_full_enchantment_dossiers=30/51",self.cross)
        self.assertIn("individual_partial_enchantment_dossiers=21/51",self.cross)
        self.assertIn("individual_existing_enchantment_dossiers=51/51",self.cross)

    def test_no_accidental_runtime_certificate(self):
        for phrase in ("provider_universe_closed=false","NO_MUTATION",
                       "client_to_server_tag_authority"):
            self.assertIn(phrase,self.card if phrase!="client_to_server_tag_authority" else json.dumps(self.d))
        self.assertFalse(self.d["limits"]["provider_universe_closed"])

if __name__=="__main__":
    unittest.main()
