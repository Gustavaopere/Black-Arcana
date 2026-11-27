#!/usr/bin/env python3
"""Read-only Depth Charge own tick, MineExplosion and inherited engine discovery.
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
W = P+"entity/item/DepthChargeEntity"
X = P+"entity/util/MineExplosion"
C = P+"misc/ACPlatform"
K = P+"misc/ACCompat"
R = P+"entity/ACEntityRegistry"
IR = P+"item/ACItemRegistry"
ALL = {I,W,X}
FACTORIES = {
    "lambda$static$112":"620d93b80cee080c5a16582cdc36b279266c396c9c32312ab22b450cb5394f5c",
    "lambda$static$113":"5b5396ac73dc271445003cefeda4e6066978b2df1997228de0b035949d3a39f8",
}
SELECT = {
    IR: set(FACTORIES),
    C: {"canEntityGrief"},
    K: {"gameRule"},
    M+"world/entity/Entity": {"baseTick","move","getY","remove","getInBlockState","checkInsideBlocks","isInWater"},
    M+"world/entity/projectile/Projectile": {"onHit","onHitEntity","getOwner","setOwner","addAdditionalSaveData","readAdditionalSaveData","updateRotation","shootFromRotation"},
    M+"world/entity/projectile/ThrowableProjectile": {"<init>","tick"},
    M+"world/entity/projectile/ThrowableItemProjectile": {"<init>","setItem","getItem","addAdditionalSaveData","readAdditionalSaveData"},
    M+"world/entity/EntityType$Builder": {"sized","setUpdateInterval","setShouldReceiveVelocityUpdates","build"},
    M+"world/level/Explosion": {"<init>","getDirectSourceEntity","getIndirectSourceEntity","getDamageSource","getToBlow","getHitPlayers","interactsWithBlocks","getSeenPercent"},
    M+"world/level/ExplosionDamageCalculator": {"getBlockExplosionResistance","shouldBlockExplode","shouldDamageEntity","getEntityDamageAmount","getKnockbackMultiplier"},
    M+"world/level/EntityBasedExplosionDamageCalculator": {"getBlockExplosionResistance","shouldBlockExplode"},
    M+"world/level/Level": {"getEntities","getBlockState","getFluidState","destroyBlock"},
    M+"world/level/block/state/BlockBehaviour$BlockStateBase": {"onExplosionHit"},
    M+"world/damagesource/DamageSources": {"thrown","explosion"},
    M+"server/level/ServerLevel": {"addFreshEntity","addEntity"},
    "net/neoforged/neoforge/event/EventHooks": {"onExplosionStart","onExplosionDetonate","getMobGriefingEvent"},
    "net/neoforged/neoforge/common/CommonHooks": {"canEntityGrief"},
}
REQUIRED = {
    I: {"<init>","use"},
    W: {"<init>","tick","explode","onHit","onHitEntity","getDefaultItem"},
    X: {"<init>","explode","finalizeExplosion"},
    IR: set(FACTORIES),
    C: {"canEntityGrief"},
    K: {"gameRule"},
    M+"world/entity/Entity": {"baseTick","move","getY","remove"},
    M+"world/level/Explosion": {"<init>"},
    M+"world/damagesource/DamageSources": {"thrown","explosion"},
}
PINS = {
    I:"925fb7047dddc8044929b0a581af2a4dcf5c6688dd277f445c9bc0dbd1f9d57d",
    W:"d9ecff8deceecb68e066b3675a8835206698180d77a846150dba94eea96094ca",
}
LIMITS = {"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
          "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
          "runtime_loaded_bytes":"NOT_OBSERVED","provider_universe_closed":False,
          "semantic_magic_roots_delta":0,"actual_effect_acceptance":"NOT_VERIFIED",
          "world_safety":"BLOCKED"}

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
        require(bool(reg["bootstrap_links"]),"depth charge entity registry handle absent")
        factories={x["method"] for x in reg["nested_factories"]} | {x["method"] for x in reg["constructor_factories"]}
        require(bool(factories),"depth charge entity registry factory absent")
        select[R]=factories
        required[R]=factories
        path="assets/alexscaves/models/item/depth_charge.json"
        raw=mod.read(path)
        require(digest(raw)=="f8ae5ab1ee385e03594e596f8664f500223ebf9b0edeccd3e4ca8ce5d9aece48","model pin")
        resources={path:{"sha256":digest(raw),"bytes":len(raw),"data":json.loads(raw)}}
        consumers=[]
        for path in sorted(p for p in mod.namelist() if p.endswith(".class")):
            rd=ClassReader(mod.read(path))
            require(rd.name+".class"==path and rd.major==65,"publisher class identity")
            refs=rd.typed_refs(X)
            if refs:
                consumers.append({"owner":rd.name,"typed_refs":refs})
        require(len(consumers)<=40 and any(x["owner"]==W for x in consumers),"mine explosion census")
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
                print("PROJECTING",owner,key[0],key[1],flush=True)
                methods.append({"executable":True,**projection(rd,key,parsed[key],d)})
            if owner in ALL:
                require({(d["name"],d["descriptor"]) for d in decls if "code_sha256" in d} ==
                        {k for k,v in parsed.items() if v},"complete executable roster mismatch "+owner)
            if owner == IR:
                for name,expected in FACTORIES.items():
                    require(any(d["name"]==name and d.get("code_sha256")==expected for d in decls),"factory Code pin "+name)
            classes[owner]={"present":True,"source":source,"available_sources":[k for k,_ in found],
                            "class_sha256":sha,"parent":rd.parent,"interfaces":rd.interfaces,
                            "fields":rd.fields,"declarations":rd.methods,"methods":methods}
    report={"schema_version":1,"scope":"DEPTH_CHARGE_MINE_EXPLOSION_DISCOVERY_ONLY",
            "artifact":artifact,"classes":classes,"entity_registry":reg,"resources":resources,"mine_explosion_consumers":consumers,"limits":LIMITS}
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
    print("CONSUMERS",json.dumps(consumers,sort_keys=True))
    print("RESOURCES",json.dumps(resources,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")

def self_test():
    require(set(PINS) <= ALL | set(SELECT),"pins out of scope")
    require(len(FACTORIES)==2,"identity pins")
    require(REQUIRED[W] >= {"tick","explode","onHit","onHitEntity"},"own tick coverage")
    require(REQUIRED[X] >= {"<init>","explode","finalizeExplosion"},"explosion coverage")
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
