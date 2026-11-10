#!/usr/bin/env python3
"""Synthetic regression and fail-closed checks for Twilight Perfection census."""
import unittest
from alexscaves_1010_twilight_perfection_probe import (
    require,strict_pairs,selected_method,verify_pivots,PIVOTS,ITEM,ARROW,MSG,RENDER
)

def row(offset,opcode="",operand="",symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":operand,"symbol":symbol}

class Tests(unittest.TestCase):
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            strict_pairs([("max_level",3),("max_level",1)])
    def test_exact_method_ambiguous_fails(self):
        m={"classes":{ITEM:{"methods":[{"name":"releaseUsing"},{"name":"releaseUsing"}]}}}
        with self.assertRaisesRegex(ValueError,"ambiguous"):
            selected_method(m,ITEM,"releaseUsing")
    def test_bytecode_offset_exact(self):
        m={"anchors":[row(14,"getstatic","#208","Field RELENTLESS_DARKNESS"),
                      row(20,"ifgt","899","")]}
        self.assertEqual(verify_pivots(m,{14:"RELENTLESS_DARKNESS",20:"899"}),2)
        with self.assertRaisesRegex(ValueError,"pivot"):
            verify_pivots(m,{20:"898"})
    def test_duplicate_anchor_offset_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate compiled"):
            verify_pivots({"anchors":[row(3),row(3)]},{3:""})
    def test_twilight_all_consumers_covered(self):
        required={(ITEM,"acInventoryTick"),(ITEM,"releaseUsing"),
                  (ITEM,"getPerfectShotTicks"),(ITEM,"setPerfectShotTicks"),
                  (ARROW,"onHitEntity"),(ARROW,"setPerfectShot"),
                  (ARROW,"isPerfectShot"),(MSG,"handle"),(RENDER,"renderByItem")}
        self.assertEqual(set(PIVOTS),required)
        self.assertIn(215,PIVOTS[(ITEM,"acInventoryTick")])
        self.assertIn(439,PIVOTS[(ITEM,"releaseUsing")])
    def test_no_rewriting_on_missing(self):
        with self.assertRaises(ValueError):
            require(False,"safe fail closed")

if __name__=="__main__":
    unittest.main()
