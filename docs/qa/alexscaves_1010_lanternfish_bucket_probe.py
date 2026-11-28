#!/usr/bin/env python3
"""Publisher-exact Lanternfish Bucket individual identity and transport boundaries.
Shared distributed bucket mechanics are already audited separately; no runtime execution.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap
from alexscaves_1010_gossamer_worm_bucket_probe import member_identity

P = "com/github/alexmodguy/alexscaves/server/"
IR, ER, ITEM = P+"item/ACItemRegistry", P+"entity/ACEntityRegistry", P+"item/ModFishBucketItem"
ID = "alexscaves:lanternfish_bucket"
ENTITY_ID = "alexscaves:lanternfish"
FACTORY = ("lambda$static$80", "()Lnet/minecraft/world/item/Item;")
FLUID = ("lambda$static$79", "()Lnet/minecraft/world/level/material/Fluid;")
FACTORY_SHA = "890937e2190ba7e244b6f1dc3c35740b4af2802b9096780d845497837ba47581"
PINS = {IR:"114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1",
        ER:"7d7c91ddbb534d7c0e86a590ef7d7c3154ec2a628153c31e9fc7318a4b29e072",
        ITEM:"9d22e586625f298993fbbf86b59ff2369cc3dccd9a9115b23d52778ed4c112dc"}
ROSTER_SHA = "2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
METHODS = {"<init>","mobInteract","interact","getBucketItemStack","saveToBucketTag",
           "loadFromBucketTag","setFromBucket","fromBucket","getPickupSound","addAdditionalSaveData",
           "readAdditionalSaveData","defineSynchedData","requiresCustomPersistence","removeWhenFarAway",
           "finalizeSpawn","createAttributes","getAddEntityPacket"}
LIMITS = {"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
          "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION","provider_universe_closed":False,
          "semantic_magic_roots_delta":0,"runtime_loaded_bytes":"NOT_OBSERVED",
          "scope":"PUBLISHER_ONLY_ITEM_ENTITY_IDENTITY_AND_TRANSPORT"}

def read_owner(z, owner):
    raw = z.read(owner+".class")
    rd = ClassReader(raw)
    require(rd.name==owner and rd.major==65,"owner identity "+owner)
    require(owner not in PINS or digest(raw)==PINS[owner],"class pin "+owner)
    return raw,rd

def row(rd, parsed, key):
    found = [d for d in rd.methods if (d["name"],d["descriptor"])==key]
    require(len(found)==1 and "code_sha256" in found[0],"executable declaration "+str(key))
    require(key in parsed and 0<len(parsed[key])<=5000,"method projection budget "+str(key))
    return projection(rd,key,parsed[key],found[0])

def refs_json(value, path=()):
    if isinstance(value,dict):
        for k,v in sorted(value.items()):
            if k in (ID,ENTITY_ID):
                yield [list(path+(k,)),"KEY",k]
            yield from refs_json(v,path+(k,))
    elif isinstance(value,list):
        for i,v in enumerate(value):
            yield from refs_json(v,path+(i,))
    elif value in (ID,ENTITY_ID):
        yield [list(path),"VALUE",value]

def inspect(jar,javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        names=z.namelist()
        roster=sorted(p for p in names if p.endswith(".class"))
        require(len(names)==len(set(names)) and len(roster)==1555,"publisher roster")
        require(digest(("\n".join(roster)+"\n").encode())==ROSTER_SHA,"roster hash")
        available=set(roster)
        _,ir=read_owner(z,IR)
        _,er=read_owner(z,ER)
        read_owner(z,ITEM)
        ip=disassemble(jar,javap,IR)
        factory=row(ir,ip,FACTORY)
        fluid=row(ir,ip,FLUID)
        require(factory["code_sha256"]==FACTORY_SHA,"prior factory Code pin")
        require(any(v["owner"]==ER and v["name"]=="LANTERNFISH" and v["offset"]==4 for v in factory["typed_members"]),"exact entity field")
        require(any(h["owner"]==IR and (h["name"],h["descriptor"])==FLUID
                    for b in factory["bootstrap_links"] for h in b["handles"]),"exact fluid bootstrap")
        ep=disassemble(jar,javap,ER)
        init=ep[("<clinit>","()V")]
        offsets=sorted(init)
        sites=[i for i,at in enumerate(offsets) if init[at][0]=="putstatic"
               and member_identity(er,init[at][1])==(ER,"LANTERNFISH","Ljava/util/function/Supplier;")]
        require(len(sites)==1 and sites[0]>=4,"registry exact write")
        i=sites[0]
        window={q:init[q] for q in offsets[i-4:i+1]}
        require([v[0] for v in window.values()] in (["getstatic","ldc","invokedynamic","invokevirtual","putstatic"],
                  ["getstatic","ldc_w","invokedynamic","invokevirtual","putstatic"]),"registry write sequence")
        require(init[offsets[i-3]][2]=="String lanternfish","registry ID")
        require(member_identity(er,init[offsets[i-1]][1])==("net/neoforged/neoforge/registries/DeferredRegister","register","(Ljava/lang/String;Ljava/util/function/Supplier;)Lnet/neoforged/neoforge/registries/DeferredHolder;"),"registry method")
        handles=[h for b in bootstrap(er,window) for h in b["handles"]
                 if h["owner"]==ER and h["kind"]==6 and h["descriptor"]=="()Lnet/minecraft/world/entity/EntityType;"]
        require(len(handles)==1,"entity factory handle")
        entity_factory=row(er,ep,(handles[0]["name"],handles[0]["descriptor"]))
        constructors=[h for b in entity_factory["bootstrap_links"] for h in b["handles"] if h["kind"]==8
                      and h["name"]=="<init>" and h["descriptor"]=="(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V"
                      and h["owner"]+".class" in available]
        require(len(constructors)==1,"publisher entity constructor")
        entity=constructors[0]["owner"]
        lineage=[]
        cursor=entity
        while cursor and cursor+".class" in available:
            require(len(lineage)<12 and cursor not in [v["owner"] for v in lineage],"lineage limit")
            raw,rd=read_owner(z,cursor)
            parsed=disassemble(jar,javap,cursor)
            methods=[]
            for d in rd.methods:
                if d["name"] in METHODS and "code_sha256" in d:
                    methods.append(row(rd,parsed,(d["name"],d["descriptor"])))
            require(len(methods)<=80,"lineage method budget")
            lineage.append({"owner":cursor,"class_sha256":digest(raw),"parent":rd.parent,
                            "interfaces":rd.interfaces,"fields":rd.fields,"declarations":rd.methods,"methods":methods})
            cursor=rd.parent
        require(bool(lineage),"publisher lineage")
        consumers=[]
        for path in roster:
            rd=ClassReader(z.read(path))
            require(rd.name+".class"==path and rd.major==65,"class identity")
            refs=rd.typed_refs(entity)
            if refs or rd.parent==entity or entity in rd.interfaces:
                consumers.append({"owner":rd.name,"refs":refs,"parent":rd.parent})
        require(len(consumers)<=100,"typed consumer budget")
        data_paths=sorted(p for p in names if p.startswith("data/") and p.endswith(".json"))
        require(len(data_paths)<=5000,"data resource budget")
        resources={}
        for path in data_paths:
            raw=z.read(path)
            require(len(raw)<=2_000_000,"JSON size "+path)
            value=json.loads(raw)
            refs=list(refs_json(value))
            if refs or path.rsplit("/",1)[-1] in ("lanternfish.json","lanternfish_bucket.json"):
                resources[path]={"sha256":digest(raw),"size":len(raw),"refs":refs,"data":value}
        require(len(resources)<=100,"resource hit budget")
        model="assets/alexscaves/models/item/lanternfish_bucket.json"
        require(digest(z.read(model))=="64a2ccfbda89984d68eeb71707ebc909628451db9b176c6150a4f89facedb87a","model pin")
        return {"schema":1,"artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
                "class_roster_sha256":ROSTER_SHA,"factory":factory,"fluid_supplier":fluid,
                "entity_factory":entity_factory,"entity":entity,
                "registry_window":[{"offset":q,"opcode":v[0],"operand":v[1],"symbol":v[2]} for q,v in window.items()],
                "lineage":lineage,"external_parent":cursor,"typed_consumers":consumers,
                "data_json_count":len(data_paths),"resources":resources,"limits":LIMITS}

def self_test():
    require(list(refs_json({"x":[ID,ID+"_other",ENTITY_ID]}))==[[["x",0],"VALUE",ID],[["x",2],"VALUE",ENTITY_ID]],"exact value filter")
    require(list(refs_json({ID:1}))==[[[ID],"KEY",ID]],"exact key filter")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS exact resource filter and policy")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--output",type=Path)
    p.add_argument("--javap",default="javap");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(a.jar is not None and a.output is not None and not a.output.exists(),"write-once")
        result=inspect(a.jar,a.javap)
        raw=canonical(result).encode()
        require(len(raw)<=5000000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as out:
            out.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for k in ("factory","fluid_supplier","entity_factory","registry_window","entity","external_parent","data_json_count","resources","typed_consumers"):
            print(k.upper(),json.dumps(result[k],sort_keys=True))
        for v in result["lineage"]:
            print("LINEAGE",json.dumps({k:x for k,x in v.items() if k!="methods"},sort_keys=True))
            for m in v["methods"]:
                print("SEMANTIC",json.dumps({"owner":v["owner"],**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")
