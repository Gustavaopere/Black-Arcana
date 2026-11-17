#!/usr/bin/env python3
"""Dazing Sweep SHA-exact static certificate/card/index cross-checks."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
LEDGER = ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
KEY = "✅-alexs-caves-continued/enchantments/dazing-sweep.md"
CLUB = "com/github/alexmodguy/alexscaves/server/item/PrimitiveClubItem.class"
EFFECT = "com/github/alexmodguy/alexscaves/server/potion/StunnedEffect.class"
MSG = ("com/github/alexmodguy/alexscaves/server/message/"
       "UpdateEffectVisualityEntityMessage.class")


class DazingSweepCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads((P / "EXACT-DAZING-SWEEP-CAUSAL-1.0.10.json")
                              .read_text(encoding="utf8"))
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf8"))
        cls.card = (P / "enchantments/dazing-sweep.md").read_text(encoding="utf8")
        cls.cross = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text(encoding="utf8")
        cls.provider = (P / "INDEX.md").read_text(encoding="utf8")
        cls.enchants = (P / "enchantments/INDEX.md").read_text(encoding="utf8")
        cls.global_index = (ROOT / "wiki/modpack-catalog/providers/INDEX.md").read_text(
            encoding="utf8")

    def test_native_roster_and_report_integrity(self):
        s = self.seal
        self.assertEqual(s["full_report_sha256"],
            "482459c63770efb81317f4e50000b66053c0c70cc372284e5da15def6324cf4e")
        self.assertEqual(s["parent_manifest_sha256"],
            "4aa87c312a4c35d5ab6aa126bd8c47f08e842b7f5e1844ad359b6a220443626b")
        self.assertEqual(s["artifact"]["sha256"],
            "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(s["artifact"]["size_bytes"], 75279314)
        self.assertEqual(s["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(len(s["native_DAZING_SWEEP_class_tokens"]), 2)
        self.assertEqual(set(s["consumer_method_sha256"]), {CLUB, EFFECT, MSG})
        self.assertEqual(sum(len(v) for v in s["consumer_method_sha256"].values()), 5)
        self.assertEqual(sum(sum(v.values())
                         for v in s["consumer_instruction_counts"].values()), 363)
        self.assertEqual(sum(sum(v.values())
                         for v in s["consumer_direct_branch_counts"].values()), 29)
        tables = s["consumer_validated_switch_tables"]
        self.assertEqual(tables[CLUB]["acHurtEnemy"], [])
        self.assertEqual(tables[EFFECT]["tick"], [])
        self.assertEqual(len(tables[MSG]["handle"]), 1)
        self.assertEqual(tables[MSG]["handle"][0]["offset"], 100)
        self.assertEqual(len(tables[MSG]["handle"][0]["cases"]), 6)

    def test_geometry_and_native_cost_scope(self):
        self.assertEqual(self.seal["nominal_geometry"], [
            {"level":1,"aabb_side":2.2,"aabb_half_side":1.1,
             "distance_filter":2.2},
            {"level":2,"aabb_side":3.2,"aabb_half_side":1.6,
             "distance_filter":3.2}])
        for token in ("L+1.2F", "150–299", "80–159",
                      "1.0F", "AABB.ofSize", "mobAttack",
                      "pop @322", "NO_MUTATION"):
            self.assertIn(token, self.card)

    def test_seven_axes_and_no_physical_qa(self):
        cert = self.ledger["objects"][KEY]
        self.assertEqual(cert["status"], "COMPLETE_PERK_READY")
        self.assertEqual(cert["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["evidence_grade"], "SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(set(cert["evidence"]), {
            "identity", "behavior", "parameters", "targeting", "costs",
            "integration", "validation"})
        self.assertEqual(cert["mutating_hook"], "NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"], "NOT_TESTED")
        self.assertEqual(self.seal["limits"]["mutation"], "NO_MUTATION")
        self.assertFalse(self.seal["limits"]["whole_provider_closed"])
        self.assertEqual(self.seal["limits"]["server_effect_acceptance"],
                         "NOT_TESTED")

    def test_card_crosswalk_and_three_indexes(self):
        self.assertIn("contrato técnico estático individual certificado", self.card)
        self.assertIn("363 instruções", self.card)
        self.assertIn("29 branches diretos", self.card)
        self.assertIn("EXACT-DAZING-SWEEP-CAUSAL-1.0.10.json", self.card)
        import sys
        sys.path.insert(0, str(ROOT / "scripts/catalog"))
        import check_perk_ready_indexes as canonical
        provider_cards = [card for card in P.rglob("*.md")
                          if canonical.is_card(card)]
        global_cards = [card for card in canonical.PROVIDERS.rglob("*.md")
                        if canonical.is_card(card)]
        objects = self.ledger["objects"]
        n_global = sum(canonical.certified(card, self.ledger) for card in global_cards)
        n_provider = sum(canonical.certified(card, self.ledger) for card in provider_cards)
        n_enchant = sum(k.startswith("✅-alexs-caves-continued/enchantments/")
                        for k in objects)
        self.assertGreaterEqual(n_global, 206)
        self.assertGreaterEqual(n_provider, 68)
        self.assertGreaterEqual(n_enchant, 40)
        self.assertIn(f"individual_full_enchantment_dossiers={n_enchant}/51",self.cross)
        self.assertIn(f"individual_partial_enchantment_dossiers={51-n_enchant}/51",self.cross)
        self.assertIn("| ✅ | " + chr(96) + "alexscaves:dazing_sweep" + chr(96),
                      self.cross)
        self.assertIn("| ✅ | Dazing Sweep |",self.provider)
        self.assertIn("| ✅ | Dazing Sweep |",self.enchants)
        self.assertIn(f"Fichas catalogadas (somente fichas detectadas): {n_enchant}/51",
                      self.enchants)
        self.assertIn(f"Fichas catalogadas (somente fichas detectadas): {n_provider}/{len(provider_cards)}",
                      self.provider)
        self.assertIn(f"Fichas com contrato técnico estático certificado: {n_global}/{len(global_cards)}",
                      self.global_index)
        self.assertRegex(self.global_index,
            rf"Fichas catalogadas \(somente fichas detectadas\): [0-9]+/{len(global_cards)}")
        self.assertIn("Providers com catálogo concluído: 4/164",
                      self.global_index)

if __name__ == "__main__":
    unittest.main()
