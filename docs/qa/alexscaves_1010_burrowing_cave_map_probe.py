#!/usr/bin/env python3
"""SHA-exact discovery of the next six physical item classes; no certification."""
from __future__ import annotations
import argparse,json,re,zipfile
from pathlib import Path
from alexscaves_1010_armor_material_audit import ClassReader,canonical,digest,require,verify_artifact,SHA1,SHA256,SIZE
from alexscaves_1010_enchantable_item_probe import disassemble,summarize
PREFIX="com/github/alexmodguy/alexscaves/server/item/"
NAMES=["BurrowingArrowItem","CandyCaneHookItem","CaveBoatItem","CaveBookItem","CaveInfoItem","CaveMapItem"]
TARGETS=tuple(PREFIX+n for n in NAMES)
def inherits(owner,target,hierarchy,seen=()):
    if owner==target:return True
    require(owner not in seen,"hierarchy cycle")
    data=hierarchy.get(owner)
    return bool(data and any(inherits(p,target,hierarchy,(*seen,owner)) for p in (data["parent"],*data["interfaces"]) if p))
def inspect(jar,javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        paths=z.namelist()
        classes=sorted(x for x in paths if x.endswith(".class"))
        require(len(paths)==len(set(paths)) and len(classes)==1555,"artifact roster drift")
        hierarchy={}; typed={t:{} for t in TARGETS}; refs={t:{} for t in TARGETS}
        for path in classes:
            rd=ClassReader(z.read(path))
            require(rd.name+".class"==path and rd.major==65,"class identity drift")
            hierarchy[rd.name]={"parent":rd.parent,"interfaces":rd.interfaces,"access":rd.access}
            for t in TARGETS:
                found=rd.typed_refs(t)
                if found:typed[t][rd.name]=found
            for i,entry in enumerate(rd.pool):
                if entry is None or entry[0] not in (9,10,11):continue
                tag,owner,sig=rd.resolve(i)
                if owner in TARGETS:
                    refs[owner].setdefault(rd.name,[]).append({"index":i,"owner":owner,"tag":tag,"name":sig[1],"descriptor":sig[2]})
        cache={}
        def parsed(owner):
            if owner not in cache:
                rd=ClassReader(z.read(owner+".class"))
                cache[owner]=(rd,disassemble(jar,javap,owner) if any("code_sha256" in m for m in rd.methods) else {})
                require(len(cache)<=160,"candidate budget exceeded")
            return cache[owner]
        out={}
        for t in TARGETS:
            rd,body=parsed(t)
            ancestors=[]; cur=rd.parent
            while cur in hierarchy:
                require(cur not in ancestors,"ancestor cycle")
                ancestors.append(cur);cur=hierarchy[cur]["parent"]
            own=[summarize(rd,k,v) for k,v in sorted(body.items()) if v]
            require(len(own)==sum("code_sha256" in m for m in rd.methods),"own body coverage")
            consumers={}
            for owner in sorted(set(typed[t])|set(refs[t])):
                other,methods=parsed(owner)
                lookup={v["index"]:v for v in refs[t].get(owner,[])}
                typeidx={v["index"] for v in typed[t].get(owner,[]) if v["kind"]=="class_constant"}
                sites=[]; selected=[]
                for k,v in sorted(methods.items()):
                    local=[]
                    for off,(op,operand,symbol) in sorted(v.items()):
                        cp=re.match(r"#(\d+)",operand)
                        if cp and (int(cp[1]) in lookup or int(cp[1]) in typeidx):
                            local.append({"method":k[0],"descriptor":k[1],"offset":off,"opcode":op,"symbol":symbol,"constant_pool_index":int(cp[1])})
                    if local:
                        sites+=local
                        selected.append(summarize(other,k,v))
                consumers[owner]={"class_sha256":digest(z.read(owner+".class")),"sites":sites,"bodies":selected}
            prior={}
            for parent in ancestors:
                p,methods=parsed(parent)
                prior[parent]={"class_sha256":digest(z.read(parent+".class")),"methods":[summarize(p,k,v) for k,v in sorted(methods.items()) if v]}
            out[t]={"class_sha256":digest(z.read(t+".class")),"hierarchy":hierarchy[t],"fields":rd.fields,"declarations":rd.methods,"attributes":rd.attributes,"descendants":sorted(o for o in hierarchy if o!=t and inherits(o,t,hierarchy)),"in_jar_ancestors":ancestors,"typed_census":typed[t],"member_refs":refs[t],"methods":own,"consumers":consumers,"ancestors":prior}
        # Resource census is filename-based discovery only, not proof of all registry identities.
        names=("burrowing_arrow","candy_cane_hook","cave_boat","cave_book","cave_info","cave_map")
        resources={}
        for p in paths:
            if p.endswith(".json") and any(n in p for n in names):
                raw=z.read(p); resources[p]={"sha256":digest(raw),"size":len(raw),"json":json.loads(raw)}
        return {"class_entries_scanned":len(classes),"targets":out,"filename_matched_resources":resources}
def compact(m):
    return {k:m[k] for k in ("declaration","instruction_count","instruction_sha256")}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ("jar","javap","output"):p.add_argument("--"+k,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists(),"new report required")
    report={"scope":"DISCOVERY_NOT_CERTIFIED","artifact":{"version":"1.0.10","sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},"native":inspect(a.jar,a.javap),"mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","provider_universe_closed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(canonical(report),encoding="utf8")
    print("REPORT_SHA256",digest(a.output.read_bytes()))
    for owner,data in report["native"]["targets"].items():
        print("TARGET",owner,json.dumps({k:v for k,v in data.items() if k not in ("methods","consumers","ancestors")},sort_keys=True))
        for m in data["methods"]:
            print("METHOD",owner,json.dumps(m,sort_keys=True))
        for c,v in data["consumers"].items():
            print("CONSUMER",owner,c,json.dumps({"class_sha256":v["class_sha256"],"sites":v["sites"],"bodies":[compact(m) for m in v["bodies"]]},sort_keys=True))
        for c,v in data["ancestors"].items():
            print("ANCESTOR",owner,c,json.dumps({"class_sha256":v["class_sha256"],"methods":[compact(m) for m in v["methods"]]},sort_keys=True))
    print("RESOURCES",json.dumps(report["native"]["filename_matched_resources"],sort_keys=True))
    print("END_SIX_CLASS_DISCOVERY")
if __name__=="__main__":main()
