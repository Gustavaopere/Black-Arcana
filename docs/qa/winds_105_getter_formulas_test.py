#!/usr/bin/env python3
"""Synthetic JVM proof obligations for clean-room scalar inspector."""
import unittest
import winds_105_getter_formulas as inspect

EXAMPLE="""public class Demo {
  public int getDuration(int);
    Code:
       0: iload_1
       1: iconst_2
       2: iadd
       3: bipush 25
       5: imul
       6: ireturn
  public void onCast();
    Code:
       0: iconst_4
       1: return
}"""

class ScalarTests(unittest.TestCase):
    def test_precise_precedence_and_scaling(self):
        steps=inspect.extract_method_instructions(EXAMPLE,'getDuration(int);')
        got=inspect.analyze(steps,'ireturn')
        expected={"kind":"binary","opcode":"imul","operator":"*",
                  "left":{"kind":"binary","opcode":"iadd","operator":"+",
                          "left":{"kind":"parameter","slot":1},
                          "right":{"kind":"literal","value":"2"}},
                  "right":{"kind":"literal","value":"25"}}
        self.assertEqual(expected,got['expression_ast'])
    def test_math_max_and_subtract_with_arguments(self):
        s="""public class Demo {
  public int getRecastCount(int, java.lang.Object);
    Code:
       0: iload_1
       1: iconst_1
       2: isub
       3: iconst_0
       4: invokestatic #100 // Method java/lang/Math.max:(II)I
       7: ireturn
}"""
        got=inspect.analyze(inspect.extract_method_instructions(s,'getRecastCount(int, java.lang.Object);'),'ireturn')
        self.assertEqual('jdk_math_max_int',got['expression_ast']['kind'])
        self.assertEqual('isub',got['expression_ast']['left']['opcode'])
    def test_nontrivial_guard_fails_closed(self):
        steps=inspect.extract_method_instructions(EXAMPLE.replace('2: iadd','2: ifle 6'),'getDuration(int);')
        with self.assertRaisesRegex(inspect.Unsupported,'unsupported opcode ifle'):
            inspect.analyze(steps,'ireturn')
    def test_nontrivial_write_fails_closed(self):
        steps=inspect.extract_method_instructions(EXAMPLE.replace('2: iadd','2: putfield #1 // Field demo/Damage:F'),'getDuration(int);')
        with self.assertRaisesRegex(inspect.Unsupported,'unsupported opcode putfield'):
            inspect.analyze(steps,'ireturn')
    def test_unknown_method_fails_closed(self):
        with self.assertRaisesRegex(inspect.Unsupported,'exact signature missing'):
            inspect.extract_method_instructions(EXAMPLE,'getInvalid(int);')
    def test_does_not_capture_neighboring_method_instructions(self):
        got=inspect.extract_method_instructions(EXAMPLE,'getDuration(int);')
        self.assertNotIn('iconst_4',[op for _,op,_ in got])
    def test_unknown_call_not_accepted(self):
        steps=[(0,'iload_1',''),(1,'invokestatic','#9 // Method foo/Bar.max:(I)I'),(4,'ireturn','')]
        with self.assertRaisesRegex(inspect.Unsupported,'unsupported opcode invokestatic'):
            inspect.analyze(steps,'ireturn')
    def test_extra_operand_rejected(self):
        steps=[(0,'iconst_1',''),(1,'iconst_2',''),(2,'ireturn','')]
        with self.assertRaisesRegex(inspect.Unsupported,'invalid final stack height'):
            inspect.analyze(steps,'ireturn')
    def test_rejects_nonnumeric_ldc(self):
        steps=[(0,'ldc','#2 // String magical'),(3,'ireturn','')]
        with self.assertRaisesRegex(inspect.Unsupported,'non-numeric ldc'):
            inspect.analyze(steps,'ireturn')
    def test_rejects_exception_table(self):
        code=EXAMPLE.replace('       6: ireturn','       6: ireturn\n    Exception table:\n      from to target type')
        with self.assertRaisesRegex(inspect.Unsupported,'exception-table'):
            inspect.extract_method_instructions(code,'getDuration(int);')

if __name__=='__main__':
    unittest.main()
