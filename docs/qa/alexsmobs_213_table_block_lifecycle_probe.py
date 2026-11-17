#!/usr/bin/env python3
"""SHA-exact, read-only Alex's Mobs 2.1.13 Transmutation Table block/menu lifecycle.

Inspects native owner dispatch, menu/session guards, tile change signals and
cross-class candidate references. Discovery/bytecode == NOT physical QA or
security certification. All external implementation remains provider-owned.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import javap, parse_methods, sha_file
from alexsmobs_213_transmutation_c2s_probe import (
    BASE, MENU, TILE, SHA1, SHA256, SIZE, fingerprint, item,
    method_name, require,
)

BLOCK = BASE + "block/BlockTransmutationTable.class"
INPUT_CONTAINER = BASE + "inventory/MenuTransmutationTable$1.class"
INPUT_SLOT = BASE + "inventory/MenuTransmutationTable$2.class"
TARGETS = (BLOCK, MENU, TILE, INPUT_CONTAINER, INPUT_SLOT)
SCOPE = "SHA_EXACT_ALEXSMOBS_213_BLOCK_MENU_LIFECYCLE_READONLY"
SYMBOLS = re.compile(
    r"(?i:Transmut|BlockEntity|ContainerLevelAccess|stillValid|"
    r"openMenu|MenuProvider|NetworkHooks|ServerPlayer|"
    r"getBlockEntity|MenuTransmutationTable|BlockTransmutationTable|"
    r"getTicker|tick|Player|BlockPos|Level|isClientSide|setChanged|"
    r"sendBlockUpdated|updateNeighbors|drop|remove|destroy|"
    r"EntityBlock|BlockState|Chunk|SimpleContainer|Slot|"
    r"ItemStack|NBT|saveAdditional|loadAdditional|setItem|"
    r"UUID|rerollPlayerUUID|setRerollPlayerUUID|"
    r"sendTo|sendPacket|MessageUpdate|DataComponents|BlockHitResult|"
    r"InteractionResult|ClipContext|register|AMMenuRegistry)"
)
INVOKES = ("invoke", "getfield", "putfield", "getstatic", "putstatic",
           "ldc", "new", "instanceof", "checkcast")
MAX_REPORT_BYTES = 275000
MAX_INSTRUCTIONS = 350
MAX_REFS = 95
MAX_BRANCHES = 70
MAX_CANDIDATES = 100
MENU_NAMES = {"MenuTransmutationTable", "stillValid", "slotsChanged",
              "clickMenuButton", "transmute", "removed",
              "lambda$removed$0", "quickMoveStack"}
TILE_NAMES = {"TileEntityTransmutationTable", "commonTick", "tick",
              "randomizeResults", "rollPossiblity", "hasPossibilities",
              "getPossibility", "postTransmute", "loadAdditional",
              "saveAdditional", "setRerollPlayerUUID"}


def choose(path, roster):
    if path == BLOCK:
        return [m for m in roster if m["instructions"]]
    if path == MENU:
        return [m for m in roster
                if method_name(m) in MENU_NAMES and m["instructions"]]
    if path == TILE:
        return [m for m in roster
                if method_name(m) in TILE_NAMES and m["instructions"]]
    return [m for m in roster if m["instructions"]]


def project(method):
    instructions = method["instructions"]
    require(1 <= len(instructions) <= MAX_INSTRUCTIONS,
            "unexpected native method size: " + method_name(method))
    positions = [r["offset"] for r in instructions]
    require(positions == sorted(set(positions)),
            "duplicate/out-of-order bytecode offsets")
    pos = set(positions)
    refs = []
    jumps = []
    for i, r in enumerate(instructions):
        if r["opcode"].startswith(("if", "goto")):
            val = r["operand"].split(" ", 1)[0]
            require(re.fullmatch(r"-?\d+", val) is not None,
                    "unparseable JVM branch offset")
            dst = int(val)
            require(dst in pos, "branch outside native method")
            jumps.append({"site": r["offset"], "opcode": r["opcode"],
                          "target": dst,
                          "prior": item(instructions[i - 1]) if i else None})
        if r["opcode"].startswith(INVOKES) and SYMBOLS.search(r["symbol"]):
            refs.append({
                "site": item(r),
                "prior": item(instructions[i-1]) if i else None,
                "next": item(instructions[i+1]) if i+1 < len(instructions)
                        else None,
            })
    require(len(jumps) <= MAX_BRANCHES and len(refs) <= MAX_REFS,
            "unbounded operator evidence for native method")
    return {
        "name": method_name(method),
        "descriptor": method["descriptor"],
        "body_sha256": fingerprint(method),
        "instruction_count": len(instructions),
        "branches": jumps,
        "relevant_refs": refs,
        "native_set_changed_calls": [
            item(r) for r in instructions
            if r["opcode"].startswith("invoke")
            and "setChanged:" in r["symbol"]
        ],
        "native_block_updates": [
            item(r) for r in instructions
            if r["opcode"].startswith("invoke")
            and "sendBlockUpdated:" in r["symbol"]
        ],
        "open_menu_calls": [
            item(r) for r in instructions
            if r["opcode"].startswith("invoke")
            and ("openMenu:" in r["symbol"]
                 or "openScreen:" in r["symbol"])
        ],
        "direct_validity_calls": [
            item(r) for r in instructions
            if r["opcode"].startswith("invoke")
            and "stillValid:" in r["symbol"]
        ],
    }


def candidates(archive):
    paths = sorted(p for p in archive.namelist()
                   if p.startswith(BASE) and p.endswith(".class"))
    require(1100 <= len(paths) <= 1700, "unexpected publisher class universe")
    discoveries = []
    for path in paths:
        raw = archive.read(path)
        if b"BlockTransmutationTable" not in raw and (
            b"TileEntityTransmutationTable" not in raw
            and b"MenuTransmutationTable" not in raw
        ):
            continue
        discoveries.append({
            "class_path": path,
            "class_sha256": hashlib.sha256(raw).hexdigest(),
            "has_block_name": b"BlockTransmutationTable" in raw,
            "has_tile_name": b"TileEntityTransmutationTable" in raw,
            "has_menu_name": b"MenuTransmutationTable" in raw,
        })
    require(3 <= len(discoveries) <= MAX_CANDIDATES,
            "missing/excessive binary table consumer candidates")
    return discoveries, len(paths)


def sealed_classfiles(old):
    require(old["artifact"]["sha1"] == SHA1 and
            old["artifact"]["sha256"] == SHA256 and
            old["artifact"]["size_bytes"] == SIZE,
            "prior publisher exactness mismatch")
    return {x["class_path"]: x["class_sha256"]
            for x in old["observations"]["classes"]}


def audit(jar: Path, javap_bin: str, predecessor: dict) -> dict:
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher JAR identity drift")
    old = sealed_classfiles(predecessor)
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP entries")
        require(all(p in names for p in TARGETS),
                "native table block/menu/slot/tile class missing")
        digests = {}
        for path in TARGETS:
            data = arc.read(path)
            require(data[:4] == b"\xca\xfe\xba\xbe" and
                    int.from_bytes(data[6:8], "big") == 65,
                    "invalid Java 21 classfile")
            digests[path] = hashlib.sha256(data).hexdigest()
            if path in old:
                require(digests[path] == old[path],
                        "sealed native classfile fingerprint drift")
        discovered, class_universe = candidates(arc)
    classes = []
    for path in TARGETS:
        disassembled = javap(
            javap_bin, jar, path.removesuffix(".class").replace("/", ".")
        )
        roster = parse_methods(disassembled)
        require(1 <= len(roster) <= 80,
                "unexpected class method count " + path)
        selected = choose(path, roster)
        require(1 <= len(selected) <= 42,
                "missing or excessive owner methods " + path)
        classes.append({
            "class_path": path,
            "class_sha256": digests[path],
            "method_count": len(roster),
            "method_roster": [
                {"name": method_name(m), "descriptor": m["descriptor"],
                 "instructions": len(m["instructions"])} for m in roster
            ],
            "selected_methods": [project(m) for m in selected],
        })
    bypath = {c["class_path"]: c for c in classes}
    block_methods = bypath[BLOCK]["selected_methods"]
    menu_methods = bypath[MENU]["selected_methods"]
    tile_methods = bypath[TILE]["selected_methods"]
    signals = {
        "block_direct_menu_open_calls": sum(
            len(x["open_menu_calls"]) for x in block_methods
        ),
        "block_direct_dirty_calls": sum(
            len(x["native_set_changed_calls"]) for x in block_methods
        ),
        "tile_direct_dirty_calls_selected": sum(
            len(x["native_set_changed_calls"]) for x in tile_methods
        ),
        "tile_direct_sync_calls_selected": sum(
            len(x["native_block_updates"]) for x in tile_methods
        ),
        "menu_direct_validity_calls_selected": sum(
            len(x["direct_validity_calls"]) for x in menu_methods
        ),
        "slot_container_set_changed": sum(
            len(x["native_set_changed_calls"])
            for x in bypath[INPUT_CONTAINER]["selected_methods"]
        ),
    }
    report = {
        "schema_version": 1,
        "scope": SCOPE,
        "artifact": {
            "filename": "alexsmobs-2.1.13-neoforge+1.21.1.jar",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
        },
        "prior_certificate": "EXACT-TRANSMUTATION-C2S-2.1.13.json",
        "provider_classes_total": class_universe,
        "classes": classes,
        "binary_consumer_candidates": discovered,
        "static_signals": signals,
        "limitations": {
            "physical_modlist_current": "NOT_RECONFIRMED",
            "real_block_use_and_menu_open": "NOT_TESTED",
            "player_table_session_ownership": "NOT_VERIFIED",
            "menu_validity_runtime_enforcement": "NOT_VERIFIED",
            "indirect_blockentity_dirty": "NOT_VERIFIED",
            "automatic_container_chunk_persistence": "NOT_TESTED",
            "cross_dimension_and_unload_recovery": "NOT_TESTED",
            "full_consumer_graph": "NOT_CERTIFIED",
            "static_perk_contract": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
        },
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf-8"))
            <= MAX_REPORT_BYTES, "unbounded clean-room JVM report")
    return report


def verify_lock(report, lock):
    payload = (json.dumps(report, indent=2, ensure_ascii=False)
               + "\n").encode("utf-8")
    require(lock["report_sha256"] == hashlib.sha256(payload).hexdigest(),
            "native table lifecycle report digest drift")
    require(lock["report_bytes"] == len(payload),
            "native table lifecycle report size drift")
    require(lock["publisher_sha256"] == report["artifact"]["sha256"],
            "publisher identity changed")
    require(lock["class_count"] == len(report["classes"]),
            "owner method cohort changed")
    require(lock["candidate_count"] == len(report["binary_consumer_candidates"]),
            "consumer cohort changed")
    require(lock["static_signals"] == report["static_signals"],
            "native dirty/open/validity signals changed")
    require(lock["mutation"] == "NO_MUTATION" and
            report["limitations"]["mutation"] == "NO_MUTATION",
            "mutating contract must fail closed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--predecessor", required=True, type=Path)
    parser.add_argument("--lock", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    previous = json.loads(args.predecessor.read_text(encoding="utf-8"))
    report = audit(args.jar, args.javap, previous)
    if args.lock:
        verify_lock(report, json.loads(args.lock.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "result": "SEALED" if args.lock else "UNSEALED_DISCOVERY",
        "owners": len(report["classes"]),
        "binary_candidates": len(report["binary_consumer_candidates"]),
        "signals": report["static_signals"],
        "mutation": "NO_MUTATION",
    }))


if __name__ == "__main__":
    main()
