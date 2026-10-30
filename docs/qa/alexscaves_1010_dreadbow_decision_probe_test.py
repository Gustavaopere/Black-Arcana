#!/usr/bin/env python3
"""Synthetic fail-closed regressions for exact Dreadbow decision anchor logic."""
import unittest
from alexscaves_1010_dreadbow_decision_probe import (
    DecisionAuditError, method_lookup, local8_10, clipped_window, strict_pairs
)

def inst(offset, opcode, operand="", symbol=""):
    return {"offset":offset,"opcode":opcode,"operand":operand,"symbol":symbol}

class DreadbowDecisionTests(unittest.TestCase):
    def test_local_slot_exact_normal_form(self):
        self.assertEqual(local8_10(inst(3,"iload","8")),8)
        self.assertEqual(local8_10(inst(3,"istore","10")),10)
        self.assertEqual(local8_10(inst(3,"iload_8")),8)
        self.assertEqual(local8_10(inst(3,"istore_10")),10)
    def test_rejects_other_slots_and_unrelated_symbols(self):
        self.assertIsNone(local8_10(inst(3,"iload","18")))
        self.assertIsNone(local8_10(inst(3,"aload","10")))
        self.assertIsNone(local8_10(inst(3,"getfield","", "Field local10:I")))
    def test_exact_descriptor_only(self):
        m={"header":"public void releaseUsing(net.minecraft.world.item.ItemStack)",
           "descriptor":"(Lnet/minecraft/world/item/ItemStack;)V","instructions":[]}
        self.assertIs(method_lookup([m],"releaseUsing",m["descriptor"]),m)
        with self.assertRaisesRegex(DecisionAuditError,"missing"):
            method_lookup([m],"releaseUsing","()V")
    def test_reject_ambiguous_method(self):
        m={"header":"public void releaseUsing()","descriptor":"()V","instructions":[]}
        with self.assertRaisesRegex(DecisionAuditError,"ambiguous"):
            method_lookup([m,m],"releaseUsing","()V")
    def test_window_bounded(self):
        xs=[inst(i,"nop") for i in range(60)]
        self.assertEqual(len(clipped_window(xs,40)),17)
        self.assertEqual(len(clipped_window(xs,0)),9)
        self.assertEqual(clipped_window(xs,40)[0]["offset"],32)
    def test_duplicate_json_rejected(self):
        with self.assertRaisesRegex(DecisionAuditError,"duplicate"):
            strict_pairs([("x",1),("x",2)])
if __name__=="__main__":
    unittest.main()
