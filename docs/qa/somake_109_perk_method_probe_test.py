#!/usr/bin/env python3
"""Synthetic red/negative fixtures for read-only Somake crafting method gate."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from somake_109_perk_method_probe import GateError, analyze, method_ops, key

FALSE = """public class Fake {
  public boolean allowCrafting();
    descriptor: ()Z
    Code:
       0: iconst_0
       1: ireturn
}
"""
DYNAMIC = """public class Fake {
  public boolean allowCrafting();
    descriptor: ()Z
    Code:
       0: invokestatic  #21   // Method sample/Progress.check:()Z
       3: ifeq          10
       6: iconst_1
       7: ireturn
      10: iconst_0
      11: ireturn
}
"""

class ProbeTests(unittest.TestCase):
    def test_false_only(self):
        r = analyze(method_ops(FALSE))
        self.assertEqual("CONSTANT_FALSE", r["classification"])
        self.assertEqual(0, r["branch_instructions"])
        self.assertEqual([], r["called_or_read_members"])

    def test_conditional_symbolic_path(self):
        r = analyze(method_ops(DYNAMIC))
        self.assertEqual("NON_CONSTANT", r["classification"])
        self.assertEqual(1, r["branch_instructions"])
        self.assertTrue(r["has_explicit_calls"])
        self.assertIn("sample/Progress.check:()Z", r["called_or_read_members"])

    def test_missing_decl_fail_closed(self):
        with self.assertRaises(GateError):
            method_ops(FALSE.replace("allowCrafting", "onCast"))

    def test_double_decl_fail_closed(self):
        with self.assertRaises(GateError):
            method_ops(FALSE + FALSE)

    def test_wrong_jvm_signature_fail_closed(self):
        with self.assertRaises(GateError):
            method_ops(FALSE.replace("descriptor: ()Z", "descriptor: (I)Z"))

    def test_class_identity_normalization(self):
        self.assertEqual(key("FuneralBloom"), key("funeral_bloom"))
        self.assertNotEqual(key("FuneralBloom"), key("RoseSecret"))

    def test_real_java21_javap(self):
        with tempfile.TemporaryDirectory() as folder:
            d=Path(folder)
            (d/"Synthetic.java").write_text(
                "public class Synthetic { public boolean allowCrafting() { return System.nanoTime() > 0; } }\n"
            )
            compile=subprocess.run(["javac",str(d/"Synthetic.java")],capture_output=True,text=True)
            self.assertEqual(0,compile.returncode,compile.stderr)
            proc=subprocess.run(["javap","-p","-c","-s","-classpath",str(d),"Synthetic"],
                                capture_output=True,text=True)
            self.assertEqual(0,proc.returncode,proc.stderr)
            parsed=analyze(method_ops(proc.stdout))
            self.assertEqual("NON_CONSTANT",parsed["classification"])
            self.assertTrue(parsed["has_explicit_calls"])

if __name__ == "__main__":
    unittest.main()
