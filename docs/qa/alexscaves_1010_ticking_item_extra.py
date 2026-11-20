#!/usr/bin/env python3
"""Additional bounded tick caller, durability and radiation parameter reference."""
import argparse
import json
from pathlib import Path
import re
import zipfile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
import alexscaves_1010_repairable_item_boundary as reference

PREFIX="com/github/alexmodguy/alexscaves/server/item/"
TARGETS={
    "net.minecraft.world.entity.player.Player":{"aiStep"},
    "net.minecraft.world.entity.player.Inventory":{"<init>"},
    "net.minecraft.world.item.ItemStack":{"getDamageValue","setDamageValue","getMaxDamage"},
}
NATIVE={
    "HazmatArmorItem":{"getWornAmount"},
    "RadioactiveItem":{"<init>"},
    "RadioactiveBlockItem":{"<init>"},
    "RadioactiveOnDestroyedBlockItem":{"<init>"},
}

def native(jar,javap):
    verify_artifact(jar)
    result={}
    with zipfile.ZipFile(jar) as z:
        for short, names in NATIVE.items():
            owner=PREFIX+short
            rd=ClassReader(z.read(owner+".class"))
            parsed=disassemble(jar,javap,owner)
            methods=[summarize(rd,k,v) for k,v in sorted(parsed.items()) if k[0] in names]
            require(names <= {m["declaration"]["name"] for m in methods}, "missing native target")
            result[owner]={"class_sha256":digest(z.read(owner+".class")),"parent":rd.parent,"fields":rd.fields,"methods":methods}
        # Identify exact references to the constructors; do not equate CP refs with actual instances.
        types={PREFIX+x for x in ("RadioactiveItem","RadioactiveBlockItem","RadioactiveOnDestroyedBlockItem")}
        refs={}
        for p in sorted(z.namelist()):
            if not p.endswith(".class"): continue
            rd=ClassReader(z.read(p))
            selected=[]
            for i,entry in enumerate(rd.pool):
                if entry is None or entry[0]!=10: continue
                tag,owner,sig=rd.resolve(i)
                if owner in types and sig[1]=="<init>":
                    selected.append({"index":i,"owner":owner,"descriptor":sig[2]})
            if selected: refs[rd.name]=selected
        return {"classes":result,"constructor_refs":refs}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ("jar","javap","output"):p.add_argument("--"+k,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists(),"new report required")
    tmp=a.output.parent/"tick-extra-reference"
    tmp.mkdir()
    reference.TARGETS=TARGETS
    report={"scope":"STATIC_REFERENCE_ONLY","native":native(a.jar,a.javap),
            "vanilla":reference.vanilla(tmp,a.javap),"mutation":"NO_MUTATION","physical_qa":"NOT_TESTED","mutating_hook":"NOT_VERIFIED"}
    a.output.write_text(canonical(report),encoding="utf8")
    print("EXTRA_SHA256",digest(a.output.read_bytes()))
    print("NATIVE_EXTRA",json.dumps(report["native"],sort_keys=True))
    for owner,data in report["vanilla"]["classes"].items():
        print("VANILLA_EXTRA_OWNER",owner,data["obfuscated_owner"],data["class_sha256"],data["parent"])
        for m in data["methods"]:print("VANILLA_EXTRA_METHOD",owner,json.dumps(m,sort_keys=True))

if __name__=="__main__":main()
