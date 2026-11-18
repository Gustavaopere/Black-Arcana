#!/usr/bin/env python3
"""Read-only SHA-exact food builder and immediate consumer discovery.

Extract typed member references and selected bounded method evidence; do not
load provider classes, reproduce implementation, or equate food with casts.
ACFoods and ACFoodPropertiesItem are adjacent consumers, not certified here.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import zipfile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, rows, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_destroyed_item_engine_reference import verify_artifact as verify_engine, ARTIFACTS

P="com/github/alexmodguy/alexscaves/"
TARGET=P+"server/item/ACFoodBuilder"
ADJACENT=(P+"server/item/ACFoodPropertiesItem",P+"server/item/ACFoods")
ENGINE=("net/neoforged/neoforge/common/extensions/IItemExtension",
        "net/neoforged/neoforge/common/extensions/IItemStackExtension",
        "net/neoforged/neoforge/common/CommonHooks")
ENAMES={"getFoodProperties","onItemUseFinish","getFoodPropertiesFromItem"}
FOOD_TOKENS=re.compile(r"FoodProperties|MobEffectInstance|finishUsingItem|consume|eat\b|getFoodProperties|LivingEntityUseItemEvent")


def refs_for(reader,targets):
    refs=[]
    for i,e in enumerate(reader.pool):
        if e is None or e[0] not in (9,10,11):
            continue
        tag,owner,sig=reader.resolve(i)
        if owner in targets:
            refs.append({"index":i,"kind":tag,"owner":owner,"name":sig[1],"descriptor":sig[2]})
    return refs


def inspect(jar,javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        paths=z.namelist()
        require(len(paths)==len(set(paths)),"duplicate members")
        classes=sorted(p for p in paths if p.endswith(".class"))
        require(len(classes)==1555,"class roster drift")
        targets={TARGET,*[p[:-6] for p in classes if p.startswith(TARGET+"$")]}
        focus=targets|set(ADJACENT)
        census={}
        consumers={}
        for path in classes:
            rd=ClassReader(z.read(path))
            require(rd.name+".class"==path and rd.major==65,"class identity drift")
            typed={t:rd.typed_refs(t) for t in sorted(focus)}
            typed={t:v for t,v in typed.items() if v}
            refs=refs_for(rd,focus)
            if typed or refs:
                census[rd.name]={"typed":typed,"member_refs":refs}
            if rd.name in targets or any(r["owner"] in targets for r in refs) or rd.name in ADJACENT:
                consumers[rd.name]=rd
        require(TARGET in consumers and len(consumers)<=30,"unexpected builder consumer count")
        data={}
        for owner,rd in sorted(consumers.items()):
            parsed=disassemble(jar,javap,owner)
            refs={r["index"]:r for r in census.get(owner,{}).get("member_refs",[])}
            selected=[]
            for k,body in sorted(parsed.items()):
                if not body:
                    continue
                sites=[]
                for off,(op,operand,symbol) in sorted(body.items()):
                    match=re.match(r"#(\d+)",operand)
                    if match and int(match.group(1)) in refs and (op.startswith("invoke") or op in ("getstatic","putstatic","getfield","putfield")):
                        sites.append({"offset":off,"opcode":op,"reference":refs[int(match.group(1))]})
                own=owner in targets
                adj=owner in ADJACENT
                keep=own or bool(sites) or (adj and (k[0] in ("<init>","<clinit>") or "FoodProperties" in k[1]))
                if keep:
                    require(len(body)<=1800,"method beyond discovery budget "+str(k))
                    item={"declaration":next(m for m in rd.methods if (m["name"],m["descriptor"])==k),
                          "instruction_count":len(body),"instruction_sha256":digest(canonical(rows(body)).encode()),
                          "typed_sites":sites}
                    # Small causal bodies only; for large registry init, use a symbolic
                    # window around exact member calls/field writes, not entire method.
                    offsets=sorted(body)
                    if own or (len(body)<=120 and (sites or adj)):
                        item["pivots"]=rows(body)
                    else:
                        selected_offsets=set()
                        for site in sites:
                            i=offsets.index(site["offset"])
                            selected_offsets.update(offsets[max(i-9,0):i+5])
                        item["pivots"]=rows({i:body[i] for i in sorted(selected_offsets)})
                    boot=[]
                    for off,(op,operand,symbol) in sorted(body.items()):
                        mat=re.search(r"InvokeDynamic #(\d+):",symbol)
                        if mat and (own or off in {r["offset"] for r in item["pivots"]}):
                            idx=int(mat.group(1))
                            table=rd.attributes.get("bootstrap_methods",[])
                            require(idx<len(table),"bootstrap out of bounds")
                            boot.append({"offset":off,"bootstrap":table[idx]})
                    item["bootstraps"]=boot
                    selected.append(item)
            data[owner]={"class_sha256":digest(z.read(owner+".class")),"parent":rd.parent,
                         "interfaces":rd.interfaces,"fields":rd.fields,"method_declarations":rd.methods if owner in focus else [],
                         "selected_methods":selected}
        return {"class_entries_scanned":len(classes),"class_roster_sha256":digest(("\n".join(classes)+"\n").encode()),
                "target_owners":sorted(targets),"typed_census":census,"consumers":data,
                "scope":"complete builder declared methods and bounded direct typed consumer evidence; no unrelated gameplay closure"}


def engine(universal,userdev,javap):
    verify_engine(universal,"universal")
    verify_engine(userdev,"userdev")
    out={}
    with zipfile.ZipFile(universal) as z:
        for owner in ENGINE:
            raw=z.read(owner+".class")
            rd=ClassReader(raw)
            parsed=disassemble(universal,javap,owner)
            out[owner]={"class_sha256":digest(raw),"methods":[summarize(rd,k,b) for k,b in sorted(parsed.items()) if k[0] in ENAMES]}
    patches=[]
    with zipfile.ZipFile(userdev) as z:
        names={"Item.java.patch","ItemStack.java.patch","FoodProperties.java.patch","LivingEntity.java.patch","Player.java.patch"}
        for path in sorted(p for p in z.namelist() if p.startswith("patches/") and Path(p).name in names):
            raw=z.read(path)
            matches=[{"line":i+1,"text":s} for i,s in enumerate(raw.decode("utf8").splitlines()) if FOOD_TOKENS.search(s)]
            patches.append({"entry":path,"sha256":digest(raw),"food_reference_lines":matches})
    return {"version":"21.1.250","artifacts":ARTIFACTS,"universal":out,"patches":patches,
            "scope":"official universal and userdev reference, not installed transformed runtime"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("jar","javap","universal","userdev","output"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists() and a.output.suffix==".json","new JSON required")
    report={"schema":"AC_FOOD_BUILDER_DISCOVERY_V1","scope":"DISCOVERY_NOT_CERTIFIED",
            "artifact":{"version":"1.0.10","size_bytes":SIZE,"sha1":SHA1,"sha256":SHA256},
            "native":inspect(a.jar,a.javap),"engine":engine(a.universal,a.userdev,a.javap),
            "mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
            "provider_universe_closed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(canonical(report),encoding="utf8")
    print("REPORT_SHA256",digest(a.output.read_bytes()))
    print("TARGETS",json.dumps(report["native"]["target_owners"]))
    print("CENSUS",json.dumps({k:sorted(v["typed"]) for k,v in report["native"]["typed_census"].items()}))
    for owner,data in report["native"]["consumers"].items():
        print("OWNER",owner,data["class_sha256"],data["parent"],json.dumps(data["interfaces"]))
        print("FIELDS",json.dumps(data["fields"]))
        for m in data["selected_methods"]:
            print("METHOD",m["declaration"]["name"],m["declaration"]["descriptor"],m["instruction_count"],m["declaration"].get("code_sha256"))
            for row in m["pivots"]:
                print(" ",row["offset"],row["opcode"],row["operand"],row["symbol"])
            if m["bootstraps"]:
                print("BOOTSTRAPS",json.dumps(m["bootstraps"]))
    for owner,data in report["engine"]["universal"].items():
        for m in data["methods"]:
            print("ENGINE_METHOD",owner,m["declaration"]["name"],m["declaration"]["descriptor"],json.dumps(m["instructions"]))
    for patch in report["engine"]["patches"]:
        print("ENGINE_PATCH",patch["entry"],patch["sha256"],json.dumps(patch["food_reference_lines"]))
    print("END_FOOD_BUILDER_DISCOVERY NO_MUTATION")


if __name__=="__main__":
    main()
