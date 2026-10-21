#!/usr/bin/env python3
"""Synthetic clean-room lambda inspector regressions."""
import unittest
from somake_109_funeral_raycast_predicate import survey
from somake_109_funeral_spell_handoff import SPELL_ONCAST_DESC
PRED="(Lnet/minecraft/world/entity/Entity;)Z"
def fixture():
    cast=[f"{i}: nop" for i in range(81)]
    cast[13]='13: invokedynamic #1, 0 // InvokeDynamic #0:test:()Ljava/util/function/Predicate;'
    predicate=[
        "0: aload_0",
        "1: instanceof #2 // class net/minecraft/world/entity/LivingEntity",
        "4: ifeq 12",
        "7: iconst_1",
        "8: ireturn",
        "12: iconst_0",
        "13: ireturn",
    ]
    return [("onCast",SPELL_ONCAST_DESC,cast),("lambda$onCast$0",PRED,predicate)]
class SurveyTests(unittest.TestCase):
    def test_bounded_typed_branch_metadata(self):
        s=survey(fixture())
        self.assertEqual("OBSERVED_RAYCAST_LAMBDA_TYPED_SHAPES",s["status"],s)
        self.assertEqual(1,len(s["candidate_lambdas"]))
        self.assertEqual("LivingEntity",s["candidate_lambdas"][0]["ops"][1]["class"])
        self.assertEqual(5,s["candidate_lambdas"][0]["ops"][2]["target_index"])
        self.assertIn("unproven",s["boundary"])
    def test_missing_lambda_fails(self):
        self.assertEqual("NOT_PROVED",survey(fixture()[:1])["status"])
    def test_wrong_factory_fails(self):
        f=fixture();f[0][2][13]="13: nop"
        self.assertEqual("NOT_PROVED",survey(f)["status"])
    def test_wrong_cast_descriptor_fails(self):
        f=fixture();f[0]=("onCast","()V",f[0][2])
        self.assertEqual("NOT_PROVED",survey(f)["status"])
    def test_duplicate_oncast_fails(self):
        f=fixture();f.append(f[0])
        self.assertEqual("NOT_PROVED",survey(f)["status"])
if __name__=="__main__":
    unittest.main()
