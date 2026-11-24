#!/usr/bin/env python3
"""Read-only downstream contracts for Holocoder, hot chocolate and both ink bombs.

Publisher 1.0.10 plus official NeoForge 21.1.250 distributed archives. Record
typed calls, branch/operand pivots, resource references and registry handles.
No provider class is executed; no runtime equivalence or mutating hook inferred.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap, numeric, MATH
from alexscaves_1010_remote_detonator_block_callbacks_probe import registry
from alexscaves_1010_destroyed_item_engine_reference import ARTIFACTS, verify_artifact as verify_universal

P="com/github/alexmodguy/alexscaves/server/"
MC="net/minecraft/"
NF="net/neoforged/neoforge/"
HOLO=P+"block/blockentity/HologramProjectorBlockEntity"
HBLOCK=P+"block/HologramProjectorBlock"
PROJ=P+"entity/item/InkBombEntity"
CLOUD=MC+"world/entity/AreaEffectCloud"
PROJECTILE=MC+"world/entity/projectile/Projectile"
THROWABLE=MC+"world/entity/projectile/ThrowableProjectile"
THROWITEM=MC+"world/entity/projectile/ThrowableItemProjectile"
STAT=MC+"stats/StatsCounter"
PHANTOM=MC+"world/level/levelgen/PhantomSpawner"
ALL={HOLO,CLOUD,PROJECTILE,THROWABLE,THROWITEM,PHANTOM}
SELECT={
    HBLOCK:{"acUse","getTicker","newBlockEntity","onRemove","<init>","useWithoutItem","useItemOn"},
    P+"event/CommonEvents":{"acPlayerEntityInteract"},
    P+"misc/ACPlatform":{"serializeEntity","getEntitySpawningPacket","setThrower"},
    P+"misc/ACCompat":{"getCompound","entityTypeFrom","setCloudColor","getBoolean","getTag","setTag"},
    P+"entity/item/SubmarineEntity":{"setLightsOn","areLightsOn","isLightsOn","getLightsOn"},
    P+"misc/AbstractProjectileDispenseBehavior":{"dispense","execute","getPower","getUncertainty","playSound","getProjectile"},
    P+"item/ACFoods":{"lambda$static$39"},
    MC+"world/effect/MobEffectInstance":{"<init>","getDuration","getAmplifier","update","tick","tickDownDuration","isInfiniteDuration","mapDuration"},
    MC+"world/entity/LivingEntity":{"addEffect","canBeAffected","removeEffect","removeEffectNoUpdate","onEffectAdded","onEffectUpdated"},
    MC+"world/entity/Entity":{"getFirstPassenger","getEncodeId","getUUID","save","saveWithoutId","load","setUUID","isAlive","canBeHitByProjectile"},
    MC+"world/entity/EntityType":{"by","getKey","create","loadEntityRecursive","createFromTag"},
    MC+"world/damagesource/DamageSources":{"thrown"},
    MC+"network/syncher/SynchedEntityData":{"get","set","packDirty","assignValues"},
    MC+"server/level/ServerPlayer":{"resetStat","awardStat","getStats"},
    STAT:{"getValue","setValue","increment"},
    MC+"stats/ServerStatsCounter":{"setValue","sendStats","markAllDirty"},
    MC+"world/item/Item$Properties":{"<init>","stacksTo","buildAndValidateComponents"},
    NF+"event/EventHooks":{"onProjectileImpact","onEntityInteract","onMobEffectAdded","onMobEffectRemove","onMobEffectApplicable"},
}
REQUIRED={
    HOLO:{"setEntity","cycleHologramScale"},
    HBLOCK:{"acUse"}, P+"event/CommonEvents":{"acPlayerEntityInteract"},
    P+"misc/ACPlatform":{"serializeEntity","getEntitySpawningPacket"},
    P+"misc/ACCompat":{"getCompound","setCloudColor"},
    P+"entity/item/SubmarineEntity":{"setLightsOn"},
    P+"item/ACFoods":{"lambda$static$39"},
    CLOUD:{"<init>","tick","setRadius","setDuration","setRadiusPerTick","addEffect","setOwner","getOwner","addAdditionalSaveData","readAdditionalSaveData"},
    PROJECTILE:{"shoot","shootFromRotation","setOwner","getOwner","onHit"},
    THROWABLE:{"tick"},
    THROWITEM:{"setItem","getItem","getDefaultItem"},
    PHANTOM:{"tick"},
    MC+"world/entity/LivingEntity":{"addEffect","canBeAffected","removeEffect"},
    MC+"server/level/ServerPlayer":{"resetStat"},
    STAT:{"getValue","setValue"},
    MC+"stats/ServerStatsCounter":{"setValue"},
}
PINS={
    HBLOCK:"ec685ba2b8db000916105c2696f61372e7ee9f93893529bfe196c262dce465fe",
    P+"event/CommonEvents":"d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43",
    P+"misc/ACCompat":"333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
    P+"item/ACFoods":"a52ec981fe51c97003383a46f7c0b2de06baa5e3ca3f73db988655abce51e12e",
    MC+"world/entity/Entity":"4f65b7d5d4628e9f10a6a23e5a0f68814520d8019f4bc001924cd752c00eed84",
    MC+"world/entity/LivingEntity":"52130dfb8dc4b5c48ec1ef12bf19b40ff29f6e38fc25b02b94202553f75ce5f4",
    MC+"server/level/ServerPlayer":"ec7c90a8b6a771cfd53b5038f377a72314b9efbf2301ed1ce540723b7d19c6d2",
}
IDS={"alexscaves:holocoder","alexscaves:hot_chocolate_bottle","alexscaves:ink_bomb","alexscaves:glow_ink_bomb"}
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
        "mutation":"NO_MUTATION","runtime_loaded_bytes":"NOT_OBSERVED","effective_config_and_tags":"NOT_VERIFIED",
        "provider_universe_closed":False,"semantic_magic_roots_delta":0,"actual_effect_acceptance":"NOT_VERIFIED"}

def identified(path,pin,size):
    data=path.read_bytes()
    require(len(data)==size and digest(data)==pin,"distribution identity mismatch "+path.name)
    return {"sha256":pin,"bytes":size}

def resource_hits(obj,path=()):
    found=[]
    if isinstance(obj,str):
        if obj in IDS:found.append({"path":list(path),"id":obj,"kind":"EXACT_STRING_VALUE"})
    elif isinstance(obj,list):
        for i,v in enumerate(obj):found.extend(resource_hits(v,(*path,i)))
    elif isinstance(obj,dict):
        for k,v in sorted(obj.items()):
            if k in IDS:found.append({"path":[*path,k],"id":k,"kind":"EXACT_OBJECT_KEY"})
            found.extend(resource_hits(v,(*path,k)))
    return found

def resources(z):
    names=sorted(p for p in z.namelist() if p.startswith(("data/","assets/")) and p.endswith(".json"))
    require(len(names)<=20000,"resource roster budget")
    hits={};errors=[];total=0
    for name in names:
        raw=z.read(name);total+=len(raw)
        require(len(raw)<=4_000_000 and total<=100_000_000,"resource byte budget")
        try: obj=json.loads(raw.decode("utf8"))
        except (UnicodeError,ValueError) as e:
            errors.append({"path":name,"type":type(e).__name__});continue
        match=resource_hits(obj)
        if match:
            require(len(match)<=1000,"resource hits budget")
            hits[name]={"sha256":digest(raw),"bytes":len(raw),"matches":match}
    return {"json_paths_scanned":len(names),"json_bytes_scanned":total,"parse_errors":errors,"exact_id_references":hits,
            "limits":"Exact decoded JSON string/key only; no effective tags, recipes or dynamically composed references."}

def projection(rd,key,body,decl):
    result=analyze(rd,body,decl)
    result["instruction_sha256"]=summarize(rd,key,body)["instruction_sha256"]
    result["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym}
        for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
    result["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
    result["strings"]=[{"offset":at,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if sym.startswith("String ")]
    result["bootstrap_links"]=bootstrap(rd,body)
    result["local_accesses"]=[{"offset":at,"opcode":op,"operand":arg}
        for at,(op,arg,_) in sorted(body.items()) if op.startswith(("aload","astore","iload","istore","fload","fstore","dload","dstore","lload","lstore")) or op=="iinc"]
    result["type_operands"]=[]
    for at,(op,arg,_) in sorted(body.items()):
        if op not in {"new","checkcast","instanceof","anewarray","multianewarray"}:continue
        match=re.match(r"#(\d+)(?:\s|,|$)",arg)
        require(match is not None and rd.pool[int(match[1])][0]==7,"unresolved typed class operand")
        result["type_operands"].append({"offset":at,"opcode":op,"owner":rd.resolve(int(match[1]))})
    return result

def consumer_census(z,jar,javap):
    roster=sorted(n for n in z.namelist() if n.endswith(".class"))
    require(len(roster)==1555,"publisher roster drift")
    candidates={}
    for name in roster:
        rd=ClassReader(z.read(name))
        require(rd.name+".class"==name and rd.major==65,"publisher identity")
        refs=rd.typed_refs(HOLO)
        if refs:candidates[rd.name]=refs
    require(1<=len(candidates)<=60,"hologram consumer budget")
    out={}
    for owner,refs in sorted(candidates.items()):
        raw=z.read(owner+".class");rd=ClassReader(raw)
        cp={x["index"] for x in refs if "index" in x and x["kind"] in {"field_reference","method_reference","interface_method_reference","class_constant"}}
        sites=[]
        for key,body in sorted(disassemble(jar,javap,owner).items()):
            matched=[]
            for at,(op,arg,_) in sorted(body.items()):
                match=re.match(r"#(\d+)(?:\s|,|$)",arg)
                if match and int(match[1]) in cp:
                    matched.append({"offset":at,"opcode":op,"constant":rd.resolve(int(match[1]))})
            if matched:
                decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
                sites.append({"name":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],"sites":matched})
        out[owner]={"class_sha256":digest(raw),"typed_references":refs,"method_sites":sites}
    return out

def inspect(args):
    verify_artifact(args.publisher)
    verify_universal(args.universal,"universal")
    require(not args.output.exists(),"write-once report required")
    artifact={
        "publisher":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "neoforge_version":"21.1.250",
        "installer":identified(args.installer,"0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60",6972109),
        "server":identified(args.server,"1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359",5675624),
        "srg":identified(args.srg,"26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71",14246609),
        "universal":ARTIFACTS["universal"],
    }
    with ZipFile(args.server) as ov,ZipFile(args.universal) as uni,ZipFile(args.srg) as mc,ZipFile(args.publisher) as mod:
        archives=[("NEOFORGE_OVERLAY",ov),("NEOFORGE_UNIVERSAL",uni),("MINECRAFT_SRG",mc),("PUBLISHER",mod)]
        for _,z in archives:require(len(z.namelist())==len(set(z.namelist())),"duplicate archive path")
        roster=[(name,z,set(z.namelist())) for name,z in archives]
        cp=":".join(map(str,(args.server,args.universal,args.srg,args.publisher)))
        classes={}
        for owner in sorted(ALL|set(SELECT)):
            found=[(name,z) for name,z,entries in roster if owner+".class" in entries]
            if not found:
                require(owner not in REQUIRED,"required owner absent "+owner)
                classes[owner]={"present":False};continue
            source,z=found[0];raw=z.read(owner+".class");sha=digest(raw);rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity "+owner)
            require(owner not in PINS or sha==PINS[owner],"prior class pin "+owner)
            decls=[d for d in rd.methods if owner in ALL or d["name"] in SELECT.get(owner,set())]
            require(REQUIRED.get(owner,set())<={d["name"] for d in decls},"required method absent "+owner)
            require(len(decls)<=120,"method roster "+owner)
            parsed=disassemble(cp,args.javap,owner)
            methods=[]
            for d in decls:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False});continue
                require(key in parsed and parsed[key],"body absent "+owner+str(key))
                print("PROJECT_METHOD",owner,*key,flush=True)
                methods.append({"executable":True,**projection(rd,key,parsed[key],d)})
            if owner in ALL:
                require({(d["name"],d["descriptor"]) for d in decls if "code_sha256" in d}==
                        {k for k,v in parsed.items() if v},"complete executable roster mismatch "+owner)
            classes[owner]={"present":True,"source":source,"available_sources":[k for k,_ in found],"class_sha256":sha,
                            "parent":rd.parent,"interfaces":rd.interfaces,"fields":rd.fields,
                            "declarations":rd.methods,"methods":methods}
        reg=registry(mod,args.publisher,args.javap,P+"entity/ACEntityRegistry",{PROJ})
        require(bool(reg["bootstrap_links"]),"Ink Bomb entity registry handle absent")
        consumer=consumer_census(mod,args.publisher,args.javap)
        res=resources(mod)
    report={"schema_version":1,"scope":"FOUR_ITEMS_DOWNSTREAM_DISCOVERY_ONLY","artifact":artifact,
            "classes":classes,"ink_bomb_entity_registry":reg,"hologram_typed_census":consumer,"resources":res,"limits":LIMITS}
    data=canonical(report).encode()
    require(len(data)<=4_000_000,"report byte budget")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("xb") as f:f.write(data)
    print("REPORT_SHA256",digest(data),"BYTES",len(data),"OWNERS",len(classes))
    for owner,row in classes.items():
        print("OWNER",owner,row.get("source"),row.get("class_sha256"),"METHODS",len(row.get("methods",[])))
        for method in row.get("methods",[]):
            print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
    print("REGISTRY",json.dumps(reg,sort_keys=True))
    print("HOLOGRAM_CENSUS",json.dumps(consumer,sort_keys=True))
    print("RESOURCE_CENSUS",json.dumps(res,sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")

def self_test():
    require(resource_hits({"item":"alexscaves:ink_bomb"})==[{"path":["item"],"id":"alexscaves:ink_bomb","kind":"EXACT_STRING_VALUE"}],"exact resource value")
    require(not resource_hits(["alexscaves:ink_bomb_suffix","ink_bomb","other:ink_bomb"]),"false-positive resource")
    require(len(resource_hits({"alexscaves:holocoder":{"item":"alexscaves:glow_ink_bomb"}}))==2,"key and nested value")
    require(LIMITS["mutation"]=="NO_MUTATION","policy")
    print("PASS: exact resource matching and policy guards")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("installer","server","srg","universal","publisher","output"):p.add_argument("--"+name,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(all(getattr(a,n) for n in ("installer","server","srg","universal","publisher","output")),"all inputs required")
        inspect(a)
