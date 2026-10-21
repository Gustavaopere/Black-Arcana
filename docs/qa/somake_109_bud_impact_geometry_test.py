#!/usr/bin/env python3
"""Original synthetic shape tests for SHA-exact Somake bud impact scanner."""
import unittest
from somake_109_bud_impact_geometry import impact_scout, category, prove_impact_box_and_query

D="(Lnet/minecraft/server/level/ServerLevel;)V"
def specimen():
    rows=[f"{i}: nop" for i in range(279)]
    rows[30]="30: invokevirtual #1 // Method net/minecraft/world/entity/LivingEntity.getBoundingBox:()Lnet/minecraft/world/phys/AABB;"
    rows[40]="40: ldc2_w #2 // double 0.6d"
    rows[43]="43: invokevirtual #3 // Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;"
    rows[52]="52: invokevirtual #4 // Method net/minecraft/server/level/ServerLevel.getEntitiesOfClass:()Ljava/util/List;"
    rows[80]="80: ifeq 90"
    rows[105]="105: invokestatic #5 // Method io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:()Z"
    rows[200]="200: return"
    return [("impact",D,rows)]
class ShapeTests(unittest.TestCase):
    def test_original_fixture_observes_only(self):
        p=impact_scout(specimen())
        self.assertEqual("OBSERVED_BUD_IMPACT_TOPOLOGY_ONLY",p["status"],p)
        self.assertEqual([43],p["calls_by_category"]["aabb_inflate_DDD"])
        self.assertEqual([52],p["calls_by_category"]["query_living_entities"])
        self.assertEqual([105],p["calls_by_category"]["apply_damage"])
        self.assertIn("not proved",p["boundary"])
        self.assertNotIn("radius_proved",p)
    def test_ambiguous_method_fails_closed(self):
        self.assertEqual("NOT_PROVED",impact_scout(specimen()*2)["status"])
    def test_unknown_signature_fails_closed(self):
        rows=specimen()[0][2]
        self.assertEqual("NOT_PROVED",impact_scout([("impact","()V",rows)])["status"])
    def test_missing_inflate_fails_closed(self):
        x=specimen();x[0][2][43]="43: nop"
        self.assertEqual("NOT_PROVED",impact_scout(x)["status"])
    def test_missing_query_fails_closed(self):
        x=specimen();x[0][2][52]="52: nop"
        self.assertEqual("NOT_PROVED",impact_scout(x)["status"])
    def test_invalid_branch_target_fails_closed(self):
        x=specimen();x[0][2][80]="80: ifeq 999"
        self.assertEqual("NOT_PROVED",impact_scout(x)["status"])
    def test_no_unlicensed_inference(self):
        self.assertEqual("",category("aload_0",""))
        self.assertEqual("aabb_inflate_DDD",category("invokevirtual",
           "Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;"))

def synthetic_geometry():
    rows=[f"{i}: nop" for i in range(279)]
    rows[0]="0: aload_0"
    rows[1]="1: invokevirtual #2 // Method getImpactPosition:()Lnet/minecraft/world/phys/Vec3;"
    rows[2]="2: astore_2"
    rows[16]="16: new #3 // class net/minecraft/world/phys/AABB"
    rows[17]="17: dup"
    rows[18]="18: aload_2"
    rows[19]="19: aload_2"
    rows[20]='20: invokespecial #4 // Method net/minecraft/world/phys/AABB."<init>":(Lnet/minecraft/world/phys/Vec3;Lnet/minecraft/world/phys/Vec3;)V'
    rows[21]="21: ldc2_w #5 // double 1.75d"
    rows[22]="22: ldc2_w #6 // double 1.35d"
    rows[23]="23: ldc2_w #5 // double 1.75d"
    rows[24]="24: invokevirtual #7 // Method net/minecraft/world/phys/AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;"
    rows[25]="25: astore 5"
    rows[28]="28: aload_1"
    rows[29]="29: ldc #8 // class net/minecraft/world/entity/LivingEntity"
    rows[30]="30: aload 5"
    rows[31]="31: invokevirtual #9 // Method net/minecraft/server/level/ServerLevel.getEntitiesOfClass:(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;)Ljava/util/List;"
    return [("impact",D,rows)]

class ExactImpactGeometryTests(unittest.TestCase):
    def test_derived_bud_aabb_and_query_only(self):
        r=prove_impact_box_and_query(synthetic_geometry())
        self.assertEqual("PROVED_BUD_INFLATED_BOX_CONSUMED_BY_LIVING_ENTITY_QUERY",r["status"],r)
        self.assertEqual(["1.75","1.35","1.75"],r["inflate_double_xyz"])
        self.assertEqual([ "local2_Vec3","local2_Vec3"],r["aabb_constructor_operands"])
        self.assertEqual(5,r["query_aabb_loaded_local"])
        self.assertTrue(r["impact_position_to_local2"])
        self.assertIn("NOT proved",r["boundary"])
    def test_bad_aabb_ctor_fails_closed(self):
        d=synthetic_geometry();d[0][2][20]="20: invokespecial #4 // Method other.AABB.init:()V"
        self.assertEqual("NOT_PROVED",prove_impact_box_and_query(d)["status"])
    def test_different_vertical_extent_fails_closed(self):
        d=synthetic_geometry();d[0][2][22]="22: ldc2_w #6 // double 2.5d"
        self.assertEqual("NOT_PROVED",prove_impact_box_and_query(d)["status"])
    def test_wrong_box_local_fails_closed(self):
        d=synthetic_geometry();d[0][2][30]="30: aload 6"
        self.assertEqual("NOT_PROVED",prove_impact_box_and_query(d)["status"])
    def test_wrong_class_fails_closed(self):
        d=synthetic_geometry();d[0][2][29]="29: ldc #8 // class net/minecraft/world/entity/Entity"
        self.assertEqual("NOT_PROVED",prove_impact_box_and_query(d)["status"])
    def test_external_jump_into_geometry_block_fails_closed(self):
        d=synthetic_geometry();d[0][2][7]="7: goto 22"
        self.assertEqual("NOT_PROVED",prove_impact_box_and_query(d)["status"])
    def test_ambiguous_method_fails_closed(self):
        self.assertEqual("NOT_PROVED",prove_impact_box_and_query(synthetic_geometry()*2)["status"])

if __name__=="__main__":
    unittest.main()
