#!/usr/bin/env python3
"""Synthetic RED/GREEN tests for exact-version native mid-filter guard model."""
import unittest
from somake_109_native_filter_middle import middle_guard, certify_exact_native_middle_109
from somake_109_perk_method_probe import GateError

D="(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z"
ALLY="Method net/minecraft/world/entity/LivingEntity.isAlliedTo:(Lnet/minecraft/world/entity/Entity;)Z"

def sample():
    # Synthetic and original fixture, not derived from or a copy of vendor code.
    rows=[f"{i}: nop" for i in range(41)]
    rows[8]="8: if_acmpne 11"
    rows[11]="11: aload_1"
    rows[12]="12: ifnull 19"
    rows[13]="13: aload_2"
    rows[14]="14: aload_1"
    rows[15]="15: invokevirtual #12 // "+ALLY
    rows[16]="16: ifeq 19"
    rows[17]="17: iconst_0"
    rows[18]="18: ireturn"
    return [("isValidTarget",D,rows)]

class MiddleGuardTests(unittest.TestCase):
    def test_nonnull_and_allied_combination_is_direct_rejection_only(self):
        p=middle_guard(sample())
        self.assertEqual("PROVED_NATIVE_NONNULL_AND_ALLIED_REJECTS",p["status"],p)
        self.assertEqual((1,2,1),(p["null_test_operand_local"],p["allied_receiver_local"],p["allied_argument_local"]))
        self.assertIs(p["rejection_value"],False)
        self.assertNotIn("caster_role",p)

    def test_exact_publisher_guard_snapshot_and_negative_mutations(self):
        certified=middle_guard(sample())
        certify_exact_native_middle_109(certified)
        for mutation in (
            {"null_test_operand_local":2},
            {"allied_receiver_local":1},
            {"allied_argument_local":2},
            {"instruction_count":40},
            {"status":"NOT_PROVED"},
            {"skip_false_return_branches":["ifnull","ifne"]},
            {"shared_continuation_index":18},
            {"rejection_value":True},
            {"boundary":"all_players_can_mutate_targeting"},
        ):
            with self.subTest(mutation=mutation):
                with self.assertRaises(GateError):
                    certify_exact_native_middle_109(dict(certified,**mutation))
        with self.assertRaises(GateError):
            certify_exact_native_middle_109(None)

    def test_different_jvm_slot_mapping_cannot_be_promoted_for_this_release(self):
        t=sample()
        t[0][2][13]="13: aload_1"
        inferred=middle_guard(t)
        self.assertEqual("PROVED_NATIVE_NONNULL_AND_ALLIED_REJECTS",inferred["status"])
        with self.assertRaises(GateError):
            certify_exact_native_middle_109(inferred)

    def test_alliance_call_altered_or_removed_fails_closed(self):
        t=sample();t[0][2][15]="15: invokevirtual #12 // Method x/y/Mock.isAlliedTo:(Lnet/minecraft/world/entity/Entity;)Z"
        self.assertEqual("NOT_PROVED",middle_guard(t)["status"])
    def test_branch_reversed_fails_closed(self):
        t=sample();t[0][2][16]="16: ifne 19"
        self.assertEqual("NOT_PROVED",middle_guard(t)["status"])
    def test_branch_target_mismatch_fails_closed(self):
        t=sample();t[0][2][12]="12: ifnull 20"
        self.assertEqual("NOT_PROVED",middle_guard(t)["status"])
    def test_no_hardcoded_actor_roles(self):
        t=sample();t[0][2][11]="11: aload_2"
        p=middle_guard(t)
        self.assertEqual("PROVED_NATIVE_NONNULL_AND_ALLIED_REJECTS",p["status"],p)
        self.assertEqual(2,p["null_test_operand_local"])
    def test_ambiguous_member_and_oversized_member_fail_closed(self):
        self.assertEqual("NOT_PROVED",middle_guard(sample()*2)["status"])
        t=sample();t[0][2].append("41: nop")
        self.assertEqual("NOT_PROVED",middle_guard(t)["status"])
    def test_unsupported_ingress_fails_closed(self):
        t=sample();t[0][2][5]="5: goto 15"
        self.assertEqual("NOT_PROVED",middle_guard(t)["status"])
if __name__=="__main__":
    unittest.main()
