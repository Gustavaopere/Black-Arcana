#!/usr/bin/env python3
"""Read-only discovery of weapon identity and enchantment/attribute dispatch.
Exact distributed 21.1.250 and publisher 1.0.10; no game execution.
Reuses the bounded projection; the previous combat and durability seals are unchanged.
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
SOURCES = MC+"world/damagesource/DamageSources"
SOURCE = MC+"world/damagesource/DamageSource"
LIVING = MC+"world/entity/LivingEntity"
ENCH = MC+"world/item/enchantment/Enchantment"
HELPER = MC+"world/item/enchantment/EnchantmentHelper"
STACK = MC+"world/item/ItemStack"
ITEM = MC+"world/item/Item"
PLAYER = MC+"world/entity/player/Player"
MOB = MC+"world/entity/Mob"
TARGETED = MC+"world/item/enchantment/TargetedConditionalEffect"
SELECT = {
    SOURCES: {"<init>"},
    SOURCE: {"getWeaponItem"},
    LIVING: {"getWeaponItem","getMainHandItem","getOffhandItem","getItemInHand"},
    PLAYER: {"getWeaponItem","getMainHandItem","getItemBySlot"},
    MOB: {"getWeaponItem","getMainHandItem","getItemBySlot"},
    HELPER: {"modifyArmorEffectiveness","getDamageProtection","getEnchantmentLevel",
             "forEachModifier","runIterationOnItem"},
    ENCH: {"modifyDamageFilteredValue","modifyArmorEffectiveness","modifyDamageProtection",
           "getDamageProtection","getAttributeModifiers","forEachModifier"},
    STACK: {"getAttributeModifiers"},
    ITEM: {"getAttributeModifiers","getDefaultAttributeModifiers"},
    TARGETED: {"matches"},
    ENCH+"$1": {"<clinit>"},
    NF+"common/extensions/IItemStackExtension": {"getAttributeModifiers"},
    NF+"common/extensions/IItemExtension": {"getAttributeModifiers","getDefaultAttributeModifiers"},
    NF+"event/EventHooks": {"getItemAttributeModifiers"},
}
PREFIXES = {
    HELPER: ("lambda$modifyArmorEffectiveness$","lambda$getDamageProtection$",
             "lambda$getEnchantmentLevel$","lambda$forEachModifier$"),
    ENCH: ("lambda$modifyDamageFilteredValue$","lambda$modifyArmorEffectiveness$",
           "lambda$modifyDamageProtection$","lambda$getDamageProtection$"),
}
PINS = {
    SOURCES: "457e0716c0fbeb86b8a228822ce720d7bc91c8808ef43c9f78677b4b28a59a18",
    SOURCE: "6fed4e35eed364877b7cb4601045235d06f29c738b58a616b0bb98520b5f660f",
    LIVING: "52130dfb8dc4b5c48ec1ef12bf19b40ff29f6e38fc25b02b94202553f75ce5f4",
    ENCH: "39f7551189481b8cb331b88605792c75f239f6bd901e2e70c86ba61592a2ca7e",
    HELPER: "b5da85025991eb5d1c0cd361c1d76a12756768506236e571c2e0a3b550a771bb",
    STACK: "072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
}
KNOWN = {
    (HELPER,"runIterationOnItem","(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/enchantment/EnchantmentHelper$EnchantmentVisitor;)V"):
        "6b686fb46d4be3e95586bb5c6bb1e36bee35163ee19054efbff9a2ccc86cc30e",
}
# Only executable methods with exact prior typed owners are required.
# Candidate overrides, synthetic names and other downstream methods are recorded
# when present; their absence is not a claim about runtime dispatch.
REQUIRED = {
    SOURCE: {"getWeaponItem"},
    HELPER: {"modifyArmorEffectiveness","getDamageProtection","getEnchantmentLevel","forEachModifier","runIterationOnItem"},
    ENCH: {"modifyDamageFilteredValue"},
    TARGETED: {"matches"},
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
          "effective_enchantment_set":"NOT_VERIFIED","weapon_identity_runtime":"NOT_VERIFIED",
          "active_datapacks":"NOT_OBSERVED"}

def selected(owner, declaration):
    name=declaration["name"]
    return name in SELECT.get(owner, set()) or name.startswith(PREFIXES.get(owner, ()))

ATTRIBUTE_SIGNATURE = ("getAttributeModifiers", "()Lnet/minecraft/world/item/component/ItemAttributeModifiers;")

def reachable(roots, load):
    """Enumerate bounded declared hierarchy, recording paths, not runtime dispatch."""
    pending=[(root,[root]) for root in roots]
    visited={}
    while pending:
        owner,path=pending.pop(0)
        if owner in visited:
            continue
        require(len(visited)<64,"hierarchy budget")
        visited[owner]=path
        node=load(owner)
        if node is not None:
            pending.extend((parent,path+[parent]) for parent in
                           ([node.parent] if node.parent else [])+node.interfaces)
    return visited

def resolve_stack_attribute(archives, rosters, order, result):
    def load(owner):
        sources=[name for name in order if owner+".class" in rosters[name]]
        if not sources:
            return None
        reader=ClassReader(archives[sources[0]].read(owner+".class"))
        require(reader.name==owner,"hierarchy identity")
        return reader
    paths=reachable([STACK],load)
    candidates=[]
    for owner,path in paths.items():
        reader=load(owner)
        if reader is None:
            continue
        for d in reader.methods:
            if (d["name"],d["descriptor"])!=ATTRIBUTE_SIGNATURE:
                continue
            # An exact executable, non-static body must also have been projected.
            if "code_sha256" in d and not d["access"] & 0x0008:
                rows=[m for m in result.get(owner,{}).get("methods",[])
                      if (m["name"],m["descriptor"])==ATTRIBUTE_SIGNATURE
                      and m.get("executable") and m.get("code_sha256")==d["code_sha256"]]
                require(len(rows)==1,"reachable attribute body not projected "+owner)
                candidates.append({"owner":owner,"path":path,"code_sha256":d["code_sha256"]})
    require(bool(candidates),"no reachable executable attribute descriptor")
    return {"reference_owner":STACK,"name":ATTRIBUTE_SIGNATURE[0],
            "descriptor":ATTRIBUTE_SIGNATURE[1],"reachable_executable_declarations":candidates,
            "scope":"DECLARED_HIERARCHY_ONLY_NOT_RUNTIME_DISPATCH"}

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
        attribute_resolution=resolve_stack_attribute(archives,rosters,order,result)
    require(seen==set(KNOWN),"prior Code coverage mismatch")
    require(sum(len(v.get("methods",[])) for v in result.values())<=120,"total method budget")
    return {"schema":1,"artifacts":identity,"classes":result,"attribute_resolution":attribute_resolution,"limits":LIMITS}

def self_test():
    require(selected(SOURCE,{"name":"getWeaponItem"}),"weapon source")
    require(selected(HELPER,{"name":"lambda$modifyArmorEffectiveness$99"}),"callback prefix")
    require(selected(ENCH,{"name":"modifyDamageFilteredValue"}),"damage filter")
    require(not selected(HELPER,{"name":"modifyDamage"}),"previous combat scope unchanged")
    require(not selected(HELPER,{"name":"processDurabilityChange"}),"durability scope reused")
    require(not selected("foreign/Enchantment",{"name":"modifyDamageFilteredValue"}),"namespace boundary")
    require(all(names<=SELECT[owner] for owner,names in REQUIRED.items()),"required scope consistency")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    require(STACK not in REQUIRED and selected(STACK,{"name":ATTRIBUTE_SIGNATURE[0]}),
            "do not conflate reference and declaration")
    class Node:
        def __init__(self,parent=None,interfaces=()):
            self.parent=parent
            self.interfaces=list(interfaces)
    graph={"Stack":Node("Object",("Extension",)), "Extension":Node(None,("Base",)),
           "Base":Node(None,("Extension",))}
    paths=reachable(["Stack"],graph.get)
    require(paths=={"Stack":["Stack"],"Object":["Stack","Object"],
                    "Extension":["Stack","Extension"],"Base":["Stack","Extension","Base"]},
            "inherited declaration traversal with cycle and missing external ancestor")
    print("PASS: ten scope, hierarchy and policy checks")

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
        print("ATTRIBUTE_RESOLUTION",json.dumps(report["attribute_resolution"],sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
