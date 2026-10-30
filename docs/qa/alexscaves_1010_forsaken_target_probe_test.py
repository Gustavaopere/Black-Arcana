#!/usr/bin/env python3
"""Fail-closed synthetic Forsaken target ABI and predicate-window tests."""
import unittest
from alexscaves_1010_forsaken_target_probe import (
    ForsakenTargetingError,exact,compact,GOAL
)
def inst(off,op,operand="",symbol=""):
    return {"offset":off,"opcode":op,"operand":operand,"symbol":symbol}
def method(name,desc="()Z",instructions=None):
    return {"header":"public boolean "+name+"()","descriptor":desc,
            "instructions":instructions or [inst(0,"iconst_1"),inst(1,"ireturn")]}

class TargetTests(unittest.TestCase):
    def test_exact_name_and_descriptor(self):
        m=method("canUse")
        self.assertIs(exact([m],"canUse","()Z"),m)
        with self.assertRaises(ForsakenTargetingError):
            exact([m],"canUse","()V")
    def test_lambda_dollar_name(self):
        m=method("lambda$static$0","(Lnet/minecraft/world/entity/LivingEntity;)Z")
        self.assertIs(exact([m],"lambda$static$0",m["descriptor"]),m)
    def test_duplicate_method_rejected(self):
        m=method("canUse")
        with self.assertRaises(ForsakenTargetingError):
            exact([m,m],"canUse","()Z")
    def test_symbolic_and_branch_windows(self):
        m=method("canUse",instructions=[
            inst(0,"aload_0"),inst(1,"invokevirtual","#4","Method Mob.getTarget:()Lnet/minecraft/world/entity/LivingEntity;"),
            inst(4,"ifnull","10"),inst(7,"iconst_1"),inst(8,"ireturn"),inst(10,"iconst_0"),inst(11,"ireturn")])
        r=compact(m)
        self.assertEqual(r["selected_symbolic_windows"][0]["offset"],1)
        self.assertEqual(r["branch_anchors"][0]["opcode"],"ifnull")
        self.assertEqual(len(r["exit_sites"]),2)
    def test_duplicate_offsets_rejected(self):
        with self.assertRaises(ForsakenTargetingError):
            compact(method("stop",instructions=[inst(0,"nop"),inst(0,"return")]))
    def test_passthrough_instructions_are_preserved(self):
        m=method("targetSelector","(Ljava/util/function/Predicate;)Ljava/util/function/Predicate;",
                 [inst(0,"aload_0"),inst(1,"areturn")])
        result=compact(m)
        self.assertEqual(result["instructions"],m["instructions"])
        self.assertEqual(result["selected_symbolic_windows"],[])
    def test_bounded_maximum_rejected(self):
        with self.assertRaises(ForsakenTargetingError):
            compact(method("stop",instructions=[inst(i,"nop") for i in range(421)]))
if __name__=="__main__":
    unittest.main()
