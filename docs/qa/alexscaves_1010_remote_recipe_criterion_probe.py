#!/usr/bin/env python3
"""Bounded, read-only resource and typed criterion projection. No runtime."""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_remote_detonator_resource_probe import RECIPE, ADV, PINS, decode
OWNER = "com/github/alexmodguy/alexscaves/server/item/RemoteDetonatorItem"
LIMITS = {"static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","mutation":"NO_MUTATION","world_safety":"BLOCKED","effective_recipe":"NOT_VERIFIED","criterion_grant":"NOT_VERIFIED","provider_universe_closed":False,"semantic_magic_roots_delta":0}
def project_resources(resources):
    recipe, adv = resources[RECIPE], resources[ADV]
    require(recipe.get("type")=="minecraft:crafting_shaped","recipe type")
    pattern, key = recipe["pattern"],recipe["key"]
    require(isinstance(pattern,list) and 0<len(pattern)<=3 and all(isinstance(row,str) and 0<len(row)<=3 for row in pattern),"pattern shape")
    require(len({len(row) for row in pattern})==1,"ragged recipe")
    require(isinstance(key,dict) and all(isinstance(k,str) and len(k)==1 and k!=" " for k in key),"key shape")
    used=set("".join(pattern))-{" "}
    require(used==set(key),"ingredient keys")
    require(recipe["result"].get("id")=="alexscaves:remote_detonator","result identity")
    criteria=adv["criteria"]
    require(isinstance(criteria,dict) and any(c.get("trigger")=="alexscaves:remote_detonation" for c in criteria.values()),"criterion identity")
    return {"recipe":{"type":recipe["type"],"pattern":pattern,"key":key,"symbol_counts":{k:sum(row.count(k) for row in pattern) for k in sorted(key)},"result":recipe["result"],"additional_fields":{k:v for k,v in recipe.items() if k not in ("type","pattern","key","result")}},"advancement":{"criteria":criteria,"requirements":adv.get("requirements"),"parent":adv.get("parent"),"rewards":adv.get("rewards"),"sends_telemetry_event":adv.get("sends_telemetry_event")}}
def scan(args):
    verify_artifact(args.jar)
    with ZipFile(args.jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate ZIP path")
        data={}
        for path in (RECIPE,ADV):
            size,sha=PINS[path]; raw=z.read(path)
            require(len(raw)==size and digest(raw)==sha,"resource pin "+path)
            data[path]=decode(raw)
        res=project_resources(data)
        raw=z.read(OWNER+".class");rd=ClassReader(raw)
        require(digest(raw)=="6d6e8cd94df306aec6f99b07af856b477b8e6f34d41aaca06a35921b53f2c4b8","owner drift")
        parsed=disassemble(args.jar,args.javap,OWNER)
        ds=[d for d in rd.methods if d["name"]=="use" and "code_sha256" in d]
        require(len(ds)==1,"use ambiguity")
        d=ds[0];row=projection(rd,(d["name"],d["descriptor"]),parsed[(d["name"],d["descriptor"])],d)
        refs=[x for x in row["typed_members"] if x["name"]=="REMOTE_DETONATION" and x["opcode"]=="getstatic"]
        require(len(refs)==1,"criterion field use")
        registry=refs[0]["owner"]
        owners={registry}
        owners.update(x["owner"] for x in row["typed_members"] if x["name"]=="trigger" and x["owner"].startswith("com/github/alexmodguy/") and x["owner"]+".class" in names)
        require(len(owners)<=6,"owner budget")
        classes={}
        for owner in sorted(owners):
            raw=z.read(owner+".class");rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity")
            bodies=disassemble(args.jar,args.javap,owner)
            if owner==registry:
                select=[d for d in rd.methods if "code_sha256" in d and d["name"]=="<clinit>"]
            else:
                select=[d for d in rd.methods if "code_sha256" in d]
            require(0<len(select)<=32,"method budget "+owner)
            methods=[]
            for d in select:
                key=(d["name"],d["descriptor"])
                require(key in bodies and bool(bodies[key]),"body missing")
                methods.append(projection(rd,key,bodies[key],d))
            classes[owner]={"sha256":digest(raw),"parent":rd.parent,"fields":rd.fields,"methods":methods}
    return {"schema":1,"publisher":{"sha1":SHA1,"sha256":SHA256,"bytes":SIZE},"resources":res,"use":row,"criterion_field":refs[0],"classes":classes,"limits":LIMITS}
def self_test():
    test={RECIPE:{"type":"minecraft:crafting_shaped","pattern":["AA"," A"],"key":{"A":{"item":"test:a"}},"result":{"id":"alexscaves:remote_detonator"}},ADV:{"criteria":{"c":{"trigger":"alexscaves:remote_detonation"}}}}
    require(project_resources(test)["recipe"]["symbol_counts"]=={"A":3},"count")
    require(LIMITS["mutation"]=="NO_MUTATION","policy")
    print("PASS: recipe multiplicity and fail-closed scope")
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--jar",type=Path);p.add_argument("--output",type=Path);p.add_argument("--javap",default="javap");p.add_argument("--self-test",action="store_true");a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar and a.output and not a.output.exists(),"inputs and write-once output")
        report=scan(a);raw=canonical(report).encode();require(len(raw)<=2_000_000,"report budget");a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        print("RESOURCE_PROJECTION",json.dumps(report["resources"],sort_keys=True))
        print("CRITERION_FIELD",json.dumps(report["criterion_field"],sort_keys=True))
        for owner,rows in report["classes"].items():
            print("OWNER",owner,rows["sha256"])
            for m in rows["methods"]:print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
        print("NO_MUTATION WORLD_SAFETY_BLOCKED NOT_CERTIFIED")
