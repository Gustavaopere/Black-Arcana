#!/usr/bin/env python3
"""Exact static Forsaken Sonic Boom proof of target-vs-victim distinction."""
import json
import unittest
from pathlib import Path
from alexscaves_1010_damage_card_test import assert_sealed_damage_contract

ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/"wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
MAN=DIR/"EXACT-FORSAKEN-SONIC-1.0.10.json"
CARD=DIR/"forsaken-sonic-boom.md"

class ForsakenSonicCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(MAN.read_text(encoding="utf8"))
        cls.goal=cls.d["classes"][0]
        cls.entity=cls.d["classes"][1]
        cls.goal_methods={m["name"]:m for m in cls.goal["selected_methods"]}
        cls.tick=cls.goal_methods["tick"]
        cls.helper=next(m for m in cls.entity["selected_methods"]
                        if m["name"]=="getSonicDamageAgainst")
        cls.card=CARD.read_text(encoding="utf8")
    def seq(self,at):
        match=[w for w in self.tick["selected_windows"] if w["at"]==at]
        self.assertEqual(len(match),1)
        return {i["offset"]:i for i in match[0]["instruction_window"]}
    def test_jvm_and_fail_closed(self):
        self.assertEqual(self.d["scope"],"EXACT_1010_FORSAKEN_SONIC_SELECTED_CALL_AND_CONTROL_ANCHORS_ONLY")
        self.assertEqual(self.tick["instruction_count"],826)
        self.assertEqual(self.goal_methods["canUse"]["descriptor"],"()Z")
        self.assertFalse(self.d["bounds"]["complete_perk_ready"])
        self.assertEqual(self.d["bounds"]["mutating_hook"],"NOT_VERIFIED")
        self.assertEqual(self.d["bounds"]["physical_qa"],"NOT_TESTED")
    def test_initial_goal_target_in_local_one(self):
        ins=self.seq(0)
        self.assertIn("getTarget:",ins[4]["symbol"])
        self.assertEqual(ins[7]["opcode"],"astore_1")
    def test_area_victim_and_primary_target_not_conflated(self):
        self.assertEqual(self.seq(557)[560]["opcode"],"aload")
        self.assertEqual(self.seq(557)[560]["operand"],"9")
        self.assertEqual(self.seq(584)[583]["opcode"],"aload_1")
        self.assertIn("getSonicDamageAgainst:",self.seq(584)[584]["symbol"])
    def test_canonical_two_sonic_factories_and_hurts(self):
        self.assertEqual([x["offset"] for x in self.tick["sealed_hurt_factory_sites"]],
                         [108,119,576,596])
        self.assertEqual(self.seq(587)[587]["symbol"],"float 0.65f")
        self.assertEqual(self.seq(590)[590]["opcode"],"fmul")
        self.assertIn("Math.ceil",self.seq(592)[592]["symbol"])
    def test_allies_radius_and_ignore_tag(self):
        syms={x["offset"]:x["symbol"] for x in self.tick["symbolic_method_and_field_anchors"]}
        for off,part in ((510,"isAlliedTo"),(522,"isAlliedTo"),
                         (534,"distanceTo"),(551,"FORSAKEN_IGNORES"),
                         (459,"getEntitiesOfClass"),(456,"AABB.inflate")):
            self.assertIn(part,syms[off])
        constants={x["offset"]:x["symbol"] for x in self.tick["numeric_constant_anchors"]}
        self.assertEqual(constants[537],"float 14.0f")
        self.assertEqual(constants[447],"double 16.0d")
        self.assertEqual(constants[450],"double 8.0d")
        self.assertEqual(constants[453],"double 16.0d")
    def test_sonic_tag_and_helper_values(self):
        syms=" ".join(x["symbol"] for x in self.helper["symbolic_method_and_field_anchors"])
        self.assertIn("WEAK_TO_FORSAKEN_SONIC_ATTACK",syms)
        vals={x["symbol"] for x in self.helper["numeric_constant_anchors"]}
        self.assertIn("float 45.0f",vals)
        self.assertIn("float 4.0f",vals)
    def final_anchors(self, manifest, owner, name, descriptor):
        path = "com/github/alexmodguy/alexscaves/" + owner + ".class"
        self.assertIn(path, manifest["classes"])
        methods = [m for m in manifest["classes"][path]["methods"]
                   if (m["name"], m["descriptor"]) == (name, descriptor)]
        self.assertEqual(len(methods), 1, (path, name, descriptor))
        return {a["offset"]: a for a in methods[0]["anchors"]}

    def test_completed_contract_covers_entire_own_goal_and_two_damage_paths(self):
        final = assert_sealed_damage_contract(self, "forsaken_sonic_boom")
        owner = "server/entity/ai/ForsakenAttackGoal"
        expected = {
            ("<init>", "(Lcom/github/alexmodguy/alexscaves/server/entity/living/ForsakenEntity;)V"),
            ("canUse", "()Z"), ("start", "()V"), ("stop", "()V"), ("tick", "()V"),
            ("canReach", "(Lnet/minecraft/world/entity/LivingEntity;)Z"),
            ("isMovementFrozen", "()Z"), ("startCleanJump", "()V"),
            ("checkAndDealDamage", "(Lnet/minecraft/world/entity/LivingEntity;DF)Z"),
            ("knockBackAngle", "(Lnet/minecraft/world/entity/LivingEntity;DF)V"),
            ("tryAnimation", "(Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;)Z"),
            ("findJumpTarget", "(Lnet/minecraft/world/entity/LivingEntity;Z)Lnet/minecraft/core/BlockPos;"),
        }
        methods = final["classes"]["com/github/alexmodguy/alexscaves/" + owner + ".class"]["methods"]
        self.assertEqual({(m["name"], m["descriptor"]) for m in methods}, expected)
        constructor = self.final_anchors(final, owner, "<init>",
                                        "(Lcom/github/alexmodguy/alexscaves/server/entity/living/ForsakenEntity;)V")
        self.assertIn("Goal$Flag.MOVE", constructor[35]["symbol"])
        self.assertIn("Goal$Flag.LOOK", constructor[38]["symbol"])
        self.assertIn("setFlags:", constructor[44]["symbol"])
        tick = self.final_anchors(final, owner, "tick", "()V")
        self.assertEqual(tick[7]["opcode"], "astore_1")
        self.assertEqual((tick[560]["opcode"], tick[560]["operand"]), ("aload", "9"))
        self.assertEqual(tick[583]["opcode"], "aload_1")
        for offset, symbol in ((108, "causeForsakenSonicBoomDamage"), (119, "LivingEntity.hurt:"),
                               (576, "causeForsakenSonicBoomDamage"), (584, "getSonicDamageAgainst:"),
                               (596, "LivingEntity.hurt:"), (1097, "hasSonicCharge:"),
                               (1112, "sonicEnqueued"), (1120, "setSonicCharge:")):
            self.assertIn(symbol, tick[offset]["symbol"])

    def test_completed_contract_keeps_charge_animation_and_target_support(self):
        final = assert_sealed_damage_contract(self, "forsaken_sonic_boom")
        entity = "server/entity/living/ForsakenEntity"
        charge = self.final_anchors(final, entity, "hurt",
                                    "(Lnet/minecraft/world/damagesource/DamageSource;F)Z")
        self.assertIn("DamageTypes.SONIC_BOOM:", charge[1]["symbol"])
        self.assertIn("DamageSource.is:", charge[4]["symbol"])
        self.assertEqual((charge[7]["opcode"], charge[7]["operand"]), ("ifeq", "17"))
        self.assertEqual(charge[11]["opcode"], "iconst_1")
        self.assertIn("setSonicCharge:", charge[12]["symbol"])
        self.assertEqual(charge[15]["opcode"], "iconst_0")
        self.assertEqual(charge[16]["opcode"], "ireturn")
        init = self.final_anchors(final, entity, "<clinit>", "()V")
        for value, call, field, duration, name in ((114,116,119,"35","ANIMATION_SONIC_ATTACK"),
                                                  (122,124,127,"45","ANIMATION_SONIC_BLAST")):
            self.assertEqual((init[value]["opcode"], init[value]["operand"]), ("bipush", duration))
            self.assertIn("Animation.create:", init[call]["symbol"])
            self.assertIn(name, init[field]["symbol"])
        self.assertEqual(init[146]["opcode"], "invokedynamic")
        self.assertIn("TARGETING:", init[151]["symbol"])
        registry = self.final_anchors(final, "server/entity/ACEntityRegistry", "<clinit>", "()V")
        self.assertIn("String forsaken", registry[1030]["symbol"])
        self.assertEqual(registry[1033]["opcode"], "invokedynamic")
        self.assertIn("DeferredRegister.register:", registry[1038]["symbol"])
        self.assertIn("FORSAKEN:", registry[1041]["symbol"])
        tags = self.final_anchors(final, "server/misc/ACTagRegistry", "<clinit>", "()V")
        self.assertIn("String weak_to_forsaken_sonic_attack", tags[725]["symbol"])
        self.assertIn("WEAK_TO_FORSAKEN_SONIC_ATTACK:", tags[731]["symbol"])
        self.assertIn("String forsaken_ignores", tags[734]["symbol"])
        self.assertIn("FORSAKEN_IGNORES:", tags[740]["symbol"])
        for path, digest in {
            "data/alexscaves/tags/entity_type/forsaken_ignores.json":
                "f68ad72f5ae970bf57b53a78f234257d4949e92a772e7669efa5dc2e0ce428b7",
            "data/alexscaves/tags/entity_type/weak_to_forsaken_sonic_attack.json":
                "603c74730688b3a8fbe59e6452f0f161a7c373d5556c33d3a1713a7be5eb1023",
        }.items():
            self.assertEqual(final["resources"][path], digest)
            self.assertIn(path, final["contract_evidence"]["damage-types/forsaken-sonic-boom.md"]["resources"])
        handler = self.final_anchors(final, "citadel/animation/AnimationHandler", "updateAnimations",
                                     "(Lnet/minecraft/world/entity/Entity;)V")
        # Event callbacks may change state: both comparisons need their own fresh reads.
        for offset, symbol in ((73,"AnimationEvent$Start.post:"), (92,"getAnimationTick:"),
                               (101,"getAnimation:"), (106,"Animation.getDuration:"),
                               (158,"AnimationEvent$Tick.post:"), (165,"getAnimationTick:"),
                               (174,"getAnimation:"), (179,"Animation.getDuration:"),
                               (190,"setAnimationTick:"), (199,"NO_ANIMATION:"), (202,"setAnimation:")):
            self.assertIn(symbol, handler[offset]["symbol"])
        for offset, opcode, target in ((76,"ifne","88"), (109,"if_icmpge","161"),
                                       (182,"if_icmpne","207")):
            self.assertEqual((handler[offset]["opcode"], handler[offset]["operand"]), (opcode, target))

    def test_card_pin_and_static_only_certification(self):
        assert_sealed_damage_contract(self, "forsaken_sonic_boom")
        for token in (
            "alvo principal", "vítima iterada", "PRECISE_VOLLEY_UNUSED",
            self.goal["class_sha256"], self.helper["parsed_method_sha256"],
            "STATIC_TECHNICAL_CATALOG_ONLY","NOT_VERIFIED","NOT_TESTED","NO_MUTATION"
        ):
            if token=="PRECISE_VOLLEY_UNUSED":
                continue
            self.assertIn(token,self.card)
        self.assertIn("EXACT-FORSAKEN-SONIC-1.0.10.json",self.card)

if __name__=="__main__":
    unittest.main()
