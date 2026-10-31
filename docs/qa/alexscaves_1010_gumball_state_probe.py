#!/usr/bin/env python3
"""Selected SHA-exact Alex's Caves 1.0.10 Gumball state/producer contract probe.

Interop research only: exports bounded references, numerical constants,
branches, selected offset windows and hashes, NOT complete bytecode/source.
This does not prove effective runtime behavior, safe mutation or physical QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)

CLASSES = {
    BASE + "server/entity/item/GumballEntity.class":
        "343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535",
    BASE + "server/entity/living/GumbeeperEntity.class":
        "6a24f05a730218352a083da32f233c3d48fb5f85a6f24f1ba45d78c422b0266c",
    BASE + "server/item/ShotGumItem.class":
        "08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238",
}

GUMBALL = "GumballEntity.class"
GUMBEEPER = "GumbeeperEntity.class"
SHOTGUM = "ShotGumItem.class"
GUMBALL_NAMES = {
    "GumballEntity", "defineSynchedData", "tick", "bounceFromDirection",
    "getMaximumBounces", "setMaximumBounces", "getBounces", "setBounces",
    "getDamage", "setDamage", "getColor", "setColor", "targetsOnBounce",
    "setTargetsOnBounce", "splitsOnHit", "setSplitsOnHit", "isExplosive",
    "setExplosive", "getDefaultGravity", "onHit", "onHitEntity",
    "addAdditionalSaveData", "readAdditionalSaveData", "getExplodeProgress",
}
GUMBEEPER_NAMES = {"tick", "shootGumball", "isCharged",
                    "getPossessedByLicowitchId", "getPossessingLicowitch"}
SHOTGUM_NAMES = {"acInventoryTick"}
METHODS = {
    GUMBALL: GUMBALL_NAMES,
    GUMBEEPER: GUMBEEPER_NAMES,
    SHOTGUM: SHOTGUM_NAMES,
}
FOCUS = {
    (GUMBALL, "onHitEntity"): [6, 11, 86, 139, 144, 174, 290, 299, 335],
    (GUMBALL, "tick"): [183, 187, 197, 200, 218, 237, 238, 239, 242, 247],
    (GUMBALL, "bounceFromDirection"): [39, 46, 101, 167, 183, 189, 242, 287],
    (GUMBEEPER, "tick"): [385, 518, 527, 542, 560, 579],
    (GUMBEEPER, "shootGumball"): [80, 265, 274, 289, 307, 326],
    (SHOTGUM, "acInventoryTick"): [316, 427, 434, 441, 448, 480, 487, 495, 499, 508],
}
MAX_SELECTED_METHODS = 35
MAX_METHOD_INSNS = 2400
MAX_PER_KIND = 260
MAX_WINDOWS = 20
MAX_WINDOW_INSNS = 21
SYMBOLIC = {"getfield", "putfield", "getstatic", "putstatic", "invokevirtual",
            "invokestatic", "invokespecial", "invokeinterface", "invokedynamic"}
BRANCHES = {"goto", "goto_w", "tableswitch", "lookupswitch"}
CONSTANTS = {"bipush", "sipush", "ldc", "ldc_w", "ldc2_w"}


class GumballStateProbeError(ValueError):
    pass


def name_of(method):
    h = method["header"]
    if "(" not in h:
        return ""
    return h.split("(", 1)[0].split()[-1].rsplit(".", 1)[-1]


def compact(ins):
    return {k: ins[k] for k in ("offset", "opcode", "operand", "symbol")}


def classify(ins):
    op = ins["opcode"]
    if op in SYMBOLIC:
        return "symbols"
    if op.startswith("if") or op in BRANCHES:
        return "branches"
    if op in CONSTANTS or op.startswith(("iconst_", "fconst_", "lconst_", "dconst_")):
        return "constants"
    return None


def summarize(method, points):
    instructions = method["instructions"]
    if not 1 <= len(instructions) <= MAX_METHOD_INSNS:
        raise GumballStateProbeError("unexpected instruction population")
    offsets = [i["offset"] for i in instructions]
    if len(offsets) != len(set(offsets)):
        raise GumballStateProbeError("duplicate bytecode offset")
    results = {"symbols": [], "branches": [], "constants": []}
    for ins in instructions:
        kind = classify(ins)
        if kind:
            results[kind].append(compact(ins))
    if any(len(items) > MAX_PER_KIND for items in results.values()):
        raise GumballStateProbeError("selected anchor budget exceeded")
    positions = {ins["offset"]: pos for pos, ins in enumerate(instructions)}
    if len(points) > MAX_WINDOWS:
        raise GumballStateProbeError("too many evidence windows")
    windows = []
    for at in points:
        if at not in positions:
            raise GumballStateProbeError("missing fixed SHA-exact offset " + str(at))
        pos = positions[at]
        window = instructions[max(0, pos - 9):pos + 10]
        if len(window) > MAX_WINDOW_INSNS:
            raise GumballStateProbeError("oversize evidence window")
        windows.append({"at": at, "instructions": [compact(i) for i in window]})
    return {
        "name": name_of(method), "header": method["header"],
        "descriptor": method["descriptor"],
        "instruction_count": len(instructions),
        "parsed_method_sha256": hashlib.sha256(json.dumps(
            method, sort_keys=True, ensure_ascii=False,
            separators=(",", ":")).encode("utf8")).hexdigest(),
        "symbolic_references": results["symbols"],
        "branches": results["branches"],
        "numeric_constants": results["constants"],
        "selected_windows": windows,
        "runtime_reachability": "NOT_PROVEN",
    }


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise GumballStateProbeError("publisher JAR hash/size changed")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise GumballStateProbeError("duplicate archive entry")
        for path, digest in CLASSES.items():
            if hashlib.sha256(archive.read(path)).hexdigest() != digest:
                raise GumballStateProbeError("class SHA mismatch: " + path)
    selected_classes, selected_total = [], 0
    for path, class_digest in sorted(CLASSES.items()):
        name = path.rsplit("/", 1)[-1]
        methods = parse_methods(javap(javap_bin, jar, path[:-6].replace("/", ".")))
        roster = [{"header": m["header"], "descriptor": m["descriptor"]}
                  for m in methods]
        chosen = []
        identities = set()
        for method in methods:
            key = (name_of(method), method["descriptor"])
            if key[0] in METHODS[name]:
                if key in identities:
                    raise GumballStateProbeError("duplicate JVM method identity")
                identities.add(key)
                chosen.append(summarize(method, FOCUS.get((name, key[0]), [])))
        if not chosen:
            raise GumballStateProbeError("selected class has no methods")
        selected_total += len(chosen)
        selected_classes.append({
            "class_path": path, "class_sha256": class_digest,
            "declared_methods": roster, "selected_methods": chosen,
        })
    if selected_total > MAX_SELECTED_METHODS:
        raise GumballStateProbeError("too many selected methods")
    core = selected_classes[0]["class_path"] if selected_classes else ""
    if not any(row["class_path"].endswith("/" + SHOTGUM)
               for row in selected_classes):
        raise GumballStateProbeError("missing ShotGum method surface")
    return {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_GUMBALL_STATE_OWNER_AND_PRODUCER_SELECTED_METHODS_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "selected_classes": selected_classes,
        "selected_method_count": selected_total,
        "limits": {
            "full_method_body_exported": False,
            "selected_methods_only": True,
            "exception_cfg_and_full_control_flow": "NOT_RECONSTRUCTED",
            "effective_cost_and_cooldown": "NOT_CERTIFIED",
            "owner_and_player_attribution": "NOT_CERTIFIED",
            "save_load_and_synched_state": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "provider_universe_closed": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = audit(args.jar, args.javap)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False)
                      + "\n", encoding="utf8")
    print("GUMBALL_STATE_1010_BEGIN")
    print(json.dumps(out, separators=(",", ":"), sort_keys=True, ensure_ascii=False))
    print("GUMBALL_STATE_1010_END")
    print("selected_methods=" + str(out["selected_method_count"])
          + " NO_RUNTIME_OR_MUTATOR_CERTIFICATION")


if __name__ == "__main__":
    main()
