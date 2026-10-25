#!/usr/bin/env python3
"""Independent synthetic mutations for exact Aeropic callsite ABI scope."""
import unittest
import winds_105_aeropic_recast_contract as gate
import winds_105_aeropic_recast_invokes as audit
import winds_105_spell_metadata as physical

def fixture():
    calls={}
    for method,decl in gate.DECLS.items():
        calls[method]={
            "method_declaration":decl,
            "invocation_opcode":"invokevirtual",
            "invoked_owner":"io.redspace.ironsspellbooks.api.spells.AbstractSpell",
            "invoked_name":"getRecastCount",
            "invoked_descriptor":"(ILnet/minecraft/world/entity/LivingEntity;)I",
            "related_call_symbols_in_same_method":sorted(gate.RELATED_TICK) if method=="applyEffectTick" else [],
            "dynamic_receiver_type":"NOT_PROVEN",
            "virtual_target_resolution":"NOT_PROVEN",
            "return_value_consumer":"NOT_PROVEN",
            "execution_in_runtime":"NOT_TESTED",
        }
    return {"result":"PASS_EXACT_AEROPIC_RECAST_CALLSITE_OPCODE_INVENTORY",
            "sha1":physical.EXPECTED_SHA1,"provider":"wind_spellbooks","release":"1.0.5",
            "effect_class":audit.EFFECT,"recast_owner_ref":audit.RECAST,
            "call_site_total":2,"runtime_override_dispatch":"NOT_PROVEN",
            "host_JAR_abi":"NOT_VERIFIED","safe_mutating_hook":"NOT_PROVEN",
            "call_sites":calls}

class ContractTests(unittest.TestCase):
    def test_exact_binary_evidence(self):
        self.assertEqual(2,gate.validate(fixture()))
    def test_wrong_hash_rejected(self):
        x=fixture();x["sha1"]="0"*40
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_wrong_invoke_type_rejected(self):
        x=fixture();x["call_sites"]["onEffectAdded"]["invocation_opcode"]="invokestatic"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_wrong_owner_rejected(self):
        x=fixture();x["call_sites"]["applyEffectTick"]["invoked_owner"]="other.Base"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_missing_method_rejected(self):
        x=fixture();x["call_sites"].pop("onEffectAdded")
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_extra_recast_related_call_rejected(self):
        x=fixture();x["call_sites"]["onEffectAdded"]["related_call_symbols_in_same_method"]=["extra.Api"]
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_receiver_promotion_rejected(self):
        x=fixture();x["call_sites"]["onEffectAdded"]["dynamic_receiver_type"]="AeropicSpell"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_return_consumer_promotion_rejected(self):
        x=fixture();x["call_sites"]["applyEffectTick"]["return_value_consumer"]="PlayerRecasts"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_fake_host_certification_rejected(self):
        x=fixture();x["host_JAR_abi"]="PROVEN"
        with self.assertRaises(gate.ContractError):gate.validate(x)
    def test_fake_hook_certification_rejected(self):
        x=fixture();x["safe_mutating_hook"]="PROVEN"
        with self.assertRaises(gate.ContractError):gate.validate(x)

if __name__=="__main__":
    unittest.main()
