#!/usr/bin/env python3
"""Negative synthetic controls for native Bouncing Bolt class/CFG boundaries."""
import unittest
from alexscaves_1010_bouncing_bolt_causal_probe import (
    strict_pairs,edges,exact_pivots,roster,validate_method
)
def op(n,opcode,symbol="",operand=""):
    return {"offset":n,"opcode":opcode,"symbol":symbol,"operand":operand}
def m(name,rows):
    return {"header":"public void "+name+"()",
            "descriptor":"()V","instructions":rows}
class Tests(unittest.TestCase):
    def test_json_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate JSON"):
            strict_pairs([("sha256","a"),("sha256","b")])
    def test_branch_success_and_back_edge(self):
        d=edges(m("use",[op(0,"ifeq",operand="4"),op(3,"goto",operand="0"),
                         op(4,"return")]))
        self.assertEqual(d[0]["fallthrough"],3)
        self.assertEqual(d[1]["target"],0)
        self.assertTrue(d[1]["back_edge"])
    def test_nonexistent_branch_target_fails(self):
        with self.assertRaisesRegex(ValueError,"destination absent"):
            edges(m("use",[op(0,"goto",operand="9"),op(3,"return")]))
    def test_switch_opcode_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"unsupported"):
            edges(m("use",[op(0,"tableswitch"),op(3,"return")]))
    def test_duplicate_offset_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            validate_method(m("use",[op(0,"nop"),op(0,"return")]))
    def test_missing_ricochet_pivot_is_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"causal pivot"):
            exact_pivots(m("damageMobs",[op(220,"getfield","ricochet")]),"damageMobs")
    def test_method_roster_checks_duplicate_identity(self):
        with self.assertRaisesRegex(ValueError,"duplicate method identity"):
            roster([m("getOwner",[op(0,"return")]),m("getOwner",[op(0,"return")])])
if __name__=="__main__":
    unittest.main()
