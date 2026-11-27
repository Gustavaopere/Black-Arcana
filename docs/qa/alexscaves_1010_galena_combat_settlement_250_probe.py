#!/usr/bin/env python3
"""Read-only Galena combat source, attribution, and enchantment effect discovery.
Exact distributed NeoForge 21.1.250 and publisher 1.0.10. Reuse the existing
bounded method projection; no transformed runtime, damage application or mutation.
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
MODIFIERS = MC+"world/item/component/ItemAttributeModifiers"
RULES = MC+"world/damagesource/CombatRules"
SELECT = {
    SOURCES: {"source","mobAttack","generic"},
    SOURCE: {"<init>","getEntity","getDirectEntity","getSourcePosition","is"},
    LIVING: {"setLastHurtByPlayer","setLastHurtByMob","getDamageAfterArmorAbsorb",
             "getDamageAfterMagicAbsorb","getHealth","setHealth","checkTotemDeathProtection","die"},
    HELPER: {"modifyDamage","doPostAttackEffects","doPostAttackEffectsWithItemSource","runIterationOnEquipment"},
    ENCH: {"modifyDamage","doPostAttack","postAttack","entityContext","damageContext"},
    STACK: {"forEachModifier"},
    MODIFIERS: {"forEach","compute"},
    RULES: {"getDamageAfterAbsorb","getDamageAfterMagicAbsorb"},
}
PREFIXES = {
    HELPER: ("lambda$modifyDamage$","lambda$doPostAttackEffects$","lambda$doPostAttackEffectsWithItemSource$","lambda$runIterationOnEquipment$"),
    ENCH: ("lambda$modifyDamage$","lambda$doPostAttack$","lambda$postAttack$"),
}
PINS = {
    SOURCES: "457e0716c0fbeb86b8a228822ce720d7bc91c8808ef43c9f78677b4b28a59a18",
    LIVING: "52130dfb8dc4b5c48ec1ef12bf19b40ff29f6e38fc25b02b94202553f75ce5f4",
    ENCH: "39f7551189481b8cb331b88605792c75f239f6bd901e2e70c86ba61592a2ca7e",
    HELPER: "b5da85025991eb5d1c0cd361c1d76a12756768506236e571c2e0a3b550a771bb",
    STACK: "072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
}
KNOWN = {
    (SOURCES,"mobAttack","(Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/damagesource/DamageSource;"):
        "377a24515b1d83a1762a6121b3b3533d9c21359d76bb1a5a28344013c05d580c",
}
# Required names originate from earlier typed callsites. Other selections are discovery candidates.
REQUIRED = {
    SOURCES: {"source","mobAttack","generic"},
    SOURCE: {"getEntity","getDirectEntity"},
    LIVING: {"setLastHurtByPlayer","setLastHurtByMob","getDamageAfterArmorAbsorb",
             "getDamageAfterMagicAbsorb","getHealth","setHealth","checkTotemDeathProtection","die"},
    HELPER: {"modifyDamage","doPostAttackEffects"},
    STACK: {"forEachModifier"},
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
          "effective_enchantment_set":"NOT_VERIFIED","damage_and_kill_settlement":"NOT_VERIFIED",
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
        resources={}
        for path in ("data/minecraft/damage_type/mob_attack.json","data/minecraft/damage_type/generic.json"):
            for name in order:
                if path in rosters[name]:
                    raw=archives[name].read(path)
                    require(len(raw)<=65536,"damage resource budget")
                    data=json.loads(raw)
                    require(isinstance(data,dict),"damage resource shape")
                    resources[name+":"+path]={"path":path,"sha256":digest(raw),"bytes":len(raw),
                        "scaling":data.get("scaling"),"exhaustion":data.get("exhaustion"),
                        "effects":data.get("effects"),"message_id":data.get("message_id"),
                        "death_message_type":data.get("death_message_type")}
        # An absent candidate is not evidence of an absent effective registry entry.
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
    return {"schema":1,"artifacts":identity,"classes":result,"damage_type_resource_candidates":resources,"limits":LIMITS}

def self_test():
    require(selected(SOURCES,{"name":"mobAttack"}),"source selection")
    require(selected(LIVING,{"name":"setLastHurtByPlayer"}),"attribution selection")
    require(selected(HELPER,{"name":"lambda$modifyDamage$99"}),"callback prefix")
    require(not selected(HELPER,{"name":"lambda$processDurabilityChange$0"}),"do not repeat durability scope")
    require(not selected("foreign/Enchantment",{"name":"modifyDamage"}),"namespace boundary")
    require(all(names<=SELECT[owner] for owner,names in REQUIRED.items()),"required scope consistency")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS: seven scope and policy checks")

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
        print("RESOURCE_CANDIDATES",json.dumps(report["damage_type_resource_candidates"],sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
