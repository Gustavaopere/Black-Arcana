#!/usr/bin/env python3
"""Synthetic constructor/wave topology regressions (no publisher body)."""
import unittest
from somake_109_bud_wither_construction import ctor_scout,certify_wither_constructor_handoff,certify_exact_wither_handoff_109,CTOR_BASE_DESC,CTOR_WAVE_DESC
from somake_109_perk_method_probe import GateError
BUD_DESC="(Lnet/minecraft/world/level/Level;)V"
WAVE_DESC="(Lnet/minecraft/server/level/ServerLevel;)V"
def fixture():
    b=["%d: nop"%i for i in range(30)]
    b[12]="12: aload_0"
    b[13]="13: iload_2"
    b[14]="14: putfield #3 // Field witherDuration:I"
    b[16]="16: putfield #4 // Field witherAmplifier:I"
    w=["%d: nop"%i for i in range(196)]
    w[93]='93: invokespecial #12 // Method com/somake/somakespells/entity/FuneralBloomBudEntity."<init>":(Lnet/minecraft/world/level/Level;)V'
    return [("com.somake.somakespells.entity.FuneralBloomBudEntity",BUD_DESC,b)], [("launchWave",WAVE_DESC,w)]
class ConstructorScoutTests(unittest.TestCase):
    def test_observational_only(self):
        p=ctor_scout(*fixture())
        self.assertEqual("OBSERVED_CONSTRUCTOR_AND_WAVE_ARGUMENT_WINDOWS_ONLY",p["status"])
        self.assertEqual(93,p["wave_bud_ctor_index"])
        self.assertEqual(1,p["constructor_count"])
        self.assertIn("No assignment chain",p["boundary"])
        self.assertNotIn("certified_wither_formula",p)
    def test_wrong_descriptor_not_promoted(self):
        b,w=fixture()
        self.assertEqual("NOT_PROVED",ctor_scout(b,[("launchWave","()V",w[0][2])])["status"])
    def test_bad_native_site_fails(self):
        b,w=fixture();w[0][2][93]="93: nop"
        self.assertEqual("NOT_PROVED",ctor_scout(b,w)["status"])
    def test_ambiguous_wave_fails(self):
        b,w=fixture()
        self.assertEqual("NOT_PROVED",ctor_scout(b,w+w)["status"])
    def test_missing_constructor_fails(self):
        b,w=fixture()
        self.assertEqual("NOT_PROVED",ctor_scout([],w)["status"])
    def test_excessive_bud_ctor_fails(self):
        b,w=fixture()
        self.assertEqual("NOT_PROVED",ctor_scout(b*7,w)["status"])

def causal_fixture():
    basic=[f"{i}: nop" for i in range(17)]
    for i,v in {
        4:"aload_0",5:"bipush 80",6:"putfield #3 // Field witherDuration:I",
    }.items():basic[i]=f"{i}: {v}"
    expanded=[f"{i}: nop" for i in range(41)]
    changes={
        27:"aload_0",28:"fload 6",29:"putfield #4 // Field impactDamage:F",
        30:"aload_0",31:"bipush 30",32:"iload 7",
        33:"invokestatic #5 // Method java/lang/Math.max:(II)I",
        34:"putfield #6 // Field witherDuration:I",
        35:"aload_0",36:"iconst_0",37:"iload 8",
        38:"invokestatic #5 // Method java/lang/Math.max:(II)I",
        39:"putfield #7 // Field witherAmplifier:I",
    }
    for i,v in changes.items():expanded[i]=f"{i}: {v}"
    wave=[f"{i}: nop" for i in range(196)]
    changes={
        79:"new #8 // class com/somake/somakespells/entity/FuneralBloomBudEntity",
        80:"dup",81:"aload_1",82:"aload_0",83:"aload 7",84:"aload 8",
        85:"fload 9",86:"invokestatic #9 // Method net/minecraft/util/Mth.ceil:(F)I",
        87:"aload_0",88:"getfield #10 // Field impactDamage:F",
        89:"aload_0",90:"getfield #11 // Field witherDuration:I",
        91:"aload_0",92:"getfield #12 // Field witherAmplifier:I",
        93:'invokespecial #13 // Method com/somake/somakespells/entity/FuneralBloomBudEntity."<init>":'+CTOR_WAVE_DESC,
    }
    for i,v in changes.items():wave[i]=f"{i}: {v}"
    return (
        [("com.somake.somakespells.entity.FuneralBloomBudEntity",CTOR_BASE_DESC,basic),
         ("com.somake.somakespells.entity.FuneralBloomBudEntity",CTOR_WAVE_DESC,expanded)],
        [("launchWave",WAVE_DESC,wave)],
    )
class CertifiedHandoffTests(unittest.TestCase):
    def test_two_constructors_and_native_argument_order(self):
        p=certify_wither_constructor_handoff(*causal_fixture())
        self.assertEqual("PROVED_CONSTRUCTION_TIME_BUD_WITHER_CLAMPS_FROM_CONTROLLER_FIELDS",p["status"],p)
        self.assertEqual(80,p["base_default_wither_duration"])
        self.assertEqual("Math.max_int(30,input_int_slot7)",p["bud_wither_duration"])
        self.assertEqual("Math.max_int(0,input_int_slot8)",p["bud_wither_amplifier"])
        certify_exact_wither_handoff_109(p)
    def test_constructor_duration_floor_mutation_fails(self):
        a,b=causal_fixture()
        a[1][2][31]="31: bipush 20"
        self.assertEqual("NOT_PROVED",certify_wither_constructor_handoff(a,b)["status"])
    def test_wither_amplifier_argument_slot_mutation_fails(self):
        a,b=causal_fixture()
        a[1][2][37]="37: iload 7"
        self.assertEqual("NOT_PROVED",certify_wither_constructor_handoff(a,b)["status"])
    def test_controller_source_field_swapped_fails(self):
        a,b=causal_fixture()
        b[0][2][90]="90: getfield #11 // Field witherAmplifier:I"
        self.assertEqual("NOT_PROVED",certify_wither_constructor_handoff(a,b)["status"])
    def test_wrong_wave_ctor_descriptor_fails(self):
        a,b=causal_fixture()
        b[0][2][93]=b[0][2][93].replace("IFII)V","IFIF)V")
        self.assertEqual("NOT_PROVED",certify_wither_constructor_handoff(a,b)["status"])
    def test_wrong_initial_wither_default_fails(self):
        a,b=causal_fixture()
        a[0][2][5]="5: bipush 60"
        self.assertEqual("NOT_PROVED",certify_wither_constructor_handoff(a,b)["status"])
    def test_duplicate_native_constructors_fail(self):
        a,b=causal_fixture()
        self.assertEqual("NOT_PROVED",certify_wither_constructor_handoff(a+a,b)["status"])
    def test_snapshot_fails_on_mutation_authorization(self):
        proof=certify_wither_constructor_handoff(*causal_fixture())
        with self.assertRaises(GateError):
            certify_exact_wither_handoff_109(dict(proof,boundary="new per-player setter approved"))
        with self.assertRaises(GateError):
            certify_exact_wither_handoff_109(None)

if __name__=="__main__":
    unittest.main()
