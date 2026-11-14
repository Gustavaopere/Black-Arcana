#!/usr/bin/env python3
"""Fail-closed and arithmetic tests for the individual Dazing Sweep JVM audit."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from alexscaves_1010_dazing_sweep_causal_probe import (
    BASE, CLUB, STUN, VISUAL, RES, TAG, RES_SHA, TAG_SHA,
    PIVOTS, METHODS, check_config, check_direct_cfg, check_pivots,
    match_previous, normalized_operand, unique_pairs,
)

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"


class DazingSweepNativeTests(unittest.TestCase):
    def test_native_consumer_scope_and_non_spell_identity(self):
        self.assertEqual(METHODS[CLUB], ("acHurtEnemy", "hurtEnemy"))
        self.assertEqual(METHODS[STUN], ("shouldTick", "tick"))
        self.assertEqual(METHODS[VISUAL], ("handle",))
        self.assertIn(136, PIVOTS[(CLUB, "acHurtEnemy")])
        self.assertEqual(PIVOTS[(CLUB, "acHurtEnemy")][322], ("pop", ""))
        self.assertEqual(PIVOTS[(CLUB, "acHurtEnemy")][327],
                         ("invokevirtual", "LivingEntity.addEffect"))

    def test_aabb_side_is_not_radius(self):
        for level, side, half in ((1, 2.2, 1.1), (2, 3.2, 1.6)):
            self.assertAlmostEqual(level + 1.2, side)
            self.assertAlmostEqual(side / 2, half)
            self.assertLess(half, side)
        self.assertEqual([150+i for i in (0,149)], [150,299])
        self.assertEqual([80+i for i in (0,79)], [80,159])

    def test_direct_cfg_rejects_nonexistent_destination(self):
        method = {"header":"test()", "instructions":[
            {"offset":0,"opcode":"ifeq","operand":"5","symbol":""},
            {"offset":3,"opcode":"return","operand":"","symbol":""},
        ]}
        with self.assertRaisesRegex(ValueError, "invalid JVM branch target"):
            check_direct_cfg(method)

    def test_native_pivot_drift_rejected(self):
        method = {"header":"test()", "instructions":[
            {"offset":136,"opcode":"getstatic","operand":"#123",
             "symbol":"Field ACEnchantmentRegistry.DAZING_SWEEP"},
        ]}
        check_pivots(method,{136:("getstatic","DAZING_SWEEP")})
        bad = copy.deepcopy(method)
        bad["instructions"][0]["symbol"] = "Field ACEnchantmentRegistry.OTHER"
        with self.assertRaisesRegex(ValueError, "pivot drift"):
            check_pivots(bad,{136:("getstatic","DAZING_SWEEP")})

    def test_previous_full_method_requirements(self):
        method = {"header":"test()", "instructions":[
            {"offset":0,"opcode":"getstatic","operand":"#110,  1","symbol":"A"},
            {"offset":4,"opcode":"return","operand":"","symbol":""},
        ]}
        old = [{"offset":0,"opcode":"getstatic","operand":"#110, 1","symbol":"A"},
               {"offset":4,"opcode":"return","operand":"","symbol":""}]
        self.assertEqual(match_previous(method,old),2)
        with self.assertRaisesRegex(ValueError, "not full-method"):
            match_previous(method, old[:1])
        old[0]["symbol"] = "OTHER"
        with self.assertRaisesRegex(ValueError, "window drift"):
            match_previous(method,old)
        self.assertEqual(normalized_operand("#110,  1"),
                         normalized_operand("#110, 1"))

    def test_json_duplicates_and_metadata_gates(self):
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            json.loads('{"max_level":2,"max_level":500}',
                       object_pairs_hook=unique_pairs)
        obj = {"description":{"translate":"enchantment.alexscaves.dazing_sweep"},
               "supported_items":"#alexscaves:enchantable/primitive_club",
               "weight":2,"max_level":2,"anvil_cost":4,
               "slots":["mainhand"],
               "min_cost":{"base":1,"per_level_above_first":10},
               "max_cost":{"base":41,"per_level_above_first":10}}
        check_config(obj)
        x = copy.deepcopy(obj); x["max_level"] = 100
        with self.assertRaisesRegex(ValueError, "metadata drift"):
            check_config(x)

    def test_existing_source_is_partial_until_certification(self):
        card = (P / "enchantments/dazing-sweep.md").read_text(encoding="utf8")
        for token in ("PrimitiveClubItem", "AABB.ofSize", "1.2F",
                      "80–159", "150–299", "NO_MUTATION",
                      RES_SHA, TAG_SHA, "NOT_TESTED"):
            self.assertIn(token, card)
        self.assertIn("Não é um cast adicional", card)  # native club proc, no new cast

if __name__ == "__main__":
    unittest.main()
