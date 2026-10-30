#!/usr/bin/env python3
"""Synthetic boundary checks for Forsaken tick and own-NBT evidence."""
import unittest
from alexscaves_1010_forsaken_timing_probe import (
    ForsakenTimingError,pick,exact_method,find_own,name,strict_pairs
)

def i(offset,op,symbol="",operand=""):
    return {"offset":offset,"opcode":op,"symbol":symbol,"operand":operand}

class TimingTests(unittest.TestCase):
    def test_exact_name_and_descriptor(self):
        m={"header":"public void readAdditionalSaveData(net.minecraft.nbt.CompoundTag)",
           "descriptor":"(Lnet/minecraft/nbt/CompoundTag;)V","instructions":[i(0,"return")]}
        self.assertEqual(name(m),"readAdditionalSaveData")
        self.assertIs(find_own([m],"readAdditionalSaveData",m["descriptor"]),m)
        self.assertIsNone(find_own([m],"addAdditionalSaveData",m["descriptor"]))
        self.assertIs(exact_method([m],"readAdditionalSaveData",m["descriptor"]),m)
    def test_no_unverified_method_selection(self):
        with self.assertRaises(ForsakenTimingError):
            exact_method([],"tick","()V")
    def test_duplicate_declaration_rejected(self):
        m={"header":"public void tick()","descriptor":"()V","instructions":[i(0,"return")]}
        with self.assertRaises(ForsakenTimingError):
            find_own([m,m],"tick","()V")
    def test_window_is_bounded(self):
        m={"header":"public void tick()","descriptor":"()V","instructions":[i(j,"nop") for j in range(80)]}
        m["instructions"][40]=i(40,"getfield","Field sonicEnqueued:Z")
        result=pick(m,("sonicEnqueued",))
        self.assertEqual(result["sites"][0]["offset"],40)
        self.assertEqual(len(result["sites"][0]["window"]),18)
    def test_duplicate_offsets_rejected(self):
        m={"header":"public void tick()","descriptor":"()V",
           "instructions":[i(0,"nop"),i(0,"return")]}
        with self.assertRaisesRegex(ForsakenTimingError,"duplicate"):
            pick(m,("tick",))
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(Exception):
            strict_pairs([("k",1),("k",2)])
if __name__=="__main__":
    unittest.main()
