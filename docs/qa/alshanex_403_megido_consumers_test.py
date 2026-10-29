"""Synthetic fixtures for an exact-JAR, clean-room callsite inventory."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from alshanex_403_megido_consumers import inspect_javap, audit

GETTERS = '''
  public float getRange();
    descriptor: ()F
    Code:
       0: ldc #17 // float 15.0f
       2: freturn

  public float getRadius();
    descriptor: ()F
    Code:
       0: ldc #18 // float 10.0f
       2: freturn
'''

class ContractTests(unittest.TestCase):
    def test_direct_oncast_calls_and_counted_indirect(self):
        text = '''public class net.alshanex.alshanex_familiars.spells.MegidoSpell {
  public void onCast(net.minecraft.world.level.Level);
    descriptor: (Lnet/minecraft/world/level/Level;)V
    Code:
       0: aload_0
       1: invokevirtual #18 // Method getRange:()F
       4: aload_0
       5: invokevirtual #19 // Method getRadius:()F
       8: return

  private void helper();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokevirtual #19 // Method getRadius:()F
       4: return
''' + GETTERS + '}\n'
        result = inspect_javap(text)
        self.assertEqual(result['getRange']['same_class_calls'], 1)
        self.assertEqual(result['getRange']['direct_on_cast_calls'], 1)
        self.assertEqual(result['getRadius']['same_class_calls'], 2)
        self.assertEqual(result['getRadius']['direct_on_cast_calls'], 1)
        self.assertEqual(result['getRadius']['calling_methods'], ['helper','onCast'])

    def test_dont_count_foreign_owner_or_string_constant(self):
        text = '''public class net.alshanex.alshanex_familiars.spells.MegidoSpell {
  public void onCast();
    descriptor: ()V
    Code:
       0: ldc #1 // String getRange:()F
       2: invokevirtual #20 // Method another/Owner.getRange:()F
       5: invokevirtual #21 // Method otherMethod:()F
       8: return
''' + GETTERS + '}\n'
        result = inspect_javap(text)
        self.assertEqual(result['getRange']['same_class_calls'],0)
        self.assertEqual(result['getRadius']['same_class_calls'],0)
        self.assertEqual(result['getRange']['status'],'NO_SAME_CLASS_DIRECT_CALL_SEEN')

    def test_enforce_method_signature_and_no_missing_oncast(self):
        text = '''public class X {
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
}'''
        with self.assertRaisesRegex(ValueError,'missing.*onCast'):
            inspect_javap(text)

    def test_reject_ambiguous_duplicate(self):
        text = '''public class X {
  public void onCast();
    descriptor: ()V
    Code:
       0: return
''' + GETTERS + GETTERS + '}\n'
        with self.assertRaisesRegex(ValueError,'duplicate.*getRange'):
            inspect_javap(text)

    def test_reject_unsupported_invocation_owner(self):
        text='''public class X {
  public void onCast();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokevirtual #20 // Method getRange:()F
       4: return
''' + GETTERS + '}\n'
        result=inspect_javap(text)
        self.assertEqual(result['getRange']['same_class_calls'],1)

    def test_wrong_jar_rejected_before_disassembly(self):
        with TemporaryDirectory() as td:
            p=Path(td)/'provider.jar'
            p.write_bytes(b'invalid')
            with self.assertRaisesRegex(ValueError,'SHA-1 mismatch'):
                audit(p)

if __name__=='__main__':
    unittest.main()
