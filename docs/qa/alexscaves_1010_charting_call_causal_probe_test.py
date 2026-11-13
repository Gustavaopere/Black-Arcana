#!/usr/bin/env python3
"""Synthetic fail-closed controls for Charting Call exact native causal audit."""
import unittest
from alexscaves_1010_charting_call_causal_probe import (
    unique_pairs,method_roster,exact_pivots,rng_bounds,
    bounded_nbt,additional,strict_method,require,
)
from alexscaves_1010_bouncy_ball_causal_probe import branch_edges

def op(offset,opcode="nop",operand="",symbol=""):
    return {"offset":offset,"opcode":opcode,
            "operand":operand,"symbol":symbol}

def meth(name,rows,desc="()V"):
    return {"header":"public void "+name+"()",
            "descriptor":desc,"instructions":rows}

class ChartingCallCausalTests(unittest.TestCase):
    def test_duplicate_manifest_key_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate JSON"):
            unique_pairs([("artifact",1),("artifact",2)])

    def test_duplicate_class_method_rejected(self):
        rows=[op(0),op(1),op(2)]
        with self.assertRaisesRegex(ValueError,"duplicate method descriptor"):
            method_roster([meth("tick",rows),meth("tick",rows)])

    def test_abstract_zero_code_counted_not_executed(self):
        method={"header":"public abstract void getDeepOneAnimation()",
                "descriptor":"()V","instructions":[]}
        roster=method_roster([method,meth("tick",[op(0),op(1),op(2)])])
        self.assertEqual(roster[0]["instruction_count"],0)
        self.assertTrue(roster[0]["declaration_only"])

    def test_nonabstract_zero_code_rejected(self):
        with self.assertRaisesRegex(ValueError,"not abstract/native"):
            method_roster([meth("use",[])])

    def test_bad_method_offset_rejected(self):
        with self.assertRaisesRegex(ValueError,"unsorted, duplicate"):
            strict_method(meth("tick",[op(0),op(0),op(2)]))

    def test_release_missing_native_pivot_rejected(self):
        with self.assertRaisesRegex(ValueError,"causal pivot drift"):
            exact_pivots(meth("releaseUsing",[op(0),op(1),op(2)]),
                         "releaseUsing")

    def test_rng_zero_guard_cannot_be_silently_changed(self):
        with self.assertRaisesRegex(ValueError,"bounded RNG opcode drift"):
            rng_bounds(meth("releaseUsing",[op(0),op(1),op(2)]))

    def test_nbt_partial_keys_rejected(self):
        a=meth("addAdditionalSaveData",
               [op(0,"ldc_w",symbol="String ConchSummoned"),
                op(3,"ldc_w",symbol="String ConchUUID")])
        b=meth("readAdditionalSaveData",
               [op(0,"ldc_w",symbol="String ConchSummoned"),
                op(3,"ldc_w",symbol="String ConchUUID")])
        with self.assertRaisesRegex(ValueError,"save/load key"):
            bounded_nbt([a,b])

    def test_related_native_method_must_be_unique(self):
        with self.assertRaisesRegex(ValueError,"missing/ambiguous"):
            additional([],("copyTarget",))

    def test_branch_destination_must_be_local(self):
        rows=[op(0,"ifeq","42"),op(3,"return")]
        with self.assertRaisesRegex(ValueError,"branch target"):
            branch_edges(meth("releaseUsing",rows))

    def test_no_unsupported_jump_in_branch_census(self):
        rows=[op(0,"jsr","3"),op(3,"return")]
        with self.assertRaisesRegex(ValueError,"unsupported"):
            branch_edges(meth("releaseUsing",rows))

    def test_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"synthetic"):
            require(False,"synthetic")

if __name__=="__main__":
    unittest.main()
