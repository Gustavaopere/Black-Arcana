"""Synthetic tests of bounded, fail-closed Megido first-use classification."""
import tempfile
import unittest
from pathlib import Path
from alshanex_403_megido_first_use import parse_calls, audit

COMMON = '''
  public float getRange();
    descriptor: ()F
    Code:
       0: ldc #16 // float 15.0f
       2: freturn
  public float getRadius();
    descriptor: ()F
    Code:
       0: ldc #17 // float 10.0f
       2: freturn
  public float getDamage(int, java.lang.Object);
    descriptor: (ILjava/lang/Object;)F
    Code:
       0: fconst_1
       1: freturn
  public int getMaxConnections(int, java.lang.Object);
    descriptor: (ILjava/lang/Object;)I
    Code:
       0: iconst_1
       1: ireturn
'''
def body(calls):
    return 'public class X {\n  public void onCast();\n    descriptor: ()V\n    Code:\n' + calls + COMMON + '}\n'

class Tests(unittest.TestCase):
    def test_conversion_and_local_storage_plus_other_calls(self):
        sample=body('''       0: aload_0
       1: invokevirtual #1 // Method getRange:()F
       4: f2d
       5: dstore_1
       6: aload_0
       7: invokevirtual #2 // Method getRadius:()F
      10: fstore_3
      11: aload_0
      12: iconst_1
      13: aconst_null
      14: invokevirtual #3 // Method getMaxConnections:(ILjava/lang/Object;)I
      17: return
''')
        got=parse_calls(sample)
        self.assertEqual(got['getters']['getRange']['first_following_category'], 'FLOAT_PRIMITIVE_CONVERSION')
        self.assertEqual(got['getters']['getRadius']['first_following_category'], 'STORED_TO_LOCAL')
        self.assertEqual(got['other_declared_methods_directly_called_from_on_cast']['getMaxConnections']['count'], 1)
        self.assertEqual(got['other_declared_methods_directly_called_from_on_cast']['getDamage']['count'], 0)

    def test_arithmetic_and_unknown_not_misrepresented(self):
        sample=body('''       0: aload_0
       1: invokevirtual #1 // Method getRange:()F
       4: fmul
       5: aload_0
       6: invokevirtual #2 // Method getRadius:()F
       9: invokestatic #6 // Method external/Helper.func:(F)V
      12: return
''')
        got=parse_calls(sample)
        self.assertEqual(got['getters']['getRange']['first_following_category'], 'FLOAT_ARITHMETIC_OR_COMPARISON')
        self.assertEqual(got['getters']['getRadius']['first_following_category'], 'NEXT_INSTRUCTION_NOT_PROVEN_CONSUMER')

    def test_foreign_owner_not_counted(self):
        sample=body('''       0: aload_0
       1: invokevirtual #1 // Method getRange:()F
       4: fstore_1
       5: aload_0
       6: invokevirtual #2 // Method getRadius:()F
       9: fstore_2
      10: invokestatic #4 // Method other/Type.getDamage:(ILjava/lang/Object;)F
      13: return
''')
        got=parse_calls(sample)
        self.assertEqual(got['other_declared_methods_directly_called_from_on_cast']['getDamage']['count'], 0)

    def test_missing_oncast(self):
        with self.assertRaisesRegex(ValueError, 'onCast'):
            parse_calls('public class X {'+COMMON+'}\n')

    def test_missing_second_getter(self):
        sample=body('''       0: aload_0
       1: invokevirtual #1 // Method getRange:()F
       4: fstore_1
       5: return
''')
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            parse_calls(sample)

    def test_duplicate_getter_invocations_are_fail_closed(self):
        sample=body('''       0: aload_0
       1: invokevirtual #1 // Method getRange:()F
       4: fstore_1
       5: aload_0
       6: invokevirtual #1 // Method getRange:()F
       9: fstore_2
      10: aload_0
      11: invokevirtual #2 // Method getRadius:()F
      14: fstore_3
      15: return
''')
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            parse_calls(sample)

    def test_wrong_jar_fails_before_javap(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'wrong.jar'
            p.write_bytes(b'not Alshanex')
            with self.assertRaisesRegex(ValueError,'SHA-1 mismatch'):
                audit(p)

if __name__ == '__main__':
    unittest.main()
