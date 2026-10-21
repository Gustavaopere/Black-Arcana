#!/usr/bin/env python3
"""Synthetic JVM method-reference regression: no publisher bytecode fixtures."""
import unittest

from somake_109_perk_method_probe import GateError
from somake_109_blood_cut_event_args import examine_event_callsite, certify_native_damage_expression, certify_native_source_actor

AMP="Method net/minecraft/world/effect/MobEffectInstance.getAmplifier:()I"
SOURCE="Method net/minecraft/world/damagesource/DamageSource.getEntity:()Lnet/minecraft/world/entity/Entity;"
MOD="Method com/somake/somakespells/effect/blood/BloodCutEffect.getDamageModifier:(ILnet/minecraft/world/entity/LivingEntity;)F"
DAMAGE="Method io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:(Lnet/minecraft/world/entity/Entity;FLnet/minecraft/world/damagesource/DamageSource;)Z"

def example():
    return [
        (0,"aload_2","",""),
        (1,"invokevirtual","",SOURCE),
        (4,"astore_3","",""),
        (5,"aload","4",""),
        (7,"invokevirtual","",AMP),
        (10,"aload_3","",""),
        (11,"checkcast","#12","class net/minecraft/world/entity/LivingEntity"),
        (14,"invokestatic","",MOD),
        (17,"fstore","5",""),
        (19,"invokestatic","",DAMAGE),
        (22,"return","","")
    ]

class EventArgumentTests(unittest.TestCase):
    def test_exact_typed_callsite_evidence(self):
        report=examine_event_callsite(example())
        self.assertEqual(1,report["modifier_calls"])
        self.assertEqual(1,report["amplifier_reads"])
        self.assertEqual(1,report["source_entity_reads"])
        self.assertEqual(7,report["modifier_call_index"])
        self.assertEqual("STATIC_CALLSITES_ONLY",report["assurance"])

    def test_changed_modifier_descriptor_fails_closed(self):
        rows=example()
        rows[7]=(14,"invokestatic","",MOD.replace("(I","(F"))
        with self.assertRaises(GateError):examine_event_callsite(rows)

    def test_duplicate_modifier_fails_closed(self):
        rows=example();rows.insert(9,(18,"invokestatic","",MOD))
        with self.assertRaises(GateError):examine_event_callsite(rows)

    def test_missing_amplifier_fails_closed(self):
        rows=example();rows[4]=(7,"invokevirtual","","Method example.getLevel:()I")
        with self.assertRaises(GateError):examine_event_callsite(rows)

    def test_unordered_instruction_offsets_fails_closed(self):
        rows=example();rows[6]=(5,"checkcast","#12","class net/minecraft/world/entity/LivingEntity")
        with self.assertRaises(GateError):examine_event_callsite(rows)


NEW_DAMAGE="Method net/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post.getNewDamage:()F"

def native_float_handoff():
    return [
        (0,"aload_0","",""),
        (1,"invokevirtual","",NEW_DAMAGE),
        (4,"aload_2","",""),
        (5,"invokevirtual","",AMP),
        (8,"aload_1","",""),
        (9,"invokestatic","",MOD),
        (12,"fmul","",""),
        (13,"fstore_3","",""),
        (14,"return","","")
    ]


class FloatDamageStackTests(unittest.TestCase):
    def test_exact_new_damage_times_amplifier_modifier(self):
        result=certify_native_damage_expression(native_float_handoff())
        self.assertEqual("DIRECT_TYPED_FLOAT_HANDOFF",result["assurance"])
        self.assertEqual("event.getNewDamage * getDamageModifier(effect.getAmplifier,local_1)",result["return_expression"])
        self.assertEqual("fstore_3",result["result_store_opcode"])

    def test_wrong_float_operator_rejected(self):
        rows=native_float_handoff();rows[6]=(12,"fadd","","")
        with self.assertRaises(GateError):certify_native_damage_expression(rows)

    def test_wrong_amplifier_load_rejected(self):
        rows=native_float_handoff();rows[2]=(4,"aload_0","","")
        with self.assertRaises(GateError):certify_native_damage_expression(rows)

    def test_inserted_cast_transform_rejected(self):
        rows=native_float_handoff();rows.insert(6,(11,"fneg","",""))
        with self.assertRaises(GateError):certify_native_damage_expression(rows)



SOURCE_EVENT="Method net/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post.getSource:()Lnet/minecraft/world/damagesource/DamageSource;"
TYPE="class net/minecraft/world/entity/LivingEntity"

def source_fixture():
    return [
      (0,"aload_0","",""),
      (1,"invokevirtual","",SOURCE_EVENT),
      (4,"invokevirtual","",SOURCE),
      (7,"astore_2","",""),
      (8,"aload_2","",""),
      (9,"instanceof","#12",TYPE),
      (12,"ifeq","30",""),
      (15,"aload_2","",""),
      (16,"checkcast","#12",TYPE),
      (19,"astore_1","",""),
      (30,"return","","")
    ]


class SourceActorTests(unittest.TestCase):
    def test_guarded_source_entity_becomes_local_1(self):
        result=certify_native_source_actor(source_fixture())
        self.assertEqual("SOURCE_ENTITY_TYPED_LOCAL1",result["assurance"])
        self.assertEqual("event.getSource().getEntity()",result["origin"])
        self.assertEqual("LivingEntity",result["verified_cast_type"])

    def test_wrong_event_source_rejected(self):
        rows=source_fixture();rows[1]=(1,"invokevirtual","","Method example.getSource:()Ljava/lang/String;")
        with self.assertRaises(GateError):certify_native_source_actor(rows)

    def test_wrong_actor_guard_rejected(self):
        rows=source_fixture();rows[5]=(9,"instanceof","#12","class net/minecraft/world/entity/player/Player")
        with self.assertRaises(GateError):certify_native_source_actor(rows)

    def test_mutated_local_store_rejected(self):
        rows=source_fixture();rows[9]=(19,"astore_3","","")
        with self.assertRaises(GateError):certify_native_source_actor(rows)

    def test_wrong_exit_target_rejected(self):
        rows=source_fixture();rows[6]=(12,"ifeq","19","")
        with self.assertRaises(GateError):certify_native_source_actor(rows)


if __name__=="__main__":
    unittest.main()
