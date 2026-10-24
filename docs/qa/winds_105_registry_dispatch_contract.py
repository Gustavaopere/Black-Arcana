#!/usr/bin/env python3
"""SHA-pinned static ABI/registry candidate proof: no dynamic dispatch or factory claim."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import winds_105_spell_metadata as binary
import winds_105_effect_registry_dispatch as audit

ABSTRACT = "io.redspace.ironsspellbooks.api.spells.AbstractSpell"
EFFECT_SUPER = "io.redspace.ironsspellbooks.effect.MagicMobEffect"
CONSTRUCTORS = {
    "lambda$static$0(": "net/raptorzizi/wind_spellbooks/effect/AeropicEffect",
    "lambda$static$1(": "net/raptorzizi/wind_spellbooks/effect/TailwindEffect",
}
FIELDS = {"ACROBATICS:Lnet/neoforged/neoforge/registries/DeferredHolder;",
          "TAILWIND:Lnet/neoforged/neoforge/registries/DeferredHolder;"}

class ContractError(ValueError):
    pass

def validate(doc: dict) -> int:
    identity={"result":"PASS_SHA_EXACT_REGISTRY_AND_DISPATCH_SYMBOLS",
              "sha1":binary.EXPECTED_SHA1,"release":"1.0.5",
              "provider":"wind_spellbooks","classes_in_provider":64}
    if not isinstance(doc,dict) or any(doc.get(k)!=v for k,v in identity.items()):
        raise ContractError("exact provider release identity changed")
    classes=doc.get("class_declarations")
    if not isinstance(classes,dict) or set(classes)!=set(audit.CLASSES):
        raise ContractError("five-class declaration roster drift")
    for short,parent in {"aeropic_spell":ABSTRACT,"tailwind_spell":ABSTRACT,
                         "aeropic_effect":EFFECT_SUPER,"tailwind_effect":EFFECT_SUPER}.items():
        if classes[short].get("immediate_superclass_token")!=parent:
            raise ContractError("unexpected compiled immediate superclass for "+short)
        if classes[short].get("semantics")!="JAVAP_DECLARATIONS_ONLY":
            raise ContractError("false runtime promotion")
    recast=doc.get("aeropic_virtual_recast",{})
    mandatory={"spell_declares_method_descriptor":audit.GET_RECAST,
               "effect_invokes_method_descriptor":audit.GET_RECAST,
               "effect_invokes_owner":ABSTRACT,
               "signature_compatible":True,
               "runtime_dispatch_to_spell_override":"NOT_PROVEN",
               "receiver_instance":"NOT_PROVEN",
               "host_abstractspell_implementation":"NOT_INSPECTED"}
    if any(recast.get(k)!=v for k,v in mandatory.items()):
        raise ContractError("recast ABI or non-dispatch boundary drift")
    if len(classes["aeropic_spell"]["recast_declarations"])!=1:
        raise ContractError("recast override declaration not unique")
    if classes["aeropic_spell"]["recast_declarations"][0]["descriptor"]!=audit.GET_RECAST:
        raise ContractError("override descriptor drift")
    registry=doc.get("registry",{})
    if (registry.get("registration_field_to_instance_binding")!="NOT_PROVEN"
        or registry.get("invokedynamic_bootstrap_resolution")!="NOT_PROVEN"
        or registry.get("semantics")!="SYMBOLIC_JVM_REGISTRY_SITES_ONLY"):
        raise ContractError("unproven native registration promoted")
    candidates=registry.get("candidate_methods")
    if not isinstance(candidates,dict) or "static {};" not in candidates:
        raise ContractError("missing registry clinit")
    stat=candidates["static {};"]
    if not {"tailwind","aeropic"}.issubset(stat.get("relevant_string_constants",[])):
        raise ContractError("registration name symbol drift")
    if not FIELDS.issubset(stat.get("field_references",[])):
        raise ContractError("registry field reference drift")
    if stat.get("invokedynamic_site_count")!=2:
        raise ContractError("registry supplier site count drift")
    if not any("DeferredRegister.register:(Ljava/lang/String;Ljava/util/function/Supplier;)"
               in x for x in stat.get("method_invokes",[])):
        raise ContractError("missing DeferredRegister supplier invocation")
    for method,clazz in CONSTRUCTORS.items():
        matches=[v for k,v in candidates.items() if method in k]
        if len(matches)!=1 or clazz not in matches[0].get("effect_constructor_candidates",[]):
            raise ContractError("missing effect constructor candidate "+method)
    return 2

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--json",required=True,type=Path)
    args=p.parse_args()
    try:
        result=validate(json.loads(args.json.read_text(encoding="utf-8")))
    except (ContractError,ValueError,OSError,TypeError,KeyError) as exc:
        print("FAIL_CLOSED: "+str(exc))
        return 1
    print(f"PASS: {result} compiled effect constructor candidates + Aeropic inherited recast ABI; supplier binding and runtime dispatch NOT_PROVEN")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
