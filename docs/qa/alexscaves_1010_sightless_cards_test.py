#!/usr/bin/env python3
"""Sightless 1.0.10 individual static certificate semantic and bytecode tests.

Read-only JVM evidence. Does not test physical gameplay, hooks or authorization.
"""
from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
PROVIDER=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
MANIFEST=PROVIDER/"EXACT-SIGHTLESS-STATIC-1.0.10.json"
CARD=PROVIDER/"enchantments/sightless.md"
CERT=ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
ENTRY="✅-alexs-caves-continued/enchantments/sightless.md"

class SightlessStaticProof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(MANIFEST.read_text(encoding="utf8"))
        cls.card=CARD.read_text(encoding="utf8")
        cls.by={name:{row["offset"]:row for row in obj["bounded_instructions"]}
                for name,obj in cls.data["methods"].items()}
    def pivot(self,method,offset,*,op=None,symbol=None,operand=None):
        row=self.by[method].get(offset)
        self.assertIsNotNone(row,method+" @"+str(offset)+" missing in exact JVM seal")
        if op is not None: self.assertEqual(row["opcode"],op)
        if symbol is not None: self.assertIn(symbol,row["symbol"])
        if operand is not None: self.assertEqual(" ".join(row["operand"].split()),str(operand))
        return row
    def test_exact_json_tag_locale_and_separate_scope(self):
        d=self.data
        self.assertEqual(d["scope"],"EXACT_1010_SIGHTLESS_READONLY_DISCOVERY")
        self.assertEqual(d["artifact"]["sha256"],
                         "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c")
        e=d["enchantment"]
        self.assertEqual(e["size_bytes"],369)
        self.assertEqual(e["sha256"],"1e7d093a0d459e2e6a29b40cd625b4fb1f990285343b53e4421c8f3727b2ecb9")
        self.assertEqual(e["json"]["supported_items"],"#alexscaves:enchantable/totem_of_possession")
        self.assertEqual(e["json"]["weight"],2)
        self.assertEqual(e["json"]["max_level"],1)
        self.assertEqual(e["json"]["min_cost"],{"base":1,"per_level_above_first":13})
        self.assertEqual(e["json"]["max_cost"],{"base":41,"per_level_above_first":10})
        self.assertEqual(e["json"]["anvil_cost"],4)
        self.assertEqual(e["json"]["slots"],["mainhand"])
        self.assertNotIn("exclusive_set",e["json"])
        self.assertEqual(d["item_tag"]["json"],{"values":["alexscaves:totem_of_possession"]})
        self.assertEqual(d["translations"]["en_us"]["enchantment.alexscaves.sightless"],"Sightless")
        self.assertEqual(d["translations"]["pt_br"],{})
        self.assertEqual(d["limits"]["mutation"],"NO_MUTATION")
    def test_class_universe_and_method_fingerprints(self):
        d=self.data
        self.assertEqual(d["class_census"]["scanned"],1555)
        self.assertEqual(d["class_census"]["sightless_token_hits"],[
            "com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class",
            "com/github/alexmodguy/alexscaves/server/item/TotemOfPossessionItem.class"])
        self.assertEqual(len(d["class_sha256"]),3)
        self.assertEqual(len(d["methods"]),11)
        self.assertEqual(d["class_sha256"]["com/github/alexmodguy/alexscaves/server/item/TotemOfPossessionItem.class"],
                         "bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e")
        lengths={"use":66,"onUseTick":478,"releaseUsing":29,
                 "isEntityLookingAt":70,"getControlledEntity":44}
        for name,n in lengths.items(): self.assertEqual(d["methods"][name]["instructions_total"],n)
        self.assertEqual(d["methods"]["onUseTick"]["method_sha256"],
                         "4d366c998c89884f53bc9554f52c6477c5c6bbb8e6aea1bf0f93867dc1b41d39")
        self.assertEqual(d["methods"]["onUseTick"]["reused_anchors"],29)
    def test_start_positive_level_but_continue_zero_level_drift(self):
        self.pivot("use",99,symbol="double 5.0d")
        self.pivot("use",102,symbol="isEntityLookingAt")
        self.pivot("use",110,symbol="SIGHTLESS")
        self.pivot("use",113,symbol="ACCompat.enchantLevel")
        self.pivot("use",116,op="ifle",operand="145")
        self.pivot("use",136,symbol="startUsingItem")
        self.pivot("use",141,symbol="useConsume")
        self.pivot("use",147,symbol="usePass")
        self.pivot("onUseTick",158,symbol="double 5.0d")
        self.pivot("onUseTick",161,symbol="isEntityLookingAt")
        self.pivot("onUseTick",168,symbol="SIGHTLESS")
        self.pivot("onUseTick",171,symbol="ACCompat.enchantLevel")
        self.pivot("onUseTick",174,op="ifeq",operand="203")
        self.pivot("onUseTick",188,symbol="totemOfPossessionPlayers")
        self.pivot("onUseTick",204,symbol="stopUsingItem")
        self.assertIn("==0",self.card)
        self.assertIn("nível positivo",self.card)
    def test_gaze_is_distance_dependent_and_los_not_five_block_range(self):
        self.pivot("isEntityLookingAt",4,symbol="distanceTo")
        self.pivot("isEntityLookingAt",8,symbol="double 0.1d")
        self.pivot("isEntityLookingAt",12,op="dadd")
        self.pivot("isEntityLookingAt",13,op="dmul")
        self.pivot("isEntityLookingAt",17,symbol="getViewVector")
        self.pivot("isEntityLookingAt",20,symbol="normalize")
        self.pivot("isEntityLookingAt",94,symbol="Vec3.dot")
        self.pivot("isEntityLookingAt",105,op="ddiv")
        self.pivot("isEntityLookingAt",106,op="dsub")
        self.pivot("isEntityLookingAt",108,op="ifle",operand="123")
        self.pivot("isEntityLookingAt",113,symbol="hasLineOfSight")
        self.assertIn("não é um alcance máximo de cinco blocos",self.card)
    def test_glow_positive_mob_gate_and_forced_false_release(self):
        self.pivot("onUseTick",376,symbol="getNavigation")
        self.pivot("onUseTick",404,symbol="PathNavigation.moveTo")
        self.pivot("onUseTick",409,symbol="SIGHTLESS")
        self.pivot("onUseTick",412,symbol="ACCompat.enchantLevel")
        self.pivot("onUseTick",415,op="ifle",operand="424")
        self.pivot("onUseTick",420,op="iconst_1")
        self.pivot("onUseTick",421,symbol="setGlowingTag")
        self.pivot("releaseUsing",10,op="ifnull",operand="19")
        self.pivot("releaseUsing",15,op="iconst_0")
        self.pivot("releaseUsing",16,symbol="setGlowingTag")
        self.assertIn("Não há captura/restauração",self.card)
    def test_client_wear_release_shrink_and_bound_data_are_separate(self):
        for off,op in ((232,"iconst_2"),(233,"irem"),(234,"ifne"),
                       (241,"ifeq"),(262,"ifne"),(270,"iconst_1"),(271,"iadd")):
            self.pivot("onUseTick",off,op=op)
        self.pivot("onUseTick",238,symbol="isClientSide")
        self.pivot("onUseTick",259,symbol="isCreative")
        self.pivot("onUseTick",272,symbol="setDamageValue")
        self.pivot("releaseUsing",20,symbol="isClientSide")
        self.pivot("releaseUsing",38,symbol="sendMSGToServer")
        self.pivot("releaseUsing",42,symbol="getDamageValue")
        self.pivot("releaseUsing",46,symbol="getMaxDamage")
        self.pivot("releaseUsing",54,symbol="shrink")
        self.pivot("getControlledEntity",1,symbol="isClientSide")
        self.pivot("getControlledEntity",15,symbol="ControllingEntityID")
        self.pivot("getControlledEntity",68,symbol="getBoundEntityUUID")
        self.pivot("getControlledEntity",85,symbol="ServerLevel.getEntity")
        for off,key in ((6,"BoundEntityTag"),(13,"BoundEntityUUID"),(20,"ControllingEntityID")):
            self.pivot("resetBound",off,symbol=key)
        self.assertIn("não comprova débito de durabilidade autoritativo no servidor",self.card)
    def test_certificate_ledger_and_alphabetical_crosswalk(self):
        l=json.loads(CERT.read_text(encoding="utf8"))
        c=l["objects"][ENTRY]
        self.assertEqual(c["status"],"COMPLETE_PERK_READY")
        self.assertEqual(c["claim_scope"],"STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(c["evidence_grade"],"SHA_EXACT_BINARY_BEHAVIOR")
        self.assertEqual(c["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(c["physical_qa"],"NOT_TESTED")
        self.assertEqual(set(c["evidence"]),{"identity","behavior","parameters","targeting",
                                            "costs","integration","validation"})
        self.assertTrue(all(row["path"].endswith("enchantments/sightless.md") for row in c["evidence"].values()))
        self.assertIn("| ✅ | `alexscaves:sightless`",
                      (PROVIDER/"ENCHANTMENT-PERK-CROSSWALK-1.0.10.md").read_text(encoding="utf8"))
        self.assertIn("NO_MUTATION",self.card)
if __name__=="__main__": unittest.main()
