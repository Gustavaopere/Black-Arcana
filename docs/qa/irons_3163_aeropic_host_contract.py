#!/usr/bin/env python3
"""Independent immutable host release and Aeropic-facing JVM ABI contract.

Compiled declaration compatibility is NOT proof of AeropicSpell receiver,
runtime dispatch, return-dataflow or safe recast mutation.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import irons_3163_aeropic_host_abi as host

PINNED_SHA1 = "e8832385c01db56b9fcb19c48fcedc76a3a70d92"
PINNED_SHA512 = ("fd782f98c6c59b193c4832f33775291d2a7e639e1e23dd47510bfb494d99d1"
                 "82bec1253566b9394f96c733a0d0108be34bd729614b82dc29e55e096fdeb96f5b")

class ContractError(ValueError):
    pass

def validate(evidence:dict) -> int:
    fixed={
        "result":"PASS_EXACT_HOST_3163_RECAST_ABI",
        "host_jar":host.HOST_NAME,
        "host_mod_version":host.HOST_VERSION,
        "sha1":PINNED_SHA1,"sha512":PINNED_SHA512,
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
    }
    if not isinstance(evidence,dict):
        raise ContractError("evidence not an object")
    for k,v in fixed.items():
        if evidence.get(k)!=v:
            raise ContractError("SHA-pinned release or causal-safety drift: "+k)
    classes=evidence.get("host_classes")
    if not isinstance(classes,dict) or set(classes)!=set(host.NEEDED):
        raise ContractError("host class roster changed")
    total=0
    for short,name in host.NEEDED.items():
        cls=classes[short]
        if cls.get("class_name")!=name or cls.get("classification")!="EXACT_PUBLISHED_JVM_DECLARATIONS_ONLY":
            raise ContractError("host class identity/claim changed "+short)
        found=cls.get("checked_signatures")
        expected=host.METHODS.get(short,set())
        if not isinstance(found,dict) or set(found)!={k for k,_ in expected}:
            raise ContractError("host methods changed "+short)
        for method,descriptor in expected:
            item=found[method]
            if (item.get("descriptor")!=descriptor
                or item.get("is_abstract") is not False
                or item.get("is_static") is not False):
                raise ContractError("host ABI or virtual-method status changed "+short+"."+method)
            total+=1
    if total!=5:
        raise ContractError("expected five frozen ABI contracts")
    return total

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--json",required=True,type=Path)
    args=p.parse_args()
    try:
        n=validate(json.loads(args.json.read_text(encoding="utf-8")))
    except (ContractError,ValueError,TypeError,KeyError,OSError) as exc:
        print("FAIL_CLOSED: "+str(exc))
        return 1
    print(f"PASS: {n} exact Iron's 3.16.3 recast ABIs match independently pinned publisher SHA512; no physical client/receiver/hook claim")
    return 0
if __name__=="__main__":
    raise SystemExit(main())
