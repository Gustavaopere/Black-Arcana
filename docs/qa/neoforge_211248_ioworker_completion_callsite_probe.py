#!/usr/bin/env python3
"""Read-only census of exact waitUntilIOWorkerComplete JVM callsites.

This scans only three SHA-pinned, officially distributed NeoForge 21.1.248
server/universal and Minecraft SRG JARs. A CP reference is only a candidate;
we confirm direct invokes by instruction CP-index resolution. No live shutdown,
physical save, ModLauncher transform or filesystem claim is established.
"""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

OWNER = "net/neoforged/neoforge/common/IOUtilities"
METHOD = "waitUntilIOWorkerComplete"
SIGNATURE = "()V"
SCOPE = "NEOFORGE_211248_IOWORKER_COMPLETION_CALLSITE_CENSUS_DISTRIBUTED_ONLY"
SHA_UNIVERSAL = "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"
BYTES_UNIVERSAL = 3551268
MAX_CLASSES = 35000
MAX_CLASS_BYTES = 650000
MAX_CANDIDATES = 120
MAX_BODY_INSTRUCTIONS = 2500
MAX_REPORT_BYTES = 400000


def target_reference(reader: ClassReader, pool_index: int) -> bool:
    entry = reader.pool[pool_index]
    if entry is None or entry[0] not in (10, 11):
        return False
    tag, owner, signature = reader.resolve(pool_index)
    return owner == OWNER and signature[1:] == [METHOD, SIGNATURE]


def inspect_jar(path: Path, source: str, javap: str):
    members = []
    candidates = []
    non_direct_handles = []
    with ZipFile(path) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP member")
        cls_names = sorted(x for x in names if x.endswith(".class") and not x.startswith("META-INF/versions/"))
        require(len(cls_names) <= MAX_CLASSES, "class budget exceeded")
        for filename in cls_names:
            raw = z.read(filename)
            require(64 < len(raw) <= MAX_CLASS_BYTES and raw[:4] == b"\xca\xfe\xba\xbe", "classfile malformed or oversized: " + filename)
            reader = ClassReader(raw)
            require(reader.name + ".class" == filename, "class owner/path drift " + filename)
            refs = [i for i in range(1, len(reader.pool)) if target_reference(reader, i)]
            # Handles may refer to a target without making an immediately executed call.
            handles = [i for i, e in enumerate(reader.pool) if e and e[0] == 15 and e[1][1] in refs]
            if refs or handles:
                candidates.append({"owner": reader.name, "class_sha256": digest(raw),
                                   "refs": refs, "handle_indices": handles})
            members.append(filename)
    require(len(candidates) <= MAX_CANDIDATES, "candidate class budget exceeded")
    sites = []
    for candidate in candidates:
        owner = candidate["owner"]
        with ZipFile(path) as z:
            reader = ClassReader(z.read(owner + ".class"))
        parsed = disassemble(str(path), javap, owner)
        declared = {(m["name"], m["descriptor"]): m for m in reader.methods}
        require(set(parsed) == set(declared), "javap/declarations drift " + owner)
        for key, body in sorted(parsed.items()):
            matching = []
            for offset, (opcode, operand, symbol) in sorted(body.items()):
                if not opcode.startswith("invoke") or opcode == "invokedynamic":
                    continue
                match = re.match(r"#(\d+)(?:\s|$)", operand)
                if match and int(match.group(1)) in candidate["refs"]:
                    matching.append({"offset": offset, "opcode": opcode,
                                     "cp_index": int(match.group(1)), "symbol": symbol})
            if matching:
                require(len(body) <= MAX_BODY_INSTRUCTIONS, "callsite method body exceeds budget")
                row = summarize(reader, key, body)
                sites.append({"source_archive": source, "owner": owner,
                              "class_sha256": candidate["class_sha256"],
                              "method": row, "callsites": matching})
        if candidate["handle_indices"]:
            non_direct_handles.append({"owner": owner, "class_sha256": candidate["class_sha256"],
                                       "cp_method_handle_indices": candidate["handle_indices"],
                                       "interpretation": "handle present in class constant pool, not an observed invoke"})
    return {"source_archive": source, "jar_sha256": digest(path.read_bytes()),
            "jar_size_bytes": path.stat().st_size,
            "class_entries_scanned": len(members),
            "class_roster_sha256": digest(("\n".join(members) + "\n").encode("utf8")),
            "candidates": candidates,
            "direct_invoke_sites": sites, "method_handles_not_direct_calls": non_direct_handles}


def audit(server: Path, srg: Path, universal: Path, javap: str) -> dict:
    distribution = verify_distribution(server, srg)
    require(universal.stat().st_size == BYTES_UNIVERSAL and digest(universal.read_bytes()) == SHA_UNIVERSAL,
            "exact official NeoForge universal hash/size mismatch")
    archives = []
    for label,jar in (("NEOFORGE_OVERLAY",server), ("INSTALLED_MINECRAFT_SRG",srg), ("NEOFORGE_UNIVERSAL",universal)):
        archives.append(inspect_jar(jar, label, javap))
    return {"schema_version": 1, "scope": SCOPE, "distribution": distribution,
            "target": {"owner": OWNER, "name": METHOD, "descriptor": SIGNATURE},
            "archives": archives,
            "conclusion_boundary": "direct invocations and separate method-handle candidates in three official distributed JARs; no exhaustive modloader/third-party classpath claim",
            "shutdown_execution": "NOT_TESTED", "worker_completion_at_server_stop": "NOT_VERIFIED",
            "modlauncher_classes": "NOT_OBSERVED", "real_disk_durability": "NOT_TESTED",
            "modpack_physical_qa": "NOT_TESTED", "static_contract": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED", "mutation": "NO_MUTATION",
            "provider_universe_closed": False, "semantic_magic_roots_delta": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", type=Path, required=True)
    parser.add_argument("--srg", type=Path, required=True)
    parser.add_argument("--universal", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path, required=True)
    a = parser.parse_args()
    require(a.output.suffix == ".json" and not a.output.exists(), "write-once JSON output path required")
    report = audit(a.server, a.srg, a.universal, a.javap)
    raw = canonical(report).encode("utf8")
    require(0 < len(raw) <= MAX_REPORT_BYTES, "bounded report byte budget exceeded")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes(raw)
    print("IOWORKER_CALLSITE_REPORT_SHA256", hashlib.sha256(raw).hexdigest())
    print("IOWORKER_CALLSITE_REPORT_BYTES",len(raw))
    for arc in report["archives"]:
        print("ARCHIVE",arc["source_archive"],arc["jar_sha256"],arc["class_entries_scanned"],
              "candidates",len(arc["candidates"]),"direct_callsites",sum(len(x["callsites"]) for x in arc["direct_invoke_sites"]))
        for row in arc["direct_invoke_sites"]:
            print("DIRECT",row["owner"],row["method"]["declaration"]["name"],
                  row["method"]["declaration"]["descriptor"],row["method"]["declaration"]["code_sha256"],
                  row["method"]["instruction_sha256"],row["callsites"])
        for row in arc["method_handles_not_direct_calls"]:
            print("HANDLE_ONLY",row["owner"],row["cp_method_handle_indices"])
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    main()
