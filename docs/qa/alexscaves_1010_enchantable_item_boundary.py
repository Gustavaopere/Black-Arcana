#!/usr/bin/env python3
"""Bounded vanilla/NeoForge enchanting reference and publisher resource crosswalk.

Official Mojang 1.21.1 client is used only as a reference for inherited vanilla
methods; it is not a transformed NeoForge runtime. Never load game classes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, rows
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_destroyed_item_engine_reference import verify_artifact as verify_engine
from minecraft_1211_mojang_mixin_target_mappings import CLASS, METHOD, official_version_downloads, official_get
from minecraft_1211_vanilla_target_callsites import jvm_type

NATIVE_REPORT_SHA256="d34a655d06d65a771ea9237ef222635e159ffcfa6fe8b454ee6826ee14979e73"
CLIENT_SHA1="30c73b1c5da787909b2f73340419fdf13b9def88"
ITEM="net.minecraft.world.item.Item"
STACK="net.minecraft.world.item.ItemStack"
HELPER="net.minecraft.world.item.enchantment.EnchantmentHelper"
VANILLA_METHODS={
    ITEM:{"getEnchantmentValue","isEnchantable"},
    STACK:{"isEnchantable","getCount","has","isEnchanted"},
    HELPER:{"getEnchantmentCost","selectEnchantment","getAvailableEnchantmentResults","canStoreEnchantments"},
}
EXTENSION="net/neoforged/neoforge/common/extensions/"
ENGINE_METHODS={"supportsEnchantment","isPrimaryItemFor","canApplyAtEnchantingTable","getEnchantmentValue"}
TAG_PREFIX="data/alexscaves/tags/item/"
ENCHANT_PREFIX="data/alexscaves/enchantment/"


def download(out,record,cap):
    require(record["url"].startswith("https://piston-data.mojang.com/"),"unexpected Mojang URL")
    b=official_get(record["url"],cap)
    require(len(b)==record["size"] and hashlib.sha1(b).hexdigest()==record["sha1"],"official download identity mismatch")
    out.write_bytes(b)
    return {"sha1":record["sha1"],"sha256":digest(b),"size_bytes":len(b),"url":record["url"]}


def vanilla(tmp,javap):
    metadata=official_version_downloads()
    d=metadata["downloads"]
    require(d["client"]["sha1"]==CLIENT_SHA1,"version hash drift")
    jar=tmp/"mojang-1.21.1-client.jar"
    mappings=tmp/"mojang-1.21.1-client-mappings.txt"
    identity={"metadata_sha1":metadata["json_sha1"],"client":download(jar,d["client"],35000000),
              "client_mappings":download(mappings,d["client_mappings"],15000000)}
    text=mappings.read_text(encoding="utf8")
    named={}
    owner=None
    mapped=[]
    for line in text.splitlines():
        if CLASS.fullmatch(line):
            owner,obf=line[:-1].split(" -> ")
            named[owner]=obf
            continue
        m=METHOD.fullmatch(line.strip()) if owner in VANILLA_METHODS else None
        if m and m.group(2) in VANILLA_METHODS[owner]:
            ret,name,args=m.groups()
            mapped.append((owner,name,ret,tuple(args.split(",")) if args else (),line.strip().rsplit(" -> ",1)[1]))
    def desc_type(t):
        dims=0
        while t.endswith("[]"):
            dims+=1
            t=t[:-2]
        known=dict(named)
        if t not in known and t not in {"boolean","byte","char","short","int","long","float","double","void"}:
            # Non-obfuscated JDK/external types retain binary names.
            known[t]=t
        return "["*dims+jvm_type(t,known)
    result={}
    with zipfile.ZipFile(jar) as z:
        for owner in VANILLA_METHODS:
            obf=named[owner].replace(".","/")
            raw=z.read(obf+".class")
            reader=ClassReader(raw)
            require(reader.name==obf and reader.major==65,"vanilla class identity drift")
            methods=disassemble(jar,javap,obf)
            selected={}
            for own,name,ret,args,m in mapped:
                if own!=owner:
                    continue
                descriptor="("+"".join(desc_type(a) for a in args)+")"+desc_type(ret)
                k=(m,descriptor)
                if k in selected:
                    continue
                require(k in methods,"mapped method absent: "+str((owner,name,k)))
                body=methods[k]
                require(len(body)<=400,"selected vanilla method exceeds bound")
                selected[k]={"named_method":name,"named_return":ret,"named_args":list(args),
                             **summarize(reader,k,body)}
            result[owner]={"obfuscated_owner":obf,"class_sha256":digest(raw),
                           "methods":list(selected.values())}
    for owner,name in ((ITEM,"isEnchantable"),(ITEM,"getEnchantmentValue"),(STACK,"isEnchantable")):
        require(any(m["named_method"]==name for m in result[owner]["methods"]),"missing vanilla declaration")
    # Keep only symbol-name mappings needed to interpret this selected scope.
    referenced={}
    with zipfile.ZipFile(jar) as z:
        for owner,data in result.items():
            reader=ClassReader(z.read(data["obfuscated_owner"]+".class"))
            ref=[]
            for m in data["methods"]:
                for row in m["instructions"]:
                    if not (row["opcode"].startswith("invoke") or row["opcode"] in ("getstatic","getfield")):
                        continue
                    cp=re.match(r"#(\d+)",row["operand"])
                    if not cp:
                        continue
                    resolved=reader.resolve(int(cp.group(1)))
                    if isinstance(resolved,list) and resolved[0] in (9,10,11):
                        ref.append({"method":m["named_method"],"offset":row["offset"],"member":resolved})
            referenced[owner]=ref
    inv={v.replace(".","/"):k for k,v in named.items()}
    targets={inv[r["member"][1]] for rs in referenced.values() for r in rs if r["member"][1] in inv}
    member_map={}
    owner=None
    field_re=re.compile(r"^(\S+)\s+([\w$]+)\s+->\s+(\S+)$")
    for line in text.splitlines():
        if CLASS.fullmatch(line):
            owner,obf=line[:-1].split(" -> ")
            continue
        if owner not in targets:
            continue
        m=METHOD.fullmatch(line.strip())
        f=field_re.fullmatch(line.strip())
        if m:
            ret,name,args=m.groups()
            desc="("+"".join(desc_type(a) for a in (args.split(",") if args else []))+")"+desc_type(ret)
            obf_name=line.strip().rsplit(" -> ",1)[1]
        elif f:
            ret,name,obf_name=f.groups()
            desc=desc_type(ret)
        else:
            continue
        key=(named[owner].replace(".","/"),obf_name,desc)
        member_map.setdefault(key,[]).append(owner+"."+name)
    for rs in referenced.values():
        for r in rs:
            _,owner,sig=r["member"]
            r["named_candidates"]=sorted(set(member_map.get((owner,sig[1],sig[2]),[])))
    return {"identity":identity,"classes":result,"resolved_member_references":referenced,
            "boundary":"vanilla client classfiles, official mappings; not transformed NeoForge runtime"}


def resources(jar):
    verify_artifact(jar)
    entries=[]
    tags={}
    with zipfile.ZipFile(jar) as z:
        for p in sorted(z.namelist()):
            if p.startswith(TAG_PREFIX) and p.endswith(".json"):
                raw=z.read(p)
                data=json.loads(raw)
                tags["#alexscaves:"+p[len(TAG_PREFIX):-5]]={"sha256":digest(raw),"replace":data.get("replace",False),"values":data.get("values",[])}
            elif p.startswith(ENCHANT_PREFIX) and p.endswith(".json"):
                raw=z.read(p)
                data=json.loads(raw)
                entries.append({"id":"alexscaves:"+p[len(ENCHANT_PREFIX):-5],"sha256":digest(raw),
                                "supported_items":data.get("supported_items"),"primary_items":data.get("primary_items"),
                                "weight":data.get("weight"),"max_level":data.get("max_level"),
                                "min_cost":data.get("min_cost"),"max_cost":data.get("max_cost"),
                                "anvil_cost":data.get("anvil_cost")})
        require(len(entries)==51,"publisher enchantment roster drift")
        refs=set()
        def collect(v):
            if isinstance(v,str) and v.startswith("#alexscaves:"):
                refs.add(v)
            elif isinstance(v,list):
                for x in v:
                    collect(x)
        for e in entries:
            collect(e["supported_items"])
            collect(e["primary_items"])
        selected={tag:tags[tag] for tag in sorted(refs) if tag in tags}
        return {"enchantments":entries,"direct_referenced_local_tags":selected,
                "unresolved_local_tags":sorted(refs-tags.keys()),
                "scope":"literal JSON and immediate local tag entries; no recursive tag closure, datapack merging, eligibility or application inferred"}


def neoforge(jar,javap):
    verify_engine(jar,"universal")
    result={}
    with zipfile.ZipFile(jar) as z:
        for name in ("IItemExtension","IItemStackExtension"):
            owner=EXTENSION+name
            raw=z.read(owner+".class")
            reader=ClassReader(raw)
            methods=disassemble(jar,javap,owner)
            result[owner]={"class_sha256":digest(raw),"methods":[summarize(reader,k,v) for k,v in sorted(methods.items()) if k[0] in ENGINE_METHODS]}
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("jar","universal","javap","native-report","output"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists() and a.output.suffix==".json","new output required")
    require(digest(a.native_report.read_bytes())==NATIVE_REPORT_SHA256,"native discovery report drift")
    tmp=a.output.parent/"mojang-downloads"
    tmp.mkdir(parents=True,exist_ok=False)
    doc={"schema":"AC_ENCHANTABLE_REFERENCE_V1","scope":"STATIC_REFERENCE_NOT_CERTIFIED",
         "native_report_sha256":NATIVE_REPORT_SHA256,"vanilla":vanilla(tmp,a.javap),
         "publisher_resources":resources(a.jar),"neoforge_universal":neoforge(a.universal,a.javap),
         "mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
         "provider_universe_closed":False}
    a.output.write_text(canonical(doc),encoding="utf8")
    print("BOUNDARY_SHA256",digest(a.output.read_bytes()))
    print("MOJANG_IDENTITY",json.dumps(doc["vanilla"]["identity"]))
    for owner,data in doc["vanilla"]["classes"].items():
        print("VANILLA_OWNER",owner,data["obfuscated_owner"],data["class_sha256"])
        for m in data["methods"]:
            print("VANILLA_METHOD",m["named_method"],m["named_args"],m["declaration"],m["instruction_count"])
            if m["named_method"] in ("isEnchantable","getEnchantmentValue","getCount","isEnchanted"):
                print("VANILLA_BODY",json.dumps(m["instructions"]))
        print("VANILLA_REFS",owner,json.dumps(doc["vanilla"]["resolved_member_references"][owner]))
    for owner,data in doc["neoforge_universal"].items():
        for m in data["methods"]:
            print("NEO_METHOD",owner,json.dumps(m))
    print("PUBLISHER_RESOURCES",json.dumps(doc["publisher_resources"]))
    print("END_BOUNDARY_DISCOVERY NO_MUTATION")


if __name__=="__main__":
    main()
