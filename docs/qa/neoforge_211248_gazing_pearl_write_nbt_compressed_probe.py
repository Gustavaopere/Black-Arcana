#!/usr/bin/env python3
"""Bounded read-only SHA-exact NeoForge 21.1.248 writeNbtCompressed boundary.

Inspect only the official versioned universal JAR and the exact official
--installServer overlay/SRG libraries. This does NOT exercise the game, and
does not establish durable I/O, a transformed ModLauncher class or safe hooks.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from neoforge_211248_gazing_pearl_ioworker_lambda_probe import locate_worker_library
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

OWNER = "net/neoforged/neoforge/common/IOUtilities"
PINNED_JAR_SHA256 = "90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5"
PINNED_CLASS_SHA256 = "3c4cfda19b620562486ca18af3d7c095c94a54c31d1028bf8e5d9860952e115a"
PINNED_WITH_IO_WORKER_CODE = "f160c3418e9acf857b202582af5a798a0f2dfa22a2bd069b2c49e4154553bf42"
MAX_DECLARED = 95
MAX_SELECTED = 24
MAX_INSTRUCTIONS = 850
MAX_BYTES = 190_000


def audit(server: Path, srg: Path, libraries: Path, javap: str) -> dict:
    engine = verify_distribution(server, srg)
    jar, raw, sha, jar_size, relative = locate_worker_library(libraries)
    require(sha == PINNED_JAR_SHA256 and jar_size == 3551268,
            "official 21.1.248 universal JAR SHA or size drift")
    require(relative == "net/neoforged/neoforge/21.1.248/neoforge-21.1.248-universal.jar",
            "versioned exact worker library path drift")
    require(digest(raw) == PINNED_CLASS_SHA256, "IOUtilities.class SHA drift")
    reader = ClassReader(raw)
    require(reader.major == 65 and reader.name == OWNER, "JVM owner/version drift")
    require(len(reader.methods) <= MAX_DECLARED, "unbounded IOUtilities method roster")
    parsed = disassemble(str(jar) + ":" + str(server) + ":" + str(srg),
                         javap, OWNER)
    declared = {(m["name"], m["descriptor"]): m for m in reader.methods}
    require(len(declared) == len(reader.methods), "duplicate JVM method declaration")
    require(set(parsed) == set(declared), "missing unexpected JVM disassembly declaration")

    # Discovery, not a guess about the disk semantics: selected methods are
    # exact calls plus closely named local helpers, bounded against JAR drift.
    names = {"writeNbtCompressed", "withIOWorker", "writeNbt"}
    selected = [
        key for key in sorted(parsed)
        if key[0] in names or key[0].startswith("lambda$writeNbtCompressed$")
    ]
    require(2 <= len(selected) <= MAX_SELECTED, "write boundary method roster drift")
    result = []
    non_executable = []
    for key in selected:
        m = declared[key]
        if "code_sha256" not in m:
            require(not parsed[key] and m["access"] & (0x0100 | 0x0400),
                    "nonexecutable method missing native or abstract flag")
            non_executable.append(m)
            continue
        body = summarize(reader, key, parsed[key])
        require(0 < body["instruction_count"] <= MAX_INSTRUCTIONS,
                "method bytecode budget exceeded")
        result.append(body)
    write_bodies = [m for m in result
                    if m["declaration"]["name"] == "writeNbtCompressed"]
    worker_bodies = [m for m in result
                     if m["declaration"]["name"] == "withIOWorker"]
    require(len(write_bodies) >= 1 and len(worker_bodies) == 1,
            "required write+worker bodies absent")
    require(worker_bodies[0]["declaration"]["code_sha256"] ==
            PINNED_WITH_IO_WORKER_CODE, "previously sealed worker changed")
    roster = [
        {"name": m["name"], "descriptor": m["descriptor"], "access": m["access"],
         "code_sha256": m.get("code_sha256")}
        for m in reader.methods
    ]
    return {
        "schema_version": 1,
        "scope": "NEOFORGE_211248_IOUTILITIES_WRITE_NBT_COMPRESSED_DISTRIBUTED_ONLY",
        "artifact": engine,
        "universal_library": {"path": relative, "bytes": jar_size,
                              "sha256": sha, "worker_class_sha256": digest(raw)},
        "owner": OWNER,
        "owner_major": reader.major,
        "method_roster": roster,
        "selected_methods": result,
        "non_executable_declarations": non_executable,
        "modlauncher_class": "NOT_OBSERVED",
        "installed_modpack_parity": "NOT_VERIFIED",
        "actual_file_io": "NOT_TESTED",
        "actual_error_recovery": "NOT_TESTED",
        "durability_after_restart": "NOT_TESTED",
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
    p.add_argument("--libraries", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    require(a.output.suffix == ".json" and not a.output.exists(),
            "write-once report path required")
    report = audit(a.server, a.srg, a.libraries, a.javap)
    payload = canonical(report).encode("utf8")
    require(len(payload) < MAX_BYTES, "evidence budget exceeded")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes(payload)
    print("WRITE_NBT_REPORT_SHA256", hashlib.sha256(payload).hexdigest())
    print("WORKER_CLASS_SHA256", report["universal_library"]["worker_class_sha256"])
    for m in report["selected_methods"]:
        d = m["declaration"]
        print("METHOD", d["name"], d["descriptor"], d["code_sha256"],
              m["instruction_sha256"], m["instruction_count"])
    print("UNSUPPORTED: LIVE_DISK_COMPLETION LIVE_MODLAUNCHER CLASS_PARITY")
    print("NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    main()
