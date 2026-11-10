#!/usr/bin/env python3
"""Negative tests for Arrow Inducting JVM lifecycle census."""
import unittest
from alexscaves_1010_arrow_inducting_lifecycle_probe import (
    summarize,select,EVENT,ARROW)
def m(name,ins):
    return {"header":"public void "+name+"()","descriptor":"()V","instructions":ins}
def r(offset,opcode="nop",symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":"","symbol":symbol}
class Tests(unittest.TestCase):
    def test_duplicate_offsets_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            summarize(m("x",[r(0),r(0)]))
    def test_out_of_order_offsets_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"order"):
            summarize(m("x",[r(10),r(1)]))
    def test_missing_event_guard_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            select([m("foo",[r(0)])],EVENT)
    def test_missing_arrow_tick_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            select([m("onHit",[r(0)])],ARROW)
    def test_record_symbol_and_branch(self):
        x=summarize(m("test",[r(0,"getfield","Field owner:Lnet/minecraft/world/entity/Entity;"),
            r(3,"ifle"),r(9,"iconst_1")]))
        self.assertEqual(x["instruction_count"],3)
        self.assertEqual(len(x["refs"]),1)
        self.assertEqual(len(x["branch_edges"]),1)
        self.assertEqual(len(x["numeric_operands"]),1)
    def test_instruction_budget_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"bounds"):
            summarize(m("oversized",[r(i) for i in range(1201)]))
    def test_numeric_budget_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"unbounded"):
            summarize(m("many_constants",[r(i,"bipush") for i in range(181)]))
if __name__=="__main__":
    unittest.main()
