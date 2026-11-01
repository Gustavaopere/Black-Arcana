#!/usr/bin/env python3
"""Exact NeoForge 21.1.248 distributed DataComponentPatch.STREAM_CODEC ABI.

Clean-room, selected symbolic JVM data only. Do NOT infer limits, C2S
authorization, final ModLauncher class transformations or physical QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import parse_methods
from alexscaves_1010_raygun_receiver_probe import method_name
from alexscaves_1010_raygun_receiver_identity_probe import digest_method
from minecraft_1211_itemstack_optional_stream_probe import MojangBoundaryError, parse_initializer
from neoforge_211248_itemstack_server_codec_probe import (
    PINNED_SERVER_JAR_SHA256, sha256_file
)

CLASS = "net/minecraft/core/component/DataComponentPatch.class"
OWNER = CLASS[:-6].replace("/", ".")
EXPECTED_JAR_SIZE = 5675624
MAX_CLASS_BYTES = 450000
MAX_JAVAP_BYTES = 2600000
MAX_CLASS_METHODS = 130
MAX_METHOD_INSNS = 1800
MAX_RELEVANT_METHODS = 24
MAX_SELECTED_REFS = 95
MAX_BRANCHES = 80
MAX_REPORT_BYTES = 85000

CUES = ("STREAM_CODEC", "ByteBufCodecs", "DataComponentPatch",
        "DataComponentType", "StreamCodec", "DataComponentMap", "readVarInt",
        "writeVarInt", "RegistryFriendlyByteBuf", "customData", "NbtOps",
        "UnboundedMapCodec", "DataResult", "DataComponentPatch$",
        "Codec", "readNbt", "writeNbt")

class ComponentPatchProbeError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise ComponentPatchProbeError(message)


def selected_method(m):
    ins = m["instructions"]
    require(len(ins) <= MAX_METHOD_INSNS, "component patch method instruction budget exceeded")
    require(len({i["offset"] for i in ins}) == len(ins), "duplicate JVM offsets")
    refs = [dict(offset=i["offset"], opcode=i["opcode"],
                 symbol=i["symbol"][:340])
            for i in ins if i["opcode"].startswith("invoke") or
            i["opcode"] in ("getstatic", "putstatic", "getfield", "putfield",
                            "new", "checkcast", "instanceof", "ldc", "ldc_w",
                            "bipush", "sipush")]
    branches = [dict(offset=i["offset"], opcode=i["opcode"],
                     operand=i["operand"][:38])
                for i in ins if i["opcode"].startswith(("if", "goto"))]
    require(len(refs) <= MAX_SELECTED_REFS, "component method reference budget exceeded")
    require(len(branches) <= MAX_BRANCHES, "component method branch budget exceeded")
    return {"name":method_name(m), "descriptor":m["descriptor"],
            "method_sha256":digest_method(m), "instruction_count":len(ins),
            "selected_refs":refs, "conditional_branches":branches}


def audit(jar, javap_bin, upstream):
    require(upstream["scope"] ==
            "OFFICIAL_NEOFORGE_211248_INSTALLED_SERVER_CLASSFILE_NOT_LOADED_RUNTIME"
            and upstream["neoforge_version"] == "21.1.248"
            and upstream["limits"]["mutation"] == "NO_MUTATION",
            "prior NeoForge server distribution authority drift")
    sha, size = sha256_file(jar)
    require(sha == PINNED_SERVER_JAR_SHA256 and size == EXPECTED_JAR_SIZE,
            "NeoForge 21.1.248 server distribution SHA/size drift")
    with zipfile.ZipFile(jar) as archive:
        members=archive.namelist()
        require(len(members) == len(set(members)), "duplicate server JAR member")
        require(CLASS in members, "component patch class missing in installed server JAR")
        binary=archive.read(CLASS)
        require(8 <= len(binary) <= MAX_CLASS_BYTES and binary[:4] == b"\xca\xfe\xba\xbe"
                and int.from_bytes(binary[6:8], "big") == 65,
                "component patch Java 21 classfile identity invalid")
        class_sha = hashlib.sha256(binary).hexdigest()
    result=subprocess.run([str(javap_bin), "-classpath",str(jar), "-c","-p","-s",OWNER],
                          capture_output=True,text=True,timeout=60,check=False)
    require(result.returncode == 0 and 100 < len(result.stdout) <= MAX_JAVAP_BYTES,
            "component patch exact javap failed or exceeded budget")
    try:
        initializer=parse_initializer(result.stdout, "STREAM_CODEC")
    except MojangBoundaryError as exc:
        raise ComponentPatchProbeError("DataComponentPatch.STREAM_CODEC static initializer unresolved: " +
                                      str(exc)) from exc
    methods=parse_methods(result.stdout)
    require(3 <= len(methods) <= MAX_CLASS_METHODS,
            "unexpected DataComponentPatch method population")
    sig=[(method_name(m),m["descriptor"]) for m in methods]
    require(len(sig)==len(set(sig)), "duplicate DataComponentPatch method signature")
    # Select only methods relevant to the codec. Do not store full disassemblies.
    candidates=[]
    for m in methods:
        symbols=" ".join(i["symbol"] for i in m["instructions"])
        name=method_name(m)
        if (name in ("<clinit>", "static", "read", "write", "encode", "decode") or
                name.startswith("lambda$") or
                any(c.lower() in symbols.lower() for c in CUES)):
            candidates.append(m)
    require(1 <= len(candidates) <= MAX_RELEVANT_METHODS,
            "bounded component patch codec method discovery exceeded")
    evidence=[selected_method(m) for m in candidates]
    require(initializer["optional_codec_putstatic_offset"] >= 0,
            "component patch static codec assignment unresolved")
    report={
        "schema_version":1,
        "scope":"NEOFORGE_211248_DISTRIBUTED_SERVER_COMPONENT_PATCH_ABI_ONLY",
        "artifact":{"server_jar_sha256":sha, "server_jar_bytes":size},
        "class_path":CLASS, "class_sha256":class_sha,
        "class_method_count":len(methods),
        "static_stream_codec_initializer":initializer,
        "selected_method_count":len(evidence),
        "methods":evidence,
        "limits":{
            "full_installed_modpack_class_loaded":"NOT_OBSERVED",
            "neoforge_runtime_modlauncher_transform":"NOT_OBSERVED",
            "data_component_patch_byte_limits":"NOT_VERIFIED",
            "data_component_patch_entry_limits":"NOT_VERIFIED",
            "nbt_depth_and_field_whitelist":"NOT_VERIFIED",
            "raygun_tag_authority":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutating_hook":"NOT_VERIFIED",
            "static_perk_certification":"NOT_CERTIFIED",
            "mutation":"NO_MUTATION"
        }
    }
    require(len(json.dumps(report,sort_keys=True).encode())<=MAX_REPORT_BYTES,
            "component patch compact evidence budget exceeded")
    return report


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--prior",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    report=audit(args.jar,args.javap,
                 json.loads(args.prior.read_text(encoding="utf8")))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
                           encoding="utf8")
    print("COMPONENT_PATCH_CLASS_SHA256="+report["class_sha256"])
    print("COMPONENT_PATCH_CLASS_METHOD_COUNT="+str(report["class_method_count"]))
    print("COMPONENT_PATCH_STATIC_CODEC_PUTSTATIC="+
          str(report["static_stream_codec_initializer"]["optional_codec_putstatic_offset"]))
    for ref in report["static_stream_codec_initializer"]["selected_preassignment_abi"]:
        print("COMPONENT_PATCH_STATIC_CODEC_REF="+json.dumps(ref,sort_keys=True))
    print("COMPONENT_PATCH_SELECTED_METHOD_COUNT="+str(report["selected_method_count"]))
    for method in report["methods"]:
        print("COMPONENT_PATCH_METHOD="+method["name"]+" "+method["descriptor"])
        print("COMPONENT_PATCH_METHOD_SHA256="+method["method_sha256"])
        print("COMPONENT_PATCH_METHOD_INSNS="+str(method["instruction_count"]))
        for ref in method["selected_refs"]:
            if any(c.lower() in ref["symbol"].lower() for c in CUES):
                print("COMPONENT_PATCH_ABI="+method["name"]+" "+json.dumps(ref,sort_keys=True))
        for b in method["conditional_branches"]:
            print("COMPONENT_PATCH_BRANCH="+method["name"]+" "+json.dumps(b,sort_keys=True))
    print("DISTRIBUTION_ONLY; LIMITS_NOT_VERIFIED; NO_MUTATION")


if __name__=="__main__":
    main()
