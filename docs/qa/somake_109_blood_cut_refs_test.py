#!/usr/bin/env python3
"""Synthetic negative and positive gates for Somake Blood Cut static evidence."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from somake_109_blood_cut_refs import discover_member
from somake_109_cast_refs import GateError, parse_javap

GOOD = "com/somake/somakespells/spells/blood/BloodCutSpell.class"


class BloodCutEvidenceTests(unittest.TestCase):
    def test_unambiguous_candidate(self):
        self.assertEqual(GOOD, discover_member([GOOD, "other/Other.class"]))

    def test_missing_candidate_fails(self):
        with self.assertRaises(GateError):
            discover_member(["com/somake/somakespells/spells/blood/OtherSpell.class"])

    def test_ambiguous_candidate_fails(self):
        with self.assertRaises(GateError):
            discover_member([GOOD, "com/somake/somakespells/spells/fire/BloodCutSpell.class"])

    def test_duplicate_zip_names_fail(self):
        with self.assertRaises(GateError):
            discover_member([GOOD, GOOD])

    def test_outside_provider_package_fails(self):
        with self.assertRaises(GateError):
            discover_member(["other/provider/spells/blood/BloodCutSpell.class"])

    def test_traversal_fails(self):
        with self.assertRaises(GateError):
            discover_member(["com/somake/somakespells/spells/../BloodCutSpell.class"])

    def test_parse_real_java21_class_symbols(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BloodCutSpell.java").write_text(
                "public class BloodCutSpell { "
                "public int getDamage(int level) { return Math.max(level, 2); } "
                "public void onCast() { getDamage(3); } "
                "}\n"
            )
            compiler = subprocess.run(["javac", str(root / "BloodCutSpell.java")],
                                      capture_output=True, text=True)
            self.assertEqual(compiler.returncode, 0, compiler.stderr)
            compiler = subprocess.run(
                ["javap", "-p", "-s", "-c", "-classpath", str(root), "BloodCutSpell"],
                capture_output=True, text=True
            )
            self.assertEqual(compiler.returncode, 0, compiler.stderr)
            result = parse_javap(compiler.stdout, "BloodCutSpell")
            members = {ref for m in result["methods"] for ref in m["members"]}
            self.assertTrue(any("java/lang/Math.max:(II)I" in ref for ref in members))
            self.assertTrue(any(m["method"] == "onCast" for m in result["methods"]))


if __name__ == "__main__":
    unittest.main()
