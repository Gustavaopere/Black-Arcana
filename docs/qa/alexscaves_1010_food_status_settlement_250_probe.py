#!/usr/bin/env python3
"""Read-only exact chocolate consumption and status/phantom event boundaries.
Distributed server classes, not physical consumption or accepted effects.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap, numeric, MATH
from alexscaves_1010_destroyed_item_engine_reference import verify_artifact as verify_universal

MC = "net/minecraft/"
NF = "net/neoforged/neoforge/"
P = "com/github/alexmodguy/alexscaves/server/"
HOT=P+"item/HotChocolateBottleItem"
BOTTLE=P+"item/DrinkableBottledItem"
LIVING=MC+"world/entity/LivingEntity"
PLAYER=MC+"world/entity/player/Player"
FOOD=MC+"world/food/FoodProperties"
HOOKS=NF+"event/EventHooks"
COMMON=NF+"common/CommonHooks"
PHANTOM=NF+"event/entity/player/PlayerSpawnPhantomsEvent"
EFFECT=NF+"event/entity/living/MobEffectEvent"
STAT=NF+"event/StatAwardEvent"
PIN = {
    HOT:"69f1d7676c60ede59dc3cb552b7877914d95fa94b89e6d8ce753bdec41191d39",
    BOTTLE:"2d51cafe21c91f964887b30b3ebf262bd8d5944d0879fd08df668623763bd713",
    LIVING:"52130dfb8dc4b5c48ec1ef12bf19b40ff29f6e38fc25b02b94202553f75ce5f4",
    HOOKS:"f810377f87c95c04bb4de7a7ac68e8f4862f9ca33a34cc74e067e65e2a92d66b",
    COMMON:"86c8a56c77fff474bf4fe90f0354ad32698f018b5e19dc52a2725ee5ff96c73e",
    MC+"stats/StatsCounter":"e769405f3dd11b371e307efe0e55cb60f59a6190cb3f501fcd1eb50f6c48a449",
}
UNIVERSAL_SHA="1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956"
UNIVERSAL_SIZE=3551255
ALL_BODIES={HOT,BOTTLE,PHANTOM,STAT,EFFECT+"$Applicable",EFFECT+"$Added",EFFECT+"$Remove",FOOD+"$PossibleEffect"}
SELECTED={
    P+"item/SackOfSatingItem":{"overrideOtherStackedOnMe","calculateWholeStackHungerValue"},
    P+"item/ACFoods":{"lambda$static$39"},
    MC+"world/item/Item":{"finishUsingItem","use","getFoodProperties"},
    MC+"world/item/ItemUtils":{"startUsingInstantly"},
    MC+"world/item/ItemStack":{"finishUsingItem","consume","getFoodProperties","use"},
    LIVING:{"eat","addEatEffect","completeUsingItem","startUsingItem","addEffect","removeEffect"},
    PLAYER:{"eat","addItem","drop"},
    MC+"world/food/FoodData":{"eat","add"},
    FOOD:{"eatDurationTicks","<init>"},
    NF+"common/extensions/IItemExtension":{"getFoodProperties"},
    NF+"common/extensions/IItemStackExtension":{"getFoodProperties"},
    HOOKS:{"onEffectRemoved","onStatAward","firePlayerSpawnPhantoms","onItemUseFinish","onItemUseStart","onItemUseTick"},
    COMMON:{"canMobEffectBeApplied"},
    MC+"stats/StatsCounter":{"getValue","setValue"},
    MC+"stats/ServerStatsCounter":{"setValue"},
    MC+"server/level/ServerPlayer":{"resetStat"},
    MC+"world/damagesource/DamageSources":{"thrown","source"},
    MC+"world/damagesource/DamageSource":{"<init>","getEntity","getDirectEntity","isIndirect"},
    MC+"world/effect/MobEffectInstance":{"<init>","update","isShorterDurationThan","getDuration","getAmplifier","mapDuration"},
}
REQUIRED={
    HOT:{"<init>","finishUsingItem"},
    BOTTLE:{"<init>","finishUsingItem","getUseDuration","use"},
    P+"item/ACFoods":{"lambda$static$39"},
    MC+"world/item/Item":{"finishUsingItem"},
    MC+"world/item/ItemUtils":{"startUsingInstantly"},
    MC+"world/item/ItemStack":{"consume","getFoodProperties"},
    LIVING:{"eat","addEatEffect","completeUsingItem","addEffect","removeEffect"},
    PLAYER:{"eat"},
    MC+"world/food/FoodData":{"eat"},
    FOOD+"$PossibleEffect":{"effect"},
    HOOKS:{"onEffectRemoved","onStatAward","firePlayerSpawnPhantoms","onItemUseFinish"},
    COMMON:{"canMobEffectBeApplied"},
    PHANTOM:{"shouldSpawnPhantoms","getPhantomsToSpawn","getResult"},
    STAT:{"getStat","getValue"},
    MC+"world/damagesource/DamageSources":{"thrown","source"},
}
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
        "mutation":"NO_MUTATION","provider_universe_closed":False,"semantic_magic_roots_delta":0,
        "actual_food_and_container_settlement":"NOT_VERIFIED","actual_effect_acceptance":"NOT_VERIFIED",
        "actual_phantom_spawn":"NOT_VERIFIED","runtime_loaded_bytes":"NOT_OBSERVED"}
def selected(owner,name):
    return owner in ALL_BODIES or name in SELECTED.get(owner,())

def scan(installer,server,srg,universal,publisher,javap):
    identity={'neoforge_version':'21.1.250','minecraft_version':'1.21.1'}
    for label,path,expected,expected_size in (
        ('installer',installer,'0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60',6972109),
        ('server',server,'1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359',5675624),
        ('srg',srg,'26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71',14246609)):
        raw=path.read_bytes()
        require(digest(raw)==expected and len(raw)==expected_size,'physical-ledger distribution pin '+label)
        identity[label]={'sha256':expected,'bytes':expected_size}
    verify_universal(universal,'universal')
    verify_artifact(publisher)
    identity['publisher']={'sha1':SHA1,'sha256':SHA256,'size_bytes':SIZE}
    data=universal.read_bytes()
    require(len(data)==UNIVERSAL_SIZE and hashlib.sha256(data).hexdigest()==UNIVERSAL_SHA,"universal pin mismatch")
    identity.update({"universal_sha256":UNIVERSAL_SHA,"universal_bytes":UNIVERSAL_SIZE})
    owners=sorted(ALL_BODIES|set(SELECTED))
    with ZipFile(server) as overlay, ZipFile(universal) as uni, ZipFile(srg) as vanilla, ZipFile(publisher) as mod:
        archives=[("NEOFORGE_OVERLAY",overlay),("NEOFORGE_UNIVERSAL",uni),("INSTALLED_MINECRAFT_SRG",vanilla),("PUBLISHER",mod)]
        for _,z in archives:
            require(len(z.namelist())==len(set(z.namelist())),"duplicate archive entry")
        roster=[(name,z,set(z.namelist())) for name,z in archives]
        classpath=":".join(map(str,(server,universal,srg,publisher)))
        classes={}
        for owner in owners:
            found=[(name,z) for name,z,entries in roster if owner+".class" in entries]
            if not found:
                require(owner not in REQUIRED,"required owner absent "+owner)
                classes[owner]={"present":False}
                continue
            source,z=found[0]
            raw=z.read(owner+".class")
            sha=digest(raw)
            require(owner not in PIN or sha==PIN[owner],"class SHA drift "+owner)
            reader=ClassReader(raw)
            require(reader.name==owner and reader.major==65,"owner/Java drift "+owner)
            declarations=[m for m in reader.methods if selected(owner,m["name"])]
            require(REQUIRED.get(owner,set()).issubset({m["name"] for m in declarations}),"required method absent "+owner)
            require(len(declarations)<=100,"method roster budget "+owner)
            parsed=disassemble(classpath,javap,owner)
            methods=[]
            for d in declarations:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]),"missing body "+owner+str(key))
                body=parsed[key]
                print("PROJECT_METHOD",owner,*key,flush=True)
                row=analyze(reader,body,d)
                row["instruction_sha256"]=summarize(reader,key,body)["instruction_sha256"]
                row["executable"]=True
                row["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym} for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
                row["strings"]=[{"offset":at,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if op.startswith("ldc") and sym.startswith("String ")]
                row["bootstrap_links"]=bootstrap(reader,body)
                row["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
                row["local_accesses"]=[{"offset":at,"opcode":op,"slot_operand":arg} for at,(op,arg,_) in sorted(body.items()) if op.startswith(("dload","dstore","fload","fstore","iload","istore","aload","astore")) or op=="iinc"]
                methods.append(row)
            classes[owner]={"present":True,"source":source,"available_sources":[name for name,_ in found],"class_sha256":sha,
                            "parent":reader.parent,"interfaces":reader.interfaces,
                            "declared_methods":[{"name":m["name"],"descriptor":m["descriptor"]} for m in reader.methods],
                            "methods":methods}
    return {"schema_version":1,"scope":"FOOD_STATUS_SETTLEMENT_250_DISTRIBUTED_DISCOVERY_ONLY","artifact":identity,"classes":classes,"limits":LIMITS}

def self_test():
    require(selected(HOT,"finishUsingItem"),"hot chocolate override")
    require(selected(BOTTLE,"finishUsingItem"),"bottle base")
    require(selected(COMMON,"canMobEffectBeApplied"),"effect admission")
    require(selected(PHANTOM,"shouldSpawnPhantoms"),"phantom rule")
    require(not selected("foreign/ItemStack","consume"),"owner scope")
    require(LIMITS["mutation"]=="NO_MUTATION","policy")
    print("PASS: five scope checks and policy")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--installer",type=Path)
    p.add_argument("--server",type=Path)
    p.add_argument("--srg",type=Path)
    p.add_argument("--universal",type=Path)
    p.add_argument("--publisher",type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all((a.installer,a.server,a.srg,a.universal,a.publisher,a.output)) and not a.output.exists(),"write-once report and artifacts required")
        result=scan(a.installer,a.server,a.srg,a.universal,a.publisher,a.javap)
        data=canonical(result).encode()
        require(len(data)<=4_000_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:
            f.write(data)
        print("REPORT_SHA256",digest(data),"BYTES",len(data))
        for owner,row in result["classes"].items():
            print("OWNER",owner,row.get("source"),row.get("class_sha256"))
            for m in row.get("methods",[]):
                print("METHOD",owner,m["name"],m["descriptor"],m.get("code_sha256"),m.get("instruction_count"))
                if m["executable"]:
                    print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
