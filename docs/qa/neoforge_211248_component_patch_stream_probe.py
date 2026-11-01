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
from minecraft_1211_itemstack_optional_stream_probe import (
    MojangBoundaryError, parse_initializer, codec_class_from_initializer,
    inspect_codec_class
)
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
    try:
        implementation_owner=codec_class_from_initializer(initializer)
        implementation=inspect_codec_class(
            jar, javap_bin, CLASS[:-6], implementation_owner)
    except (MojangBoundaryError, KeyError, zipfile.BadZipFile) as exc:
        raise ComponentPatchProbeError(
            "DataComponentPatch actual STREAM_CODEC inner class unresolved: " +
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
    # Bound a small JVM prefix of the *anonymous decoder* for count/loop
    # provenance. It is not the full implementation or any proof of limits.
    impl_cmd = [str(javap_bin), "-classpath", str(jar), "-c", "-p", "-s",
                implementation["class_path"][:-6].replace("/", ".")]
    compiled = subprocess.run(impl_cmd, capture_output=True, text=True,
                              timeout=60, check=False)
    require(compiled.returncode == 0 and 0 < len(compiled.stdout) < MAX_JAVAP_BYTES,
            "anonymous codec JVM prefix not readable")
    impl_methods = parse_methods(compiled.stdout)
    decoder = [m for m in impl_methods if method_name(m) == "decode" and
               m["descriptor"] ==
               "(Lnet/minecraft/network/RegistryFriendlyByteBuf;)"
               "Lnet/minecraft/core/component/DataComponentPatch;"]
    require(len(decoder) == 1, "anonymous component patch decoder signature drift")
    prefix = [
        {"offset":i["offset"], "opcode":i["opcode"],
         "operand":i["operand"][:60],
         "symbol":i["symbol"][:240]}
        for i in decoder[0]["instructions"] if i["offset"] <= 52
    ]
    require(10 <= len(prefix) <= 36, "unbounded/empty codec count prefix")
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
        "stream_codec_implementation":implementation,
        "stream_codec_count_prefix":prefix,
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



EXACT_CLASS_SHA256 = "24f57ec112e9f3ec1e8db754e9014b5b02e2f2c6283f13fbffd27fb90be8d263"
EXACT_CODEC_SHA256 = "d98b1334116457aea1f6b174e9f0760e6897d965eda58b7f57865bd1e5427880"
DECODE = ("decode", "(Lnet/minecraft/network/RegistryFriendlyByteBuf;)Lnet/minecraft/core/component/DataComponentPatch;")
ENCODE = ("encode", "(Lnet/minecraft/network/RegistryFriendlyByteBuf;Lnet/minecraft/core/component/DataComponentPatch;)V")
ENCODE_COMPONENT = ("encodeComponent", "(Lnet/minecraft/network/RegistryFriendlyByteBuf;Lnet/minecraft/core/component/DataComponentType;Ljava/lang/Object;)V")
EXACT_CODEC_METHODS = (
    ("DataComponentPatch$1", "()V"), DECODE, ENCODE, ENCODE_COMPONENT,
    ("decode", "(Ljava/lang/Object;)Ljava/lang/Object;"),
    ("encode", "(Ljava/lang/Object;Ljava/lang/Object;)V")
)
# (method, descriptor, JVM offset, opcode, symbolic fragment, optional target)
ABI_SITES = (
    (*DECODE, 1, "invokevirtual", "RegistryFriendlyByteBuf.readVarInt:", ""),
    (*DECODE, 6, "invokevirtual", "RegistryFriendlyByteBuf.readVarInt:", ""),
    (*DECODE, 11, "ifne", "", "22"),
    (*DECODE, 15, "ifne", "", "22"),
    (*DECODE, 18, "getstatic", "DataComponentPatch.EMPTY:", ""),
    (*DECODE, 35, "invokestatic", "java/lang/Math.min:", ""),
    (*DECODE, 38, "invokespecial", "Reference2ObjectArrayMap.", ""),
    (*DECODE, 49, "if_icmpge", "", "102"),
    (*DECODE, 52, "getstatic", "DataComponentType.STREAM_CODEC:", ""),
    (*DECODE, 56, "invokeinterface", "StreamCodec.decode:", ""),
    (*DECODE, 68, "invokeinterface", "DataComponentType.streamCodec:", ""),
    (*DECODE, 74, "invokeinterface", "StreamCodec.decode:", ""),
    (*DECODE, 99, "goto", "", "46"),
    (*DECODE, 108, "if_icmpge", "", "144"),
    (*DECODE, 111, "getstatic", "DataComponentType.STREAM_CODEC:", ""),
    (*DECODE, 115, "invokeinterface", "StreamCodec.decode:", ""),
    (*DECODE, 129, "invokestatic", "java/util/Optional.empty:", ""),
    (*DECODE, 144, "new", "DataComponentPatch", ""),
    (*ENCODE, 4, "ifeq", "", "22"),
    (*ENCODE, 9, "invokevirtual", "RegistryFriendlyByteBuf.writeVarInt:", ""),
    (*ENCODE, 15, "invokevirtual", "RegistryFriendlyByteBuf.writeVarInt:", ""),
    (*ENCODE, 93, "invokevirtual", "RegistryFriendlyByteBuf.writeVarInt:", ""),
    (*ENCODE, 100, "invokevirtual", "RegistryFriendlyByteBuf.writeVarInt:", ""),
    (*ENCODE, 172, "getstatic", "DataComponentType.STREAM_CODEC:", ""),
    (*ENCODE, 191, "invokestatic", "encodeComponent:", ""),
    (*ENCODE, 261, "getstatic", "DataComponentType.STREAM_CODEC:", ""),
    (*ENCODE_COMPONENT, 1, "invokeinterface", "DataComponentType.streamCodec:", ""),
    (*ENCODE_COMPONENT, 8, "invokeinterface", "StreamCodec.encode:", ""),
)
# JVM prefix: source of two counters, sum, capacity initialization, loop bound.
COUNT_PREFIX_SITES = (
    (1, "invokevirtual", "RegistryFriendlyByteBuf.readVarInt:", ""),
    (4, "istore_2", "", ""),
    (6, "invokevirtual", "RegistryFriendlyByteBuf.readVarInt:", ""),
    (9, "istore_3", "", ""),
    (24, "iadd", "", ""),
    (25, "istore", "", "4"),
    (31, "iload", "", "4"),
    (33, "ldc", "int 65536", ""),
    (35, "invokestatic", "java/lang/Math.min:", ""),
    (38, "invokespecial", "Reference2ObjectArrayMap.", ""),
    (46, "iload", "", "6"),
    (48, "iload_2", "", ""),
    (49, "if_icmpge", "", "102"),
)
LIMITS = {
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


def snapshot_projection(report):
    """Solely distributed 21.1.248 JVM ABI; preserve the capacity-vs-limit boundary."""
    require(report["scope"] == "NEOFORGE_211248_DISTRIBUTED_SERVER_COMPONENT_PATCH_ABI_ONLY"
            and report["artifact"] == {
                "server_jar_sha256":PINNED_SERVER_JAR_SHA256,
                "server_jar_bytes":EXPECTED_JAR_SIZE},
            "official 21.1.248 distribution authority drift")
    require(report["class_path"] == CLASS and
            report["class_sha256"] == EXACT_CLASS_SHA256 and
            report["class_method_count"] == 15 and
            report["selected_method_count"] == 7,
            "component patch outer class roster/hash drift")
    init=report["static_stream_codec_initializer"]
    require(init["optional_codec_putstatic_offset"] == 49,
            "DataComponentPatch.STREAM_CODEC assigned at unexpected JVM offset")
    initializer=init["selected_preassignment_abi"]
    for off,op,sym in (
        (42,"new","DataComponentPatch$1"),
        (46,"invokespecial","DataComponentPatch$1"),
        (49,"putstatic","Field STREAM_CODEC:"),
    ):
        matches=[x for x in initializer if x["offset"] == off]
        require(len(matches)==1 and matches[0]["opcode"] == op and
                sym in matches[0]["symbol"], "component patch static codec owner drift")
    codec=report["stream_codec_implementation"]
    require(codec["class_path"] ==
            "net/minecraft/core/component/DataComponentPatch$1.class" and
            codec["class_sha256"] == EXACT_CODEC_SHA256,
            "component patch anonymous codec class hash drift")
    require(tuple((m["name"],m["descriptor"]) for m in codec["methods"]) ==
            EXACT_CODEC_METHODS, "component patch native codec method signatures drift")
    prefix=report["stream_codec_count_prefix"]
    require(len({p["offset"] for p in prefix}) == len(prefix),
            "duplicate component patch decoder prefix offset")
    count_anchors=[]
    for off,op,sym,operand in COUNT_PREFIX_SITES:
        m=[x for x in prefix if x["offset"] == off]
        require(len(m)==1 and m[0]["opcode"] == op and
                sym in m[0]["symbol"] and
                (not operand or m[0]["operand"] == operand),
                "decoded patch counter or initial map capacity ABI drift")
        count_anchors.append(m[0])
    # 65536 is passed to Math.min(total count, 65536) for map *capacity*.
    # The loops use the original packet counts. Do not label it a count cap.
    method_pivots=[]
    for name,desc,off,op,sym,operand in ABI_SITES:
        method=next(m for m in codec["methods"]
                    if m["name"] == name and m["descriptor"] == desc)
        matching=[x for x in method["selected_refs"] if x["offset"]==off]
        require(len(matching)==1 and matching[0]["opcode"] == op and
                sym in matching[0]["symbol"] and
                (not operand or matching[0]["operand"] == operand),
                "distributed component patch decode/encode pivot drift")
        method_pivots.append({"method":name,"descriptor":desc,**matching[0]})
    require(report["limits"]==LIMITS,
            "false gameplay/security/certification promotion")
    return {
        "schema_version":report["schema_version"],
        "scope":report["scope"],
        "artifact":report["artifact"],
        "class_path":report["class_path"],
        "class_sha256":report["class_sha256"],
        "class_method_count":report["class_method_count"],
        "selected_method_count":report["selected_method_count"],
        "static_codec_assignment_offset":init["optional_codec_putstatic_offset"],
        "codec_class_path":codec["class_path"],
        "codec_class_sha256":codec["class_sha256"],
        "codec_method_signatures":[
            {"name":m["name"],"descriptor":m["descriptor"]}
            for m in codec["methods"]],
        "counter_and_initial_capacity_abi":count_anchors,
        "count_capacity_interpretation":"65536_MAP_INITIAL_CAPACITY_ONLY_NOT_VERIFIED_ENTRY_LIMIT",
        "critical_codec_abi":method_pivots,
        "limits":report["limits"]
    }


def verify_snapshot(report, snapshot):
    require(snapshot_projection(report) == snapshot,
            "sealed 21.1.248 component patch ABI snapshot mismatch")
    return True


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--prior",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--snapshot",type=Path,required=True)
    args=p.parse_args()
    report=audit(args.jar,args.javap,
                 json.loads(args.prior.read_text(encoding="utf8")))
    verify_snapshot(report,json.loads(args.snapshot.read_text(encoding="utf8")))
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
    impl=report["stream_codec_implementation"]
    print("COMPONENT_PATCH_CODEC_CLASS="+impl["class_path"])
    print("COMPONENT_PATCH_CODEC_CLASS_SHA256="+impl["class_sha256"])
    for row in report["stream_codec_count_prefix"]:
        print("COMPONENT_PATCH_COUNT_PREFIX="+json.dumps(row,sort_keys=True))
    for method in impl["methods"]:
        print("COMPONENT_PATCH_CODEC_METHOD="+method["name"]+" "+method["descriptor"])
        print("COMPONENT_PATCH_CODEC_METHOD_INSNS="+str(method["instruction_count"]))
        for row in method["selected_refs"]:
            print("COMPONENT_PATCH_CODEC_REF="+method["name"]+" "+json.dumps(row,sort_keys=True))
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
