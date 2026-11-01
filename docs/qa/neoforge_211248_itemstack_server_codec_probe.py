#!/usr/bin/env python3
"""Read-only, bounded ItemStack stream codec scan of NeoForge 21.1.248 server distribution.

This inspects the official NeoForge *installed server JAR*. It does not execute
ModLauncher, mixin transforms, a client or the full user modpack, and cannot
prove bytecode of the final runtime-loaded class or server packet authorization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

from minecraft_1211_itemstack_optional_stream_probe import (
    MojangBoundaryError, codec_class_from_initializer, inspect_codec_class,
    parse_initializer
)

VERSION = "21.1.248"
ITEM = "net/minecraft/world/item/ItemStack"
ITEM_CLASS = ITEM + ".class"
MAX_SERVER_JAR_BYTES = 85_000_000
MAX_REPORT_BYTES = 48000


class NeoForgeServerCodecError(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise NeoForgeServerCodecError(reason)


def sha256_file(path):
    digest = hashlib.sha256()
    size = 0
    with Path(path).open("rb") as f:
        while chunk := f.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def method_reference_counts(implementation):
    methods = implementation["methods"]
    if not 2 <= len(methods) <= 12:
        raise NeoForgeServerCodecError("server codec method count exceeded")
    return [
        {"name": m["name"], "descriptor": m["descriptor"],
         "instructions": m["instruction_count"],
         "reference_count": len(m["selected_refs"])}
        for m in methods
    ]


def audit(server_jar, java_disassembler, vanilla_seal):
    require(vanilla_seal.get("scope") ==
            "OFFICIAL_MOJANG_VANILLA_1211_ITEMSTACK_STATIC_ABI_CORROBORATION_ONLY" and
            vanilla_seal.get("version") == "1.21.1" and
            vanilla_seal["limits"]["neoforge_21_1_248_merged_runtime"] == "NOT_INSPECTED",
            "upstream vanilla evidence scope/policy drift")
    server_sha, server_size = sha256_file(server_jar)
    require(5_000_000 < server_size <= MAX_SERVER_JAR_BYTES,
            "NeoForge installed server class JAR size implausible")
    with zipfile.ZipFile(server_jar) as jar:
        members = jar.namelist()
        require(len(members) == len(set(members)), "duplicate server distribution member")
        require(ITEM_CLASS in members,
                "expected mapped Minecraft ItemStack class absent from server distribution")
        raw = jar.read(ITEM_CLASS)
        require(len(raw) >= 8 and raw[:4] == b"\xca\xfe\xba\xbe" and
                int.from_bytes(raw[6:8], "big") == 65,
                "wrong Java 21 Minecraft ItemStack classfile")
        item_sha = hashlib.sha256(raw).hexdigest()
    result = subprocess.run([
        str(java_disassembler), "-classpath", str(server_jar),
        "-c", "-p", "-s", ITEM.replace("/", ".")],
        capture_output=True, text=True, timeout=60, check=False)
    require(result.returncode == 0 and result.stdout and
            len(result.stdout) < 2_300_000,
            "cannot inspect exact distributed ItemStack JVM bytecode")
    try:
        init = parse_initializer(result.stdout, "OPTIONAL_STREAM_CODEC")
        inner = codec_class_from_initializer(init)
        implementation = inspect_codec_class(
            server_jar, java_disassembler, ITEM, inner)
    except (MojangBoundaryError, KeyError, zipfile.BadZipFile) as exc:
        raise NeoForgeServerCodecError(
            "NeoForge distributed ItemStack codec not resolvable; fail closed: " +
            str(exc)) from exc
    require(implementation["class_path"].startswith(ITEM + "$"),
            "NeoForge ItemStack codec inner class provenance drift")
    report = {
        "schema_version": 1,
        "scope": "OFFICIAL_NEOFORGE_211248_INSTALLED_SERVER_CLASSFILE_NOT_LOADED_RUNTIME",
        "minecraft_version": "1.21.1",
        "neoforge_version": VERSION,
        "installed_server_jar_sha256": server_sha,
        "installed_server_jar_size": server_size,
        "itemstack_class_path": ITEM_CLASS,
        "itemstack_class_sha256": item_sha,
        "optional_codec_initializer": init,
        "optional_codec_implementation": implementation,
        "method_reference_counts": method_reference_counts(implementation),
        "vanilla_comparison": {
            "official_client_sha1": vanilla_seal["official_client_sha1"],
            "vanilla_itemstack_sha256": vanilla_seal["class_sha256"],
            "vanilla_codec_class_sha256": vanilla_seal["codec_class_sha256"],
            "same_itemstack_class_bytes": item_sha ==
                vanilla_seal["class_sha256"],
            "same_codec_class_bytes": implementation["class_sha256"] ==
                vanilla_seal["codec_class_sha256"]
        },
        "limits": {
            "jvm_modlauncher_class_loaded": "NOT_OBSERVED",
            "neoforge_modpack_runtime_transformations": "NOT_OBSERVED",
            "gameplay_network_authorization": "NOT_VERIFIED",
            "data_component_patch_limits": "NOT_VERIFIED",
            "nbt_size_depth_and_fields": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutating_hook": "NOT_VERIFIED",
            "perk_static_certification": "NOT_CERTIFIED",
            "mutation": "NO_MUTATION"
        }
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf8"))
            < MAX_REPORT_BYTES, "bounded server ABI report overflow")
    return report



# Observed in official 21.1.248 --installServer distribution (not a loaded class).
PINNED_SERVER_JAR_SHA256 = "1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359"
PINNED_ITEMSTACK_CLASS_SHA256 = "072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13"
PINNED_CODEC_CLASS_SHA256 = "414239d4c913a25cda60a8fc9e6f41661d7939dc9f9f6f4e23f0731468c46925"
REQUIRED_METHODS = (
    ("ItemStack$1", "()V"),
    ("decode", "(Lnet/minecraft/network/RegistryFriendlyByteBuf;)Lnet/minecraft/world/item/ItemStack;"),
    ("encode", "(Lnet/minecraft/network/RegistryFriendlyByteBuf;Lnet/minecraft/world/item/ItemStack;)V"),
    ("decode", "(Ljava/lang/Object;)Ljava/lang/Object;"),
    ("encode", "(Ljava/lang/Object;Ljava/lang/Object;)V")
)
DEC = REQUIRED_METHODS[1][1]
ENC = REQUIRED_METHODS[2][1]
ABI_PIVOTS = (
    ("decode", DEC, 1, "invokevirtual", "RegistryFriendlyByteBuf.readVarInt:", ""),
    ("decode", DEC, 6, "ifgt", "", "13"),
    ("decode", DEC, 9, "getstatic", "ItemStack.EMPTY:", ""),
    ("decode", DEC, 13, "getstatic", "ITEM_STREAM_CODEC:", ""),
    ("decode", DEC, 17, "invokeinterface", "StreamCodec.decode:", ""),
    ("decode", DEC, 26, "getstatic", "DataComponentPatch.STREAM_CODEC:", ""),
    ("decode", DEC, 30, "invokeinterface", "StreamCodec.decode:", ""),
    ("encode", ENC, 4, "ifeq", "", "16"),
    ("encode", ENC, 9, "invokevirtual", "RegistryFriendlyByteBuf.writeVarInt:", ""),
    ("encode", ENC, 21, "invokevirtual", "RegistryFriendlyByteBuf.writeVarInt:", ""),
    ("encode", ENC, 25, "getstatic", "ITEM_STREAM_CODEC:", ""),
    ("encode", ENC, 33, "invokeinterface", "StreamCodec.encode:", ""),
    ("encode", ENC, 38, "getstatic", "DataComponentPatch.STREAM_CODEC:", ""),
    ("encode", ENC, 46, "invokevirtual", "PatchedDataComponentMap.asPatch:", ""),
    ("encode", ENC, 49, "invokeinterface", "StreamCodec.encode:", "")
)
SEALED_LIMITS = {
    "jvm_modlauncher_class_loaded": "NOT_OBSERVED",
    "neoforge_modpack_runtime_transformations": "NOT_OBSERVED",
    "gameplay_network_authorization": "NOT_VERIFIED",
    "data_component_patch_limits": "NOT_VERIFIED",
    "nbt_size_depth_and_fields": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "mutating_hook": "NOT_VERIFIED",
    "perk_static_certification": "NOT_CERTIFIED",
    "mutation": "NO_MUTATION"
}


def snapshot_projection(report):
    """Server distribution checksum + bounded decoded JVM ABI; not runtime proof."""
    require(report["scope"] ==
            "OFFICIAL_NEOFORGE_211248_INSTALLED_SERVER_CLASSFILE_NOT_LOADED_RUNTIME" and
            report["neoforge_version"] == VERSION and
            report["minecraft_version"] == "1.21.1",
            "authority scope/version drift")
    require(report["installed_server_jar_sha256"] == PINNED_SERVER_JAR_SHA256
            and report["installed_server_jar_size"] == 5675624,
            "installed server distribution JAR identity drift")
    require(report["itemstack_class_path"] == ITEM_CLASS and
            report["itemstack_class_sha256"] == PINNED_ITEMSTACK_CLASS_SHA256,
            "distributed ItemStack class identity drift")
    codec = report["optional_codec_implementation"]
    require(codec["class_path"] == ITEM + "$1.class" and
            codec["class_sha256"] == PINNED_CODEC_CLASS_SHA256,
            "distributed optional stream codec class identity drift")
    require(report["optional_codec_initializer"]["optional_codec_putstatic_offset"] == 127,
            "distributed codec initialization ABI drift")
    methods = codec["methods"]
    require(tuple((m["name"], m["descriptor"]) for m in methods) ==
            REQUIRED_METHODS, "distributed codec method roster drift")
    pivots = []
    for name, desc, off, opcode, symbol, operand in ABI_PIVOTS:
        method = next(x for x in methods
                      if x["name"] == name and x["descriptor"] == desc)
        matches = [x for x in method["selected_refs"] if x["offset"] == off]
        require(len(matches) == 1 and matches[0]["opcode"] == opcode
                and symbol in matches[0]["symbol"] and
                matches[0]["operand"] == operand,
                "distributed codec critical branch or delegate drift")
        pivots.append({
            "method": name, "descriptor": desc, **matches[0]
        })
    require(report["limits"] == SEALED_LIMITS,
            "false security/runtime/gameplay authority promotion")
    vanilla = report["vanilla_comparison"]
    require(vanilla["same_itemstack_class_bytes"] is False and
            vanilla["same_codec_class_bytes"] is False,
            "unjustified byte-for-byte vanilla/NeoForge parity claim")
    return {
        **{key: report[key] for key in (
            "schema_version", "scope", "minecraft_version", "neoforge_version",
            "installed_server_jar_sha256", "installed_server_jar_size",
            "itemstack_class_path", "itemstack_class_sha256")},
        "codec_class_path": codec["class_path"],
        "codec_class_sha256": codec["class_sha256"],
        "codec_static_assignment_offset":
            report["optional_codec_initializer"]["optional_codec_putstatic_offset"],
        "codec_methods": [
            {"name": m["name"], "descriptor": m["descriptor"]} for m in methods
        ],
        "critical_codec_abi": pivots,
        "vanilla_comparison": vanilla,
        "limits": report["limits"]
    }


def verify_snapshot(report, snapshot):
    require(snapshot_projection(report) == snapshot,
            "sealed official NeoForge distribution codec ABI mismatch")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--server", required=True, type=Path)
    p.add_argument("--vanilla-snapshot", required=True, type=Path)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--snapshot", required=True, type=Path)
    args = p.parse_args()
    prior = json.loads(args.vanilla_snapshot.read_text(encoding="utf8"))
    report = audit(args.server, args.javap, prior)
    verify_snapshot(report, json.loads(args.snapshot.read_text(encoding="utf8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True,
                                      ensure_ascii=False) + "\n", encoding="utf8")
    print("NEOFORGE_211248_SERVER_JAR_SHA256=" + report["installed_server_jar_sha256"])
    print("NEOFORGE_211248_SERVER_JAR_BYTES=" + str(report["installed_server_jar_size"]))
    print("NEOFORGE_211248_OPTIONAL_PUTSTATIC=" +
          str(report["optional_codec_initializer"]["optional_codec_putstatic_offset"]))
    print("NEOFORGE_211248_DISTRIBUTION_CLASS_SHA256=" +
          report["itemstack_class_sha256"])
    print("NEOFORGE_211248_DISTRIBUTION_CODEC_CLASS=" +
          report["optional_codec_implementation"]["class_path"])
    print("NEOFORGE_211248_DISTRIBUTION_CODEC_SHA256=" +
          report["optional_codec_implementation"]["class_sha256"])
    print("NEOFORGE_211248_DISTRIBUTION_COMPARED_VANILLA=" +
          json.dumps(report["vanilla_comparison"], sort_keys=True))
    for m in report["optional_codec_implementation"]["methods"]:
        print("NEOFORGE_211248_DISTRIBUTION_CODEC_METHOD=" +
              m["name"] + " " + m["descriptor"])
        for row in m["selected_refs"]:
            print("NEOFORGE_211248_DISTRIBUTION_CODEC_REF=" +
                  m["name"] + " " + json.dumps(row, sort_keys=True))
    print("DISTRIBUTION_ONLY; LOADED_RUNTIME_NOT_OBSERVED; NO_MUTATION")


if __name__ == "__main__":
    main()
