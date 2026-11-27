#!/usr/bin/env python3
"""Read-only Ortholance, WaveEntity and inherited engine boundary discovery.
Publisher and distributed NeoForge 21.1.250 references, not transformed runtime.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection, identified, verify_universal, ARTIFACTS
from alexscaves_1010_remote_detonator_block_callbacks_probe import registry

P = "com/github/alexmodguy/alexscaves/server/"
M = "net/minecraft/"
I = P+"item/OrtholanceItem"
W = P+"entity/item/WaveEntity"
C = P+"misc/ACCompat"
R = P+"entity/ACEntityRegistry"
ALL = {I,W}
SELECT = {
    C: {"attackDamageBonus","lambda$attackDamageBonus$2","itemAttributes","enchantLevel",
        "hurtAndBreakUsedHand","hurtAndBreak","hurt","knockback","useConsume"},
    M+"world/item/ItemStack": {"hurtAndBreak","isDamageableItem","getDamageValue","getMaxDamage","getAttributeModifiers","forEachModifier","getEnchantments","shrink","grow","setCount"},
    M+"world/item/component/ItemAttributeModifiers": {"forEach","compute"},
    M+"world/entity/Entity": {"setDeltaMovement","getDeltaMovement","move","isAlliedTo","stopRiding","getTeam","getBoundingBox","getViewVector","getEyePosition"},
    M+"world/entity/LivingEntity": {"hurt","knockback","hasLineOfSight","getUsedItemHand","startUsingItem","releaseUsingItem"},
    M+"world/entity/player/Player": {"isAlliedTo","canHarmPlayer","attack"},
    M+"world/entity/EntityType$Builder": {"sized","setUpdateInterval","setShouldReceiveVelocityUpdates","build"},
    M+"world/damagesource/DamageSources": {"mobAttack","mobProjectile"},
    M+"world/level/Level": {"clip","getEntitiesOfClass"},
    M+"world/level/EntityGetter": {"getEntitiesOfClass"},
    M+"world/level/BlockGetter": {"clip"},
    M+"server/level/ServerLevel": {"addFreshEntity","addEntity","getEntity"},
    M+"world/phys/AABB": {"<init>","inflate","intersects"},
    M+"world/phys/Vec3": {"normalize","scale","multiply","add","yRot"},
    M+"world/item/enchantment/EnchantmentHelper": {"processDurabilityChange"},
}
REQUIRED = {
    I: {"<init>","releaseUsing","acHurtEnemy","use","mineBlock","getDefaultAttributeModifiers"},
    W: {"<init>","tick","attackEntities","getOwner","setOwner","getDimensions","addAdditionalSaveData","readAdditionalSaveData"},
    C: {"attackDamageBonus","enchantLevel","hurtAndBreakUsedHand","hurt","knockback","itemAttributes"},
    M+"world/item/ItemStack": {"hurtAndBreak","isDamageableItem"},
    M+"world/entity/LivingEntity": {"hasLineOfSight","knockback"},
    M+"world/damagesource/DamageSources": {"mobAttack","mobProjectile"},
    M+"server/level/ServerLevel": {"addFreshEntity","addEntity"},
}
PINS = {
    I:"996b208a60f2c26c275e60e5d0e3a2fd0090cfb0ba1687907cac242de9a17d09",
    W:"93fdaee0239cc4985b351a6c2ac1edd23a51cf0088cb1172f983d0f869d9e42e",
    C:"333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
}
LIMITS = {"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
          "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
          "runtime_loaded_bytes":"NOT_OBSERVED","provider_universe_closed":False,
          "semantic_magic_roots_delta":0,"actual_effect_acceptance":"NOT_VERIFIED"}

def inspect(args):
    select = {k:set(v) for k,v in SELECT.items()}
    required = {k:set(v) for k,v in REQUIRED.items()}
    verify_artifact(args.publisher)
    verify_universal(args.universal, "universal")
    require(not args.output.exists(), "write-once report required")
    artifact = {
        "publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "neoforge_version":"21.1.250",
        "installer":identified(args.installer,"0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60",6972109),
        "server":identified(args.server,"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",5675624),
        "srg":identified(args.srg,"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",14246609),
        "universal":ARTIFACTS["universal"],
    }
    with ZipFile(args.server) as ov, ZipFile(args.universal) as uni, ZipFile(args.srg) as mc, ZipFile(args.publisher) as mod:
        archives = [("NEOFORGE_OVERLAY",ov),("NEOFORGE_UNIVERSAL",uni),("MINECRAFT_SRG",mc),("PUBLISHER",mod)]
        for _, z in archives:
            require(len(z.namelist()) == len(set(z.namelist())), "duplicate archive path")
        roster = [(name,z,set(z.namelist())) for name,z in archives]
        cp = ":".join(map(str,(args.server,args.universal,args.srg,args.publisher)))
        require(sum(p.endswith(".class") for p in mod.namelist())==1555,"publisher class roster")
        reg=registry(mod,args.publisher,args.javap,R,{W})
        require(bool(reg["bootstrap_links"]),"wave registry handle absent")
        factories={x["method"] for x in reg["nested_factories"]}
        require(bool(factories),"wave registry factory absent")
        select[R]=factories
        required[R]=factories
        classes = {}
        for owner in sorted(ALL | set(select)):
            found = [(name,z) for name,z,entries in roster if owner+".class" in entries]
            if not found:
                require(owner not in required,"required owner absent "+owner)
                classes[owner] = {"present":False}
                continue
            source,z = found[0]
            raw=z.read(owner+".class")
            sha=digest(raw)
            rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity "+owner)
            require(owner not in PINS or sha==PINS[owner],"prior class pin "+owner)
            decls=[d for d in rd.methods if owner in ALL or d["name"] in select.get(owner,set())]
            require(required.get(owner,set()) <= {d["name"] for d in decls},"required declaration absent "+owner)
            require(len(decls)<=120,"method budget "+owner)
            parsed=disassemble(cp,args.javap,owner)
            methods=[]
            for d in decls:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and parsed[key],"body absent "+owner+str(key))
                methods.append({"executable":True,**projection(rd,key,parsed[key],d)})
            if owner in ALL:
                require({(d["name"],d["descriptor"]) for d in decls if "code_sha256" in d} ==
                        {k for k,v in parsed.items() if v},"complete executable roster mismatch "+owner)
            classes[owner]={"present":True,"source":source,"available_sources":[k for k,_ in found],
                            "class_sha256":sha,"parent":rd.parent,"interfaces":rd.interfaces,
                            "fields":rd.fields,"declarations":rd.methods,"methods":methods}
    report={"schema_version":1,"scope":"ORTHOLANCE_ENGINE_DISCOVERY_ONLY",
            "artifact":artifact,"classes":classes,"entity_registry":reg,"limits":LIMITS}
    data=canonical(report).encode()
    require(len(data)<=10_000_000,"report byte budget")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("xb") as f:
        f.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"OWNERS",len(classes))
    for owner,row in classes.items():
        print("OWNER",owner,row.get("source"),row.get("class_sha256"),"METHODS",len(row.get("methods",[])))
        for method in row.get("methods",[]):
            print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
    print("REGISTRY",json.dumps(reg,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")

def self_test():
    require(set(PINS) <= ALL | set(SELECT),"pins out of scope")
    require(REQUIRED[I] >= {"releaseUsing","acHurtEnemy"},"producer coverage")
    require(REQUIRED[W] >= {"tick","attackEntities","getOwner"},"wave coverage")
    require(LIMITS["static_contract"]=="NOT_CERTIFIED" and LIMITS["mutation"]=="NO_MUTATION","policy")
    print("PASS: discovery scope and policy guards")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("installer","server","srg","universal","publisher","output"):
        p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all(getattr(a,n) for n in ("installer","server","srg","universal","publisher","output")),"all inputs required")
        inspect(a)
