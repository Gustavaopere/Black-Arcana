#!/usr/bin/env python3
"""Synthetic fail-closed JVM CFG and linkage tests for two exact provider artifacts."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_radius_irons_contract import (
    POWER_DESC, SOMAKE_GETTER_DESC, radius_cfg, callsite_descriptors, opcode_rows, sections,
)

RADIUS=[
    "    Code:",
    "       0: iload_1",
    "       1: ifeq 15",
    "       4: fconst_1",
    "       5: ldc #7 // float 10.0f",
    "       7: ldc #8 // float 15.0f",
    "       9: invokestatic #9 // Method net/minecraft/util/Mth.clamp:(FFF)F",
    "      12: freturn",
    "      15: fconst_0",
    "      16: freturn",
]
DAMAGE=[
    "    Code:",
    "       0: aload_0",
    "       1: iload_1",
    "       2: aload_2",
    "       3: invokevirtual #3 // Method getSpellPower:(ILnet/minecraft/world/entity/Entity;)F",
    "       6: freturn",
]
CLASSFILE="""public class FuneralBloomSpell {
  public float getRadius(int, net.minecraft.world.entity.LivingEntity);
    descriptor: (ILnet/minecraft/world/entity/LivingEntity;)F
    Code:
       0: iload_1
       1: ifeq 10
       4: fconst_0
       5: freturn
      10: fconst_1
      11: freturn
  public float getImpactDamage(int, net.minecraft.world.entity.LivingEntity);
    descriptor: (ILnet/minecraft/world/entity/LivingEntity;)F
    Code:
       0: aload_0
       1: iload_1
       2: aload_2
       3: invokevirtual #3 // Method getSpellPower:(ILnet/minecraft/world/entity/Entity;)F
       6: freturn
}
"""
class CfgContracts(unittest.TestCase):
    def test_two_live_paths(self):
        result=radius_cfg(RADIUS)
        self.assertEqual(1,result["conditional_branches"])
        self.assertEqual(2,result["terminal_returns"])
        self.assertEqual(len(opcode_rows(RADIUS)),result["reachable_instruction_count"])
        self.assertEqual(["ifeq"],result["branch_predicates"])
        self.assertEqual(0,result["back_edges"])

    def test_invalid_target_fail_closed(self):
        broken=[x.replace("ifeq 15","ifeq 999") for x in RADIUS]
        with self.assertRaises(GateError):
            radius_cfg(broken)

    def test_unreachable_block_fail_closed(self):
        broken=[x.replace("ifeq 15","goto 15") for x in RADIUS]
        with self.assertRaises(GateError):
            radius_cfg(broken)

    def test_unsupported_switch_fail_closed(self):
        with self.assertRaises(GateError):
            radius_cfg(["0: tableswitch","1: freturn"])

    def test_callsite_binary_descriptor(self):
        self.assertEqual([POWER_DESC],callsite_descriptors(DAMAGE,"getSpellPower"))
        self.assertEqual([],callsite_descriptors(DAMAGE,"getSchoolType"))

    def test_missing_callsite_signature_fail_closed(self):
        broken=[x.replace("getSpellPower:(ILnet/minecraft/world/entity/Entity;)F","getSpellPower") for x in DAMAGE]
        with self.assertRaises(GateError):
            callsite_descriptors(broken,"getSpellPower")

    def test_sections_exact_descriptors(self):
        result=sections(CLASSFILE)
        self.assertEqual(["getRadius","getImpactDamage"],[x[0] for x in result])
        self.assertEqual([SOMAKE_GETTER_DESC,SOMAKE_GETTER_DESC],[x[1] for x in result])

    def test_invalid_duplicate_method_offsets(self):
        with self.assertRaises(GateError):
            opcode_rows(["0: fconst_1","0: freturn"])

    def test_negative_method_scope_missing_desc(self):
        with self.assertRaises(GateError):
            sections(CLASSFILE.replace("descriptor: (ILnet/minecraft/world/entity/LivingEntity;)F","descriptor removed",1))

if __name__=="__main__":
    unittest.main()
