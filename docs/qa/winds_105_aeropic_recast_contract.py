#!/usr/bin/env python3
"""Frozen Wind 1.0.5 AeropicEffect opcode/owner evidence, not dispatch proof."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import winds_105_spell_metadata as physical
import winds_105_aeropic_recast_invokes as evidence

DECLS = {
    "applyEffectTick": "public boolean applyEffectTick(net.minecraft.world.entity.LivingEntity, int);",
    "onEffectAdded": "public void onEffectAdded(net.minecraft.world.entity.LivingEntity, int);",
}
RELATED_TICK = {
    "io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.addRecast:(Lio/redspace/ironsspellbooks/capabilities/magic/RecastInstance;Lio/redspace/ironsspellbooks/api/magic/MagicData;)Z",
    "io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.hasRecastForSpell:(Ljava/lang/String;)Z",
    "io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.\"<init>\":(Ljava/lang/String;IIILio/redspace/ironsspellbooks/api/spells/CastSource;Lio/redspace/ironsspellbooks/api/spells/ICastDataSerializable;)V",
}

class ContractError(ValueError):
    pass

def validate(doc:dict) -> int:
    frozen={
        "result":"PASS_EXACT_AEROPIC_RECAST_CALLSITE_OPCODE_INVENTORY",
        "sha1":physical.EXPECTED_SHA1,
        "release":"1.0.5",
        "provider":"wind_spellbooks",
        "effect_class":evidence.EFFECT,
        "recast_owner_ref":evidence.RECAST,
        "call_site_total":2,
        "runtime_override_dispatch":"NOT_PROVEN",
        "host_JAR_abi":"NOT_VERIFIED",
        "safe_mutating_hook":"NOT_PROVEN",
    }
    if not isinstance(doc,dict):
        raise ContractError("evidence must be a JSON object")
    for k,v in frozen.items():
        if doc.get(k)!=v:
            raise ContractError("frozen opcode source drift: "+k)
    calls=doc.get("call_sites")
    if not isinstance(calls,dict) or set(calls)!=set(DECLS):
        raise ContractError("wrong exact method callsite population")
    for name,decl in DECLS.items():
        c=calls[name]
        for field,val in {
            "method_declaration":decl,
            "invocation_opcode":"invokevirtual",
            "invoked_owner":"io.redspace.ironsspellbooks.api.spells.AbstractSpell",
            "invoked_name":"getRecastCount",
            "invoked_descriptor":"(ILnet/minecraft/world/entity/LivingEntity;)I",
            "dynamic_receiver_type":"NOT_PROVEN",
            "virtual_target_resolution":"NOT_PROVEN",
            "return_value_consumer":"NOT_PROVEN",
            "execution_in_runtime":"NOT_TESTED",
        }.items():
            if c.get(field)!=val:
                raise ContractError(f"unsupported callsite fact: {name}.{field}")
        related=c.get("related_call_symbols_in_same_method")
        required=RELATED_TICK if name=="applyEffectTick" else set()
        if not isinstance(related,list) or set(related)!=required:
            raise ContractError("wrong co-present recast method symbol inventory: "+name)
    return 2

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--json",required=True,type=Path)
    args=p.parse_args()
    try:
        count=validate(json.loads(args.json.read_text(encoding="utf8")))
    except (ContractError,ValueError,OSError,TypeError,KeyError) as exc:
        print("FAIL_CLOSED: "+str(exc))
        return 1
    print(f"PASS: {count}/2 AeropicEffect invokevirtual calls to AbstractSpell.getRecastCount; receiver and gameplay NOT_PROVEN")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
