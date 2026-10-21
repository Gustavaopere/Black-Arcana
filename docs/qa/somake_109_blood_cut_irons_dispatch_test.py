#!/usr/bin/env python3
"""Synthetic method signatures and calls, not redistributed provider bytecode."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_blood_cut_irons_dispatch import survey_overload_family

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

if __name__=="__main__":unittest.main()
