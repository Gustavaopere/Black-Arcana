#!/usr/bin/env python3
"""Synthetic original wave-cardinality scanner regressions."""
import unittest
from somake_109_perk_method_probe import GateError
from somake_109_wave_maxtargets import wave_cardinality_scout, prove_wave_list_cap, prove_wave_loop_spawn_sites, certify_exact_wave_list_cap_109, certify_exact_wave_loop_109
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
    x[40]="40: aload 4"
    x[41]="41: invokeinterface #3, 1 // InterfaceMethod java/util/List.size:()I"
    x[42]="42: aload_0"
    x[43]="43: getfield #1 // Field maxTargets:I"
    x[44]="44: if_icmple 51"
    x[45]="45: aload 4"
    x[46]="46: iconst_0"
    x[47]="47: aload_0"
    x[48]="48: getfield #1 // Field maxTargets:I"
    x[49]="49: invokeinterface #4, 3 // InterfaceMethod java/util/List.subList:(II)Ljava/util/List;"
    x[50]="50: astore 4"
    x[51]="51: iconst_0"
    x[53]="53: aload 4"
    x[54]="54: invokeinterface #5, 1 // InterfaceMethod java/util/List.iterator:()Ljava/util/Iterator;"
    return [("launchWave",D,x)]

class WaveCapOperandTests(unittest.TestCase):
    def test_cap_proof_requires_exact_list_size_branch_and_sublist(self):
        proof=prove_wave_list_cap(cap_fixture())
        self.assertEqual("PROVED_WAVE_CANDIDATE_LIST_TRUNCATION",proof["status"],proof)
        self.assertEqual("list_size_greater_than_maxTargets",proof["truncation_condition"])
        self.assertEqual(4,proof["list_local"])
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
        d=cap_fixture();d[0][2][50]="50: astore 2"
        self.assertEqual("NOT_PROVED",prove_wave_list_cap(d)["status"])
    def test_wrong_iterator_source_rejected(self):
        d=cap_fixture();d[0][2][53]="53: aload 2"
        self.assertEqual("NOT_PROVED",prove_wave_list_cap(d)["status"])
    def test_external_jump_into_sublist_rejected(self):
        d=cap_fixture();d[0][2][18]="18: goto 46"
        self.assertEqual("NOT_PROVED",prove_wave_list_cap(d)["status"])


def loop_fixture():
    row=cap_fixture()[0][2]
    row[55]="55: astore 6"
    row[56]="56: aload 6"
    row[57]="57: invokeinterface #1, 1 // InterfaceMethod java/util/Iterator.hasNext:()Z"
    row[58]="58: ifeq 166"
    row[59]="59: aload 6"
    row[60]="60: invokeinterface #2, 1 // InterfaceMethod java/util/Iterator.next:()Ljava/lang/Object;"
    row[93]='93: invokespecial #3 // Method com/somake/somakespells/entity/FuneralBloomBudEntity."<init>":()V'
    row[156]="156: invokevirtual #4 // Method net/minecraft/server/level/ServerLevel.addFreshEntity:(Lnet/minecraft/world/entity/Entity;)Z"
    row[157]="157: pop"
    row[159]="159: getfield #5 // Field activeTargetIds:Ljava/util/Set;"
    row[161]="161: invokevirtual #6 // Method net/minecraft/world/entity/LivingEntity.getUUID:()Ljava/util/UUID;"
    row[162]="162: invokeinterface #7, 2 // InterfaceMethod java/util/Set.add:(Ljava/lang/Object;)Z"
    row[163]="163: pop"
    row[164]="164: iinc 7, 1"
    row[165]="165: goto 56"
    return [("launchWave",D,row)]

class WaveNormalPathLoopTests(unittest.TestCase):
    def test_single_spawn_attempt_per_iteration_but_not_success(self):
        p=prove_wave_loop_spawn_sites(loop_fixture())
        self.assertEqual("PROVED_ONE_BUD_SPAWN_ATTEMPT_AND_UUID_SET_ADD_PER_NORMAL_ITERATION",p["status"],p)
        self.assertEqual(93,p["bud_constructor_index"])
        self.assertEqual(156,p["spawn_call_index"])
        self.assertTrue(p["spawn_boolean_result_discarded"])
        self.assertIn("not successful bud spawn",p["boundary"])
    def test_skip_over_spawn_inside_loop_fails(self):
        d=loop_fixture();d[0][2][104]="104: goto 160"
        self.assertEqual("NOT_PROVED",prove_wave_loop_spawn_sites(d)["status"])
    def test_missing_boolean_pop_fails(self):
        d=loop_fixture();d[0][2][157]="157: nop"
        self.assertEqual("NOT_PROVED",prove_wave_loop_spawn_sites(d)["status"])
    def test_uuid_add_drift_fails(self):
        d=loop_fixture();d[0][2][162]="162: invokeinterface #7, 2 // InterfaceMethod java/util/Set.contains:(Ljava/lang/Object;)Z"
        self.assertEqual("NOT_PROVED",prove_wave_loop_spawn_sites(d)["status"])
    def test_changed_iterator_receiver_fails(self):
        d=loop_fixture();d[0][2][59]="59: aload 4"
        self.assertEqual("NOT_PROVED",prove_wave_loop_spawn_sites(d)["status"])
    def test_wrong_loop_exit_fails(self):
        d=loop_fixture();d[0][2][58]="58: ifeq 160"
        self.assertEqual("NOT_PROVED",prove_wave_loop_spawn_sites(d)["status"])


class ExactPublisherReleaseGateTests(unittest.TestCase):
    def test_physical_candidate_slice_snapshot(self):
        proof=prove_wave_list_cap(cap_fixture())
        certify_exact_wave_list_cap_109(proof)
        for delta in (
            {"status":"NOT_PROVED"},{"list_local":2},{"conditional_index":43},
            {"truncation_condition":"size_smaller_than_maxTargets"},
            {"slice_start_literal":1},{"slice_upper_source":"list_size"},
            {"iterator_call_index":53},{"boundary":"all_perks_approved"},
        ):
            with self.subTest(delta=delta):
                with self.assertRaises(GateError):
                    certify_exact_wave_list_cap_109(dict(proof,**delta))
    def test_physical_loop_normal_path_snapshot(self):
        proof=prove_wave_loop_spawn_sites(loop_fixture())
        certify_exact_wave_loop_109(proof)
        for delta in (
            {"status":"NOT_PROVED"},{"loop_receiver_slot":5},
            {"bud_constructor_index":92},{"spawn_call_index":157},
            {"spawn_boolean_result_discarded":False},
            {"active_uuid_set_add_index":163},
            {"back_edge_index":164},
            {"boundary":"spawn guaranteed"},
        ):
            with self.subTest(delta=delta):
                with self.assertRaises(GateError):
                    certify_exact_wave_loop_109(dict(proof,**delta))
        with self.assertRaises(GateError):
            certify_exact_wave_loop_109(None)

if __name__=="__main__":
    unittest.main()
