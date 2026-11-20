#!/usr/bin/env python3
"""SHA-exact AlexMealItem discovery, concrete class and typed consumers."""
import argparse
import json
from pathlib import Path
import re
import zipfile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

TARGET="com/github/alexmodguy/alexscaves/server/item/AlexMealItem"
REGISTRY="com/github/alexmodguy/alexscaves/server/item/ACItemRegistry"
FACTORY=("lambda$static$196","()Lnet/minecraft/world/item/Item;")

def inspect(jar,javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        paths=z.namelist()
        require(len(paths)==len(set(paths)),"duplicate ZIP members")
        classes=sorted(p for p in paths if p.endswith(".class"))
        require(len(classes)==1555,"class roster drift")
        rd=ClassReader(z.read(TARGET+".class"))
        all_methods=disassemble(jar,javap,TARGET)
        bodies=[summarize(rd,k,v) for k,v in sorted(all_methods.items()) if v]
        require(len(bodies)==sum("code_sha256" in m for m in rd.methods),"target body coverage")
        typed={}
        hierarchy={}
        refs={}
        for p in classes:
            c=ClassReader(z.read(p))
            require(c.name+".class"==p and c.major==65,"class identity drift")
            hierarchy[c.name]={"parent":c.parent,"interfaces":c.interfaces}
            found=c.typed_refs(TARGET)
            if found:typed[c.name]=found
            matched=[]
            for i,e in enumerate(c.pool):
                if e is None or e[0] not in (9,10,11):continue
                tag,owner,sig=c.resolve(i)
                if owner==TARGET or (owner==REGISTRY and sig[1]=="ALEX_MEAL"):
                    matched.append({"index":i,"owner":owner,"tag":tag,"name":sig[1],"descriptor":sig[2]})
            if matched:refs[c.name]=matched
        descendants=[]
        for owner in hierarchy:
            if owner==TARGET:continue
            cur=hierarchy[owner]["parent"]
            seen=set()
            while cur in hierarchy:
                require(cur not in seen,"cycle")
                seen.add(cur)
                if cur==TARGET:
                    descendants.append(owner)
                    break
                cur=hierarchy[cur]["parent"]
        consumers={}
        for owner in sorted(refs):
            c=ClassReader(z.read(owner+".class"))
            by_index={x["index"]:x for x in refs[owner]}
            parsed=disassemble(jar,javap,owner)
            hits=[]
            for k,body in sorted(parsed.items()):
                for off,(op,operand,symbol) in sorted(body.items()):
                    cp=re.match(r"#(\d+)",operand)
                    if cp and int(cp[1]) in by_index:
                        hits.append({"method":k[0],"descriptor":k[1],"offset":off,"opcode":op,"symbol":symbol,"reference":by_index[int(cp[1])]})
            consumers[owner]={"class_sha256":digest(z.read(owner+".class")),"sites":hits}
        registry=ClassReader(z.read(REGISTRY+".class"))
        factory=disassemble(jar,javap,REGISTRY)
        require(FACTORY in factory,"factory absent")
        summary=summarize(registry,FACTORY,factory[FACTORY])
        resources={}
        for p in paths:
            if not p.endswith(".json") or not any(s in p for s in ("alex_meal","alex_meal_item")):continue
            raw=z.read(p)
            resources[p]={"sha256":digest(raw),"size":len(raw),"json":json.loads(raw)}
        return {"class_entries_scanned":len(classes),"target":TARGET,"class_sha256":digest(z.read(TARGET+".class")),
                "parent":rd.parent,"interfaces":rd.interfaces,"fields":rd.fields,"declarations":rd.methods,
                "methods":bodies,"descendants":sorted(descendants),"typed_census":typed,"member_refs":refs,
                "consumers":consumers,"factory":summary,"resources":resources}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for x in ("jar","javap","output"):p.add_argument("--"+x,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists(),"new output required")
    report={"scope":"DISCOVERY_NOT_CERTIFIED","artifact":{"version":"1.0.10","sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "native":inspect(a.jar,a.javap),"mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","provider_universe_closed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(canonical(report),encoding="utf8")
    print("REPORT_SHA256",digest(a.output.read_bytes()))
    print("NATIVE",json.dumps(report["native"],sort_keys=True))
    print("END_ALEX_MEAL_DISCOVERY")
if __name__=="__main__":main()
