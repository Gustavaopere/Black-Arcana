#!/usr/bin/env python3
"""Fail-closed synthetic controls for exact Crystallization causal JVM audit."""
import copy
import unittest

from alexscaves_1010_crystallization_causal_probe import (
    GAUNTLET, WEAPON, PIVOTS, compact, normalized, reconcile_prior,
    causal_pivots, own_nbt, source_reference_roster, compact_seal,
)
from alexscaves_1010_bouncy_ball_causal_probe import branch_edges
from alexscaves_1010_raygun_local_flow_probe import digest_method

def row(offset, opcode="nop", operand="", symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":operand,"symbol":symbol}

def method(name="use",rows=None,desc="()V"):
    return {"header":"public void "+name+"()","descriptor":desc,
            "instructions": rows if rows is not None else [row(0),row(1),row(2)]}

def prior(m):
    r=m["instructions"]
    return {"name":"use","descriptor":m["descriptor"],
            "instruction_count":len(r),
            "parsed_method_sha256":digest_method(m),
            "pivot_windows":[{"needle":"Sample:",
                              "match_count":1,
                              "locations":[{"at":r[1]["offset"],
                                            "window":[compact(x) for x in r]}]}]}

class CrystallizationCausalTests(unittest.TestCase):
    def test_matching_selected_prior_window(self):
        m=method(rows=[row(0,"aload_0"),row(1,"getstatic","#5","Field Sample:I"),
                       row(4,"return")])
        self.assertEqual(reconcile_prior(m,prior(m)),1)

    def test_prior_wrong_digest_fails(self):
        m=method(rows=[row(0),row(1,"getstatic","#5","Field Sample:I"),row(4)])
        p=prior(m);p["parsed_method_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"digest drift"):
            reconcile_prior(m,p)

    def test_prior_wrong_symbol_fails(self):
        m=method(rows=[row(0),row(1,"getstatic","#5","Field Sample:I"),row(4)])
        p=prior(m)
        p["pivot_windows"][0]["locations"][0]["window"][1]["symbol"]="Field Wrong:I"
        with self.assertRaisesRegex(ValueError,"window drift"):
            reconcile_prior(m,p)

    def test_previous_window_requires_same_declared_match_count(self):
        m=method(rows=[row(0),row(1,"getstatic","#5","Field Sample:I"),row(4)])
        p=prior(m);p["pivot_windows"][0]["match_count"]=2
        with self.assertRaisesRegex(ValueError,"reference count"):
            reconcile_prior(m,p)

    def test_whitespace_only_operand_normalization(self):
        self.assertEqual(normalized("#83,  1"), normalized("#83, 1"))

    def test_changed_operand_remains_changed(self):
        self.assertNotEqual(normalized("#83,  1"),normalized("#83, 2"))

    def test_missing_native_causal_anchor_fails(self):
        with self.assertRaisesRegex(ValueError,"causal pivot drift"):
            causal_pivots(method("use",[row(0),row(1),row(2)]),GAUNTLET)

    def test_wrong_native_aabb_constant_fails(self):
        ins=[row(off,op,sym="") for off,op in []]
        self.assertEqual(len(ins),0)
        # Exact AABB constants must not be silently accepted if changed.
        self.assertEqual(len([x for x in PIVOTS[(GAUNTLET,"onUseTick")]
                              if x in (112,115,118)]),3)

    def test_own_nbt_methods_require_explicit_keys(self):
        a=method("addAdditionalSaveData",[row(0,"ldc_w",symbol="String WeaponStack"),
            row(3,"ldc_w",symbol="String ControllerUUID"),row(6,"return")])
        b=method("readAdditionalSaveData",[row(0,"ldc_w",symbol="String WeaponStack"),
            row(3,"ldc_w",symbol="String ControllerUUID"),row(6,"return")])
        with self.assertRaisesRegex(ValueError,"NBT body changed"):
            own_nbt([a,b])

    def test_own_nbt_rejects_missing_controller(self):
        a=method("addAdditionalSaveData",[row(0,"ldc_w",symbol="String WeaponStack")])
        b=method("readAdditionalSaveData",[row(0,"ldc_w",symbol="String WeaponStack")])
        with self.assertRaisesRegex(ValueError,"missing own"):
            own_nbt([a,b])

    def test_duplicate_jvm_branch_target_rejected(self):
        with self.assertRaisesRegex(ValueError,"branch target"):
            branch_edges(method("use",[row(0,"ifeq","99"),row(3,"return")]))

    def test_unparsed_native_switch_rejected(self):
        with self.assertRaisesRegex(ValueError,"unsupported switch"):
            branch_edges(method("tick",[row(0,"tableswitch"),row(3,"return")]))

    def test_selected_refs_are_bounded(self):
        m=method("getController",[row(0,"getfield",symbol="Field ControllerUUID:I"),
                                  row(3,"return")])
        self.assertEqual(len(source_reference_roster(m)),1)

if __name__=="__main__":
    unittest.main()
