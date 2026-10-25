#!/usr/bin/env python3
"""Host 3.16.3 pinned binary contract mutations, separate from metadata parser."""
import unittest
import irons_3163_aeropic_host_abi as host
import irons_3163_aeropic_host_contract as contract

def exact():
    doc={
        "result":"PASS_EXACT_HOST_3163_RECAST_ABI","host_jar":host.HOST_NAME,
        "host_mod_version":host.HOST_VERSION,
        "sha1":contract.PINNED_SHA1,"sha512":contract.PINNED_SHA512,
        "file_size":host.EXPECTED_BYTES,
        "provenance":"OFFICIAL_MODRINTH_VERSION_METADATA_MATCHED_SHA512",
        "scope":"EXACT_PUBLISHED_COMPILED_HOST_ABI_NOT_RUNTIME",
        "host_abi_compatible_with_Wind_calls":True,
        "aeropic_effect_receiver":"NOT_PROVEN",
        "aeropic_override_execution":"NOT_PROVEN",
        "recast_flow_to_host_state":"NOT_PROVEN",
        "safe_black_arcana_or_rpg_mutator":"NOT_PROVEN",
        "gameplay_validation":"NOT_TESTED",
        "wind_provider":"wind_spellbooks-1.0.5; sha1 8744886899bc245ae147a44baa2b183689cec7da",
        "host_classes":{}
    }
    for short,name in host.NEEDED.items():
        doc["host_classes"][short]={
            "class_name":name,"classification":"EXACT_PUBLISHED_JVM_DECLARATIONS_ONLY",
            "checked_signatures":{method:{
                "descriptor":descriptor,"is_static":False,"is_abstract":False}
                for method,descriptor in host.METHODS.get(short,set())}}
    return doc

class ContractTests(unittest.TestCase):
    def test_valid_five_abis(self):
        self.assertEqual(5,contract.validate(exact()))
    def test_sha1_drift_rejected(self):
        doc=exact();doc["sha1"]="a"*40
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_sha512_drift_rejected(self):
        doc=exact();doc["sha512"]="b"*128
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_release_size_drift_rejected(self):
        doc=exact();doc["file_size"]+=1
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_wrong_host_version_rejected(self):
        doc=exact();doc["host_mod_version"]="1.20.1-3.16.3"
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_missing_host_class_rejected(self):
        doc=exact();doc["host_classes"].pop("magic_data")
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_missing_recast_method_rejected(self):
        doc=exact();doc["host_classes"]["player_recasts"]["checked_signatures"].pop("addRecast")
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_static_recast_rejected(self):
        doc=exact();doc["host_classes"]["abstract_spell"]["checked_signatures"]["getRecastCount"]["is_static"]=True
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_false_receiver_claim_rejected(self):
        doc=exact();doc["aeropic_effect_receiver"]="AeropicSpell"
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_false_override_claim_rejected(self):
        doc=exact();doc["aeropic_override_execution"]="PASS"
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_false_return_dataflow_rejected(self):
        doc=exact();doc["recast_flow_to_host_state"]="PROVEN"
        with self.assertRaises(contract.ContractError):contract.validate(doc)
    def test_false_hook_claim_rejected(self):
        doc=exact();doc["safe_black_arcana_or_rpg_mutator"]="APPROVED"
        with self.assertRaises(contract.ContractError):contract.validate(doc)

if __name__=="__main__":
    unittest.main()
