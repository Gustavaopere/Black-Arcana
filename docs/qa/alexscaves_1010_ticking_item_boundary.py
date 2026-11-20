#!/usr/bin/env python3
"""Read-only annotation, engine dispatch and callback boundary audit."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import zipfile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact
from alexscaves_1010_destroyed_item_engine_reference import verify_artifact as verify_engine, ARTIFACTS
import alexscaves_1010_repairable_item_boundary as reference
from alexscaves_1010_ticking_item_probe import inspect

MIXIN = "com/github/alexmodguy/alexscaves/mixin/ItemStackTickMixin"
TARGETS = {
    "net.minecraft.world.item.ItemStack": {"inventoryTick"},
    "net.minecraft.world.item.Item": {"inventoryTick"},
    "net.minecraft.world.entity.player.Inventory": {"tick"},
    "net.minecraft.world.entity.player.Player": {"tick"},
}

def annotation(jar, javap):
    verify_artifact(jar)
    result = subprocess.run([str(javap), "-v", "-p", "-classpath", str(jar), MIXIN.replace("/", ".")],
                            check=True, text=True, capture_output=True).stdout
    # Parse only rendered annotation sections; no raw source or full javap copy.
    lines = result.splitlines()
    records = []
    for i, line in enumerate(lines):
        if re.fullmatch(r"\s*Runtime(?:Visible|Invisible)Annotations:", line):
            out = []
            for row in lines[i+1:]:
                if not row.strip() or row.strip() == "}" or re.match(r"\s*(?:Runtime\w+Annotations|SourceFile|InnerClasses|BootstrapMethods|descriptor|flags):", row):
                    break
                if not re.match(r"\s", row):
                    break
                out.append(row.strip())
            records.append({"section": line.strip(), "entries": out})
    require(records, "no annotation evidence")
    flattened = "\n".join(r for record in records for r in record["entries"])
    require("org.spongepowered.asm.mixin.Mixin" in flattened and "org.spongepowered.asm.mixin.injection.Inject" in flattened, "missing mixin/inject")
    with zipfile.ZipFile(jar) as z:
        raw = z.read(MIXIN+".class")
        conf = json.loads(z.read("alexscaves.mixins.json"))
        metadata = {}
        for p in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml", "META-INF/MANIFEST.MF"):
            if p in z.namelist():
                raw_meta = z.read(p)
                lines_meta = raw_meta.decode("utf8").splitlines()
                hits = {i for i,line in enumerate(lines_meta) if re.search(r"mixin",line,re.I)}
                selected = {j for i in hits for j in range(max(0,i-1),min(len(lines_meta),i+3))}
                metadata[p] = {"sha256": digest(raw_meta), "mixin_lines": [{"line":i+1,"text":lines_meta[i]} for i in sorted(selected)]}
    return {"class_sha256":digest(raw), "annotations":records, "config":{k:conf.get(k) for k in ("required","minVersion","compatibilityLevel","injectors","refmap","package")}, "loader_metadata":metadata}

def neo(universal,userdev):
    verify_engine(universal,"universal")
    verify_engine(userdev,"userdev")
    patches={}
    pattern=re.compile(r"inventoryTick|tick\(|getSelected|selected|armor|equipment",re.I)
    with zipfile.ZipFile(userdev) as z:
        for owner in ("world/item/ItemStack.java","world/item/Item.java","world/entity/player/Inventory.java","world/entity/player/Player.java","world/entity/LivingEntity.java"):
            p="patches/net/minecraft/"+owner+".patch"
            if p not in z.namelist():
                patches[p]={"present":False}
                continue
            raw=z.read(p)
            lines=raw.decode("utf8").splitlines()
            hits={i for i,l in enumerate(lines) if pattern.search(l) and re.search(r"inventoryTick|\.tick\(|getSelected",l)}
            selected={j for i in hits for j in range(max(0,i-3),min(len(lines),i+4))}
            patches[p]={"present":True,"sha256":digest(raw),"selected":[{"line":i+1,"text":lines[i]} for i in sorted(selected)]}
    return {"artifacts":ARTIFACTS,"patches":patches}

def profiles(jar,javap):
    native=inspect(jar,javap)
    result={}
    for owner in native["direct_implementers"]:
        m=next(x for x in native["owners"][owner]["methods"] if x["declaration"]["name"]=="acInventoryTick")
        # Index all branch destinations, constants and resolved calls for manual causal review.
        rows=m["instructions"]
        result[owner]={"descriptor":m["declaration"]["descriptor"],"code_sha256":m["declaration"]["code_sha256"],
                       "instruction_sha256":m["instruction_sha256"],"instruction_count":m["instruction_count"],
                       "branches":[r for r in rows if r["opcode"].startswith("if") or r["opcode"] in ("goto","tableswitch","lookupswitch")],
                       "constants":[r for r in rows if r["opcode"].startswith(("ldc","iconst","fconst","dconst","lconst")) or r["opcode"] in ("bipush","sipush")],
                       "calls":[r for r in rows if r["opcode"].startswith("invoke")],
                       "fields":[r for r in rows if r["opcode"] in ("getfield","putfield","getstatic","putstatic")],
                       "returns":[r["offset"] for r in rows if r["opcode"]=="return"]}
    require(len(result)==17,"callback roster drift")
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ("jar","javap","universal","userdev","output"):
        p.add_argument("--"+n,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists(),"new output required")
    tmp=a.output.parent/"tick-reference"
    tmp.mkdir()
    reference.TARGETS=TARGETS
    report={"scope":"STATIC_REFERENCE_ONLY","native_annotation":annotation(a.jar,a.javap),
            "profiles":profiles(a.jar,a.javap),"vanilla":reference.vanilla(tmp,a.javap),
            "neoforge":neo(a.universal,a.userdev),"mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED"}
    a.output.write_text(canonical(report),encoding="utf8")
    print("BOUNDARY_SHA256",digest(a.output.read_bytes()))
    print("MIXIN_ANNOTATION",json.dumps(report["native_annotation"],sort_keys=True))
    for owner,data in report["profiles"].items():
        print("CALLBACK_PROFILE",owner,json.dumps(data,sort_keys=True))
    for owner,data in report["vanilla"]["classes"].items():
        print("VANILLA_OWNER",owner,data["obfuscated_owner"],data["class_sha256"],data["parent"])
        for m in data["methods"]:
            print("VANILLA_METHOD",owner,json.dumps(m,sort_keys=True))
    for path,data in report["neoforge"]["patches"].items():
        print("NEO_PATCH",path,json.dumps(data,sort_keys=True))

if __name__=="__main__":
    main()
