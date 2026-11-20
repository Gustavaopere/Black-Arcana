#!/usr/bin/env python3
"""Read-only SHA-exact CaveBookItem and bounded UI/progression candidate inspection."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

SHA1="6960b299a39a039ac8a5eb9b07be4ad0e3e0a570"
SHA256="36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
SIZE=75279314
ITEM="com/github/alexmodguy/alexscaves/server/item/CaveBookItem"
ITEM_SHA="84177c0ff1fdb42d766262624f877874c7c6db22a16036faf4dd6fe0540fcacf"
MARKERS=(b"openBookGUI",b"CaveBookItem",b"cave_book",b"LecternBooks",
         b"BookProgress",b"bookProgress",b"CaveBook",b"CONSUME_ITEM")
MAX_CAPTURE=26

def digest(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def relevant_classes(classes:dict[str,bytes])->tuple[list[str],list[dict]]:
    matched=[]
    for path,raw in sorted(classes.items()):
        short=path.rsplit("/",1)[-1]
        hits=[m.decode("ascii") for m in MARKERS if m in raw]
        if not hits and not any(v in short for v in ("Book","Codex","Lectern")):
            continue
        prio=(10000 if path==ITEM+".class" else 0)
        prio+=2200*("openBookGUI" in hits)+1300*("CaveBookItem" in hits)
        prio+=450*any(v in short for v in ("Book","Codex","Lectern"))
        prio+=400*("LecternBooks" in hits)+100*("cave_book" in hits)
        matched.append({"path":path,"priority":prio,"markers":hits,
                        "sha256":digest(raw),"bytes":len(raw)})
    matched.sort(key=lambda row:(-row["priority"],row["path"]))
    selected=[x["path"] for x in matched[:MAX_CAPTURE]]
    if ITEM+".class" not in selected:
        raise RuntimeError("FAIL-CLOSED: item missing from bytecode candidates")
    return selected,matched

def resource_summary(path:str,raw:bytes)->dict:
    obj=json.loads(raw)
    if not isinstance(obj,dict):
        raise RuntimeError("FAIL-CLOSED: unexpected resource JSON "+path)
    data={"path":path,"sha256":digest(raw),"bytes":len(raw),
          "top_level_keys":sorted(obj),"resource_type":obj.get("type")}
    if "/recipe/" in path or "/recipes/" in path:
        refs=[]
        def visit(x):
            if isinstance(x,dict):
                for k,v in x.items():
                    if k in ("item","tag") and isinstance(v,str):refs.append({"kind":k,"id":v})
                    else:visit(v)
            elif isinstance(x,list):
                for v in x:visit(v)
        visit(obj.get("ingredients",[]))
        visit(obj.get("key",{}))
        data["ingredient_ids"]=sorted(refs,key=lambda x:(x["kind"],x["id"]))
        data["result"]=obj.get("result")
    elif "/advancement/" in path:
        data["parent"]=obj.get("parent")
        data["criteria_names"]=sorted(obj.get("criteria",{}))
        data["criterion_triggers"]={
            name:crit.get("trigger") for name,crit in obj.get("criteria",{}).items()
            if isinstance(crit,dict)}
        data["requirements"]=obj.get("requirements")
    elif "/models/item/" in path:
        data["model_parent"]=obj.get("parent")
        data["texture_keys"]=sorted(obj.get("textures",{}))
    return data

def run(jar:Path,javap:str,out:Path)->dict:
    raw=jar.read_bytes()
    if len(raw)!=SIZE or digest(raw)!=SHA256 or hashlib.sha1(raw).hexdigest()!=SHA1:
        raise RuntimeError("FAIL-CLOSED: exact publisher JAR mismatch")
    out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(jar) as z:
        paths=z.namelist()
        classpaths=sorted(p for p in paths if p.endswith(".class"))
        if len(paths)!=8898 or len(classpaths)!=1555 or len(set(paths))!=len(paths):
            raise RuntimeError("FAIL-CLOSED: publisher archive roster drift")
        classes={p:z.read(p) for p in classpaths}
        if digest(classes.get(ITEM+".class",b""))!=ITEM_SHA:
            raise RuntimeError("FAIL-CLOSED: CaveBookItem class mismatch")
        selected,candidates=relevant_classes(classes)
        resources=sorted([
            resource_summary(p,z.read(p)) for p in paths
            if p.endswith(".json") and "cave_book" in p],key=lambda row:row["path"])
        if not resources:raise RuntimeError("FAIL-CLOSED: cave_book resource census empty")
        outputs={}
        for path in selected:
            internal=path[:-6]
            cmd=[javap,"-v","-p","-c","-s","-classpath",str(jar),
                 internal.replace("/",".")]
            p=subprocess.run(cmd,check=True,capture_output=True,text=True)
            if not p.stdout.strip():raise RuntimeError("FAIL-CLOSED: javap empty "+internal)
            binary=p.stdout.encode("utf-8")
            name=internal.replace("/","_").replace("$","_")+".javap.txt"
            (out/name).write_bytes(binary)
            outputs[internal]={"class_sha256":digest(classes[path]),
                "class_bytes":len(classes[path]),"javap_sha256":digest(binary),
                "javap_lines":len(p.stdout.splitlines()),
                "transcript":name,"contains_code":"    Code:" in p.stdout}
    report={"scope":"DISCOVERY_NOT_CERTIFIED",
       "jar":{"version":"1.0.10","sha1":SHA1,"sha256":SHA256,"bytes":SIZE,
              "class_count":1555,"entry_count":8898},
       "item":{"class_name":ITEM,"class_sha256":ITEM_SHA},
       "candidates":candidates,"candidate_count":len(candidates),
       "captures":outputs,"capture_limit":MAX_CAPTURE,"resources":resources,
       "mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED",
       "physical_qa":"NOT_TESTED","provider_universe_closed":False}
    (out/"report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"DISCOVERY_NOT_CERTIFIED","candidates":len(candidates),
                      "captures":len(outputs),"resources":len(resources)}))
    return report

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    parser.add_argument("--javap",default="javap")
    parser.add_argument("--output-dir",type=Path,required=True)
    args=parser.parse_args()
    run(args.jar,args.javap,args.output_dir)
