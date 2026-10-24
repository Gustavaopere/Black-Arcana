#!/usr/bin/env python3
"""Synthetic mutations for Wind 1.0.5 native effect method-symbol evidence."""
import unittest

import winds_105_effect_contract as gate
import winds_105_spell_metadata as binary

def valid():
    data={
        "result":"PASS_SHA_EXACT_EFFECT_CANDIDATE_SYMBOL_AUDIT",
        "sha1":binary.EXPECTED_SHA1,"provider":"wind_spellbooks","release":"1.0.5",
        "classes_inspected":gate.EXPECTED_CLASSES,
        "candidate_class_count":gate.EXPECTED_CANDIDATES,
        "entry_spell_field_refs":{
            key:{"referenced_provider_effect_registry_field":field,
                 "effect_class_or_instance_proven":False,
                 "proof":"EXACT_JVM_FIELD_READ_INSIDE_ONCAST_ONLY"}
            for key,field in {"aeropic":"ACROBATICS","tailwind":"TAILWIND"}.items()},
        "candidate_classes":{},
    }
    for short,methods in gate.REQUIRED.items():
        full=gate.PREFIX+short
        blocks={}
        for hint,fields in methods.items():
            blocks[f"public void {hint}int);"]={
                **fields, "strength":"JVM_METHOD_SYMBOL_INVENTORY_NOT_ARGUMENT_FLOW",
            }
        data["candidate_classes"][full]={
            "class_name":full, "class_name_candidate":True,
            "runtime_effect_settlement":"NOT_PROVEN",
            "classification":"CANDIDATE_AND_OR_REGISTRY_REFERENCE_ONLY",
            "candidate_methods":blocks,
        }
    for i in range(gate.EXPECTED_CANDIDATES-len(data["candidate_classes"])):
        full=f"net.raptorzizi.wind_spellbooks.effect.Other{i}"
        data["candidate_classes"][full]={"class_name":full}
    return data

class BoundaryContractTests(unittest.TestCase):
    def test_valid_synthetic_binary_fingerprint(self):
        self.assertEqual(2,gate.validate(valid()))
    def test_reject_wrong_sha(self):
        row=valid();row["sha1"]="0"*40
        with self.assertRaises(gate.ContractError):gate.validate(row)
    def test_reject_wrong_class_count(self):
        row=valid();row["classes_inspected"]=63
        with self.assertRaises(gate.ContractError):gate.validate(row)
    def test_reject_missing_aeropic_recast_path(self):
        row=valid()
        record=row["candidate_classes"][gate.PREFIX+"AeropicEffect"]
        method=next(k for k in record["candidate_methods"] if " applyEffectTick(" in k)
        record["candidate_methods"][method]["observed_invoked_symbols"]=[]
        with self.assertRaises(gate.ContractError):gate.validate(row)
    def test_reject_missing_tailwind_jump_attribute(self):
        row=valid();record=row["candidate_classes"][gate.PREFIX+"TailwindEffect"]
        method=next(k for k in record["candidate_methods"] if " onEffectStarted(" in k)
        record["candidate_methods"][method]["read_fields"]=[]
        with self.assertRaises(gate.ContractError):gate.validate(row)
    def test_reject_fall_distance_absence(self):
        row=valid();record=row["candidate_classes"][gate.PREFIX+"TailwindEffect"]
        method=next(k for k in record["candidate_methods"] if " applyEffectTick(" in k)
        record["candidate_methods"][method]["written_fields"]=[]
        with self.assertRaises(gate.ContractError):gate.validate(row)
    def test_reject_unfounded_native_settlement_claim(self):
        row=valid()
        row["candidate_classes"][gate.PREFIX+"TailwindEffect"]["runtime_effect_settlement"]="PROVEN"
        with self.assertRaises(gate.ContractError):gate.validate(row)
    def test_reject_claiming_ownership_from_spell_field(self):
        row=valid();row["entry_spell_field_refs"]["tailwind"]["effect_class_or_instance_proven"]=True
        with self.assertRaises(gate.ContractError):gate.validate(row)
    def test_reject_modified_method_semantics_label(self):
        row=valid();record=row["candidate_classes"][gate.PREFIX+"AeropicEffect"]
        method=next(k for k in record["candidate_methods"] if " onEffectRemoved(" in k)
        record["candidate_methods"][method]["strength"]="PROVEN_GAMEPLAY"
        with self.assertRaises(gate.ContractError):gate.validate(row)
    def test_reject_missing_method_signature(self):
        row=valid();record=row["candidate_classes"][gate.PREFIX+"AeropicEffect"]
        key=next(k for k in record["candidate_methods"] if " onEffectAdded(" in k)
        record["candidate_methods"].pop(key)
        with self.assertRaises(gate.ContractError):gate.validate(row)

if __name__=="__main__":
    unittest.main()
