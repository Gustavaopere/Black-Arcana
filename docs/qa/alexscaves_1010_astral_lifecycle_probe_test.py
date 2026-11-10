#!/usr/bin/env python3
"""Fail-closed synthetic tests for 1.0.10 Totem lifecycle inspection."""
import unittest
from alexscaves_1010_astral_lifecycle_probe import (
  strict_pairs,exact_method,method_summary,transfer_region,branch_target,require,
  TRANSFER_DESC
)
def op(offset,opcode,operand="",symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":operand,"symbol":symbol}
def method(name,body,desc="()V"):
    return {"header":"public void "+name+"()","descriptor":desc,
            "instructions":body}
class Tests(unittest.TestCase):
    def test_duplicate_json_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            strict_pairs([("sha256","one"),("sha256","forged")])
    def test_method_overload_requires_descriptor(self):
        a=method("onUseTick",[],TRANSFER_DESC)
        b=method("onUseTick",[],"(I)V")
        self.assertIs(exact_method([a,b],"onUseTick",TRANSFER_DESC),a)
        with self.assertRaisesRegex(ValueError,"ambiguous"):
            exact_method([a,b],"onUseTick")
    def test_branch_back_edges_and_outgoing(self):
        self.assertEqual(branch_target(op(100,"ifne","120")),120)
        self.assertIsNone(branch_target(op(100,"invokevirtual","#55","Method foo")))
        s=method_summary(method("tick",[op(0,"goto","0"),op(2,"ifne","5"),op(5,"return")]))
        self.assertEqual(s["branch_count"],2)
        self.assertTrue(s["branches"][0]["is_back_edge"])
        self.assertFalse(s["branches"][1]["is_back_edge"])
    def test_duplicate_or_unsorted_instructions_rejected(self):
        with self.assertRaisesRegex(ValueError,"invalid"):
            method_summary(method("tick",[op(4,"nop"),op(2,"nop")]))
        with self.assertRaisesRegex(ValueError,"invalid"):
            method_summary(method("tick",[op(2,"nop"),op(2,"return")]))
    def test_transfer_requires_all_native_pivots(self):
        with self.assertRaisesRegex(ValueError,"unexpected native"):
            transfer_region(method("onUseTick",[op(920,"getstatic",symbol="ASTRAL_TRANSFERRING")],TRANSFER_DESC))
    def test_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"no contract"):
            require(False,"no contract")
if __name__=="__main__":
    unittest.main()
