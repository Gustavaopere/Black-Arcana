#!/usr/bin/env python3
"""Synthetic clean-room lambda inspector regressions."""
import unittest
from somake_109_funeral_raycast_predicate import survey,certify_constant_false_predicate,bootstrap_scout
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

def constant_fixture():
    b=fixture()
    b[0][2][14]='14: invokestatic #3 // Method io/redspace/ironsspellbooks/util/SpellUtil.raycastForEntity:(Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/phys/EntityHitResult;'
    b[1]=("lambda$onCast$0",PRED,["0: iconst_0","1: ireturn"])
    return b
class FalsePredicateGateTests(unittest.TestCase):
    def test_original_false_lambda_with_native_cast_factory(self):
        p=certify_constant_false_predicate(constant_fixture())
        self.assertEqual("PROVED_ONCAST_UNLINKED_LAMBDA_CONSTANT_FALSE",p["status"],p)
        self.assertIs(False,p["lambda_boolean_result"])
        self.assertIn("bootstrap linkage",p["boundary"])
    def test_true_constant_mutation_fails(self):
        p=constant_fixture();p[1][2][0]="0: iconst_1"
        self.assertEqual("NOT_PROVED",certify_constant_false_predicate(p)["status"])
    def test_additional_condition_fails(self):
        p=constant_fixture();p[1]=("lambda$onCast$0",PRED,["0: iconst_0","1: nop","2: ireturn"])
        self.assertEqual("NOT_PROVED",certify_constant_false_predicate(p)["status"])
    def test_wrong_oncast_bootstrap_fails(self):
        p=constant_fixture();p[0][2][13]=p[0][2][13].replace("#0:test","#1:test")
        self.assertEqual("NOT_PROVED",certify_constant_false_predicate(p)["status"])
    def test_bootstrap_scanner_does_not_make_gameplay_claim(self):
        table=("\nBootstrapMethods:\n"
               "  0: #15 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/Object;)V\n"
               "    Method arguments:\n"
               "      #33 REF_invokeStatic com/somake/somakespells/spells/blood/FuneralBloomSpell.lambda$onCast$0:(Lnet/minecraft/world/entity/Entity;)Z\n"
               "\nInnerClasses:\n")
        p=bootstrap_scout(table)
        self.assertEqual("OBSERVED_BOOTSTRAP_METHOD_REFERENCES",p["status"])
        self.assertTrue(p["bootstrap_entries"][0]["funeral_lambda_handle"])
        self.assertIn("no proof of raycastForEntity",p["boundary"])
if __name__=="__main__":
    unittest.main()
