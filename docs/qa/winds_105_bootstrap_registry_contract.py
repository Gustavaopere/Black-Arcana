#!/usr/bin/env python3
"""SHA-frozen 1.0.5 supplier->holder compiled ABI contract, not gameplay authority."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import winds_105_spell_metadata as binary
import winds_105_bootstrap_registry_trace as trace

class ContractError(ValueError):
    pass

def validate(doc: dict) -> int:
    if not isinstance(doc,dict):
        raise ContractError("not an object")
    identity={
        "result":"PASS_COMPILED_REGISTRATION_EDGES",
        "sha1":binary.EXPECTED_SHA1,
        "provider":"wind_spellbooks","release":"1.0.5",
        "scope":"EXACT_JAR_COMPILED_CLINIT_BOOTSTRAP_AND_FACTORY_ONLY",
        "runtime_cast_effect":"NOT_TESTED",
    }
    for k,v in identity.items():
        if doc.get(k)!=v:
            raise ContractError("release scope or identity drift: "+k)
    found=doc.get("registration_edges")
    if not isinstance(found,dict) or set(found)!=set(trace.TARGETS):
        raise ContractError("expected exactly two compiled registry holders")
    for field, expected in trace.TARGETS.items():
        actual=found[field]
        frozen={
            "registration_key":expected["key"],
            "holder_field":field,
            "receiver_binary_type":"net.neoforged.neoforge.registries.DeferredRegister",
            "registration_call":trace.REGISTRY_REGISTER,
            "supplier_bootstrap_site":0 if field=="ACROBATICS" else 1,
            "supplier_target":expected["supplier_method"],
            "factory_constructs_class":expected["effect"].replace("/","."),
            "compiled_supplier_to_holder":"PROVEN_BOUNDED_JVM_STACK_AND_BOOTSTRAP",
            "runtime_instance_registration":"NOT_TESTED",
            "client_gameplay_effect":"NOT_TESTED",
            "safe_mutating_hook":"NOT_PROVEN",
        }
        if not isinstance(actual,dict):
            raise ContractError("invalid holder record")
        for key,value in frozen.items():
            if actual.get(key)!=value:
                raise ContractError("compiled binding or authority drift: "+field+"."+key)
    return 2

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--json",required=True,type=Path)
    args=p.parse_args()
    try:
        count=validate(json.loads(args.json.read_text(encoding="utf-8")))
    except (ContractError,ValueError,OSError,TypeError,KeyError) as exc:
        print("FAIL_CLOSED: "+str(exc))
        return 1
    print(f"PASS: {count}/2 compiled exact-JAR effect registry edges; no runtime, dispatch or mutator-hook claims")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
