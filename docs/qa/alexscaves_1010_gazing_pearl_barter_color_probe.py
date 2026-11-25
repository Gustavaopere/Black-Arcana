#!/usr/bin/env python3
"""Read-only exact consumer audit: barter request ingress and color boundary."""
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import refs

P="com/github/alexmodguy/alexscaves/server/"
BASE=P+"entity/living/DeepOneBaseEntity"
COLORS=P+"misc/ACColors"
COMPAT=P+"misc/ACCompat"
GENERATE=("generateBarterLoot","()Ljava/util/List;")
GETTER=("getBarterLootTable","()Lnet/minecraft/resources/ResourceLocation;")
OPAQUE=("opaque","(I)I")
TABLE=("lootTable","(Lnet/minecraft/server/MinecraftServer;Lnet/minecraft/resources/ResourceLocation;)Lnet/minecraft/world/level/storage/loot/LootTable;")
BASE_PIN="185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470"
GENERATE_PIN="d3df12394c1f7c4a7f78109c323ba56c1616f02aa2f329dbcb33deb941b09022"
LIMITS={"scope":"DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION","provider_universe_closed":False,
        "semantic_magic_roots_delta":0,"effective_loot":"NOT_VERIFIED","client_render":"NOT_TESTED"}

def classify(owner,key,family):
    if owner in family and key in {GENERATE,GETTER}:return "BARTER_METHOD"
    if owner==COLORS and key==OPAQUE:return "COLOR_HELPER"
    if owner==COMPAT and key==TABLE:return "LOOT_LOOKUP"
    return None

def callsites(rd,body,family):
    out=[]
    for at,(op,arg,_) in sorted(body.items()):
        if not op.startswith("invoke") or op=="invokedynamic":continue
        match=re.match(r"#(\d+)(?:\s|,|$)",arg)
        require(match is not None,"invoke operand absent")
        i=int(match[1])
        require(rd.pool[i][0] in (10,11),"invoke reference type")
        _,owner,(_,name,desc)=rd.resolve(i)
        kind=classify(owner,(name,desc),family)
        if kind:out.append({"offset":at,"opcode":op,"cp_index":i,"owner":owner,
                            "name":name,"descriptor":desc,"kind":kind})
    return out

def collect(rd,jar,javap,family):
    parsed=disassemble(jar,javap,rd.name)
    records=[]
    for d in rd.methods:
        if "code_sha256" not in d:continue
        key=(d["name"],d["descriptor"])
        require(key in parsed and parsed[key],"missing executable body")
        body=parsed[key];sites=callsites(rd,body,family)
        selected=classify(rd.name,key,family)
        # Other color/loot users are recorded as callsites; full semantics
        # are limited to exact selected definitions and barter-request callers.
        barter=any(s["kind"]=="BARTER_METHOD" and s["name"]==GENERATE[0] for s in sites)
        if not selected and not sites:continue
        if rd.name==BASE and key==GENERATE:
            require(d["code_sha256"]==GENERATE_PIN,"previous generateBarterLoot Code drift")
        row={"name":key[0],"descriptor":key[1],"code_sha256":d["code_sha256"],
             "instruction_sha256":summarize(rd,key,body)["instruction_sha256"],
             "instruction_count":len(body),"sites":sites,"projection":"CALLSITES_ONLY"}
        if selected or barter:
            if len(body)<=180:
                row.update(projection(rd,key,body,d))
                row["projection"]="FULL_BOUNDED_SEMANTICS"
                if selected=="COLOR_HELPER":
                    require(len(body)<=64,"opaque body budget")
                    row["opcode_pivots"]=[{"offset":at,"opcode":op,"operand":arg}
                                          for at,(op,arg,_) in sorted(body.items())]
            else:
                offsets=sorted(body)
                row["windows"]=[]
                for s in sites:
                    i=offsets.index(s["offset"])
                    sub={q:body[q] for q in offsets[max(0,i-14):i+15]}
                    row["windows"].append({"site":s["offset"],"members":refs(rd,sub),
                         "opcode_pivots":[{"offset":q,"opcode":op,"operand":arg}
                                          for q,(op,arg,_) in sorted(sub.items())]})
                row["projection"]="WINDOWS_ONLY"
        records.append(row)
    return records

def inspect(jar,javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        names=z.namelist(); roster=sorted(n for n in names if n.endswith(".class"))
        require(len(names)==len(set(names)) and len(roster)==1555,"publisher roster")
        hierarchy={}
        for p in roster:
            rd=ClassReader(z.read(p))
            require(rd.name+".class"==p and rd.major==65,"class identity")
            hierarchy[rd.name]=rd.parent
        family={BASE}
        while True:
            extended=family|{o for o,p in hierarchy.items() if p in family}
            if extended==family:break
            require(len(extended)<=40,"Deep One family budget")
            family=extended
        owners={}
        for p in roster:
            raw=z.read(p);rd=ClassReader(raw)
            candidates=[]
            for i,e in enumerate(rd.pool):
                if e is None or e[0] not in (10,11):continue
                _,owner,(_,n,desc)=rd.resolve(i)
                kind=classify(owner,(n,desc),family)
                if kind:candidates.append({"index":i,"owner":owner,"name":n,"descriptor":desc,"kind":kind})
            if not candidates and rd.name not in family|{COLORS,COMPAT}:continue
            require(len(owners)<100,"candidate owner budget")
            if rd.name==BASE:require(digest(raw)==BASE_PIN,"base class pin")
            rows=collect(rd,jar,javap,family)
            owners[rd.name]={"sha256":digest(raw),"parent":rd.parent,
                             "candidate_refs":candidates,"methods":rows}
        for owner,key in [(BASE,GENERATE),(COLORS,OPAQUE),(COMPAT,TABLE)]:
            require(any((row["name"],row["descriptor"])==key for row in owners[owner]["methods"]),
                    "required executable declaration absent "+owner)
    return {"schema":1,"publisher":{"sha1":SHA1,"sha256":SHA256,"bytes":SIZE},
            "class_entries_scanned":len(roster),"family":sorted(family),"owners":owners,"limits":LIMITS}

def self_test():
    require(classify(BASE,GENERATE,{BASE})=="BARTER_METHOD","exact method")
    require(classify(BASE,(GENERATE[0],"()V"),{BASE}) is None,"descriptor must match")
    require(classify("unrelated/Owner",GENERATE,{BASE}) is None,"owner must match")
    require(classify(COLORS,OPAQUE,{BASE})=="COLOR_HELPER","opaque exact")
    require(classify(COMPAT,TABLE,{BASE})=="LOOT_LOOKUP","loot lookup exact")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS: six scope checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path);p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar and a.output and not a.output.exists(),"write-once report")
        result=inspect(a.jar,a.javap);raw=canonical(result).encode()
        require(0<len(raw)<=3_000_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw),"OWNERS",len(result["owners"]))
        print("FAMILY",json.dumps(result["family"]))
        for owner,row in result["owners"].items():
            print("OWNER",owner,row["sha256"])
            for method in row["methods"]:
                print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION NOT_CERTIFIED")
