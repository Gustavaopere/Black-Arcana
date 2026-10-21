#!/usr/bin/env python3
"""Synthetic JVM method-reference regression: no publisher bytecode fixtures."""
import unittest

from somake_109_perk_method_probe import GateError
from somake_109_blood_cut_event_args import examine_event_callsite

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

if __name__=="__main__":
    unittest.main()
