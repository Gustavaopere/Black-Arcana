#!/usr/bin/env python3
"""Immutable SHA-exact negative stack result and no unsafe hook promotion."""
import copy
import unittest
import winds_105_aeropic_stack_slice_contract as contract
import winds_105_spell_metadata as binary
import winds_105_aeropic_recast_invokes as invokes

def pair():
    st={"result":"PASS_EXACT_JVM_BASIC_BLOCK_RECAST_RECEIVER_CLASSIFICATION",
        "sha1":binary.EXPECTED_SHA1,"provider":"wind_spellbooks","release":"1.0.5",
        "compiled_jvm_stack_observations_only":True,
        "untrusted_provider_code_copied":False,
        "host_installed_checksum":"NOT_VERIFIED","runtime_dispatch":"NOT_PROVEN",
        "safe_mutating_hook":"NOT_PROVEN","physical_gameplay":"NOT_TESTED",
        "call_sites":{}}
    dr={"result":"PASS_SHA_EXACT_CONSERVATIVE_AEROPIC_RECEIVER_SLICE",
        "sha1":binary.EXPECTED_SHA1,"provider":"wind_spellbooks","release":"1.0.5",
        "sender_jvm_bytecode_redistributed":False,
        "runtime_recast_dispatch":"NOT_PROVEN",
        "safe_mutating_hook":"NOT_PROVEN","real_client_survival_qa":"NOT_TESTED",
        "call_sites":{}}
    for method,known in contract.EXPECTED_METHODS.items():
        st["call_sites"][method]={
            "method":method,"compiled_receiver_source":"NOT_PROVEN",
            "evidence_grade":"NOT_PROVEN",
            "non_proof_reason":known["stack_reason"],
            "recast_invoke_symbol":invokes.RECAST,
            "runtime_receiver_concrete_class":"NOT_PROVEN",
            "supplier_actual_spell_class":"NOT_PROVEN",
            "dynamic_override_executed":"NOT_PROVEN",
            "return_value_to_PlayerRecasts":"NOT_PROVEN",
            "safe_perk_mutator":"NOT_PROVEN"}
        dr["call_sites"][method]={
            "method":method,"method_owner_and_descriptor":invokes.RECAST,
            "owner_opcode":"invokevirtual",
            "static_receiver_origin":"NOT_PROVEN",
            "origin_proof_rule":"NO_SAFE_CONTIGUOUS_SLICE",
            "non_proof_reason":known["direct_reason"],
            "receiver_runtime_type":"NOT_PROVEN",
            "abstractspell_override_target":"NOT_PROVEN",
            "recast_state_value_flow":"NOT_PROVEN",
            "safe_mutating_hook":"NOT_PROVEN"}
    return st,dr

class ContractTests(unittest.TestCase):
    def test_valid_pinned_two_callers(self):
        self.assertEqual(2,contract.validate(*pair()))
    def test_wrong_sha_rejected(self):
        a,b=pair();a["sha1"]="0"*40
        with self.assertRaises(contract.ContractError):contract.validate(a,b)
    def test_forged_static_receiver_rejected(self):
        a,b=pair();a["call_sites"]["onEffectAdded"]["compiled_receiver_source"]="PROVEN"
        with self.assertRaises(contract.ContractError):contract.validate(a,b)
    def test_forged_runtime_override_rejected(self):
        a,b=pair();a["call_sites"]["onEffectAdded"]["dynamic_override_executed"]="YES"
        with self.assertRaises(contract.ContractError):contract.validate(a,b)
    def test_missing_branch_blocker_rejected(self):
        a,b=pair();a["call_sites"]["applyEffectTick"]["non_proof_reason"]=None
        with self.assertRaises(contract.ContractError):contract.validate(a,b)
    def test_forged_player_recasts_flow_rejected(self):
        a,b=pair();a["call_sites"]["applyEffectTick"]["return_value_to_PlayerRecasts"]="YES"
        with self.assertRaises(contract.ContractError):contract.validate(a,b)
    def test_forged_supplier_spell_rejected(self):
        a,b=pair();a["call_sites"]["onEffectAdded"]["supplier_actual_spell_class"]="AeropicSpell"
        with self.assertRaises(contract.ContractError):contract.validate(a,b)
    def test_incorrect_direct_owner_rejected(self):
        a,b=pair();b["call_sites"]["onEffectAdded"]["owner_opcode"]="invokestatic"
        with self.assertRaises(contract.ContractError):contract.validate(a,b)
    def test_forged_hook_rejected(self):
        a,b=pair();b["safe_mutating_hook"]="YES"
        with self.assertRaises(contract.ContractError):contract.validate(a,b)
    def test_missing_method_rejected(self):
        a,b=pair();a["call_sites"].pop("onEffectAdded")
        with self.assertRaises(contract.ContractError):contract.validate(a,b)
    def test_binary_release_drift_rejected(self):
        a,b=pair();b["release"]="1.0.6"
        with self.assertRaises(contract.ContractError):contract.validate(a,b)

if __name__=="__main__":
    unittest.main()
