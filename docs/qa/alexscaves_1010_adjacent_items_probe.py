#!/usr/bin/env python3
"""Batch binary discovery of five adjacent item/support classes; no certification."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import zipfile
from alexscaves_1010_armor_material_audit import ClassReader,canonical,digest,require,verify_artifact,SHA1,SHA256,SIZE
from alexscaves_1010_enchantable_item_probe import disassemble,summarize

PREFIX="com/github/alexmodguy/alexscaves/server/item/"
NAMES=("AlwaysCombinableOnAnvil","BiomeTreatItem","BlockItemWithISTER","BlockItemWithScaffolding","BlockItemWithSupplierLore")
TARGETS=tuple(PREFIX+n for n in NAMES)
REGISTRY=PREFIX+"ACItemRegistry"
FACTORY=("lambda$static$197","()Lnet/minecraft/world/item/Item;")

def inherit(owner,target,hierarchy,chain=()):
    if owner==target:return True
    require(owner not in chain,"hierarchy cycle")
    data=hierarchy.get(owner)
    return bool(data and any(inherit(p,target,hierarchy,(*chain,owner)) for p in (data["parent"],*data["interfaces"]) if p))

def inspect(jar,javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        paths=z.namelist()
        classes=sorted(p for p in paths if p.endswith(".class"))
        require(len(paths)==len(set(paths)) and len(classes)==1555,"artifact roster drift")
        hierarchy={}
        typed={t:{} for t in TARGETS}
        refs={t:{} for t in TARGETS}
        for p in classes:
            rd=ClassReader(z.read(p))
            require(rd.name+".class"==p and rd.major==65,"class identity drift")
            hierarchy[rd.name]={"parent":rd.parent,"interfaces":rd.interfaces,"access":rd.access}
            for target in TARGETS:
                found=rd.typed_refs(target)
                if found:typed[target][rd.name]=found
            for i,entry in enumerate(rd.pool):
                if entry is None or entry[0] not in (9,10,11):continue
                tag,owner,sig=rd.resolve(i)
                target=owner if owner in TARGETS else PREFIX+"BiomeTreatItem" if owner==REGISTRY and sig[1]=="BIOME_TREAT" else None
                if target:
                    refs[target].setdefault(rd.name,[]).append({"index":i,"owner":owner,"tag":tag,"name":sig[1],"descriptor":sig[2]})
        result={}
        requested=set()
        for target in TARGETS:
            rd=ClassReader(z.read(target+".class"))
            descendants=sorted(o for o in hierarchy if o!=target and inherit(o,target,hierarchy))
            ancestors=[]
            cur=rd.parent
            while cur in hierarchy:
                require(cur not in ancestors,"ancestor cycle")
                ancestors.append(cur)
                cur=hierarchy[cur]["parent"]
            requested.update((target,*refs[target],*ancestors))
            result[target]={"class_sha256":digest(z.read(target+".class")),"hierarchy":hierarchy[target],
                "fields":rd.fields,"declarations":rd.methods,"descendants":descendants,
                "in_jar_ancestors":ancestors,"typed_census":typed[target],"member_refs":refs[target]}
        require(len(requested)<=100,"candidate budget")
        parsed={}
        for owner in sorted(requested):
            rd=ClassReader(z.read(owner+".class"))
            parsed[owner]=disassemble(jar,javap,owner) if any("code_sha256" in m for m in rd.methods) else {}
        for target,data in result.items():
            own=ClassReader(z.read(target+".class"))
            data["methods"]=[summarize(own,k,v) for k,v in sorted(parsed[target].items()) if v]
            require(len(data["methods"])==sum("code_sha256" in m for m in own.methods),"own method coverage")
            data["ancestors"]={}
            for owner in data["in_jar_ancestors"]:
                rd=ClassReader(z.read(owner+".class"))
                data["ancestors"][owner]={"class_sha256":digest(z.read(owner+".class")),
                    "methods":[summarize(rd,k,v) for k,v in sorted(parsed[owner].items()) if v]}
            consumers={}
            for owner,group in data["member_refs"].items():
                lookup={x["index"]:x for x in group}
                sites=[]
                for k,body in sorted(parsed[owner].items()):
                    for off,(op,operand,symbol) in sorted(body.items()):
                        cp=re.match(r"#(\d+)",operand)
                        if cp and int(cp[1]) in lookup:
                            sites.append({"method":k[0],"descriptor":k[1],"offset":off,"opcode":op,
                                          "symbol":symbol,"reference":lookup[int(cp[1])]})
                consumers[owner]={"class_sha256":digest(z.read(owner+".class")),"sites":sites}
            data["consumers"]=consumers
        reg=ClassReader(z.read(REGISTRY+".class"))
        fac=parsed.get(REGISTRY) or disassemble(jar,javap,REGISTRY)
        require(FACTORY in fac,"biome treat factory missing")
        resources={}
        for p in paths:
            if p.endswith(".json") and "biome_treat" in p:
                raw=z.read(p)
                resources[p]={"sha256":digest(raw),"size":len(raw),"json":json.loads(raw)}
        return {"class_entries_scanned":len(classes),"targets":result,
                "biome_treat_factory":summarize(reg,FACTORY,fac[FACTORY]),"biome_treat_resources":resources}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ("jar","javap","output"):p.add_argument("--"+k,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists(),"new report required")
    report={"scope":"DISCOVERY_NOT_CERTIFIED","artifact":{"version":"1.0.10","sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "native":inspect(a.jar,a.javap),"mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","provider_universe_closed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(canonical(report),encoding="utf8")
    print("REPORT_SHA256",digest(a.output.read_bytes()))
    for owner,data in report["native"]["targets"].items():
        print("TARGET",owner,json.dumps({k:v for k,v in data.items() if k not in ("methods","ancestors")},sort_keys=True))
        for m in data["methods"]:print("METHOD",owner,json.dumps(m,sort_keys=True))
        for parent,group in data["ancestors"].items():
            print("ANCESTOR",owner,parent,group["class_sha256"])
            for m in group["methods"]:print("ANCESTOR_METHOD",owner,parent,json.dumps(m,sort_keys=True))
    print("BIOME_TREAT_FACTORY",json.dumps(report["native"]["biome_treat_factory"],sort_keys=True))
    print("BIOME_TREAT_RESOURCES",json.dumps(report["native"]["biome_treat_resources"],sort_keys=True))
    print("END_ADJACENT_ITEM_DISCOVERY")
if __name__=="__main__":main()
