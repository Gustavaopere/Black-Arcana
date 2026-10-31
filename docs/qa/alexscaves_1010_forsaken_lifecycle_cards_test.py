#!/usr/bin/env python3
"""Exact Forsaken AI lifecycle and world-safety card regression."""
import json
import unittest
from pathlib import Path
from alexscaves_1010_damage_card_test import assert_sealed_damage_contract

DIR=Path(__file__).resolve().parents[2]/"wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types"
SOURCE=DIR/"EXACT-FORSAKEN-LIFECYCLE-1.0.10.json"
CARD=DIR/"forsaken-sonic-boom.md"

class LifecycleCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SOURCE.read_text(encoding="utf8"))
        cls.m={m["header"].split("(")[0].split(" ")[-1]:m
               for c in cls.d["classes"] for m in c["selected_methods"]}
        cls.card=CARD.read_text(encoding="utf8")

    def refs(self,name):
        return {w["instruction"]["offset"]:w["instruction"]["symbol"]
                for w in self.m[name]["selected_symbol_windows"]}

    def test_scope_and_fail_closed(self):
        self.assertEqual(self.d["scope"],"EXACT_1010_FORSAKEN_GOAL_REGISTRATION_AND_LIFECYCLE_SYMBOLS_ONLY")
        self.assertEqual(len(self.m),9)
        self.assertEqual(self.d["limits"]["mutating_hook"],"NOT_VERIFIED")
        self.assertFalse(self.d["limits"]["complete_perk_ready"])

    def test_registration_of_goal_and_three_target_rules(self):
        r=self.refs("registerGoals")
        self.assertIn("ForsakenAttackGoal",r[26])
        self.assertIn("HurtByTargetGoal",r[122])
        self.assertIn("NearestAttackableTargetGoal",r[142])
        self.assertIn("TARGETING:",r[164])
        self.assertIn("ACCompat.targetSelector",r[167])
        self.assertIn("NearestAttackableTargetGoal",r[170])
        self.assertIn("GoalSelector.addGoal",r[173])

    def test_sonic_animation_is_not_hit_count(self):
        r=self.refs("tick")
        self.assertIn("ANIMATION_SONIC_ATTACK",r[806])
        self.assertIn("ANIMATION_SONIC_BLAST",r[898])
        self.assertIn("AnimationHandler.updateAnimations",r[1679])
        self.assertIn("FORSAKEN_SONAR",r[843])
        self.assertIn("FORSAKEN_SONAR_LARGE",r[935])

    def test_distinct_world_safety_path(self):
        r=self.refs("customServerAiStep")
        for off,part in ((40,"canEntityGrief"),(153,"canEntityDestroy"),
                         (175,"onEntityDestroyBlock"),(189,"destroyBlock")):
            self.assertIn(part,r[off])
        self.assertIn("WorldEffectPolicy",self.card)

    def test_path_and_state_methods(self):
        self.assertIn("PathNavigation.createPath",self.refs("canReach")[9])
        self.assertIn("Level.isUnobstructed",self.refs("findJumpTarget")[258])
        self.assertIn("jumpEnqueued",self.refs("startCleanJump")[7])
        self.assertIn("SONAR_ID",self.refs("setSonarId")[4])
        self.assertIn("LEAPING",self.refs("setLeaping")[4])
        self.assertIn("animationTick",self.refs("setAnimationTick")[2])

    def test_exact_method_pins_documented_and_only_static_promoted(self):
        assert_sealed_damage_contract(self, "forsaken_sonic_boom")
        for m in self.m.values():
            self.assertIn(m["method_sha256"],self.card)
        for tok in ("STATIC_TECHNICAL_CATALOG_ONLY","NOT_VERIFIED","NOT_TESTED","NO_MUTATION",
                    "EXACT-FORSAKEN-LIFECYCLE-1.0.10.json"):
            self.assertIn(tok,self.card)

if __name__=="__main__":
    unittest.main()
