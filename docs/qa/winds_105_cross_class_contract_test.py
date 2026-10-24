#!/usr/bin/env python3
"""Mutation fixtures: binary-invoke counts must be pinned without gameplay claims."""
from copy import deepcopy
import unittest

import winds_105_cross_class_contract as gate
import winds_105_spell_metadata as binary
import winds_105_getter_consumer_edges as edges

def valid():
    result = {"result":"PASS_SHA_EXACT_CROSS_CLASS_DIRECT_CALL_INVENTORY",
              "sha1":binary.EXPECTED_SHA1,"provider":"wind_spellbooks",
              "release":"1.0.5","classes_inspected":64,"getters_scoped":9,
              "explicit_invokes_found":16,"out_of_declaring_spell_invokes":0,
              "selected_getters":{}}
    for spell, getters in gate.CALL_COUNTS.items():
        owner=binary.BASE+binary.ROSTER[spell]
        result["selected_getters"][spell]={}
        for getter, n in getters.items():
            desc=edges.GETTERS[spell][getter]
            rows=[{"caller_class":owner,"callee_spell":spell,
                   "callee_getter":getter,
                   "callee_jvm_ref":owner.replace(".","/")+"."+getter+":"+desc,
                   "evidence":"DIRECT_COMPILED_INVOKE_ONLY"}
                  for _ in range(n)]
            result["selected_getters"][spell][getter]={
                "direct_calls":rows,"calls_outside_declaring_spell_class":0,
                "runtime_getter_to_sink_flow":"NOT_PROVEN"}
    return result

class FrozenContractTests(unittest.TestCase):
    def test_exact_fixture(self):
        self.assertEqual(16,gate.validate(valid()))
    def test_reject_sha_change(self):
        d=valid();d["sha1"]="0"*40
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_reject_missing_class(self):
        d=valid();d["classes_inspected"]=63
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_reject_new_outside_class_call(self):
        d=valid();d["out_of_declaring_spell_invokes"]=1
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_reject_mutated_getter_count(self):
        d=valid();d["selected_getters"]["wind_jump"]["getFloatDuration"]["direct_calls"].pop()
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_reject_false_causal_promotion(self):
        d=valid();d["selected_getters"]["tornado"]["getDuration"]["runtime_getter_to_sink_flow"]="PROVEN"
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_reject_foreign_owner(self):
        d=valid();d["selected_getters"]["tailwind"]["getPercentJump"]["direct_calls"][0]["caller_class"]="other.Mod"
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_reject_wrong_descriptor(self):
        d=valid();d["selected_getters"]["tailwind"]["getPercentJump"]["direct_calls"][0]["callee_jvm_ref"]="bad.Get"
        with self.assertRaises(gate.ContractError):gate.validate(d)

if __name__=="__main__":
    unittest.main()
