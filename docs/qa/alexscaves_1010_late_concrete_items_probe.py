#!/usr/bin/env python3
"""Exact read-only discovery of bounded late item outer classes, 1.0.10."""
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
REG = ROOT + "ACItemRegistry"
TARGETS = {ROOT + x for x in ["SackOfSatingItem","SeekingArrowItem","SharpenedCandyCaneItem","SodaBottleRocketItem","SubmarineItem","SweetishFishBucketItem","tooltip/SackOfSatingTooltip"]}
FACTORIES = {
    "lambda$static$191": (ROOT + "SodaBottleRocketItem", "4dc589cd486b67dc65677e0388911cb53182ffdfb49ca2459bf226a07bb96d72"),
    "lambda$static$183": (ROOT + "SackOfSatingItem", "9dcd9c444f05df03a91cce7f516726bc079f55db87d018ef5a704b5d83365d9b"),
    "lambda$static$18": (ROOT + "SeekingArrowItem", "f8ce2e07f40753612f56ebe56edb49e12174a8c1042dbf16864db018597cf438"),
    "lambda$static$172": (ROOT + "SharpenedCandyCaneItem", "8566af6220458047a5bcd4b371172601c61fac9f8574338bf463d0220a9469f1"),
    "lambda$static$98": (ROOT + "SubmarineItem", "230455d831544af1585d3aa7b09b67eae3496a0ea6e124691121a4427c13f618"),
    "lambda$static$151": (ROOT + "SweetishFishBucketItem", "2cf146833c4613f3c6038bd925527e834d419dad1399b796fa484062d7341773"),
    "lambda$static$150": (ROOT + "SweetishFishBucketItem", "a90039a60a0bc10b2d11d2ccc0faa534b6c9e1bc6dc48daf9f42f409fae8a3d1"),
    "lambda$static$153": (ROOT + "SweetishFishBucketItem", "b679636ea7c47b3b75cebed47103963c4c5088e28c3e89d1d572e5bbea20c813"),
    "lambda$static$149": (ROOT + "SweetishFishBucketItem", "ef1b8448d9d33e5c71ab2d445960e3321419a7113df99662978c5bb17b49dfe2"),
    "lambda$static$152": (ROOT + "SweetishFishBucketItem", "55645415c36c0551bd0e31b7bafcc45d52cdd5d7ecd1107c5ed0e48e936b6d79"),
}
REG_SHA = "114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1"
ROSTER_SHA = "2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
LIMITS = {"scope":"STATIC_DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED",
          "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","mutation":"NO_MUTATION",
          "provider_universe_closed":False,"semantic_magic_roots_delta":0,
          "resource_scope":"PATH_NAME_MATCH_ONLY","consumer_scope":"TYPED_REFS_AND_DIRECT_SITES_ONLY"}

def resource_match(path):
    return path.endswith(".json") and any(token in path.lower() for token in ("purple_soda_bottle_rocket","sack_of_sating","seeking_arrow","sharpened_candy_cane","submarine","sweetish_fish_blue_bucket","sweetish_fish_green_bucket","sweetish_fish_pink_bucket","sweetish_fish_red_bucket","sweetish_fish_yellow_bucket","sweetish_fish","soda_bottle_rocket"))

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
        require(1<=len(candidates)<=180,"typed consumer owner budget")
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
            require(len(rows)<=100,"per-owner method budget")
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
        require(sum(len(s["sites"]) for v in consumers.values() for s in v["method_sites"])<=1200,"site budget")
        for path in sorted(p for p in paths if resource_match(p)):
            raw=z.read(path)
            require(len(raw)<=100000,"resource budget")
            resources[path]={"sha256":digest(raw),"size":len(raw),"decoded":json.loads(raw)}
        require(len(resources)<=180,"resource roster budget")
    require(sum(len(v["methods"]) for v in classes.values())<=320,"method budget")
    return {"schema":1,"artifact":{"sha1":SHA1,"sha256":SHA256,"size":SIZE},"class_roster_sha256":ROSTER_SHA,
            "classes":classes,"consumers":consumers,"resources":resources,"limits":LIMITS}

def self_test():
    require(len(TARGETS)==7 and len(FACTORIES)==10,"scope")
    require(resource_match("data/alexscaves/recipe/sack_of_sating.json"),"recipe")
    require(resource_match("assets/alexscaves/models/item/sack_of_sating.json"),"model")
    require(not resource_match("assets/alexscaves/textures/item/sack_of_sating.png"),"resource type")
    require(not resource_match("data/alexscaves/recipe/remote_detonator.json"),"unrelated")
    require(resource_match("data/alexscaves/recipe/purple_soda_bottle_rocket.json"),"second matching resource")
    require(len({target for target, _ in FACTORIES.values()})==6,"target roster")
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
        require(len(raw)<=8000000,"report byte budget")
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
