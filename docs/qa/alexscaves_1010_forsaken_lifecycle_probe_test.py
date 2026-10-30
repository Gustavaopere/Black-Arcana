#!/usr/bin/env python3
import unittest
from alexscaves_1010_forsaken_lifecycle_probe import (
    LifecycleProbeError,selected_symbol,compact
)

def ins(off,op,sym="",operand=""):
    return {"offset":off,"opcode":op,"operand":operand,"symbol":sym}

class ForsakenLifecycleTests(unittest.TestCase):
    def test_selected_symbols(self):
        self.assertTrue(selected_symbol("Method ForsakenEntity.setAnimation:(...)V"))
        self.assertTrue(selected_symbol("Field sonicEnqueued:Z"))
        self.assertFalse(selected_symbol("Method SomethingCompletelyUnrelated:()V"))
    def test_synthetic_bounded_method(self):
        m={"header":"public void registerGoals()","descriptor":"()V",
           "instructions":[ins(0,"aload_0"),
              ins(1,"invokevirtual","Method GoalSelector.addGoal:(ILnet/minecraft/world/entity/ai/goal/Goal;)V"),
              ins(4,"iconst_1"),ins(5,"ifne","","9"),ins(8,"return"),ins(9,"return")]}
        d=compact(m)
        self.assertEqual(d["selected_symbol_windows"][0]["at"],1)
        self.assertEqual(d["branches"][0]["simple_target"],9)
        self.assertEqual(len(d["returns"]),2)
        self.assertEqual(d["runtime_reachability"],"NOT_VERIFIED")
    def test_duplicate_jvm_offset_rejected(self):
        m={"header":"public void foo()","descriptor":"()V",
           "instructions":[ins(0,"nop"),ins(0,"return")]}
        with self.assertRaisesRegex(LifecycleProbeError,"duplicate"):
            compact(m)
    def test_method_size_rejected(self):
        m={"header":"public void foo()","descriptor":"()V",
           "instructions":[ins(i,"nop") for i in range(4501)]}
        with self.assertRaisesRegex(LifecycleProbeError,"size"):
            compact(m)
    def test_oversized_symbol_population_rejected(self):
        m={"header":"public void foo()","descriptor":"()V",
           "instructions":[ins(i,"invokevirtual","Method X.setAnimation:()V")
                           for i in range(126)]}
        with self.assertRaisesRegex(LifecycleProbeError,"symbolic"):
            compact(m)
    def test_empty_unverified_state_fails_closed(self):
        with self.assertRaises(LifecycleProbeError):
            compact({"header":"public void foo()","descriptor":"()V","instructions":[]})

if __name__=="__main__":
    unittest.main()
