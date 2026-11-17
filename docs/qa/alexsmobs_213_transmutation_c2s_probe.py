#!/usr/bin/env python3
"""Alex's Mobs 2.1.13: exact read-only Transmutation Table C2S boundaries.

Provider publisher identity is hard-gated against the installed sibling modlist.
No message invocation, code reuse, live networking, item/XP mutation, or permission
claims. Relevant callsites and a small number of operator windows only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import javap, parse_methods, sha_file

BASE = "com/github/alexthe666/alexsmobs/"
MESSAGE = BASE + "message/MessageTransmuteFromMenu.class"
MENU = BASE + "inventory/MenuTransmutationTable.class"
TILE = BASE + "tileentity/TileEntityTransmutationTable.class"
PATHS = (MESSAGE, MENU, TILE)

SHA1 = "50ddafdf3d12b33331e4eecb4ab514ae451baadd"
SHA256 = "eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8"
SIZE = 27452738
SCOPE = "SHA_EXACT_ALEXSMOBS_213_TRANSMUTATION_C2S_OWNER_CAUSAL_DISCOVERY_READONLY"

NAME = re.compile(r"(?:(?:clickMenuButton|transmute|stillValid|removed|quickMoveStack|"
                  r"getPossibility|hasPossibilities|rollPossiblity|postTransmute|"
                  r"setPossibility|setPossibilities|MenuTransmutationTable)|"
                  r"(?i:lambda.*transmut))")
REF = re.compile(
    r"(?i:MessageTransmuteFromMenu|getSender|enqueueWork|"
    r"containerMenu|playerId|player_id|isClientSide|getEntity|"
    r"getPossibility|hasPossibilities|rollPossiblity|postTransmute|"
    r"transmute\b|experienceLevel|giveExperienceLevels|"
    r"transmutingExperienceCost|AMConfig|instabuild|"
    r"Mth.clamp|Slot.set|\.setChanged|"
    r"getPossibilities|canUse|stillValid|"
    r"getCount|setCount|setItem|setOutput|"
    r"Packet|Context|getLevel|getSender)")
CRITICAL = re.compile(r"(?i:getSender|enqueueWork|containerMenu|"
                      r"getEntity|transmute|MessageTransmuteFromMenu)")
MAX_BODY = 1800
MAX_METHODS = 65
MAX_SELECTED = 25
MAX_REFS_PER = 65
MAX_REFERENCES = 260
MAX_REPORT_BYTES = 145000


class TransmuteProbeError(ValueError):
    pass


def require(condition, text):
    if not condition:
        raise TransmuteProbeError(text)


def method_name(m):
    return m["header"].split("(", 1)[0].split()[-1].rsplit(".", 1)[-1]


def fingerprint(m):
    return hashlib.sha256(json.dumps(m, sort_keys=True, ensure_ascii=False,
                                   separators=(",", ":")).encode("utf-8")).hexdigest()


def item(row):
    return {
        "offset": row["offset"],
        "opcode": row["opcode"],
        "operand": row["operand"][:36],
        "symbol": row["symbol"][:210],
    }


def opcode_window(rows, center, before=3, after=4):
    require(0 <= center < len(rows), "invalid callsite index")
    return [item(r) for r in rows[max(0, center-before):min(len(rows), center+after+1)]]


def project_method(m):
    rows = m["instructions"]
    require(1 <= len(rows) <= MAX_BODY, "invalid/oversize message method")
    offsets = [x["offset"] for x in rows]
    require(offsets == sorted(set(offsets)), "duplicate/non-monotonic JVM offsets")
    calls = []
    critical = []
    for i, row in enumerate(rows):
        if row["opcode"].startswith(("invoke", "getfield", "putfield",
                                    "getstatic", "putstatic", "new",
                                    "checkcast", "instanceof", "ldc")) and REF.search(
                                        row["symbol"]):
            calls.append({
                "site": item(row),
                "previous": item(rows[i-1]) if i else None,
                "next": item(rows[i+1]) if i+1 < len(rows) else None,
            })
            if CRITICAL.search(row["symbol"]) and len(critical) < 8:
                critical.append({
                    "anchor": row["offset"],
                    "operators": opcode_window(rows, i),
                })
    require(len(calls) <= MAX_REFS_PER, "unbounded C2S callsite list " + method_name(m))
    branches = []
    for row in rows:
        if row["opcode"].startswith(("if", "goto")):
            target = row["operand"].split(" ", 1)[0]
            require(re.fullmatch(r"-?\d+", target or "") is not None,
                    "unparseable JVM branch target")
            branches.append({
                "offset": row["offset"],
                "opcode": row["opcode"],
                "target": int(target),
            })
    require(len(branches) <= 100, "unbounded message branch list")
    return {
        "name": method_name(m), "descriptor": m["descriptor"],
        "body_sha256": fingerprint(m), "instruction_count": len(rows),
        "branch_count": len(branches), "branches": branches,
        "selected_refs": calls, "critical_windows": critical,
    }


def projection(methods):
    out = []
    grand_total = 0
    for path in PATHS:
        require(path in methods, "missing transmutation class")
        native = methods[path]
        require(1 <= len(native) <= MAX_METHODS, "unexpected method count " + path)
        roster = [
            {"name": method_name(m), "descriptor": m["descriptor"],
             "instructions": len(m["instructions"])}
            for m in native
        ]
        pairs = [(r["name"], r["descriptor"]) for r in roster]
        require(len(pairs) == len(set(pairs)), "duplicate JVM method signature")
        if path == MESSAGE:
            chosen = [m for m in native if m["instructions"]]
        else:
            chosen = [m for m in native if m["instructions"] and
                      NAME.search(method_name(m))]
        require(1 <= len(chosen) <= MAX_SELECTED,
                "empty/oversize selected C2S method cohort " + path)
        if path == MENU:
            require({"clickMenuButton", "transmute"}.issubset({
                method_name(m) for m in chosen}), "menu sender/settlement missing")
        if path == TILE:
            require({"getPossibility", "postTransmute"}.issubset({
                method_name(m) for m in chosen}), "table reader/post-settlement missing")
        projections = [project_method(m) for m in chosen]
        count = sum(len(m["selected_refs"]) for m in projections)
        grand_total += count
        out.append({
            "class_path": path, "declared_methods": len(native),
            "roster": roster,
            "selected_methods": projections,
            "relevant_refs": count,
        })
    require(grand_total <= MAX_REFERENCES, "unbounded global C2S reference count")
    return {"classes": out, "bounded_reference_count": grand_total}


def audit(jar, javap_bin):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "installed publisher SHA-1/SHA-256/size mismatch")
    sha = {}
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP entries")
        for path in PATHS:
            require(path in names, "missing native transmutation class " + path)
            raw = archive.read(path)
            require(raw[:4] == b"\xca\xfe\xba\xbe"
                    and int.from_bytes(raw[6:8], "big") == 65,
                    "unexpected 1.21.1/JVM classfile version")
            sha[path] = hashlib.sha256(raw).hexdigest()
    methods = {
        path: parse_methods(javap(javap_bin, jar, path[:-6].replace("/", ".")))
        for path in PATHS
    }
    observed = projection(methods)
    for cls in observed["classes"]:
        cls["class_sha256"] = sha[cls["class_path"]]
    report = {
        "schema_version": 1,
        "scope": SCOPE,
        "artifact": {
            "filename": "alexsmobs-2.1.13-neoforge+1.21.1.jar",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
        },
        "observations": observed,
        "limitations": {
            "read_only": True,
            "complete_sender_receiver_identity": "NOT_CERTIFIED",
            "context_sender_authentication": "NOT_VERIFIED",
            "menu_player_session_binding": "NOT_VERIFIED",
            "packet_choice_validation": "NOT_VERIFIED",
            "replay_and_concurrent_settlement": "NOT_VERIFIED",
            "transmutation_xp_and_item_effective_qa": "NOT_TESTED",
            "runtime_packet_registration": "NOT_RECONSTRUCTED",
            "exceptional_cfg_and_transformed_runtime": "NOT_RECONSTRUCTED",
            "static_perk_contract": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
        }
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf-8")) <= MAX_REPORT_BYTES,
            "clean-room report exceeds bounded byte budget")
    return report


def verify_snapshot(report, expected):
    require(report == expected, "transmutation C2S JAR snapshot drift")
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", default="javap")
    p.add_argument("--snapshot", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--print-candidate", action="store_true")
    args = p.parse_args()
    report = audit(args.jar, args.javap)
    if args.snapshot:
        verify_snapshot(report, json.loads(args.snapshot.read_text(encoding="utf8")))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf8")
    if args.print_candidate:
        print("TRANSMUTATION_C2S_EVIDENCE_BEGIN")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print("TRANSMUTATION_C2S_EVIDENCE_END")
    print(json.dumps({
        "result": ("SHA_EXACT_TRANSMUTATION_C2S_SNAPSHOT_VERIFIED"
                   if args.snapshot else "UNSEALED_TRANSMUTATION_C2S_DISCOVERY"),
        "classes": len(report["observations"]["classes"]),
        "refs": report["observations"]["bounded_reference_count"],
        "mutation": "NO_MUTATION",
    }))


if __name__ == "__main__":
    main()
