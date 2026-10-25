#!/usr/bin/env python3
"""Pin observed 1.0.5 recast-adjacent symbols, never infer operand provenance."""
import argparse
import json
from pathlib import Path
import winds_105_spell_metadata as physical
import winds_105_aeropic_recast_operand_sites as probe

EXPECTED = {
    "applyEffectTick": {
        "immediately_prior_opcode": "aload",
        "immediately_after_opcode": "bipush",
        "instructions_examined_before": 24,
        "instructions_examined_after": 12,
        "prelude_branch_opcode_count": 1,
        "prelude_method_refs": [
            "io/redspace/ironsspellbooks/api/magic/MagicData.getPlayerRecasts:()Lio/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts;",
            "io/redspace/ironsspellbooks/api/spells/AbstractSpell.getSpellId:()Ljava/lang/String;",
            "io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.hasRecastForSpell:(Ljava/lang/String;)Z",
        ],
        "following_method_refs": [
            "io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.addRecast:(Lio/redspace/ironsspellbooks/capabilities/magic/RecastInstance;Lio/redspace/ironsspellbooks/api/magic/MagicData;)Z",
            'io/redspace/ironsspellbooks/capabilities/magic/RecastInstance."<init>":(Ljava/lang/String;IIILio/redspace/ironsspellbooks/api/spells/CastSource;Lio/redspace/ironsspellbooks/api/spells/ICastDataSerializable;)V',
        ],
    },
    "onEffectAdded": {
        "immediately_prior_opcode": "aload_3",
        "immediately_after_opcode": "iconst_1",
        "instructions_examined_before": 24,
        "instructions_examined_after": 9,
        "prelude_branch_opcode_count": 2,
        "prelude_field_refs": [
            "net/raptorzizi/wind_spellbooks/registries/ModSpellRegistry.ACROBATICS_SPELL:Ljava/util/function/Supplier;",
        ],
        "prelude_class_refs": [
            "io/redspace/ironsspellbooks/api/spells/AbstractSpell",
        ],
        "prelude_method_refs": [
            "java/util/function/Supplier.get:()Ljava/lang/Object;",
        ],
        "following_method_refs": [
            "net/minecraft/nbt/CompoundTag.putInt:(Ljava/lang/String;I)V",
        ],
    },
}
class ContractError(ValueError):
    pass

def validate(doc:dict) -> int:
    frozen={
        "result":"PASS_SHA_EXACT_RECAST_OPERAND_ADJACENCY_ONLY",
        "release":"1.0.5","provider":"wind_spellbooks",
        "sha1":physical.EXPECTED_SHA1,
        "effect_class":probe.EFFECT,
        "calls_observed":2,
        "bytecode_context_not_published":True,
        "receiver_concrete_type":"NOT_TRACED",
        "getRecastCount_return_consumer":"NOT_TRACED",
        "installed_host_binary_identity":"NOT_VERIFIED",
        "safe_mutating_hook":"NOT_PROVEN",
        "physical_gameplay_validation":"NOT_TESTED",
    }
    if not isinstance(doc,dict) or any(doc.get(k)!=v for k,v in frozen.items()):
        raise ContractError("frozen JAR identity or unproven runtime claim changed")
    found=doc.get("call_sites")
    if not isinstance(found,dict) or set(found)!=set(EXPECTED):
        raise ContractError("two selected recast method boundaries drifted")
    for method,known in EXPECTED.items():
        row=found[method]
        if not isinstance(row,dict):
            raise ContractError("invalid method evidence")
        for k,v in {
            "invocation_opcode":"invokevirtual",
            "owner_and_descriptor":probe.RECAST,
            "receiver_object":"NOT_TRACED",
            "return_value_dataflow":"NOT_TRACED",
            "runtime_override_dispatch":"NOT_PROVEN",
            "scope":"ADJACENT_SYMBOLS_NOT_JVM_STACK_DATAFLOW",
        }.items():
            if row.get(k)!=v:
                raise ContractError("unsupported recast invocation or stack claim "+method+"."+k)
        for field,required in known.items():
            value=row.get(field)
            if isinstance(required,list):
                if not isinstance(value,list) or not set(required).issubset(value):
                    raise ContractError("missing bytecode-adjacent symbol "+method+"."+field)
            elif value!=required:
                raise ContractError("drifted frozen opcode neighborhood "+method+"."+field)
    return 2

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--json",required=True,type=Path)
    args=p.parse_args()
    try:
        n=validate(json.loads(args.json.read_text(encoding="utf8")))
    except (ContractError,OSError,ValueError,TypeError,KeyError) as exc:
        print("FAIL_CLOSED: "+str(exc))
        return 1
    print(f"PASS: {n} exact Wind Aeropic recast symbol neighborhoods; receiver and dataflow still NOT_TRACED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
