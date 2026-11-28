#!/usr/bin/env python3
"""Read-only Purple Soda Bottle Rocket publisher + distributed engine audit."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import identified, projection
from alexscaves_1010_destroyed_item_engine_reference import ARTIFACTS, verify_artifact as verify_universal

P = "com/github/alexmodguy/alexscaves/server/"
MC = "net/minecraft/"
NF = "net/neoforged/neoforge/"
ROCKET = P+"entity/item/SodaBottleRocketEntity"
ITEM = P+"item/SodaBottleRocketItem"
IR, ER = P+"item/ACItemRegistry", P+"entity/ACEntityRegistry"
FIREWORK = MC+"world/entity/projectile/FireworkRocketEntity"
PROJECTILE = MC+"world/entity/projectile/Projectile"
COMPAT = P+"misc/ACCompat"
ALL = {ROCKET, ITEM, FIREWORK}
SELECT = {
    IR: {"lambda$static$191"},
    ER: {"lambda$static$81"},
    COMPAT: {"hasTag"},
    PROJECTILE: {"setOwner","getOwner","addAdditionalSaveData","readAdditionalSaveData","onHit","canHitEntity","tick"},
    MC+"world/item/ItemStack": {"get","getOrDefault","copy","shrink"},
    MC+"world/entity/Entity": {"getDeltaMovement","setDeltaMovement","discard","getId"},
    MC+"world/entity/LivingEntity": {"isFallFlying","getLookAngle","hurt"},
    MC+"world/item/component/Fireworks": {"<init>","flightDuration","explosions"},
    MC+"world/item/component/FireworkExplosion": {"<init>"},
    MC+"world/damagesource/DamageSources": {"fireworks"},
    NF+"event/EventHooks": {"onProjectileImpact"},
}
REQUIRED = {ROCKET:{"<init>","tick","getItem","handleEntityEvent"},
            ITEM:{"<init>","use","useOn"},
            FIREWORK:{"<init>","tick","getItem","defineSynchedData","addAdditionalSaveData","readAdditionalSaveData"},
            IR:{"lambda$static$191"},ER:{"lambda$static$81"},COMPAT:{"hasTag"},
            PROJECTILE:{"setOwner","getOwner"}}
PINS = {ROCKET:"73a4d9bb64f255503ffeca52e8576aa4570052a75ba7c87767bb9ff8b9d53877",
        ITEM:"bbc633c61e6226a10cbf00bce158c2a272d3a7f1ee40dd03b3a049d8c957fb42",
        IR:"114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1",
        ER:"7d7c91ddbb534d7c0e86a590ef7d7c3154ec2a628153c31e9fc7318a4b29e072",
        COMPAT:"333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b"}
CODE_PINS = {(ROCKET,"<init>","(Lnet/minecraft/world/level/Level;DDDLnet/minecraft/world/item/ItemStack;)V"):
             "2593b82d9b9bca3de8485f870d73f147a564a5f279e14ee5b04ab373ea23b298",
             (ROCKET,"tick","()V"):"bd67a7ad6729d27559db4d396e51b3e0ce1c4a44a4327adbf31103d5e909ec7f",
             (IR,"lambda$static$191","()Lnet/minecraft/world/item/Item;"):"4dc589cd486b67dc65677e0388911cb53182ffdfb49ca2459bf226a07bb96d72"}
LIMITS = {"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
          "mutation":"NO_MUTATION","runtime_loaded_bytes":"NOT_OBSERVED","semantic_magic_roots_delta":0}
def inspect(a):
    verify_artifact(a.publisher)
    verify_universal(a.universal,"universal")
    artifact = {"publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "installer":identified(a.installer,"0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60",6972109),
        "server":identified(a.server,"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",5675624),
        "srg":identified(a.srg,"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",14246609),
        "universal":ARTIFACTS["universal"]}
    classes, observed = {}, set()
    with ZipFile(a.server) as ov, ZipFile(a.universal) as uni, ZipFile(a.srg) as mc, ZipFile(a.publisher) as mod:
        archives=[("NEOFORGE_OVERLAY",ov),("NEOFORGE_UNIVERSAL",uni),("MINECRAFT_SRG",mc),("PUBLISHER",mod)]
        for _,z in archives:
            require(len(z.namelist())==len(set(z.namelist())),"duplicate path")
        cp=":".join(map(str,(a.server,a.universal,a.srg,a.publisher)))
        for owner in sorted(ALL|set(SELECT)):
            found=[(name,z) for name,z in archives if owner+".class" in z.namelist()]
            if not found:
                require(owner not in REQUIRED,"required owner absent "+owner)
                classes[owner]={"present":False};continue
            source,z=found[0];raw=z.read(owner+".class");rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity "+owner)
            require(owner not in PINS or digest(raw)==PINS[owner],"class pin "+owner)
            if owner==ROCKET: require(rd.parent==FIREWORK,"exact parent")
            decls=[d for d in rd.methods if owner in ALL or d["name"] in SELECT.get(owner,set())]
            require(REQUIRED.get(owner,set())<={d["name"] for d in decls},"required method absent "+owner)
            require(len(decls)<=120,"method budget")
            parsed=disassemble(cp,a.javap,owner)
            methods=[]
            for d in decls:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False});continue
                require(key in parsed and 0<len(parsed[key])<=5000,"body budget "+owner+str(key))
                pin=(owner,*key)
                if pin in CODE_PINS:
                    require(d["code_sha256"]==CODE_PINS[pin],"Code pin "+str(pin));observed.add(pin)
                methods.append({"executable":True,**projection(rd,key,parsed[key],d)})
            if owner in ALL:
                require({(d["name"],d["descriptor"]) for d in decls if "code_sha256" in d}==
                        {k for k,v in parsed.items() if v},"complete method roster "+owner)
            classes[owner]={"present":True,"source":source,"available_sources":[n for n,_ in found],
                "class_sha256":digest(raw),"parent":rd.parent,"fields":rd.fields,"declarations":rd.methods,"methods":methods}
        require(observed==set(CODE_PINS),"all Code pins observed")
    return {"schema":1,"scope":"SODA_ROCKET_DISTRIBUTED_ENGINE_DISCOVERY","artifact":artifact,"classes":classes,"limits":LIMITS}
def self_test():
    require(ALL=={ROCKET,ITEM,FIREWORK} and ALL<=set(REQUIRED),"complete owner scope")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS bounded scope and fail-closed policy")
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("installer","server","srg","universal","publisher","output"):
        p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(all(getattr(a,n) for n in ("installer","server","srg","universal","publisher","output")),"all inputs")
        require(not a.output.exists(),"write-once")
        result=inspect(a);raw=canonical(result).encode()
        require(len(raw)<=8_000_000,"report byte budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in result["classes"].items():
            print("OWNER",owner,row.get("source"),row.get("class_sha256"),"METHODS",len(row.get("methods",[])))
            for method in row.get("methods",[]):
                print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")
