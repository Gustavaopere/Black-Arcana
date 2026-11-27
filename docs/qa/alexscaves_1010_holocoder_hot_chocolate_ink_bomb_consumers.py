#!/usr/bin/env python3
"""Bounded publisher consumer census and projectile/registry semantic projection."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze, SELECT_OPS
from alexscaves_1010_nuclear_explosion_effect_probe import numeric, MATH, bootstrap, context

P="com/github/alexmodguy/alexscaves/server/"
ITEM=P+"item/ACItemRegistry"
ENTITY=P+"entity/ACEntityRegistry"
FOOD=P+"item/ACFoods"
PROJECTILE=P+"entity/item/InkBombEntity"
COMPAT=P+"misc/ACCompat"
FACTORIES={"lambda$static$17","lambda$static$105","lambda$static$106","lambda$static$164"}
KEYS={"BoundEntityTag","BoundEntityUUID"}
FIELDS={ITEM:{"HOLOCODER","HOT_CHOCOLATE_BOTTLE","INK_BOMB","GLOW_INK_BOMB"},
        ENTITY:{"INK_BOMB"}, FOOD:{"HOT_CHOCOLATE_BOTTLE"}}
HELPERS={"getTag","getOrCreateTag","setTag","putUUID","getUUID","hasUUID","entityTypeFrom","useSidedSuccess"}
LIMITS={"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
        "mutation":"NO_MUTATION","provider_universe_closed":False,"semantic_magic_roots_delta":0,
        "installed_dump_comparison":"NOT_VERIFIED","effective_tags":"NOT_VERIFIED",
        "scope":"PUBLISHER_NATIVE_ONLY"}

def matches(rd,i):
    entry=rd.pool[i]
    if entry is None: return False
    if entry[0]==8: return rd.resolve(i) in KEYS
    if entry[0] not in (9,10,11): return False
    tag,owner,sig=rd.resolve(i)
    return (tag==9 and sig[1] in FIELDS.get(owner,set())) or owner==PROJECTILE

def self_test():
    require("BoundEntityUUID" in KEYS and "BoundEntityUUIDSuffix" not in KEYS,"exact key")
    require("INK_BOMB" in FIELDS[ITEM] and "INK_BOMB" not in FIELDS[FOOD],"owner-scoped field")
    require(LIMITS["mutation"]=="NO_MUTATION","policy")
    print("PASS: exact key, field scope and policy")

def inspect(jar,javap,output):
    verify_artifact(jar)
    require(not output.exists(),"write-once output")
    with ZipFile(jar) as z:
        paths=z.namelist()
        roster=sorted(x for x in paths if x.endswith(".class"))
        require(len(paths)==len(set(paths)) and len(roster)==1555,"roster drift")
        candidates={}
        for path in roster:
            rd=ClassReader(z.read(path))
            require(rd.name+".class"==path and rd.major==65,"owner identity")
            hits={i:rd.resolve(i) for i in range(1,len(rd.pool)) if matches(rd,i)}
            if hits: candidates[rd.name]=hits
        selected=set(candidates)|{ITEM,FOOD,ENTITY,PROJECTILE,COMPAT,ITEM+"$3",ITEM+"$4"}
        require(len(selected)<=70,"candidate budget")
        owners={}
        for owner in sorted(selected):
            raw=z.read(owner+".class")
            rd=ClassReader(raw)
            bodies=disassemble(jar,javap,owner)
            methods=[]
            for k,body in sorted(bodies.items()):
                if not body: continue
                offsets=sorted(body)
                hits=[]
                for at,(op,arg,sym) in sorted(body.items()):
                    cp=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if cp and int(cp[1]) in candidates.get(owner,{}):
                        i=offsets.index(at)
                        hits.append({"offset":at,"opcode":op,"constant":candidates[owner][int(cp[1])],
                            "window":[{"offset":v,"opcode":body[v][0],"symbol":body[v][2],"operand":body[v][1]}
                                      for v in offsets[max(0,i-8):i+9]]})
                core=(owner==PROJECTILE or owner in (ITEM+"$3",ITEM+"$4") or
                      owner==ITEM and k[0] in FACTORIES or owner==COMPAT and k[0] in HELPERS)
                member_count=sum(op in SELECT_OPS for op,_,_ in body.values())
                branch_count=sum(op.startswith("if") or op in ("goto","goto_w") for op,_,_ in body.values())
                terminal_count=sum(op.endswith("return") or op=="athrow" for op,_,_ in body.values())
                bounded=len(body)<=500 and member_count<=180 and branch_count<=90 and terminal_count<=30
                full=core or (owner not in (ITEM,FOOD,ENTITY,COMPAT) and bool(hits) and bounded)
                if not hits and not full: continue
                print("PROJECT_METHOD",owner,k[0],k[1],"CORE",core,"MEMBERS",member_count,"FULL",full,flush=True)
                decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==k)
                row={"name":k[0],"descriptor":k[1],"code_sha256":decl["code_sha256"],
                     "instruction_count":len(body),"instruction_sha256":summarize(rd,k,body)["instruction_sha256"],
                     "sites":hits,"projection":"FULL_BOUNDED_SEMANTICS" if full else "DIRECT_SITE_WINDOWS_ONLY","typed_member_count":member_count}
                if full:
                    row["semantics"]=analyze(rd,body,decl)
                    row["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym}
                                            for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
                    row["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
                    row["strings"]=[{"offset":at,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if sym.startswith("String ")]
                    row["bootstrap_links"]=bootstrap(rd,body)
                methods.append(row)
            owners[owner]={"class_sha256":digest(raw),"parent":rd.parent,
                           "fields":rd.fields if owner==PROJECTILE else [],
                           "declarations":rd.methods if owner==PROJECTILE else [],
                           "methods":methods}
        require({(v["name"],v["descriptor"]) for v in owners[PROJECTILE]["methods"]}==
                {(v["name"],v["descriptor"]) for v in owners[PROJECTILE]["declarations"] if "code_sha256" in v},
                "projectile executable coverage drift")
        require(FACTORIES=={x["name"] for x in owners[ITEM]["methods"] if x["name"] in FACTORIES},"factory coverage")
    report={"schema_version":1,"artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "roster_count":1555,"owners":owners,"limits":LIMITS}
    raw=canonical(report).encode()
    require(len(raw)<=2_500_000,"report budget")
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("xb") as f:f.write(raw)
    print("REPORT_SHA256",digest(raw),"BYTES",len(raw),"OWNERS",len(owners))
    for owner,row in owners.items():
        print("OWNER",owner,row["class_sha256"],row["parent"])
        for method in row["methods"]:
            print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar is not None and a.output is not None,"jar/output required")
        inspect(a.jar,a.javap,a.output)
