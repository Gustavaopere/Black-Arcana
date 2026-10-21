#!/usr/bin/env python3
"""Original synthetic regression tests for Somake 1.0.9 bud damage path."""
import unittest
from somake_109_bud_impact_damage_gates import impact_damage_branch_scout, certify_damage_success_effect_path, certify_exact_damage_effect_gate_109, certify_heal_guard_and_event_path, certify_exact_heal_event_gate_109
from somake_109_perk_method_probe import GateError
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

def gated_fixture():
    f=fixture()
    rows=f[0][2]
    rows[131]='131: invokespecial #7 // Method net/minecraft/world/effect/MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;IIZZZ)V'
    rows[133]="133: pop"
    rows[144]="144: iinc 6, 1"
    return f
class DamageBooleanCausalTests(unittest.TestCase):
    def test_boolean_damage_false_skips_wither_and_push_true_reaches_calls(self):
        proof=certify_damage_success_effect_path(gated_fixture())
        self.assertEqual("PROVED_WAVE_BUD_DAMAGE_TRUE_PATH_REACHES_WITHER_AND_PUSH_CALLS",proof["status"],proof)
        self.assertEqual(119,proof["damage_false_branch_index"])
        self.assertEqual(145,proof["damage_false_branch_target_index"])
        self.assertEqual(123,proof["wither_field_index"])
        self.assertEqual(132,proof["add_effect_index"])
        self.assertEqual(138,proof["push_index"])
        self.assertFalse(proof["effect_region_has_external_ingress"])
        certify_exact_damage_effect_gate_109(proof)
    def test_wrong_damage_return_type_fails(self):
        f=gated_fixture()
        f[0][2][118]=f[0][2][118].replace(")Z",")V")
        self.assertEqual("NOT_PROVED",certify_damage_success_effect_path(f)["status"])
    def test_wrong_wither_field_fails(self):
        f=gated_fixture()
        f[0][2][123]=f[0][2][123].replace("WITHER","POISON")
        self.assertEqual("NOT_PROVED",certify_damage_success_effect_path(f)["status"])
    def test_external_jump_into_effect_fails(self):
        f=gated_fixture();f[0][2][50]="50: goto 125"
        self.assertEqual("NOT_PROVED",certify_damage_success_effect_path(f)["status"])
    def test_internal_exit_skips_effect_fails(self):
        f=gated_fixture();f[0][2][126]="126: goto 145"
        self.assertEqual("NOT_PROVED",certify_damage_success_effect_path(f)["status"])
    def test_return_of_add_effect_not_discarded_fails(self):
        f=gated_fixture();f[0][2][133]="133: nop"
        self.assertEqual("NOT_PROVED",certify_damage_success_effect_path(f)["status"])
    def test_modified_post_effect_branch_fails(self):
        f=gated_fixture();f[0][2][143]="143: ifne 145"
        self.assertEqual("NOT_PROVED",certify_damage_success_effect_path(f)["status"])
    def test_mutated_release_snapshot_fails_closed(self):
        p=certify_damage_success_effect_path(gated_fixture())
        for delta in ({"damage_false_branch_index":120},
                      {"effect_region_has_external_ingress":True},
                      {"push_index":139},
                      {"boundary":"approved_per_player_damage_setter"},
                      {"status":"NOT_PROVED"}):
            with self.subTest(delta=delta):
                with self.assertRaises(GateError):
                    certify_exact_damage_effect_gate_109(dict(p,**delta))
        with self.assertRaises(GateError):
            certify_exact_damage_effect_gate_109(None)


def healing_fixture():
    rows=gated_fixture()[0][2]
    rows[146]="146: aload 4"
    rows[147]="147: ifnull 173"
    rows[148]="148: iload 6"
    rows[149]="149: ifle 173"
    rows[168]="168: invokeinterface #10, 2 // InterfaceMethod net/neoforged/bus/api/IEventBus.post:(Lnet/neoforged/bus/api/Event;)Lnet/neoforged/bus/api/Event;"
    rows[169]="169: pop"
    rows[170]="170: aload 4"
    rows[171]="171: fload 7"
    return [("impact",D,rows)]

class HealingGuardsTests(unittest.TestCase):
    def test_nonnull_and_positive_counter_guard_post_then_heal(self):
        p=certify_heal_guard_and_event_path(healing_fixture())
        self.assertEqual("PROVED_BUD_HEAL_GUARDED_EVENT_POST_THEN_HEAL_CALL",p["status"],p)
        self.assertEqual((4,6,7),(p["nullable_receiver_slot"],p["positive_integer_slot"],p["heal_amount_float_slot"]))
        self.assertEqual([167,168,172],[p["event_constructor_index"],p["event_post_index"],p["heal_call_index"]])
        self.assertTrue(p["event_post_return_discarded"])
        certify_exact_heal_event_gate_109(p)
    def test_heal_nonnull_operand_changed_fails(self):
        p=healing_fixture();p[0][2][146]="146: aload 3"
        self.assertEqual("NOT_PROVED",certify_heal_guard_and_event_path(p)["status"])
    def test_positive_counter_changed_fails(self):
        p=healing_fixture();p[0][2][148]="148: iload 7"
        self.assertEqual("NOT_PROVED",certify_heal_guard_and_event_path(p)["status"])
    def test_event_return_not_dropped_fails(self):
        p=healing_fixture();p[0][2][169]="169: nop"
        self.assertEqual("NOT_PROVED",certify_heal_guard_and_event_path(p)["status"])
    def test_heal_amount_and_target_mismatch_fails(self):
        p=healing_fixture();p[0][2][171]="171: fload 8"
        self.assertEqual("NOT_PROVED",certify_heal_guard_and_event_path(p)["status"])
    def test_external_jump_into_heal_block_fails(self):
        p=healing_fixture();p[0][2][80]="80: goto 165"
        self.assertEqual("NOT_PROVED",certify_heal_guard_and_event_path(p)["status"])
    def test_guard_drift_or_inverted_conditional_fails(self):
        p=healing_fixture();p[0][2][149]="149: ifgt 173"
        self.assertEqual("NOT_PROVED",certify_heal_guard_and_event_path(p)["status"])
    def test_release_gate_rejects_perk_claim_and_changed_provenance(self):
        p=certify_heal_guard_and_event_path(healing_fixture())
        for change in ({"heal_receiver_slot":3},{"event_post_return_discarded":False},
                       {"boundary":"approved_second_heal_on_event"},{"status":"NOT_PROVED"}):
            with self.subTest(change=change):
                with self.assertRaises(GateError):
                    certify_exact_heal_event_gate_109(dict(p,**change))
        with self.assertRaises(GateError):
            certify_exact_heal_event_gate_109(None)

if __name__=="__main__":
    unittest.main()
