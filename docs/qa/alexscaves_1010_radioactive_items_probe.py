#!/usr/bin/env python3
"""Exact read-only discovery of three next item outer classes, 1.0.10."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap

ROOT = "com/github/alexmodguy/alexscaves/server/item/"
BLOCK = ROOT + "RadioactiveBlockItem"
ITEM = ROOT + "RadioactiveItem"
DESTROY = ROOT + "RadioactiveOnDestroyedBlockItem"
REG = ROOT + "ACItemRegistry"
TARGETS = {BLOCK, ITEM, DESTROY}
FACTORIES = {
    "lambda$static$74": (ITEM, "a8f68e374288c6495c5ab854c9c17cd777cc30b4be5e4e71a31e41531873d736"),
    "lambda$static$73": (ITEM, "97c2de487a982e04941e1183de8616b31f8ca5d1b29a6fd9a009ac03cbe85d20"),
    "lambda$static$58": (ITEM, "1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f"),
    "lambda$static$59": (ITEM, "1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f"),
}
REG_SHA = "114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1"
ROSTER_SHA = "2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
LIMITS = {"scope":"STATIC_DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED",
          "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
          "provider_universe_closed":False,"semantic_magic_roots_delta":0,
          "resource_scope":"PATH_NAME_MATCH_ONLY","consumer_scope":"TYPED_REFS_AND_DIRECT_SITES_ONLY","registry_binding_scope":"CONSTRUCTOR_PRODUCERS_AND_SAME_OWNER_BOOTSTRAP_WINDOWS_NOT_FULL_ID_FLOW"}

def resource_match(path):
    return path.endswith(".json") and any(token in path.lower() for token in ("uranium","fissile_core","charred_remnant","radioactive","irradiated","radiation","nuclear_furnace","nuclear_bomb","hazmat"))

def inspect(jar,javap):
    verify_artifact(jar)
    classes={};consumers={};resources={};factory_candidates={};binding_windows={}
    with ZipFile(jar) as z:
        paths=z.namelist()
        roster=sorted(p for p in paths if p.endswith(".class"))
        require(len(paths)==len(set(paths)) and len(roster)==1555,"publisher roster")
        require(digest(("\n".join(roster)+"\n").encode())==ROSTER_SHA,"class path roster pin")
        candidates={}
        for path in roster:
            rd=ClassReader(z.read(path))
            require(rd.name+".class"==path,"class identity")
            matches={}
            for target in sorted(TARGETS):
                refs=rd.typed_refs(target)
                if refs or rd.parent==target or target in rd.interfaces:
                    matches[target]={"refs":refs,"extends_directly":rd.parent==target,"implements_directly":target in rd.interfaces}
            if matches:candidates[rd.name]=matches
        require(1<=len(candidates)<=80,"typed consumer owner budget")
        for owner in sorted(TARGETS|{REG}):
            raw=z.read(owner+".class");rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"owner identity")
            if owner==REG:require(digest(raw)==REG_SHA,"previous registry class pin")
            parsed=disassemble(jar,javap,owner)
            rows=[]
            for d in rd.methods:
                if owner==REG and d["name"] not in FACTORIES:continue
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    rows.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]) and len(parsed[key])<=1200,"method scope")
                row=projection(rd,key,parsed[key],d);row["executable"]=True
                if owner==REG:
                    target,pin=FACTORIES[key[0]]
                    require(d["code_sha256"]==pin,"factory Code drift")
                    require(any(x["owner"]==target and x["opcode"]=="new" for x in row["type_operands"]),"factory target absent")
                rows.append(row)
            require(len(rows)<=60,"per-owner method budget")
            classes[owner]={"class_sha256":digest(raw),"parent":rd.parent,"interfaces":rd.interfaces,"fields":rd.fields,"methods":rows}
        require(len(classes[REG]["methods"])==len(FACTORIES),"direct factory roster")
        # Candidate registry producers are discovered by typed references, not inferred from item names.
        discovered={}
        for owner,matches in sorted(candidates.items()):
            raw=z.read(owner+".class");rd=ClassReader(raw)
            parsed=disassemble(jar,javap,owner)
            cp={x["index"] for target in matches for x in matches[target]["refs"] if x.get("kind")=="class_constant"}
            for key,body in sorted(parsed.items()):
                new_sites=[]
                for at,(op,arg,_) in sorted(body.items()):
                    match=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if op=="new" and match and int(match[1]) in cp:
                        new_sites.append({"offset":at,"target":rd.resolve(int(match[1]))})
                if not new_sites:continue
                decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
                require(len(body)<=1200,"constructor producer method scope")
                factory_candidates.setdefault(owner,[]).append({"new_sites":new_sites,**projection(rd,key,body,decl)})
                discovered.setdefault(owner,set()).add(key)
        require(4<=sum(len(v) for v in factory_candidates.values())<=100,"constructor producer roster budget")
        for owner,keys in sorted(discovered.items()):
            rd=ClassReader(z.read(owner+".class"));parsed=disassemble(jar,javap,owner)
            for key,body in sorted(parsed.items()):
                offsets=sorted(body);hits=[]
                for link in bootstrap(rd,body):
                    if not any(h["owner"]==owner and (h["name"],h["descriptor"]) in keys for h in link["handles"]):continue
                    at=link["offset"];i=offsets.index(at)
                    hits.append({**link,"window":[{"offset":q,"opcode":body[q][0],"operand":body[q][1],"symbol":body[q][2]} for q in offsets[max(0,i-8):i+9]]})
                if hits:
                    decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
                    binding_windows.setdefault(owner,[]).append({"name":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],"sites":hits})
        require(sum(len(s["sites"]) for v in binding_windows.values() for s in v)<=200,"binding site budget")
        for owner,matches in sorted(candidates.items()):
            raw=z.read(owner+".class");rd=ClassReader(raw)
            parsed=disassemble(jar,javap,owner)
            sites=[]
            cp={x["index"] for v in matches.values() for x in v["refs"] if "index" in x and x["kind"] in {"field_reference","method_reference","interface_method_reference","class_constant"}}
            for key,body in sorted(parsed.items()):
                offsets=sorted(body);hits=[]
                for i,at in enumerate(offsets):
                    op,arg,_=body[at]
                    match=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if match and int(match[1]) in cp:
                        hits.append({"offset":at,"opcode":op,"constant":rd.resolve(int(match[1])),
                                     "window":[{"offset":q,"opcode":body[q][0],"operand":body[q][1],"symbol":body[q][2]} for q in offsets[max(0,i-6):i+7]]})
                if hits:
                    d=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
                    sites.append({"name":key[0],"descriptor":key[1],"code_sha256":d["code_sha256"],"sites":hits})
            consumers[owner]={"class_sha256":digest(raw),"parent":rd.parent,"interfaces":rd.interfaces,"typed_references":matches,"method_sites":sites}
        require(sum(len(s["sites"]) for v in consumers.values() for s in v["method_sites"])<=500,"site budget")
        for path in sorted(p for p in paths if resource_match(p)):
            raw=z.read(path)
            require(len(raw)<=100000,"resource budget")
            resources[path]={"sha256":digest(raw),"size":len(raw),"decoded":json.loads(raw)}
        require(len(resources)<=100,"resource roster budget")
    require(sum(len(v["methods"]) for v in classes.values())<=140,"method budget")
    return {"schema":1,"artifact":{"sha1":SHA1,"sha256":SHA256,"size":SIZE},"class_roster_sha256":ROSTER_SHA,
            "classes":classes,"consumers":consumers,"resources":resources,"factory_candidates":factory_candidates,"binding_windows":binding_windows,"limits":LIMITS}

def self_test():
    require(len(TARGETS)==3 and len(FACTORIES)==4,"scope")
    require(resource_match("data/alexscaves/recipe/uranium.json"),"recipe")
    require(resource_match("assets/alexscaves/models/item/fissile_core.json"),"model")
    require(not resource_match("assets/alexscaves/textures/item/fissile_core.png"),"resource type")
    require(not resource_match("data/alexscaves/recipe/remote_detonator.json"),"unrelated")
    require(resource_match("data/alexscaves/recipe/charred_remnant.json"),"second item recipe")
    require({target for target, _ in FACTORIES.values()}=={ITEM},"target roster")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS eight scope and policy checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--output",type=Path)
    p.add_argument("--javap",default="javap");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar is not None and a.output is not None and not a.output.exists(),"write once")
        report=inspect(a.jar,a.javap);raw=canonical(report).encode()
        require(len(raw)<=4000000,"report byte budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in report["classes"].items():
            print("OWNER",owner,row["class_sha256"],"PARENT",row["parent"],"METHODS",len(row["methods"]))
            for method in row["methods"]:print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
        for owner,row in report["consumers"].items():
            print("CONSUMER",json.dumps({"owner":owner,**row},sort_keys=True))
        for path,row in report["resources"].items():print("RESOURCE",json.dumps({"path":path,**row},sort_keys=True))
        for owner,rows in report["factory_candidates"].items():
            for row in rows:print("FACTORY_CANDIDATE",json.dumps({"owner":owner,**row},sort_keys=True))
        for owner,rows in report["binding_windows"].items():
            for row in rows:print("BINDING_WINDOW",json.dumps({"owner":owner,**row},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
