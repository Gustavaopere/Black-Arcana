#!/usr/bin/env python3
"""SHA-exact clean-room contract of Galena Gauntlet player targeting/return JVM pivots.

This is a bounded, read-only *subcontract* of the exact 1.0.10 publisher JAR,
not a certification of actual raycast results, damage, world edits, perk hooks,
network synchronization or physical QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCOPE="ALEXSCAVES_1010_GALENA_GAUNTLET_PLAYER_TARGETING_COOLDOWN_RETURN_STATIC_ONLY"
ITEM="com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem"
ENTITY="com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity"
PUBLISHER_SHA="36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
ITEM_SHA="5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0"
ENTITY_SHA="a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071"
METHOD_NAMES={"tick","isOwnerWearingGauntlet","plopItem","getTarget"}
STATES={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
        "perk_certification":"NOT_CERTIFIED","provider_universe_closed":False,
        "semantic_magic_roots_delta":0,"actual_targeting_effects":"NOT_TESTED",
        "projectile_predicate_semantics":"NOT_VERIFIED",
        "gameplay_damage_settlement":"NOT_TESTED"}

def require(p,why):
    if not p:
        raise ValueError(why)

def no_dups(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,"duplicate JSON key "+k)
        out[k]=v
    return out

def read(path,limit):
    raw=Path(path).read_bytes()
    require(0<len(raw)<=limit,"bounded input bytes exceeded")
    return raw,json.loads(raw,object_pairs_hook=no_dups)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical_sha(value):
    return sha((json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf8"))

def assert_pivot(body,p):
    rows=[i for i in body if i["offset"]==p["offset"]]
    require(len(rows)==1,"JVM pivot offset missing/ambiguous "+str(p["offset"]))
    row=rows[0]
    require(row["opcode"]==p["opcode"],
            f"JVM opcode drift at {p['offset']}: {row['opcode']} != {p['opcode']}")
    require(p.get("contains","") in (row.get("symbol","")+" "+row.get("operand","")),
            "JVM symbol drift at "+str(p["offset"]))
    if "operand" in p:
        require(row["operand"]==p["operand"],"JVM operand drift at "+str(p["offset"]))

def check(report,manifest):
    raw,r=read(report,2_100_000)
    _,m=read(manifest,35_000)
    require(m["schema_version"]==r["schema_version"]==1,"schema drift")
    require(m["scope"]==SCOPE and r["scope"]=="GALENA_GAUNTLET_FULL_CLASS_DISCOVERY_NOT_CERTIFIED","scope drift")
    require(m["evidence"]["report_sha256"]==sha(raw),"exact discovery report digest drift")
    require(m["evidence"]["report_bytes"]==len(raw),"exact discovery report length drift")
    require(m["evidence"]["discovery_run_id"]==44934418449 and
            m["evidence"]["artifact_id"]==14719225697,"discovery provenance drift")
    a=r["artifact"];p=m["publisher"]
    require(a["sha256"]==p["sha256"]==PUBLISHER_SHA and
            a["size_bytes"]==p["size_bytes"]==75279314 and
            a["sha1"]==p["sha1"] and
            a["version"]==p["mod_version"]=="1.0.10" and
            a["filename"]==p["filename"]=="alexscaves-1.0.10-neoforge+1.21.1.jar",
            "publisher identity drift")
    require(p["minecraft"]=="1.21.1" and p["mod_id"]=="alexscaves" and
            p["installed_dump_parity"]==a["installed_dump_parity"]=="NOT_VERIFIED",
            "modlist/runtime inference drift")
    require(r["mutating_hook"]=="NOT_VERIFIED" and
            r["physical_qa"]=="NOT_TESTED" and
            r["mutation"]=="NO_MUTATION" and
            r["provider_universe_closed"] is False and
            r["semantic_magic_roots_certified_delta"]==0,"discovery scope drift")
    require(m["states"]==STATES,"safety scope status drift")
    require(set(r["native"]["targets"])=={ITEM} and
            set(r["entity_native"]["targets"])=={ENTITY},"class roster scope drift")
    i=r["native"]["targets"][ITEM]
    e=r["entity_native"]["targets"][ENTITY]
    require(i["class_sha256"]==m["item_class"]["sha256"]==ITEM_SHA and
            e["class_sha256"]==m["entity_class"]["sha256"]==ENTITY_SHA,
            "publisher class identity drift")
    require(len(i["methods"])==m["item_class"]["total_executable_methods"]==17 and
            len(e["methods"])==m["entity_class"]["total_executable_methods"]==24,
            "full executable method census drift")
    require(r["native"]["class_entries_scanned"]==r["entity_native"]["class_entries_scanned"]==1555,
            "classfile scan universe drift")
    bridge=m["predicate_bootstrap"]
    require(bridge["index"]==0 and bridge["invoke_dynamic_offset"]==651 and
            bridge["callsite_symbol"]=="InvokeDynamic #0:test:()Ljava/util/function/Predicate;",
            "predicate invokedynamic callsite drift")
    bootstraps=e["attributes"].get("bootstrap_methods",[])
    require(len(bootstraps)==1 and bootstraps[0]==bridge["entry"],
            "predicate bootstrap entry drift")
    expected_handle={"reference_kind":5,"reference":[10,
         "net/minecraft/world/entity/Entity",[12,"canBeHitByProjectile","()Z"]]}
    require(bootstraps[0]["arguments"][1]==expected_handle,
            "predicate method handle drift")
    require(bootstraps[0]["arguments"][0]=="(Ljava/lang/Object;)Z" and
            bootstraps[0]["arguments"][2]=="(Lnet/minecraft/world/entity/Entity;)Z",
            "predicate functional bridge drift")
    require(bootstraps[0]["handle"]["reference_kind"]==6 and
            bootstraps[0]["handle"]["reference"][1]=="java/lang/invoke/LambdaMetafactory" and
            bootstraps[0]["handle"]["reference"][2][1]=="metafactory",
            "predicate bootstrap factory drift")
    methods={(x["declaration"]["name"],x["declaration"]["descriptor"]):x for x in e["methods"]}
    require(len(methods)==len(e["methods"]),"ambiguous method declaration")
    require(len(m["methods"])==len(METHOD_NAMES)==4 and
            {v["name"] for v in m["methods"]}==METHOD_NAMES,
            "individual caller method roster drift")
    total_pivots=0
    for spec in m["methods"]:
        key=(spec["name"],spec["descriptor"])
        require(key in methods,"missing relevant JVM method "+repr(key))
        body=methods[key]
        require(body["declaration"]["code_sha256"]==spec["code_sha256"],
                "JVM Code SHA drift in "+key[0])
        require(body["instruction_sha256"]==spec["instruction_sha256"]==
                canonical_sha(body["instructions"]),"JVM disassembly SHA drift in "+key[0])
        require(len(body["instructions"])==body["instruction_count"]==spec["instruction_count"],
                "JVM instruction roster drift in "+key[0])
        require(len(spec["pivots"])>=5 and len(spec["pivots"])<=70,
                "JVM pivot bound drift")
        offsets=[p["offset"] for p in spec["pivots"]]
        require(offsets==sorted(set(offsets)),"duplicate/unsorted JVM pivots")
        for pivot in spec["pivots"]:
            assert_pivot(body["instructions"],pivot)
            total_pivots+=1
    require(total_pivots>=55 and total_pivots<=80,"causal pivot coverage drift")
    print("PASS: Galena Gauntlet 1.0.10 four exact JVM methods and",total_pivots,"behavior pivots")
    print("PASS: typed invokedynamic Entity.canBeHitByProjectile method-reference bridge")
    print("PASS: raycast scalar, owner-use guard, strike/cooldown, return/drop subcontracts")
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report",type=Path,required=True)
    parser.add_argument("--manifest",type=Path,required=True)
    args=parser.parse_args()
    check(args.report,args.manifest)
