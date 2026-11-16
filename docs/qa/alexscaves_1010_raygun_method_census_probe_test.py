#!/usr/bin/env python3
"""Synthetic fail-closed Raygun 26-method roster discovery regression tests."""
import copy
import unittest

from alexscaves_1010_raygun_method_census_probe import (
    CensusError, SCOPE, census, unique_pairs,
)
from alexscaves_1010_raygun_local_flow_probe import digest_method

def row(offset, opcode, operand="", symbol=""):
    return {"offset":offset, "opcode":opcode, "operand":operand, "symbol":symbol}

def fake_methods():
    return [{"header":f"public void method{n}();", "descriptor":"()V",
             "instructions":[row(0,"return")]} for n in range(26)]

def prior_for(methods):
    return {
        "scope":"SHA_EXACT_1010_RAYGUN_SELECTED_METHOD_REFERENCES_AND_NUMERIC_OPERANDS_ONLY",
        "declared_method_count":26,
        "selected_method_digests":{
            f"method{i} ()V":digest_method(methods[i]) for i in range(8)
        }
    }

class RaygunNativeMethodCensus(unittest.TestCase):
    def test_discovery_scope_not_certification(self):
        self.assertIn("DISCOVERY_ONLY", SCOPE)

    def test_missing_method_rejected(self):
        ms=fake_methods()
        with self.assertRaisesRegex(CensusError, "declared method population"):
            census(ms[:-1],prior_for(ms))

    def test_duplicate_identity_rejected(self):
        ms=fake_methods()
        ms[-1]=copy.deepcopy(ms[0])
        with self.assertRaisesRegex(CensusError,"duplicate compiled method"):
            census(ms,prior_for(ms))

    def test_unchanged_old_digest_required(self):
        ms=fake_methods()
        prior=prior_for(ms)
        prior["selected_method_digests"]["method0 ()V"]="0"*64
        with self.assertRaisesRegex(CensusError,"historical full-body method drift"):
            census(ms,prior)

    def test_wrong_old_scope_rejected(self):
        ms=fake_methods()
        prior=prior_for(ms)
        prior["scope"]="OTHER"
        with self.assertRaisesRegex(CensusError,"wrong prior"):
            census(ms,prior)

    def test_wrong_method_population_in_prior_rejected(self):
        ms=fake_methods()
        prior=prior_for(ms)
        prior["declared_method_count"]=25
        with self.assertRaisesRegex(CensusError,"prior declared"):
            census(ms,prior)

    def test_missing_code_rejected(self):
        ms=fake_methods()
        ms[-1]["instructions"]=[]
        with self.assertRaisesRegex(CensusError,"missing descriptor or bytecode"):
            census(ms,prior_for(ms))

    def test_branch_to_unrecognized_offset_rejected(self):
        ms=fake_methods()
        ms[-1]["instructions"]=[row(0,"ifeq","99"),row(3,"return")]
        with self.assertRaisesRegex(ValueError,"branch destination"):
            census(ms,prior_for(ms))

    def test_duplicate_manifest_key_rejected(self):
        with self.assertRaisesRegex(CensusError,"duplicate JSON key"):
            unique_pairs([("x",1),("x",2)])

if __name__=="__main__":
    unittest.main()
