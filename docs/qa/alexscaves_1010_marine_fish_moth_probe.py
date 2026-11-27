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

ROOT = "com/github/alexmodguy/alexscaves/server/item/"
MARINE = ROOT + "MarineSnowItem"
FISH = ROOT + "ModFishBucketItem"
MOTH = ROOT + "MothDustItem"
REG = ROOT + "ACItemRegistry"
TARGETS = {MARINE, FISH, MOTH}
FACTORIES = {
    "lambda$static$92": (FISH, "6ee50396f6047acee481212ad62d3c4cbd750e9f550376efcf754d6068cb5eae"),
    "lambda$static$80": (FISH, "890937e2190ba7e244b6f1dc3c35740b4af2802b9096780d845497837ba47581"),
    "lambda$static$90": (MARINE, "d385d5b08e71c8ae683c30c5f0402acecbcb5ec0b6f13d0e33c25bbf57cdf7ba"),
    "lambda$static$122": (MOTH, "20fac1a05d60f7390148c4a90e14a151511ba918fb57388a09b978b7dbcd4948"),
    "lambda$static$55": (FISH, "d7729687750c047d200bb210236a4297426cad16d43e8e27a3403f58ca9bfc4b"),
    "lambda$static$88": (FISH, "fc3ae35eecabc8a02f3f04ab286e47880a5b1f2742409b6101bd83a9ebca3072"),
    "lambda$static$28": (FISH, "453b73b31f0029d7869d40793ba0788953f6c7cfe17fef1b1958c8c9bf282087"),
    "lambda$static$84": (FISH, "2afb9a0374d54244d796e67cdb0c0e9dd5393eab63049456bf109f686dadeb0b"),
}
REG_SHA = "114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1"
ROSTER_SHA = "2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
LIMITS = {"scope":"STATIC_DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED",
          "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
          "provider_universe_closed":False,"semantic_magic_roots_delta":0,
          "resource_scope":"PATH_NAME_MATCH_ONLY","consumer_scope":"TYPED_REFS_AND_DIRECT_SITES_ONLY"}

def resource_match(path):
    return path.endswith(".json") and any(token in path.lower() for token in ("gossamer_worm_bucket","lanternfish_bucket","marine_snow","moth_dust","radgill_bucket","sea_pig_bucket","trilocaris_bucket","tripodfish_bucket"))

def inspect(jar,javap):
    verify_artifact(jar)
    classes={};consumers={};resources={}
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
        require(len(classes[REG]["methods"])==len(FACTORIES),"factory roster")
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
            "classes":classes,"consumers":consumers,"resources":resources,"limits":LIMITS}

def self_test():
    require(len(TARGETS)==3 and len(FACTORIES)==8,"scope")
    require(resource_match("data/alexscaves/recipe/marine_snow.json"),"recipe")
    require(resource_match("assets/alexscaves/models/item/moth_dust.json"),"model")
    require(not resource_match("assets/alexscaves/textures/item/moth_dust.png"),"resource type")
    require(not resource_match("data/alexscaves/recipe/remote_detonator.json"),"unrelated")
    require(resource_match("assets/alexscaves/models/item/lanternfish_bucket.json"),"bucket model")
    require(len({target for target, _ in FACTORIES.values()})==3,"all target factories")
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
        print("DISCOVERY_ONLY NO_MUTATION")
