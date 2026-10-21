#!/usr/bin/env python3
"""Provider-independent synthetic callsite guards for second-damage inspector."""
import unittest

from somake_109_blood_cut_apply import survey_application, certify_final_apply_stack
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
        self.assertEqual(6,report["apply_damage_instruction_index"])
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


EVENT_TARGET="Method net/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post.getEntity:()Lnet/minecraft/world/entity/LivingEntity;"
HOLDER="Method net/neoforged/neoforge/registries/DeferredHolder.get:()Ljava/lang/Object;"
SOURCE_GETTER="Method com/somake/somakespells/spells/blood/BloodCutSpell.getDamageSource:(Lnet/minecraft/world/entity/Entity;)Lio/redspace/ironsspellbooks/damage/SpellDamageSource;"
CAST="class com/somake/somakespells/spells/blood/BloodCutSpell"

def final_fixture():
    # Two synthetic predecessor instructions, then final 11-op typed stack handoff.
    ops=[
      ("fstore_3","",""),
      ("nop","",""),
      ("aload_0","",""),
      ("invokevirtual","",EVENT_TARGET),
      ("fload_3","",""),
      ("getstatic","","Field com/somake/somakespells/registries/ModSpells.BLOOD_CUT:Lnet/neoforged/neoforge/registries/DeferredHolder;"),
      ("invokevirtual","",HOLDER),
      ("checkcast","#9",CAST),
      ("aload_1","",""),
      ("invokevirtual","",SOURCE_GETTER),
      ("invokestatic","",APPLY),
      ("pop","",""),
      ("return","",""),
    ]
    return [(3*i,o,a,c) for i,(o,a,c) in enumerate(ops)]

class FinalStackHandoffTests(unittest.TestCase):
    def test_actual_target_float_source_order(self):
        d=certify_final_apply_stack(final_fixture())
        self.assertEqual("EXACT_TYPED_APPLY_HANDOFF",d["assurance"])
        self.assertEqual("event.getEntity()",d["target_argument"])
        self.assertEqual("local_3",d["float_amount_argument"])
        self.assertEqual("BloodCutSpell.getDamageSource(local_1)",d["source_argument"])
        self.assertEqual("ONE_ENTITY_ARGUMENT",d["source_factory_overload"])

    def test_blood_cut_source_overload_with_two_entities_rejected(self):
        rows=final_fixture()
        rows[9]=(27,"invokevirtual","",SOURCE_GETTER.replace("(Lnet/minecraft/world/entity/Entity;)", "(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/entity/Entity;)"))
        with self.assertRaises(GateError):certify_final_apply_stack(rows)

    def test_wrong_target_getter_rejected(self):
        rows=final_fixture()
        rows[3]=(9,"invokevirtual","","Method example.getEntity:()Ljava/lang/Object;")
        with self.assertRaises(GateError):certify_final_apply_stack(rows)

    def test_wrong_source_local_rejected(self):
        rows=final_fixture();rows[8]=(24,"aload_2","","")
        with self.assertRaises(GateError):certify_final_apply_stack(rows)

    def test_wrong_final_float_rejected(self):
        rows=final_fixture();rows[4]=(12,"fconst_1","","")
        with self.assertRaises(GateError):certify_final_apply_stack(rows)

    def test_guard_may_branch_directly_to_terminal_return(self):
        rows=final_fixture();rows[1]=(3,"ifeq","36","")
        result=certify_final_apply_stack(rows)
        self.assertEqual("EXACT_TYPED_APPLY_HANDOFF",result["assurance"])

    def test_guard_must_not_enter_float_argument_construction(self):
        rows=final_fixture();rows[1]=(3,"ifeq","12","")
        with self.assertRaises(GateError):certify_final_apply_stack(rows)

    def test_return_value_must_be_discarded(self):
        rows=final_fixture();rows[11]=(33,"nop","","")
        with self.assertRaises(GateError):certify_final_apply_stack(rows)

if __name__=="__main__":
    unittest.main()
