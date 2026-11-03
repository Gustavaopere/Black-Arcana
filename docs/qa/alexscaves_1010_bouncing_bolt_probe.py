#!/usr/bin/env python3
"""Read-only SHA-exact 1.0.10 Bouncing Bolt enchantment and ricochet probe.

Selected JVM symbol/branch/numeric windows only; not a full CFG, source
decompilation, live gameplay evidence, or safe perk hook certification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

SCOPE = "EXACT_ALEXSCAVES_1010_BOUNCING_BOLT_RICOCHET_SELECTED_ABI"
ENCHANTMENT = "alexscaves:bouncing_bolt"
SEA_STAFF = BASE + "server/item/SeaStaffItem.class"
WATER_BOLT = BASE + "server/entity/item/WaterBoltEntity.class"
CLASSES = {
    SEA_STAFF: "cb3153a35e7f4c3ab23e68693aec110edf03ecd050c3b485e35ccbb257b4bbc6",
    WATER_BOLT: "342c011b0178e1f65cd2e6ef315fe6bad49bd5ead237b2274e822560e2eac401",
}
RESOURCE_PATHS = (
    "data/alexscaves/enchantment/bouncing_bolt.json",
    "data/alexscaves/enchantment/triple_splash.json",
    "data/alexscaves/tags/item/enchantable/sea_staff.json",
)
SELECTORS = {
    SEA_STAFF: (("use","(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;",270,335),),
    WATER_BOLT: (
        ("damageMobs","()V",95,275),
        ("onRicochetHit","(Lnet/minecraft/world/entity/Entity;)V",0,275),
    ),
}
PIVOTS = {
    "use": ("BOUNCING_BOLT:", "enchantLevel:", "setRicochet:", "TRIPLE_SPLASH:"),
    "damageMobs": ("hurt:", "onRicochetHit:", "isRicochet:", "getRicochet:", "setRicochet:"),
    "onRicochetHit": ("getEntities:", "getOwner:", "isAlliedTo:", "distanceTo:",
                      "setArcingTowards:", "setTarget:", "addFreshEntity:",
                      "setDeltaMovement:", "setBubbling:", "setPos:",
                      "setRicochet:"),
}
SYMBOLIC = {"getfield","putfield","getstatic","putstatic","invokestatic",
            "invokevirtual","invokespecial","invokeinterface","invokedynamic"}
NUMERIC = {"ldc","ldc_w","ldc2_w","bipush","sipush","fconst_0","fconst_1",
           "fconst_2","dconst_0","dconst_1","iconst_0","iconst_1",
           "iconst_2","iconst_3","iconst_4","iconst_5"}

def require(ok,reason):
    if not ok:
        raise ValueError(reason)

def slim(row):
    return {k:row[k] for k in ("offset","opcode","operand","symbol")}

def select(methods,name,descriptor):
    matches=[m for m in methods if name_of(m)==name and m["descriptor"]==descriptor]
    require(len(matches)==1,"missing/ambiguous method "+name+" "+descriptor)
    m=matches[0]
    ins=m["instructions"]
    require(15<=len(ins)<=1800,"unexpected selected method size "+name)
    offsets=[x["offset"] for x in ins]
    require(offsets==sorted(set(offsets)),"duplicate/unsorted JVM offsets "+name)
    return m

def selected_evidence(m,name,lo,hi):
    ins=m["instructions"]
    local=[x for x in ins if lo<=x["offset"]<=hi]
    require(len(local)>=5,"empty/small critical bytecode window "+name)
    symbols=[slim(x) for x in local if x["opcode"] in SYMBOLIC]
    branches=[slim(x) for x in local if x["opcode"].startswith(("if","goto"))]
    nums=[slim(x) for x in local if x["opcode"] in NUMERIC]
    require(len(symbols)<=100 and len(branches)<=90 and len(nums)<=100,
            "unbounded selected evidence "+name)
    pivot_rows=[]
    for token in PIVOTS[name]:
        matched=[i for i,x in enumerate(ins) if token in x["symbol"]]
        if matched:
            i=matched[0]
            pivot_rows.append({
                "marker":token,"matches":len(matched),
                "first_offset":ins[i]["offset"],
                "nearby":[slim(x) for x in ins[max(0,i-4):i+7]],
            })
    require(len(pivot_rows)<=len(PIVOTS[name]),"unbounded pivot count")
    if name=="use":
        require(any("BOUNCING_BOLT:" in x["symbol"] for x in local),
                "Bouncing Bolt consumer missing inside bounded use region")
        require(any(x["marker"]=="BOUNCING_BOLT:" for x in pivot_rows),
                "Bouncing Bolt field missing")
    if name=="damageMobs":
        require(any("onRicochetHit:" in x["symbol"] for x in ins),
                "native ricochet handoff missing")
    if name=="onRicochetHit":
        require(any("getEntities:" in x["symbol"] for x in ins),
                "ricochet candidate query missing")
        require(any("addFreshEntity:" in x["symbol"] for x in ins),
                "ricochet child spawn call missing")
    return {
        "name":name,"header":m["header"],"descriptor":m["descriptor"],
        "instruction_count":len(ins),"parsed_method_sha256":digest_method(m),
        "selected_offset_window":[lo,hi],
        "symbolic_refs":symbols,"branch_instructions":branches,
        "numeric_operands":nums,"pivots":pivot_rows,
        "scope":"SELECTED_NATIVE_INSTRUCTIONS_NOT_COMPLETE_CFG",
    }

def resource(z,path):
    raw=z.read(path)
    require(len(raw)<=18000,"oversized resource "+path)
    data=json.loads(raw)
    require(isinstance(data,dict),"non-object resource "+path)
    return {"path":path,"sha256":hashlib.sha256(raw).hexdigest(),"json":data}

def audit(jar,javap_bin):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),
            "publisher 1.0.10 SHA-1/SHA-256/size mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate JAR entry")
        for path in (*RESOURCE_PATHS,*CLASSES):
            require(path in names,"required exact JAR entry absent: "+path)
        resources=[resource(z,path) for path in RESOURCE_PATHS]
        hashes={path:hashlib.sha256(z.read(path)).hexdigest() for path in CLASSES}
    require(hashes==CLASSES,"existing Sea Staff/Water Bolt class contracts drift")
    e=resources[0]["json"]
    require(e.get("description",{}).get("translate")==
            "enchantment.alexscaves.bouncing_bolt","enchantment ID mismatch")
    require(e.get("supported_items")=="#alexscaves:enchantable/sea_staff",
            "Sea Staff support tag changed")
    require(e.get("max_level")==1,"unexpected Bouncing Bolt max level")
    require("alexscaves:sea_staff" in resources[2]["json"].get("values",[]),
            "Sea Staff missing from publisher enchantment item tag")
    t=resources[1]["json"]
    require("alexscaves:bouncing_bolt" in t.get("exclusive_set",[]) or
            "alexscaves:triple_splash" in e.get("exclusive_set",[]),
            "Bouncing Bolt/Triple Splash exclusivity declaration absent")
    selected=[]
    for path,entries in SELECTORS.items():
        methods=parse_methods(javap(javap_bin,jar,path[:-6].replace("/",".")))
        for name,descriptor,lo,hi in entries:
            m=select(methods,name,descriptor)
            selected.append({
                "owner":path,"owner_class_sha256":hashes[path],
                "class_method_count":len(methods),
                "method":selected_evidence(m,name,lo,hi),
            })
    return {
        "schema_version":1,"scope":SCOPE,
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "enchantment":{"id":ENCHANTMENT,"resource":resources[0]},
        "associated_resources":resources[1:],
        "classes":[{"path":p,"sha256":hashes[p]} for p in CLASSES],
        "consumers":selected,
        "limits":{
            "1_1_1_public_source_is_exact_authority":False,
            "complete_method_cfg":"NOT_RECONSTRUCTED",
            "accepted_hit_and_damage":"NOT_VERIFIED",
            "spawn_success_and_child_ownership":"NOT_CERTIFIED",
            "target_exclusivity_and_alliance_effective":"NOT_VERIFIED",
            "effective_datapacks":"NOT_VERIFIED",
            "client_server_replay_pvp_claims":"NOT_VERIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
            "perk_certification":"NOT_CERTIFIED",
        },
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",required=True,type=Path)
    parser.add_argument("--javap",default="javap")
    parser.add_argument("--seal",type=Path)
    parser.add_argument("--output",type=Path)
    a=parser.parse_args()
    result=audit(a.jar,a.javap)
    if a.seal:
        expected=json.loads(a.seal.read_text(encoding="utf8"))
        require(result==expected,"Bouncing Bolt exact seal drift")
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
