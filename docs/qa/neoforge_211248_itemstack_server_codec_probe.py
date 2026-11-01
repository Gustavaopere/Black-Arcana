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


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--server", required=True, type=Path)
    p.add_argument("--vanilla-snapshot", required=True, type=Path)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    prior = json.loads(args.vanilla_snapshot.read_text(encoding="utf8"))
    report = audit(args.server, args.javap, prior)
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
