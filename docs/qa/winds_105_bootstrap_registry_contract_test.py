#!/usr/bin/env python3
"""Reject frozen Wind supplier wiring drift without promoting runtime claims."""
import unittest

import winds_105_bootstrap_registry_contract as gate
import winds_105_bootstrap_registry_trace as trace
import winds_105_spell_metadata as binary

def fixture():
    out={"result":"PASS_COMPILED_REGISTRATION_EDGES",
         "sha1":binary.EXPECTED_SHA1,"release":"1.0.5","provider":"wind_spellbooks",
         "scope":"EXACT_JAR_COMPILED_CLINIT_BOOTSTRAP_AND_FACTORY_ONLY",
         "runtime_cast_effect":"NOT_TESTED","registration_edges":{}}
    for field,t in trace.TARGETS.items():
        out["registration_edges"][field]={
            "registration_key":t["key"],"holder_field":field,
            "receiver_binary_type":"net.neoforged.neoforge.registries.DeferredRegister",
            "registration_call":trace.REGISTRY_REGISTER,
            "supplier_bootstrap_site":0 if field=="ACROBATICS" else 1,
            "supplier_target":t["supplier_method"],
            "factory_constructs_class":t["effect"].replace("/","."),
            "compiled_supplier_to_holder":"PROVEN_BOUNDED_JVM_STACK_AND_BOOTSTRAP",
            "runtime_instance_registration":"NOT_TESTED",
            "client_gameplay_effect":"NOT_TESTED",
            "safe_mutating_hook":"NOT_PROVEN"}
    return out

class PinnedContractTests(unittest.TestCase):
    def test_accepts_two_exact_registry_edges(self):
        self.assertEqual(2,gate.validate(fixture()))
    def test_rejects_untrusted_sha(self):
        x=fixture();x["sha1"]="0"*40
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_missing_holder(self):
        x=fixture();x["registration_edges"].pop("TAILWIND")
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_changed_supplier_bootstrap(self):
        x=fixture();x["registration_edges"]["ACROBATICS"]["supplier_bootstrap_site"]=1
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_wrong_factory(self):
        x=fixture();x["registration_edges"]["TAILWIND"]["factory_constructs_class"]="other.Effect"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_changed_registration_key(self):
        x=fixture();x["registration_edges"]["TAILWIND"]["registration_key"]="aeropic"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_wrong_holder(self):
        x=fixture();x["registration_edges"]["ACROBATICS"]["holder_field"]="TAILWIND"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_unproven_gameplay_promotion(self):
        x=fixture();x["registration_edges"]["TAILWIND"]["client_gameplay_effect"]="PROVEN"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_unapproved_mutator(self):
        x=fixture();x["registration_edges"]["ACROBATICS"]["safe_mutating_hook"]="PROVEN"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_rejects_runtime_instance_claim(self):
        x=fixture();x["registration_edges"]["TAILWIND"]["runtime_instance_registration"]="PROVEN"
        with self.assertRaises(gate.ContractError):gate.validate(x)

if __name__=="__main__":
    unittest.main()
