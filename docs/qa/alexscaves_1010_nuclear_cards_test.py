#!/usr/bin/env python3
"""Bounded nuclear contract coverage; static evidence never grants runtime use."""
import json
import unittest
from pathlib import Path
from alexscaves_1010_damage_card_test import assert_sealed_damage_contract
from alexscaves_1010_nuclear_ticket_promotion_gate_test import gate

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued"
PREFIX="com/github/alexmodguy/alexscaves/"

class NuclearContractCards(unittest.TestCase):
    def anchors(self, doc, owner, name, descriptor=None):
        rows=[m for m in doc["classes"][PREFIX+owner+".class"]["methods"]
              if m["name"]==name and (descriptor is None or m["descriptor"]==descriptor)]
        self.assertEqual(len(rows),1,(owner,name,descriptor))
        return {a["offset"]:a for a in rows[0]["anchors"]}

    def test_all_twenty_own_members_and_single_damage_bifurcation(self):
        d=assert_sealed_damage_contract(self,"nuke")
        assert_sealed_damage_contract(self,"intentional_game_design")
        owner="server/entity/item/NuclearExplosionEntity"
        expected={"<init>","<clinit>","getAddEntityPacket","tick","remove","getChunksAffected",
                  "loadChunksAround","calculateDamage","removeChunk","isDestroyable","defineSynchedData",
                  "getSize","setSize","isNoGriefing","setNoGriefing","isIntentionalGameDesign",
                  "setIntentionalGameDesign","readAdditionalSaveData","addAdditionalSaveData","lambda$tick$0"}
        methods=d["classes"][PREFIX+owner+".class"]["methods"]
        self.assertEqual(len(methods),20)
        self.assertEqual({m["name"] for m in methods},expected)
        tick=self.anchors(d,owner,"tick","()V")
        for offset, symbol in ((592,"isIntentionalGameDesign"),(605,"causeIntentionalGameDesign"),
                               (618,"causeNukeDamage"),(623,"LivingEntity.hurt"),
                               (643,"setDeltaMovement"),(647,"isIntentionalGameDesign")):
            self.assertIn(symbol,tick[offset]["symbol"])
        self.assertEqual((tick[595]["opcode"],tick[595]["operand"]),("ifeq","611"))
        self.assertEqual((tick[608]["opcode"],tick[608]["operand"]),("goto","621"))
        self.assertEqual(tick[626]["opcode"],"pop")
        helper=self.anchors(d,owner,"calculateDamage","(FF)F")
        self.assertEqual((helper[2]["opcode"],helper[4]["opcode"],helper[44]["opcode"]),
                         ("fsub","fdiv","fmul"))

    def test_four_emitters_and_asymmetric_ticket_calls_are_sealed(self):
        d=assert_sealed_damage_contract(self,"nuke")
        for owner, name in (("server/item/SackOfSatingItem","acInventoryTick"),
                            ("server/entity/item/NuclearBombEntity","explode"),
                            ("server/entity/living/NucleeperEntity","explode"),
                            ("server/block/blockentity/NuclearFurnaceBlockEntity","destroyWhileCritical")):
            rows=self.anchors(d,owner,name)
            self.assertTrue(any("NUCLEAR_EXPLOSION" in a["symbol"] for a in rows.values()),owner)
            self.assertTrue(any("addFreshEntity" in a["symbol"] for a in rows.values()),owner)
        owner="server/entity/item/NuclearExplosionEntity"
        tick=self.anchors(d,owner,"tick")
        remove=self.anchors(d,owner,"remove")
        load=self.anchors(d,owner,"loadChunksAround")
        self.assertEqual(tick[210]["opcode"],"iconst_1")
        self.assertIn("loadChunksAround",tick[211]["symbol"])
        self.assertEqual(remove[23]["opcode"],"iconst_0")
        self.assertIn("loadChunksAround",remove[24]["symbol"])
        self.assertEqual((load[86]["opcode"],load[87]["opcode"]),("iload_1","iload_1"))
        self.assertIn("ACPlatform.forceChunk",load[88]["symbol"])
        platform=self.anchors(d,"server/misc/ACPlatform","forceChunk",
                             "(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/Entity;IIZZ)V")
        self.assertIn("TicketController.forceChunk",platform[20]["symbol"])
        self.assertEqual(platform[23]["opcode"],"pop")

    def test_sealed_pair_preserves_independent_physical_gate(self):
        d=assert_sealed_damage_contract(self,"nuke")
        old=json.loads((P/"EXACT-NEOFORGE-TICKETS-21.1.248.json").read_text())
        ledger=json.loads((ROOT/"wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json").read_text())
        cards={name:(P/"damage-types"/(name+".md")).read_text()
               for name in ("intentional-game-design","nuke")}
        gate(old,ledger,cards,(P/"INDEX.md").read_text(),(P/"damage-types/INDEX.md").read_text(),d)
        self.assertEqual(old["actual_persistent_ticket_leak"],"NOT_OBSERVED")
        self.assertEqual(old["limits"]["physical_qa"],"NOT_TESTED")

if __name__=="__main__":
    unittest.main()
