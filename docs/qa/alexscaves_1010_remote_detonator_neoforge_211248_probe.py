#!/usr/bin/env python3
"""Bounded read-only NeoForge 21.1.248 distributed ticket/ignition ABI discovery.

This uses the official installed server overlay and SRG library. It never
launches Minecraft, transforms classes, modifies tickets or certifies hooks.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution
from neoforge_211248_custom_data_delegate_probe import choose_archive

CHUNK = "net/neoforged/neoforge/common/world/chunk/"
REQUIRED = {
    CHUNK + "TicketController": {"<init>", "forceChunk"},
    CHUNK + "TicketHelper": {"getEntityTickets", "getBlockTickets", "removeAllTickets"},
    CHUNK + "RegisterTicketControllersEvent": {"register"},
    "net/neoforged/neoforge/common/extensions/IBlockStateExtension": {"onCaughtFire"},
    "net/neoforged/neoforge/common/extensions/IBlockExtension": {"onCaughtFire"},
    "net/minecraft/world/level/block/TntBlock": {"onCaughtFire"},
}
OPTIONAL = {
    "net/minecraft/world/level/block/state/BlockBehaviour$BlockStateBase": {"onCaughtFire", "getBlock"},
    "net/minecraft/world/level/block/state/BlockState": {"onCaughtFire"},
}
CANDIDATE_NAMES = {"ForcedChunkManager", "TicketController", "TicketHelper",
                   "LoadingValidationCallback", "RegisterTicketControllersEvent"}
EXTRA_METHODS = {"forceChunk", "removeAllTickets", "getEntityTickets", "getBlockTickets",
                 "register", "validateTickets", "reinstatePersistentChunks", "loadForcedChunks",
                 "saveForcedChunks", "getId", "getCallback", "getValidationCallback"}
LIMITS = {
    "runtime_loaded_bytes": "NOT_OBSERVED", "actual_ticket_acceptance": "NOT_VERIFIED",
    "actual_ticket_release": "NOT_VERIFIED", "effective_datapack_tag": "NOT_VERIFIED",
    "actual_block_ignition": "NOT_VERIFIED", "world_safety": "BLOCKED",
    "static_contract": "NOT_CERTIFIED", "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
    "provider_universe_closed": False, "semantic_magic_roots_delta": 0,
}


def candidates(paths):
    return sorted(p[:-6] for p in paths if p.startswith(CHUNK) and p.endswith(".class")
                  and p.rsplit("/", 1)[-1][:-6] in CANDIDATE_NAMES)


def inspect(server, srg, javap, output):
    identity = verify_distribution(server, srg)
    require(not output.exists(), "write-once report required")
    with ZipFile(server) as overlay, ZipFile(srg) as vanilla:
        a, b = overlay.namelist(), vanilla.namelist()
        require(len(a) == len(set(a)) and len(b) == len(set(b)), "duplicate archive entries")
        av, bv = set(a), set(b)
        discovered = candidates(av | bv)
        owners = set(REQUIRED) | set(OPTIONAL) | set(discovered)
        require(len(owners) <= 20, "bounded owner roster")
        result = {}
        for owner in sorted(owners):
            entry = owner + ".class"
            source = choose_archive(entry, av, bv)
            if source not in {"NEOFORGE_OVERLAY", "INSTALLED_MINECRAFT_SRG"}:
                require(owner not in REQUIRED, "required class absent: " + owner)
                result[owner] = {"source": source, "present": False}
                continue
            raw = (overlay if source == "NEOFORGE_OVERLAY" else vanilla).read(entry)
            reader = ClassReader(raw)
            require(reader.name == owner and reader.major == 65, "class identity drift")
            names = set(REQUIRED.get(owner, ())) | set(OPTIONAL.get(owner, ()))
            if owner in discovered:
                names |= EXTRA_METHODS
            declarations = [m for m in reader.methods if m["name"] in names]
            require(REQUIRED.get(owner, set()).issubset({m["name"] for m in declarations}),
                    "required declaration absent: " + owner)
            parsed = disassemble(str(server)+":"+str(srg), javap, owner)
            selected = []
            for d in declarations:
                key = (d["name"], d["descriptor"])
                if "code_sha256" not in d:
                    selected.append({"name": key[0], "descriptor": key[1], "executable": False})
                    continue
                require(key in parsed and bool(parsed[key]), "executable body absent")
                body = parsed[key]
                item = analyze(reader, body, d)
                item["instruction_sha256"] = summarize(reader, key, body)["instruction_sha256"]
                item["executable"] = True
                item["branch_operands"] = [
                    {"offset": p, "opcode": op, "operand": arg, "symbol": sym}
                    for p, (op, arg, sym) in sorted(body.items())
                    if op.startswith(("iconst_", "fconst_", "dconst_", "lconst_"))
                    or op in {"bipush", "sipush", "aconst_null"}
                    or (op.startswith("ldc") and sym.startswith(("int ", "float ", "double ", "long ")))
                ]
                selected.append(item)
            result[owner] = {"source": source, "present": True, "class_sha256": digest(raw),
                             "parent": reader.parent, "interfaces": reader.interfaces,
                             "declared_method_names": sorted({m["name"] for m in reader.methods}),
                             "selected": selected}
    report = {"schema_version": 1, "scope": "NEOFORGE_211248_DISTRIBUTED_TICKET_IGNITION_DISCOVERY_ONLY",
              "artifact": identity, "chunk_class_candidates": discovered, "classes": result, "limits": LIMITS}
    payload = canonical(report).encode()
    require(len(payload) <= 700000, "report size budget")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(payload)
    print("ENGINE_REPORT_SHA256", digest(payload), "BYTES", len(payload))
    print("CHUNK_CANDIDATES", json.dumps(discovered))
    for owner, row in result.items():
        print("OWNER", owner, row.get("source"), row.get("class_sha256"))
        for m in row.get("selected", []):
            print("METHOD", owner, m["name"], m["descriptor"], m.get("code_sha256"), m.get("instruction_count"))
            if m["executable"]:
                print("SEMANTIC", json.dumps({"owner": owner, **m}, sort_keys=True))
    print("DISCOVERY_ONLY NO_MUTATION WORLD_SAFETY_BLOCKED")


def self_test():
    actual = candidates({CHUNK+"TicketController.class", CHUNK+"TicketHelper.class",
                         CHUNK+"TicketController$1.class", "foreign/TicketController.class",
                         CHUNK+"Other.class", CHUNK+"ForcedChunkManager.class"})
    require(actual == [CHUNK+"ForcedChunkManager", CHUNK+"TicketController", CHUNK+"TicketHelper"],
            "candidate namespace filter")
    require(LIMITS["mutation"] == "NO_MUTATION" and LIMITS["world_safety"] == "BLOCKED",
            "discovery policy drift")
    print("PASS: namespace and discovery policy checks")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server", type=Path)
    p.add_argument("--srg", type=Path)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
    else:
        require(all((args.server, args.srg, args.output)), "engine paths and report required")
        inspect(args.server, args.srg, args.javap, args.output)
