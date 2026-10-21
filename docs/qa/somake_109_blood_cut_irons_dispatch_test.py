#!/usr/bin/env python3
"""Synthetic method signatures and calls, not redistributed provider bytecode."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_blood_cut_irons_dispatch import survey_overload_family, certify_virtual_lifesteal_bridge

E="Lnet/minecraft/world/entity/Entity;"
S="Lio/redspace/ironsspellbooks/damage/SpellDamageSource;"
ONE="("+E+")"+S
TWO="("+E+E+")"+S

def fixture():
    base=[("getDamageSource",ONE,[
       (0,"aload_0","",""),(1,"aload_1","",""),
       (2,"aconst_null","",""),(3,"invokevirtual","",
        "Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getDamageSource:"+TWO),
       (6,"areturn","","")])]
    child=[("getDamageSource",TWO,[
       (0,"aload_0","",""),(1,"aload_1","",""),(2,"aload_2","",""),
       (3,"invokespecial","","Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getDamageSource:"+TWO),
       (6,"areturn","","")])]
    return base,child

class OverloadFamilyTests(unittest.TestCase):
    def test_distinct_typed_one_vs_two_entity_methods(self):
        b,c=fixture()
        v=survey_overload_family(b,c)
        self.assertEqual(ONE,v["base_one_entity_descriptor"])
        self.assertEqual(TWO,v["child_two_entity_descriptor"])
        self.assertEqual("OVERLOAD_DECLARATIONS_ONLY",v["assurance"])
        self.assertEqual(1,len(v["base_one_arg_getDamageSource_calls"]))

    def test_duplicate_base_one_arg_fails(self):
        b,c=fixture()
        with self.assertRaises(GateError):survey_overload_family(b+b,c)

    def test_wrong_child_return_fails(self):
        b,c=fixture()
        c=[("getDamageSource","("+E+E+")V",c[0][2])]
        with self.assertRaises(GateError):survey_overload_family(b,c)

    def test_missing_child_overload_fails(self):
        b,_=fixture()
        with self.assertRaises(GateError):survey_overload_family(b,[])

    def test_missing_base_one_arg_fails(self):
        _,c=fixture()
        with self.assertRaises(GateError):survey_overload_family([],c)


SOURCE_CALL="Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getDamageSource:"+TWO
SETTER="Method io/redspace/ironsspellbooks/damage/SpellDamageSource.setLifestealPercent:(F)Lio/redspace/ironsspellbooks/damage/SpellDamageSource;"

def bridge_fixture():
    parent=[("getDamageSource",ONE,[
       (0,"aload_0","",""),(1,"aload_1","",""),
       (2,"aconst_null","",""),(3,"invokevirtual","",SOURCE_CALL),
       (6,"areturn","","")])]
    child=[("getDamageSource",TWO,[
       (0,"aload_0","",""),(1,"aload_1","",""),(2,"aload_2","",""),
       (3,"invokespecial","",SOURCE_CALL),
       (6,"ldc","#12","float 0.15f"),
       (8,"invokevirtual","",SETTER),
       (11,"areturn","","")])]
    return parent,child

class NativeVirtualBridgeTests(unittest.TestCase):
    def test_one_arg_virtual_call_reaches_two_arg_015f_setter(self):
        base,child=bridge_fixture()
        proof=certify_virtual_lifesteal_bridge(base,child)
        self.assertEqual("SHA_EXACT_VIRTUAL_DISPATCH_WITH_015F_SETTER",proof["assurance"])
        self.assertEqual("aconst_null",proof["default_second_entity_operand"])
        self.assertEqual(0.15,proof["lifesteal_setter_argument"])
        self.assertEqual("invokevirtual",proof["base_dispatch_opcode"])

    def test_invokespecial_instead_of_virtual_rejected(self):
        base,child=bridge_fixture()
        base[0][2][3]=(3,"invokespecial","",SOURCE_CALL)
        with self.assertRaises(GateError):certify_virtual_lifesteal_bridge(base,child)

    def test_non_null_second_entity_argument_rejected(self):
        base,child=bridge_fixture()
        base[0][2][2]=(2,"aload_2","","")
        with self.assertRaises(GateError):certify_virtual_lifesteal_bridge(base,child)

    def test_setter_float_mutation_rejected(self):
        base,child=bridge_fixture()
        child[0][2][4]=(6,"ldc","#12","float 0.2f")
        with self.assertRaises(GateError):certify_virtual_lifesteal_bridge(base,child)

    def test_child_source_super_dispatch_change_rejected(self):
        base,child=bridge_fixture()
        child[0][2][3]=(3,"invokevirtual","",SOURCE_CALL)
        with self.assertRaises(GateError):certify_virtual_lifesteal_bridge(base,child)

    def test_setter_method_drift_rejected(self):
        base,child=bridge_fixture()
        child[0][2][5]=(8,"invokevirtual","","Method example.Other.setLifestealPercent:(F)V")
        with self.assertRaises(GateError):certify_virtual_lifesteal_bridge(base,child)

if __name__=="__main__":unittest.main()
