#!/usr/bin/env python3
"""Double Stab individual publisher certificate/ledger/index and scope tests."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
KEY = "✅-alexs-caves-continued/enchantments/double-stab.md"
I = "com/github/alexmodguy/alexscaves/server/item/DesolateDaggerItem.class"
E = "com/github/alexmodguy/alexscaves/server/entity/item/DesolateDaggerEntity.class"
C = "com/github/alexmodguy/alexscaves/server/misc/ACCompat.class"
D = "com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class"

class DoubleStabStaticCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((P/"EXACT-DOUBLE-STAB-CAUSAL-1.0.10.json")
                            .read_text(encoding="utf8"))
        cls.ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json")
                              .read_text(encoding="utf8"))
        cls.card=(P/"enchantments/double-stab.md").read_text(encoding="utf8")
        cls.cross=(P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text(encoding="utf8")
        cls.provider=(P/"INDEX.md").read_text(encoding="utf8")
        cls.enchants=(P/"enchantments/INDEX.md").read_text(encoding="utf8")
        cls.global_index=(ROOT/"wiki/modpack-catalog/providers/INDEX.md").read_text(
            encoding="utf8")

    def test_exact_version_class_hashes_and_full_report(self):
        s=self.seal
        self.assertEqual(s["schema_version"],1)
        self.assertEqual(s["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(s["artifact"]["size_bytes"],75279314)
        self.assertEqual(s["artifact"]["sha256"],
            "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(s["parent_manifest_sha256"],
            "e9f23c323fb9a04af9ac215b1e589de5933d99e70d9e8b96c91a4e7421d58ff1")
        self.assertEqual(s["full_report_sha256"],
            "7b9dfd24d8af0f89cd96adddcf1a95ed7bfde71adbcfba2275be17f0891d05b0")
        self.assertEqual(set(s["native_method_sha256"]), {I,E,C,D})
        self.assertEqual(sum(map(len,s["native_method_sha256"].values())),12)
        self.assertEqual(sum(sum(ms.values()) for ms in
                             s["native_instruction_counts"].values()),507)
        self.assertEqual(sum(sum(ms.values()) for ms in
                             s["native_direct_branch_counts"].values()),32)
        self.assertEqual(sum(sum(ms.values()) for ms in
                             s["native_historical_anchor_counts"].values()),391)
        self.assertEqual(s["native_method_sha256"][I]["acSpawnDaggers"],
            "e0dd34391401c5794681af190285f62a591a35868e62914c9ddf491f633c9914")
        self.assertEqual(s["native_method_sha256"][E]["tick"],
            "86b8a9b6831bf179710d06128a324cf7c0e5423b81402c598310d5cd32caf165")

    def test_no_new_spell_or_executable_perk_claim(self):
        s=self.seal
        self.assertFalse(s["limits"]["new_spell_root"])
        self.assertFalse(s["limits"]["independent_projectile_spell"])
        self.assertFalse(s["limits"]["provider_universe_closed"])
        self.assertEqual(s["limits"]["mutation"],"NO_MUTATION")
        self.assertEqual(s["limits"]["physical_qa"],"NOT_TESTED")
        self.assertEqual(s["limits"]["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(s["nominal_spawn_attempts"]["level_1"],2)
        self.assertEqual(s["nominal_spawn_attempts"]["no_enchant"],1)
        self.assertEqual(s["nominal_spawn_attempts"]["accepted_spawns"],"NOT_VERIFIED")

    def test_seven_axis_individual_evidence(self):
        cert=self.ledger["objects"][KEY]
        self.assertEqual(cert["status"],"COMPLETE_PERK_READY")
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(cert["evidence"]),{
            "identity","behavior","parameters","targeting","costs",
            "integration","validation"})
        for k,v in cert["evidence"].items():
            self.assertEqual(v["path"],"wiki/modpack-catalog/providers/"+KEY)
            self.assertGreater(len(v["reason"]),55,k)

    def test_card_maintains_runtime_and_causal_distinctions(self):
        for token in ("contrato técnico estático individual certificado",
                      "507 instruções", "32 branches", "391 âncoras",
                      "NO_MUTATION", "NOT_TESTED", "NOT_VERIFIED",
                      "1+L", "addFreshEntity", "setPlayerId",
                      "DOUBLE_STAB", "IMPENDING_STAB",
                      "7b9dfd24d8af0f89cd96adddcf1a95ed7bfde71adbcfba2275be17f0891d05b0"):
            self.assertIn(token,self.card)

    def test_individual_counts_derive_from_canonical_ledger(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts/catalog"))
        import check_perk_ready_indexes as canonical
        provider_cards = [card for card in P.rglob("*.md")
                          if canonical.is_card(card)]
        global_cards = [card for card in canonical.PROVIDERS.rglob("*.md")
                        if canonical.is_card(card)]
        keys=self.ledger["objects"]
        all_count=sum(canonical.certified(card, self.ledger) for card in global_cards)
        mod_count=sum(canonical.certified(card, self.ledger) for card in provider_cards)
        enchant_count=sum(k.startswith("✅-alexs-caves-continued/enchantments/")
                          for k in keys)
        self.assertGreaterEqual(all_count,208)
        self.assertGreaterEqual(mod_count,70)
        self.assertGreaterEqual(enchant_count,42)
        self.assertIn("individual_full_enchantment_dossiers="+str(enchant_count)+"/51",self.cross)
        self.assertIn("individual_partial_enchantment_dossiers="+str(51-enchant_count)+"/51",self.cross)
        self.assertIn("| ✅ | "+chr(96)+"alexscaves:double_stab",self.cross)
        self.assertIn("| ✅ | Double Stab |",self.enchants)
        self.assertIn("| ✅ | Double Stab |",self.provider)
        self.assertIn("Fichas catalogadas (somente fichas detectadas): "+str(mod_count)+"/"+str(len(provider_cards)),self.provider)
        self.assertIn("Fichas catalogadas (somente fichas detectadas): "+str(enchant_count)+"/51",self.enchants)
        self.assertIn("Fichas com contrato técnico estático certificado: "+str(all_count)+"/"+str(len(global_cards)),self.global_index)
        self.assertIn("Providers com catálogo concluído: 4/164",self.global_index)
        self.assertIn("Mods com escopo integral certificado: 0/164",self.global_index)

if __name__=="__main__":
    unittest.main()
