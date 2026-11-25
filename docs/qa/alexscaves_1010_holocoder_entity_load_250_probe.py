#!/usr/bin/env python3
"""Bounded read-only entity representation and UUID deserialization discovery.

Project exact distributed method bodies, typed calls, exception-table entries and
bootstrap handles. No game execution, loaded-mod inference or mutation.
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
P = "com/github/alexmodguy/alexscaves/server/"
TYPE = MC + "world/entity/EntityType"
ENTITY = MC + "world/entity/Entity"
TAG = MC + "nbt/CompoundTag"
HOLO = P + "block/blockentity/HologramProjectorBlockEntity"
ITEM = P + "item/HolocoderItem"
COMPAT = P + "misc/ACCompat"
PLATFORM = P + "misc/ACPlatform"
SELECT = {
    TYPE: {"by", "create", "loadStaticEntity", "loadEntityRecursive",
           "lambda$create$4", "lambda$create$5", "lambda$create$6", "lambda$loadEntityRecursive$7"},
    ENTITY: {"saveAsPassenger", "saveWithoutId", "load", "startRiding", "addPassenger",
             "serializeNBT", "deserializeNBT", "readAdditionalSaveData", "addAdditionalSaveData"},
    TAG: {"getUUID", "putUUID", "hasUUID", "contains", "getList", "getIntArray", "getString", "getCompound"},
    MC+"nbt/NbtUtils": {"loadUUID", "createUUID"},
    MC+"core/UUIDUtil": {"uuidFromIntArray", "uuidToIntArray", "leastMostToIntArray"},
    MC+"nbt/IntArrayTag": {"getAsIntArray", "<init>"},
    MC+"nbt/ListTag": {"getCompound", "getElementType", "size"},
    MC+"resources/ResourceLocation": {"parse", "tryParse", "bySeparator", "tryBySeparator", "assertValidNamespace", "assertValidPath"},
    "net/neoforged/neoforge/common/extensions/IEntityExtension": {"serializeNBT", "deserializeNBT"},
    HOLO: {"getDisplayEntity", "setEntity", "loadAdditional", "saveAdditional"},
    ITEM: {"getBoundEntityUUID", "isBound"},
    COMPAT: {"entityTypeFrom", "getUUID", "putUUID", "hasUUID", "markDisplayEntity"},
    PLATFORM: {"serializeEntity"},
}
PINS = {
    TYPE: "48c9761c2756859bf6734d6d623532e382fa78d52f73e33a6671c8a9fef2cb8d",
    ENTITY: "4f65b7d5d4628e9f10a6a23e5a0f68814520d8019f4bc001924cd752c00eed84",
    TAG: "93a9643a11aa61b666871cadeb14be32ff4f813bf97b05951bae389bada15fe6",
    HOLO: "5aaf4f2f96190d740a101f75c2603d2f3b1001a8c494eaa0594e6aebde308057",
    ITEM: "7d2697b694b97483ad592733fad8ad595de0fa0805de7a0396ac6cb4715dfd96",
    COMPAT: "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
}
KNOWN = {
    (TYPE,"by","(Lnet/minecraft/nbt/CompoundTag;)Ljava/util/Optional;"):
        "7805295fd5281c3f0fa3b347af587a0609a4bb2e2d0aa9eb0b9002db7e38b745",
    (TYPE,"create","(Lnet/minecraft/nbt/CompoundTag;Lnet/minecraft/world/level/Level;)Ljava/util/Optional;"):
        "0a5cac55bbb389687a277d8126d51488c6d7d4f495905364f5210faa15b5f49e",
    (TYPE,"loadEntityRecursive","(Lnet/minecraft/nbt/CompoundTag;Lnet/minecraft/world/level/Level;Ljava/util/function/Function;)Lnet/minecraft/world/entity/Entity;"):
        "3a63201fa9087a793c3f872c58d7dcedfde2bd5a8481cce2ac0a2e9e33376d91",
    (ENTITY,"load","(Lnet/minecraft/nbt/CompoundTag;)V"):
        "776e21588ffb8384705ac584255b82bdb9a471e89e49bc8949048d60e0fbbe88",
    (ENTITY,"saveWithoutId","(Lnet/minecraft/nbt/CompoundTag;)Lnet/minecraft/nbt/CompoundTag;"):
        "04ba844cbcb8c70d4ec427dfe8f56bfeef10cb0a564066cd679f63bdeec5ab5d",
    (COMPAT,"entityTypeFrom","(Lnet/minecraft/nbt/CompoundTag;)Ljava/util/Optional;"):
        "ccffa1ba52333413dbc8952ba9eb956bfed3448c7eea64746c64c5ba5eeceeec",
}
# Bootstrap targets previously observed; a missing or non-executable target fails closed.
REQUIRED = {
    TYPE: {"loadStaticEntity", "lambda$create$4", "lambda$create$5", "lambda$create$6", "lambda$loadEntityRecursive$7"},
    TAG: {"getUUID", "hasUUID", "putUUID"},
    COMPAT: {"entityTypeFrom", "getUUID", "hasUUID", "putUUID", "markDisplayEntity"},
    HOLO: {"getDisplayEntity", "setEntity"}, ITEM: {"getBoundEntityUUID", "isBound"},
    PLATFORM: {"serializeEntity"},
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
          "external_entity_callbacks":"NOT_CLOSED","actual_capture_and_inventory_settlement":"NOT_VERIFIED"}

def selected(owner, declaration):
    return declaration["name"] in SELECT.get(owner, set())

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
    require(sum(len(v.get("methods",[])) for v in result.values())<=120,"total method budget")
    return {"schema":1,"artifacts":identity,"classes":result,"limits":LIMITS}

def self_test():
    require(selected(TYPE,{"name":"lambda$loadEntityRecursive$7"}),"exact bootstrap target")
    require(not selected(TYPE,{"name":"lambda$loadEntityRecursive$70"}),"suffix false positive")
    require(not selected(ENTITY,{"name":"tick"}),"out-of-scope method")
    require(not selected("unrelated/EntityType",{"name":"by"}),"out-of-scope owner")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS: five scope and policy checks")

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
