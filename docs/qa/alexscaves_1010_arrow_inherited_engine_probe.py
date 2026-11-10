#!/usr/bin/env python3
"""Read-only search of Gradle-resolved 1.21.1 engine bytecode for Arrow Inducting.

Only class fingerprints, method signatures, direct symbolic callsites, branch
targets and constants are reported. This does not copy Minecraft implementation
or certify the actual ModLauncher-transformed runtime, accepted damage or QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, sha_file, javap, parse_methods
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

CLASSES = {
    "abstract_arrow": "net/minecraft/world/entity/projectile/AbstractArrow.class",
    "projectile": "net/minecraft/world/entity/projectile/Projectile.class",
}
RELEVANT = {
    "abstract_arrow": {
        "AbstractArrow", "onHitEntity", "onHitBlock", "doPostHurtEffects",
        "canHitEntity", "addAdditionalSaveData", "readAdditionalSaveData",
        "getBaseDamage", "setBaseDamage", "getPickupItem", "tick"
    },
    "projectile": {
        "Projectile", "setOwner", "getOwner", "getOwnerUUID", "onHit",
        "onHitEntity", "onHitBlock", "canHitEntity",
        "addAdditionalSaveData", "readAdditionalSaveData", "tick"
    },
}
REF_KEYS = tuple(token.lower() for token in (
    "damage", "hurt", "owner", "hit", "arrow", "projectile", "save",
    "load", "getEntity", "discard", "setBaseDamage", "getBaseDamage",
    "isClientSide", "getData", "enchantment", "getPickupItem"
))
MAX_VISITED = 20000
MAX_CANDIDATES = 16
MAX_METHODS = 60
MAX_INS = 2500
MAX_REF_ROWS = 150

def require(value, message):
    if not value:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def pin_build_files(root: Path):
    props = {}
    for line in (root / "gradle.properties").read_text(encoding="utf8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k,v=line.split("=",1)
            props[k.strip()]=v.strip()
    require(props.get("minecraft_version")=="1.21.1", "minecraft version drift")
    require(props.get("neo_version")=="21.1.248", "NeoForge version drift")
    gradle=(root/"build.gradle").read_text(encoding="utf8")
    require("id 'net.neoforged.moddev' version '2.0.144'" in gradle,
            "ModDevGradle pin drift")
    return {"minecraft":props["minecraft_version"],
            "neoforge":props["neo_version"],"moddevgradle":"2.0.144"}

def roots(root: Path):
    values=[Path.home()/".gradle"/"caches",root/".gradle"]
    return [p for p in values if p.exists() and p.is_dir()]

def find_candidates(root: Path):
    found=[]
    scanned=0
    for top in roots(root):
        for directory,subs,files in os.walk(top, followlinks=False):
            subs[:]=[s for s in subs if s not in {"tmp","transforms","daemon","kotlin-dsl"}]
            for f in files:
                if not f.lower().endswith(".jar"):
                    continue
                scanned+=1
                require(scanned<=MAX_VISITED,"JAR discovery exceeded bounded budget")
                path=Path(directory)/f
                try:
                    with zipfile.ZipFile(path) as z:
                        if not all(n in z.NameToInfo for n in CLASSES.values()):
                            continue
                        bytes_by_class={k:z.read(n) for k,n in CLASSES.items()}
                    found.append({"path":path,
                        "class_digests":{k:digest(raw) for k,raw in bytes_by_class.items()}})
                    require(len(found)<=MAX_CANDIDATES,
                            "too many engine class candidates; exact origin ambiguous")
                except (OSError, zipfile.BadZipFile, PermissionError):
                    continue
    return found,scanned

def unique_candidates(candidates):
    grouped={}
    for obj in candidates:
        identity=tuple(sorted(obj["class_digests"].items()))
        grouped.setdefault(identity,[]).append(obj)
    return [group[0] for _,group in sorted(
        grouped.items(),key=lambda x:tuple(x[0]))]

def select_from_compile_classpath(candidates, classpath_file: Path):
    require(classpath_file.is_file(), "Gradle compileClasspath export missing")
    raw_paths=[line.strip() for line in
               classpath_file.read_text(encoding="utf8").splitlines() if line.strip()]
    require(raw_paths and len(raw_paths)<4000, "invalid compileClasspath export")
    resolved={Path(line).resolve() for line in raw_paths}
    for obj in candidates:
        is_compiler_input=obj["path"].resolve() in resolved
        print("ENGINE_CANDIDATE",str(obj["path"]),
              "compile_classpath",is_compiler_input,
              "abstract_arrow_sha256",obj["class_digests"]["abstract_arrow"],
              "projectile_sha256",obj["class_digests"]["projectile"])
    selected=[obj for obj in candidates if obj["path"].resolve() in resolved]
    require(selected, "no Minecraft engine class artifact on effective compileClasspath")
    unique=unique_candidates(selected)
    require(len(unique)==1,
            "multiple distinct Minecraft bytecodes on effective compileClasspath")
    return unique[0]

def method_evidence(method):
    ins=method["instructions"]
    require(len(ins)<=MAX_INS,"oversized Minecraft method; no partial promotion")
    offsets=[x["offset"] for x in ins]
    require(offsets==sorted(set(offsets)),"duplicate/unsorted JVM offsets")
    allrefs=[x for x in ins if x["opcode"].startswith("invoke") or
             x["opcode"] in ("getfield","putfield","getstatic","putstatic")]
    direct=[{"offset":r["offset"],"opcode":r["opcode"],"symbol":r["symbol"]}
            for r in allrefs if any(t in r["symbol"].lower() for t in REF_KEYS)]
    require(len(direct)<=MAX_REF_ROWS,"too many relevant callsites")
    branches=[{"offset":r["offset"],"opcode":r["opcode"],"target":r["operand"]}
              for r in ins if r["opcode"].startswith("if") or
              r["opcode"] in ("goto","goto_w")]
    constants=[{"offset":r["offset"],"opcode":r["opcode"],"operand":r["operand"],
                "symbol":r["symbol"]} for r in ins if
               r["opcode"].startswith(("iconst_","fconst_","dconst_","lconst_"))
               or r["opcode"] in ("ldc","ldc2_w","ldc_w","bipush","sipush")]
    return {"name":name_of(method),"descriptor":method["descriptor"],
            "method_sha256":digest_method(method),
            "instruction_count":len(ins),
            "total_symbolic_refs":len(allrefs),
            "relevant_symbolic_refs":direct,
            "branches":branches[:180],
            "branch_count":len(branches),
            "numeric_operands":constants[:120],
            "numeric_operand_count":len(constants)}

def inspect(jar: Path, javap_bin: str, pins):
    names={}
    with zipfile.ZipFile(jar) as z:
        for key, member in CLASSES.items():
            raw=z.read(member)
            dotted=member[:-6].replace("/",".")
            methods=parse_methods(javap(javap_bin, jar, dotted))
            require(1<=len(methods)<=MAX_METHODS,"unexpected Minecraft method roster")
            selected=[m for m in methods if name_of(m) in RELEVANT[key]]
            require(selected,"no relevant inherited Minecraft methods")
            names[key]={"class_sha256":digest(raw),
                        "class_bytes":len(raw),
                        "declared_method_count":len(methods),
                        "inspected_methods":[method_evidence(m) for m in selected]}
    return {"engine_archive_sha256":digest(jar.read_bytes()),
            "engine_archive_size":jar.stat().st_size,
            "classes":names,"pins":pins}

def audit(provider: Path, project_root: Path, javap_bin: str, classpath_file: Path):
    require(sha_file(provider)==(SHA1,SHA256,SIZE),
            "wrong SHA-exact Alex's Caves 1.0.10 JAR")
    pins=pin_build_files(project_root)
    candidates,scanned=find_candidates(project_root)
    require(candidates,"no mapped Minecraft engine class artifact in Gradle caches")
    chosen=select_from_compile_classpath(candidates,classpath_file)
    data=inspect(chosen["path"],javap_bin,pins)
    require(all(data["classes"][k]["class_sha256"]==chosen["class_digests"][k]
                for k in CLASSES),"engine class digest mismatch")
    return {"schema_version":1,
            "scope":"ALEXSCAVES_1010_SEEKING_ARROW_INHERITED_ENGINE_STATIC_DISCOVERY",
            "provider_sha256":SHA256,
            "platform_pins":pins,
            "engine":data,
            "provenance":{
                "engine_archive_origin":"PINNED_GRADLE_COMPILE_CLASSPATH_NOT_MODLAUNCHER_RUNTIME",
                "compile_classpath_selection":"UNIQUE_CLASS_BYTECODE_SET",
                "cache_scan_budget":MAX_VISITED
            },
            "limits":{
                "direct_engine_bytecode":"FOUND_IN_GRADLE_CACHE",
                "modlauncher_transformed_runtime":"NOT_VERIFIED",
                "on_hit_damage_settlement":"NOT_CERTIFIED",
                "player_attribution_and_mastery":"NOT_VERIFIED",
                "actual_datapacks_and_mixins":"NOT_VERIFIED",
                "physical_qa":"NOT_TESTED",
                "mutating_hook":"NOT_VERIFIED",
                "perk_certification":"NOT_CERTIFIED",
                "mutation":"NO_MUTATION"
            }}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--provider",required=True,type=Path)
    p.add_argument("--classpath-file",required=True,type=Path)
    p.add_argument("--project",type=Path,default=Path("."))
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path)
    p.add_argument("--seal",type=Path)
    p.add_argument("--print-summary",action="store_true")
    args=p.parse_args()
    data=audit(args.provider,args.project,args.javap,args.classpath_file)
    if args.seal:
        expected=json.loads(args.seal.read_text(encoding="utf8"))
        require(data==expected,"inherited-engine manifest drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",
                               encoding="utf8")
    if args.print_summary:
        print("ENGINE_DISCOVERY_JSON="+json.dumps(data,separators=(",",":"),ensure_ascii=False))
    for key,v in data["engine"]["classes"].items():
        print("ENGINE_CLASS",key,v["class_sha256"],v["declared_method_count"])
        for m in v["inspected_methods"]:
            print("ENGINE_METHOD",key,m["name"],m["descriptor"],
                  m["instruction_count"],m["method_sha256"])
            if m["name"] in ("onHitEntity","doPostHurtEffects","setOwner",
                             "getOwner","addAdditionalSaveData","readAdditionalSaveData"):
                for r in m["relevant_symbolic_refs"]:
                    print("ENGINE_CALL",key,m["name"],r["offset"],r["symbol"])
    print("ENGINE_STATUS", "SEALED" if args.seal else "UNSEALED_DISCOVERY",
          "NOT_RUNTIME_PROOF","NO_MUTATION")

if __name__=="__main__":
    main()
