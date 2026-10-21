#!/usr/bin/env python3
"""Synthetic branch-dependent numeric JVM return tests with no provider code."""
import unittest
from somake_109_blood_cut_modifier_flow import symbolic_modifier, certify_native_modifier_formula
from somake_109_perk_method_probe import GateError

def fixture():
    return [
      (0,"aload_1","",""),(1,"ifnonnull","4",""),
      (2,"fconst_1","",""),(3,"goto","10",""),
      (4,"getstatic","","Field com/somake/somakespells/registries/ModSpells.BLOOD_CUT:Lnet/neoforged/neoforge/registries/DeferredHolder;"),
      (5,"invokevirtual","","Method net/neoforged/neoforge/registries/DeferredHolder.get:()Ljava/lang/Object;"),
      (6,"checkcast","17","class com/somake/somakespells/spells/blood/BloodCutSpell"),
      (7,"aload_1","",""),
      (8,"invokevirtual","","Method com/somake/somakespells/spells/blood/BloodCutSpell.getEntityPowerMultiplier:(Lnet/minecraft/world/entity/LivingEntity;)F"),
      (9,"nop","",""),
      (10,"iload_0","",""),(11,"iconst_1","",""),(12,"iadd","",""),
      (13,"i2f","",""),(14,"fmul","",""),
      (15,"ldc","#10","float 0.1f"),(16,"fmul","",""),
      (17,"freturn","",""),(18,"nop","","")
    ]

# Move the spare test-only row into a reachable neutral position.
def valid():
    rows=fixture()
    rows[17]=(17,"nop","","")
    rows[18]=(18,"freturn","","")
    return rows

def exact_operand_order_fixture():
    """Cast factor ordering independent of native implementation details."""
    return [
      (0,"iload_0","",""),(1,"iconst_1","",""),(2,"iadd","",""),
      (3,"i2f","",""),(4,"aload_1","",""),(5,"ifnonnull","9",""),
      (6,"fconst_1","",""),(7,"goto","14",""),(8,"nop","",""),
      (9,"getstatic","","Field com/somake/somakespells/registries/ModSpells.BLOOD_CUT:Lnet/neoforged/neoforge/registries/DeferredHolder;"),
      (10,"invokevirtual","","Method net/neoforged/neoforge/registries/DeferredHolder.get:()Ljava/lang/Object;"),
      (11,"checkcast","17","class com/somake/somakespells/spells/blood/BloodCutSpell"),
      (12,"aload_1","",""),
      (13,"invokevirtual","","Method com/somake/somakespells/spells/blood/BloodCutSpell.getEntityPowerMultiplier:(Lnet/minecraft/world/entity/LivingEntity;)F"),
      (14,"fmul","",""),(15,"ldc","#10","float 0.1f"),
      (16,"fmul","",""),(17,"nop","",""),(18,"freturn","","")
    ]


class SymbolicTests(unittest.TestCase):
    def test_two_nullable_paths_and_float_expression(self):
        result=symbolic_modifier(valid())
        self.assertEqual(["arg1 != null","arg1 == null"],[x["guard"] for x in result])
        nonnull=next(x["expression"] for x in result if x["guard"]=="arg1 != null")
        null=next(x["expression"] for x in result if x["guard"]=="arg1 == null")
        self.assertIn("entity_power_multiplier",str(nonnull))
        self.assertNotIn("entity_power_multiplier",str(null))
        self.assertIn("0.1",str(nonnull))
        self.assertIn("iadd",str(null))

    def test_float_local_merge_tracks_each_guard(self):
        rows=[
            (0,"aload_1","",""),(1,"ifnonnull","5",""),
            (2,"fconst_1","",""),(3,"fstore_2","",""),(4,"goto","10",""),
            (5,"getstatic","","Field com/somake/somakespells/registries/ModSpells.BLOOD_CUT:Lnet/neoforged/neoforge/registries/DeferredHolder;"),
            (6,"invokevirtual","","Method net/neoforged/neoforge/registries/DeferredHolder.get:()Ljava/lang/Object;"),
            (7,"aload_1","",""),
            (8,"invokevirtual","","Method com/somake/somakespells/spells/blood/BloodCutSpell.getEntityPowerMultiplier:(Lnet/minecraft/world/entity/LivingEntity;)F"),
            (9,"fstore_2","",""),(10,"fload_2","",""),
            (11,"iload_0","",""),(12,"iconst_1","",""),(13,"iadd","",""),
            (14,"i2f","",""),(15,"fmul","",""),
            (16,"ldc","#10","float 0.1f"),(17,"fmul","",""),(18,"freturn","","")
        ]
        result=symbolic_modifier(rows)
        self.assertEqual(2,len(result))
        left=next(x for x in result if x["guard"]=="arg1 == null")
        right=next(x for x in result if x["guard"]=="arg1 != null")
        self.assertIn("entity_power_multiplier",str(right))
        self.assertNotIn("entity_power_multiplier",str(left))

    def test_exact_native_float_expression_certificate(self):
        result=symbolic_modifier(exact_operand_order_fixture())
        cert=certify_native_modifier_formula(result)
        self.assertEqual("SHA_EXACT_TWO_ROUTE_FLOAT_EXPRESSION",cert["verified"])
        self.assertEqual(0.1,cert["float_coefficient"])

    def test_coefficient_mutation_rejected_by_exact_certificate(self):
        rows=exact_operand_order_fixture(); rows[15]=(15,"ldc","#10","float 0.2f")
        result=symbolic_modifier(rows)
        with self.assertRaises(GateError):certify_native_modifier_formula(result)

    def test_branch_return_mutation_rejected_by_exact_certificate(self):
        rows=exact_operand_order_fixture();rows[6]=(6,"fconst_2","","")
        result=symbolic_modifier(rows)
        with self.assertRaises(GateError):certify_native_modifier_formula(result)

    def test_unknown_opcode_rejected(self):
        rows=valid();rows[9]=(9,"unknownop","","")
        with self.assertRaises(GateError):symbolic_modifier(rows)

    def test_wrong_nonnull_source_rejected(self):
        rows=valid();rows[0]=(0,"aload_0","","")
        with self.assertRaises(GateError):symbolic_modifier(rows)

    def test_unrecognized_constant_rejected(self):
        rows=valid();rows[15]=(15,"ldc","#10","String not_numeric")
        with self.assertRaises(GateError):symbolic_modifier(rows)

    def test_numeric_branch_wrong_destination_rejected(self):
        rows=valid();rows[3]=(3,"goto","777","")
        with self.assertRaises(GateError):symbolic_modifier(rows)

    def test_nonnull_guard_drift_rejected(self):
        rows=valid();rows[1]=(1,"ifeq","4","")
        with self.assertRaises(GateError):symbolic_modifier(rows)

if __name__=="__main__":unittest.main()
