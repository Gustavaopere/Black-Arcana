#!/usr/bin/env python3
"""Bounded Gazing Pearl snapshot audit: exact 1.0.10 and NeoForge 21.1.250.
Resolve the missing long/boolean tag boundaries and inherited default item use.
Only read classfiles; preserve prior evidence and do not execute the game.
"""
from __future__ import annotations
import argparse
import json
from contextlib import ExitStack
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection

MC = "net/minecraft/"
NF = "net/neoforged/neoforge/"
P = "com/github/alexmodguy/alexscaves/server/"
PEARL = P+"item/GazingPearlItem"
COMPAT = P+"misc/ACCompat"
TAG = MC+"nbt/CompoundTag"
LONG = MC+"nbt/LongTag"
BYTE = MC+"nbt/ByteTag"
STACK = MC+"world/item/ItemStack"
DATA = MC+"world/item/component/CustomData"
ITEM = MC+"world/item/Item"
SELECT = {
    PEARL: {"acInventoryTick","appendHoverText","getPearlColor"},
    COMPAT: {"getLong","getBoolean"},
    TAG: {"getLong","putLong","getBoolean","getByte","contains","copy"},
    LONG: {"valueOf","getAsLong","getId","write"},
    BYTE: {"valueOf","getAsByte","getId","write"},
    DATA: {"of","copyTag","<init>"},
    ITEM: {"appendHoverText","inventoryTick","use","useOn","interactLivingEntity",
           "finishUsingItem","getUseDuration","isFoil","isEnchantable","getEnchantmentValue"},
    STACK: {"is"},
    MC+"world/level/Level": {"getGameTime"},
    MC+"world/entity/Entity": {"getUUID"},
}
PREFIXES = {}
PINS = {
    PEARL: "2519bc5aed494deccc0423053ea42904314511094b29cd1e4025cc65a08a5a07",
    COMPAT: "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    TAG: "93a9643a11aa61b666871cadeb14be32ff4f813bf97b05951bae389bada15fe6",
    DATA: "23463cf7238fbd2b9ff5bb11bb4a5466fcc06137e89f65d199fe31b7b7d451c9",
    STACK: "072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
}
KNOWN = {
    (PEARL,"getPearlColor","(Lnet/minecraft/world/item/ItemStack;)I"):
        "0b2790fa924d0e99c0acf32b85906e4b9ea72ca3a8807ec0c14419e33e400630",
    (COMPAT,"getBoolean","(Lnet/minecraft/nbt/CompoundTag;Ljava/lang/String;)Z"):
        "3be2c9e983db0531b1b9c240989d3b0cbf688fdbf99660deb9a7fb7ad7f55e62",
    (TAG,"getBoolean","(Ljava/lang/String;)Z"):
        "f767371f026e90d6f4444cda7f08280c44f1615f814b9c9e506e0882ef8def09",
    (TAG,"getByte","(Ljava/lang/String;)B"):
        "affb845efc023172015333d6ef85bb9ab040ecb8ea97a149958e5f261a6aa8ae",
    (DATA,"copyTag","()Lnet/minecraft/nbt/CompoundTag;"):
        "6289f2d8de89191b13354b90b6c79b1a13f1f66e12a54ba76f18f0535ef96ebc",
}
# Typed publisher callsites and previous executable bodies establish these names.
# Inherited defaults and primitive tag writers are candidates pending inspection.
REQUIRED = {
    PEARL: {"acInventoryTick","appendHoverText","getPearlColor"},
    COMPAT: {"getLong","getBoolean"},
    TAG: {"getLong","putLong","getBoolean","getByte"},
    DATA: {"copyTag"},
    ITEM: {"appendHoverText"},
}
DIST = {
    "installer": ("0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60", 6972109),
    "server": ("1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359", 5675624),
    "srg": ("26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71", 14246609),
    "universal": ("1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956", 3551255),
}
LIMITS = {"scope":"DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED","physical_qa":"NOT_TESTED",
          "mutating_hook":"NOT_VERIFIED","mutation":"NO_MUTATION","provider_universe_closed":False,
          "semantic_magic_roots_delta":0,"runtime_loaded_bytes":"NOT_OBSERVED",
          "snapshot_sync":"NOT_VERIFIED","actual_world_save":"NOT_VERIFIED",
          "active_datapacks":"NOT_OBSERVED"}

def selected(owner, declaration):
    name=declaration["name"]
    return name in SELECT.get(owner, set()) or name.startswith(PREFIXES.get(owner, ()))

def scan(args):
    identity={}
    for name,(sha,size) in DIST.items():
        raw=getattr(args,name).read_bytes()
        require(len(raw)==size and digest(raw)==sha,"distribution mismatch "+name)
        identity[name]={"sha256":sha,"bytes":size}
    verify_artifact(args.publisher)
    identity["publisher"]={"sha1":SHA1,"sha256":SHA256,"bytes":SIZE}
    order=("server","universal","srg","publisher")
    seen=set()
    result={}
    with ExitStack() as stack:
        archives={name:stack.enter_context(ZipFile(getattr(args,name))) for name in order}
        rosters={}
        for name,z in archives.items():
            paths=z.namelist()
            require(len(paths)==len(set(paths)),"duplicate paths "+name)
            rosters[name]=set(paths)
        cp=":".join(str(getattr(args,name)) for name in order)
        for owner in sorted(SELECT):
            sources=[name for name in order if owner+".class" in rosters[name]]
            if not sources:
                require(owner not in REQUIRED and owner not in PINS,"required owner absent "+owner)
                result[owner]={"present":False}
                continue
            raw=archives[sources[0]].read(owner+".class")
            sha=digest(raw)
            reader=ClassReader(raw)
            require(reader.name==owner and reader.major==65,"class identity "+owner)
            require(owner not in PINS or sha==PINS[owner],"prior class identity "+owner)
            declarations=[d for d in reader.methods if selected(owner,d)]
            require(len(declarations)<=32,"per-owner method budget")
            require(REQUIRED.get(owner,set())<={d["name"] for d in declarations if "code_sha256" in d},
                    "required executable name absent "+owner)
            parsed=disassemble(cp,args.javap,owner)
            methods=[]
            for d in declarations:
                key=(d["name"],d["descriptor"])
                qualified=(owner,*key)
                if "code_sha256" not in d:
                    require(qualified not in KNOWN,"prior Code absent "+str(qualified))
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]),"missing parsed method "+str(qualified))
                if qualified in KNOWN:
                    require(d["code_sha256"]==KNOWN[qualified],"prior Code mismatch "+str(qualified))
                    seen.add(qualified)
                row=projection(reader,key,parsed[key],d)
                row["exception_handlers"]=d["exception_handlers"]
                row["executable"]=True
                methods.append(row)
            result[owner]={"present":True,"source":sources[0],"available_sources":sources,"class_sha256":sha,
                           "parent":reader.parent,"interfaces":reader.interfaces,
                           "declared_signatures":[[d["name"],d["descriptor"]] for d in reader.methods],
                           "methods":methods}
    require(seen==set(KNOWN),"prior Code coverage mismatch")
    require(result[PEARL]["parent"]==ITEM,"pearl native parent drift")
    require(len(result[PEARL]["declared_signatures"])==5,"pearl local method roster drift")
    # Confirm the exact native callsite signatures, not only the candidate names.
    def method(owner,name,descriptor):
        rows=[m for m in result[owner]["methods"] if (m["name"],m["descriptor"])==(name,descriptor)]
        require(len(rows)==1 and rows[0].get("executable"),"exact method absent "+owner+"."+name)
        return rows[0]
    tick=method(PEARL,"acInventoryTick","(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V")
    for offset,owner,name,desc in (
        (17,COMPAT,"getLong","(Lnet/minecraft/nbt/CompoundTag;Ljava/lang/String;)J"),
        (62,TAG,"putLong","(Ljava/lang/String;J)V"),
        (70,TAG,"putBoolean","(Ljava/lang/String;Z)V"),
        (86,TAG,"putInt","(Ljava/lang/String;I)V"),
        (92,COMPAT,"setTag","(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V"),
    ):
        require(any((m["offset"],m["owner"],m["name"],m["descriptor"])==(offset,owner,name,desc)
                    for m in tick["typed_members"]),"snapshot callsite mismatch "+name)
    method(COMPAT,"getLong","(Lnet/minecraft/nbt/CompoundTag;Ljava/lang/String;)J")
    method(TAG,"getLong","(Ljava/lang/String;)J")
    method(TAG,"putLong","(Ljava/lang/String;J)V")
    require(sum(len(v.get("methods",[])) for v in result.values())<=120,"total method budget")
    return {"schema":1,"artifacts":identity,"classes":result,"limits":LIMITS}

def self_test():
    require(selected(PEARL,{"name":"acInventoryTick"}),"native snapshot")
    require(selected(COMPAT,{"name":"getLong"}),"long wrapper")
    require(selected(TAG,{"name":"putLong"}),"long producer")
    require(selected(ITEM,{"name":"appendHoverText"}),"native super call")
    require(not selected(COMPAT,{"name":"putUUID"}),"reuse existing UUID scope")
    require(not selected("foreign/GazingPearlItem",{"name":"acInventoryTick"}),"namespace boundary")
    require(all(names<=SELECT[owner] for owner,names in REQUIRED.items()),"required scope consistency")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS: eight scope and policy checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in (*DIST,"publisher","output"):
        p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all(getattr(a,n) for n in (*DIST,"publisher","output")) and not a.output.exists(),
                "all exact inputs and write-once output required")
        report=scan(a)
        raw=canonical(report).encode()
        require(len(raw)<=3_000_000,"report byte budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as out:
            out.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in report["classes"].items():
            print("OWNER",owner,row.get("source"),row.get("class_sha256"),"METHODS",len(row.get("methods",[])))
            for m in row.get("methods",[]):
                print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
