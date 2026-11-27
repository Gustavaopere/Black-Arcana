#!/usr/bin/env python3
"""Read-only Cinder Brick impact, block authority, dispenser and registry discovery.
Publisher and distributed NeoForge 21.1.250 references, not transformed runtime.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection, identified, verify_universal, ARTIFACTS
from alexscaves_1010_remote_detonator_block_callbacks_probe import registry

P = "com/github/alexmodguy/alexscaves/server/"
M = "net/minecraft/"
I = P+"item/ThrownProjectileItem"
W = P+"entity/item/CinderBrickEntity"
R = P+"entity/ACEntityRegistry"
IR = P+"item/ACItemRegistry"
D = IR+"$2"
T = P+"misc/ACTagRegistry"
ALL = {I,W,D}
FACTORIES = {
    "lambda$static$63":"6170bbfd08b2836ed9e776a6faf4682e4f9708646716c0160e13bcc32986c125",
    "lambda$static$62":"bac38bfbe1e84aa5e44899e89c1c1f99fb192995ee71d1ea50d65e1c155b1c6b",
}
SELECT = {
    IR: set(FACTORIES),
    M+"world/level/Level": {"destroyBlock","setBlock","getBlockState","getFluidState"},
    M+"world/level/LevelAccessor": {"destroyBlock"},
    M+"world/level/LevelWriter": {"destroyBlock","setBlock","removeBlock"},
    M+"world/level/block/Block": {"getExplosionResistance","dropResources","getDrops","playerDestroy"},
    M+"world/level/block/state/BlockBehaviour$BlockStateBase": {"is","isAir","getBlock","getDrops"},
    M+"world/level/block/state/BlockState": {"is","isAir","getBlock"},
    M+"world/entity/projectile/Projectile": {"onHit","onHitEntity","onHitBlock","hitTargetOrDeflectSelf","setOwner","getOwner","addAdditionalSaveData","readAdditionalSaveData","shootFromRotation","canHitEntity"},
    M+"world/entity/projectile/ThrowableProjectile": {"<init>","tick","getDefaultGravity"},
    M+"world/entity/projectile/ThrowableItemProjectile": {"<init>","setItem","getItem","addAdditionalSaveData","readAdditionalSaveData"},
    M+"world/entity/EntityType$Builder": {"sized","setUpdateInterval","setShouldReceiveVelocityUpdates","build"},
    M+"world/entity/EntityType": {"getDimensions","clientTrackingRange","updateInterval","trackDeltas"},
    M+"world/damagesource/DamageSources": {"thrown"},
    M+"world/item/ItemStack": {"shrink","getCount","setCount","copyWithCount"},
    P+"misc/AbstractProjectileDispenseBehavior": {"execute","getProjectile","getPower","getUncertainty"},
    M+"core/dispenser/DefaultDispenseItemBehavior": {"dispense"},
    M+"world/level/block/DispenserBlock": {"registerBehavior","getDispensePosition"},
    M+"server/level/ServerLevel": {"addFreshEntity","addEntity"},
    "net/neoforged/neoforge/event/EventHooks": {"onProjectileImpact","onBlockBreak"},
}
REQUIRED = {
    I: {"<init>","use"},
    W: {"<init>","onHitEntity","onHit","getDefaultItem"},
    D: {"<init>","getProjectile"},
    IR: set(FACTORIES),
    M+"world/level/Level": {"destroyBlock"},
    M+"world/level/block/Block": {"getExplosionResistance","dropResources"},
    M+"world/entity/projectile/ThrowableProjectile": {"tick"},
    M+"world/entity/projectile/ThrowableItemProjectile": {"setItem","getItem"},
    M+"world/damagesource/DamageSources": {"thrown"},
    P+"misc/AbstractProjectileDispenseBehavior": {"execute"},
    M+"server/level/ServerLevel": {"addFreshEntity"},
}
PINS = {
    I:"925fb7047dddc8044929b0a581af2a4dcf5c6688dd277f445c9bc0dbd1f9d57d",
    W:"d09510632ca5e4dbb367227830291074fb6f94c1d39bc8fce368db0bf3a76a53",
    P+"misc/AbstractProjectileDispenseBehavior":"1f733bdb487927c5d4f5d995c439c0bd8de4f611b239128c4f5a70bb88ce15a0",
}
RESOURCES = {
    "assets/alexscaves/models/item/cinder_brick.json":"7d738ea07d4d3f596242aa02220dabce47a6d420d98b6510e1793bf20e319769",
    "data/alexscaves/recipe/cinder_brick.json":"6f9e801364c5eb742faa4586ef6af12bd1ec911772921f059f105657de705738",
}
LIMITS = {"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
          "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
          "runtime_loaded_bytes":"NOT_OBSERVED","provider_universe_closed":False,
          "semantic_magic_roots_delta":0,"actual_effect_acceptance":"NOT_VERIFIED"}

MEMBER_OPS = {"getstatic","putstatic","getfield","putfield","invokestatic","invokevirtual","invokespecial","invokeinterface"}

def member_at(rd, instruction):
    op,arg,_ = instruction
    if op not in MEMBER_OPS:
        return None
    match=re.match(r"#(\d+)(?:\s|,|$)",arg)
    require(match is not None,"unresolved member operand")
    idx=int(match[1])
    require(0<idx<len(rd.pool) and rd.pool[idx][0] in (9,10,11),"invalid member operand")
    tag,owner,signature=rd.resolve(idx)
    return {"kind":tag,"owner":owner,"name":signature[1],"descriptor":signature[2],"cp_index":idx}

def census_sites(rd, parsed, refs):
    indices={r["index"] for r in refs}
    declarations={(m["name"],m["descriptor"]):m for m in rd.methods}
    result=[]
    for key,body in sorted(parsed.items()):
        offsets=sorted(body)
        members={at:member_at(rd,body[at]) for at in offsets if body[at][0] in MEMBER_OPS}
        hits=[at for at,v in members.items() if v["cp_index"] in indices]
        if not hits:
            continue
        require(key in declarations,"site method missing declaration")
        require(len(hits)<=100,"site budget")
        windows=[]
        for at in hits:
            i=offsets.index(at)
            around=offsets[max(0,i-12):i+13]
            windows.append({"offset":at,"member":members[at],
                "context":[{"offset":a,"opcode":body[a][0],
                            **({"member":members[a]} if a in members else {}),
                            **({"literal":body[a][2]} if body[a][2].startswith("String ") else {})}
                           for a in around]})
        result.append({"name":key[0],"descriptor":key[1],"code_sha256":declarations[key]["code_sha256"],
                       "instruction_count":len(body),"member_count":len(members),"coverage":"EXACT_TARGET_SITES_AND_BOUNDED_CONTEXT",
                       "sites":windows})
    require(len(result)<=100,"consumer method site budget")
    return result

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
        require(bool(reg["bootstrap_links"]),"cinder entity registry handle absent")
        factories={x["method"] for x in reg["nested_factories"]} | {x["method"] for x in reg["constructor_factories"]}
        require(bool(factories),"cinder entity registry factory absent")
        select[R]=factories
        required[R]=factories
        resources={}
        for path,expected in RESOURCES.items():
            raw=mod.read(path)
            require(digest(raw)==expected,"resource pin "+path)
            resources[path]={"sha256":digest(raw),"bytes":len(raw),"data":json.loads(raw)}
        # Inventory only matching shipped tags, not effective datapack resolution.
        tags=[p for p in sorted(mod.namelist()) if "/tags/" in p and p.endswith(".json")
              and any(x in p.rsplit("/",1)[-1] for x in ("unmoveable","unmovable","concrete"))]
        require(len(tags)<=40,"tag candidate budget")
        for path in tags:
            raw=mod.read(path)
            resources[path]={"sha256":digest(raw),"bytes":len(raw),"data":json.loads(raw)}
        census=[]
        for owner,field in [(IR,"CINDER_BRICK"),(T,"UNMOVEABLE")]:
            raw=mod.read(owner+".class")
            rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"registry identity")
            refs=[x for x in rd.typed_refs(owner) if x.get("kind")=="field_reference" and x.get("name")==field]
            require(bool(refs),"registry field ref absent "+field)
            sites=census_sites(rd,disassemble(args.publisher,args.javap,owner),refs)
            require(any(x["name"]=="<clinit>" for x in sites),"registry initialization absent "+field)
            census.append({"owner":owner,"class_sha256":digest(raw),"refs":refs,"methods":sites})
        require(any(m["name"]=="setup" for m in census[0]["methods"]),"dispenser registration site absent")
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
            if owner==D:
                require(rd.parent==P+"misc/AbstractProjectileDispenseBehavior","dispenser superclass mismatch")
            if owner==P+"misc/AbstractProjectileDispenseBehavior":
                require(any(d["name"]=="execute" and d.get("code_sha256")=="b44158b7c89f9a6f6e5473c1e0de31a90057ef824782947e0646fe0a2335e6ef" for d in rd.methods),"dispenser execute Code pin")
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
    report={"schema_version":1,"scope":"CINDER_BRICK_WORLD_DISCOVERY_ONLY",
            "artifact":artifact,"classes":classes,"entity_registry":reg,"resources":resources,"registry_sites":census,"limits":LIMITS}
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
    print("REGISTRY_SITES",json.dumps(census,sort_keys=True))
    print("RESOURCES",json.dumps(resources,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")

def self_test():
    require(set(PINS) <= ALL | set(SELECT),"pins out of scope")
    require(len(FACTORIES)==2 and len(RESOURCES)==2,"identity pins")
    require(REQUIRED[W] >= {"onHit","onHitEntity"},"impact coverage")
    require(REQUIRED[D] >= {"getProjectile"},"dispenser coverage")
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
