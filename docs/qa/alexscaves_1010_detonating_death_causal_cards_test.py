#!/usr/bin/env python3
"""Detonating Death SHA seal, 7-axis certificate, crosswalk and index checks."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
LEDGER = ROOT / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
KEY = "✅-alexs-caves-continued/enchantments/detonating-death.md"
T = "com/github/alexmodguy/alexscaves/server/item/TotemOfPossessionItem.class"
X = "com/github/alexmodguy/alexscaves/server/entity/util/TotemExplosion.class"

class DetonatingDeathStaticCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads((P / "EXACT-DETONATING-DEATH-CAUSAL-1.0.10.json")
                              .read_text(encoding="utf8"))
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf8"))
        cls.card = (P / "enchantments/detonating-death.md").read_text(encoding="utf8")
        cls.cross = (P / "ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text(
            encoding="utf8")
        cls.mod_index = (P / "INDEX.md").read_text(encoding="utf8")
        cls.enchant_index = (P / "enchantments/INDEX.md").read_text(encoding="utf8")
        cls.global_index = (ROOT / "wiki/modpack-catalog/providers/INDEX.md").read_text(
            encoding="utf8")

    def test_individual_publisher_sha_seal(self):
        s = self.seal
        self.assertEqual(s["schema_version"],1)
        self.assertEqual(s["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(s["artifact"]["size_bytes"],75279314)
        self.assertEqual(s["artifact"]["sha256"],
            "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(s["parent_manifest_sha256"],
            "3af3efd097dc60f2877211604a49543275f6d2b9ac24d1e9050ed175fe0382ef")
        self.assertEqual(s["full_report_sha256"],
            "8a90445bd7e3b32569c3d81896970df064f2cbf217b9ca9beb9b20233545db9b")
        self.assertEqual(set(s["native_method_sha256"]),{T,X})
        self.assertEqual(sum(map(len,s["native_method_sha256"].values())),3)
        self.assertEqual(sum(sum(m.values()) for m in
                             s["native_instruction_counts"].values()),1013)
        self.assertEqual(sum(sum(m.values()) for m in
                             s["native_direct_branch_counts"].values()),100)
        self.assertTrue(s["limits"]["detonation_branch_no_direct_side_guard"])
        self.assertFalse(s["limits"]["new_spell_root"])
        self.assertEqual(s["limits"]["mutation"],"NO_MUTATION")
        self.assertEqual(s["limits"]["physical_qa"],"NOT_TESTED")

    def test_seven_independent_static_evidence_axes(self):
        row=self.ledger["objects"][KEY]
        self.assertEqual(row["status"],"COMPLETE_PERK_READY")
        self.assertEqual(row["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(row["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(row["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(row["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(row["evidence"]),{
            "identity","behavior","parameters","targeting","costs",
            "integration","validation"})
        for k,proof in row["evidence"].items():
            self.assertEqual(proof["path"],"wiki/modpack-catalog/providers/"+KEY)
            self.assertGreater(len(proof["reason"]),40,k)

    def test_fiche_does_not_promote_runtime(self):
        for token in ("contrato técnico estático individual certificado",
                      "1.013 instruções","100 branches", "50 âncoras",
                      "NO_MUTATION", "NOT_TESTED", "NOT_VERIFIED",
                      "STATIC_TECHNICAL_CATALOG_ONLY", "2+floor"):
            self.assertIn(token,self.card)

    def test_ledger_derived_indexes_and_alpha_row(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts/catalog"))
        import check_perk_ready_indexes as canonical
        provider_cards = [card for card in P.rglob("*.md")
                          if canonical.is_card(card)]
        global_cards = [card for card in canonical.PROVIDERS.rglob("*.md")
                        if canonical.is_card(card)]
        keys=self.ledger["objects"]
        global_count=sum(canonical.certified(card, self.ledger) for card in global_cards)
        provider_count=sum(canonical.certified(card, self.ledger) for card in provider_cards)
        enchant_count=sum(k.startswith("✅-alexs-caves-continued/enchantments/")
                          for k in keys)
        self.assertGreaterEqual(global_count,207)
        self.assertGreaterEqual(provider_count,69)
        self.assertGreaterEqual(enchant_count,41)
        self.assertIn(f"individual_full_enchantment_dossiers={enchant_count}/51",
                      self.cross)
        self.assertIn(f"individual_partial_enchantment_dossiers={51-enchant_count}/51",
                      self.cross)
        self.assertIn("| ✅ | " + chr(96) + "alexscaves:detonating_death", self.cross)
        self.assertIn("| ✅ | Detonating Death |", self.enchant_index)
        self.assertIn("| ✅ | Detonating Death |", self.mod_index)
        self.assertIn(f"Fichas catalogadas (somente fichas detectadas): {enchant_count}/51",
                      self.enchant_index)
        self.assertIn(f"Fichas catalogadas (somente fichas detectadas): {provider_count}/{len(provider_cards)}",
                      self.mod_index)
        self.assertIn(f"Fichas com contrato técnico estático certificado: {global_count}/{len(global_cards)}",
                      self.global_index)
        self.assertIn("Providers com catálogo concluído: 4/164",
                      self.global_index)
        self.assertIn("Mods com escopo integral certificado: 0/164",
                      self.global_index)

if __name__=="__main__":
    unittest.main()
