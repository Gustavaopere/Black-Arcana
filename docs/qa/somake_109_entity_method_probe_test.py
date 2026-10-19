#!/usr/bin/env python3
"""Synthetic and Java21 tests for bounded Somake downstream entity symbol discovery."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from somake_109_perk_method_probe import GateError
from somake_109_entity_method_probe import ENTITIES, ENTITY_FOCUS, indicators, summarize
from somake_109_cast_refs import parse_javap

CLASSFILE = """Compiled from "SyntheticEntity.java"
public class SyntheticEntity {
  public SyntheticEntity();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return
  public void tick();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokevirtual #9                  // Method my/pkg/Target.getEntitiesOfClass:()V
       4: invokestatic  #20                 // Method io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:()V
       7: return
  public boolean shouldBeSaved();
    descriptor: ()Z
    Code:
       0: iconst_0
       1: ireturn
}
"""

class EntityMethodTests(unittest.TestCase):
    def test_five_concrete_classes_and_no_duplicates(self):
        self.assertEqual(5, len(ENTITIES))
        self.assertEqual(5, len(set(ENTITIES.values())))
        self.assertTrue(all(v.startswith("com.somake.somakespells.entity.") for v in ENTITIES.values()))

    def test_method_descriptors_and_indicator_names(self):
        parsed = parse_javap(CLASSFILE, "SyntheticEntity")
        result = summarize(parsed)
        self.assertEqual(2, result["focus_methods"])
        self.assertIn("tick", result["indicator_methods"]["damage"])
        self.assertIn("tick", result["indicator_methods"]["entity_targets"])
        self.assertEqual("()V", result["methods"][0]["descriptor"])

    def test_pulse_and_finale_helpers_are_included(self):
        sample = CLASSFILE.replace("public void tick();", "public void pulseDamage();")
        parsed = parse_javap(sample, "SyntheticEntity", focus_pattern=ENTITY_FOCUS)
        self.assertIn("pulseDamage", [x["method"] for x in parsed["methods"]])
        self.assertIn("pulseDamage", summarize(parsed)["indicator_methods"]["damage"])

    def test_absent_method_is_not_runtime_absence(self):
        parsed = parse_javap(CLASSFILE.replace("DamageSources.applyDamage", "OtherUtils.adjustValue"),
                             "SyntheticEntity")
        result = summarize(parsed)
        self.assertFalse(result["indicator_methods"]["damage"])
        self.assertIn("does not establish", result["limits"][0])

    def test_malformed_members_fail_closed(self):
        with self.assertRaises(GateError):
            indicators([{"method": "tick", "members": "a string"}])

    def test_symbol_budget_rejects_oversized(self):
        parsed = parse_javap(CLASSFILE, "SyntheticEntity")
        parsed["methods"][0]["members"] = ["Method Other.something:()V"] * 401
        with self.assertRaises(GateError):
            summarize(parsed)

    def test_duplicate_method_rejected(self):
        source = CLASSFILE.replace("public boolean shouldBeSaved();", "public void tick();").replace(
            "descriptor: ()Z", "descriptor: ()V")
        with self.assertRaises(GateError):
            parse_javap(source, "SyntheticEntity")

    def test_java21_produces_readable_tick(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            (folder/"SyntheticEntity.java").write_text(
                "public class SyntheticEntity { public int tick() { return Math.max(4,5); } }\n")
            build=subprocess.run(["javac",str(folder/"SyntheticEntity.java")],capture_output=True,text=True)
            self.assertEqual(0,build.returncode,build.stderr)
            proc=subprocess.run(["javap","-s","-c","-p","-classpath",str(folder),"SyntheticEntity"],
                                 capture_output=True,text=True)
            self.assertEqual(0,proc.returncode,proc.stderr)
            result=parse_javap(proc.stdout,"SyntheticEntity")
            self.assertIn("Method java/lang/Math.max:(II)I",result["methods"][0]["members"])

if __name__ == "__main__":
    unittest.main()
