#!/usr/bin/env python3
"""Read-only discovery of exact NeoForge 21.1.248 NBT Tag.write implementations.

The official --installServer NeoForge overlay and Minecraft 1.21.1 SRG JARs
are authoritative for this limited distributed-bytecode observation. This
is not a live ModLauncher, filesystem, persistence or game test.
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

OWNERS = (
    "net/minecraft/nbt/Tag",
    "net/minecraft/nbt/CompoundTag",
    "net/minecraft/nbt/ListTag",
    "net/minecraft/nbt/IntTag",
    "net/minecraft/nbt/IntArrayTag",
    "net/minecraft/nbt/StringTag",
)
SCOPE = "NEOFORGE_211248_NBT_TAG_WRITERS_DISTRIBUTED_DISCOVERY_ONLY"
MAX_CLASS_BYTES = 450_000
MAX_METHODS_PER_CLASS = 240
MAX_SELECTED_PER_CLASS = 25
MAX_INSTRUCTIONS = 850
MAX_REPORT_BYTES = 750_000


def audit(server: Path, srg: Path, javap: str) -> dict:
    dist = verify_distribution(server, srg)
    entries = []
    with ZipFile(server) as overlay, ZipFile(srg) as vanilla:
        ov, mc = set(overlay.namelist()), set(vanilla.namelist())
        require(len(ov) == len(overlay.namelist()) and len(mc) == len(vanilla.namelist()),
                "duplicate JAR member names")
        for owner in OWNERS:
            member = owner + ".class"
            source = choose_archive(member, ov, mc)
            require(source in ("NEOFORGE_OVERLAY", "INSTALLED_MINECRAFT_SRG"),
                    "required exact Tag class missing: " + owner)
            raw = (overlay if source == "NEOFORGE_OVERLAY" else vanilla).read(member)
            require(64 < len(raw) <= MAX_CLASS_BYTES and raw[:4] == b"\xca\xfe\xba\xbe",
                    "Tag classfile budget/identity failure: " + owner)
            reader = ClassReader(raw)
            require(reader.name == owner and reader.major == 65,
                    "Tag class identity/version mismatch: " + owner)
            require(1 <= len(reader.methods) <= MAX_METHODS_PER_CLASS,
                    "Tag class declaration count outside budget: " + owner)
            declared = {(m["name"], m["descriptor"]): m for m in reader.methods}
            require(len(declared) == len(reader.methods), "duplicate method declaration")
            parsed = disassemble(str(server) + ":" + str(srg), javap, owner)
            require(set(parsed) == set(declared), "javap/classfile declaration mismatch: " + owner)
            selected = sorted(k for k in parsed if k[0] in ("write", "writeNamedTag", "getId"))
            require(1 <= len(selected) <= MAX_SELECTED_PER_CLASS,
                    "unexpected Tag write/getId selection: " + owner)
            methods = []
            nonexec = []
            for key in selected:
                decl = declared[key]
                if "code_sha256" not in decl:
                    require(not parsed[key] and bool(decl["access"] & (0x0400 | 0x0100)),
                            "body missing without abstract/native flag: " + owner)
                    nonexec.append({"name": key[0], "descriptor": key[1], "access": decl["access"]})
                    continue
                item = summarize(reader, key, parsed[key])
                require(0 < item["instruction_count"] <= MAX_INSTRUCTIONS,
                        "Tag writer exceeds bounded instructions: " + owner)
                methods.append(item)
            if owner != "net/minecraft/nbt/Tag":
                require(any(m["declaration"]["name"] == "write" for m in methods),
                        "concrete Tag.write method missing: " + owner)
            entries.append({
                "owner": owner, "source_archive": source, "class_major": reader.major,
                "class_sha256": digest(raw), "parent": reader.parent,
                "declared_method_count": len(reader.methods),
                "fields": [f["name"] for f in reader.fields],
                "roster": [{"name": m["name"], "descriptor": m["descriptor"],
                            "access": m["access"], "code_sha256": m.get("code_sha256")}
                           for m in reader.methods],
                "selected_methods": methods, "non_executable_selected": nonexec,
            })
    return {
        "schema_version": 1, "scope": SCOPE, "distribution": dist,
        "classes": entries,
        "context": "NbtIo.writeUnnamedTag -> Tag.write virtual dispatch; this probe audits a bounded set of exact concrete NBT writers and the Tag interface",
        "all_tag_implementations_audited": False,
        "live_modlauncher": "NOT_OBSERVED",
        "installed_modpack_parity": "NOT_VERIFIED",
        "filesystem_write_or_restart": "NOT_TESTED",
        "actual_nbt_reload": "NOT_TESTED",
        "shutdown_wait_callsite": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server", type=Path, required=True)
    p.add_argument("--srg", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    require(args.output.suffix == ".json" and not args.output.exists(),
            "write-once JSON evidence output required")
    report = audit(args.server, args.srg, args.javap)
    raw = canonical(report).encode("utf8")
    require(0 < len(raw) <= MAX_REPORT_BYTES, "report exceeds bounded output")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    print("NBT_TAG_WRITER_REPORT_SHA256", hashlib.sha256(raw).hexdigest())
    print("NBT_TAG_WRITER_REPORT_BYTES", len(raw))
    for row in report["classes"]:
        print("CLASS", row["owner"], row["source_archive"], row["class_sha256"],
              "declared", row["declared_method_count"])
        for m in row["selected_methods"]:
            d = m["declaration"]
            print("METHOD", row["owner"], d["name"], d["descriptor"],
                  d["code_sha256"], m["instruction_sha256"], m["instruction_count"])
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED NOT_MODLAUNCHER")


if __name__ == "__main__":
    main()
