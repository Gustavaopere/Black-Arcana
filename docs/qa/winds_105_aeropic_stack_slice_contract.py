#!/usr/bin/env python3
"""Pin negative-but-informative SHA-exact Aeropic JVM stack slice conclusions.

No static receiver producer, runtime dispatch or perk hook may be silently
promoted from a symbol-neighborhood result or an unresolved basic block.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import winds_105_spell_metadata as physical
import winds_105_aeropic_recast_invokes as invocations
import winds_105_aeropic_supplier_receiver_slice as direct

class ContractError(ValueError):
    pass

EXPECTED_METHODS={
    "applyEffectTick":{
        "stack_reason":"FAIL_CLOSED_control flow or return in candidate stack slice",
        "direct_reason":"NO_MATCHING_UNBRANCHED_FIVE_INSTRUCTION_PRODUCER",
    },
    "onEffectAdded":{
        "stack_reason":"RECEIVER_NOT_FROM_CHECKED_SUPPLIER_RESULT",
        "direct_reason":"NO_MATCHING_UNBRANCHED_FIVE_INSTRUCTION_PRODUCER",
    },
}

def validate(stack_doc:dict, direct_doc:dict) -> int:
    top={
        "result":"PASS_EXACT_JVM_BASIC_BLOCK_RECAST_RECEIVER_CLASSIFICATION",
        "sha1":physical.EXPECTED_SHA1,
        "release":"1.0.5",
        "provider":"wind_spellbooks",
        "compiled_jvm_stack_observations_only":True,
        "untrusted_provider_code_copied":False,
        "host_installed_checksum":"NOT_VERIFIED",
        "runtime_dispatch":"NOT_PROVEN",
        "safe_mutating_hook":"NOT_PROVEN",
        "physical_gameplay":"NOT_TESTED",
    }
    if not isinstance(stack_doc,dict) or any(stack_doc.get(k)!=v for k,v in top.items()):
        raise ContractError("exact SHA 1.0.5 or non-runtime classification drift")
    dtop={
        "result":"PASS_SHA_EXACT_CONSERVATIVE_AEROPIC_RECEIVER_SLICE",
        "sha1":physical.EXPECTED_SHA1,
        "provider":"wind_spellbooks",
        "release":"1.0.5",
        "sender_jvm_bytecode_redistributed":False,
        "runtime_recast_dispatch":"NOT_PROVEN",
        "safe_mutating_hook":"NOT_PROVEN",
        "real_client_survival_qa":"NOT_TESTED",
    }
    if not isinstance(direct_doc,dict) or any(direct_doc.get(k)!=v for k,v in dtop.items()):
        raise ContractError("exact conservative direct-slice identity drift")
    stacks=stack_doc.get("call_sites")
    directs=direct_doc.get("call_sites")
    if not isinstance(stacks,dict) or not isinstance(directs,dict) or \
       set(stacks)!=set(EXPECTED_METHODS) or set(directs)!=set(EXPECTED_METHODS):
        raise ContractError("method population must be exactly two")
    for method,expected in EXPECTED_METHODS.items():
        row=stacks[method]
        drow=directs[method]
        frozen_stack={
            "method":method,
            "compiled_receiver_source":"NOT_PROVEN",
            "evidence_grade":"NOT_PROVEN",
            "non_proof_reason":expected["stack_reason"],
            "recast_invoke_symbol":invocations.RECAST,
            "runtime_receiver_concrete_class":"NOT_PROVEN",
            "supplier_actual_spell_class":"NOT_PROVEN",
            "dynamic_override_executed":"NOT_PROVEN",
            "return_value_to_PlayerRecasts":"NOT_PROVEN",
            "safe_perk_mutator":"NOT_PROVEN",
        }
        frozen_direct={
            "method":method,
            "method_owner_and_descriptor":invocations.RECAST,
            "owner_opcode":"invokevirtual",
            "static_receiver_origin":"NOT_PROVEN",
            "origin_proof_rule":"NO_SAFE_CONTIGUOUS_SLICE",
            "non_proof_reason":expected["direct_reason"],
            "receiver_runtime_type":"NOT_PROVEN",
            "abstractspell_override_target":"NOT_PROVEN",
            "recast_state_value_flow":"NOT_PROVEN",
            "safe_mutating_hook":"NOT_PROVEN",
        }
        if not isinstance(row,dict) or not isinstance(drow,dict):
            raise ContractError("missing method evidence row")
        for key,value in frozen_stack.items():
            if row.get(key)!=value:
                raise ContractError("static stack or runtime claim drift: "+method+"."+key)
        for key,value in frozen_direct.items():
            if drow.get(key)!=value:
                raise ContractError("direct slice or runtime claim drift: "+method+"."+key)
    return 2

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--stack-json",required=True,type=Path)
    p.add_argument("--direct-json",required=True,type=Path)
    a=p.parse_args()
    try:
        count=validate(json.loads(a.stack_json.read_text(encoding="utf8")),
                       json.loads(a.direct_json.read_text(encoding="utf8")))
    except (ContractError,ValueError,TypeError,KeyError,OSError) as exc:
        print("FAIL_CLOSED: "+str(exc))
        return 1
    print(f"PASS: {count} SHA-frozen Aeropic compiled recast receiver paths remain NOT_PROVEN; no gameplay/perk claims")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
