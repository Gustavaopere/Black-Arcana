#!/usr/bin/env python3
"""Hash-checked Mojang 1.21.1 CLIENT classfile callsite reconnaissance.

Counts selected invocation instructions in obfuscated vanilla classfiles, using
hash-checked official 1.21.1 client mappings to resolve names. No Mojang
binaries are distributed. NOT NeoForge-patched bytecode or applied Mixin QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

from minecraft_1211_mojang_mixin_target_mappings import (
    CLASS, METHOD, official_version_downloads, official_get, MC_VERSION
)

ENTITY="net.minecraft.world.entity.Entity"
LIVING="net.minecraft.world.entity.LivingEntity"
RANGED="net.minecraft.world.entity.ai.attributes.RangedAttribute"
VEC="net.minecraft.world.phys.Vec3"

TARGETS={
    ENTITY: [
        ("move", "void", ("net.minecraft.world.entity.MoverType",VEC)),
        ("collide",VEC,(VEC,)),
        ("tryCheckInsideBlocks","void",()),
        ("setDeltaMovement","void",("double","double","double")),
    ],
    LIVING: [
        ("travel","void",(VEC,)),
        ("handleRelativeFrictionAndCalculateMovement",VEC,(VEC,"float"))
    ]
}

HEADER=re.compile(r"^  .+\([^;]*\);$")
DESC=re.compile(r"^    descriptor: (\S+)$")
CALL=re.compile(r"^\s*(\d+):\s+(invokevirtual|invokespecial|invokestatic|invokeinterface)\s+#\d+\s+// (?:InterfaceMethod|Method) (?:(?P<owner>[\w/$]+)\.)?(?P<name>[\w$<>]+):(?P<desc>\S+)")
OPCODE=re.compile(r"^\s*(\d+):\s+(\w+)")
PUBLISHER_MAX=35000000

def official_client(downloads:dict, destination:Path):
    record=downloads["client"]
    # Do not bypass the official manifest if a CDN URL changes.
    if not record["url"].startswith("https://piston-data.mojang.com/"):
        raise ValueError("CLIENT_NOT_FROM_MOJANG")
    with destination.open("wb") as f:
        data=official_get(record["url"],PUBLISHER_MAX)
        f.write(data)
    if len(data)!=record["size"]:
        raise ValueError("OFFICIAL_CLIENT_SIZE_MISMATCH")
    sha1=hashlib.sha1(data).hexdigest()
    if sha1!=record["sha1"]:
        raise ValueError("OFFICIAL_CLIENT_SHA1_MISMATCH")
    with zipfile.ZipFile(destination) as z:
        if z.testzip() is not None:
            raise ValueError("OFFICIAL_CLIENT_ZIP_CORRUPT")
    return {"publisher_sha1":sha1,"bytes":len(data)}

def find_mappings(body:str):
    names=set(TARGETS)|{RANGED,VEC,"net.minecraft.world.entity.MoverType"}
    classes={}
    methods={}
    current=None
    for line in body.splitlines():
        x=CLASS.fullmatch(line)
        if x:
            current=x.group(1)
            if current in names:
                classes[current]=line.split(" -> ",1)[1][:-1]
            continue
        if current not in TARGETS or not line.startswith("    "):
            continue
        x=METHOD.fullmatch(line.strip())
        if x:
            ret,name,args=x.group(1),x.group(2),tuple(x.group(3).split(",")) if x.group(3) else ()
            if (name,ret,args) in TARGETS[current]:
                mapped=line.strip().rsplit(" -> ",1)[1]
                key=(current,name,ret,args)
                if key in methods and methods[key]!=mapped:
                    raise ValueError("DUPLICATE_TARGET_METHOD_WITH_CONFLICTING_MAPPING")
                methods[key]=mapped
    missing=names-classes.keys()
    if missing:
        raise ValueError("OFFICIAL_OBF_CLASS_MISSING:"+str(sorted(missing)))
    for clazz, specs in TARGETS.items():
        for name,ret,args in specs:
            if (clazz,name,ret,args) not in methods:
                raise ValueError("OFFICIAL_OBF_METHOD_MISSING:"+str((clazz,name,args)))
    return classes,methods

def jvm_type(java:str, classes:dict):
    primitives={"void":"V","boolean":"Z","float":"F","double":"D","int":"I","long":"J","short":"S","byte":"B","char":"C"}
    if java in primitives:
        return primitives[java]
    if java not in classes:
        raise ValueError("UNMAPPED_JVM_REF:"+java)
    return "L"+classes[java].replace(".","/")+";"

def exact_method(javap_out:str,method_name:str,descriptor:str):
    lines=javap_out.splitlines()
    candidates=[]
    for i,line in enumerate(lines[:-1]):
        if not HEADER.match(line) or not re.search(r"\b"+re.escape(method_name)+r"\(",line):
            continue
        if DESC.match(lines[i+1]) and DESC.match(lines[i+1]).group(1)==descriptor:
            end=next((j for j in range(i+2,len(lines)) if HEADER.match(lines[j]) or lines[j]=="}"),len(lines))
            candidates.append(lines[i:end])
    if len(candidates)!=1:
        raise ValueError(f"TARGET_METHOD_DECLARATION_NOT_UNIQUE:{method_name}{descriptor}: {len(candidates)}")
    return candidates[0]

def matched_calls(method:list[str], name:str, descriptor:str, owner_classes:set[str]):
    found=[]
    for line in method:
        x=CALL.match(line)
        if not x: continue
        pc,opcode,owner,calleename,desc=x.group(1),x.group(2),x.group("owner"),x.group("name"),x.group("desc")
        if calleename==name and desc==descriptor and (owner is None or owner.replace("/",".") in owner_classes):
            found.append({"pc":int(pc),"invoke":opcode,"obfuscated_owner":owner or "same_class"})
    return found

def javap_class(jar:Path,clazz:str):
    return subprocess.run(["javap","-p","-c","-s","-classpath",str(jar),clazz],
                          check=True,capture_output=True,text=True).stdout

def inspect_vanilla(jar:Path,mapping:str):
    classes,methods=find_mappings(mapping)
    entity=classes[ENTITY]
    living=classes[LIVING]
    ranged=classes[RANGED]
    classfiles={ENTITY:javap_class(jar,entity),LIVING:javap_class(jar,living),
                RANGED:javap_class(jar,ranged)}
    def named(owner,name,ret,args):
        obf=methods[(owner,name,ret,args)]
        desc="("+ "".join(jvm_type(arg,classes) for arg in args)+")"+jvm_type(ret,classes)
        return obf,desc
    def get(owner,name,ret,args):
        obf,desc=named(owner,name,ret,args)
        return exact_method(classfiles[owner],obf,desc)

    emove=get(ENTITY,"move","void",("net.minecraft.world.entity.MoverType",VEC))
    ltravel=get(LIVING,"travel","void",(VEC,))
    labels=[
        ("Entity.move -> collide",emove,ENTITY,"collide",VEC,(VEC,),{entity}),
        ("Entity.move -> tryCheckInsideBlocks",emove,ENTITY,"tryCheckInsideBlocks","void",(),{entity}),
        ("LivingEntity.travel -> handleRelativeFrictionAndCalculateMovement",ltravel,LIVING,
            "handleRelativeFrictionAndCalculateMovement",VEC,(VEC,"float"),{living}),
        ("LivingEntity.travel -> setDeltaMovement(DDD)",ltravel,ENTITY,"setDeltaMovement",
            "void",("double","double","double"),{entity,living})
    ]
    results=[]
    for key,block,owner,name,ret,args,allowed in labels:
        obf,desc=named(owner,name,ret,args)
        calls=matched_calls(block,obf,desc,allowed)
        results.append({"edge":key,"obfuscated_callee":obf,"callee_descriptor":desc,
                        "callsites":calls,"count":len(calls)})
    bounce=results[-1]
    # A zero-indexed ordinal of 3 needs at least four matching callsites.
    ordinal3_exists=bounce["count"]>=4
    # Verify RangedAttribute constructor is present in vanilla bytecode; no
    # ProGuard constructor mapping assumption is needed.
    range_ctor="(Ljava/lang/String;DDD)V"
    ctor_owner=ranged.rsplit(".",1)[-1]
    constructor=exact_method(classfiles[RANGED],ctor_owner,range_ctor)
    return {
        "status":"PASS_MINECRAFT_1211_VANILLA_CLIENT_CALLSITE_INSPECTION",
        "scope":"official unmodified vanilla CLIENT.jar, not NeoForge patched",
        "method_owner_classes":{k:classes[k] for k in (ENTITY,LIVING,RANGED)},
        "invocation_edges":results,
        "ordinal_3_at_fourth_setDeltaMovement": {
            "vanilla_client_has_fourth_matching_call":ordinal3_exists,
            "count":bounce["count"],
            "fourth_pc":bounce["callsites"][3]["pc"] if ordinal3_exists else None,
            "limit":"vanilla original instruction order ONLY; no NeoForge/Mixin patch or runtime",
        },
        "ranged_attribute_constructor":{
            "descriptor":range_ctor,"vanilla_client_declared":True,
            "line_count":len(constructor)},
        "limitations":[
            "No NeoForge 21.1.250 patched Minecraft target or mixin application.",
            "Client-only vanilla callsite count cannot assert dedicated-server target cardinality.",
            "Mojang mappings remap named methods only; a callsite count cannot prove later compatibility.",
            "No physical user's installed SHA, Slime Boots/Aspect gameplay or perk bridge."
        ],
        "deviations":[]
    }

class Regression(unittest.TestCase):
    def test_identifies_zero_based_fourth_position(self):
        fake=[
            "       "+str(i*5)+": invokevirtual #30  // Method ab.c:(DDD)V" for i in range(4)
        ]
        xs=matched_calls(fake,"c","(DDD)V",{"ab"})
        self.assertEqual([x["pc"] for x in xs],[0,5,10,15])
        self.assertEqual(xs[3]["pc"],15)
    def test_excludes_wrong_descriptor_or_owner(self):
        fake=["  1: invokevirtual #3 // Method ab.c:(DDD)V",
              "  4: invokevirtual #3 // Method xx.c:(DDD)V",
              "  8: invokevirtual #3 // Method ab.c:(FFF)V"]
        self.assertEqual(len(matched_calls(fake,"c","(DDD)V",{"ab"})),1)
    def test_exact_method_rejects_missing(self):
        with self.assertRaisesRegex(ValueError,"TARGET_METHOD_DECLARATION_NOT_UNIQUE"):
            exact_method("class Empty {\n}\n","f","()V")
    def test_exact_method_selects_overload_by_descriptor(self):
        fake="  public void a(int);\n    descriptor: (I)V\n    Code:\n    0: return\n\n  public void a(double);\n    descriptor: (D)V\n    Code:\n    0: return\n}\n"
        self.assertIn("descriptor: (D)V",exact_method(fake,"a","(D)V"))
    def test_jvm_primitive(self):
        self.assertEqual(jvm_type("double",{}),"D")
        self.assertEqual(jvm_type("void",{}),"V")
    def test_missing_reference_mapping(self):
        with self.assertRaisesRegex(ValueError,"UNMAPPED_JVM_REF"):
            jvm_type("net.minecraft.Missing",{})
    def test_missing_class_mapping(self):
        with self.assertRaisesRegex(ValueError,"OFFICIAL_OBF_CLASS_MISSING"):
            find_mappings("")
    def test_client_download_host_is_pinned(self):
        with self.assertRaisesRegex(ValueError,"CLIENT_NOT_FROM_MOJANG"):
            with tempfile.TemporaryDirectory() as d:
                official_client({"client":{"url":"https://example.org/a"}},Path(d)/"x.jar")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    if args.self_test:
        r=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Regression))
        return 0 if r.wasSuccessful() else 1
    if not args.output:p.error("--output required")
    try:
        version=official_version_downloads()
        mappings=version["downloads"]["client_mappings"]
        mapping_bytes=official_get(mappings["url"],15000000)
        if hashlib.sha1(mapping_bytes).hexdigest()!=mappings["sha1"]:
            raise ValueError("OFFICIAL_CLIENT_MAPPING_SHA1_MISMATCH")
        with tempfile.TemporaryDirectory() as d:
            jar=Path(d)/"minecraft-1.21.1-vanilla-client.jar"
            sha=official_client(version["downloads"],jar)
            report=inspect_vanilla(jar,mapping_bytes.decode("utf-8"))
            report["publisher"]=sha
            report["minecraft_version"]=MC_VERSION
            report["client_mapping_sha1"]=mappings["sha1"]
            report["version_json_sha1"]=version["json_sha1"]
    except (OSError,ValueError,KeyError,subprocess.CalledProcessError,zipfile.BadZipFile,UnicodeError) as e:
        report={"status":"FAIL_CLOSED","deviations":[str(e)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"deviations":report["deviations"],
                      "edges":[(x["edge"],x["count"]) for x in report.get("invocation_edges",[])],
                      "ordinal_3":report.get("ordinal_3_at_fourth_setDeltaMovement",{})}))
    return 0 if report["status"]=="PASS_MINECRAFT_1211_VANILLA_CLIENT_CALLSITE_INSPECTION" else 2

if __name__=="__main__":
    sys.exit(main())
