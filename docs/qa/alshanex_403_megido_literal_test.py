#!/usr/bin/env python3
"""Synthetic fail-closed tests; never bundles third-party bytecode."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from alshanex_403_megido_literal import inspect_javap, audit


class TestMegido(unittest.TestCase):
    def test_direct_literals_only(self):
        j="""public class X {
  public float getRange();
    descriptor: ()F
    Code:
       0: ldc           #38                 // float 12.5f
       2: freturn

  public float getRadius();
    descriptor: ()F
    Code:
       0: fconst_2
       1: freturn
}"""
        values=inspect_javap(j)
        self.assertEqual(values['getRange'],{'status':'EXACT_DIRECT_FLOAT_LITERAL','value':12.5})
        self.assertEqual(values['getRadius'],{'status':'EXACT_DIRECT_FLOAT_LITERAL','value':2.0})

    def test_refuse_dynamic_fields_and_arithmetic(self):
        j="""public class X {
  public float getRange();
    descriptor: ()F
    Code:
       0: aload_0
       1: getfield      #20 // Field range:F
       4: freturn

  public float getRadius();
    descriptor: ()F
    Code:
       0: fconst_2
       1: fload_1
       2: fadd
       3: freturn
}"""
        values=inspect_javap(j)
        self.assertEqual(values['getRange'],{'status':'DYNAMIC_NOT_VERIFIED','value':None})
        self.assertEqual(values['getRadius']['status'],'DYNAMIC_NOT_VERIFIED')

    def test_refuse_changed_descriptor(self):
        j="""public class X {
  public float getRange(int);
    descriptor: (I)F
    Code:
       0: fconst_2
       1: freturn
}"""
        with self.assertRaisesRegex(ValueError,'missing.*getRange'):
            inspect_javap(j)

    def test_refuse_missing_second_method(self):
        j="""public class X {
  public float getRange();
    descriptor: ()F
    Code:
       0: fconst_2
       1: freturn
}"""
        with self.assertRaisesRegex(ValueError,'missing.*getRadius'):
            inspect_javap(j)

    def test_refuse_extra_method_invocation(self):
        j="""public class X {
  public float getRange();
    descriptor: ()F
    Code:
       0: ldc           #38                 // float 12.5f
       2: invokestatic  #39                 // Method foo:()F
       5: freturn

  public float getRadius();
    descriptor: ()F
    Code:
       0: ldc           #38                 // float 1.5f
       2: freturn
}"""
        values=inspect_javap(j)
        self.assertEqual(values['getRange']['status'],'DYNAMIC_NOT_VERIFIED')
        self.assertEqual(values['getRadius']['value'],1.5)

    def test_refuse_wrong_hash_before_javap(self):
        with TemporaryDirectory() as directory:
            p=Path(directory)/'wrong.jar'
            p.write_bytes(b'wrong artifact')
            with self.assertRaisesRegex(ValueError,'SHA-1 mismatch'):
                audit(p)


if __name__=='__main__':
    unittest.main()
