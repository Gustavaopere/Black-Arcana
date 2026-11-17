#!/usr/bin/env python3
"""Read-only 2.1.13 Transmutation Table settlement, menu lifecycle, and replay boundaries.

Audits the SHA-exact publisher JAR plus already-sealed native method identities.
Only sparse JVM operator evidence is reported; never invokes provider code.
The result is NOT proof of replay safety, an approved perk seam or runtime QA.
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
    BASE, MENU, MESSAGE, TILE, SHA1, SHA256, SIZE,
    fingerprint, item, method_name, require,
)

TARGETS = {
    MESSAGE: {"MessageTransmuteFromMenu", "read", "write"},
    MENU: {"MenuTransmutationTable", "stillValid", "slotsChanged",
           "clickMenuButton", "transmute", "removed", "lambda$removed$0"},
    TILE: {"loadAdditional", "saveAdditional", "randomizeResults",
           "rollPossiblity", "hasPossibilities", "getPossibility",
           "postTransmute", "tick", "setRerollPlayerUUID"},
}
TARGET_PATHS = tuple(TARGETS)
RELEVANT = re.compile(
    r"(?i:transmut|possibilit|experience|instabuild|"
    r"Slot\.set|setCount|setChanged|ContainerLevelAccess|stillValid|"
    r"drop|clearContent|BlockPos|UUID|Reroll|Loot|ItemStack|"
    r"CompoundTag|ListTag|RegistryFriendlyByteBuf|FriendlyByteBuf|"
    r"readInt|writeInt|playerId|choice|Mth\.clamp|hasPossibilities|"
    r"itemHandler|setItem|setData|sendBlockUpdated|"
    r"randomizeResults|loadAdditional|saveAdditional|"
    r"getMaxStackSize|Math\.max|Math\.floor|BlockEntity|"
    r"rollPossiblity|TransmutationTable)"
)
SETTLEMENT_SYMBOLS = {
    "selected_count": r"ItemStack\.setCount:",
    "output_slot": r"Slot\.set:",
    "xp_debit": r"Player\.giveExperienceLevels:",
    "post_settlement_callback": r"TileEntityTransmutationTable\.postTransmute:",
}
MAX_METHOD_INSTRUCTIONS = 350
MAX_REFS_PER_METHOD = 100
MAX_BRANCHES = 65
MAX_REPORT_BYTES = 210000


def select_method(methods, name, descriptor=None):
    found = [m for m in methods if method_name(m) == name
             and (descriptor is None or m["descriptor"] == descriptor)]
    require(len(found) == 1, "ambiguous/missing method " + name)
    return found[0]


def anchors(method, expressions):
    rows = method["instructions"]
    result = {}
    for key, pattern in expressions.items():
        matched = [r["offset"] for r in rows if re.search(pattern, r["symbol"])]
        result[key] = matched
    return result


def settlement_sequence(method):
    sites = anchors(method, SETTLEMENT_SYMBOLS)
    require(all(len(v) == 1 for v in sites.values()),
            "missing/duplicate native output, XP or post-settlement effect")
    offsets = [sites[k][0] for k in SETTLEMENT_SYMBOLS]
    require(offsets == sorted(offsets),
            "native transmutation effect order changed")
    require(offsets == [122, 131, 138, 149],
            "SHA-exact transmutation settlement JVM anchors drift")
    return {
        "sites": sites,
        "ordered_effects": list(SETTLEMENT_SYMBOLS),
        "observed_order": offsets,
        "runtime_atomicity": "NOT_TESTED",
    }


def projected_method(method):
    rows = method["instructions"]
    require(1 <= len(rows) <= MAX_METHOD_INSTRUCTIONS,
            "unbounded native method " + method_name(method))
    offsets = [r["offset"] for r in rows]
    require(offsets == sorted(set(offsets)),
            "duplicate or out-of-order JVM offsets")
    offsetset = set(offsets)
    branches = []
    refs = []
    for i, r in enumerate(rows):
        if r["opcode"].startswith(("if", "goto")):
            target_text = r["operand"].split(" ", 1)[0]
            require(re.fullmatch(r"-?\d+", target_text) is not None,
                    "invalid JVM branch target")
            target = int(target_text)
            require(target in offsetset, "JVM branch outside method body")
            branches.append({
                "offset": r["offset"], "opcode": r["opcode"], "target": target,
                "preceding": item(rows[i-1]) if i else None,
            })
        if r["opcode"].startswith(
            ("invoke", "getfield", "putfield", "getstatic", "putstatic",
             "ldc", "new", "instanceof", "checkcast")
        ) and RELEVANT.search(r["symbol"]):
            refs.append({
                "site": item(r),
                "preceding": item(rows[i-1]) if i else None,
                "following": item(rows[i+1]) if i + 1 < len(rows) else None,
            })
    require(len(branches) <= MAX_BRANCHES and len(refs) <= MAX_REFS_PER_METHOD,
            "unbounded branch/ref evidence")
    return {
        "name": method_name(method),
        "descriptor": method["descriptor"],
        "body_sha256": fingerprint(method),
        "instruction_count": len(rows),
        "branches": branches,
        "relevant_sites": refs,
        "direct_still_valid_call": any(
            r["opcode"].startswith("invoke") and
            "stillValid:" in r["symbol"] for r in rows
        ),
    }


def validate_against_sealed_snapshot(methods, snapshot):
    require(snapshot["artifact"]["sha256"] == SHA256 and
            snapshot["artifact"]["sha1"] == SHA1 and
            snapshot["artifact"]["size_bytes"] == SIZE,
            "prior physical JAR certificate mismatch")
    prior = {c["class_path"]: c for c in snapshot["observations"]["classes"]}
    for path in TARGET_PATHS:
        require(path in prior, "missing sealed native class")
        existing = {(m["name"], m["descriptor"]): m["body_sha256"]
                    for m in prior[path]["selected_methods"]}
        for m in methods[path]:
            key = (method_name(m), m["descriptor"])
            if key in existing:
                require(fingerprint(m) == existing[key],
                        "previously certified bytecode fingerprint drift at "
                        + path + ":" + str(key))
    return True


def reroll_lifecycle(methods):
    """Report only exact JVM state transitions, not a runtime reliability claim."""
    post = select_method(methods, "postTransmute")
    tick = select_method(methods, "tick")
    loaded = select_method(methods, "loadAdditional")
    saved = select_method(methods, "saveAdditional")
    randomize = select_method(methods, "randomizeResults")

    def exact(method, offset, opcode, symbol=None, operand=None):
        found = [r for r in method["instructions"] if r["offset"] == offset]
        require(len(found) == 1 and found[0]["opcode"] == opcode,
                "reroll JVM offset/opcode drift at " + str(offset))
        row = found[0]
        if symbol:
            require(symbol in row["symbol"],
                    "reroll JVM symbol drift at " + str(offset))
        if operand:
            require(row["operand"].split(" ", 1)[0] == operand,
                    "reroll branch target drift at " + str(offset))
        return item(row)

    markers = {
        "post_transmute_count": exact(post, 79, "putfield", "totalTransmuteCount:I"),
        "post_transmute_queues_uuid": exact(
            post, 114, "invokevirtual", "setRerollPlayerUUID:"
        ),
        "tick_pending_uuid_check": exact(tick, 14, "ifnull", operand="87"),
        "tick_player_lookup": exact(
            tick, 25, "invokevirtual", "Level.getPlayerByUUID:"
        ),
        "tick_missing_player_skips_reroll": exact(
            tick, 30, "ifnull", operand="82"
        ),
        "tick_randomize_with_player": exact(
            tick, 79, "invokevirtual", "randomizeResults:"
        ),
        "tick_clear_pending_uuid": exact(
            tick, 84, "putfield", "rerollPlayerUUID:"
        ),
    }
    require(not any(
        "randomizeResults:" in r["symbol"] for r in post["instructions"]
    ), "postTransmute now directly rerolls, not a deferred marker")
    serialization = {}
    for name, method in (("loadAdditional", loaded), ("saveAdditional", saved)):
        used = any("rerollPlayerUUID:" in r["symbol"]
                   for r in method["instructions"])
        require(not used, "reroll UUID persistence now exists: review scope")
        serialization[name + "_directly_references_reroll_uuid"] = used
    reroll_calls = [r["offset"] for r in randomize["instructions"]
                    if r["opcode"].startswith("invoke") and
                    "rollPossiblity:" in r["symbol"]]
    require(reroll_calls == [3, 9, 15],
            "native three-output reroll callsites drift")
    return {
        "anchors": markers,
        "randomize_result_option_calls": reroll_calls,
        "serialization": serialization,
        "missing_player_branch_bypasses_randomize": True,
        "pending_uuid_cleared_after_missing_player_branch": True,
        "scope": "EXACT_STATIC_TICK_CFG_ONLY_NO_LOGIN_RELOAD_QA",
    }


def audit(jar, javap_bin, sealed):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher JAR SHA-1/SHA-256/size mismatch")
    class_sha = {}
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        require(len(names) == len(set(names)), "duplicate archive entries")
        for path in TARGET_PATHS:
            require(path in names, "missing native transmutation owner " + path)
            raw = arc.read(path)
            require(raw[:4] == b"\xca\xfe\xba\xbe" and
                    int.from_bytes(raw[6:8], "big") == 65,
                    "invalid publisher classfile or Java major version")
            class_sha[path] = hashlib.sha256(raw).hexdigest()
    old_sha = {c["class_path"]: c["class_sha256"]
               for c in sealed["observations"]["classes"]}
    require(class_sha == {p: old_sha[p] for p in TARGET_PATHS},
            "previously sealed native class hash drift")
    native = {
        path: parse_methods(javap(javap_bin, jar, path[:-6].replace("/", ".")))
        for path in TARGET_PATHS
    }
    validate_against_sealed_snapshot(native, sealed)
    projections = []
    for path in TARGET_PATHS:
        selected = [m for m in native[path] if method_name(m) in TARGETS[path]]
        require(2 <= len(selected) <= 20, "unexpected method cohort")
        projections.append({
            "class_path": path,
            "class_sha256": class_sha[path],
            "selected_methods": [projected_method(m) for m in selected],
        })
    transmute = select_method(native[MENU], "transmute")
    require(transmute["descriptor"] ==
            "(Lnet/minecraft/world/entity/player/Player;I)V",
            "unexpected native transaction signature")
    sequence = settlement_sequence(transmute)
    table_fields = {
        "has_still_valid_override": bool(
            [m for m in native[MENU] if method_name(m) == "stillValid"]
        ),
        "transmute_invokes_stillValid": any(
            "stillValid:" in r["symbol"] and r["opcode"].startswith("invoke")
            for r in transmute["instructions"]
        ),
        "transmute_invokes_removed": any(
            "removed:" in r["symbol"] and r["opcode"].startswith("invoke")
            for r in transmute["instructions"]
        ),
        "transmute_uses_menu_container": any(
            "Slot.set:" in r["symbol"] for r in transmute["instructions"]
        ),
    }
    report = {
        "schema_version": 1,
        "scope": "SHA_EXACT_ALEXSMOBS_213_TRANSMUTATION_SETTLEMENT_AND_LIFECYCLE_READONLY",
        "artifact": {
            "filename": "alexsmobs-2.1.13-neoforge+1.21.1.jar",
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE,
        },
        "sealed_predecessor": "EXACT-TRANSMUTATION-C2S-2.1.13.json",
        "classes": projections,
        "settlement": sequence,
        "menu_lifecycle": table_fields,
        "reroll_lifecycle": reroll_lifecycle(native[TILE]),
        "limitations": {
            "scope": "EXACT_PUBLISHER_STATIC_ONLY",
            "effective_pack_configuration": "NOT_VERIFIED_CURRENT_MODLIST",
            "still_valid_call_absence_means_unusable_menu": "NOT_PROVEN",
            "replay_safety": "NOT_VERIFIED",
            "concurrency_and_atomicity": "NOT_TESTED",
            "stale_menu_or_table_ownership": "NOT_VERIFIED",
            "invalid_choice_rejection": "NOT_VERIFIED",
            "world_and_saveddata_lifecycle": "NOT_VERIFIED",
            "mutation": "NO_MUTATION",
            "mutating_hook": "NOT_VERIFIED",
            "static_perk_contract": "NOT_CERTIFIED",
            "physical_qa": "NOT_TESTED",
        },
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf-8"))
            <= MAX_REPORT_BYTES, "oversized clean-room audit report")
    return report


def verify_snapshot(report, expected):
    if "report_sha256" not in expected:
        require(report == expected, "publisher settlement snapshot drift")
        return
    raw = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    require(expected.get("report_sha256") == hashlib.sha256(raw).hexdigest(),
            "SHA-locked publisher settlement report drift")
    require(expected.get("report_bytes") == len(raw),
            "publisher settlement report length drift")
    require(expected.get("publisher_sha256") == report["artifact"]["sha256"],
            "publisher SHA mismatch in settlement lock")
    require(expected.get("selected_methods") ==
            sum(len(c["selected_methods"]) for c in report["classes"]),
            "native method coverage drift")
    require(expected.get("settlement_offsets") ==
            report["settlement"]["observed_order"],
            "settlement callsite order drift")
    require(expected.get("missing_player_reroll_disposition") ==
            report["reroll_lifecycle"]["missing_player_branch_bypasses_randomize"],
            "reroll tick branch disposition drift")
    require(expected.get("mutation") == "NO_MUTATION" and
            report["limitations"]["mutation"] == "NO_MUTATION",
            "mutating lock not allowed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--sealed", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit(
        args.jar, args.javap,
        json.loads(args.sealed.read_text(encoding="utf-8")),
    )
    if args.snapshot:
        verify_snapshot(report, json.loads(args.snapshot.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "result": "SEALED" if args.snapshot else "UNSEALED_DISCOVERY",
        "classes": len(report["classes"]),
        "selected_methods": sum(len(x["selected_methods"])
                                for x in report["classes"]),
        "settlement_offsets": report["settlement"]["observed_order"],
        "mutation": "NO_MUTATION",
    }))


if __name__ == "__main__":
    main()
