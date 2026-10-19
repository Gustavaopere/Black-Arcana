#!/usr/bin/env python3
"""Synthetic and Java21 positive/negative tests for exact float dataflow audit."""
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from somake_109_perk_method_probe import GateError
from somake_109_float_dataflow import decode_descriptor, float_formula, selected_methods, TARGETS, certify_exact_release, EXACT_DAMAGE_EXPRESSION
from somake_109_numeric_fingerprint import CODE

SAMPLE = """public class FuneralBloomSpell {
  public FuneralBloomSpell();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokespecial #1 // Method java/lang/Object."<init>":()V
       4: return
  public float getImpactDamage(int, net.minecraft.world.entity.LivingEntity);
    descriptor: (ILnet/minecraft/world/entity/LivingEntity;)F
    Code:
       0: aload_0
       1: iload_1
       2: aload_2
       3: invokevirtual #4 // Method abstract/AbstractSpell.getSpellPower:(ILnet/minecraft/world/entity/LivingEntity;)F
       6: ldc #7 // float 0.75f
       8: fmul
       9: ldc #9 // float 1.5f
      11: fadd
      12: freturn
  public float getRadius(int, net.minecraft.world.entity.LivingEntity);
    descriptor: (ILnet/minecraft/world/entity/LivingEntity;)F
    Code:
       0: iload_1
       1: ifeq 10
       4: ldc #9 // float 10.0f
       6: freturn
      10: ldc #10 // float 15.0f
      12: freturn
}
"""

def body_of(sample:str,name:str)->list[str]:
    lines=sample.splitlines()
    match=[i for i,line in enumerate(lines) if re.search(r"^\s+public float "+name+r"\(",line)]
    assert len(match)==1
    start=match[0]+1
    end=next((i for i in range(start,len(lines)) if lines[i].startswith("  public ") or lines[i]=="}"),len(lines))
    return lines[start:end]

class FloatDataflowTests(unittest.TestCase):
    def test_full_symbolic_proof(self):
        rows=selected_methods(SAMPLE)
        d=rows["getImpactDamage"]["symbolic_dataflow"]
        self.assertEqual("PROVED_STRAIGHT_LINE_JVM_FLOAT_EXPRESSION",d["status"])
        self.assertEqual("((spellPower(level_input,caster)*0.75)+1.5)",d["expression"])
        self.assertEqual(["getSpellPower"],d["external_calls"])

    def test_radius_branches_fail_closed(self):
        rows=selected_methods(SAMPLE)
        self.assertEqual("NOT_PROVED",rows["getRadius"]["symbolic_dataflow"]["status"])
        self.assertEqual("branch_or_throw",rows["getRadius"]["symbolic_dataflow"]["reason"])

    def test_unlisted_invocation_is_not_interpreted(self):
        bad=SAMPLE.replace(".getSpellPower:",".getSpellMagic:")
        rows=selected_methods(bad)
        self.assertEqual("NOT_PROVED",rows["getImpactDamage"]["symbolic_dataflow"]["status"])
        self.assertEqual("unsupported_invocation",rows["getImpactDamage"]["symbolic_dataflow"]["reason"])

    def test_missing_or_wrong_signature_fails(self):
        with self.assertRaises(GateError):
            selected_methods(SAMPLE.replace("descriptor: (ILnet/minecraft/world/entity/LivingEntity;)F",
                                            "descriptor: (I)F",1))

    def test_int_float_stack_mismatch_is_fail_closed(self):
        bad=SAMPLE.replace("       8: fmul","       8: iadd")
        self.assertEqual("NOT_PROVED",selected_methods(bad)["getImpactDamage"]["symbolic_dataflow"]["status"])

    def test_duplicate_method_identity_fails(self):
        extra=SAMPLE.replace("}\n",SAMPLE[SAMPLE.index("  public float getImpactDamage"):SAMPLE.index("  public float getRadius")]+"}\n")
        with self.assertRaises(GateError):
            selected_methods(extra)

    def test_descriptor_decoder_object_primitive_arrays(self):
        args,out=decode_descriptor("(ILjava/lang/Object;[FF)F")
        self.assertEqual(["I","R","R","F"],args)
        self.assertEqual("F",out)

    def test_wrong_spellpower_return_type_fails(self):
        bad=SAMPLE.replace("getSpellPower:(ILnet/minecraft/world/entity/LivingEntity;)F",
                           "getSpellPower:(ILnet/minecraft/world/entity/LivingEntity;)I")
        self.assertEqual("NOT_PROVED",selected_methods(bad)["getImpactDamage"]["symbolic_dataflow"]["status"])

    def test_static_initializer_discarded(self):
        marker="}\n"
        stat="""  static {};
    Code:
       0: invokestatic #5 // Method evil/Runtime.mutate:()V
       3: return
}
"""
        rows=selected_methods(SAMPLE.replace(marker,stat))
        self.assertEqual("PROVED_STRAIGHT_LINE_JVM_FLOAT_EXPRESSION",
                         rows["getImpactDamage"]["symbolic_dataflow"]["status"])

    def test_exact_release_requires_verified_expression_and_radius_pair(self):
        rows=selected_methods(SAMPLE)
        rows["getImpactDamage"]["symbolic_dataflow"]["expression"]=EXACT_DAMAGE_EXPRESSION
        rows["getRadius"]["direct_trailing_clamp_literals"]=[{
            "descriptor":"(FFF)F","second_argument_literal":"10.0",
            "third_argument_literal":"15.0"}]
        certify_exact_release(rows)
        rows["getRadius"]["direct_trailing_clamp_literals"][0]["third_argument_literal"]="16.0"
        with self.assertRaises(GateError):
            certify_exact_release(rows)

    def test_exact_release_refuses_formula_drift(self):
        rows=selected_methods(SAMPLE)
        rows["getImpactDamage"]["symbolic_dataflow"]["expression"]="(1.5+(spellPower(level_input,caster)*0.75))"
        rows["getRadius"]["direct_trailing_clamp_literals"]=[{
            "descriptor":"(FFF)F","second_argument_literal":"10.0",
            "third_argument_literal":"15.0"}]
        certify_exact_release(rows)
        rows["getImpactDamage"]["symbolic_dataflow"]["expression"]="(spellPower(level_input,caster)*0.75)"
        with self.assertRaises(GateError):
            certify_exact_release(rows)

    def test_real_java21_compiler_fixture(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"Probe.java").write_text(
                "public class Probe {"
                "public float getSpellPower(int level,Object caster){return 4.0f;}"
                "public float getImpactDamage(int level,Object caster){return getSpellPower(level,caster)*0.75f+1.5f;}"
                "}\n")
            comp=subprocess.run(["javac",str(root/"Probe.java")],capture_output=True,text=True)
            self.assertEqual(0,comp.returncode,comp.stderr)
            output=subprocess.run(["javap","-c","-s","-p","-classpath",str(root),"Probe"],
                                  capture_output=True,text=True)
            self.assertEqual(0,output.returncode,output.stderr)
            parsed=body_of(output.stdout,"getImpactDamage")
            d=float_formula(parsed,TARGETS["getImpactDamage"])
            self.assertEqual("PROVED_STRAIGHT_LINE_JVM_FLOAT_EXPRESSION",d["status"],d)
            self.assertIn("spellPower(level_input,caster)",d["expression"])

if __name__=="__main__":
    unittest.main()
