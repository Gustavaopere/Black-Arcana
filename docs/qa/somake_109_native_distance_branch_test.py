#!/usr/bin/env python3
"""Original synthetic fixtures for the Somake distance branch clean-room probe."""
import unittest
from somake_109_native_distance_branch import arithmetic_window, method_kind

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
    put(22,"aload_0")
    put(23,"invokevirtual #2", "Method net/minecraft/world/entity/Entity.getY:()D")
    put(24,"aload_0")
    put(25,"invokevirtual #3", "Method net/minecraft/world/entity/Entity.getZ:()D")
    put(26,"invokevirtual #4", DIST)
    put(27,"aload_0")
    put(28,"invokevirtual #5", RADIUS)
    put(29,"f2d")
    put(30,"dup2")
    put(31,"dmul")
    put(32,"dcmpg")
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
        self.assertEqual("cmp(distSq(slot2,x(slot0),y(slot0),z(slot0)),(R*R)) > 0",
                         r["derived_rejection_condition"])
        self.assertEqual(["x","y","z","distance","radius"],r["call_categories"])
        self.assertEqual(39,r["false_return_index"])
    def test_unknown_call_never_certifies_formula(self):
        d=fixture()
        rows=d[0][2]
        rows[26]=rows[26].replace("LivingEntity.distanceToSqr","other.Entity.distanceToSqr")
        self.assertEqual("NOT_PROVED",arithmetic_window(d)["status"])
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
        d[0][2][31]="31: invokestatic #8 // Method com/example/Math.multiply:(DD)D"
        self.assertEqual("NOT_PROVED",arithmetic_window(d)["status"])
    def test_wrong_receiver_kept_visible_for_release_gate(self):
        d=fixture()
        d[0][2][27]="27: aload_1"
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
