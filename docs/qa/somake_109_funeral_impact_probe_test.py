#!/usr/bin/env python3
"""Synthetic/Java21 tests for bounded Somake impact-entity JVM introspection."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from somake_109_perk_method_probe import GateError
from somake_109_cast_refs import parse_javap
from somake_109_funeral_bud_probe import isolate_named_methods
from somake_109_funeral_impact_probe import FQCN, FOCUS_ALL, summarize

TEXT = """public class ImpactFixture {
  public ImpactFixture();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokespecial #1 // Method java/lang/Object."<init>":()V
       4: return
  public void tick();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokevirtual #2 // Method net/minecraft/world/entity/Entity.discard:()V
       4: return
  private void renderParticle();
    descriptor: ()V
    Code:
       0: invokestatic #3 // Method net/minecraft/server/level/ServerLevel.sendParticles:()V
       3: return
}
"""

def parse(source=TEXT):
    return parse_javap(isolate_named_methods(source), "ImpactFixture",
                       focus_pattern=FOCUS_ALL)

class ImpactProbeTest(unittest.TestCase):
    def test_pinned_identity(self):
        self.assertEqual("com.somake.somakespells.entity.FuneralBloomImpactEntity", FQCN)

    def test_named_method_capture(self):
        r = summarize(parse())
        self.assertEqual(2, r["named_methods"])
        self.assertEqual(["tick", "renderParticle"], [m["method"] for m in r["methods"]])
        self.assertEqual("()V", r["methods"][0]["descriptor"])

    def test_lifecycle_and_particles_are_only_symbol_hints(self):
        r = summarize(parse())
        self.assertEqual(["tick()V"], r["categories_by_method"]["lifecycle"])
        self.assertEqual(["renderParticle()V"], r["categories_by_method"]["particles_sounds"])
        self.assertEqual([], r["categories_by_method"]["damage"])

    def test_duplicate_signature_fails_closed(self):
        bad = TEXT.replace("private void renderParticle();", "private void tick();")
        with self.assertRaises(GateError):
            parse(bad)

    def test_initialization_block_does_not_pollute_last_method(self):
        bad = TEXT.replace("}\n", """  static {};
    Code:
       0: invokestatic #4 // Method fake/DamageSources.applyDamage:()V
       3: return
}
""")
        r = summarize(parse(bad))
        self.assertEqual([], r["categories_by_method"]["damage"])
        self.assertEqual(2, r["named_methods"])

    def test_budget_fails_closed(self):
        p = parse()
        p["methods"][0]["members"] = ["Method X.foo:()V"] * 461
        with self.assertRaises(GateError):
            summarize(p)

    def test_real_java21_method_descriptor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ImpactFixture.java").write_text(
                "public class ImpactFixture { public int tick() { return Math.max(1,2); } }\n")
            compile_result = subprocess.run(["javac",str(root / "ImpactFixture.java")],
                                            capture_output=True,text=True)
            self.assertEqual(0, compile_result.returncode, compile_result.stderr)
            q = subprocess.run(["javap","-p","-s","-c","-classpath",str(root),"ImpactFixture"],
                               capture_output=True,text=True)
            self.assertEqual(0, q.returncode, q.stderr)
            parsed = summarize(parse(q.stdout))
            self.assertIn("Method java/lang/Math.max:(II)I", parsed["methods"][0]["members"])

if __name__ == "__main__":
    unittest.main()
