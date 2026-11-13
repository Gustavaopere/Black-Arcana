#!/usr/bin/env python3
"""Evidence-gated Charting Call 1.0.10 static dossier and ledger tests."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
META=ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
CARD=P/"enchantments/charting-call.md"
CROSS=P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md"
KEY="✅-alexs-caves-continued/enchantments/charting-call.md"

class ChartingCallCausalCardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((P/"EXACT-CHARTING-CALL-CAUSAL-1.0.10.json").read_text())
        cls.parent=json.loads((P/"EXACT-CHARTING-CALL-1.0.10.json").read_text())
        cls.ledger=json.loads(META.read_text())
        cls.card=CARD.read_text()
        cls.cross=CROSS.read_text()

    def test_jar_authority_and_original_seal(self):
        self.assertEqual(self.seal["artifact"],self.parent["artifact"])
        self.assertEqual(self.seal["artifact"]["sha256"],
                         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(self.seal["artifact"]["size_bytes"],75279314)

    def test_full_owner_census_not_provider_universe(self):
        owners=self.seal["owner_method_rosters"]
        self.assertEqual([c["declared_method_count"] for c in owners],[9,72])
        self.assertEqual(sum(x.get("declaration_only",False)
                             for c in owners for x in c["methods"]),3)
        self.assertFalse(self.seal["limits"]["provider_universe_closed"])
        self.assertEqual(len(self.seal["direct_class_token_CHARTING_CALL"]),2)
        self.assertTrue(any("MagicConchItem.class" in x
                            for x in self.seal["direct_class_token_CHARTING_CALL"]))

    def test_method_digests_and_direct_branch_destination_census(self):
        methods=self.seal["core_consumers"]
        self.assertEqual([m["name"] for m in methods],
                         [r["method"]["name"] for r in self.parent["selected_consumers"]])
        self.assertEqual([len(m["direct_branch_edges"]) for m in methods],[20,8,0,46])
        self.assertEqual([m["instruction_count"] for m in methods],[211,134,11,360])
        self.assertTrue(all(not m["verified_switch_tables"] for m in methods))
        for m in methods:
            old=next(x["method"] for x in self.parent["selected_consumers"]
                     if x["method"]["name"]==m["name"])
            self.assertEqual(m["parsed_method_sha256"],old["parsed_method_sha256"])

    def test_zero_bounds_are_static_and_no_runtime_crash_claim(self):
        release=self.seal["core_consumers"][0]
        expected={"deep_one":("iconst_2","Math.max:","RandomSource.nextInt:"),
                  "knight":("iconst_0","Math.max:","RandomSource.nextInt:"),
                  "mage":("iconst_0","Math.max:","RandomSource.nextInt:")}
        for family, (bound,maximum,rng) in expected.items():
            seq=release["verified_rng_bound_sequences"][family]
            self.assertEqual(seq[3]["opcode"],bound)
            self.assertIn(maximum,seq[4]["symbol"])
            self.assertIn(rng,seq[5]["symbol"])
        self.assertEqual(self.seal["limits"]["RandomSource_nextInt_zero_runtime_result"],
                         "NOT_TESTED")
        self.assertIn("não um crash reproduzido",self.card)

    def test_summon_nbt_and_native_related_consumers(self):
        store=self.seal["summon_nbt_overrides"]
        self.assertEqual([store[k]["instruction_count"] for k in
                          ("addAdditionalSaveData","readAdditionalSaveData")],[56,62])
        for data in store.values():
            self.assertEqual(data["required_nbt_keys"],
                             ["ConchSummoned","ConchUUID","ConchTime"])
        rel={x["owner"].rsplit("/",1)[-1]:
             {m["name"] for m in x["methods"]}
             for x in self.seal["related_native_methods"]}
        self.assertTrue({"copyTarget","isAlliedTo","getReactionTo",
                         "addAdditionalSaveData","readAdditionalSaveData"}
                        <=rel["DeepOneBaseEntity.class"])

    def test_perk_ready_means_static_only(self):
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

    def test_card_crosswalk_and_counts(self):
        for token in ("81 métodos declarados","74 branches diretos",
                      "EXACT-CHARTING-CALL-CAUSAL-1.0.10.json",
                      "NO_MUTATION","NOT_VERIFIED","NOT_TESTED"):
            self.assertIn(token,self.card)
        n=sum(k.startswith("✅-alexs-caves-continued/enchantments/")
              for k in self.ledger["objects"])
        self.assertEqual(n,36)
        self.assertIn(f"individual_full_enchantment_dossiers={n}/51",self.cross)
        self.assertIn(f"individual_partial_enchantment_dossiers={51-n}/51",self.cross)
        self.assertIn("| ✅ | "+chr(96)+"alexscaves:charting_call",self.cross)

if __name__=="__main__":
    unittest.main()
