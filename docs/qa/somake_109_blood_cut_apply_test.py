#!/usr/bin/env python3
"""Provider-independent synthetic callsite guards for second-damage inspector."""
import unittest

from somake_109_blood_cut_apply import survey_application
from somake_109_perk_method_probe import GateError

APPLY=("Method io/redspace/ironsspellbooks/damage/DamageSources."
       "applyDamage:(Lnet/minecraft/world/entity/Entity;"
       "FLnet/minecraft/world/damagesource/DamageSource;)Z")

def fixture():
    return [
      (0,"aload_0","",""),
      (1,"invokevirtual","","Method example.Event.getNewDamage:()F"),
      (4,"fstore_3","",""),
      (5,"aload_1","",""),
      (6,"fload_3","",""),
      (7,"aload_2","",""),
      (8,"invokestatic","",APPLY),
      (11,"pop","",""),
      (12,"return","",""),
    ]

class ApplyCallsiteTests(unittest.TestCase):
    def test_uniquely_typed_static_damage_callsite_report(self):
        report=survey_application(fixture())
        self.assertEqual(1,report["apply_damage_callsite_count"])
        self.assertEqual(7,report["apply_damage_instruction_index"])
        self.assertEqual("STATIC_CALLSITE_SURVEY_ONLY",report["assurance"])
        self.assertIn("fload_3",report["preceding_opcode_kinds"])
        self.assertIn("invoke",report["invocation_opcode_families"])

    def test_missing_damage_site_rejected(self):
        rows=fixture()
        rows[7]=(8,"invokestatic","","Method other.apply:()V")
        with self.assertRaises(GateError):survey_application(rows)

    def test_duplicate_damage_site_rejected(self):
        rows=fixture()
        rows.insert(8,(9,"invokestatic","",APPLY))
        with self.assertRaises(GateError):survey_application(rows)

    def test_unordered_program_counters_rejected(self):
        rows=fixture()
        rows[5]=(1,"fload_3","","")
        with self.assertRaises(GateError):survey_application(rows)

    def test_wrong_invoke_category_rejected(self):
        rows=fixture()
        rows[7]=(8,"getfield","",APPLY)
        with self.assertRaises(GateError):survey_application(rows)

if __name__=="__main__":
    unittest.main()
