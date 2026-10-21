#!/usr/bin/env python3
"""Synthetic constructor/wave topology regressions (no publisher body)."""
import unittest
from somake_109_bud_wither_construction import ctor_scout
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
if __name__=="__main__":
    unittest.main()
