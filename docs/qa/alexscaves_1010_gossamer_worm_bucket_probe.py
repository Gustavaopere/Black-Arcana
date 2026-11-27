#!/usr/bin/env python3
"""Read-only Gossamer Worm Bucket identity, native bucket and spawn boundaries.
Publisher-exact 1.0.10 and distributed NeoForge 21.1.250, not loaded runtime.
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

P="com/github/alexmodguy/alexscaves/server/"
M="net/minecraft/"
N="net/neoforged/neoforge/"
I=P+"item/ModFishBucketItem"
IR=P+"item/ACItemRegistry"
ER=P+"entity/ACEntityRegistry"
C=P+"misc/ACCompat"
ET=M+"world/entity/EntityType"
BU=M+"world/item/BucketItem"
MB=M+"world/item/MobBucketItem"
BA=M+"world/entity/animal/Bucketable"
SL=M+"server/level/ServerLevel"
SELECT={
    IR:{"lambda$static$92","lambda$static$91"},
    C:{"getOrCreateTag"},
    BU:{"use","emptyContents","getEmptySuccessItem","checkExtraContent","playEmptySound","getContent"},
    MB:{"<init>","checkExtraContent","spawn","appendHoverText","playEmptySound"},
    BA:{"bucketMobPickup","saveDefaultDataToBucketTag","loadDefaultDataFromBucketTag","getBucketItemStack","saveToBucketTag","loadFromBucketTag","setFromBucket","fromBucket"},
    ET:{"spawn","create","createDefaultStackConfig","createDefaultStackConfigForMob","updateCustomEntityTag"},
    SL:{"addFreshEntity","addEntity","tryAddFreshEntityWithPassengers","addWithUUID"},
    M+"world/item/ItemUtils":{"createFilledResult"},
    M+"world/level/block/DispenserBlock":{"getDispenseMethod","dispenseFrom"},
    M+"world/level/Level":{"mayInteract"},
    N+"event/EventHooks":{"onBucketUse","onEntityJoinLevel","onFinalizeSpawn","onPlayerInteractEntity"},
}
REQUIRED={
    I:{"<init>","checkExtraContent","spawnFish","addExtraAttributes","appendHoverText"},
    IR:{"lambda$static$92","lambda$static$91"},
    C:{"getOrCreateTag"},
    BU:{"use","emptyContents"},
    BA:{"bucketMobPickup"},
    ET:{"spawn"},
    SL:{"addFreshEntity","addEntity"},
}
PINS={I:"9d22e586625f298993fbbf86b59ff2369cc3dccd9a9115b23d52778ed4c112dc",
      IR:"114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1"}
CODE_PINS={
    (IR,"lambda$static$92"):"6ee50396f6047acee481212ad62d3c4cbd750e9f550376efcf754d6068cb5eae",
    (I,"spawnFish"):"bd106b4cdeed0c33da4a95b9fe241ce074bebe0f7404a8d863d9ded5a9233945",
    (I,"checkExtraContent"):"9afd208eba966e70dffc5385cd7ea9cfe66cc0b4cbe2d5629ff94fee058eb89b",
}
EXACT={ET:{("spawn","(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/entity/MobSpawnType;ZZ)Lnet/minecraft/world/entity/Entity;")},
       C:{("getOrCreateTag","(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/nbt/CompoundTag;")}}
ENTITY_METHODS={"<init>","mobInteract","interact","getBucketItemStack","saveToBucketTag","loadFromBucketTag","setFromBucket","fromBucket","getPickupSound","addAdditionalSaveData","readAdditionalSaveData","defineSynchedData","requiresCustomPersistence","removeWhenFarAway","finalizeSpawn"}
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","mutation":"NO_MUTATION","provider_universe_closed":False,"semantic_magic_roots_delta":0,"runtime_loaded_bytes":"NOT_OBSERVED","actual_spawn_acceptance":"NOT_VERIFIED"}

def inspect(a):
    verify_artifact(a.publisher)
    verify_universal(a.universal,"universal")
    require(not a.output.exists(),"write-once report")
    artifact={"publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "installer":identified(a.installer,"0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60",6972109),
        "server":identified(a.server,"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",5675624),
        "srg":identified(a.srg,"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",14246609),
        "universal":ARTIFACTS["universal"],"neoforge_version":"21.1.250"}
    with ZipFile(a.server) as ov, ZipFile(a.universal) as uni, ZipFile(a.srg) as mc, ZipFile(a.publisher) as mod:
        archives=[("NEOFORGE_OVERLAY",ov),("NEOFORGE_UNIVERSAL",uni),("MINECRAFT_SRG",mc),("PUBLISHER",mod)]
        for _,z in archives:
            require(len(z.namelist())==len(set(z.namelist())),"duplicate archive entry")
        roster=[(n,z,set(z.namelist())) for n,z in archives]
        cp=":".join(map(str,(a.server,a.universal,a.srg,a.publisher)))
        classes=sorted(p[:-6] for p in mod.namelist() if p.endswith(".class"))
        require(len(classes)==1555,"publisher roster")
        require(digest(("\n".join(x+".class" for x in classes)+"\n").encode())=="2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed","class roster pin")
        # Resolve named candidates from the binary, then require registry linkage.
        entities=[x for x in classes if x.rsplit("/",1)[-1]=="GossamerWormEntity"]
        dispensers=[x for x in classes if x.rsplit("/",1)[-1]=="FluidContainerDispenseItemBehavior"]
        require(len(entities)==1 and len(dispensers)==1,"entity or dispenser candidate missing/ambiguous")
        entity=entities[0]; dispenser=dispensers[0]
        reg=registry(mod,a.publisher,a.javap,ER,{entity})
        require(any("gossamer_worm" in json.dumps(row).lower() for row in reg["bootstrap_links"]),"gossamer registry identity")
        select={k:set(v) for k,v in SELECT.items()}
        select[ER]={x["method"] for x in reg["nested_factories"]+reg["constructor_factories"]}
        require(bool(select[ER]),"entity factory missing")
        # Actual superclass chain, not inferred from the entity's name.
        lineage=[]; cursor=entity
        for _ in range(16):
            if cursor is None or cursor=="java/lang/Object":
                break
            found=[(n,z) for n,z,paths in roster if cursor+".class" in paths]
            if not found:
                break
            rd=ClassReader(found[0][1].read(cursor+".class"))
            require(rd.name==cursor,"lineage identity")
            lineage.append({"owner":cursor,"parent":rd.parent,"interfaces":rd.interfaces,"source":found[0][0]})
            select.setdefault(cursor,set()).update(ENTITY_METHODS if found[0][0]=="PUBLISHER" else ENTITY_METHODS-{"<init>","finalizeSpawn"})
            cursor=rd.parent
        require(len(lineage)<16 and any(x["owner"]==entity for x in lineage),"lineage budget")
        all_own={I,dispenser}
        consumers=[]
        for owner in classes:
            rd=ClassReader(mod.read(owner+".class"))
            require(rd.name==owner and rd.major==65,"publisher identity")
            match={t:rd.typed_refs(t) for t in sorted({I,entity,dispenser})}
            match={t:refs for t,refs in match.items() if refs or rd.parent==t or t in rd.interfaces}
            if match:
                consumers.append({"owner":owner,"refs":match,"parent":rd.parent})
        require(len(consumers)<=100,"typed consumer budget")
        records={}
        for owner in sorted(all_own|set(select)):
            found=[(n,z) for n,z,paths in roster if owner+".class" in paths]
            if not found:
                require(owner not in REQUIRED,"required owner absent "+owner)
                records[owner]={"present":False}
                continue
            source,z=found[0]; raw=z.read(owner+".class"); rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"owner identity "+owner)
            require(owner not in PINS or digest(raw)==PINS[owner],"prior class pin "+owner)
            decls=[d for d in rd.methods if owner in all_own or d["name"] in select.get(owner,set())]
            require(REQUIRED.get(owner,set())<={d["name"] for d in decls},"required method absent "+owner)
            require(EXACT.get(owner,set())<={(d["name"],d["descriptor"]) for d in decls if "code_sha256" in d},"exact call descriptor absent "+owner)
            require(len(decls)<=120,"method budget "+owner)
            parsed=disassemble(cp,a.javap,owner)
            methods=[]
            for d in decls:
                key=(d["name"],d["descriptor"])
                pin=CODE_PINS.get((owner,key[0]))
                require(pin is None or d.get("code_sha256")==pin,"prior Code pin "+owner)
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]),"body missing "+owner+str(key))
                print("PROJECTING",owner,*key,flush=True)
                methods.append({"executable":True,**projection(rd,key,parsed[key],d)})
            records[owner]={"present":True,"source":source,"class_sha256":digest(raw),"parent":rd.parent,"interfaces":rd.interfaces,"fields":rd.fields,"declarations":rd.methods,"methods":methods}
        resources={}
        for path in sorted(p for p in mod.namelist() if p.endswith(".json") and "gossamer_worm" in p.lower()):
            raw=mod.read(path)
            require(len(raw)<=100000,"resource size")
            resources[path]={"sha256":digest(raw),"bytes":len(raw),"data":json.loads(raw)}
        require(resources.get("assets/alexscaves/models/item/gossamer_worm_bucket.json",{}).get("sha256")=="b78cc41faf66a35938ce69ba9935026346186c89a2f1507571bbdb54b9b6945c","model pin")
    report={"schema_version":1,"scope":"GOSSAMER_WORM_BUCKET_DISCOVERY_ONLY","artifact":artifact,"entity":entity,"dispenser":dispenser,"registry":reg,"lineage":lineage,"classes":records,"typed_consumers":consumers,"resources":resources,"limits":LIMITS}
    data=canonical(report).encode()
    require(len(data)<=10000000,"report byte budget")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("xb") as out:
        out.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"OWNERS",len(records))
    for owner,row in records.items():
        print("OWNER",owner,row.get("source"),row.get("class_sha256"),"METHODS",len(row.get("methods",[])))
        for method in row.get("methods",[]):
            print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
    print("REGISTRY",json.dumps(reg,sort_keys=True))
    print("LINEAGE",json.dumps(lineage,sort_keys=True))
    print("CONSUMERS",json.dumps(consumers,sort_keys=True))
    print("RESOURCES",json.dumps(resources,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")

def self_test():
    require(set(PINS)=={I,IR},"prior identity pin scope")
    require({"lambda$static$91","lambda$static$92"}<=REQUIRED[IR],"fluid supplier/identity")
    require(all(set(n for n,d in values)<=SELECT[owner] for owner,values in EXACT.items()),"exact descriptor selector scope")
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
