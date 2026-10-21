#!/usr/bin/env python3
"""Synthetic JVM method-reference regression: no publisher bytecode fixtures."""
import unittest

from somake_109_perk_method_probe import GateError
from somake_109_blood_cut_event_args import examine_event_callsite, certify_native_damage_expression, certify_native_source_actor, certify_effect_holder_receiver, certify_early_post_damage_exclusion

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



EFFECT_FIELD="Field com/somake/somakespells/registries/ModMobEffects.BLOOD_CUT:Lnet/neoforged/neoforge/registries/DeferredHolder;"
EFFECT_GETTER="Method net/minecraft/world/entity/LivingEntity.getEffect:(Lnet/minecraft/core/Holder;)Lnet/minecraft/world/effect/MobEffectInstance;"

def holder_fixture():
    return [
      (0,"aload_1","",""),
      (1,"getstatic","",EFFECT_FIELD),
      (4,"invokevirtual","",EFFECT_GETTER),
      (7,"astore_2","",""),
      (8,"aload_2","",""),
      (9,"ifnull","30",""),
      (12,"aload_0","",""),
      (13,"invokevirtual","",NEW_DAMAGE),
      (16,"aload_2","",""),
      (17,"invokevirtual","",AMP),
      (20,"nop","",""),
      (21,"nop","",""),
      (30,"return","","")
    ]


class EffectOwnerTests(unittest.TestCase):
    def test_blood_cut_effect_loaded_from_source_actor(self):
        got=certify_effect_holder_receiver(holder_fixture())
        self.assertEqual("BLOOD_CUT_FROM_SOURCE_ENTITY",got["assurance"])
        self.assertEqual("local_1",got["effect_receiver_local"])
        self.assertEqual("local_2",got["effect_storage_local"])

    def test_changed_effect_owner_fails(self):
        rows=holder_fixture();rows[0]=(0,"aload_0","","")
        with self.assertRaises(GateError):certify_effect_holder_receiver(rows)

    def test_wrong_mob_effect_fails(self):
        rows=holder_fixture();rows[1]=(1,"getstatic","",EFFECT_FIELD.replace("BLOOD_CUT","POISON"))
        with self.assertRaises(GateError):certify_effect_holder_receiver(rows)

    def test_unprotected_effect_instance_fails(self):
        rows=holder_fixture();rows[5]=(9,"nop","","")
        with self.assertRaises(GateError):certify_effect_holder_receiver(rows)



def early_exclusion_fixture():
    return [(i,"nop","","") for i in range(10)] + [
      (10,"aload_0","",""),
      (11,"invokevirtual","","Method net/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post.getSource:()Lnet/minecraft/world/damagesource/DamageSource;"),
      (12,"instanceof","#45","class io/redspace/ironsspellbooks/damage/SpellDamageSource"),
      (13,"ifeq","15",""),
      (14,"return","",""),
      (15,"nop","",""),
    ]

class EventEarlyTypeGuardTests(unittest.TestCase):
    def test_if_instanceof_true_returns_before_handler(self):
        v=certify_early_post_damage_exclusion(early_exclusion_fixture())
        self.assertEqual("EXACT_EARLY_INSTANCEOF_RETURN_BRANCH",v["assurance"])
        self.assertEqual("io/redspace/ironsspellbooks/damage/SpellDamageSource",v["excluded_class_internal_name"])

    def test_changed_excluded_class_must_fail_closed(self):
        rows=early_exclusion_fixture()
        rows[12]=(12,"instanceof","#45",
                  "class net/minecraft/world/damagesource/DamageSource")
        with self.assertRaises(GateError):
            certify_early_post_damage_exclusion(rows)

    def test_changed_branch_target_rejected(self):
        rows=early_exclusion_fixture();rows[13]=(13,"ifeq","14","")
        with self.assertRaises(GateError):certify_early_post_damage_exclusion(rows)

    def test_missing_source_getter_rejected(self):
        rows=early_exclusion_fixture();rows[11]=(11,"invokevirtual","","Method other.getEntity:()Ljava/lang/Object;")
        with self.assertRaises(GateError):certify_early_post_damage_exclusion(rows)


if __name__=="__main__":
    unittest.main()
