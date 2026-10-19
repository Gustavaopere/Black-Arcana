#!/usr/bin/env python3
"""Synthetic and Java21 regression checks for Somake Funeral Bloom bud probe."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from somake_109_perk_method_probe import GateError
from somake_109_funeral_bud_probe import CATEGORIES, FQCN, FOCUS_ALL_NAMED, classify, summarize
from somake_109_cast_refs import parse_javap

FIXTURE = """public class BudFixture {
  public BudFixture();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokespecial #1 // Method java/lang/Object."<init>":()V
       4: return
  public void tick();
    descriptor: ()V
    Code:
       0: invokestatic #2 // Method net/minecraft/server/level/ServerLevel.getEntitiesOfClass:()V
       3: return
  private void pulse();
    descriptor: ()V
    Code:
       0: invokestatic #3 // Method io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:()Z
       3: return
  public void onAntiMagic();
    descriptor: ()V
    Code:
       0: invokevirtual #4 // Method net/minecraft/world/entity/Entity.discard:()V
       3: return
}
"""

class BudProbeTests(unittest.TestCase):
    def test_exact_target_name(self):
        self.assertEqual("com.somake.somakespells.entity.FuneralBloomBudEntity", FQCN)

    def test_all_named_methods_including_pulse(self):
        data = summarize(parse_javap(FIXTURE, "BudFixture", focus_pattern=FOCUS_ALL_NAMED))
        self.assertEqual(3, data["named_methods_analyzed"])
        names = [x["method"] for x in data["methods"]]
        self.assertEqual(["tick", "pulse", "onAntiMagic"], names)

    def test_classification_is_reference_only(self):
        data = summarize(parse_javap(FIXTURE, "BudFixture", focus_pattern=FOCUS_ALL_NAMED))
        self.assertEqual(["pulse"], data["candidate_categories"]["damage"])
        self.assertEqual(["tick"], data["candidate_categories"]["targets"])
        self.assertEqual(["onAntiMagic"], data["candidate_categories"]["lifecycle"])
        self.assertEqual([], data["candidate_categories"]["healing"])

    def test_absence_of_symbol_is_not_absence_of_effect(self):
        data = summarize(parse_javap(FIXTURE.replace("DamageSources.applyDamage", "Something.compute"),
                                     "BudFixture", focus_pattern=FOCUS_ALL_NAMED))
        self.assertEqual([], data["candidate_categories"]["damage"])

    def test_duplicate_jvm_method_fail_closed(self):
        double = FIXTURE.replace("private void pulse();", "public void tick();")
        with self.assertRaises(GateError):
            parse_javap(double, "BudFixture", focus_pattern=FOCUS_ALL_NAMED)

    def test_bad_method_evidence_fails(self):
        with self.assertRaises(GateError):
            classify([{"method": "tick", "members": "not_a_list"}])

    def test_ref_budget_fails(self):
        parsed = parse_javap(FIXTURE, "BudFixture", focus_pattern=FOCUS_ALL_NAMED)
        parsed["methods"][0]["members"] = ["Method aa.foo:()V"] * 461
        with self.assertRaises(GateError):
            summarize(parsed)

    def test_java21_compiled_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            (p / "BudFixture.java").write_text(
                "public class BudFixture { public double pulse() { return Math.sqrt(4); } }\n")
            build = subprocess.run(["javac", str(p/"BudFixture.java")], capture_output=True, text=True)
            self.assertEqual(0, build.returncode, build.stderr)
            out = subprocess.run(["javap", "-p", "-s", "-c", "-classpath", str(p), "BudFixture"],
                                 capture_output=True, text=True)
            self.assertEqual(0, out.returncode, out.stderr)
            data = summarize(parse_javap(out.stdout, "BudFixture", focus_pattern=FOCUS_ALL_NAMED))
            self.assertIn("pulse", [x["method"] for x in data["methods"]])

if __name__ == "__main__":
    unittest.main()
