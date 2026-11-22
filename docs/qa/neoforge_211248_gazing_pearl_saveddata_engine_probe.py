#!/usr/bin/env python3
"""Read-only installed NeoForge 21.1.248 SavedData/DimensionDataStorage ABI probe.

Inspect official --installServer distributed Minecraft 1.21.1 SRG classes and
NeoForge overlay (overlay wins). Never load third-party classes or infer the
runtime-transformed ModLauncher class, disk settlement or physical modpack QA.
No Minecraft or NeoForge bytecode is copied into project source files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from neoforge_211248_custom_data_delegate_probe import (
    PINNED_SERVER_JAR_SHA256, PINNED_SRG_JAR_SHA256, EXPECTED_SERVER_BYTES,
    choose_archive,
)
from neoforge_211248_itemstack_server_codec_probe import sha256_file

CLASSES = {
    "storage": "net/minecraft/world/level/storage/DimensionDataStorage",
    "saved_data": "net/minecraft/world/level/saveddata/SavedData",
    "factory": "net/minecraft/world/level/saveddata/SavedData$Factory",
}
SELECT = {
    "storage": {"computeIfAbsent", "get", "set", "save", "readSavedData",
                "readTagFromDisk", "getDataFile"},
    "saved_data": {"setDirty", "isDirty", "save"},
    "factory": {"<init>", "creator", "deserializer", "type"},
}
MAX_METHODS = 120
MAX_SELECTED = 26
MAX_INSTRUCTIONS = 800
MAX_FIELDS = 40
MAX_BYTES = 350_000


def verify_distribution(server: Path, srg: Path) -> dict:
    server_sha, server_bytes = sha256_file(server)
    srg_sha, srg_bytes = sha256_file(srg)
    require((server_sha, server_bytes) ==
            (PINNED_SERVER_JAR_SHA256, EXPECTED_SERVER_BYTES),
            "official NeoForge server 21.1.248 JAR SHA/length drift")
    require(srg_sha == PINNED_SRG_JAR_SHA256 and 2_000_000 < srg_bytes < 120_000_000,
            "installed Minecraft 1.21.1 SRG JAR identity drift")
    return {
        "minecraft_version": "1.21.1", "neoforge_version": "21.1.248",
        "installer_sha256":
            "68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c",
        "neoforge_server_sha256": server_sha,
        "neoforge_server_bytes": server_bytes,
        "minecraft_srg_sha256": srg_sha,
        "minecraft_srg_bytes": srg_bytes,
        "modlauncher_loaded_bytes": "NOT_OBSERVED",
    }


def inspect(server: Path, srg: Path, javap: str) -> dict:
    artifact = verify_distribution(server, srg)
    with ZipFile(server) as overlay, ZipFile(srg) as vanilla:
        ov_names, mc_names = overlay.namelist(), vanilla.namelist()
        require(len(ov_names) == len(set(ov_names)) and
                len(mc_names) == len(set(mc_names)),
                "duplicate entries in official distribution archive")
        captured = {}
        for label, owner in CLASSES.items():
            entry = owner + ".class"
            source = choose_archive(entry, set(ov_names), set(mc_names))
            require(source in {"NEOFORGE_OVERLAY", "INSTALLED_MINECRAFT_SRG"},
                    "expected engine class absent: " + entry)
            blob = (overlay if source == "NEOFORGE_OVERLAY" else vanilla).read(entry)
            require(64 <= len(blob) <= 600_000 and blob[:4] == b"\xca\xfe\xba\xbe",
                    "engine classfile missing or malformed: " + label)
            captured[label] = (owner, source, blob)

    classes = {}
    classpath = str(server) + ":" + str(srg)
    for label, (owner, source, blob) in captured.items():
        reader = ClassReader(blob)
        require(reader.name == owner and reader.major == 65,
                "unexpected JVM identity/Java major: " + label)
        require(len(reader.fields) <= MAX_FIELDS and
                len(reader.methods) <= MAX_METHODS,
                "engine class declaration budget exceeded: " + label)
        parsed = disassemble(classpath, javap, owner)
        required = {"storage": {"computeIfAbsent", "save"},
                    "saved_data": {"setDirty", "isDirty", "save"},
                    "factory": {"<init>"}}[label]
        methods = []
        abstract_or_native = []
        candidates = [(name, desc) for (name, desc) in parsed
                      if name in SELECT[label]]
        require(len(candidates) <= MAX_SELECTED,
                "unbounded selected engine method roster: " + label)
        for key in sorted(candidates):
            matches = [m for m in reader.methods
                       if (m["name"], m["descriptor"]) == key]
            require(len(matches) == 1, "engine declaration not unique: " + str(key))
            declaration = matches[0]
            if "code_sha256" not in declaration:
                # javap includes abstract declarations as empty parsed bodies.
                # Preserve them explicitly; a missing Code is not a silent skip.
                require(not parsed[key], "non-executable JVM declaration had opcodes")
                require(declaration["access"] & (0x0400 | 0x0100),
                        "missing Code attribute without abstract/native flag")
                abstract_or_native.append(declaration)
                continue
            body = summarize(reader, key, parsed[key])
            require(len(body["instructions"]) <= MAX_INSTRUCTIONS,
                    "unexpected engine method bytecode budget: " + str(key))
            methods.append(body)
        declared = {m["declaration"]["name"] for m in methods} | {
            m["name"] for m in abstract_or_native}
        require(required.issubset(declared),
                "required engine method declaration missing: " + label)
        if label == "saved_data":
            require({"setDirty", "isDirty"}.issubset(
                {m["declaration"]["name"] for m in methods}),
                "SavedData dirtiness methods must have executable Code")
        classes[label] = {
            "owner": owner, "source_archive": source,
            "class_sha256": digest(blob), "class_major": reader.major,
            "parent": reader.parent, "access": reader.access,
            "fields": reader.fields, "declared_method_count": len(reader.methods),
            "selected_method_count": len(methods),
            "non_executable_declarations": abstract_or_native,
            "selected_methods": methods,
            "not_transformed_runtime": True,
        }
    return {
        "artifacts": artifact,
        "classes": classes,
        "selection": "Finite exact names for factory, storage cache/load/save and dirty flag",
        "provenance": "Official NeoForge 21.1.248 --installServer overlay+Minecraft SRG",
    }


def make_report(server: Path, srg: Path, javap: str) -> dict:
    native = inspect(server, srg, javap)
    return {
        "schema_version": 1,
        "scope": "GAZING_PEARL_OFFICIAL_NEOFORGE_211248_SAVEDDATA_DISTRIBUTED_ABI_ONLY",
        "native": native,
        "installed_modpack_engine_bytes": "NOT_VERIFIED",
        "publisher_engine_callsite": "ACPlatform.computeIfAbsent -> DimensionDataStorage.computeIfAbsent",
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server", type=Path, required=True)
    p.add_argument("--srg", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    require(args.output.suffix == ".json" and not args.output.exists(),
            "write-once exact engine report required")
    report = make_report(args.server, args.srg, args.javap)
    data = canonical(report).encode("utf8")
    require(len(data) <= MAX_BYTES, "engine report byte budget exceeded")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print("ENGINE_REPORT_SHA256", hashlib.sha256(data).hexdigest())
    for label, row in report["native"]["classes"].items():
        print("CLASS", label, row["source_archive"], row["class_sha256"],
              row["selected_method_count"])
        for method in row["selected_methods"]:
            d = method["declaration"]
            print("METHOD", label, d["name"], d["descriptor"],
                  d["code_sha256"], method["instruction_sha256"])
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED MODLAUNCHER_NOT_OBSERVED")


if __name__ == "__main__":
    main()
