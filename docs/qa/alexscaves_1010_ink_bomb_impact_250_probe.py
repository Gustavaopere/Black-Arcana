#!/usr/bin/env python3
"""Bounded exact Ink Bomb native impact, targeting and status registry discovery.

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
BOMB = P+"entity/item/InkBombEntity"
ITEM = P+"item/InkBombItem"
D3 = P+"item/ACItemRegistry$3"
D4 = P+"item/ACItemRegistry$4"
UTIL = MC+"world/entity/projectile/ProjectileUtil"
PROJECTILE = MC+"world/entity/projectile/Projectile"
THROWITEM = MC+"world/entity/projectile/ThrowableItemProjectile"
CLOUD = MC+"world/entity/AreaEffectCloud"
EFFECTS = MC+"world/effect/MobEffects"
DAMAGE = MC+"world/damagesource/DamageTypes"
ENTITY = MC+"world/entity/Entity"
LIVING = MC+"world/entity/LivingEntity"
SELECT = {
    BOMB: {"<clinit>","<init>","onHit","onHitEntity","getAddEntityPacket","getDefaultItem",
           "setGlowingBomb","isGlowingBomb","defineSynchedData","addAdditionalSaveData",
           "readAdditionalSaveData","handleEntityEvent"},
    ITEM: {"<init>","use"},
    D3: {"<init>","getProjectile"},
    D4: {"<init>","getProjectile"},
    UTIL: {"getHitResultOnMoveVector","getHitResult","getEntityHitResult","getHitResultOnViewVector"},
    PROJECTILE: {"canHitEntity","checkLeftOwner","hitTargetOrDeflectSelf","deflect","setOwner","getOwner"},
    THROWITEM: {"setItem","readAdditionalSaveData","addAdditionalSaveData","defineSynchedData"},
    CLOUD: {"getDimensions","onSyncedDataUpdated","setRadius","getRadius","isWaiting"},
    ENTITY: {"getFirstPassenger","canBeHitByProjectile","isCurrentlyGlowing","setGlowingTag"},
    LIVING: {"isAffectedByPotions","updateGlowingStatus","isCurrentlyGlowing","canBeAffected"},
    MC+"world/entity/player/Player": {"canSprint","isCurrentlyGlowing"},
    MC+"client/player/LocalPlayer": {"canStartSprinting","canSprint"},
    MC+"client/renderer/FogRenderer$BlindnessFogFunction": {"setupFog","getModifiedVoidDarkness"},
    MC+"world/entity/EntityDimensions": {"scalable","makeBoundingBox"},
    MC+"world/damagesource/DamageSources": {"thrown"},
    EFFECTS: {"<clinit>"},
    DAMAGE: {"<clinit>"},
}
PINS = {
    BOMB:"efce464cc9a4ade95cf15ba416935a6fc7a3b085b8295b45fe2b085b56344427",
    ITEM:"4d663e3810455f285e55f50a1fd6c75454d0c88c42fc241cc794e83a5f50162b",
    PROJECTILE:"d0c6d3fb293b2840ccb6a10906c7dfed90052c8511f35d059622ef7d7dad9d02",
    THROWITEM:"3665c07e17db9cda73827e80d281b97028e0dd30a5951ce139e117c689724547",
    CLOUD:"0e87f8bfa4ac02006ae2474f3739ccfd25ed2baceb41bf045c88792d309f0958",
    ENTITY:"4f65b7d5d4628e9f10a6a23e5a0f68814520d8019f4bc001924cd752c00eed84",
    LIVING:"52130dfb8dc4b5c48ec1ef12bf19b40ff29f6e38fc25b02b94202553f75ce5f4",
    MC+"world/damagesource/DamageSources":"457e0716c0fbeb86b8a228822ce720d7bc91c8808ef43c9f78677b4b28a59a18",
}
KNOWN = {
    (BOMB,"onHit","(Lnet/minecraft/world/phys/HitResult;)V"):
        "b6d048fa7c327f7b64e3417fc776f9dee6d30cf62e68a0d954774a5c30821436",
    (BOMB,"onHitEntity","(Lnet/minecraft/world/phys/EntityHitResult;)V"):
        "3bb50e81c9e4f051f4bfed310339d9c019ea5303032053120765181722e1a48f",
    (BOMB,"setGlowingBomb","(Z)V"):
        "c8338b4dc8bd89e9741566c3354556b74d16a828b1438793629b904117aae849",
    (BOMB,"readAdditionalSaveData","(Lnet/minecraft/nbt/CompoundTag;)V"):
        "55690571e8c031e5e7739528a0d2933b3ad5845dd3612bfd3cd3da7b35600b0d",
    (ITEM,"use","(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;"):
        "6b4fb3cd4eb6f2bf9873ce9bbf54705985ac050a5a95c6e8eb88f6b719d4b4a2",
    (THROWITEM,"setItem","(Lnet/minecraft/world/item/ItemStack;)V"):
        "342ca58804f1d89ec96ff7c5359e827563c025ca2af343d8ae8c6c252aa621",
    (CLOUD,"getDimensions","(Lnet/minecraft/world/entity/Pose;)Lnet/minecraft/world/entity/EntityDimensions;"):
        "b34f5152e4e7f88bc325ba24f30c835827dfbb99a572b9c82777f1054900cdeb",
    (PROJECTILE,"hitTargetOrDeflectSelf","(Lnet/minecraft/world/phys/HitResult;)Lnet/minecraft/world/entity/projectile/ProjectileDeflection;"):
        "a8efc3ef15eccd3b64830896f27554f86c9e62313aa2f89ac9a2c7777a239c83",
    (MC+"world/damagesource/DamageSources","thrown","(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;"):
        "6b46209a49fb0bb1ec39473978a8f425b03edc561f4fa5f6413a42f07093170b",
}
REQUIRED = {
    BOMB:SELECT[BOMB], ITEM:SELECT[ITEM], D3:SELECT[D3], D4:SELECT[D4],
    UTIL:{"getHitResultOnMoveVector","getEntityHitResult"},
    PROJECTILE:{"canHitEntity","checkLeftOwner","hitTargetOrDeflectSelf","deflect"},
    THROWITEM:{"setItem","readAdditionalSaveData"},
    CLOUD:{"getDimensions","setRadius","onSyncedDataUpdated"},
    ENTITY:{"getFirstPassenger","canBeHitByProjectile"},
    EFFECTS:{"<clinit>"}, DAMAGE:{"<clinit>"},
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
          "effective_status_acceptance":"NOT_VERIFIED","installed_client_effects":"NOT_OBSERVED"}

def registry_windows(owner, reader, body, decl):
    wanted = {"BLINDNESS","GLOWING","NIGHT_VISION","CONDUIT_POWER"} if owner==EFFECTS else {"THROWN"}
    offsets=sorted(body)
    sites={}
    for pos,at in enumerate(offsets):
        op,arg,sym=body[at]
        if op!="putstatic":
            continue
        for name in wanted:
            if "Field "+name+":" not in sym:
                continue
            require(name not in sites,"duplicate registry write "+name)
            sites[name]={"offset":at,"window":[{"offset":v,"opcode":body[v][0],"operand":body[v][1],"symbol":body[v][2]}
                             for v in offsets[max(0,pos-24):pos+2]]}
    require(set(sites)==wanted,"required registry write absent "+owner)
    return {"name":decl["name"],"descriptor":decl["descriptor"],"code_sha256":decl["code_sha256"],
            "instruction_count":len(body),"projection":"BOUNDED_REGISTRY_WRITE_WINDOWS_ONLY","sites":sites}

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
            require(len(declarations)<=40,"per-owner method budget")
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
                row=registry_windows(owner,reader,parsed[key],d) if owner in (EFFECTS,DAMAGE) else projection(reader,key,parsed[key],d)
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
    require(selected(BOMB,{"name":"onHitEntity"}),"native impact")
    require(selected(D4,{"name":"getProjectile"}),"glowing dispenser")
    require(selected(EFFECTS,{"name":"<clinit>"}),"effect registry")
    require(not selected("foreign/InkBombEntity",{"name":"onHit"}),"namespace")
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
