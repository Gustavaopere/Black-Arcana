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

    def test_reject_hash_before_javap(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"bad.jar"
            path.write_bytes(b"not exact artifact")
            with self.assertRaisesRegex(ValueError, "SHA-1 mismatch"):
                audit(path)

if __name__=="__main__":
    unittest.main()
