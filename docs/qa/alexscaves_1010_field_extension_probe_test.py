#!/usr/bin/env python3
"""Fail-closed synthetic tests for the exact Field Extension publisher probe."""
import unittest

from alexscaves_1010_field_extension_probe import (
    MUST_HAVE, SCOPE, locate_tick, validate_windows, verify_enchant, require
)

def ins(offset):
    return {"offset":offset,"opcode":"nop","operand":"","symbol":""}

def rows():
    allrows=[ins(i) for i in range(900)]
    for offset,(op,needle) in MUST_HAVE.items():
        allrows[offset]["opcode"]=op
        allrows[offset]["symbol"]="Method "+needle
    allrows[644]["operand"]="8"
    allrows[656]["operand"]="8"
    return allrows

class FieldExtensionProbeTests(unittest.TestCase):
    def test_scope(self):
        self.assertIn("1010",SCOPE)
        self.assertEqual(len(MUST_HAVE),12)

    def test_wrong_identity_fails(self):
        with self.assertRaisesRegex(ValueError,"wrong field extension identity"):
            verify_enchant({"json":{"description":{"translate":"bad"}}},
                           {"json":{"values":[]}})

    def test_wrong_max_level_fails(self):
        e={"json":{"description":{"translate":"enchantment.alexscaves.field_extension"},
                   "supported_items":"#alexscaves:enchantable/galena_gauntlet",
                   "max_level":3,"weight":10}}
        with self.assertRaisesRegex(ValueError,"maximum level"):
            verify_enchant(e,{"json":{"values":["alexscaves:galena_gauntlet"]}})

    def test_valid_window_selection(self):
        validate_windows(rows())

    def test_wrong_constant_rejected(self):
        x=rows()
        x[639]["symbol"]="float 6.0f"
        with self.assertRaisesRegex(ValueError,"@639"):
            validate_windows(x)

    def test_wrong_raycast_local_rejected(self):
        x=rows()
        x[656]["operand"]="7"
        with self.assertRaisesRegex(ValueError,"range local"):
            validate_windows(x)

    def test_missing_tick_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing or ambiguous"):
            locate_tick([])

    def test_reject_malformed_method_count(self):
        m={"header":"public void tick();","descriptor":"()V",
           "instructions":[ins(x) for x in range(10)]}
        with self.assertRaisesRegex(ValueError,"instruction count"):
            locate_tick([m])

    def test_require_blocks_negative(self):
        with self.assertRaisesRegex(ValueError,"negative"):
            require(False,"negative")

if __name__=="__main__":
    unittest.main()
