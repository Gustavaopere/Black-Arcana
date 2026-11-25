#!/usr/bin/env python3
"""Read-only publisher-exact audit of Resistor Shield inherited audio lifecycle.
Scope: observed ItemTickableSound superclass and ResistorShieldSound, not
the client sound engine or transformed runtime.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection

ROOT = "com/github/alexmodguy/alexscaves/client/sound/"
CHILD = ROOT + "ResistorShieldSound"
PARENT = ROOT + "ItemTickableSound"
CHILD_SHA = "ce6dfd8dd29846aef7f139f313997119a0eae1e40277a28924b0a863236d2b1d"
CHILD_CODE = {
    "<init>": "1949fd7cc2fd98f9d31295aa2537f2d323940441c18b59c8e4605fc75ce3838b",
    "isValidItem": "7b2508b51d3560bc79137aecb470ff0a5831fdf8c3722b9a2287f9ab86248458",
    "tickVolume": "2f0372825d04c50e73fc91e987e7600678b7b2dbdf27c350712f6c3e39734bfa",
    "isAzure": "f33eb3645199a92a72da61be7b282d9a17a50e0648b912834e99f6b271d78e9e",
}
LIMITS = {"scope":"STATIC_DISCOVERY_ONLY","static_contract":"NOT_CERTIFIED",
          "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
          "mutation":"NO_MUTATION","provider_universe_closed":False,
          "semantic_magic_roots_delta":0}

def selected(owner):
    return owner in {CHILD,PARENT}

def inspect(jar,javap):
    verify_artifact(jar)
    out={}
    with ZipFile(jar) as z:
        paths=z.namelist()
        require(len(paths)==len(set(paths)) and sum(x.endswith(".class") for x in paths)==1555,"publisher class roster")
        for owner in sorted({CHILD,PARENT}):
            raw=z.read(owner+".class")
            rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"class identity")
            if owner==CHILD:
                require(digest(raw)==CHILD_SHA and rd.parent==PARENT,"previous child identity or superclass mismatch")
                require(len(rd.methods)==4 and {d["name"]:d.get("code_sha256") for d in rd.methods}==CHILD_CODE,"child Code pins")
            require(0<len(rd.methods)<=30,"owner method budget")
            parsed=disassemble(jar,javap,owner)
            rows=[]
            for d in rd.methods:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    rows.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]) and len(parsed[key])<=600,"body scope")
                row=projection(rd,key,parsed[key],d)
                row["executable"]=True
                rows.append(row)
            out[owner]={"class_sha256":digest(raw),"parent":rd.parent,"interfaces":rd.interfaces,"fields":rd.fields,"methods":rows}
    require(any(m["name"]=="<init>" and m["executable"] for m in out[PARENT]["methods"]),"inherited constructor")
    require(sum(len(v["methods"]) for v in out.values())<=40,"method budget")
    return {"schema":1,"artifact":{"sha1":SHA1,"sha256":SHA256,"size":SIZE},"classes":out,"limits":LIMITS}

def self_test():
    require(selected(CHILD) and selected(PARENT),"scope")
    require(not selected("foreign/ItemTickableSound"),"exact owner")
    require(len(CHILD_CODE)==4 and all(len(x)==64 for x in CHILD_CODE.values()),"Code pin roster")
    require(LIMITS["mutation"]=="NO_MUTATION" and LIMITS["static_contract"]=="NOT_CERTIFIED","policy")
    print("PASS four scope and policy checks")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path);p.add_argument("--output",type=Path)
    p.add_argument("--javap",default="javap");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar is not None and a.output is not None and not a.output.exists(),"write once")
        report=inspect(a.jar,a.javap);raw=canonical(report).encode()
        require(len(raw)<=1000000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in report["classes"].items():
            print("OWNER",owner,row["class_sha256"],"PARENT",row["parent"],"METHODS",len(row["methods"]))
            for method in row["methods"]:print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION")
