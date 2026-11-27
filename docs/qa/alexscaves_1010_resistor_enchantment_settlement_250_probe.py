#!/usr/bin/env python3
"""Bounded read-only enchantment effect filtering and durability settlement discovery.

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
NF = "net/neoforged/neoforge/"
P = "com/github/alexmodguy/alexscaves/server/"
ENCH = MC+"world/item/enchantment/Enchantment"
HELPER = MC+"world/item/enchantment/EnchantmentHelper"
STACK = MC+"world/item/ItemStack"
HOOKS = NF+"event/EventHooks"
COMMON = NF+"common/CommonHooks"
STACKEXT = NF+"common/extensions/IItemStackExtension"
ITEMEXT = NF+"common/extensions/IItemExtension"
COMPAT = P+"misc/ACCompat"
SELECT = {
    ENCH: {"getEffects","itemContext","applyEffects","modifyDurabilityChange",
           "modifyItemFilteredCount","lambda$modifyItemFilteredCount$5","matchingSlot"},
    HELPER: {"processDurabilityChange","lambda$processDurabilityChange$0","runIterationOnItem"},
    STACK: {"getEnchantments","getTagEnchantments","hurtAndBreak","isDamageableItem","getDamageValue","setDamageValue"},
    HOOKS: {"getAllEnchantmentLevels","getEnchantmentLevelSpecific"},
    COMMON: {"resolveLookup"},
    STACKEXT: {"getAllEnchantments","getEnchantmentLevel"},
    ITEMEXT: {"getAllEnchantments","getEnchantmentLevel"},
    COMPAT: {"enchantLevel","hurtAndBreakUsedHand"},
    MC+"world/item/enchantment/ConditionalEffect":{"matches","effect","requirements","<init>"},
    MC+"world/item/enchantment/effects/EnchantmentValueEffect":{"process"},
    MC+"world/item/enchantment/effects/RemoveBinomial":{"process","<init>","chance"},
    MC+"world/item/enchantment/LevelBasedValue$Linear":{"calculate","<init>"},
    MC+"world/item/enchantment/LevelBasedValue$Constant":{"calculate","<init>"},
    MC+"world/level/storage/loot/LootContext$Builder":{"create","withOptionalRandomSource","<init>"},
    MC+"world/level/storage/loot/LootParams$Builder":{"create","withParameter","withOptionalParameter","<init>"},
    MC+"world/level/storage/loot/predicates/LootItemCondition":{"test"},
    NF+"event/enchanting/GetEnchantmentLevelEvent":{"<init>","getEnchantments","getEnchantmentLevel","setEnchantmentLevel","getLevel","setLevel","getLookup"},
    NF+"event/enchanting/GetEnchantmentLevelEvent$EnchantmentLevel":{"<init>","getLevel","setLevel"},
}
PINS = {
    ENCH:"39f7551189481b8cb331b88605792c75f239f6bd901e2e70c86ba61592a2ca7e",
    HELPER:"b5da85025991eb5d1c0cd361c1d76a12756768506236e571c2e0a3b550a771bb",
    STACK:"072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
    HOOKS:"f810377f87c95c04bb4de7a7ac68e8f4862f9ca33a34cc74e067e65e2a92d66b",
    COMMON:"86c8a56c77fff474bf4fe90f0354ad32698f018b5e19dc52a2725ee5ff96c73e",
    STACKEXT:"244993a9cd1a5e99507c88a0a8e1d65b6ef997d44bd73ab696a510ccf2d0397e",
    ITEMEXT:"d65a413962ab6bf6cf8c33119b010dd16fcf482c114b8ae8abe5c59da951b088",
    COMPAT:"333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
}
KNOWN = {
    (ENCH,"modifyDurabilityChange","(Lnet/minecraft/server/level/ServerLevel;ILnet/minecraft/world/item/ItemStack;Lorg/apache/commons/lang3/mutable/MutableFloat;)V"):
        "875341b3fcf8e245e748255c106de30a32d98f5df71f9e6d462d06966af34f06",
    (ENCH,"modifyItemFilteredCount","(Lnet/minecraft/core/component/DataComponentType;Lnet/minecraft/server/level/ServerLevel;ILnet/minecraft/world/item/ItemStack;Lorg/apache/commons/lang3/mutable/MutableFloat;)V"):
        "e4eafe1199563036eb1f6f45eda9bee29ea722bd2c3607d3e44c7945a0257124",
    (ENCH,"lambda$modifyItemFilteredCount$5","(Lorg/apache/commons/lang3/mutable/MutableFloat;ILnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/item/enchantment/effects/EnchantmentValueEffect;)V"):
        "e143d89bc5f041153fef3feb4d5b29d167eaac75877ce0c5bb94dd2eb8e74d15",
    (HELPER,"processDurabilityChange","(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/item/ItemStack;I)I"):
        "89a14566218ef8a9b87dd342bc5e6c6fc148253f4fcfb2a95c2ba2fd7ff275b9",
    (HELPER,"runIterationOnItem","(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/enchantment/EnchantmentHelper$EnchantmentVisitor;)V"):
        "6b686fb46d4be3e95586bb5c6bb1e36bee35163ee19054efbff9a2ccc86cc30e",
    (COMMON,"resolveLookup","(Lnet/minecraft/resources/ResourceKey;)Lnet/minecraft/core/HolderLookup$RegistryLookup;"):
        "90ff10aa28f4c35fa065d4d9ad7ac7090d1b787d7eb7b647746e76b56431753b",
    (STACKEXT,"getAllEnchantments","(Lnet/minecraft/core/HolderLookup$RegistryLookup;)Lnet/minecraft/world/item/enchantment/ItemEnchantments;"):
        "62fe211295ef711e36898365cac4ad9fb40730bd21da18f33d405fac960c2987",
}
REQUIRED = {
    ENCH:{"getEffects","itemContext","applyEffects","modifyDurabilityChange","modifyItemFilteredCount","lambda$modifyItemFilteredCount$5"},
    HELPER:{"processDurabilityChange","lambda$processDurabilityChange$0","runIterationOnItem"},
    HOOKS:{"getAllEnchantmentLevels","getEnchantmentLevelSpecific"},
    STACKEXT:{"getAllEnchantments","getEnchantmentLevel"},
    ITEMEXT:{"getAllEnchantments","getEnchantmentLevel"},
    COMPAT:{"enchantLevel","hurtAndBreakUsedHand"},
    COMMON:{"resolveLookup"},
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
          "effective_enchantment_set":"NOT_VERIFIED","durability_settlement":"NOT_VERIFIED",
          "active_datapacks":"NOT_OBSERVED"}

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
        resources={}
        path="data/minecraft/enchantment/unbreaking.json"
        for name in order:
            if path in rosters[name]:
                raw=archives[name].read(path)
                require(len(raw)<=65536,"unbreaking resource budget")
                data=json.loads(raw)
                require(isinstance(data,dict),"unbreaking resource shape")
                resources[name]={"path":path,"sha256":digest(raw),"bytes":len(raw),
                                 "effects":data.get("effects"),"slots":data.get("slots")}
        # Resource absence from selected distributions is reported explicitly,
        # not converted into absence in the effective vanilla registry.
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
    return {"schema":1,"artifacts":identity,"classes":result,"unbreaking_resource_candidates":resources,"limits":LIMITS}

def self_test():
    require(selected(ENCH,{"name":"applyEffects"}),"filter selection")
    require(selected(HOOKS,{"name":"getAllEnchantmentLevels"}),"hook selection")
    require(selected(HELPER,{"name":"lambda$processDurabilityChange$0"}),"observed handle")
    require(not selected(ENCH,{"name":"unrelated"}),"scope")
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
        print("RESOURCE_CANDIDATES",json.dumps(report["unbreaking_resource_candidates"],sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
