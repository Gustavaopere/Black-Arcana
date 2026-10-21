#!/usr/bin/env python3
"""Original synthetic shape tests for SHA-exact Somake bud impact scanner."""
import unittest
from somake_109_bud_impact_geometry import impact_scout, category

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
if __name__=="__main__":
    unittest.main()
