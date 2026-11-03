#!/usr/bin/env python3
"""Fail-closed synthetic tests of Charting Call exact static probe."""
import unittest
from alexscaves_1010_charting_call_probe import find_method,analyze_method,require,SELECTORS,CONCH

def ins(offset,opcode="nop",symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":"","symbol":symbol}

def method(name,descriptor,rows):
    return {"header":"public void "+name+"();","descriptor":descriptor,"instructions":rows}

class ChartingCallProbeTests(unittest.TestCase):
    def test_select_unique(self):
        name,desc,_=SELECTORS[CONCH][0]
        self.assertEqual(find_method([method(name,desc,[ins(i*2) for i in range(25)])],name,desc)["descriptor"],desc)
    def test_missing_method_rejected(self):
        name,desc,_=SELECTORS[CONCH][0]
        with self.assertRaisesRegex(ValueError,"missing"):
            find_method([],name,desc)
    def test_duplicate_method_rejected(self):
        name,desc,_=SELECTORS[CONCH][0]
        m=method(name,desc,[ins(i*2) for i in range(25)])
        with self.assertRaisesRegex(ValueError,"duplicate"):
            find_method([m,m],name,desc)
    def test_duplicate_offset_rejected(self):
        name,desc,_=SELECTORS[CONCH][0]
        xs=[ins(i*2) for i in range(25)]
        xs[15]=ins(28)
        with self.assertRaisesRegex(ValueError,"duplicate"):
            find_method([method(name,desc,xs)],name,desc)
    def test_missing_charting_rejected(self):
        name,desc,_=SELECTORS[CONCH][0]
        with self.assertRaisesRegex(ValueError,"Charting Call"):
            analyze_method(method(name,desc,[ins(i*2) for i in range(25)]),())
    def test_unknown_fixed_anchor_rejected(self):
        name,desc,_=SELECTORS[CONCH][0]
        with self.assertRaisesRegex(ValueError,"fixed exact offset"):
            analyze_method(method(name,desc,[ins(i*2) for i in range(25)]),(2222,))
    def test_no_spawn_bridge_rejected(self):
        name,desc,_=SELECTORS[CONCH][1]
        with self.assertRaisesRegex(ValueError,"placement/spawn"):
            analyze_method(method(name,desc,[ins(i*2) for i in range(25)]),())
    def test_error_for_false_assertion(self):
        with self.assertRaisesRegex(ValueError,"negative"):
            require(False,"negative")

if __name__=="__main__":
    unittest.main()
