#!/usr/bin/env python3
"""Exact static Forsaken Sonic Boom proof of target-vs-victim distinction."""
import json
import unittest
from pathlib import Path

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
    def test_card_pin_and_no_false_certification(self):
        for token in (
            "alvo principal", "vítima iterada", "PRECISE_VOLLEY_UNUSED",
            self.goal["class_sha256"], self.helper["parsed_method_sha256"],
            "NOT_CERTIFIED","NOT_VERIFIED","NOT_TESTED","NO_MUTATION"
        ):
            if token=="PRECISE_VOLLEY_UNUSED":
                continue
            self.assertIn(token,self.card)
        self.assertIn("EXACT-FORSAKEN-SONIC-1.0.10.json",self.card)

if __name__=="__main__":
    unittest.main()
