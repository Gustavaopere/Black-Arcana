#!/usr/bin/env python3
"""Read-only JVM audit: SavedData.save/DimensionDataStorage.save → IOUtilities.

Authority: checksum-pinned official NeoForge 21.1.248 --installServer overlay +
Minecraft 1.21.1 SRG library. This is not a ModLauncher-loaded, physical modpack
or durable filesystem observation. No third-party implementation is copied.
"""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from neoforge_211248_custom_data_delegate_probe import choose_archive
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

OWNERS = {
    "storage": "net/minecraft/world/level/storage/DimensionDataStorage",
    "saved_data": "net/minecraft/world/level/saveddata/SavedData",
    "worker": "net/neoforged/neoforge/common/IOUtilities",
}
PINNED = {
    "storage": "6316f03f8ff914c9d7f26fd91359ae98af449f7894e423a2209144e7181e3993",
    "saved_data": "b55a20a77d7f3d4a69c7af79240d6bf14cfa4c7536414a70543030631b265310",
}
SAVE_DESC = {
    "storage": "()V",
    "saved_data": "(Ljava/io/File;Lnet/minecraft/core/HolderLookup$Provider;)V",
}
SAVE_CODE_SHA = {
    "storage": "4d9b55ddd4b2504d1c2eaf7d22331d9aba3e1c8bbfe71aa7bed8891b6ba2ab6b",
    "saved_data": "17391efcb49f300ec019d10d3c6ff49376ce4b821ce2f2823b579955241f44b5",
}
MAX_CLASS_BYTES = 750_000
MAX_CODE_METHODS = 125
MAX_SELECTED = 24
MAX_INSTRUCTIONS = 650
MAX_REPORT = 200_000


def methods_to_inspect(label, methods):
    found = []
    for key in methods:
        name, _ = key
        if label in ("storage", "saved_data"):
            match = name == "save" or name.startswith("lambda$save$")
        else:
            match = (name == "<clinit>" or name == "withIOWorker"
                     or name.startswith("lambda$withIOWorker$"))
        if match:
            found.append(key)
    require(1 <= len(found) <= MAX_SELECTED, "method selection budget exceeded " + label)
    return sorted(found)


def invocation_link(reader: ClassReader, body, expected_offset: int):
    matches = [r for r in body["instructions"] if r["offset"] == expected_offset]
    require(len(matches) == 1 and matches[0]["opcode"] == "invokedynamic",
            "expected save invokedynamic changed")
    call = matches[0]
    matched = re.fullmatch(r"#([0-9]+), 0", call["operand"])
    require(matched is not None, "invokedynamic operand not JVM constant index")
    index = int(matched.group(1))
    require(0 < index < len(reader.pool), "constant pool reference outside range")
    cp = reader.pool[index]
    require(cp is not None and cp[0] == 18,
            "expected CONSTANT_InvokeDynamic tag")
    bootstrap_id, name_type_index = cp[1]
    bootstraps = reader.attributes.get("bootstrap_methods")
    require(isinstance(bootstraps, list) and 1 <= len(bootstraps) <= 80,
            "class BootstrapMethods not bounded/present")
    require(0 <= bootstrap_id < len(bootstraps), "bootstrap index out of range")
    typed = reader.resolve(name_type_index)
    require(typed[0] == 12, "dynamic NameAndType tag mismatch")
    entry = bootstraps[bootstrap_id]
    mh = entry["handle"]
    require(mh["reference_kind"] == 6 and
            mh["reference"][1] == "java/lang/invoke/LambdaMetafactory"
            and mh["reference"][2][1] == "metafactory",
            "savedata dispatcher bootstrap is not LambdaMetafactory")
    local = []
    for arg in entry["arguments"]:
        if not isinstance(arg, dict) or "reference" not in arg:
            continue
        ref = arg["reference"]
        if not isinstance(ref, list) or len(ref) != 3:
            continue
        if ref[1] == reader.name:
            name, desc = ref[2][1], ref[2][2]
            declared = [m for m in reader.methods
                        if m["name"] == name and m["descriptor"] == desc
                        and "code_sha256" in m]
            require(len(declared) == 1, "bootstrap implementation unresolved")
            local.append({"name": name, "descriptor": desc,
                          "handle": arg, "code_sha256": declared[0]["code_sha256"]})
    require(len(local) == 1, "expected one explicitly linked local save adapter")
    return {
        "offset": expected_offset,
        "operand": call["operand"],
        "cp_index": index,
        "bootstrap_index": bootstrap_id,
        "type": typed,
        "entry": entry,
        "linked_local": local[0],
        "bootstrap_table_sha256": digest(canonical(bootstraps).encode("utf8")),
        "bootstrap_table_count": len(bootstraps),
    }


def locate_worker_library(libraries: Path):
    """Find the NeoForge-owned IO helper in the exact official installed libraries."""
    require(libraries.is_dir(), "NeoForge --installServer libraries root missing")
    home = libraries / "net/neoforged/neoforge/21.1.248"
    require(home.is_dir(), "exact versioned NeoForge library directory missing")
    jars = sorted(home.glob("*.jar"))
    require(1 <= len(jars) <= 16, "unbounded versioned NeoForge library candidates")
    candidates = []
    target = OWNERS["worker"] + ".class"
    for jar in jars:
        require(jar.is_file() and jar.stat().st_size <= 90_000_000,
                "unbounded official NeoForge library")
        with ZipFile(jar) as z:
            names = z.namelist()
            require(len(names) == len(set(names)), "duplicate NeoForge library entries")
            if target in names:
                raw = z.read(target)
                sha = hashlib.sha256(jar.read_bytes()).hexdigest()
                relative = jar.relative_to(libraries).as_posix()
                candidates.append((jar, raw, sha, jar.stat().st_size, relative))
    require(len(candidates) == 1, "IOUtilities owner not uniquely located in versioned official installed NeoForge libraries")
    return candidates[0]


def inspect(server, srg, libraries, javap):
    distribution = verify_distribution(server, srg)
    with ZipFile(server) as overlay, ZipFile(srg) as vanilla:
        ov, mc = overlay.namelist(), vanilla.namelist()
        require(len(ov) == len(set(ov)) and len(mc) == len(set(mc)),
                "duplicate official archive entries")
        found = {}
        for label, owner in OWNERS.items():
            if label == "worker":
                continue
            path = owner + ".class"
            archive = choose_archive(path, set(ov), set(mc))
            require(archive in ("NEOFORGE_OVERLAY", "INSTALLED_MINECRAFT_SRG"),
                    "engine owner absent " + owner)
            raw = (overlay if archive == "NEOFORGE_OVERLAY" else vanilla).read(path)
            require(64 <= len(raw) <= MAX_CLASS_BYTES and raw[:4] == b"\xca\xfe\xba\xbe",
                    "malformed/oversize classfile " + owner)
            found[label] = (owner, raw, archive, None, None)
    worker_jar, worker_raw, worker_sha, worker_bytes, worker_path = locate_worker_library(libraries)
    require(64 <= len(worker_raw) <= MAX_CLASS_BYTES and
            worker_raw[:4] == b"\xca\xfe\xba\xbe", "malformed IOUtilities classfile")
    found["worker"] = (OWNERS["worker"], worker_raw, "NEOFORGE_211248_INSTALLED_LIBRARY",
                       worker_jar, {"sha256": worker_sha, "bytes": worker_bytes,
                                    "relative_path": worker_path})
    classes = {}
    cp = str(server) + ":" + str(srg)
    for label, (owner, raw, archive, worker_src, archive_metadata) in found.items():
        reader = ClassReader(raw)
        require(reader.name == owner and reader.major == 65,
                "unexpected JVM owner or major")
        require(len(reader.methods) <= MAX_CODE_METHODS,
                "owner method roster outside bounded discovery")
        if label in PINNED:
            require(digest(raw) == PINNED[label],
                    "preaudited engine class hash drift")
        classpath = (str(worker_src) + ":" + cp) if worker_src is not None else cp
        parsed = disassemble(classpath, javap, owner)
        selected = methods_to_inspect(label, parsed)
        bodies = []
        non_executable_declarations = []
        for key in selected:
            declarations = [m for m in reader.methods
                            if (m["name"], m["descriptor"]) == key]
            require(len(declarations) == 1,
                    "selected save/worker JVM declaration not unique")
            declaration = declarations[0]
            if "code_sha256" not in declaration:
                require(not parsed[key] and (declaration["access"] & (0x0400 | 0x0100)),
                        "missing Code with unexpected executable method")
                non_executable_declarations.append(declaration)
                continue
            item = summarize(reader, key, parsed[key])
            require(1 <= item["instruction_count"] <= MAX_INSTRUCTIONS,
                    "unbounded JVM instruction roster")
            bodies.append(item)
        if label in ("storage", "saved_data"):
            save = [x for x in bodies
                    if (x["declaration"]["name"], x["declaration"]["descriptor"]) ==
                    ("save", SAVE_DESC[label])]
            require(len(save) == 1, "expected save boundary missing")
            require(save[0]["declaration"]["code_sha256"] == SAVE_CODE_SHA[label],
                    "expected exact engine save method code changed")
            site_offset = 5 if label == "storage" else 49
            site = invocation_link(reader, save[0], site_offset)
            require(any(
                x["declaration"]["name"] == site["linked_local"]["name"] and
                x["declaration"]["descriptor"] == site["linked_local"]["descriptor"] and
                x["declaration"]["code_sha256"] == site["linked_local"]["code_sha256"]
                for x in bodies), "linked save lambda not among selected executables")
        else:
            site = None
            require(any(x["declaration"]["name"] == "withIOWorker"
                        for x in bodies), "IO worker entrypoint absent")
        classes[label] = {
            "owner": owner, "source_archive": archive,
            "class_sha256": digest(raw),
            "class_major": reader.major,
            "declared_method_count": len(reader.methods),
            "archive_metadata": archive_metadata,
            "fields": reader.fields,
            "selected_methods": bodies,
            "non_executable_declarations": non_executable_declarations,
            "save_lambda_bootstrap": site,
        }
    return {
        "schema_version": 1,
        "scope": "NEOFORGE_211248_SAVEDDATA_WRITE_LAMBDA_IOWORKER_DISTRIBUTED_ONLY",
        "engine": distribution,
        "classes": classes,
        "modlauncher_loaded": "NOT_OBSERVED",
        "installed_modpack_parity": "NOT_VERIFIED",
        "io_completion_durability": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED",
        "mutation": "NO_MUTATION",
        "provider_universe_closed": False,
        "semantic_magic_roots_delta": 0,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server", type=Path, required=True)
    p.add_argument("--srg", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--libraries", type=Path, required=True,
                   help="official --installServer libraries root")
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    require(a.output.suffix == ".json" and not a.output.exists(),
            "write-once read-only report required")
    report = inspect(a.server, a.srg, a.libraries, a.javap)
    payload = canonical(report).encode("utf8")
    require(0 < len(payload) <= MAX_REPORT, "bounded evidence report too large")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes(payload)
    print("WRITE_CHAIN_REPORT_SHA256", hashlib.sha256(payload).hexdigest())
    for label, row in report["classes"].items():
        print("CLASS", label, row["source_archive"], row["class_sha256"],
              "methods", len(row["selected_methods"]),
              "library", row["archive_metadata"])
        for meth in row["selected_methods"]:
            print("METHOD", label, meth["declaration"]["name"],
                  meth["declaration"]["descriptor"],
                  meth["declaration"]["code_sha256"],
                  meth["instruction_sha256"])
        if row["save_lambda_bootstrap"] is not None:
            link = row["save_lambda_bootstrap"]
            print("BOOTSTRAP", label, link["offset"], link["cp_index"],
                  link["bootstrap_index"], link["linked_local"]["name"])
    print("NOT_LOADED_RUNTIME NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    main()
