#!/usr/bin/env python3
"""SHA-exact read-only discovery of FloaterItem and FrostmintSpearItem.

Reuses the existing verified six-class typed consumer and bytecode scanner.
No certification, mutation or physical gameplay assertion.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
import alexscaves_1010_burrowing_cave_map_probe as discovery
from alexscaves_1010_armor_material_audit import SHA1,SHA256,SIZE,require,verify_artifact,canonical,digest

PREFIX="com/github/alexmodguy/alexscaves/server/item/"
NAMES=("FloaterItem","FrostmintSpearItem")
SPEAR_RELATED=("FrostmintSpearEntity","FrostmintSpear","Frozen","Frostmint")
RESOURCE_TERMS=("floater","frostmint","frost_mint")
FACTORIES=("lambda$static$103","lambda$static$192","lambda$static$193")

def read_resources(jar):
    resources={}
    with ZipFile(jar) as z:
        for path in sorted(z.namelist()):
            if not path.endswith(".json") or not any(t in path.lower() for t in RESOURCE_TERMS):
                continue
            raw=z.read(path)
            data=json.loads(raw)
            resources[path]={"sha256":digest(raw),"size":len(raw),"json":data}
    return resources

def run(jar,javap,output):
    verify_artifact(jar)
    discovery.TARGETS=tuple(PREFIX+n for n in NAMES)
    native=discovery.inspect(jar,javap)
    assert set(native["targets"])==set(discovery.TARGETS)
    resources=read_resources(jar)
    require(bool(resources),"no item resources matched, inspect publisher")
    native["filename_matched_resources"]=resources
    main={
        "scope":"DISCOVERY_NOT_CERTIFIED",
        "artifact":{"version":"1.0.10","filename":"alexscaves-1.0.10-neoforge+1.21.1.jar",
                    "sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "native":native,
        "next_unreviewed":"server/item/GalenaGauntletItem",
        "mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED","provider_universe_closed":False,
        "semantic_magic_roots_certified_delta":0,
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    require(not output.exists(),"write-once report required")
    output.write_text(canonical(main),encoding="utf-8")
    print("REPORT_SHA256",digest(output.read_bytes()))
    for owner,v in native["targets"].items():
        print("CLASS",owner,v["class_sha256"],"methods",len(v["methods"]),
              "consumers",len(v["consumers"]),"ancestors",len(v["ancestors"]))
        for m in v["methods"]:
            print("METHOD",owner,m["declaration"]["name"],m["declaration"]["descriptor"],
                  m.get("instruction_count"),m.get("instruction_sha256"))
        for c,v2 in v["consumers"].items():
            print("CALLER",owner,c,"sites",len(v2["sites"]),
                  "methods",[x["declaration"]["name"] for x in v2["bodies"]])
    print("RESOURCES",len(resources),json.dumps(sorted(resources)))
    print("STATIC_DISCOVERY_ONLY NO_MUTATION")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args();run(a.jar,a.javap,a.output)
