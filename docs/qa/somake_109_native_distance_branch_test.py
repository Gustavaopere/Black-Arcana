#!/usr/bin/env python3
"""Original synthetic fixtures for the Somake distance branch clean-room probe."""
import unittest
from somake_109_native_distance_branch import arithmetic_window, method_kind, certify_exact_final_distance_109
from somake_109_perk_method_probe import GateError

DESC="(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z"
DIST="Method net/minecraft/world/entity/LivingEntity.distanceToSqr:(DDD)D"
RADIUS="Method getRadius:()F"
def fixture():
    rows=[f"{i}: nop" for i in range(41)]
    def put(i,op,comment=""):
        rows[i]=f"{i}: {op}"+(f" // {comment}" if comment else "")
    put(19,"aload_2")
    put(20,"aload_0")
    put(21,"invokevirtual #1", "Method net/minecraft/world/entity/Entity.getX:()D")
    put(22,"aload_2")
    put(23,"invokevirtual #2", "Method net/minecraft/world/entity/Entity.getY:()D")
    put(24,"aload_0")
    put(25,"invokevirtual #3", "Method net/minecraft/world/entity/Entity.getZ:()D")
    put(26,"invokevirtual #4", DIST)
    put(27,"dstore_3")
    put(28,"dload_3")
    put(29,"aload_0")
    put(30,"invokevirtual #5", RADIUS)
    put(31,"aload_0")
    put(32,"invokevirtual #6", RADIUS)
    put(33,"fmul")
    put(34,"f2d")
    put(35,"dcmpg")
    put(36,"ifgt 39")
    put(37,"iconst_1")
    put(38,"ireturn")
    put(39,"iconst_0")
    put(40,"ireturn")
    return [("isValidTarget",DESC,rows)]

class FinalDistanceTest(unittest.TestCase):
    def test_synthetic_sq_distance_to_radius_rejection(self):
        r=arithmetic_window(fixture())
        self.assertEqual("PROVED_FINAL_IFGT_NUMERIC_COMPARISON",r["status"],r)
        self.assertEqual("cmp(distSq(slot2,x(slot0),y(slot2),z(slot0)),(R*R)) > 0",
                         r["derived_rejection_condition"])
        self.assertEqual(["x","y","z","distance","radius","radius"],r["call_categories"])
        self.assertEqual(39,r["false_return_index"])
    def test_physical_release_fingerprint_guard_rejects_every_relevant_drift(self):
        baseline=arithmetic_window(fixture())
        certify_exact_final_distance_109(baseline)
        for delta in (
            {"status":"NOT_PROVED"},
            {"window_instruction_count":17},
            {"derived_rejection_condition":"cmp(distSq(slot2,x(slot0),y(slot0),z(slot0)),(R*R)) > 0"},
            {"comparison_semantics":"unknown"},
            {"last_conditional_index":35},
            {"false_return_index":38},
            {"call_categories":["distance","x","y","z","radius","radius"]},
            {"call_positions":[]},
            {"opcode_histogram":{}},
            {"math_opcode_histogram":{"dmul":1}},
            {"boundary":"PERK_MUTATOR_APPROVED"},
        ):
            with self.subTest(delta=delta):
                with self.assertRaises(GateError):
                    certify_exact_final_distance_109(dict(baseline,**delta))
        with self.assertRaises(GateError):
            certify_exact_final_distance_109(None)
    def test_jvm_nan_and_float_rounding_are_not_overclaimed(self):
        proof=arithmetic_window(fixture())
        self.assertIn("cmp(",proof["derived_rejection_condition"])
        self.assertEqual(1,proof["math_opcode_histogram"]["fmul"])
        self.assertEqual(1,proof["math_opcode_histogram"]["f2d"])
        self.assertEqual(1,proof["math_opcode_histogram"]["dcmpg"])
    def test_wrong_height_operand_is_rejected_by_release_gate(self):
        d=fixture()
        d[0][2][22]="22: aload_0"
        p=arithmetic_window(d)
        self.assertEqual("PROVED_FINAL_IFGT_NUMERIC_COMPARISON",p["status"])
        with self.assertRaises(GateError):
            certify_exact_final_distance_109(p)

    def test_unknown_call_never_certifies_formula(self):
        d=fixture()
        rows=d[0][2]
        rows[26]=rows[26].replace("LivingEntity.distanceToSqr","other.Entity.distanceToSqr")
        self.assertEqual("NOT_PROVED",arithmetic_window(d)["status"])
    def test_saved_distance_double_slot_must_be_defined(self):
        d=fixture()
        d[0][2][27]="27: nop"
        self.assertEqual("NOT_PROVED",arithmetic_window(d)["status"])
    def test_saved_double_local_must_not_be_reassigned(self):
        d=fixture()
        d[0][2][28]="28: dstore_3"
        self.assertEqual("NOT_PROVED",arithmetic_window(d)["status"])
    def test_wrong_height_reference_changes_expression(self):
        d=fixture()
        d[0][2][22]="22: aload_0"
        actual=arithmetic_window(d)
        self.assertEqual("PROVED_FINAL_IFGT_NUMERIC_COMPARISON",actual["status"])
        self.assertIn("y(slot0)",actual["derived_rejection_condition"])
    def test_branch_to_true_is_rejected(self):
        d=fixture()
        d[0][2][36]="36: ifgt 37"
        self.assertEqual("NOT_PROVED",arithmetic_window(d)["status"])
    def test_failure_on_target_without_direct_false_return(self):
        d=fixture()
        d[0][2][39]="39: iconst_1"
        self.assertEqual("NOT_PROVED",arithmetic_window(d)["status"])
    def test_unmodeled_math_is_never_promoted(self):
        d=fixture()
        d[0][2][33]="33: invokestatic #8 // Method com/example/Math.multiply:(FF)F"
        self.assertEqual("NOT_PROVED",arithmetic_window(d)["status"])
    def test_wrong_receiver_kept_visible_for_release_gate(self):
        d=fixture()
        d[0][2][29]="29: aload_1"
        self.assertEqual("NOT_PROVED",arithmetic_window(d)["status"])
    def test_ambiguous_native_member_rejected(self):
        d=fixture()
        self.assertEqual("NOT_PROVED",arithmetic_window(d+d)["status"])
    def test_scope_does_not_infer_player_role_or_perk_api(self):
        r=arithmetic_window(fixture())
        self.assertNotIn("owner_is",str(r))
        self.assertIn("No actual player roles",r["boundary"])
    def test_call_classifier_is_constrained_to_exact_descriptor(self):
        self.assertEqual("distance",method_kind(DIST))
        self.assertIsNone(method_kind("Method net/minecraft/world/entity/Entity.distanceToSqr:(Lnet/minecraft/world/entity/Entity;)D"))

if __name__=="__main__":
    unittest.main()
