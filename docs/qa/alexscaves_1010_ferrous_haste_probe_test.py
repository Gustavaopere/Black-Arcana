#!/usr/bin/env python3
"""Synthetic fail-closed tests for the Ferrous Haste exact-JAR probe."""
import unittest
from alexscaves_1010_ferrous_haste_probe import (
    WEAPON, SCOPE, PIVOTS, check_json, extract, select_method, require
)

def ins(offset, opcode="nop", symbol=""):
    return {"offset":offset, "opcode":opcode, "operand":"", "symbol":symbol}

def method(name, rows):
    return {"header":f"public void {name}();",
            "descriptor":"()V", "instructions":rows}

class FerrousHasteProbeTests(unittest.TestCase):
    def test_scope(self):
        self.assertIn("1010",SCOPE)
        self.assertIn("tick",PIVOTS)
    def test_wrong_resource_rejected(self):
        e={"json":{"description":{"translate":"wrong"},"supported_items":"#alexscaves:enchantable/galena_gauntlet","max_level":1}}
        t={"json":{"values":["alexscaves:galena_gauntlet"]}}
        with self.assertRaisesRegex(ValueError,"wrong enchantment"):
            check_json(e,t)
    def test_missing_supported_item_rejected(self):
        e={"json":{"description":{"translate":"enchantment.alexscaves.ferrous_haste"},"supported_items":"#alexscaves:enchantable/galena_gauntlet","max_level":1}}
        t={"json":{"values":[]}}
        with self.assertRaisesRegex(ValueError,"absent"):
            check_json(e,t)
    def test_ambiguous_methods_rejected(self):
        m=method("tick",[ins(i*3) for i in range(15)])
        with self.assertRaisesRegex(ValueError,"ambiguous"):
            select_method([m,m],"tick")
    def test_unsorted_method_rejected(self):
        arr=[ins(i*3) for i in range(15)]
        arr[5]=ins(4)
        with self.assertRaisesRegex(ValueError,"unsorted"):
            select_method([method("tick",arr)],"tick")
    def test_missing_haste_gate_rejected(self):
        arr=[ins(i*3+575) for i in range(28)]
        with self.assertRaisesRegex(ValueError,"FERROUS_HASTE"):
            extract(method("tick",arr))
    def test_wrong_method_population_rejected(self):
        with self.assertRaisesRegex(ValueError,"size"):
            select_method([method("tick",[ins(i) for i in range(1901)])],"tick")
    def test_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"negative"):
            require(False,"negative")

if __name__=="__main__":
    unittest.main()
