#!/usr/bin/env python3
"""Negative tests: exact-version Detonating Death remains fail-closed."""
from __future__ import annotations

import copy
import json
import unittest

from alexscaves_1010_detonating_death_causal_probe import (
    TOTEM, EXPLOSION, REGISTRY, RES, TAG, CLASS_SHAS,
    RESOURCE_SHAS, METHODS, PIVOTS, compare_sparse_anchors,
    verify_pivots, choose, unique_pairs, verify_config,
)
from alexscaves_1010_bouncy_ball_causal_probe import branch_edges


class DetonatingDeathProbeTests(unittest.TestCase):
    def test_exact_identity_and_consumer_roster(self):
        self.assertEqual(set(CLASS_SHAS), {TOTEM, EXPLOSION})
        self.assertEqual(set(RESOURCE_SHAS), {RES, TAG})
        self.assertIn("onUseTick", METHODS[TOTEM])
        self.assertIn("getControlledEntity", METHODS[TOTEM])
        self.assertEqual(METHODS[EXPLOSION], {"explode": "()V"})
        self.assertEqual(PIVOTS[(TOTEM, "onUseTick")][103][1],
                         "TotemExplosion.finalizeExplosion")
        self.assertIn("ACEnchantmentRegistry", REGISTRY)

    def test_json_duplicate_key_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            json.loads('{"weight":2,"weight":3}', object_pairs_hook=unique_pairs)

    def test_enchantment_resource_non_cast_and_costs(self):
        info = {
            "description": {"translate": "enchantment.alexscaves.detonating_death"},
            "supported_items": "#alexscaves:enchantable/totem_of_possession",
            "weight": 2, "max_level": 1, "anvil_cost": 4, "slots": ["mainhand"],
            "exclusive_set": "alexscaves:astral_transferring",
            "min_cost": {"base": 1, "per_level_above_first": 11},
            "max_cost": {"base": 41, "per_level_above_first": 10}
        }
        verify_config(info)
        bad = copy.deepcopy(info);bad["max_level"] = 2
        with self.assertRaisesRegex(ValueError, "settings drift"):
            verify_config(bad)
        bad = copy.deepcopy(info);bad["min_cost"]["base"] = 0
        with self.assertRaisesRegex(ValueError, "min-cost drift"):
            verify_config(bad)

    def test_sparse_parent_proof_is_not_full_proof(self):
        method = {"header":"public void onUseTick(...)","descriptor":"()V",
                  "instructions":[
            {"offset":0,"opcode":"aload_0","operand":"","symbol":""},
            {"offset":3,"opcode":"return","operand":"","symbol":""}]}
        recorded = [{"offset":0,"opcode":"aload_0","operand":"","symbol":""}]
        self.assertEqual(compare_sparse_anchors(method, recorded),1)
        with self.assertRaisesRegex(ValueError, "missing/repeated"):
            compare_sparse_anchors(method, recorded+recorded)
        with self.assertRaisesRegex(ValueError, "anchor drift"):
            broken = copy.deepcopy(recorded);broken[0]["opcode"]="nop"
            compare_sparse_anchors(method,broken)

    def test_method_pivot_and_target_rejected_on_drift(self):
        method={"header":"public void onUseTick(...)","descriptor":"()V",
                "instructions":[
            {"offset":97,"opcode":"invokevirtual","operand":"#1",
             "symbol":"Method TotemExplosion.explode:()V"}]}
        verify_pivots(method,{97:("invokevirtual","TotemExplosion.explode")})
        bad=copy.deepcopy(method);bad["instructions"][0]["symbol"]="Method Other.explode:()V"
        with self.assertRaisesRegex(ValueError, "pivot drift"):
            verify_pivots(bad,{97:("invokevirtual","TotemExplosion.explode")})
        with self.assertRaisesRegex(ValueError, "missing/ambiguous"):
            choose([], "onUseTick", "()V")

    def test_cfg_rejects_non_existing_branch_destination(self):
        method={"instructions":[
            {"offset":0,"opcode":"ifeq","operand":"20","symbol":""},
            {"offset":3,"opcode":"return","operand":"","symbol":""}]}
        with self.assertRaisesRegex(ValueError, "invalid JVM branch target"):
            branch_edges(method, [])

if __name__ == "__main__":
    unittest.main()
