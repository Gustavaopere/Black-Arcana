"""Synthetic parse checks for Megido symbolic target consumer inventory."""
import tempfile
import unittest
from pathlib import Path
from alshanex_403_megido_oncast_targets import inventory, audit

FIXTURE = """public class X {
  public void onCast();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokevirtual #1 // Method getMaxConnections:(ILnet/minecraft/world/entity/LivingEntity;)I
       4: invokestatic #2 // Method net/minecraft/world/entity/EntitySelector.NO_SPECTATORS:()V
       7: goto 0
      10: return

  public float getRange();
    descriptor: ()F
    Code:
       0: fconst_1
       1: freturn
  public float getRadius();
    descriptor: ()F
    Code:
       0: fconst_1
       1: freturn
  public float getDamage();
    descriptor: ()F
    Code:
       0: fconst_1
       1: freturn
  public int getMaxConnections();
    descriptor: ()I
    Code:
       0: iconst_1
       1: ireturn
}"""

class TestInventory(unittest.TestCase):
    def test_owner_and_method_identifiers_without_bytecode(self):
        v=inventory(FIXTURE)
        self.assertEqual(v["on_cast_branch_instruction_count"],1)
        self.assertEqual(v["on_cast_goto_instruction_count"],1)
        self.assertEqual(v["selected_target_count"],"NOT_VERIFIED")
        self.assertEqual(v["direct_method_references"], [
            {"symbol_owner":"UNQUALIFIED_OWNER","symbol_method":"getMaxConnections","count":1},
            {"symbol_owner":"net/minecraft/world/entity/EntitySelector","symbol_method":"NO_SPECTATORS","count":1}
        ])
        self.assertNotIn("goto 0",str(v))

    def test_dont_promote_string_constant_to_call(self):
        z=FIXTURE.replace("4: invokestatic #2 // Method net/minecraft/world/entity/EntitySelector.NO_SPECTATORS:()V",
                          "4: ldc #2 // String net/minecraft/world/entity/EntitySelector.NO_SPECTATORS:()V")
        self.assertEqual(len(inventory(z)["direct_method_references"]),1)

    def test_unresolved_invokedynamic_is_explicit(self):
        z=FIXTURE.replace("4: invokestatic #2 // Method net/minecraft/world/entity/EntitySelector.NO_SPECTATORS:()V",
                          "4: invokedynamic #2 // InvokeDynamic #0:foo:()V")
        self.assertEqual(inventory(z)["unresolved_invoke_count"],1)

    def test_targeted_descriptor_observed(self):
        a = inventory(FIXTURE)
        self.assertIn(
            {"owner":"UNQUALIFIED_OWNER", "method":"getMaxConnections",
             "jvm_descriptor":"(ILnet/minecraft/world/entity/LivingEntity;)I", "count":1},
            a["targeted_jvm_signatures"])

    def test_constructor_descriptor_is_recorded_without_body(self):
        fixture = FIXTURE.replace(
            "4: invokestatic #2 // Method net/minecraft/world/entity/EntitySelector.NO_SPECTATORS:()V",
            '4: invokespecial #2 // Method net/alshanex/alshanex_familiars/entity/misc/MegidoEntity."<init>":(Lnet/minecraft/world/level/Level;)V')
        a = inventory(fixture)
        self.assertIn(
            {"owner":"net/alshanex/alshanex_familiars/entity/misc/MegidoEntity",
             "method":"<init>", "jvm_descriptor":"(Lnet/minecraft/world/level/Level;)V", "count":1},
            a["targeted_jvm_signatures"])

    def test_missing_method_rejected(self):
        z=FIXTURE.replace("getRadius();","radiusOther();")
        with self.assertRaisesRegex(ValueError,"getter"):
            inventory(z)

    def test_ambiguous_oncast_rejected(self):
        z=FIXTURE.replace("  public float getRange();", """  public void onCast();
    descriptor: ()V
    Code:
       0: return
  public float getRange();""")
        with self.assertRaisesRegex(ValueError,"duplicate method body"):
            inventory(z)

    def test_sha_checked_before_javap(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"fake.jar"
            p.write_bytes(b"invalid")
            with self.assertRaisesRegex(ValueError,"SHA-1 mismatch"):
                audit(p)

if __name__=="__main__":
    unittest.main()
