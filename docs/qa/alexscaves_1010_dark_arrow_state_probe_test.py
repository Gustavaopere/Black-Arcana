#!/usr/bin/env python3
import unittest
from alexscaves_1010_dark_arrow_state_probe import (
    ProbeError, field_offsets, relevant_offsets, method_record, strict_pairs
)
F = lambda off,op,sym: {"offset":off,"opcode":op,"operand":"","symbol":sym}
class DarkArrowStateProbeTests(unittest.TestCase):
    def setUp(self):
        self.arrow={"header":"public void setPerfectShot(boolean)","descriptor":"(Z)V",
            "instructions":[
                F(0,"aload_0",""),
                F(1,"getstatic","Field PERFECT_SHOT:Lnet/minecraft/network/syncher/EntityDataAccessor;"),
                F(4,"invokevirtual","Method net/minecraft/network/syncher/SynchedEntityData.set:(Lnet/minecraft/network/syncher/EntityDataAccessor;Ljava/lang/Object;)V"),
                F(7,"return","")
            ]}
    def test_writer_offsets_and_context(self):
        self.assertEqual(field_offsets(self.arrow),[1])
        self.assertEqual(relevant_offsets(self.arrow,True),[1,2])
        record=method_record(self.arrow,[1,2])
        self.assertEqual(record["anchors"][0]["offset"],1)
        self.assertEqual(record["control_flow_reachability"],"NOT_PROVEN")
    def test_other_class_needs_direct_reference(self):
        self.assertEqual(relevant_offsets(self.arrow,False),[])
    def test_other_class_can_call_dark_arrow(self):
        m={"header":"public void shoot()","descriptor":"()V",
           "instructions":[F(0,"invokevirtual",
                             "Method com/github/alexmodguy/alexscaves/server/entity/item/DarkArrowEntity.setPerfectShot:(Z)V")]}
        self.assertEqual(relevant_offsets(m,False),[0])
    def test_no_guess_of_unobserved_setter(self):
        m={"header":"public void noop()","descriptor":"()V","instructions":[F(0,"return","")]}
        self.assertEqual(relevant_offsets(m,True),[])
    def test_duplicate_offset_fails_closed(self):
        m=dict(self.arrow);m["instructions"]=self.arrow["instructions"]+self.arrow["instructions"]
        with self.assertRaisesRegex(ProbeError,"duplicate JVM"):
            method_record(m,[1])
    def test_duplicate_json_key_fails_closed(self):
        with self.assertRaisesRegex(ProbeError,"duplicate JSON"):
            strict_pairs([("x",1),("x",2)])
if __name__=="__main__":
    unittest.main()
