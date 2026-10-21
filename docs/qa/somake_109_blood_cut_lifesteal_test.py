#!/usr/bin/env python3
"""No third-party bytecode fixtures; synthetic hardening gates for lifesteal."""
import unittest
from somake_109_blood_cut_lifesteal import survey
from somake_109_perk_method_probe import GateError

BASE="Method io/redspace/ironsspellbooks/api/spells/AbstractSpell.getDamageSource:(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/entity/Entity;)Lio/redspace/ironsspellbooks/damage/SpellDamageSource;"
SETTER="Method io/redspace/ironsspellbooks/damage/SpellDamageSource.setLifestealPercent:(F)V"

def fixture():
    return [
        (0,"aload_0","",""),
        (1,"invokespecial","",BASE),
        (4,"ldc","#17","float 0.25f"),
        (6,"invokevirtual","",SETTER),
        (9,"areturn","",""),
    ]

def native_shape():
    return [
        (0,"aload_0","",""),
        (1,"aload_1","",""),
        (2,"aload_2","",""),
        (3,"invokespecial","",BASE),
        (7,"ldc","#17","float 0.15f"),
        (9,"invokevirtual","",SETTER),
        (12,"areturn","",""),
    ]

class LifestealReferenceTests(unittest.TestCase):
    def test_one_base_and_one_typed_setter(self):
        s=survey(fixture())
        self.assertEqual(1,s["base_source_call_index"])
        self.assertEqual(3,s["lifesteal_setter_call_index"])
        self.assertTrue(s["setter_typed_float_argument"])
        self.assertEqual("ldc",s["immediate_argument_producer_opcode"])

    def test_015_float_is_certified_as_direct_setter_argument(self):
        p=survey(native_shape())
        self.assertEqual(0.15,p["certified_lifesteal_float_argument"])
        self.assertTrue(p["literal_adjacent_to_setter"])

    def test_changed_float_literal_fails_closed(self):
        rows=native_shape()
        rows[4]=(7,"ldc","#17","float 0.25f")
        with self.assertRaises(GateError):
            survey(rows)

    def test_intervening_float_transform_fails_closed(self):
        rows=native_shape()
        rows[4]=(7,"fmul","","")
        with self.assertRaises(GateError):
            survey(rows)

    def test_duplicated_setter_rejected(self):
        rows=fixture()
        rows.insert(4,(7,"invokevirtual","",SETTER))
        with self.assertRaises(GateError):survey(rows)

    def test_missing_base_source_rejected(self):
        rows=fixture();rows[1]=(1,"nop","","")
        with self.assertRaises(GateError):survey(rows)

    def test_wrong_argument_descriptor_rejected(self):
        rows=fixture();rows[3]=(6,"invokevirtual","",SETTER.replace("(F)","(D)"))
        with self.assertRaises(GateError):survey(rows)

    def test_source_after_setter_rejected(self):
        rows=fixture();rows[1]=(1,"invokevirtual","",SETTER)
        rows[3]=(6,"invokespecial","",BASE)
        with self.assertRaises(GateError):survey(rows)

    def test_no_object_return_rejected(self):
        rows=fixture();rows[-1]=(9,"return","","")
        with self.assertRaises(GateError):survey(rows)

    def test_unordered_pcs_rejected(self):
        rows=fixture();rows[2]=(0,"ldc","#17","float 0.25f")
        with self.assertRaises(GateError):survey(rows)

if __name__=="__main__":
    unittest.main()
