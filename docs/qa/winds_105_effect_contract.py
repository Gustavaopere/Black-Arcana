#!/usr/bin/env python3
"""Immutable SHA-exact Wind 1.0.5 effect/attribute/recast symbol contract.

A successful audit proves JVM method and symbol references, NEVER execution,
dispatch resolution, actual effect magnitude, perk hooks or host authority.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import winds_105_spell_metadata as binary

PREFIX = "net.raptorzizi.wind_spellbooks.effect."
EXPECTED_CLASSES = 64
EXPECTED_CANDIDATES = 9

# All symbols below are exact SHA-frozen symbolic refs from CI #40136512061.
REQUIRED = {
    "AeropicEffect": {
        "applyEffectTick(": {
            "observed_invoked_symbols": [
                "io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I",
                "io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.addRecast:(Lio/redspace/ironsspellbooks/capabilities/magic/RecastInstance;Lio/redspace/ironsspellbooks/api/magic/MagicData;)Z",
                "io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:(Lnet/minecraft/world/entity/Entity;FLnet/minecraft/world/damagesource/DamageSource;)Z",
            ],
            "written_fields": ["net/minecraft/world/entity/LivingEntity.fallDistance:F"],
        },
        "onEffectAdded(": {
            "observed_invoked_symbols": [
                "io/redspace/ironsspellbooks/api/spells/AbstractSpell.getRecastCount:(ILnet/minecraft/world/entity/LivingEntity;)I",
            ],
        },
        "onEffectRemoved(": {
            "observed_invoked_symbols": [
                "io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.decrementRecastCount:(Ljava/lang/String;)V",
            ],
        },
    },
    "TailwindEffect": {
        "applyEffectTick(": {
            "observed_invoked_symbols": [
                "net/minecraft/world/entity/LivingEntity.setDeltaMovement:(DDD)V",
            ],
            "written_fields": ["net/minecraft/world/entity/LivingEntity.fallDistance:F"],
        },
        "onEffectStarted(": {
            "observed_invoked_symbols": [
                "net/minecraft/world/entity/ai/attributes/AttributeInstance.addTransientModifier:(Lnet/minecraft/world/entity/ai/attributes/AttributeModifier;)V",
            ],
            "read_fields": [
                "net/minecraft/world/entity/ai/attributes/Attributes.JUMP_STRENGTH:Lnet/minecraft/core/Holder;",
                "net/minecraft/world/entity/ai/attributes/AttributeModifier$Operation.ADD_MULTIPLIED_TOTAL:Lnet/minecraft/world/entity/ai/attributes/AttributeModifier$Operation;",
            ],
        },
        "onEffectRemoved(": {
            "observed_invoked_symbols": [
                "net/minecraft/world/entity/ai/attributes/AttributeInstance.removeModifier:(Lnet/minecraft/resources/ResourceLocation;)Z",
            ],
            "read_fields": [
                "net/minecraft/world/entity/ai/attributes/Attributes.JUMP_STRENGTH:Lnet/minecraft/core/Holder;",
                "net/minecraft/world/entity/ai/attributes/Attributes.MOVEMENT_SPEED:Lnet/minecraft/core/Holder;",
            ],
        },
    },
}

class ContractError(ValueError):
    pass

def validate(doc: dict) -> int:
    if not isinstance(doc, dict):
        raise ContractError("invalid evidence document")
    frozen = {
        "result": "PASS_SHA_EXACT_EFFECT_CANDIDATE_SYMBOL_AUDIT",
        "sha1": binary.EXPECTED_SHA1, "provider":"wind_spellbooks", "release":"1.0.5",
        "classes_inspected":EXPECTED_CLASSES,
        "candidate_class_count":EXPECTED_CANDIDATES,
    }
    for field, value in frozen.items():
        if doc.get(field) != value:
            raise ContractError("frozen binary evidence drift at " + field)
    field_refs = doc.get("entry_spell_field_refs")
    if not isinstance(field_refs, dict) or set(field_refs) != {"aeropic", "tailwind"}:
        raise ContractError("missing spell entrypoint references")
    for spell, field in {"aeropic":"ACROBATICS", "tailwind":"TAILWIND"}.items():
        row = field_refs[spell]
        if (row.get("referenced_provider_effect_registry_field") != field
            or row.get("proof") != "EXACT_JVM_FIELD_READ_INSIDE_ONCAST_ONLY"
            or row.get("effect_class_or_instance_proven") is not False):
            raise ContractError("unsupported effect registration or onCast field claim")
    classes = doc.get("candidate_classes")
    if not isinstance(classes, dict) or len(classes) != EXPECTED_CANDIDATES:
        raise ContractError("candidate class population changed")
    for class_short, methods in REQUIRED.items():
        name=PREFIX+class_short
        row=classes.get(name)
        if (not isinstance(row,dict)
            or row.get("class_name") != name
            or row.get("class_name_candidate") is not True
            or row.get("runtime_effect_settlement") != "NOT_PROVEN"
            or row.get("classification") != "CANDIDATE_AND_OR_REGISTRY_REFERENCE_ONLY"):
            raise ContractError("candidate effect class identity or caveat changed: " + name)
        actual_methods=row.get("candidate_methods")
        if not isinstance(actual_methods,dict):
            raise ContractError("no candidate method mapping")
        for method_hint, fieldsets in methods.items():
            found=[v for k,v in actual_methods.items() if (" "+method_hint) in k]
            if len(found) != 1:
                raise ContractError("missing or ambiguous effect method "+name+"."+method_hint)
            block=found[0]
            if block.get("strength") != "JVM_METHOD_SYMBOL_INVENTORY_NOT_ARGUMENT_FLOW":
                raise ContractError("unfounded runtime dataflow promotion")
            for bucket, expected_symbols in fieldsets.items():
                values=block.get(bucket)
                if not isinstance(values,list) or not set(expected_symbols).issubset(values):
                    raise ContractError("missing JVM symbol "+name+"."+method_hint+"."+bucket)
    return 2

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--json",required=True,type=Path)
    args=p.parse_args()
    try:
        count=validate(json.loads(args.json.read_text(encoding="utf-8")))
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print("FAIL_CLOSED: "+str(exc))
        return 1
    print(f"PASS: {count} native Wind effect class symbolic boundaries, with NO dispatch/flow/gameplay/adapter claim")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
