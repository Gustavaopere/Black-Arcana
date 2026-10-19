#!/usr/bin/env python3
"""Positive and fail-closed synthetic JVM path fixtures, plus Java21 compiled CFG."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from somake_109_radius_typed_paths import interpret, certify_exact_109, EXPECTED_EXACT_109_RADIUS_PATHS
from somake_109_radius_irons_contract import SOMAKE_GETTER_DESC, radius_cfg, opcode_rows

GOOD=[
 "   0: aload_2",
 "   1: ifnonnull 10",
 "   4: fconst_1",
 "   5: goto 20",
 "  10: aload_0",
 "  11: invokevirtual #7 // Method getSchoolType:()Lio/redspace/ironsspellbooks/api/spells/SchoolType;",
 "  14: aload_2",
 "  15: invokevirtual #8 // Method io/redspace/ironsspellbooks/api/spells/SchoolType.getPowerFor:(Lnet/minecraft/world/entity/LivingEntity;)D",
 "  18: d2f",
 "  20: ldc #11 // float 0.82f",
 "  22: fmul",
 "  23: ldc #12 // float 9.5f",
 "  25: invokestatic #13 // Method java/lang/Math.max:(FF)F",
 "  28: ldc #14 // float 10.0f",
 "  30: ldc #15 // float 15.0f",
 "  32: invokestatic #16 // Method net/minecraft/util/Mth.clamp:(FFF)F",
 "  35: freturn"
]
class RadiusPathTests(unittest.TestCase):
    def test_both_paths_proven_in_synthetic_fixture(self):
        result=interpret(GOOD,SOMAKE_GETTER_DESC)
        self.assertEqual("PROVED_TWO_PATH_JVM_FLOAT_EXPRESSION",result["status"],result)
        paths={x["condition"]:x for x in result["paths"]}
        self.assertEqual({"caster == null","caster != null"},set(paths))
        self.assertIn("schoolPower(caster)",paths["caster != null"]["jvm_float_expression"])
        self.assertNotIn("schoolPower",paths["caster == null"]["jvm_float_expression"])
        self.assertIn("Mth.clamp_f32",paths["caster == null"]["jvm_float_expression"])

    def test_wrong_guard_subject_rejected(self):
        bad=GOOD.copy();bad[0]="0: aload_0"
        self.assertEqual("NOT_PROVED",interpret(bad,SOMAKE_GETTER_DESC)["status"])

    def test_unknown_opcode_rejected(self):
        bad=GOOD.copy();bad[9]="20: f2i"
        self.assertEqual("NOT_PROVED",interpret(bad,SOMAKE_GETTER_DESC)["status"])

    def test_altered_clamp_limits_fail_closed(self):
        bad=[x.replace("15.0f","19.0f") for x in GOOD]
        self.assertEqual("NOT_PROVED",interpret(bad,SOMAKE_GETTER_DESC)["status"])

    def test_external_nonallowlisted_call_rejected(self):
        bad=[x.replace("SchoolType.getPowerFor","SchoolType.getWorldPower") for x in GOOD]
        self.assertEqual("NOT_PROVED",interpret(bad,SOMAKE_GETTER_DESC)["status"])

    def test_wrong_descriptor_never_certified(self):
        self.assertEqual("NOT_PROVED",interpret(GOOD,"(I)F")["status"])

    def test_unreachable_code_must_not_be_skipped(self):
        bad=GOOD.copy()
        bad.insert(-1,"  34: fconst_0")
        self.assertEqual("NOT_PROVED",interpret(bad,SOMAKE_GETTER_DESC)["status"])

    def test_stack_type_mismatch_refused(self):
        bad=GOOD.copy();bad[10]="22: dmul"
        self.assertEqual("NOT_PROVED",interpret(bad,SOMAKE_GETTER_DESC)["status"])

    def test_bad_branch_target_refused(self):
        bad=[x.replace("ifnonnull 10","ifnonnull 999") for x in GOOD]
        self.assertEqual("NOT_PROVED",interpret(bad,SOMAKE_GETTER_DESC)["status"])

    def test_exact_release_path_snapshot_accepts_both_original_chains(self):
        paths=[{"condition":condition,**attrs}
               for condition,attrs in EXPECTED_EXACT_109_RADIUS_PATHS.items()]
        certify_exact_109({"status":"PROVED_TWO_PATH_JVM_FLOAT_EXPRESSION",
                           "jvm_instructions":28,"paths":paths})

    def test_exact_release_rejects_level_coefficient_drift(self):
        paths=[{"condition":condition,**attrs}
               for condition,attrs in EXPECTED_EXACT_109_RADIUS_PATHS.items()]
        paths[0]["jvm_float_expression"]=paths[0]["jvm_float_expression"].replace("0.82","0.83")
        with self.assertRaises(Exception):
            certify_exact_109({"status":"PROVED_TWO_PATH_JVM_FLOAT_EXPRESSION",
                               "jvm_instructions":28,"paths":paths})

    def test_exact_release_rejects_lost_school_dependency(self):
        paths=[{"condition":condition,**attrs}
               for condition,attrs in EXPECTED_EXACT_109_RADIUS_PATHS.items()]
        paths[0]["calls"]=["Math.max","Mth.clamp"]
        with self.assertRaises(Exception):
            certify_exact_109({"status":"PROVED_TWO_PATH_JVM_FLOAT_EXPRESSION",
                               "jvm_instructions":28,"paths":paths})

    def test_exact_release_rejects_ambiguous_branch_identity(self):
        paths=[{"condition":"caster == null",**attrs}
               for attrs in EXPECTED_EXACT_109_RADIUS_PATHS.values()]
        with self.assertRaises(Exception):
            certify_exact_109({"status":"PROVED_TWO_PATH_JVM_FLOAT_EXPRESSION",
                               "jvm_instructions":28,"paths":paths})

    def test_java21_compiled_branch_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/"RadiusFixture.java").write_text(
                "public class RadiusFixture {"
                "public float radius(Object caster) {"
                "float v; if (caster == null) { v=1.0f; } else { v=2.0f; }"
                "return Math.max(v,3.0f);"
                "}}\n")
            build=subprocess.run(["javac",str(p/"RadiusFixture.java")],
                                  capture_output=True,text=True)
            self.assertEqual(0,build.returncode,build.stderr)
            scan=subprocess.run(["javap","-p","-s","-c","-classpath",str(p),"RadiusFixture"],
                                capture_output=True,text=True)
            self.assertEqual(0,scan.returncode,scan.stderr)
            raw=scan.stdout.split("public float radius(")[1].split("}",1)[0]
            rows=opcode_rows(raw.splitlines())
            self.assertGreater(len(rows),4)
            proof=radius_cfg(raw.splitlines())
            self.assertEqual(1,proof["conditional_branches"])
            self.assertEqual(0,proof["back_edges"])

if __name__=="__main__":
    unittest.main()
