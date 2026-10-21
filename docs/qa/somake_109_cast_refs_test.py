#!/usr/bin/env python3
"""Bounded synthetic tests for Somake cast-reference discovery."""
import subprocess
import tempfile
import unittest
from pathlib import Path
from somake_109_cast_refs import GateError, parse_javap

SAMPLE = """Compiled from "Fixture.java"
public class Fixture {
  public Fixture();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokespecial #1  // Method java/lang/Object."<init>":()V
       4: return
  public void onCast();
    descriptor: ()V
    Code:
       0: aload_0
       1: getfield #9  // Field my/pkg/Fixture.radius:F
       4: invokestatic #15 // Method my/pkg/Spawn.spawn:(F)V
       7: return
  private void helper();
    descriptor: ()V
    Code:
       0: return
}
"""

class DiscoveryTests(unittest.TestCase):
    def test_extract_focus_and_symbols(self):
        row = parse_javap(SAMPLE, "Fixture")
        self.assertEqual(2, row["declared_methods"])
        self.assertEqual(1, row["focused_methods"])
        focus = row["methods"][0]
        self.assertEqual("onCast", focus["method"])
        self.assertEqual("()V", focus["descriptor"])
        self.assertIn("Field my/pkg/Fixture.radius:F", focus["members"])
        self.assertIn("Method my/pkg/Spawn.spawn:(F)V", focus["members"])
        self.assertEqual(1, focus["invokes"])
        self.assertEqual([{"method":"helper","descriptor":"()V"}],row["other_declared"])

    def test_missing_descriptor_rejected(self):
        with self.assertRaises(GateError):
            parse_javap(SAMPLE.replace("descriptor: ()V\n    Code:", "no-descriptor\n    Code:", 1)
                              .replace("descriptor: ()V\n    Code:", "no-descriptor\n    Code:", 1),
                        "Fixture")

    def test_duplicate_signature_rejected(self):
        fake = SAMPLE.replace("  private void helper();", "  public void onCast();").replace(
            "  public void onCast();", "  public void onCast();", 1)
        with self.assertRaises(GateError):
            parse_javap(fake, "Fixture")

    def test_no_focus_rejected(self):
        with self.assertRaises(GateError):
            parse_javap(SAMPLE.replace("onCast", "ordinary"), "Fixture")

    def test_oversize_rejected(self):
        with self.assertRaises(GateError):
            parse_javap("x" * 1_000_001, "Fixture")

    def test_abnormally_long_symbol_rejected(self):
        oversized = SAMPLE.replace("my/pkg/Fixture.radius:F", "A" * 2050)
        with self.assertRaises(GateError):
            parse_javap(oversized, "Fixture")

    def test_real_java21_symbols(self):
        with tempfile.TemporaryDirectory() as temp:
            d=Path(temp)
            (d/"Fixture.java").write_text(
                "public class Fixture { public int onCast() { return Math.max(2,3); } }\n"
            )
            j=subprocess.run(["javac", str(d/"Fixture.java")],capture_output=True,text=True)
            self.assertEqual(0,j.returncode,j.stderr)
            p=subprocess.run(["javap","-p","-s","-c","-classpath",str(d),"Fixture"],
                             capture_output=True,text=True)
            self.assertEqual(0,p.returncode,p.stderr)
            v=parse_javap(p.stdout,"Fixture")
            self.assertIn("Method java/lang/Math.max:(II)I",v["methods"][0]["members"])

if __name__ == "__main__":
    unittest.main()
