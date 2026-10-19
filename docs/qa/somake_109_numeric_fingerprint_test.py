#!/usr/bin/env python3
"""Positive, negative and Java21 tests for exact Somake numeric fingerprints."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from somake_109_perk_method_probe import GateError
from somake_109_numeric_fingerprint import decode_numeric, fingerprint, parse_selected_javap

SYNTHETIC = """public class NumericFixture {
  public NumericFixture();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokespecial #1 // Method java/lang/Object."<init>":()V
       4: return
  public float getRadius(int);
    descriptor: (I)F
    Code:
       0: fconst_2
       1: ldc #2 // float 3.5f
       3: fadd
       4: bipush 10
       6: i2f
       7: invokestatic #4 // Method net/minecraft/util/Mth.clamp:(FFF)F
      10: freturn
  public void tick();
    descriptor: ()V
    Code:
       0: ldc #9 // String do_not_export
       2: iconst_m1
       3: istore_1
       4: return
}
"""

class NumericTests(unittest.TestCase):
    def test_numeric_opcodes_are_typed(self):
        self.assertEqual(("int","-1"),decode_numeric("iconst_m1","",""))
        self.assertEqual(("float","2"),decode_numeric("fconst_2","",""))
        self.assertEqual(("float","3.5"),decode_numeric("ldc","#2","float 3.5f"))
        self.assertEqual(("int","10"),decode_numeric("bipush","10",""))
        self.assertEqual(("double","0.125"),decode_numeric("ldc2_w","#2","double 0.125d"))

    def test_string_constants_excluded(self):
        self.assertIsNone(decode_numeric("ldc","#7","String 3.5f"))
        self.assertIsNone(decode_numeric("getstatic","#3","Field XXX:F"))

    def test_method_scope_keeps_literal_values_separate(self):
        d=parse_selected_javap(SYNTHETIC,("getRadius","tick"))
        self.assertEqual("(I)F",d["getRadius"]["descriptor"])
        self.assertEqual("()V",d["tick"]["descriptor"])
        self.assertEqual(1,d["getRadius"]["bounded_callsite_counts"]["Mth.clamp:"])
        self.assertEqual(1,d["getRadius"]["arithmetic_opcode_counts"]["fadd"])
        self.assertEqual(3,d["getRadius"]["numeric_literal_occurrences"])
        self.assertEqual([{"type":"int","literal":"-1","occurrences":1}],d["tick"]["numeric_literals"])

    def test_direct_clamp_literal_operand_positions(self):
        d=parse_selected_javap(SYNTHETIC,("getRadius",))
        proof=d["getRadius"]["direct_trailing_clamp_literals"]
        self.assertEqual([],proof)  # i2f immediately precedes clamp, so fail closed
        direct=SYNTHETIC.replace(
            "       4: bipush 10\n       6: i2f\n",
            "       4: ldc #5 // float 3.5f\n       6: ldc #6 // float 10.0f\n"
        )
        e=parse_selected_javap(direct,("getRadius",))
        self.assertEqual(1,len(e["getRadius"]["direct_trailing_clamp_literals"]))
        literal=e["getRadius"]["direct_trailing_clamp_literals"][0]
        self.assertEqual("3.5",literal["second_argument_literal"])
        self.assertEqual("10.0",literal["third_argument_literal"])

    def test_intervening_arithmetic_never_certifies_trailing_literals(self):
        direct=SYNTHETIC.replace(
            "       4: bipush 10\n       6: i2f\n",
            "       4: ldc #5 // float 3.5f\n       6: fmul\n       7: ldc #6 // float 10.0f\n"
        )
        q=parse_selected_javap(direct,("getRadius",))
        self.assertEqual([],q["getRadius"]["direct_trailing_clamp_literals"])

    def test_missing_method_fails_closed(self):
        with self.assertRaises(GateError):
            parse_selected_javap(SYNTHETIC,("getDamage",))

    def test_duplicate_method_name_is_ambiguous_even_overloaded(self):
        text=SYNTHETIC.replace("public void tick();","public float getRadius();")
        with self.assertRaises(GateError):
            parse_selected_javap(text,("getRadius",))

    def test_invalid_int_immediate_fails_closed(self):
        with self.assertRaises(GateError):
            decode_numeric("bipush","NaN","")

    def test_literal_budget_enforced(self):
        with self.assertRaises(GateError):
            fingerprint(["       0: iconst_1"]*111)

    def test_static_initializer_excluded_from_last_method(self):
        data=SYNTHETIC.replace("}\n", """  static {};
    Code:
       0: ldc #10 // int 900000
       2: return
}
""")
        d=parse_selected_javap(data,("tick",))
        self.assertNotIn("900000",repr(d))

    def test_java21_compiled_literals(self):
        with tempfile.TemporaryDirectory() as temp:
            d=Path(temp)
            (d/"NumericFixture.java").write_text(
                "public class NumericFixture { public float getRadius(int x) { return x + 5.5f; } }\n")
            result=subprocess.run(["javac",str(d/"NumericFixture.java")],text=True,capture_output=True)
            self.assertEqual(0,result.returncode,result.stderr)
            p=subprocess.run(["javap","-c","-p","-s","-classpath",str(d),"NumericFixture"],
                             text=True,capture_output=True)
            self.assertEqual(0,p.returncode,p.stderr)
            q=parse_selected_javap(p.stdout,("getRadius",))
            self.assertIn({"type":"float","literal":"5.5","occurrences":1},
                          q["getRadius"]["numeric_literals"])

if __name__ == "__main__":
    unittest.main()
