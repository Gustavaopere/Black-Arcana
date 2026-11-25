#!/usr/bin/env python3
"""Exact, read-only extension: effect lifecycle and Gingerbread target type operands.
No provider/engine classes loaded, no mutation, no static certificate promotion.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
from zipfile import ZipFile
from contextlib import ExitStack

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze
from alexscaves_1010_nuclear_explosion_effect_probe import numeric, MATH, bootstrap

P = "com/github/alexmodguy/alexscaves/server/"
MC = "net/minecraft/"
GOAL = P+"entity/ai/GingerbreadManStealGoal"
HANDLER = P+"misc/ACPlatform$ItemHandlerAccess"
EFFECT = MC+"world/effect/MobEffectInstance"
LIVING = MC+"world/entity/LivingEntity"
FOOD = MC+"world/food/FoodData"
PINS = {
    GOAL: "b6ae64af30ce2ff6432a8ae610b5f8b1244c1456e1ad1397b1221e30fd7a738b",
    HANDLER: "0e8340413b59be264dbd16824be21425439fddf48fc7d27a68c1f1ffd32ff92d",
    EFFECT: "a4336ebb7e30be8538b2f93f23f3d69e74c8e35e6b0a051e1bef705bd7a9695f",
    LIVING: "52130dfb8dc4b5c48ec1ef12bf19b40ff29f6e38fc25b02b94202553f75ce5f4",
    FOOD: "40f96f8f4f7f4194542370145cedb9908d4dc1630ee363b04503ee9153aff65c",
}
METHOD_PINS = {
    (GOAL,"canStealFromEntityType","(Lnet/minecraft/world/entity/Entity;)Z"):
        "45bb21045d88050e186e94235feab21fe14af050e19ffe608f77cdbb9da034f8",
    (HANDLER,"takeOne","(I)Lnet/minecraft/world/item/ItemStack;"):
        "25727ad1b559496542bd46c92d9b51c2bbe0c3bbed5aca1df3bb69f0a99bbf2c",
    (EFFECT,"update","(Lnet/minecraft/world/effect/MobEffectInstance;)Z"):
        "3a78f4d49785b4657224cc5410bac4642e29b844a26ddfc37a36641a42dde3bf",
    (EFFECT,"isShorterDurationThan","(Lnet/minecraft/world/effect/MobEffectInstance;)Z"):
        "32afcd883827d50f6b9a79172c6a7e3e18ef78fb77049d9f272ac833e27c2205",
    (LIVING,"addEffect","(Lnet/minecraft/world/effect/MobEffectInstance;Lnet/minecraft/world/entity/Entity;)Z"):
        "612bacd43ba4d0a5e2d94df479997582ccc4d2306a14ebbd65c6daa80c400776",
    (FOOD,"add","(IF)V"):
        "9742a98e4b36cc8bd77a34ce66dca114f66af0208986f179e7db9e212109c7e2",
}
# Names in this set are discovery filters, not claims of declarations.
CANDIDATES = {
    EFFECT: {"tick","tickDownDuration","isInfiniteDuration","hasRemainingDuration","mapDuration"},
    LIVING: {"tickEffects","onEffectAdded","onEffectUpdated","onEffectRemoved"},
}
DIST = {
    "installer": ("0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60", 6972109),
    "server": ("1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359", 5675624),
    "srg": ("26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71", 14246609),
    "universal": ("1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956", 3551255),
}
EXPECTED_SOURCE = {GOAL:"publisher",HANDLER:"publisher",EFFECT:"server",LIVING:"server",FOOD:"srg"}
LIMITS = {"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
          "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
          "provider_universe_closed":False,"semantic_magic_roots_delta":0,
          "installed_runtime":"NOT_OBSERVED","effective_inventory_capability":"NOT_VERIFIED",
          "actual_effect_acceptance":"NOT_VERIFIED"}
TYPE_OPS = {"instanceof","checkcast","new","anewarray","multianewarray"}

def type_sites(reader, body):
    result = []
    for at,(op,arg,_) in sorted(body.items()):
        if op not in TYPE_OPS:
            continue
        match = re.match(r"#(\d+)(?:\s|,|$)",arg)
        require(match is not None,"type operand missing constant-pool index")
        index = int(match.group(1))
        require(0 < index < len(reader.pool) and reader.pool[index] is not None
                and reader.pool[index][0] == 7,"type operand not CONSTANT_Class")
        result.append({"offset":at,"opcode":op,"cp_index":index,"type":reader.resolve(index)})
    return result

def projection(reader, body, decl):
    row=analyze(reader,body,decl)
    row["instruction_sha256"]=summarize(reader,(decl["name"],decl["descriptor"]),body)["instruction_sha256"]
    row["type_operands"]=type_sites(reader,body)
    row["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym}
                             for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
    row["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
    row["bootstrap_links"]=bootstrap(reader,body)
    row["exception_handlers"]=decl.get("exception_handlers",[])
    return row

def scan(args):
    identity={}
    for name,(sha,size) in DIST.items():
        raw=getattr(args,name).read_bytes()
        require(len(raw)==size and digest(raw)==sha,"artifact identity mismatch "+name)
        identity[name]={"sha256":sha,"bytes":size}
    verify_artifact(args.publisher)
    identity["publisher"]={"sha1":SHA1,"sha256":SHA256,"bytes":SIZE}
    order=("server","universal","srg","publisher")
    seen=set()
    classes={}
    with ExitStack() as stack:
        archives={name:stack.enter_context(ZipFile(getattr(args,name))) for name in order}
        rosters={}
        for name,z in archives.items():
            roster=z.namelist()
            require(len(roster)==len(set(roster)),"duplicate archive path "+name)
            rosters[name]=set(roster)
        cp=":".join(str(getattr(args,name)) for name in order)
        for owner,sha in sorted(PINS.items()):
            owners=[name for name in order if owner+".class" in rosters[name]]
            require(bool(owners) and owners[0]==EXPECTED_SOURCE[owner],"class source changed "+owner)
            raw=archives[owners[0]].read(owner+".class")
            require(digest(raw)==sha,"class identity mismatch "+owner)
            reader=ClassReader(raw)
            require(reader.name==owner and reader.major==65,"class declaration mismatch "+owner)
            parsed=disassemble(cp,args.javap,owner)
            methods=[]
            for decl in reader.methods:
                key=(owner,decl["name"],decl["descriptor"])
                if key not in METHOD_PINS and decl["name"] not in CANDIDATES.get(owner,set()):
                    continue
                if "code_sha256" not in decl:
                    require(key not in METHOD_PINS,"pinned method lacks Code")
                    continue
                if key in METHOD_PINS:
                    require(decl["code_sha256"]==METHOD_PINS[key],"Code identity mismatch "+str(key))
                    seen.add(key)
                signature=key[1:]
                require(signature in parsed and bool(parsed[signature]),"missing parsed body "+str(key))
                methods.append(projection(reader,parsed[signature],decl))
            require(len(methods)<=40,"method roster budget")
            classes[owner]={"source":owners[0],"available_sources":owners,"class_sha256":sha,
                            "declared_methods":[{"name":m["name"],"descriptor":m["descriptor"]} for m in reader.methods],
                            "methods":methods}
    require(seen==set(METHOD_PINS),"missing pinned Code")
    goal=next(m for m in classes[GOAL]["methods"] if m["name"]=="canStealFromEntityType")
    types=[t for t in goal["type_operands"] if t["opcode"]=="instanceof"]
    require([t["offset"] for t in types]==[1,22],"target gate type sites drift")
    require(types[0]["type"]==MC+"world/entity/player/Player","player type gate drift")
    require(any(m["name"]=="isInfiniteDuration" for m in classes[EFFECT]["methods"]),
            "referenced duration method not resolved")
    return {"schema":1,"scope":"CHOCOLATE_STATUS_LIFECYCLE_AND_STEAL_TYPE_DISCOVERY_ONLY",
            "artifact":identity,"classes":classes,"limits":LIMITS}

def self_test():
    class Reader:
        pool=[None,(7,2),(1,"example/Type"),(10,())]
        def resolve(self,index):
            return self.pool[self.pool[index][1]][1]
    reader=Reader()
    result=type_sites(reader,{1:("instanceof","#1",""),4:("ifeq","9","")})
    require(result==[{"offset":1,"opcode":"instanceof","cp_index":1,"type":"example/Type"}],"positive type projection")
    for arg in ("","#0","#2","#3","#9"):
        try:
            type_sites(reader,{1:("instanceof",arg,"")})
        except ValueError:
            continue
        raise AssertionError("invalid type operand accepted "+arg)
    require(LIMITS["mutation"]=="NO_MUTATION","mutation policy")
    require(LIMITS["static_contract"]=="NOT_CERTIFIED","certification policy")
    print("PASS: 8 type-operand and policy checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in (*DIST,"publisher","output"):
        p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:
        self_test()
    else:
        require(all(getattr(args,n) for n in (*DIST,"publisher","output"))
                and not args.output.exists(),"write-once report and all artifacts required")
        result=scan(args)
        raw=canonical(result).encode()
        require(len(raw)<=2_000_000,"report budget")
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("xb") as handle:
            handle.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in result["classes"].items():
            print("OWNER",owner,row["source"],row["class_sha256"])
            for m in row["methods"]:
                print("SEMANTIC",canonical({"owner":owner,**m}).replace("\n"," "))
        print("DISCOVERY_ONLY NO_MUTATION")
