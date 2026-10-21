#!/usr/bin/env python3
"""Synthetic original wave-cardinality scanner regressions."""
import unittest
from somake_109_wave_maxtargets import wave_cardinality_scout
D="(Lnet/minecraft/server/level/ServerLevel;)V"
def sample():
    x=[f"{i}: nop" for i in range(196)]
    x[21]="21: getfield #1 // Field maxTargets:I"
    x[31]="31: ifeq 48"
    x[78]="78: getfield #1 // Field maxTargets:I"
    x[128]='128: invokespecial #5 // Method com/somake/somakespells/entity/FuneralBloomBudEntity."<init>":()V'
    x[159]="159: ifne 180"
    x[185]="185: goto 31"
    return [("launchWave",D,x)]
class WaveCardinalityScoutTests(unittest.TestCase):
    def test_structural_inventory_does_not_claim_cap(self):
        p=wave_cardinality_scout(sample())
        self.assertEqual("OBSERVED_WAVE_BRANCH_AND_MAXTARGETS_CALLSITES_ONLY",p["status"],p)
        self.assertEqual([21,78],p["max_targets_field_read_indices"])
        self.assertEqual([128],p["bud_constructor_indices"])
        self.assertEqual(3,len(p["branch_map"]))
        self.assertTrue(p["boundary"].startswith("No target-count cap"))
        self.assertNotIn("cap_enforced",p)
        self.assertNotIn("spawn_count",p)
    def test_wrong_member_not_proved(self):
        self.assertEqual("NOT_PROVED",wave_cardinality_scout([("launchWave","()V",sample()[0][2])])["status"])
    def test_ambiguous_member_not_proved(self):
        self.assertEqual("NOT_PROVED",wave_cardinality_scout(sample()*2)["status"])
    def test_changed_reads_not_proved(self):
        a=sample();a[0][2][78]="78: nop"
        self.assertEqual("NOT_PROVED",wave_cardinality_scout(a)["status"])
    def test_missing_bud_not_proved(self):
        a=sample();a[0][2][128]="128: nop"
        self.assertEqual("NOT_PROVED",wave_cardinality_scout(a)["status"])
    def test_invalid_branch_target_not_proved(self):
        a=sample();a[0][2][185]="185: goto 999"
        self.assertEqual("NOT_PROVED",wave_cardinality_scout(a)["status"])
if __name__=="__main__":
    unittest.main()
