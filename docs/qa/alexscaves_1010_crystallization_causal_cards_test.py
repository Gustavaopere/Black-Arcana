#!/usr/bin/env python3
"""Static-only Crystallization SHA-exact card, seal, ledger and indexes gates."""
from __future__ import annotations
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
KEY="✅-alexs-caves-continued/enchantments/crystallization.md"

class CrystallizationStaticCardsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal=json.loads((P/"EXACT-CRYSTALLIZATION-CAUSAL-1.0.10.json").read_text())
        cls.parent=json.loads((P/"EXACT-CRYSTALLIZATION-1.0.10.json").read_text())
        cls.ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cls.card=(P/"enchantments/crystallization.md").read_text()
        cls.cross=(P/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text()
        cls.ench_index=(P/"enchantments/INDEX.md").read_text()
        cls.provider_index=(P/"INDEX.md").read_text()
        cls.global_index=(ROOT/"wiki/modpack-catalog/providers/INDEX.md").read_text()

    def test_pinned_artifact_and_unabridged_report_hash(self):
        self.assertEqual(self.seal["artifact"],self.parent["artifact"])
        self.assertEqual(self.seal["artifact"]["sha256"],
                         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        self.assertEqual(self.seal["artifact"]["size_bytes"],75279314)
        self.assertEqual(self.seal["full_report_sha256"],
                         "8927e0f12b8b20922008a20c8ed000d1f8b2d6516b7f87abd58e339501ca86ba")
        self.assertRegex(self.seal["parent_manifest_sha256"],r"^[0-9a-f]{64}$")

    def test_resources_preserve_exact_original_seals(self):
        self.assertEqual(self.seal["resources_sha256"],
                         {k:v["sha256"] for k,v in self.parent["resource_evidence"].items()})
        self.assertEqual(self.parent["resource_evidence"]["enchantment"]
                         ["json"]["max_level"],1)
        self.assertEqual(len(self.parent["resource_evidence"]["crystallization"]
                             ["json"]["values"]),10)
        self.assertEqual(len(self.parent["resource_evidence"]["ferromagnetic"]
                             ["json"]["values"]),82)

    def test_two_native_owners_and_eleven_reconciled_consumers(self):
        self.assertEqual(self.seal["owner_method_counts"],{
            "GalenaGauntletItem.class":17,"MagneticWeaponEntity.class":23})
        digest=self.seal["consumer_method_sha256"]
        counts=self.seal["consumer_instruction_counts"]
        self.assertEqual(len(digest),11)
        self.assertEqual(len(counts),11)
        self.assertEqual(set(counts),set(digest))
        self.assertTrue(all(re.fullmatch("[0-9a-f]{64}",v) for v in digest.values()))
        self.assertEqual(counts["MagneticWeaponEntity.tick"],744)
        self.assertEqual(counts["GalenaGauntletItem.onUseTick"],120)

    def test_exact_direct_cfg_counts_and_no_selected_switch(self):
        self.assertEqual(self.seal["consumer_direct_branch_counts"],{
            "GalenaGauntletItem.use":8,
            "GalenaGauntletItem.onUseTick":15,
            "GalenaGauntletItem.releaseUsing":1,
            "MagneticWeaponEntity.tick":82,
            "MagneticWeaponEntity.hurtEntity":10,
            "MagneticWeaponEntity.getController":5,
            "MagneticWeaponEntity.getTarget":2,
            "MagneticWeaponEntity.isOwnerWearingGauntlet":5,
            "MagneticWeaponEntity.plopItem":2,
            "MagneticWeaponEntity.addAdditionalSaveData":2,
            "MagneticWeaponEntity.readAdditionalSaveData":2,
        })
        self.assertEqual(sum(self.seal["consumer_direct_branch_counts"].values()),134)
        self.assertEqual(self.seal["consumer_switch_tables"],{})

    def test_crystallization_native_token_census(self):
        self.assertEqual(self.seal["direct_CRYSTALLIZATION_class_tokens"],[
            "com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class",
            "com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem.class",
            "com/github/alexmodguy/alexscaves/server/misc/ACTagRegistry.class",
        ])

    def test_native_inventory_order_precedes_spawn_and_discards_result(self):
        pivots=self.seal["consumer_pivots"]["GalenaGauntletItem.onUseTick"]
        rows={x["offset"]:x for x in pivots}
        for offset,token in ((193,"ItemStack.copy:"),(201,"ItemStack.setCount:"),
                             (216,"createEntity:"),(228,"setItemStack:"),
                             (252,"setControllerUUID:"),(258,"addFreshEntity:")):
            self.assertIn(token,rows[offset]["symbol"])
        self.assertEqual(rows[261]["opcode"],"pop")
        self.assertEqual([rows[x]["opcode"] for x in (112,115,118)],
                         ["ldc2_w"]*3)
        self.assertTrue(all("64.0" in rows[x]["symbol"] for x in (112,115,118)))
        self.assertEqual(self.seal["limits"]["spawn_acceptance_after_setCount0"],
                         "NOT_TESTED")

    def test_native_own_nbt_keys_do_not_claim_successful_reload(self):
        nbt=self.seal["own_magnetic_weapon_nbt_overrides"]
        self.assertEqual(set(nbt),{"addAdditionalSaveData","readAdditionalSaveData"})
        for entry in nbt.values():
            self.assertEqual(entry["instruction_count"],23)
            self.assertEqual(entry["explicit_keys"],["WeaponStack","ControllerUUID"])
            self.assertEqual(entry["actual_inventory_restoration"],"NOT_TESTED")
            self.assertEqual(entry["inherited_engine_state"],"NOT_VERIFIED")

    def test_seven_evidence_axes_static_contract_no_mutation(self):
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

    def test_card_scope_and_all_indexes_consistent_with_ledger(self):
        for text in ("40 métodos declarados","134 branches",
                     "EXACT-CRYSTALLIZATION-CAUSAL-1.0.10.json",
                     "WeaponStack","ControllerUUID","NO_MUTATION",
                     "NOT_VERIFIED","NOT_TESTED"):
            self.assertIn(text,self.card)
        objects=self.ledger["objects"]
        n_global=len(objects)
        n_provider=sum(k.startswith("✅-alexs-caves-continued/")
                       for k in objects)
        n_enchant=sum(k.startswith("✅-alexs-caves-continued/enchantments/")
                      for k in objects)
        self.assertGreaterEqual(n_enchant,38)
        self.assertIn(f"individual_full_enchantment_dossiers={n_enchant}/51",
                      self.cross)
        self.assertIn(f"individual_partial_enchantment_dossiers={51-n_enchant}/51",
                      self.cross)
        self.assertIn("| ✅ | "+chr(96)+"alexscaves:crystallization",self.cross)
        self.assertIn(f"Fichas catalogadas (somente fichas detectadas): {n_enchant}/51",
                      self.ench_index)
        self.assertIn(f"Fichas catalogadas (somente fichas detectadas): {n_provider}/81",
                      self.provider_index)
        self.assertIn(f"Fichas com contrato técnico estático certificado: {n_global}/2393",
                      self.global_index)

if __name__=="__main__":
    unittest.main()
