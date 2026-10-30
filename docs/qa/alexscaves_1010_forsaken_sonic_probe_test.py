#!/usr/bin/env python3
"""Synthetic assertions for the Forsaken Sonic Boom bytecode probe."""
import unittest
from alexscaves_1010_forsaken_sonic_probe import (
    ForsakenEvidenceError, method_name, strict_pairs, clipped, summarize, GOAL
)
def ins(offset,op,operand="",symbol=""):
    return {"offset":offset,"opcode":op,"operand":operand,"symbol":symbol}

class ForsakenSonicProbeTests(unittest.TestCase):
    def test_method_name_from_header(self):
        self.assertEqual(method_name({"header":"public void knockBackAngle(net.minecraft.world.entity.LivingEntity, double, float)"}),"knockBackAngle")
        self.assertEqual(method_name({"header":"public void tick()"}),"tick")
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(ForsakenEvidenceError,"duplicate"):
            strict_pairs([("k",1),("k",2)])
    def test_bounded_window(self):
        array=[ins(x,"nop") for x in range(70)]
        self.assertEqual(len(clipped(array,30,8)),17)
        self.assertEqual(clipped(array,30,8)[0]["offset"],22)
    def test_unsafe_offset_collision(self):
        meth={"header":"public void start()","descriptor":"()V",
              "instructions":[ins(0,"nop"),ins(0,"return")]}
        with self.assertRaisesRegex(ForsakenEvidenceError,"duplicate"):
            summarize(GOAL,meth)
    def test_no_unsealed_tick_callsite_accepted(self):
        meth={"header":"public void tick()","descriptor":"()V",
              "instructions":[ins(0,"return")]}
        with self.assertRaises(ForsakenEvidenceError):
            summarize(GOAL,meth)
    def test_conditional_jump_recorded(self):
        meth={"header":"public boolean canUse()","descriptor":"()Z",
              "instructions":[ins(0,"iconst_1"),ins(1,"ifne","5"),ins(4,"iconst_0"),ins(5,"ireturn")]}
        result=summarize(GOAL,meth)
        self.assertEqual(result["branch_anchors"][0]["simple_target"],5)
        self.assertEqual(result["numeric_constant_anchors"][0]["opcode"],"iconst_1")
        self.assertEqual(result["hook_mutability"],"NOT_VERIFIED")

if __name__=="__main__":
    unittest.main()
