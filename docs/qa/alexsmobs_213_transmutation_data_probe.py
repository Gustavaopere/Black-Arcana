#!/usr/bin/env python3
"""Alex's Mobs 2.1.13 TransmutationData, NBT and display-network clean-room audit.

Publisher JAR is SHA-exact and historically matched to the physical modlist.
Inspect classfile/bytecode metadata only; never execute provider gameplay code,
reproduce provider implementation or infer safe mutating hooks from callsites.
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
    BASE, MENU, TILE, SHA1, SHA256, SIZE, fingerprint,
    item, method_name, require,
)

DATA = BASE + "misc/TransmutationData.class"
COMPAT = BASE + "misc/AMCompat.class"
DISPLAY = BASE + "message/MessageUpdateTransmutablesToDisplay.class"
DISPLAY_HANDLER = BASE + "message/MessageUpdateTransmutablesToDisplay$Handler.class"
MENU_SLOT1 = BASE + "inventory/MenuTransmutationTable$1.class"
MENU_SLOT2 = BASE + "inventory/MenuTransmutationTable$2.class"

REQUIRED = (DATA, COMPAT, TILE, MENU, DISPLAY)
OPTIONAL = (DISPLAY_HANDLER, MENU_SLOT1, MENU_SLOT2)
PERMITTED = set(REQUIRED + OPTIONAL)
SCOPE = "SHA_EXACT_ALEXSMOBS_213_TRANSMUTATION_DATA_NBT_DISPLAY_READONLY"
OBSERVABLE = re.compile(
    r"(?i:Transmut|weight|Random|loot|ItemStack|CompoundTag|ListTag|UUID|"
    r"AMCompat|Map|HashMap|List|Registry|save|load|NBT|"
    r"sendTo|sendPacket|Packet|MessageUpdate|player|"
    r"BlockEntity|setChanged|markDirty|sendBlockUpdated|"
    r"possible|possibl|count|Integer|Double|Math|Rarity|Tag|"
    r"CompoundTag|FriendlyByteBuf|readInt|writeInt)"
)
OPCODES = ("invoke", "getfield", "putfield", "getstatic",
           "putstatic", "ldc", "new", "checkcast", "instanceof")
LITERALS = ("ldc", "iconst", "bipush", "sipush", "dconst", "fconst", "lconst")
MAX_METHODS = 42
MAX_INSTRUCTIONS = 520
MAX_BRANCHES = 90
MAX_REFS = 100
MAX_LITERALS = 65
MATH_OPERATORS = {"dadd", "dsub", "dmul", "ddiv", "dneg", "dcmpl", "dcmpg", "i2d"}
MAX_REPORT_BYTES = 250_000
MAX_CANDIDATES = 80
AMCOMPAT_RELEVANT = {
    "getInt", "getList", "getCompound", "getUUID",
    "putUUID", "contains", "loadItem", "saveItem", "put",
}
TILE_RELEVANT = {
    "loadAdditional", "saveAdditional", "randomizeResults",
    "rollPossiblity", "postTransmute", "tick",
    "setRerollPlayerUUID",
}
MENU_RELEVANT = {"slotsChanged", "removed", "MenuTransmutationTable"}
EXPECTED_DATA = {
    "fromNBT", "saveAsNBT", "onTransmuteItem",
    "getTotalWeight", "getRandomItem",
}


def selected_methods(path, methods):
    if path == DATA:
        require(2 <= len(methods) <= MAX_METHODS,
                "unbounded TransmutationData method roster")
        names = {method_name(m) for m in methods}
        require(EXPECTED_DATA.issubset(names),
                "TransmutationData API drift: expected state/weighted methods")
        return [m for m in methods if m["instructions"]]
    if path == COMPAT:
        return [m for m in methods if method_name(m) in AMCOMPAT_RELEVANT]
    if path == TILE:
        return [m for m in methods if method_name(m) in TILE_RELEVANT]
    if path == MENU:
        return [m for m in methods if method_name(m) in MENU_RELEVANT]
    if path in (DISPLAY, DISPLAY_HANDLER):
        return [m for m in methods if m["instructions"]]
    if path in (MENU_SLOT1, MENU_SLOT2):
        return [m for m in methods if m["instructions"]]
    raise ValueError("unexpected class path")


def method_projection(method):
    rows = method["instructions"]
    require(1 <= len(rows) <= MAX_INSTRUCTIONS,
            "unbounded selected method bytecode: " + method_name(method))
    offsets = [r["offset"] for r in rows]
    require(offsets == sorted(set(offsets)),
            "nonmonotonic or duplicate JVM bytecode offsets")
    branches, refs, constants, math_ops = [], [], [], []
    for index, row in enumerate(rows):
        op = row["opcode"]
        if op.startswith(("if", "goto")):
            value = row["operand"].split(" ", 1)[0]
            require(re.fullmatch(r"-?\d+", value) is not None,
                    "unparseable JVM branch target")
            target = int(value)
            require(target in set(offsets), "branch target not in method")
            branches.append({"offset": row["offset"],
                             "opcode": op, "target": target})
        if op.startswith(OPCODES) and OBSERVABLE.search(row["symbol"]):
            refs.append({
                "site": item(row),
                "before": item(rows[index - 1]) if index else None,
                "after": item(rows[index + 1])
                         if index + 1 < len(rows) else None,
            })
        if op.startswith(LITERALS):
            constants.append(item(row))
        if op in MATH_OPERATORS:
            math_ops.append({
                "site": item(row),
                "before": item(rows[index - 1]) if index else None,
                "after": item(rows[index + 1])
                         if index + 1 < len(rows) else None,
            })
    require(len(branches) <= MAX_BRANCHES
            and len(refs) <= MAX_REFS
            and len(constants) <= MAX_LITERALS
            and len(math_ops) <= 75,
            "unbounded TransmutationData control/evidence cohort")
    return {
        "name": method_name(method),
        "descriptor": method["descriptor"],
        "instruction_count": len(rows),
        "body_sha256": fingerprint(method),
        "branches": branches,
        "relevant_refs": refs,
        "literal_operators": constants,
        "arithmetic_operators": math_ops,
        "native_set_changed_calls": [
            item(row) for row in rows
            if row["opcode"].startswith("invoke")
            and "setChanged:" in row["symbol"]
        ],
        "native_send_block_updated_calls": [
            item(row) for row in rows
            if row["opcode"].startswith("invoke")
            and "sendBlockUpdated:" in row["symbol"]
        ],
    }


def discover_consumers(archive):
    members = sorted(p for p in archive.namelist()
                     if p.startswith(BASE) and p.endswith(".class"))
    require(1100 <= len(members) <= 1700,
            "unexpected publisher provider class count")
    result = []
    for path in members:
        raw = archive.read(path)
        has_data = b"TransmutationData" in raw
        has_display = b"MessageUpdateTransmutablesToDisplay" in raw
        if has_data or has_display:
            result.append({
                "class_path": path,
                "mentions_transmutation_data": has_data,
                "mentions_display_message": has_display,
                "class_sha256": hashlib.sha256(raw).hexdigest(),
            })
    require(2 <= len(result) <= MAX_CANDIDATES,
            "missing/oversize transmutation consumer discovery")
    return result, len(members)


def prior_hashes(snapshot):
    require(snapshot["artifact"]["sha1"] == SHA1 and
            snapshot["artifact"]["sha256"] == SHA256 and
            snapshot["artifact"]["size_bytes"] == SIZE,
            "predecessor evidence uses another publisher")
    return {r["class_path"]: r["class_sha256"]
            for r in snapshot["observations"]["classes"]}


def audit(jar: Path, javap_bin: str, predecessor: dict) -> dict:
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher SHA-1/SHA-256/size mismatch")
    sealed = prior_hashes(predecessor)
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP member")
        require(all(p in names for p in REQUIRED),
                "missing required transmutation data or network class")
        selected_paths = list(REQUIRED) + [
            p for p in OPTIONAL if p in names
        ]
        digests = {}
        for path in selected_paths:
            raw = archive.read(path)
            require(raw[:4] == b"\xca\xfe\xba\xbe" and
                    int.from_bytes(raw[6:8], "big") == 65,
                    "unexpected JVM classfile version")
            digests[path] = hashlib.sha256(raw).hexdigest()
        for path, expected_sha in sealed.items():
            if path in digests:
                require(digests[path] == expected_sha,
                        "previously certified owner classfile drift")
        consumers, provider_class_count = discover_consumers(archive)
    result = []
    for path in selected_paths:
        methods = parse_methods(
            javap(javap_bin, jar, path[:-6].replace("/", "."))
        )
        # AMCompat is a cross-version compatibility utility with a broader API;
        # selected evidence remains restricted to the named NBT helpers.
        bound = 240 if path == COMPAT else 80
        require(1 <= len(methods) <= bound,
                "unexpected native method roster: " + path +
                " count=" + str(len(methods)))
        chosen = selected_methods(path, methods)
        require(1 <= len(chosen) <= MAX_METHODS,
                "unexpected selected method count")
        result.append({
            "class_path": path,
            "class_sha256": digests[path],
            "native_method_count": len(methods),
            "roster": [
                {"name": method_name(m), "descriptor": m["descriptor"],
                 "bytecode_instructions": len(m["instructions"])}
                for m in methods
            ],
            "selected_methods": [method_projection(m) for m in chosen],
        })
    report = {
        "schema_version": 1,
        "scope": SCOPE,
        "artifact": {
            "filename": "alexsmobs-2.1.13-neoforge+1.21.1.jar",
            "sha1": SHA1, "sha256": SHA256,
            "size_bytes": SIZE,
        },
        "prior_certificate": "EXACT-TRANSMUTATION-C2S-2.1.13.json",
        "provider_class_count": provider_class_count,
        "classes": result,
        "candidate_consumer_population": consumers,
        "limitations": {
            "physical_modlist_current": "NOT_RECONFIRMED",
            "read_only": True,
            "complete_consumer_universe": "NOT_CERTIFIED",
            "class_candidate_strings": "DISCOVERY_NOT_CALL_GRAPH_PROOF",
            "real_weighted_random_distribution": "NOT_TESTED",
            "runtime_config_and_datapack": "NOT_CAPTURED",
            "state_persistence_durability": "NOT_TESTED",
            "cross_dimension_and_reload": "NOT_TESTED",
            "menu_or_network_replay_protection": "NOT_VERIFIED",
            "data_synchronicity": "NOT_TESTED",
            "static_perk_contract": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
        },
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf-8"))
            <= MAX_REPORT_BYTES, "clean-room report exceeds byte budget")
    return report


def verify_lock(report, lock):
    raw = (json.dumps(report, indent=2, ensure_ascii=False)
           + "\n").encode("utf-8")
    require(lock["report_sha256"] == hashlib.sha256(raw).hexdigest(),
            "TransmutationData evidence SHA-256 drift")
    require(lock["report_bytes"] == len(raw), "report length drift")
    require(lock["publisher_sha256"] == report["artifact"]["sha256"],
            "publisher identity drift")
    require(lock["class_count"] == len(report["classes"]),
            "native class cohort drift")
    require(lock["candidate_consumer_count"] ==
            len(report["candidate_consumer_population"]),
            "consumer discovery drift")
    require(lock["mutation"] == "NO_MUTATION" and
            report["limitations"]["mutation"] == "NO_MUTATION",
            "mutation cannot be certified by this read-only audit")


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
        "result": "LOCK_VERIFIED" if args.lock else "DISCOVERY_UNSEALED",
        "publisher_sha256": report["artifact"]["sha256"],
        "owners": len(report["classes"]),
        "consumer_candidates": len(report["candidate_consumer_population"]),
        "mutation": "NO_MUTATION",
    }))


if __name__ == "__main__":
    main()
