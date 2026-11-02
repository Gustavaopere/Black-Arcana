#!/usr/bin/env python3
"""Bounded clean-room metadata and callsite census of FTB Chunks 2101.1.22.

Static binary references and declared mixins are NOT evidence of runtime
injection, claim enforcement, or dispatch of an explosion protection hook.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tomllib
import zipfile
from pathlib import Path

from neoforge_211248_grief_event_probe import EvidenceError, parse_methods, require

JAR_NAME = "ftb-chunks-neoforge-2101.1.22.jar"
JAR_SHA256 = "4ba1b3352184fa7f6e2aa4bca76edd074867697d62344dfa50dcccdb4dab5217"
CONFIG = "ftbchunks-common.mixins.json"
TOML = "META-INF/neoforge.mods.toml"
OWNER = "dev/ftb/mods/ftbchunks/FTBChunks.class"
TARGET_METHOD = "explosionDetonate"
TARGET_DESCRIPTOR = "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/level/Explosion;Ljava/util/List;)V"
LIMITS = {
    "metadata_registration":"DECLARATIVE_ONLY",
    "runtime_mixin_application":"NOT_OBSERVED",
    "external_mod_event_registration":"NOT_VERIFIED",
    "native_explosion_dispatch":"NOT_VERIFIED",
    "claim_per_affected_block":"NOT_CERTIFIED",
    "tremorzilla_level_destroy_block":"NOT_VERIFIED",
    "tremorzilla_blockstate_on_block_exploded":"NOT_VERIFIED",
    "black_arcana_world_effect_policy":"NOT_VERIFIED",
    "loaded_modpack_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "perk_certification":"NOT_CERTIFIED"
}
MARKERS = (b"Explosion",b"explosionDetonate",b"getToBlow",
           b"destroyBlock",b"onBlockExploded",b"LevelEvent",
           b"BlockState",b"Inject",b"Redirect",b"Modify")

def hash_(data):
    return hashlib.sha256(data).hexdigest()

def analyze_manifest(config_bytes,toml_bytes):
    require(len(config_bytes)<18000 and len(toml_bytes)<18000,"metadata budget exceeded")
    try:
        obj=json.loads(config_bytes)
        meta=tomllib.loads(toml_bytes.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise EvidenceError("invalid publisher metadata: "+str(exc)[:100]) from exc
    require(isinstance(obj,dict),"mixin metadata must be object")
    pkg=obj.get("package")
    require(isinstance(pkg,str) and
            re.fullmatch(r"[a-zA-Z_][\w]*(?:\.[a-zA-Z_][\w]*){3,12}",pkg),
            "invalid mixin package")
    groups={}
    for key in ("mixins","client","server"):
        entries=obj.get(key,[])
        require(isinstance(entries,list) and len(entries)<=80,"invalid mixin group")
        require(all(isinstance(e,str) and
                    re.fullmatch(r"[\w$]+(?:\.[\w$]+){0,8}",e)
                    for e in entries),"invalid mixin entry")
        require(len(set(entries))==len(entries),"duplicate mixin entry in group")
        groups[key]=entries
    flat=[(grp,entry) for grp,arr in groups.items() for entry in arr]
    require(len(flat)<=120,"combined mixin population too large")
    mixin_refs=meta.get("mixins",[])
    if isinstance(mixin_refs,dict):
        mixin_refs=[mixin_refs]
    require(isinstance(mixin_refs,list) and len(mixin_refs)<=20,"invalid neoforge mixin refs")
    configs=[x.get("config") for x in mixin_refs if isinstance(x,dict)]
    require(CONFIG in configs,"NeoForge metadata does not register selected mixin config")
    mod_entries=meta.get("mods",[])
    require(isinstance(mod_entries,list) and
            any(isinstance(x,dict) and x.get("modId")=="ftbchunks" for x in mod_entries),
            "FTB Chunks mod ID missing")
    return {"config_sha256":hash_(config_bytes),
            "neoforge_metadata_sha256":hash_(toml_bytes),
            "mixin_package":pkg,"declared_mixin_groups":groups,
            "declared_mixin_population":len(flat),
            "neo_registered_mixins":configs,
            "java_compatibility_level":obj.get("compatibilityLevel"),
            "injector_default_require":obj.get("injectors",{}).get("defaultRequire")}

def extract_jar(jar,javap):
    file=Path(jar)
    require(file.name==JAR_NAME,"wrong exact publisher artifact filename")
    require(file.is_file() and 10000<file.stat().st_size<5_000_000,"missing/oversized publisher JAR")
    raw=file.read_bytes()
    require(hash_(raw)==JAR_SHA256,"publisher JAR SHA-256 drift")
    require(zipfile.is_zipfile(file),"publisher archive invalid")
    with zipfile.ZipFile(file) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate ZIP members")
        require(CONFIG in names and TOML in names and OWNER in names,
                "missing required metadata or exact method owner")
        metadata=analyze_manifest(z.read(CONFIG),z.read(TOML))
        classes=[p for p in names if p.endswith(".class")]
        require(0<len(classes)<5000,"unbounded publisher class census")
        mixins=[]
        for group,entries in metadata["declared_mixin_groups"].items():
            for name in entries:
                path=metadata["mixin_package"].replace(".","/")+"/"+name.replace(".","/")+".class"
                require(path in names,"declared mixin class absent: "+path)
                content=z.read(path)
                mixins.append({
                    "group":group,"name":name,"class_path":path,
                    "class_sha256":hash_(content),
                    "raw_constant_pool_string_presence":{
                        x.decode("ascii"):x in content for x in MARKERS
                    }})
        refs=[p for p in classes if TARGET_METHOD.encode("ascii") in z.read(p)]
        require(len(refs)<=30,"bounded cross-class method-name refs exceeded")
        candidates=[(p,hash_(z.read(p))) for p in sorted(refs)]
    references=[]
    owners=[]
    for path,digest in candidates:
        fqcn=path[:-6].replace("/",".")
        p=subprocess.run([javap,"-classpath",str(file),"-p","-s","-c",fqcn],
                         capture_output=True,text=True,timeout=45,check=False)
        require(p.returncode==0,"javap failed: "+path+" "+p.stderr[:160])
        methods=parse_methods(p.stdout)
        declared=[m for m in methods if m["name"]==TARGET_METHOD]
        if declared:
            require(len(declared)<=2,"ambiguous target declarations")
            owners.append({
                "class_path":path,"class_sha256":digest,
                "target_method_descriptors":[m["descriptor"] for m in declared]
            })
        for m in methods:
            for i in m["instructions"]:
                if i["opcode"].startswith("invoke") and
                   TARGET_METHOD+":" in i["symbol"]:
                    references.append({"owner_class":path,"owner_class_sha256":digest,
                         "method_name":m["name"],"method_descriptor":m["descriptor"],
                         "offset":i["offset"],"opcode":i["opcode"],"symbol":i["symbol"]})
        require(len(references)<=35,"too many direct JVM method references")
    require(any(x["class_path"]==OWNER and TARGET_DESCRIPTOR in x["target_method_descriptors"]
                for x in owners),"exact previously observed method owner/descriptor drift")
    result={
        "schema_version":1,"scope":"FTB_CHUNKS_2101_1_22_DECLARED_MIXINS_AND_EXPLOSION_CALLSITE_CENSUS",
        "artifact":{"coordinates":"dev.ftb.mods:ftb-chunks-neoforge:2101.1.22",
                    "size_bytes":len(raw),"sha256":hash_(raw)},
        "metadata":metadata,
        "class_population":len(classes),
        "mixins":mixins,
        "compiled_method_name_reference_class_population":len(candidates),
        "compiled_method_declarations":owners,
        "direct_jvm_invocation_sites":references,
        "direct_jvm_invocation_site_count":len(references),
        "interpretation":"DECLARED_MIXINS_AND_STATIC_JVM_REFS_ONLY_NOT_EFFECTIVE_DISPATCH",
        "limits":LIMITS
    }
    require(len(json.dumps(result).encode("utf-8"))<30_000,"report budget exceeded")
    return result

def verify_seal(report,seal):
    require(seal.get("scope")==report.get("scope"),"unrecognized evidence scope")
    require(seal.get("limits")==LIMITS,"unsafe safety limit change")
    require(report==seal,"SHA-exact JAR metadata/callsite seal drift")
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--output",required=True)
    ap.add_argument("--seal")
    a=ap.parse_args()
    try:
        report=extract_jar(a.jar,a.javap)
        if a.seal:
            verify_seal(report,json.loads(Path(a.seal).read_text(encoding="utf-8")))
        path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print("PASS: FTB Chunks exact mixin metadata/callsite census sha256="+
              report["artifact"]["sha256"])
        print("mixin_classes="+str(len(report["mixins"]))+
              "; direct_jvm_invocations="+str(report["direct_jvm_invocation_site_count"]))
        print("NO_MUTATION / NOT_CERTIFIED / transformed-game claims not verified")
    except (EvidenceError,ValueError,OSError,KeyError,TypeError,subprocess.TimeoutExpired) as e:
        ap.exit(1,"FAIL-CLOSED: "+str(e)+"\n")

if __name__=="__main__":
    main()
