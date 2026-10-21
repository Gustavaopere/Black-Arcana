#!/usr/bin/env python3
"""Original synthetic regression tests for Somake 1.0.9 bud damage path."""
import unittest
from somake_109_bud_impact_damage_gates import impact_damage_branch_scout
D="(Lnet/minecraft/server/level/ServerLevel;)V"
def fixture():
    rows=[f"{i}: nop" for i in range(279)]
    rows[118]="118: invokestatic #1 // Method io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:(Lnet/minecraft/world/entity/Entity;)Z"
    rows[119]="119: ifeq 145"
    rows[123]="123: getstatic #2 // Field net/minecraft/world/effect/MobEffects.WITHER:Lnet/minecraft/core/Holder;"
    rows[132]="132: invokevirtual #3 // Method net/minecraft/world/entity/LivingEntity.addEffect:(Lnet/minecraft/world/effect/MobEffectInstance;)Z"
    rows[138]="138: invokevirtual #4 // Method net/minecraft/world/entity/Entity.push:(DDD)V"
    rows[143]="143: ifeq 145"
    rows[145]="145: goto 34"
    rows[167]='167: invokespecial #5 // Method io/redspace/ironsspellbooks/api/events/SpellHealEvent."<init>":()V'
    rows[172]="172: invokevirtual #6 // Method net/minecraft/world/entity/LivingEntity.heal:(F)V"
    return [("impact",D,rows)]
class ImpactDamageScoutTests(unittest.TestCase):
    def test_damage_gate_and_calls_are_structural_only(self):
        r=impact_damage_branch_scout(fixture())
        self.assertEqual("OBSERVED_DAMAGE_RETURN_GATE_AND_EFFECT_CALL_SITES",r["status"],r)
        self.assertEqual([118],r["damage_call_indices"])
        self.assertEqual(145,r["damage_branch_target"])
        self.assertEqual([132],r["status_call_indices"])
        self.assertEqual([138],r["push_call_indices"])
        self.assertIn("no targets",r["boundary"])
    def test_wrong_branch_target_fails_closed(self):
        r=fixture();r[0][2][119]="119: ifeq 140"
        self.assertEqual("NOT_PROVED",impact_damage_branch_scout(r)["status"])
    def test_wrong_damage_index_fails_closed(self):
        r=fixture();r[0][2][118]="118: nop"
        self.assertEqual("NOT_PROVED",impact_damage_branch_scout(r)["status"])
    def test_wrong_status_call_fails_closed(self):
        r=fixture();r[0][2][132]="132: nop"
        self.assertEqual("NOT_PROVED",impact_damage_branch_scout(r)["status"])
    def test_duplicate_exact_method_fails_closed(self):
        self.assertEqual("NOT_PROVED",impact_damage_branch_scout(fixture()*2)["status"])
    def test_descriptor_mismatch_fails_closed(self):
        self.assertEqual("NOT_PROVED",impact_damage_branch_scout([("impact","()V",fixture()[0][2])])["status"])
if __name__=="__main__":
    unittest.main()
