"""Synthetic regressions for exact-JAR numerical ABI footprint audit."""
import tempfile
import unittest
from pathlib import Path
from alshanex_403_megido_numeric_footprint import inspect, audit

DAMAGE = """
  public float getDamage(int, net.minecraft.world.entity.LivingEntity);
    descriptor: (ILnet/minecraft/world/entity/LivingEntity;)F
    Code:
       0: iload_1
       1: i2f
       2: aload_2
       3: invokevirtual #27 // Method net/minecraft/world/entity/LivingEntity.getHealth:()F
       6: fmul
       7: freturn
"""
CONNECT = """
  public int getMaxConnections(int, net.minecraft.world.entity.LivingEntity);
    descriptor: (ILnet/minecraft/world/entity/LivingEntity;)I
    Code:
       0: iload_1
       1: iconst_2
       2: iadd
       3: ireturn
"""
class TestFootprints(unittest.TestCase):
    def test_arithmetic_and_external_method_group(self):
        result = inspect("public class X {\n" + DAMAGE + CONNECT + "}\n")
        d=result["getDamage"]
        self.assertEqual(d["float_arithmetic_op_count"],1)
        self.assertEqual(d["primitive_conversion_op_count"],1)
        self.assertEqual(d["level_parameter_local_load_op_count"],1)
        self.assertEqual(d["caster_parameter_local_load_op_count"],1)
        self.assertEqual(d["direct_invocation_owner_group_counts"], {"minecraft":1})
        self.assertEqual(d["numeric_formula"], "NOT_VERIFIED")
        self.assertEqual(result["getMaxConnections"]["int_arithmetic_op_count"],1)

    def test_no_invention_of_external_call_from_string(self):
        extra=DAMAGE.replace('3: invokevirtual #27 // Method net/minecraft/world/entity/LivingEntity.getHealth:()F','3: ldc #27 // String net/minecraft/world/entity/LivingEntity.getHealth:()F')
        result=inspect("public class X {\n"+extra+CONNECT+"}\n")
        self.assertEqual(result["getDamage"]["direct_invocation_owner_group_counts"], {})

    def test_unknown_invokedynamic_is_explicit(self):
        extra=DAMAGE.replace('3: invokevirtual #27 // Method net/minecraft/world/entity/LivingEntity.getHealth:()F','3: invokedynamic #19, 0 // InvokeDynamic #0:accept:()F')
        result=inspect("public class X {\n"+extra+CONNECT+"}\n")
        self.assertEqual(result["getDamage"]["unresolved_invocation_ref_count"],1)

    def test_missing_exact_signature_fails(self):
        with self.assertRaisesRegex(ValueError,"descriptor drift"):
            inspect("public class X {\n"+DAMAGE.replace('descriptor: (ILnet/minecraft/world/entity/LivingEntity;)F','descriptor: ()F')+CONNECT+"}\n")

    def test_missing_method_body_fails(self):
        with self.assertRaisesRegex(ValueError,"missing exact method"):
            inspect("public class X {\n"+DAMAGE+"}\n")

    def test_duplicate_method_body_fails(self):
        with self.assertRaisesRegex(ValueError,"duplicate method body"):
            inspect("public class X {\n"+DAMAGE+DAMAGE+CONNECT+"}\n")

    def test_foreign_mod_and_branch_categories(self):
        changed = DAMAGE.replace("3: invokevirtual #27 // Method net/minecraft/world/entity/LivingEntity.getHealth:()F", "3: invokestatic #27 // Method io/redspace/ironsspellbooks/api/magic/SpellPower.get:()F")
        changed = changed.replace("7: freturn", "7: ifeq 14\n      10: freturn")
        obj=inspect("public class X {\n"+changed+CONNECT+"}\n")["getDamage"]
        self.assertEqual(obj["direct_invocation_owner_group_counts"], {"irons_spellbooks":1})
        self.assertEqual(obj["branch_op_count"], 1)

    def test_exact_direct_integer_literals(self):
        from alshanex_403_megido_numeric_footprint import direct_integer_return
        self.assertEqual(direct_integer_return([("iconst_3", ""), ("ireturn", "")]), 3)
        self.assertEqual(direct_integer_return([("iconst_m1", ""), ("ireturn", "")]), -1)
        self.assertEqual(direct_integer_return([("bipush", "12"), ("ireturn", "")]), 12)
        self.assertEqual(direct_integer_return([("sipush", "300"), ("ireturn", "")]), 300)
        self.assertEqual(direct_integer_return([("ldc", "#7 // int 2000"), ("ireturn", "")]), 2000)
        self.assertIsNone(direct_integer_return([("iload_1", ""), ("ireturn", "")]))
        self.assertIsNone(direct_integer_return([("iconst_2", ""), ("iadd", ""), ("ireturn", "")]))

    def test_unqualified_method_target_does_not_imply_same_class_owner(self):
        sample = DAMAGE.replace(
            "3: invokevirtual #27 // Method net/minecraft/world/entity/LivingEntity.getHealth:()F",
            "3: invokevirtual #27 // Method getDamageFromStats:(ILnet/minecraft/world/entity/LivingEntity;)F")
        result=inspect("public class X {\n"+sample+CONNECT+"}\n")["getDamage"]
        self.assertEqual(result["direct_invocation_owner_group_counts"], {"unqualified_owner_not_verified":1})
        self.assertEqual(result["unqualified_direct_target_method_names"], ["getDamageFromStats"])

    def test_direct_spell_power_forward_only_when_exact(self):
        from alshanex_403_megido_numeric_footprint import direct_spell_power_delegation
        good = [
            ("aload_0", ""), ("iload_1", ""), ("aload_2", ""),
            ("invokevirtual", "#7 // Method getSpellPower:(ILnet/minecraft/world/entity/LivingEntity;)F"),
            ("freturn", ""),
        ]
        self.assertTrue(direct_spell_power_delegation(good))
        self.assertFalse(direct_spell_power_delegation(good[:-1]+[("fmul", ""),("freturn", "")]))
        self.assertFalse(direct_spell_power_delegation(good[:3]+[("invokevirtual", "#7 // Method other:(ILnet/minecraft/world/entity/LivingEntity;)F")]+good[4:]))
        self.assertFalse(direct_spell_power_delegation(good[:3]+[("invokevirtual", "#7 // Method getSpellPower:()F")]+good[4:]))

    def test_reject_hash_before_javap(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"bad.jar"
            path.write_bytes(b"not exact artifact")
            with self.assertRaisesRegex(ValueError, "SHA-1 mismatch"):
                audit(path)

if __name__=="__main__":
    unittest.main()
