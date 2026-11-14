#!/usr/bin/env python3
"""Chomping Spirit exact static seal, dossier, safe ledger and index checks."""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
META=ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
KEY="✅-alexs-caves-continued/enchantments/chomping-spirit.md"

class ChompingSpiritStaticCardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads(
            (PROVIDER/"EXACT-CHOMPING-SPIRIT-CAUSAL-1.0.10.json").read_text())
        cls.parent=json.loads(
            (PROVIDER/"EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json").read_text())
        cls.ledger=json.loads(META.read_text())
        cls.card=(PROVIDER/"enchantments/chomping-spirit.md").read_text()
        cls.cross=(PROVIDER/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        cls.global_index=(ROOT/"wiki/modpack-catalog/providers/INDEX.md").read_text()
        cls.mod_index=(PROVIDER/"INDEX.md").read_text()

    def test_exact_artifact_authority_and_full_report_binding(self):
        self.assertEqual(self.seal["artifact"]["sha1"],
                         self.parent["artifact_sha1"])
        self.assertEqual(self.seal["artifact"]["sha256"],
                         self.parent["artifact_sha256"])
        self.assertEqual(self.seal["artifact"]["size_bytes"],
                         self.parent["artifact_size_bytes"])
        self.assertEqual(self.seal["full_report_sha256"],
                         "44e8552ba4a803a2c8735fe78803795f37c63ac66e56624acc519167d29ab814")
        self.assertRegex(self.seal["parent_manifest_sha256"],r"^[0-9a-f]{64}$")

    def test_four_native_owner_rosters(self):
        self.assertEqual(self.seal["owner_method_counts"],{
            "ExtinctionSpearItem.class":9,"SpearItem.class":12,
            "DinosaurSpiritEntity.class":32,"ExtinctionSpearEntity.class":18})
        self.assertEqual(sum(self.seal["owner_method_counts"].values()),71)
        self.assertEqual(self.seal["direct_class_token_CHOMPING_SPIRIT"],[
            "com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class",
            "com/github/alexmodguy/alexscaves/server/item/ExtinctionSpearItem.class"])

    def test_native_damage_producer_and_consumer_hashes(self):
        digests=self.seal["core_method_sha256"]
        self.assertEqual(set(digests),{
            "ExtinctionSpearItem.acHurtEnemy","SpearItem.acHurtEnemy",
            "DinosaurSpiritEntity.tick","DinosaurSpiritEntity.tickTremorsaurus",
            "ExtinctionSpearEntity.onHitEntity"})
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{64}",x)
                            for x in digests.values()))
        self.assertEqual(self.seal["core_direct_branch_counts"],{
            "ExtinctionSpearItem.acHurtEnemy":0,
            "SpearItem.acHurtEnemy":0,
            "DinosaurSpiritEntity.tick":20,
            "DinosaurSpiritEntity.tickTremorsaurus":10,
            "ExtinctionSpearEntity.onHitEntity":8})

    def test_three_species_jvm_dispatch_verified(self):
        self.assertEqual(self.seal["dispatcher_switch_cases"],[{
            "offset":279,"opcode":"tableswitch","cases":[
                {"case":"0","target":304},{"case":"1","target":312},
                {"case":"2","target":320},{"case":"default","target":325}
            ]}])

    def test_nbt_has_only_two_explicit_own_keys(self):
        for name in ("addAdditionalSaveData","readAdditionalSaveData"):
            entry=self.seal["spirit_own_nbt_overrides"][name]
            self.assertEqual(entry["instruction_count"],15)
            self.assertEqual(entry["exact_own_nbt_keys"],
                             ["UsingPlayerUUID","DinosaurType"])
            self.assertFalse(entry["enchantment_level_and_victim_id_in_own_overrides"])
            self.assertEqual(entry["inherited_engine_persistence"],"NOT_VERIFIED")

    def test_static_certificate_has_seven_evidence_axes_and_no_hook(self):
        cert=self.ledger["objects"][KEY]
        self.assertEqual(cert["status"],"COMPLETE_PERK_READY")
        self.assertEqual(cert["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(cert["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(set(cert["evidence"]),{
            "identity","behavior","parameters","targeting","costs",
            "integration","validation"})
        self.assertEqual(cert["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(cert["physical_qa"],"NOT_TESTED")
        self.assertEqual(self.seal["limits"]["mutation"],"NO_MUTATION")
        self.assertEqual(self.seal["limits"]["runtime_hit_acceptance"],"NOT_TESTED")

    def test_card_names_distinct_throwing_damage_and_reload_boundary(self):
        for token in ("71 métodos declarados","38 desvios condicionais/goto",
                      "tableswitch","UsingPlayerUUID","DinosaurType",
                      "ENCHANTMENT_LEVEL","ATTACKING_ENTITY_ID",
                      "NO_MUTATION","NOT_VERIFIED","NOT_TESTED",
                      "EXACT-CHOMPING-SPIRIT-CAUSAL-1.0.10.json"):
            self.assertIn(token,self.card)
        self.assertIn("cadeia",self.card.lower())
        self.assertIn("distint",self.card.lower())

    def test_indexes_follow_ledger_without_rewriting(self):
        all_objects=self.ledger["objects"]
        enchantments=sum(k.startswith("✅-alexs-caves-continued/enchantments/")
                         for k in all_objects)
        alex=sum(k.startswith("✅-alexs-caves-continued/")
                 for k in all_objects)
        self.assertGreaterEqual(enchantments,37)
        self.assertIn(f"individual_full_enchantment_dossiers={enchantments}/51",
                      self.cross)
        self.assertIn(f"individual_partial_enchantment_dossiers={51-enchantments}/51",
                      self.cross)
        self.assertIn("| ✅ | "+chr(96)+"alexscaves:chomping_spirit",self.cross)
        self.assertIn(f"Fichas com contrato técnico estático certificado: {len(all_objects)}/",
                      self.global_index)
        self.assertIn(f"Fichas catalogadas (somente fichas detectadas): {alex}/81",
                      self.mod_index)

if __name__=="__main__":
    unittest.main()
