#!/usr/bin/env python3
"""Synthetic original wave-cardinality scanner regressions."""
import unittest
from somake_109_wave_maxtargets import wave_cardinality_scout, prove_wave_list_cap
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

def cap_fixture():
    """Independent synthetic arithmetic and list-slot flow, not vendor instructions."""
    x=[f"{i}: nop" for i in range(196)]
    x[40]="40: aload 2"
    x[41]="41: invokeinterface #3, 1 // InterfaceMethod java/util/List.size:()I"
    x[42]="42: aload_0"
    x[43]="43: getfield #1 // Field maxTargets:I"
    x[44]="44: if_icmple 51"
    x[45]="45: aload 2"
    x[46]="46: iconst_0"
    x[47]="47: aload_0"
    x[48]="48: getfield #1 // Field maxTargets:I"
    x[49]="49: invokeinterface #4, 3 // InterfaceMethod java/util/List.subList:(II)Ljava/util/List;"
    x[50]="50: astore 2"
    x[51]="51: iconst_0"
    x[53]="53: aload 2"
    x[54]="54: invokeinterface #5, 1 // InterfaceMethod java/util/List.iterator:()Ljava/util/Iterator;"
    return [("launchWave",D,x)]

class WaveCapOperandTests(unittest.TestCase):
    def test_cap_proof_requires_exact_list_size_branch_and_sublist(self):
        proof=prove_wave_list_cap(cap_fixture())
        self.assertEqual("PROVED_WAVE_CANDIDATE_LIST_TRUNCATION",proof["status"],proof)
        self.assertEqual("list_size_greater_than_maxTargets",proof["truncation_condition"])
        self.assertEqual(2,proof["list_local"])
        self.assertEqual(51,proof["branch_skip_index"])
        self.assertIn("not bud count",proof["boundary"])
    def test_inverse_branch_rejected(self):
        d=cap_fixture();d[0][2][44]="44: if_icmpgt 51"
        self.assertEqual("NOT_PROVED",prove_wave_list_cap(d)["status"])
    def test_wrong_sublist_bounds_rejected(self):
        d=cap_fixture();d[0][2][46]="46: iconst_1"
        self.assertEqual("NOT_PROVED",prove_wave_list_cap(d)["status"])
    def test_wrong_max_targets_operand_rejected(self):
        d=cap_fixture();d[0][2][48]="48: getfield #8 // Field otherLimit:I"
        self.assertEqual("NOT_PROVED",prove_wave_list_cap(d)["status"])
    def test_list_slot_reassignment_rejected(self):
        d=cap_fixture();d[0][2][50]="50: astore 3"
        self.assertEqual("NOT_PROVED",prove_wave_list_cap(d)["status"])
    def test_wrong_iterator_source_rejected(self):
        d=cap_fixture();d[0][2][53]="53: aload 3"
        self.assertEqual("NOT_PROVED",prove_wave_list_cap(d)["status"])
    def test_external_jump_into_sublist_rejected(self):
        d=cap_fixture();d[0][2][18]="18: goto 46"
        self.assertEqual("NOT_PROVED",prove_wave_list_cap(d)["status"])

if __name__=="__main__":
    unittest.main()
