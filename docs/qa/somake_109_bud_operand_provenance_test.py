#!/usr/bin/env python3
"""Synthetic own fixtures for typed metadata; fail closed for descriptor drift."""
import unittest
from somake_109_bud_operand_provenance import classify_comment, describe_instruction, scout
D="(Lnet/minecraft/server/level/ServerLevel;)V"
def fixture():
    ops=[f"{i}: nop" for i in range(279)]
    ops[34]="34: aload 4"
    ops[89]="89: getfield #12 // Field witherDuration:I"
    ops[120]="120: aload 8"
    ops[125]="125: getfield #13 // Field witherDuration:I"
    ops[131]='131: invokespecial #19 // Method net/minecraft/world/effect/MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;IIZZZ)V'
    ops[136]="136: ldc2_w #20 // double 0.42d"
    ops[138]="138: invokevirtual #21 // Method net/minecraft/world/entity/Entity.push:(DDD)V"
    ops[146]="146: aload 4"
    ops[148]="148: iload 6"
    ops[159]="159: iinc 6, 1"
    ops[168]="168: invokeinterface #32, 2 // InterfaceMethod net/neoforged/bus/api/IEventBus.post:(Lnet/neoforged/bus/api/Event;)Lnet/neoforged/bus/api/Event;"
    return [("impact",D,ops)]
class ScoutTests(unittest.TestCase):
    def test_scoped_windows_and_types_are_observations_only(self):
        proof=scout(fixture())
        self.assertEqual("OBSERVED_TYPED_OPERAND_WINDOWS_ONLY",proof["status"],proof)
        self.assertEqual(279,proof["instruction_count"])
        self.assertEqual(6,len(proof["ranges"]))
        self.assertIn("NOT_PROVED",proof["boundary"])
    def test_local_and_call_metadata(self):
        x=describe_instruction(__import__("somake_109_radius_irons_contract",fromlist=["opcode_rows"]).opcode_rows(fixture()[0][2]),146)
        self.assertEqual(4,x["slot"])
        self.assertEqual("call",classify_comment("invokevirtual",
            "Method net/minecraft/world/entity/Entity.push:(DDD)V")["kind"])
    def test_wrong_signature_fails_closed(self):
        self.assertEqual("NOT_PROVED",scout([("impact","()V",fixture()[0][2])])["status"])
    def test_ambiguous_member_fails_closed(self):
        self.assertEqual("NOT_PROVED",scout(fixture()*2)["status"])
    def test_missing_instruction_fails_closed(self):
        x=fixture();x[0][2].pop()
        self.assertEqual("NOT_PROVED",scout(x)["status"])
    def test_no_copy_of_jvm_comments(self):
        p=scout(fixture())
        self.assertNotIn("raw_code",str(p))
        self.assertNotIn("vendor_method_body",str(p))
if __name__=="__main__":
    unittest.main()
