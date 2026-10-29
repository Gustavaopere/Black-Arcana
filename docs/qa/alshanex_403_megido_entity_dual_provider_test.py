"""Synthetic clean-room entity ABI regression checks, no provider sources."""
import tempfile
import unittest
from pathlib import Path
from alshanex_403_megido_entity_dual_provider import parse_class, verify_and_inspect, SPECS

FIXTURE = """public class SampleEntity {
  public void tick();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokevirtual #7 // Method net/minecraft/world/entity/Entity.getTarget:()Lnet/minecraft/world/entity/Entity;
       4: invokevirtual #8 // Method net/minecraft/world/entity/LivingEntity.hurt:(Lnet/minecraft/world/damagesource/DamageSource;F)Z
       7: ifeq 11
      10: goto 0
      11: return
  public void setDamage(float);
    descriptor: (F)V
    Code:
       0: aload_0
       1: fload_1
       2: putfield #21 // Field damage:F
       5: return
  public SampleEntity();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokespecial #1 // Method java/lang/Object."<init>":()V
       4: return
}"""

class EntityAuditTests(unittest.TestCase):
    def test_exact_entity_method_and_targets(self):
        obj=parse_class(FIXTURE, "SampleEntity")
        self.assertEqual(obj["declared_method_bodies"],3)
        tick=next(x for x in obj["methods"] if x["declared_method"]=="tick")
        self.assertEqual(tick["branch_op_count"],2)
        self.assertEqual(tick["direct_invocations_by_owner"]["minecraft"],2)
        self.assertEqual(tick["risk_related_direct_references"][1]["symbol_method"],"hurt")
        self.assertEqual(obj["runtime_target_count"],"NOT_VERIFIED")
        self.assertNotIn("ifeq",str(obj))

    def test_overload_descriptors_are_distinct(self):
        source=FIXTURE.replace("  public void setDamage(float);", """  public void setDamage(int);
    descriptor: (I)V
    Code:
       0: return
  public void setDamage(float);""")
        obj=parse_class(source,"SampleEntity")
        self.assertEqual(obj["declared_method_bodies"],4)

    def test_duplicate_abi_fails(self):
        source=FIXTURE.replace("  public void setDamage(float);", """  public void tick();
    descriptor: ()V
    Code:
       0: return
  public void setDamage(float);""")
        with self.assertRaisesRegex(ValueError,"duplicate"):
            parse_class(source,"SampleEntity")

    def test_unresolved_invokedynamic_not_evidence(self):
        src=FIXTURE.replace("7: ifeq 11","7: invokedynamic #18 // InvokeDynamic #0:test:()V")
        o=parse_class(src,"SampleEntity")
        tick=next(x for x in o["methods"] if x["declared_method"]=="tick")
        self.assertEqual(tick["unresolved_invoke_count"],1)

    def test_missing_methods_fail(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            parse_class("public class X {}", "X")

    def test_hash_rejected_before_zip_or_javap_for_both(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"not-a-jar.jar"
            p.write_bytes(b"definitely not a pinned jar")
            for spec in SPECS:
                with self.assertRaisesRegex(ValueError,"SHA-1 mismatch"):
                    verify_and_inspect(p,spec)

if __name__ == "__main__":
    unittest.main()
