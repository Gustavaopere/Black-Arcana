#!/usr/bin/env python3
"""SHA-exact Energy Efficiency 1.0.10 Raygun consumption discovery.

Read-only physical JAR audit; this discovery stage MUST NOT certify static
behavior or allow mutating hooks until the JVM branch and stack proof is sealed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_raygun_local_flow_probe import (
    CLASS, CLASS_SHA256, DESC, METHOD_SHA256, digest_method,
)
from alexscaves_1010_bouncy_ball_causal_probe import (
    branch_edges, method_switch_tables,
)

RES="data/alexscaves/enchantment/energy_efficiency.json"
TAG="data/alexscaves/tags/item/enchantable/raygun.json"
CLASS_REG="com/github/alexmodguy/alexscaves/server/enchantment/ACEnchantmentRegistry.class"
CANONICAL_METHODS={
    "onUseTick":DESC,
    "hasCharge":"(Lnet/minecraft/world/item/ItemStack;)Z",
    "getCharge":"(Lnet/minecraft/world/item/ItemStack;)I",
    "setCharge":"(Lnet/minecraft/world/item/ItemStack;I)V",
}
PARENT_HASHES={
    "onUseTick":METHOD_SHA256,
    "hasCharge":"0b89217b97ca4f3d1c155c01b4170d1f0cb9141e4ee854ccf0c72892cd3b1db7",
    "getCharge":"c69c154524dbe4b4e46ed589438f7548cc39658305072a59b7c6a7dc9ec25baa",
    "setCharge":"cedf012dbfb8edf1ca2171c57001dc8937f2982e3755a156da058a74d260993e",
}
LIMITS={
    "individual_static_certificate":"PENDING_JVM_CAUSAL_SEAL",
    "artifact":"EXACT_PUBLISHER_1.0.10",
    "mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "effective_world_state":"NOT_TESTED",
    "network_authorization":"NOT_VERIFIED",
    "effective_charge_settlement":"NOT_TESTED",
}

def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)

def unique_pairs(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,"duplicate JSON key "+k)
        result[k]=v
    return result

def digest(payload: bytes):
    return hashlib.sha256(payload).hexdigest()

def method_select(methods, name, desc):
    hits=[m for m in methods if m["descriptor"]==desc and
          re.search(r"\b"+re.escape(name)+r"\(",m["header"])]
    require(len(hits)==1,"missing/ambiguous native method "+name)
    return hits[0]

def windows(rows, start=180, end=365):
    """Bounded exact raw JVM instructions, not source code or game execution."""
    result=[{key:r[key] for key in ("offset","opcode","operand","symbol")}
            for r in rows if start<=r["offset"]<=end]
    require(25<len(result)<160,"unexpected charge-region instruction population")
    offsets=[r["offset"] for r in result]
    require(offsets==sorted(set(offsets)),"bad exact JVM offset ordering")
    return result

def audit(jar: Path, javap_bin: str):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher 1.0.10 JAR fingerprint drift")
    with zipfile.ZipFile(jar) as arc:
        names=arc.namelist()
        require(len(names)==len(set(names)),"duplicate ZIP member")
        required=[RES,TAG,CLASS,CLASS_REG]
        for name in required:
            require(name in names,"missing 1.0.10 provider resource: "+name)
        require(digest(arc.read(CLASS))==CLASS_SHA256,
                "publisher Raygun compiled class drift")
        metadata=json.loads(arc.read(RES),object_pairs_hook=unique_pairs)
        tag=json.loads(arc.read(TAG),object_pairs_hook=unique_pairs)
        resource_hashes={name:digest(arc.read(name)) for name in (RES,TAG)}
        token_owners=sorted(name for name in names
                           if name.startswith("com/github/alexmodguy/alexscaves/")
                           and name.endswith(".class")
                           and b"ENERGY_EFFICIENCY" in arc.read(name))
        require(CLASS in token_owners and CLASS_REG in token_owners
                and len(token_owners)<=12,
                "unbounded/missing compiled ENERGY_EFFICIENCY consumers")
    source=javap(javap_bin,jar,CLASS[:-6].replace("/","."))
    declared=parse_methods(source)
    require(len(declared)==26,"native Raygun declared method count drift")
    selected={}
    for name,desc in CANONICAL_METHODS.items():
        method=method_select(declared,name,desc)
        require(digest_method(method)==PARENT_HASHES[name],
                "prior exact Raygun JVM method identity mismatch: "+name)
        selected[name]=method
    on_tick=selected["onUseTick"]
    ins=on_tick["instructions"]
    require(len(ins)==523,"native Raygun onUseTick instruction count drift")
    refs=[r for r in ins if "ACEnchantmentRegistry.ENERGY_EFFICIENCY:" in r["symbol"]]
    require(len(refs)==1 and refs[0]["offset"]==246 and refs[0]["opcode"]=="getstatic",
            "unexpected Energy Efficiency lookup location")
    branches=branch_edges(on_tick,method_switch_tables(on_tick,source))
    charge_window=windows(ins)
    return {
        "schema_version":1,
        "scope":"READ_ONLY_ENERGY_EFFICIENCY_1010_CHARGE_REGION_DISCOVERY",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "class":{"path":CLASS,"sha256":CLASS_SHA256},
        "resources":resource_hashes,
        "resource_data":{"enchantment":metadata,"raygun_item_tag":tag},
        "token_owners":token_owners,
        "declared_methods":len(declared),
        "native_methods":{name:{"descriptor":CANONICAL_METHODS[name],
            "method_sha256":digest_method(m),"instructions":len(m["instructions"])}
            for name,m in selected.items()},
        "onUseTick_direct_branches":len(branches),
        "onUseTick_charge_window":charge_window,
        "onUseTick_entry_window":[{k:r[k] for k in ("offset","opcode","operand","symbol")} for r in ins if r["offset"]<=85],
        "onUseTick_precharge_window":[{k:r[k] for k in ("offset","opcode","operand","symbol")} for r in ins if 132<=r["offset"]<=216],
        "limits":LIMITS,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    result=audit(a.jar,a.javap)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    a.output.write_text(data,encoding="utf8")
    print("ENERGY_EFFICIENCY_PUBLISHER_EXPLORATION")
    print("metadata="+json.dumps(result["resource_data"],sort_keys=True))
    print("resource_hashes="+json.dumps(result["resources"],sort_keys=True))
    print("token_owners="+json.dumps(result["token_owners"]))
    print("onUseTick_branches="+str(result["onUseTick_direct_branches"]))
    for label in ("onUseTick_entry_window","onUseTick_precharge_window","onUseTick_charge_window"):
        print("JVM_WINDOW="+label)
        for row in result[label]:
            print("@%d %s %s %s"%(row["offset"],row["opcode"],row["operand"],row["symbol"]))
    print("report_sha256="+digest(data.encode("utf8")))
    print("DISCOVERY_ONLY NO_MUTATION NOT_TESTED NO_STATIC_CERTIFICATE")

if __name__=="__main__":
    main()
