#!/usr/bin/env python3
"""Fail-closed synthetic and arithmetic Double Stab 1.0.10 tests."""
import copy
import json
import unittest
from alexscaves_1010_double_stab_causal_probe import (
    ITEM, ENTITY, COMPAT, DAMAGE, REG, RES, TAG, OTHER,
    CLASS_SHAS, RESOURCE_SHAS, METHODS, PIVOTS,
    check_config, check_pivots, compare_anchors,
    check_causal_counters, unique_pairs, select,
)
from alexscaves_1010_bouncy_ball_causal_probe import branch_edges


class DoubleStabProbeTests(unittest.TestCase):
    def test_scope_is_native_melee_proc_and_downstream_owners(self):
        self.assertEqual(set(METHODS),{ITEM,ENTITY,COMPAT,DAMAGE})
        self.assertEqual(len(METHODS[ITEM]),2)
        self.assertIn("tick",METHODS[ENTITY])
        self.assertIn("enchantLevel",METHODS[COMPAT])
        self.assertEqual(PIVOTS[(ITEM,"acSpawnDaggers")][112],("goto","12"))
        self.assertEqual(PIVOTS[(ITEM,"acSpawnDaggers")][108],("pop",""))
        self.assertIn("Registry", REG)

    def test_quantity_concept_is_attempts_and_unbounded_noncanonical_levels(self):
        self.assertEqual([1+level for level in (0,1)], [1,2])
        self.assertEqual([1+level for level in (2,3)], [3,4])
        self.assertEqual([20+v for v in (0,9)],[20,29])
        self.assertEqual([40+v for v in (0,9)],[40,49])
        self.assertEqual([2+2*L for L in (0,1,2,3)],[2,4,6,8])

    def test_native_json_and_asymmetric_exclusion(self):
        base={"description":{"translate":"enchantment.alexscaves.double_stab"},
              "supported_items":"#alexscaves:enchantable/desolate_dagger",
              "weight":2,"max_level":1,"anvil_cost":4,"slots":["mainhand"],
              "min_cost":{"base":1,"per_level_above_first":12},
              "max_cost":{"base":41,"per_level_above_first":10}}
        tag={"values":["alexscaves:desolate_dagger"]}
        adjacent={"exclusive_set":["alexscaves:double_stab"]}
        check_config(base,tag,adjacent)
        bad=copy.deepcopy(base);bad["max_level"]=2
        with self.assertRaisesRegex(ValueError,"metadata drift"):
            check_config(bad,tag,adjacent)
        bad=copy.deepcopy(adjacent);bad["exclusive_set"]="alexscaves:double_stab"
        with self.assertRaisesRegex(ValueError,"asymmetric exclusion"):
            check_config(base,tag,bad)
        with self.assertRaisesRegex(ValueError,"duplicate JSON key"):
            json.loads('{"max_level":1,"max_level":2}',object_pairs_hook=unique_pairs)

    def test_native_pivot_rejects_drift(self):
        method={"header":"acSpawnDaggers()", "instructions":[
            {"offset":16,"opcode":"getstatic","operand":"#63",
             "symbol":"Field ACEnchantmentRegistry.DOUBLE_STAB"}]}
        check_pivots(method,{16:("getstatic","DOUBLE_STAB")})
        bad=copy.deepcopy(method);bad["instructions"][0]["symbol"]="Field OTHER"
        with self.assertRaisesRegex(ValueError,"pivot drift"):
            check_pivots(bad,{16:("getstatic","DOUBLE_STAB")})

    def test_sparse_or_complete_parent_consumer_anchor_check(self):
        method={"header":"acSpawnDaggers()", "instructions":[
            {"offset":0,"opcode":"aload_1","operand":"","symbol":""},
            {"offset":1,"opcode":"return","operand":"","symbol":""}]}
        old=[{"offset":0,"opcode":"aload_1","operand":"","symbol":""}]
        self.assertEqual(compare_anchors(method,old),1)
        with self.assertRaisesRegex(ValueError,"missing/duplicate"):
            compare_anchors(method,old+old)
        with self.assertRaisesRegex(ValueError,"bytecode drift"):
            changed=copy.deepcopy(old);changed[0]["opcode"]="nop"
            compare_anchors(method,changed)

    def test_missing_method_and_invalid_branch_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"missing/ambiguous"):
            select([],"acSpawnDaggers","()V")
        method={"instructions":[
            {"offset":0,"opcode":"ifeq","operand":"12","symbol":""},
            {"offset":3,"opcode":"return","operand":"","symbol":""}]}
        with self.assertRaisesRegex(ValueError,"invalid JVM branch target"):
            branch_edges(method,[])

    def test_new_owner_assignment_or_duplicate_spawn_not_accepted(self):
        def row(offset,symbol,opcode="invokevirtual"):
            return {"offset":offset,"opcode":opcode,"operand":"","symbol":symbol}
        chosen={
            (ITEM,"acSpawnDaggers"):{"instructions":[
                row(1,"Field ACEnchantmentRegistry.IMPENDING_STAB","getstatic"),
                row(16,"Field ACEnchantmentRegistry.DOUBLE_STAB","getstatic"),
                row(105,"Method Level.addFreshEntity:()Z"),
                row(107,"Method DesolateDaggerEntity.setPlayerId:(I)V")]},
            (ITEM,"hurtEnemy"):{"instructions":[
                row(4,"Method SwordItem.hurtEnemy:()Z"),
                row(14,"Method acSpawnDaggers:()V")]},
            (ENTITY,"tick"):{"instructions":[
                row(344,"Method ACCompat.hurt:()Z"),
                row(339,"Method ACDamageTypes.causeDesolateDaggerDamage:()V")]}
        }
        with self.assertRaisesRegex(ValueError,"player ID"):
            check_causal_counters(chosen)

if __name__ == "__main__":
    unittest.main()
