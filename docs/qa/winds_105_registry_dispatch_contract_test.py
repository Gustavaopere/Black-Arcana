#!/usr/bin/env python3
"""Independent mutation fixtures for exact Wind effect registry and ABI evidence."""
import unittest

import winds_105_registry_dispatch_contract as gate
import winds_105_effect_registry_dispatch as audit
import winds_105_spell_metadata as binary

def good():
    classes={}
    for key,fqcn in audit.CLASSES.items():
        parent=gate.ABSTRACT if key in {"aeropic_spell","tailwind_spell"} else (
            gate.EFFECT_SUPER if key in {"aeropic_effect","tailwind_effect"} else None)
        classes[key]={"immediate_superclass_token":parent,
                      "semantics":"JAVAP_DECLARATIONS_ONLY",
                      "recast_declarations":[]}
    classes["aeropic_spell"]["recast_declarations"]=[{"descriptor":audit.GET_RECAST}]
    cand={"static {};":{
        "relevant_string_constants":["aeropic","tailwind"],
        "field_references":sorted(gate.FIELDS),
        "invokedynamic_site_count":2,
        "method_invokes":["net/neoforged/neoforge/registries/DeferredRegister.register:(Ljava/lang/String;Ljava/util/function/Supplier;)Lnet/neoforged/neoforge/registries/DeferredHolder;"],
    }}
    for method,cls in gate.CONSTRUCTORS.items():
        cand["private static Object "+method+"String);"]={
            "effect_constructor_candidates":[cls]}
    return {"result":"PASS_SHA_EXACT_REGISTRY_AND_DISPATCH_SYMBOLS",
            "sha1":binary.EXPECTED_SHA1,"release":"1.0.5","provider":"wind_spellbooks",
            "classes_in_provider":64,"class_declarations":classes,
            "aeropic_virtual_recast":{
                "spell_declares_method_descriptor":audit.GET_RECAST,
                "effect_invokes_method_descriptor":audit.GET_RECAST,
                "effect_invokes_owner":gate.ABSTRACT,
                "signature_compatible":True,
                "runtime_dispatch_to_spell_override":"NOT_PROVEN",
                "receiver_instance":"NOT_PROVEN",
                "host_abstractspell_implementation":"NOT_INSPECTED"},
            "registry":{
                "candidate_methods":cand,
                "registration_field_to_instance_binding":"NOT_PROVEN",
                "invokedynamic_bootstrap_resolution":"NOT_PROVEN",
                "semantics":"SYMBOLIC_JVM_REGISTRY_SITES_ONLY"}}

class EvidenceGateTests(unittest.TestCase):
    def test_accept_only_static_evidence(self):
        self.assertEqual(2,gate.validate(good()))
    def test_wrong_sha_fails(self):
        d=good();d["sha1"]="0"*40
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_missing_class_fails(self):
        d=good();d["classes_in_provider"]=63
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_changed_superclass_fails(self):
        d=good();d["class_declarations"]["aeropic_spell"]["immediate_superclass_token"]="other.Base"
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_wrong_override_descriptor_fails(self):
        d=good();d["aeropic_virtual_recast"]["spell_declares_method_descriptor"]="(I)I"
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_false_dispatch_claim_fails(self):
        d=good();d["aeropic_virtual_recast"]["runtime_dispatch_to_spell_override"]="PROVEN"
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_false_supplier_binding_fails(self):
        d=good();d["registry"]["registration_field_to_instance_binding"]="PROVEN"
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_missing_supplier_bootstrap_fails(self):
        d=good();d["registry"]["candidate_methods"]["static {};"]["invokedynamic_site_count"]=1
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_missing_effect_constructor_candidate_fails(self):
        d=good();d["registry"]["candidate_methods"].pop("private static Object lambda$static$1(String);")
        with self.assertRaises(gate.ContractError):gate.validate(d)
    def test_missing_registry_field_fails(self):
        d=good();d["registry"]["candidate_methods"]["static {};"]["field_references"]=[]
        with self.assertRaises(gate.ContractError):gate.validate(d)

if __name__=="__main__":
    unittest.main()
