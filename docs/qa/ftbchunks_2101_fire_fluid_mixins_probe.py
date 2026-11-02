#!/usr/bin/env python3
"""Read-only exact-release mixin annotation inventory: fire and flowing fluids.

Uses the independently-tested classfile metadata parser from PR #1013.
It deliberately does NOT infer that an injection is applied at runtime, that
a claim is authorized, or that the Tremorzilla beam takes these code paths.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from ftbchunks_2101_blockstate_mixin_probe import (
    AuditError, Classfile, digest, require,
    JAR_NAME, JAR_SHA256, CONFIG, CONFIG_SHA256,
)

SOURCE = "dev.ftb.mods.ftbchunks.core.mixin"
CLASSES = {
    "FireBlockMixin": {
        "path":"dev/ftb/mods/ftbchunks/core/mixin/FireBlockMixin.class",
        "sha256":"670463ce84b03d26852ba333370f15f0edf69eae89d8a89d504167b14caa41e2",
    },
    "FlowingFluidMixin": {
        "path":"dev/ftb/mods/ftbchunks/core/mixin/FlowingFluidMixin.class",
        "sha256":"24ffbe40205ff6db02093f18cdc96bb23c54e80e9afd29e769c8067b0a85d971",
    },
}
SCOPE="EXACT_FTBCHUNKS_2101_1_22_FIRE_AND_FLOWING_FLUID_MIXIN_ANNOTATIONS"
SAFETY={
    "registered_mixin_configuration":"STATIC_DECLARATION_ONLY",
    "runtime_mixin_application":"NOT_OBSERVED",
    "effective_injection_behavior":"NOT_VERIFIED",
    "claims_per_affected_block":"NOT_CERTIFIED",
    "tremorzilla_direct_block_mutation":"NOT_VERIFIED",
    "explosion_world_events":"NOT_VERIFIED",
    "black_arcana_world_effect_policy":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutating_hook":"NOT_VERIFIED",
    "mutation":"NO_MUTATION",
    "perk_certification":"NOT_CERTIFIED",
}
ALLOWED_ANNOTATIONS={
    "Lorg/spongepowered/asm/mixin/Mixin;",
    "Lorg/spongepowered/asm/mixin/injection/Inject;",
    "Lorg/spongepowered/asm/mixin/injection/Redirect;",
    "Lorg/spongepowered/asm/mixin/injection/ModifyArg;",
    "Lorg/spongepowered/asm/mixin/injection/ModifyVariable;",
    "Lorg/spongepowered/asm/mixin/injection/ModifyConstant;",
    "Lorg/spongepowered/asm/mixin/Overwrite;",
    "Lorg/spongepowered/asm/mixin/Shadow;",
    "Lorg/spongepowered/asm/mixin/Unique;",
    "Lorg/spongepowered/asm/mixin/Final;",
}
MAX_BYTES=24000

def report_mixins(class_by_name):
    require(set(class_by_name)==set(CLASSES),"incorrect mixin class universe")
    result=[]
    for name in ("FireBlockMixin","FlowingFluidMixin"):
        data=class_by_name[name]
        require(digest(data)==CLASSES[name]["sha256"],"mixin class checksum drift: "+name)
        metadata=Classfile(data).summary()
        require(metadata["method_count"] <= 35,"unexpected method population "+name)
        class_types=[x["annotation"]["type"] for x in metadata["class_annotations"]]
        require("Lorg/spongepowered/asm/mixin/Mixin;" in class_types,
                "missing declared @Mixin class annotation: "+name)
        methods=[]
        for m in metadata["methods"]:
            anns=m["annotations"]
            methods.append({
                "name":m["name"],"descriptor":m["descriptor"],
                "access_flags":m["access_flags"],
                "bytecode":m["code"],
                "annotations":anns,
                "recognized_transform_annotation_types":[
                    x["annotation"]["type"] for x in anns
                    if x["annotation"]["type"] in ALLOWED_ANNOTATIONS
                    and x["annotation"]["type"] not in (
                        "Lorg/spongepowered/asm/mixin/Unique;",
                        "Lorg/spongepowered/asm/mixin/Shadow;",
                    )],
            })
        result.append({
            "name":name,"class_path":CLASSES[name]["path"],
            "class_sha256":CLASSES[name]["sha256"],
            "jvm_class_major_version":metadata["jvm_class_major_version"],
            "class_annotations":metadata["class_annotations"],
            "annotation_types":metadata["annotation_types"],
            "declared_methods":methods,
            "method_count":metadata["method_count"],
            "field_count":metadata["field_count"],
            "method_annotation_count":sum(len(x["annotations"]) for x in methods),
            "interpretation":"ANNOTATION_TARGETS_ONLY_NO_EFFECTIVE_HOOK_OR_PER_BLOCK_AUTHORITY",
        })
    return result

def analyze_jar(jar):
    p=Path(jar)
    require(p.name==JAR_NAME,"wrong FTB Chunks 2101.1.22 JAR filename")
    require(p.is_file() and 10000<p.stat().st_size<5_000_000,
            "missing or oversized publisher artifact")
    raw=p.read_bytes()
    require(digest(raw)==JAR_SHA256,"publisher exact artifact SHA-256 drift")
    require(zipfile.is_zipfile(p),"invalid JAR archive")
    with zipfile.ZipFile(p) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate JAR archive entry")
        require(CONFIG in names,"missing registered mixin configuration")
        b=z.read(CONFIG)
        require(digest(b)==CONFIG_SHA256,"registered mixin JSON SHA-256 drift")
        config=json.loads(b)
        require(config.get("package")==SOURCE,
                "mixin metadata package unexpectedly changed")
        mixins=config.get("mixins")
        require(isinstance(mixins,list),"invalid common mixin declarations")
        for name in CLASSES:
            require(mixins.count(name)==1,"missing or duplicate declared mixin "+name)
        for entry in CLASSES.values():
            require(entry["path"] in names,"missing exact publisher mixin class")
        class_by_name={n:z.read(x["path"]) for n,x in CLASSES.items()}
    out={
        "schema_version":1,"scope":SCOPE,
        "artifact":{"coordinates":"dev.ftb.mods:ftb-chunks-neoforge:2101.1.22",
                    "sha256":JAR_SHA256,"size_bytes":len(raw)},
        "config":{"path":CONFIG,"sha256":CONFIG_SHA256,
                  "package":SOURCE,"two_mixins_declared":True},
        "mixins":report_mixins(class_by_name),
        "limits":SAFETY,
        "interpretation":"STATIC_CLASSFILE_ANNOTATIONS_NOT_RUNTIME_MODPACK_CLAIM_ENFORCEMENT",
    }
    require(len(json.dumps(out,ensure_ascii=False).encode("utf-8"))<MAX_BYTES,
            "bounded evidence output budget exceeded")
    return out

def verify_seal(observed,manifest):
    require(manifest.get("scope")==SCOPE,"wrong manifest scope")
    require(manifest.get("limits")==SAFETY,"unsafe or incorrect safety limits")
    require(observed==manifest,"exact fire/fluid annotation ABI evidence drift")
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--seal")
    args=ap.parse_args()
    try:
        report=analyze_jar(args.jar)
        if args.seal:
            verify_seal(report,json.loads(Path(args.seal).read_text(encoding="utf-8")))
        dest=Path(args.output)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",
                        encoding="utf-8")
        print("PASS: exact FTB Chunks 2101.1.22 fire/fluid mixin annotations")
        for m in report["mixins"]:
            print(m["name"]+": methods="+str(m["method_count"])+
                  " annotated="+str(m["method_annotation_count"])+
                  " types="+repr(m["annotation_types"]))
        print("NOT_CERTIFIED / NO_MUTATION / no physical claim QA")
    except (AuditError,ValueError,KeyError,OSError,TypeError,UnicodeDecodeError) as e:
        ap.exit(1,"FAIL-CLOSED: "+str(e)+"\n")

if __name__=="__main__":
    main()
