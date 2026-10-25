#!/usr/bin/env python3
"""Mutation regression on exact SHA-verified Aeropic symbolic boundaries."""
import unittest
import copy
import winds_105_spell_metadata as physical
import winds_105_aeropic_recast_operand_sites as probe
import winds_105_aeropic_recast_operand_contract as contract

def good():
    doc={
        "result":"PASS_SHA_EXACT_RECAST_OPERAND_ADJACENCY_ONLY",
        "release":"1.0.5","provider":"wind_spellbooks",
        "sha1":physical.EXPECTED_SHA1,"effect_class":probe.EFFECT,
        "calls_observed":2,"bytecode_context_not_published":True,
        "receiver_concrete_type":"NOT_TRACED",
        "getRecastCount_return_consumer":"NOT_TRACED",
        "installed_host_binary_identity":"NOT_VERIFIED",
        "safe_mutating_hook":"NOT_PROVEN",
        "physical_gameplay_validation":"NOT_TESTED",
        "call_sites":{},
    }
    for method,expected in contract.EXPECTED.items():
        row={
            "invocation_opcode":"invokevirtual",
            "owner_and_descriptor":probe.RECAST,
            "receiver_object":"NOT_TRACED",
            "return_value_dataflow":"NOT_TRACED",
            "runtime_override_dispatch":"NOT_PROVEN",
            "scope":"ADJACENT_SYMBOLS_NOT_JVM_STACK_DATAFLOW",
        }
        row.update(copy.deepcopy(expected))
        doc["call_sites"][method]=row
    return doc

class FrozenContractTests(unittest.TestCase):
    def test_observed_fingerprint(self):
        self.assertEqual(2,contract.validate(good()))
    def test_reject_wrong_sha(self):
        d=good();d["sha1"]="0"*40
        with self.assertRaises(contract.ContractError):contract.validate(d)
    def test_reject_missing_callsite(self):
        d=good();d["call_sites"].pop("onEffectAdded")
        with self.assertRaises(contract.ContractError):contract.validate(d)
    def test_reject_wrong_invoke(self):
        d=good();d["call_sites"]["applyEffectTick"]["invocation_opcode"]="invokestatic"
        with self.assertRaises(contract.ContractError):contract.validate(d)
    def test_reject_missing_registry_field(self):
        d=good();d["call_sites"]["onEffectAdded"]["prelude_field_refs"]=[]
        with self.assertRaises(contract.ContractError):contract.validate(d)
    def test_reject_missing_supplier_get(self):
        d=good();d["call_sites"]["onEffectAdded"]["prelude_method_refs"]=[]
        with self.assertRaises(contract.ContractError):contract.validate(d)
    def test_reject_missing_player_recast(self):
        d=good();d["call_sites"]["applyEffectTick"]["following_method_refs"]=[]
        with self.assertRaises(contract.ContractError):contract.validate(d)
    def test_reject_wrong_immediate_opcode(self):
        d=good();d["call_sites"]["onEffectAdded"]["immediately_after_opcode"]="pop"
        with self.assertRaises(contract.ContractError):contract.validate(d)
    def test_reject_receiver_promotion(self):
        d=good();d["receiver_concrete_type"]="AeropicSpell"
        with self.assertRaises(contract.ContractError):contract.validate(d)
    def test_reject_stack_flow_promotion(self):
        d=good();d["call_sites"]["applyEffectTick"]["return_value_dataflow"]="PROVEN"
        with self.assertRaises(contract.ContractError):contract.validate(d)
    def test_reject_runtime_hook_promotion(self):
        d=good();d["safe_mutating_hook"]="ALLOWED"
        with self.assertRaises(contract.ContractError):contract.validate(d)

if __name__=="__main__":
    unittest.main()
