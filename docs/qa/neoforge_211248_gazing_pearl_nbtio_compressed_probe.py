#!/usr/bin/env python3
"""Read-only exact NeoForge 21.1.248 NbtIo compressed writer JVM discovery.

Source: checksum-pinned --installServer Minecraft 1.21.1 SRG and NeoForge
overlay, not a live transformed ModLauncher class nor a disk durability test.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from neoforge_211248_custom_data_delegate_probe import choose_archive
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

OWNER = "net/minecraft/nbt/NbtIo"
FALLBACK_OWNER = OWNER + "$StringFallbackDataOutput"
SELECT = {"writeCompressed", "write", "writeUnnamedTag", "writeUnnamedTagWithFallback", "writeAnyTag", "createCompressorStream"}
SCOPE = "NEOFORGE_211248_NBTIO_COMPRESSED_WRITE_DISTRIBUTED_ONLY"
MAX_METHODS = 175
MAX_SELECTED = 25
MAX_INSTRUCTIONS = 700
MAX_BYTES = 260_000
MAX_CLASS_BYTES = 450_000


def audit(server: Path, srg: Path, javap: str) -> dict:
    dist = verify_distribution(server, srg)
    member = OWNER + ".class"
    with ZipFile(server) as overlay, ZipFile(srg) as vanilla:
        ov, mc = overlay.namelist(), vanilla.namelist()
        require(len(ov) == len(set(ov)) and len(mc) == len(set(mc)),
                "duplicate archive member names")
        source = choose_archive(member, set(ov), set(mc))
        require(source in ("NEOFORGE_OVERLAY", "INSTALLED_MINECRAFT_SRG"),
                "NbtIo absent from exact server distribution")
        raw = (overlay if source == "NEOFORGE_OVERLAY" else vanilla).read(member)
    require(64 < len(raw) <= MAX_CLASS_BYTES and raw[:4] == b"\xca\xfe\xba\xbe",
            "NbtIo class byte budget/signature mismatch")
    reader = ClassReader(raw)
    require(reader.name == OWNER and reader.major == 65,
            "wrong NbtIo class identity/bytecode major")
    require(len(reader.methods) <= MAX_METHODS, "unbounded NbtIo declarations")
    declared = {(m["name"], m["descriptor"]): m for m in reader.methods}
    require(len(declared) == len(reader.methods), "duplicate NbtIo declaration")
    parsed = disassemble(str(server) + ":" + str(srg), javap, OWNER)
    require(set(parsed) == set(declared), "javap/constant pool declaration mismatch")
    selected = sorted(k for k in parsed if k[0] in SELECT
                      or k[0].startswith("lambda$writeCompressed$"))
    require(8 <= len(selected) <= MAX_SELECTED,
            "unexpected compressed writer method selection size")
    bodies, nonexecutable = [], []
    for key in selected:
        decl = declared[key]
        if "code_sha256" not in decl:
            require(not parsed[key] and decl["access"] & (0x0400 | 0x0100),
                    "Code absent without abstract/native declaration")
            nonexecutable.append(decl)
            continue
        item = summarize(reader, key, parsed[key])
        require(0 < item["instruction_count"] <= MAX_INSTRUCTIONS,
                "selected JVM body unbounded")
        bodies.append(item)
    compressed = [x for x in bodies
                  if x["declaration"]["name"] == "writeCompressed" and
                  x["declaration"]["descriptor"] ==
                  "(Lnet/minecraft/nbt/CompoundTag;Ljava/io/OutputStream;)V"]
    require(len(compressed) == 1, "expected exact compressed OutputStream ABI absent")
    # This wrapper is a direct transitive writer consumer through
    # writeUnnamedTagWithFallback; do not infer its behavior from its name.
    fallback_member = FALLBACK_OWNER + ".class"
    with ZipFile(server) as overlay, ZipFile(srg) as vanilla:
        ov, mc = overlay.namelist(), vanilla.namelist()
        fallback_source = choose_archive(fallback_member, set(ov), set(mc))
        require(fallback_source in ("NEOFORGE_OVERLAY", "INSTALLED_MINECRAFT_SRG"),
                "exact string fallback inner class not located")
        fallback_raw = (overlay if fallback_source == "NEOFORGE_OVERLAY" else vanilla).read(fallback_member)
    require(64 < len(fallback_raw) <= MAX_CLASS_BYTES and fallback_raw[:4] == b"\xca\xfe\xba\xbe",
            "string fallback classfile budget/signature drift")
    fallback_reader = ClassReader(fallback_raw)
    require(fallback_reader.name == FALLBACK_OWNER and fallback_reader.major == 65,
            "string fallback JVM identity drift")
    require(1 <= len(fallback_reader.methods) <= 45, "string fallback method roster unbounded")
    fallback_parsed = disassemble(str(server) + ":" + str(srg), javap, FALLBACK_OWNER)
    fallback_declarations = {(m["name"],m["descriptor"]):m for m in fallback_reader.methods}
    require(set(fallback_declarations) == set(fallback_parsed) and
            len(fallback_declarations) == len(fallback_reader.methods),
            "fallback class declarations mismatch")
    fallback_bodies = []
    fallback_nonexec = []
    for key in sorted(fallback_parsed):
        decl = fallback_declarations[key]
        if "code_sha256" not in decl:
            require(not fallback_parsed[key] and decl["access"] & (0x0400 | 0x0100),
                    "non-executable fallback method not flagged")
            fallback_nonexec.append(decl)
            continue
        item = summarize(fallback_reader, key, fallback_parsed[key])
        require(0 < item["instruction_count"] <= MAX_INSTRUCTIONS,
                "fallback method instruction budget exceeded")
        fallback_bodies.append(item)
    roster = [
        {"name":m["name"],"descriptor":m["descriptor"],"access":m["access"],
         "code_sha256":m.get("code_sha256")}
        for m in reader.methods
    ]
    return {
        "schema_version":1,"scope":SCOPE,
        "distribution":dist,
        "class":{
            "owner":OWNER,"source_archive":source,"class_major":reader.major,
            "class_sha256":digest(raw),"declared_method_count":len(reader.methods),
            "declared_methods":roster,"field_names":[f["name"] for f in reader.fields],
            "selected_methods":bodies,
            "non_executable_declarations":nonexecutable,
        },
        "string_fallback":{
            "owner":FALLBACK_OWNER,
            "source_archive":fallback_source,
            "class_sha256":digest(fallback_raw),
            "class_major":fallback_reader.major,
            "parent":fallback_reader.parent,
            "declared_method_count":len(fallback_reader.methods),
            "fields":[field["name"] for field in fallback_reader.fields],
            "selected_methods":fallback_bodies,
            "non_executable_declarations":fallback_nonexec,
        },
        "publisher_callsite":"SavedData.lambda$save$0 → IOUtilities.writeNbtCompressed → IOUtilities.lambda$writeNbtCompressed$1 → NbtIo.writeCompressed(CompoundTag,OutputStream)",
        "scope_limit":"exact official 21.1.248 distributed JVM only",
        "modlauncher_loaded":"NOT_OBSERVED",
        "physical_installed_modpack_parity":"NOT_VERIFIED",
        "filesystem_write_or_restart":"NOT_TESTED",
        "actual_nbt_reload":"NOT_TESTED",
        "shutdown_wait_callsite":"NOT_VERIFIED",
        "physical_qa":"NOT_TESTED",
        "static_contract":"NOT_CERTIFIED",
        "mutating_hook":"NOT_VERIFIED",
        "mutation":"NO_MUTATION",
        "provider_universe_closed":False,
        "semantic_magic_roots_delta":0,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server",type=Path,required=True)
    p.add_argument("--srg",type=Path,required=True)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    require(a.output.suffix == ".json" and not a.output.exists(),
            "write-once bounded JSON evidence path required")
    report=audit(a.server,a.srg,a.javap)
    raw=canonical(report).encode("utf8")
    require(0 < len(raw) <= MAX_BYTES,"report budget exceeded")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(raw)
    print("NBTIO_REPORT_SHA256",hashlib.sha256(raw).hexdigest())
    print("NBTIO_CLASS",report["class"]["source_archive"],
          report["class"]["class_sha256"],
          "declared",report["class"]["declared_method_count"])
    print("FALLBACK_CLASS",report["string_fallback"]["class_sha256"],"methods",report["string_fallback"]["declared_method_count"])
    for m in report["class"]["selected_methods"]:
        d=m["declaration"]
        print("METHOD",d["name"],d["descriptor"],d["code_sha256"],
              m["instruction_sha256"],m["instruction_count"])
    for m in report["string_fallback"]["selected_methods"]:
        d=m["declaration"]
        print("FALLBACK_METHOD",d["name"],d["descriptor"],d["code_sha256"],m["instruction_sha256"],m["instruction_count"])
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED NOT_MODLAUNCHER")


if __name__=="__main__":
    main()
