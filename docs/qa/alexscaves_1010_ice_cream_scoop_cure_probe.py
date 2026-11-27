#!/usr/bin/env python3
"""Read-only three Ice Cream Scoop variants, milk cure and inherited projectile boundaries.
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
I = P+"item/ThrownProjectileItem"
W = P+"entity/item/ThrownIceCreamScoopEntity"
C = P+"misc/ACPlatform"
R = P+"entity/ACEntityRegistry"
IR = P+"item/ACItemRegistry"
L = M+"world/entity/LivingEntity"
ALL = {I,W}
FACTORIES = {
    "lambda$static$166":"b1207d3c3493cba9f22a6a9f795d105ae5176c5ba075726e0b9f4280c72d1609",
    "lambda$static$168":"4c62609bf9f25265d90a3f88bffd4493e6362f978abda2161d7f97ea9ec9ac28",
    "lambda$static$170":"b8243502eff7adfa97638db4839e654631ff1cf86a89b85cbba221b3a5be8052",
    **{f"lambda$static${n}":"512e6c38b9e98613519743dc5bbc34cff32de2d237b4486a74b02dbf5c2867a4" for n in (165,167,169)},
}
FIELDS = {"CHOCOLATE_ICE_CREAM_SCOOP","SWEETBERRY_ICE_CREAM_SCOOP","VANILLA_ICE_CREAM_SCOOP"}
SELECT = {
    C: {"cureWithMilk"},
    IR: set(FACTORIES) | {"setup"},
    L: {"removeEffectsCuredBy","removeAllEffects","removeEffect","removeEffectNoUpdate","onEffectRemoved"},
    M+"world/effect/MobEffectInstance": {"getCures","getEffect"},
    M+"world/effect/MobEffect": {"fillEffectCures","removeAttributeModifiers"},
    M+"world/item/MilkBucketItem": {"finishUsingItem"},
    M+"world/entity/projectile/Projectile": {"onHit","onHitEntity","hitTargetOrDeflectSelf","setOwner","getOwner","addAdditionalSaveData","readAdditionalSaveData","shootFromRotation","canHitEntity"},
    M+"world/entity/projectile/ThrowableProjectile": {"<init>","tick","getDefaultGravity"},
    M+"world/entity/projectile/ThrowableItemProjectile": {"<init>","setItem","getItem","addAdditionalSaveData","readAdditionalSaveData"},
    M+"world/entity/EntityType$Builder": {"sized","setUpdateInterval","setShouldReceiveVelocityUpdates","build"},
    M+"world/entity/EntityType": {"getDimensions","clientTrackingRange","updateInterval","trackDeltas"},
    M+"world/damagesource/DamageSources": {"thrown"},
    M+"world/item/ItemStack": {"shrink","getCount","setCount","copyWithCount"},
    M+"world/entity/player/Player": {"hasInfiniteMaterials","awardStat"},
    M+"server/level/ServerLevel": {"addFreshEntity","addEntity"},
    "net/neoforged/neoforge/event/EventHooks": {"onEffectRemoved","onProjectileImpact"},
    "net/neoforged/neoforge/common/EffectCures": {"<clinit>"},
}
REQUIRED = {
    I: {"<init>","use"},
    W: {"<init>","onHitEntity","onHit","getDefaultItem"},
    C: {"cureWithMilk"},
    IR: set(FACTORIES),
    L: {"removeEffect","removeEffectNoUpdate","onEffectRemoved"},
    M+"world/effect/MobEffect": {"removeAttributeModifiers"},
    M+"world/entity/projectile/Projectile": {"onHit","onHitEntity","setOwner","getOwner","shootFromRotation"},
    M+"world/entity/projectile/ThrowableProjectile": {"tick"},
    M+"world/entity/projectile/ThrowableItemProjectile": {"setItem","getItem"},
    M+"world/damagesource/DamageSources": {"thrown"},
    M+"server/level/ServerLevel": {"addFreshEntity"},
}
PINS = {
    I:"925fb7047dddc8044929b0a581af2a4dcf5c6688dd277f445c9bc0dbd1f9d57d",
    W:"5710f87a67dd8be88e05b1ac01dcc57a4d68f51bc9dc6e226d354fad05fde5e8",
}
MODELS = {
    "chocolate":"07d6f782959f521614b8c7945c33770cc4f55198774717029c1fb35970d83d73",
    "sweetberry":"ff35e43dfb5d0cd47bb8865e392903a1076a41e9098aed340c74c4c6fa1dd13b",
    "vanilla":"87e70240aff942d1b026910e02b80ce82cee216992e429d1a0aa97036fa6aec0",
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
        require(bool(reg["bootstrap_links"]),"scoop entity registry handle absent")
        factories={x["method"] for x in reg["nested_factories"]} | {x["method"] for x in reg["constructor_factories"]}
        require(bool(factories),"scoop entity registry factory absent")
        select[R]=factories
        required[R]=factories
        resources={}
        for flavor, expected in MODELS.items():
            path=f"assets/alexscaves/models/item/{flavor}_ice_cream_scoop.json"
            raw=mod.read(path)
            require(digest(raw)==expected,"model pin "+flavor)
            resources[path]={"sha256":digest(raw),"bytes":len(raw),"data":json.loads(raw)}
        census=[]
        for path in sorted(mod.namelist()):
            if not path.endswith(".class"):
                continue
            rd=ClassReader(mod.read(path))
            refs=[x for x in rd.typed_refs(IR) if x.get("kind")=="field_reference" and x.get("name") in FIELDS]
            refs += [x for x in rd.typed_refs(C) if x.get("kind")=="method_reference" and x.get("name")=="cureWithMilk"]
            if refs:
                census.append({"owner":rd.name,"refs":refs})
                # Include methods using the exact member; no name-only owner guessing.
                parsed=disassemble(args.publisher,args.javap,rd.name)
                names=set()
                for k,body in parsed.items():
                    for offset,(op,operand,symbol) in body.items():
                        if op not in {"getstatic","putstatic","invokestatic"}:
                            continue
                        if any(operand.split(",")[0].strip()=="#"+str(x["index"]) for x in refs):
                            if k[0]!="<clinit>":
                                names.add(k[0])
                if names:
                    select.setdefault(rd.name,set()).update(names)
        require(len(census)<=40,"typed census owner budget")
        require(any(x["owner"]==W for x in census),"cure callsite absent")
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
            if owner == IR:
                for name,sha_expected in FACTORIES.items():
                    require(any(d["name"]==name and d.get("code_sha256")==sha_expected for d in decls),"factory Code pin "+name)
            classes[owner]={"present":True,"source":source,"available_sources":[k for k,_ in found],
                            "class_sha256":sha,"parent":rd.parent,"interfaces":rd.interfaces,
                            "fields":rd.fields,"declarations":rd.methods,"methods":methods}
    report={"schema_version":1,"scope":"ICE_CREAM_SCOOP_CURE_DISCOVERY_ONLY",
            "artifact":artifact,"classes":classes,"entity_registry":reg,"resources":resources,"typed_census":census,"limits":LIMITS}
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
    print("CENSUS",json.dumps(census,sort_keys=True))
    print("RESOURCES",json.dumps(resources,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")

def self_test():
    require(set(PINS) <= ALL | set(SELECT),"pins out of scope")
    require(len(FACTORIES)==6 and len(MODELS)==3,"variant coverage")
    require(REQUIRED[C]=={"cureWithMilk"},"milk cure coverage")
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
