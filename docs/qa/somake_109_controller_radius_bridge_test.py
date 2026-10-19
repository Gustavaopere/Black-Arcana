#!/usr/bin/env python3
"""Positive/negative direct field provenance fixtures; no provider bytecode."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_controller_radius_bridge import (
  FQCN,CONSTRUCTOR_DESC,FLOAT_SLOTS,GETTER_DESC,
  analyze,local_id,direct_float_getter,constructor_direct_assignments
)

def specimen(getter=None,slot=3):
    getter=getter or [
        "0: aload_0",
        "1: getfield #10 // Field radius:F",
        "4: freturn",
    ]
    return (
       "public class "+FQCN+" {\n"
       "  public "+FQCN+"(net.minecraft.world.level.Level,net.minecraft.world.entity.LivingEntity,float,int,int,int,int,float,int,int);\n"
       "    descriptor: "+CONSTRUCTOR_DESC+"\n"
       "    Code:\n"
       "       0: aload_0\n"
       "       1: invokespecial #1 // Method java/lang/Object.\"<init>\":()V\n"
       "       4: aload_0\n"
       "       5: fload "+str(slot)+"\n"
       "       7: putfield #10 // Field radius:F\n"
       "      10: return\n"
       "  public float getRadius();\n"
       "    descriptor: "+GETTER_DESC+"\n"
       "    Code:\n"
       +"".join("      "+s+"\n" for s in getter)
       +"}\n"
    )

class RadiusBridgeTests(unittest.TestCase):
    def test_direct_float_arg3_maps_to_exact_radius_field(self):
        result=analyze(specimen())
        self.assertEqual("PROVED_DIRECT_INSTANCE_FLOAT_GETTER",result["getter"]["status"])
        binding=result["constructor_to_getter"]
        self.assertEqual("PROVED_DIRECT_FLOAT_ARGUMENT_FIELD_BINDING",binding["status"])
        self.assertEqual(3,binding["jvm_local_slot"])
        self.assertEqual(1,binding["float_ordinal"])

    def test_second_float_slot_maps_without_guess(self):
        result=analyze(specimen(slot=8))
        self.assertEqual(8,result["constructor_to_getter"]["jvm_local_slot"])
        self.assertEqual(2,result["constructor_to_getter"]["float_ordinal"])

    def test_getter_with_operation_is_not_certified_direct(self):
        getter=["0: aload_0","1: getfield #10 // Field radius:F",
                "4: fconst_1","5: fadd","6: freturn"]
        x=analyze(specimen(getter=getter))
        self.assertEqual("NOT_PROVED",x["getter"]["status"])
        self.assertEqual("NOT_PROVED",x["constructor_to_getter"]["status"])

    def test_field_conflict_rejected(self):
        x=analyze(specimen().replace("putfield #10 // Field radius:F",
                                     "putfield #10 // Field impactDamage:F"))
        self.assertEqual("NOT_PROVED",x["constructor_to_getter"]["status"])

    def test_unknown_local_source_not_guessed(self):
        x=analyze(specimen(slot=4))
        self.assertEqual("NOT_PROVED",x["constructor_to_getter"]["status"])

    def test_descriptor_mismatch_rejected(self):
        with self.assertRaises(GateError):
            analyze(specimen().replace(CONSTRUCTOR_DESC,"(IF)V",1))

    def test_duplicate_field_writes_fail_closed(self):
        body=["0: aload_0","1: fload_3","2: putfield #1 // Field radius:F",
              "5: aload_0","6: fload 8","8: putfield #1 // Field radius:F","11: return"]
        x=constructor_direct_assignments(body,"radius")
        self.assertEqual("NOT_PROVED",x["status"])
        self.assertEqual(2,x["field_write_count"])

    def test_strict_load_slot_parser(self):
        self.assertEqual(0,local_id("aload_0","","aload"))
        self.assertEqual(8,local_id("fload","8","fload"))
        self.assertIsNone(local_id("dload_2","","fload"))

if __name__=="__main__":unittest.main()
