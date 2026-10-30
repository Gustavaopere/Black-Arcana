#!/usr/bin/env python3
"""Fail-closed regression for exact helper descriptors and bounded JVM windows."""
import unittest
from alexscaves_1010_forsaken_helper_probe import (
    ForsakenHelperError,exact_method,bounded_window,compact,GOAL
)
def ins(n,op,symbol="",operand=""):
    return {"offset":n,"opcode":op,"operand":operand,"symbol":symbol}
def method(name="tryAnimation",desc="()Z"):
    return {"header":"private boolean "+name+"()","descriptor":desc,"instructions":[
        ins(0,"iconst_1"),ins(1,"ifeq","","4"),ins(4,"ireturn")]}

class ForsakenHelpersTests(unittest.TestCase):
    def test_descriptor_must_match(self):
        m=method()
        self.assertIs(exact_method([m],"tryAnimation","()Z"),m)
        with self.assertRaisesRegex(ForsakenHelperError,"missing"):
            exact_method([m],"tryAnimation","()V")
    def test_duplicate_exact_method_rejected(self):
        m=method()
        with self.assertRaisesRegex(ForsakenHelperError,"ambiguous"):
            exact_method([m,m],"tryAnimation","()Z")
    def test_bounded_window(self):
        rows=[ins(i,"nop") for i in range(60)]
        self.assertEqual(len(bounded_window(rows,30)),15)
        self.assertEqual(len(bounded_window(rows,30,11,0)),12)
    def test_branch_and_return_are_not_runtime_certified(self):
        m=method()
        parsed=compact(m,GOAL,"tryAnimation")
        self.assertEqual(parsed["branch_anchors"][0]["simple_target"],4)
        self.assertEqual(parsed["constant_anchors"][0]["opcode"],"iconst_1")
        self.assertEqual(parsed["return_instruction_windows"][0]["at"],4)
        self.assertEqual(parsed["decision_reachability"],"NOT_VERIFIED")
    def test_duplicate_instruction_fails_closed(self):
        m=method()
        m["instructions"].append(ins(0,"return"))
        with self.assertRaisesRegex(ForsakenHelperError,"duplicate"):
            compact(m,GOAL,"tryAnimation")
    def test_instruction_budget_fail_closed(self):
        m=method()
        m["instructions"]=[ins(i,"nop") for i in range(1401)]
        with self.assertRaisesRegex(ForsakenHelperError,"unbounded"):
            compact(m,GOAL,"tryAnimation")

if __name__=="__main__":
    unittest.main()
