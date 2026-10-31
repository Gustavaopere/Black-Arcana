#!/usr/bin/env python3
"""Read-only SHA-exact NuclearExplosionEntity 1.0.10 damage envelope probe.

Bounded interop evidence only. Never infer safe hooks, operational damage,
PVP/world-safety compliance or actual tick execution from bytecode anchors.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import (
    GumballStateProbeError, classify, compact, name_of, strict_pairs,
)

CLASS = BASE + "server/entity/item/NuclearExplosionEntity.class"
CLASS_SHA = "d9c827a9acb2d0f9e7050252ed57e6a3d0a8ad49053e54f19a8eaeb6b84da912"
NAMES = {
    "NuclearExplosionEntity", "defineSynchedData", "tick",
    "calculateDamage", "isIntentionalGameDesign",
    "addAdditionalSaveData", "readAdditionalSaveData",
}
# These offsets were already verified by EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json.
TICK_OFFSETS = (
    1, 80, 83, 167, 225, 288, 318, 466,
    579, 580, 582, 584, 585, 586, 592, 595, 605,
    608, 618, 621, 623, 626, 633, 635, 638, 640, 643, 647, 650,
)
MAX_METHODS = 32
MAX_WINDOW = 15
MAX_ANCHORS = 300
MAX_METHOD_INSNS = 1600


def selected_anchors(method, selected_offsets):
    instructions = method["instructions"]
    if len(instructions) > MAX_METHOD_INSNS or not instructions:
        raise GumballStateProbeError("selected Nuclear method budget exceeded")
    offsets = [i["offset"] for i in instructions]
    if len(offsets) != len(set(offsets)):
        raise GumballStateProbeError("duplicate Nuclear method instruction offsets")
    picked = {}
    for ins in instructions:
        category = classify(ins)
        if category:
            picked.setdefault(category, []).append(compact(ins))
    if sum(len(v) for v in picked.values()) > MAX_ANCHORS:
        raise GumballStateProbeError("Nuclear method symbolic/constant bound exceeded")
    positions = {i["offset"]: n for n, i in enumerate(instructions)}
    if len(selected_offsets) > 30:
        raise GumballStateProbeError("too many Nuclear windows")
    windows = []
    for at in selected_offsets:
        if at not in positions:
            raise GumballStateProbeError("exact Nuclear offset missing: " + str(at))
        ix = positions[at]
        records = [compact(i) for i in instructions[max(0, ix - 6):ix + 8]]
        if len(records) > MAX_WINDOW:
            raise GumballStateProbeError("Nuclear window budget exceeded")
        windows.append({"at": at, "ins": records})
    return {
        "header": method["header"],
        "name": name_of(method),
        "descriptor": method["descriptor"],
        "instruction_count": len(instructions),
        "parsed_method_sha256": hashlib.sha256(json.dumps(
            method, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf8")).hexdigest(),
        "symbols": picked.get("symbols", []),
        "constants": picked.get("constants", []),
        "branches": picked.get("branches", []),
        "windows": windows,
    }


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise GumballStateProbeError("Nuclear publisher JAR drift")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        if len(set(names)) != len(names):
            raise GumballStateProbeError("duplicate publisher JAR entry")
        if hashlib.sha256(z.read(CLASS)).hexdigest() != CLASS_SHA:
            raise GumballStateProbeError("Nuclear class hash drift")
    methods = parse_methods(javap(javap_bin, jar, CLASS[:-6].replace("/", ".")))
    roster = [{"header": x["header"], "descriptor": x["descriptor"]}
              for x in methods]
    if len(roster) > 110:
        raise GumballStateProbeError("Nuclear class method count drift")
    seen = set()
    selected = []
    for method in methods:
        name = name_of(method)
        if name not in NAMES:
            continue
        key = (name, method["descriptor"])
        if key in seen:
            raise GumballStateProbeError("ambiguous Nuclear method identity")
        seen.add(key)
        points = TICK_OFFSETS if name == "tick" else ()
        selected.append(selected_anchors(method, points))
    if not 1 <= len(selected) <= MAX_METHODS:
        raise GumballStateProbeError("Nuclear selected method count outside bounds")
    tick = [m for m in selected if m["name"] == "tick" and m["descriptor"] == "()V"]
    if len(tick) != 1:
        raise GumballStateProbeError("missing Nuclear tick")
    calls = [x for x in tick[0]["symbols"] if "ACDamageTypes.cause" in x["symbol"]]
    if {(c["offset"], c["opcode"]) for c in calls} != {
        (605, "invokestatic"), (618, "invokestatic")
    }:
        raise GumballStateProbeError("Nuclear damage factory callsites drift")
    return {
        "schema_version": 1,
        "scope": "SHA_EXACT_NUCLEAR_EXPLOSION_1010_SELECTED_STATE_DAMAGE_AND_WORLD_ENVELOPE",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "class_path": CLASS, "class_sha256": CLASS_SHA,
        "declared_methods": roster, "selected_methods": selected,
        "limits": {
            "complete_cfg": "NOT_RECONSTRUCTED",
            "runtime_reachability": "NOT_PROVEN",
            "applicability_to_pvp_and_player_owner": "NOT_PROVEN",
            "world_effect_policy": "NOT_VERIFIED_FOR_NATIVE_PROVIDER",
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
            "complete_perk_ready": False,
            "provider_universe_closed": False,
        },
    }


def seal(evidence):
    critical = {}
    for m in evidence["selected_methods"]:
        ref = m["name"] + ":" + m["descriptor"]
        if ref in critical:
            raise GumballStateProbeError("duplicate Nuclear selected method seal")
        all_anchors = m["symbols"] + m["branches"] + m["constants"]
        chosen = []
        if m["name"] == "tick" and m["descriptor"] == "()V":
            for offset in TICK_OFFSETS:
                matches = [x for x in all_anchors if x["offset"] == offset]
                # fstore/fload/fmul are tracked by bounded windows, not
                # misclassified as numeric constants.
                if matches:
                    if len(matches) != 1:
                        raise GumballStateProbeError("duplicate Nuclear seal anchor")
                    chosen.append(matches[0])
                else:
                    window = next((w for w in m["windows"] if w["at"] == offset), None)
                    matches = [x for x in window["ins"] if x["offset"] == offset] if window else []
                    if len(matches) != 1:
                        raise GumballStateProbeError("missing Nuclear seal instruction " + str(offset))
                    chosen.append(matches[0])
        critical[ref] = {
            "parsed_method_sha256": m["parsed_method_sha256"],
            "instruction_count": m["instruction_count"],
            "selected_offsets": chosen,
        }
    if len(critical) != len(evidence["selected_methods"]):
        raise GumballStateProbeError("Nuclear seal missing methods")
    return {
        "schema_version": 1, "scope": evidence["scope"],
        "artifact": evidence["artifact"],
        "class_path": evidence["class_path"],
        "class_sha256": evidence["class_sha256"],
        "declared_method_count": len(evidence["declared_methods"]),
        "selected_method_count": len(evidence["selected_methods"]),
        "methods": critical,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--snapshot")
    args = p.parse_args()
    evidence = audit(Path(args.jar), args.javap)
    projection = seal(evidence)
    if args.snapshot:
        expected = json.loads(Path(args.snapshot).read_text(encoding="utf8"),
                              object_pairs_hook=strict_pairs)
        if expected != projection:
            raise GumballStateProbeError("Nuclear SHA-exact snapshot drift")
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, sort_keys=True, ensure_ascii=False,
                               indent=2) + "\n", encoding="utf8")
    print("NUCLEAR_1010_ENVELOPE_BEGIN")
    print(json.dumps(projection, sort_keys=True, separators=(",", ":")))
    print("NUCLEAR_1010_ENVELOPE_END")
    # A bounded explanation bundle; complete method bodies are not emitted.
    selected_explanation = {}
    for method in evidence["selected_methods"]:
        if method["name"] == "tick":
            relevant = ("calculateDamage:", "isIntentionalGameDesign:",
                        "causeIntentionalGameDesign:", "causeNukeDamage:",
                        "hurt:", "getEntitiesOfClass:", "isDestroyable:",
                        "remove:", "setDeltaMovement:", "discard:")
            selected_explanation["tick"] = {
                "symbols": [v for v in method["symbols"]
                            if any(token in v["symbol"] for token in relevant)],
                "windows": [w for w in method["windows"]
                            if w["at"] in (466, 580, 586, 592, 605, 623, 647, 650)],
                "constants": method["constants"],
            }
        else:
            selected_explanation[method["name"]] = {
                "symbols": method["symbols"], "constants": method["constants"],
                "branches": method["branches"],
            }
    print("NUCLEAR_1010_DETAILS_BEGIN")
    print(json.dumps(selected_explanation, separators=(",", ":"),
                     ensure_ascii=False, sort_keys=True))
    print("NUCLEAR_1010_DETAILS_END")
    print("NO_MUTATION NO_RUNTIME_CERTIFICATION")


if __name__ == "__main__":
    main()
