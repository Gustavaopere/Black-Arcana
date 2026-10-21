#!/usr/bin/env python3
"""Synthetic own fixtures for typed metadata; fail closed for descriptor drift."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_bud_operand_provenance import classify_comment, describe_instruction, scout, operand_contract, certify_exact_bud_operand_contract_109
D="(Lnet/minecraft/server/level/ServerLevel;)V"
def fixture():
    ops=[f"{i}: nop" for i in range(279)]
    ops[34]="34: aload 4"
    ops[89]="89: getfield #12 // Field witherDuration:I"
    ops[120]="120: aload 8"
    ops[125]="125: getfield #13 // Field witherDuration:I"
    ops[131]='131: invokespecial #19 // Method net/minecraft/world/effect/MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;IIZZZ)V'
    ops[136]="136: ldc2_w #20 // double 0.42d"
    ops[138]="138: invokevirtual #21 // Method net/minecraft/world/entity/Entity.push:(DDD)V"
    ops[146]="146: aload 4"
    ops[148]="148: iload 6"
    ops[159]="159: iinc 6, 1"
    ops[168]="168: invokeinterface #32, 2 // InterfaceMethod net/neoforged/bus/api/IEventBus.post:(Lnet/neoforged/bus/api/Event;)Lnet/neoforged/bus/api/Event;"
    return [("impact",D,ops)]
class ScoutTests(unittest.TestCase):
    def test_scoped_windows_and_types_are_observations_only(self):
        proof=scout(fixture())
        self.assertEqual("OBSERVED_TYPED_OPERAND_WINDOWS_ONLY",proof["status"],proof)
        self.assertEqual(279,proof["instruction_count"])
        self.assertEqual(6,len(proof["ranges"]))
        self.assertIn("NOT_PROVED",proof["boundary"])
    def test_local_and_call_metadata(self):
        x=describe_instruction(__import__("somake_109_radius_irons_contract",fromlist=["opcode_rows"]).opcode_rows(fixture()[0][2]),146)
        self.assertEqual(4,x["slot"])
        self.assertEqual("call",classify_comment("invokevirtual",
            "Method net/minecraft/world/entity/Entity.push:(DDD)V")["kind"])
    def test_wrong_signature_fails_closed(self):
        self.assertEqual("NOT_PROVED",scout([("impact","()V",fixture()[0][2])])["status"])
    def test_ambiguous_member_fails_closed(self):
        self.assertEqual("NOT_PROVED",scout(fixture()*2)["status"])
    def test_missing_instruction_fails_closed(self):
        x=fixture();x[0][2].pop()
        self.assertEqual("NOT_PROVED",scout(x)["status"])
    def test_no_copy_of_jvm_comments(self):
        p=scout(fixture())
        self.assertNotIn("raw_code",str(p))
        self.assertNotIn("vendor_method_body",str(p))

def exact_contract_fixture():
    data=fixture()
    r=data[0][2]
    updates={
       3:"aload_0",
       4:"invokevirtual #3 // Method getOwner:()Lnet/minecraft/world/entity/Entity;",
       5:"astore_3",6:"aload_3",
       7:"instanceof #4 // class net/minecraft/world/entity/LivingEntity",
       8:"ifeq 14",9:"aload_3",
       10:"checkcast #4 // class net/minecraft/world/entity/LivingEntity",
       11:"astore 5",12:"aload 5",13:"goto 15",14:"aconst_null",15:"astore 4",
       26:"iconst_0",27:"istore 6",
       101:"aload 8",
       102:"getstatic #7 // Field net/minecraft/world/effect/MobEffects.WITHER:Lnet/minecraft/core/Holder;",
       103:"invokevirtual #8 // Method net/minecraft/world/entity/LivingEntity.hasEffect:(Lnet/minecraft/core/Holder;)Z",
       104:"istore 14",
       118:"invokestatic #9 // Method io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:(Lnet/minecraft/world/entity/Entity;FLnet/minecraft/world/damagesource/DamageSource;)Z",
       119:"ifeq 145",
       123:"getstatic #7 // Field net/minecraft/world/effect/MobEffects.WITHER:Lnet/minecraft/core/Holder;",
       124:"aload_0",125:"getfield #10 // Field witherDuration:I",
       126:"aload_0",127:"getfield #11 // Field witherAmplifier:I",
       128:"iconst_0",129:"iconst_1",130:"iconst_1",
       131:'invokespecial #12 // Method net/minecraft/world/effect/MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;IIZZZ)V',
       132:"invokevirtual #13 // Method net/minecraft/world/entity/LivingEntity.addEffect:(Lnet/minecraft/world/effect/MobEffectInstance;)Z",
       134:"aload 8",135:"dconst_0",136:"ldc2_w #14 // double 0.34d",137:"dconst_0",
       138:"invokevirtual #15 // Method net/minecraft/world/entity/Entity.push:(DDD)V",
       139:"aload 8",140:"iconst_1",141:"putfield #16 // Field net/minecraft/world/entity/Entity.hurtMarked:Z",
       142:"iload 14",143:"ifeq 145",144:"iinc 6, 1",
       146:"aload 4",147:"ifnull 173",148:"iload 6",149:"ifle 173",
       150:"ldc_w #17 // float 3.75f",151:"ldc_w #18 // float 1.25f",
       152:"iload 6",153:"i2f",154:"fmul",
       155:"invokestatic #19 // Method java/lang/Math.min:(FF)F",
       156:"fstore 7",170:"aload 4",171:"fload 7",
       172:"invokevirtual #20 // Method net/minecraft/world/entity/LivingEntity.heal:(F)V",
    }
    for i,val in updates.items():
        r[i]=f"{i}: {val}"
    return data

class ExactNativeOperandTests(unittest.TestCase):
    def test_owner_preexisting_wither_and_capped_heal_physical_shape(self):
        p=operand_contract(exact_contract_fixture())
        self.assertEqual("PROVED_BUD_OWNER_PREEXISTING_WITHER_COUNTER_AND_CAPPED_HEAL_INPUT",p["status"],p)
        self.assertEqual("bud.getOwner():Entity",p["owner_source"])
        self.assertEqual("applyDamage_true_AND_victim_had_WITHER_before_damage",p["counter_condition"])
        self.assertEqual([0,0.34,0],p["push_vector_xyz"])
        self.assertEqual("min_f32(3.75f,1.25f*float32(counter_local6))",p["heal_formula"])
        certify_exact_bud_operand_contract_109(p)
    def test_owner_guard_type_drift_fails(self):
        f=exact_contract_fixture()
        f[0][2][7]="7: instanceof #4 // class net/minecraft/world/entity/Player"
        self.assertEqual("NOT_PROVED",operand_contract(f)["status"])
    def test_unlicensed_branch_into_count_increment_fails_closed(self):
        f=exact_contract_fixture()
        f[0][2][207]="207: goto 144"
        self.assertEqual("NOT_PROVED",operand_contract(f)["status"])
    def test_wrong_existing_wither_receiver_fails_closed(self):
        f=exact_contract_fixture()
        f[0][2][101]="101: aload 3"
        self.assertEqual("NOT_PROVED",operand_contract(f)["status"])
    def test_wrong_wither_counter_provenance_fails(self):
        f=exact_contract_fixture()
        f[0][2][142]="142: iload 6"
        self.assertEqual("NOT_PROVED",operand_contract(f)["status"])
    def test_wrong_push_vector_fails(self):
        f=exact_contract_fixture()
        f[0][2][136]="136: ldc2_w #14 // double 0.44d"
        self.assertEqual("NOT_PROVED",operand_contract(f)["status"])
    def test_changed_wither_parameters_fails(self):
        f=exact_contract_fixture()
        f[0][2][125]="125: getfield #10 // Field otherDuration:I"
        self.assertEqual("NOT_PROVED",operand_contract(f)["status"])
    def test_wrong_healing_multiplier_fails(self):
        f=exact_contract_fixture()
        f[0][2][151]="151: ldc_w #18 // float 1.75f"
        self.assertEqual("NOT_PROVED",operand_contract(f)["status"])
    def test_method_shape_ambiguous_fails(self):
        self.assertEqual("NOT_PROVED",operand_contract(exact_contract_fixture()*2)["status"])
    def test_physical_release_gate_fails_on_invented_perk_approval(self):
        p=operand_contract(exact_contract_fixture())
        with self.assertRaises(GateError):
            certify_exact_bud_operand_contract_109(dict(p,boundary="per_player_mutator_available"))
        with self.assertRaises(GateError):
            certify_exact_bud_operand_contract_109(None)

if __name__=="__main__":
    unittest.main()
