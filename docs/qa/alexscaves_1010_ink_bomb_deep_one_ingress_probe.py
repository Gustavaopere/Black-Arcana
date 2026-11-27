#!/usr/bin/env python3
"""Read-only exact Deep One producer ingress and barter resource references.

This projects typed callsites and bounded semantic operands, not third-party
source or a complete AI/loot engine contract. No loaded game or mutation.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze
from alexscaves_1010_nuclear_explosion_effect_probe import numeric, MATH, bootstrap

P="com/github/alexmodguy/alexscaves/server/"
BASE=P+"entity/living/DeepOneBaseEntity"
ONE=P+"entity/living/DeepOneEntity"
KNIGHT=P+"entity/living/DeepOneKnightEntity"
SIG="(Lnet/minecraft/world/entity/player/Player;)Z"
PINS={
    BASE:"185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470",
    ONE:"745cdea0175d313fae6082a6c1fed67d0afd2e6e9e2964cbf637c0afb066ca2f",
    KNIGHT:"e8a3648a5d342c9a098b58894c57a323eb74ae5d5c1c599b1850d1e114b5bab6",
}
METHOD_PINS={
    BASE:"b585ad2aa8be0ddfc83b205c8faed995ea2c61b4d17dbf3b0f0a050694beb232",
    ONE:"180097bf11ee7809d47d474a18706932e4f3f82d63ae91f1aaa2b9ff0557ebc7",
    KNIGHT:"1ab97b7f5a3bd3f84e3f0f4e0470d55af4c35cf4a4d76e94065478fab9bbd174",
}
TARGETS={
    ("startDisappearBehavior",SIG),
    ("swapItemsForAnimation","(Lnet/minecraft/world/item/ItemStack;)V"),
    ("restoreSwappedItem","()V"),
    ("addReputation","(Ljava/util/UUID;I)V"),
}
LOOT={f"{prefix}{name}" for name in ("deep_one_barter","deep_one_knight_barter","deep_one_mage_barter")
      for prefix in ("","gameplay/","alexscaves:","alexscaves:gameplay/")}
LIMITS={"scope":"DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION","provider_universe_closed":False,
        "semantic_magic_roots_delta":0,"actual_barter_and_spawn_settlement":"NOT_VERIFIED",
        "runtime_loaded_bytes":"NOT_OBSERVED"}

def candidates(reader,family):
    hits={}
    for i,entry in enumerate(reader.pool):
        if entry is None:
            continue
        if entry[0] in (10,11):
            _,owner,(_,name,desc)=reader.resolve(i)
            if owner in family and (name,desc) in TARGETS:
                hits[i]={"kind":"METHOD","owner":owner,"name":name,"descriptor":desc}
        elif entry[0]==8:
            value=reader.resolve(i)
            if value in LOOT:
                hits[i]={"kind":"EXACT_STRING","value":value}
    return hits

def sites(body,hits):
    result=[]
    offsets=sorted(body)
    for pos,at in enumerate(offsets):
        op,arg,_=body[at]
        match=re.match(r"#(\d+)(?:\s|,|$)",arg)
        if not match or int(match[1]) not in hits:
            continue
        index=int(match[1]); hit=hits[index]
        if hit["kind"]=="METHOD" and not op.startswith("invoke"):
            continue
        if hit["kind"]=="EXACT_STRING" and op not in {"ldc","ldc_w"}:
            continue
        window=[{"offset":q,"opcode":body[q][0]} for q in offsets[max(0,pos-6):pos+7]]
        result.append({"offset":at,"opcode":op,"cp_index":index,**hit,"opcode_window":window})
    return result

def full_projection(reader,body,decl):
    row=analyze(reader,body,decl)
    row["instruction_sha256"]=summarize(reader,(decl["name"],decl["descriptor"]),body)["instruction_sha256"]
    row["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym}
                             for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
    row["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
    row["local_accesses"]=[{"offset":at,"opcode":op,"operand":arg} for at,(op,arg,_) in sorted(body.items())
                           if op.startswith(("aload","astore","dload","dstore","iload","istore","fload","fstore"))]
    row["bootstrap_links"]=bootstrap(reader,body)
    return row

def scan(jar,javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate archive entry")
        roster=sorted(n for n in names if n.endswith(".class"))
        require(len(roster)==1555,"publisher class roster drift")
        hierarchy={}
        for p in roster:
            r=ClassReader(z.read(p))
            require(r.name+".class"==p and r.major==65,"class identity drift")
            hierarchy[r.name]=r.parent
        family={BASE}
        while True:
            extended=family|{o for o,parent in hierarchy.items() if parent in family}
            if extended==family:break
            family=extended
        require({ONE,KNIGHT}<=family and len(family)<=40,"Deep One family drift")
        output={}
        for p in roster:
            raw=z.read(p); reader=ClassReader(raw); owner=reader.name
            hits=candidates(reader,family)
            if owner not in family and not hits:continue
            require(len(output)<80,"candidate owner budget")
            if owner in PINS:require(digest(raw)==PINS[owner],"pinned class drift "+owner)
            parsed=disassemble(jar,javap,owner)
            records=[]
            for d in reader.methods:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:continue
                require(key in parsed and parsed[key],"missing executable body "+owner+str(key))
                body=parsed[key]
                direct=sites(body,hits)
                selected=owner in family and (key in TARGETS or re.search("barter",d["name"],re.I))
                if not direct and not selected:continue
                if owner in METHOD_PINS and key==("startDisappearBehavior",SIG):
                    require(d["code_sha256"]==METHOD_PINS[owner],"known producer Code drift")
                item={"name":key[0],"descriptor":key[1],"code_sha256":d["code_sha256"],
                      "instruction_count":len(body),"sites":direct,"projection":"SITES_ONLY"}
                if selected and len(body)<=180:
                    item.update(full_projection(reader,body,d))
                    item["projection"]="FULL_BOUNDED_SEMANTICS"
                records.append(item)
            output[owner]={"class_sha256":digest(raw),"parent":reader.parent,
                "declared_signatures":[[d["name"],d["descriptor"]] for d in reader.methods],
                "constant_pool_candidates":[{"index":i,**v} for i,v in sorted(hits.items())],"methods":records}
        for owner,sha in METHOD_PINS.items():
            require(any(m["name"]=="startDisappearBehavior" and m["descriptor"]==SIG and m["code_sha256"]==sha
                        for m in output[owner]["methods"]),"pinned producer absent "+owner)
        return {"schema":1,"artifact":{"sha1":SHA1,"sha256":SHA256,"bytes":SIZE},
                "class_entries_scanned":len(roster),"family":sorted(family),
                "candidate_owners":output,"limits":LIMITS}

def self_test():
    h={2:{"kind":"METHOD","owner":BASE,"name":"startDisappearBehavior","descriptor":SIG},
       3:{"kind":"EXACT_STRING","value":"gameplay/deep_one_barter"}}
    b={0:("invokespecial","#2",""),3:("ldc","#3",""),5:("getfield","#2",""),8:("ldc","#99","")}
    require([x["offset"] for x in sites(b,h)]==[0,3],"typed call and string filter")
    require("gameplay/deep_one_barter" in LOOT and "deep_one_barter_extra" not in LOOT,"exact string scope")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS: 3 scope checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar and a.output and not a.output.exists(),"write-once report and publisher required")
        result=scan(a.jar,a.javap)
        raw=canonical(result).encode()
        require(len(raw)<=3_000_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as handle:handle.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw),"OWNERS",len(result["candidate_owners"]))
        print("FAMILY",canonical(result["family"]).replace("\n"," "))
        for owner,row in result["candidate_owners"].items():
            print("OWNER",owner,row["class_sha256"],row["parent"])
            for m in row["methods"]:
                print("SEMANTIC",canonical({"owner":owner,**m}).replace("\n"," "))
        print("DISCOVERY_ONLY NO_MUTATION")
