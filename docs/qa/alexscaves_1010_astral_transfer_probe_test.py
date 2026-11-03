#!/usr/bin/env python3
"""Synthetic negative regressions for SHA-exact Astral Transferring probe."""
import unittest
from alexscaves_1010_astral_transfer_probe import (
    select_consumer,view_consumer,load_resource,DESC,require
)

def ins(offset,op,sym=""):
    return {"offset":offset,"opcode":op,"operand":"","symbol":sym}

def m(instructions):
    return {"header":"public void onUseTick();","descriptor":DESC,
            "instructions":instructions}

class AstralTransferProbeTests(unittest.TestCase):
    def test_rejects_missing_guard(self):
        xs=[ins(i*2,"nop") for i in range(530)]
        with self.assertRaisesRegex(ValueError,"guard"):
            select_consumer([m(xs)])

    def test_rejects_duplicate_guard(self):
        xs=[ins(i*2,"nop") for i in range(530)]
        xs[450]=ins(900,"getstatic","Field ACEnchantmentRegistry.ASTRAL_TRANSFERRING:Ljava/lang/Object;")
        xs[452]=ins(904,"getstatic","Field ACEnchantmentRegistry.ASTRAL_TRANSFERRING:Ljava/lang/Object;")
        with self.assertRaisesRegex(ValueError,"unique"):
            select_consumer([m(xs)])

    def test_rejects_no_transfer_state_write(self):
        xs=[ins(i*2,"nop") for i in range(530)]
        xs[450]=ins(900,"getstatic","Field ACEnchantmentRegistry.ASTRAL_TRANSFERRING:Ljava/lang/Object;")
        with self.assertRaisesRegex(ValueError,"possession setter"):
            view_consumer(m(xs))

    def test_rejects_unsorted_instructions(self):
        xs=[ins(i*2,"nop") for i in range(530)]
        xs[450]=ins(895,"getstatic","Field ACEnchantmentRegistry.ASTRAL_TRANSFERRING:Ljava/lang/Object;")
        with self.assertRaisesRegex(ValueError,"order"):
            select_consumer([m(xs)])

    def test_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"negative"):
            require(False,"negative")

if __name__=="__main__":
    unittest.main()
