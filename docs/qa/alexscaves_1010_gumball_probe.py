#!/usr/bin/env python3
"""Read-only, SHA-exact Gumball impact evidence. No mutation or gameplay claims.

Only bounded symbolic/constant/branch anchors are exported, never full
method bytecode, source code, asset bytes, or a decompilation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)

CLASS = BASE + "server/entity/item/GumballEntity.class"
CLASS_SHA256 = "343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535"
ON_HIT = "(Lnet/minecraft/world/phys/EntityHitResult;)V"
FACTORY_SITE = 86
MAX_METHODS = 24
MAX_INSTRUCTIONS = 2200
MAX_ANCHORS = 180
MAX_WINDOWS = 24
CALL_OPS = {"getfield", "putfield", "getstatic", "putstatic",
            "invokevirtual", "invokestatic", "invokespecial",
            "invokeinterface", "invokedynamic"}
MATCH_METHOD = re.compile(r"([A-Za-z0-9_$<>]+)\(")
INTERESTING = re.compile(
    r"(?:hit|tick|impact|damage|bounce|split|explode|remove|discard|"
    r"save|load|owner|shoot|collid|deflect|hurt)", re.I
)
WINDOW = re.compile(
    r"(?:causeGumballDamage|\.hurt:|ACCompat\.hurt|addFreshEntity|"
    r"getOwner|discard|setDeltaMovement|\.explode:)"
)


class GumballEvidenceError(ValueError):
    pass


def method_name(m):
    match = MATCH_METHOD.search(m["header"])
    return match.group(1) if match else ""


def compact(inst):
    return {k: inst[k] for k in ("offset", "opcode", "operand", "symbol")}


def summarize(method):
    instructions = method["instructions"]
    if not 1 <= len(instructions) <= MAX_INSTRUCTIONS:
        raise GumballEvidenceError("invalid instruction budget")
    offsets = [i["offset"] for i in instructions]
    if len(offsets) != len(set(offsets)):
        raise GumballEvidenceError("duplicate bytecode offsets")
    symbolic, branches, constants, windows = [], [], [], []
    for j, i in enumerate(instructions):
        op = i["opcode"]
        if op in CALL_OPS:
            symbolic.append(compact(i))
        if op.startswith("if") or op in ("goto", "goto_w", "tableswitch", "lookupswitch"):
            branches.append(compact(i))
        if op.startswith(("iconst_", "lconst_", "fconst_", "dconst_")) or op in ("bipush", "sipush", "ldc", "ldc_w", "ldc2_w"):
            constants.append(compact(i))
        if len(windows) < MAX_WINDOWS and WINDOW.search(i["symbol"]):
            windows.append({
                "at": i["offset"],
                "instructions": [compact(v) for v in instructions[max(0,j-9):j+10]],
            })
    if max(len(symbolic), len(branches), len(constants)) > MAX_ANCHORS:
        raise GumballEvidenceError("anchor budget exceeded")
    return {
        "name": method_name(method),
        "header": method["header"],
        "descriptor": method["descriptor"],
        "parsed_method_sha256": hashlib.sha256(
            json.dumps(method, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf8")
        ).hexdigest(),
        "instruction_count": len(instructions),
        "symbolic_references": symbolic,
        "branches": branches,
        "constants": constants,
        "callsite_windows": windows,
        "control_flow_reachability": "NOT_PROVEN",
    }


def validate_on_hit(method):
    if method_name(method) != "onHitEntity" or method["descriptor"] != ON_HIT:
        raise GumballEvidenceError("wrong exact impact method")
    calls = [x for x in method["instructions"]
             if "causeGumballDamage" in x["symbol"]]
    if len(calls) != 1 or calls[0]["offset"] != FACTORY_SITE or calls[0]["opcode"] != "invokestatic":
        raise GumballEvidenceError("Gumball factory site changed; fail closed")
    return calls[0]


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise GumballEvidenceError("JAR SHA/size mismatch")
    with zipfile.ZipFile(jar) as archive:
        if len(archive.namelist()) != len(set(archive.namelist())):
            raise GumballEvidenceError("duplicate ZIP member")
        binary = archive.read(CLASS)
        observed_sha = hashlib.sha256(binary).hexdigest()
        if observed_sha != CLASS_SHA256:
            raise GumballEvidenceError("Gumball class SHA mismatch")
    methods = parse_methods(javap(javap_bin, jar, CLASS[:-6].replace("/", ".")))
    hits = [m for m in methods if method_name(m) == "onHitEntity" and m["descriptor"] == ON_HIT]
    if len(hits) != 1:
        raise GumballEvidenceError("missing or ambiguous onHitEntity")
    validate_on_hit(hits[0])
    selected = [m for m in methods if INTERESTING.search(method_name(m))]
    if not 1 <= len(selected) <= MAX_METHODS:
        raise GumballEvidenceError("selected method budget changed")
    evidence = {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_GUMBALL_SELECTED_BYTECODE_ANCHORS_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "class_path": CLASS,
        "class_sha256": observed_sha,
        "declared_methods": [{"header": m["header"], "descriptor": m["descriptor"]} for m in methods],
        "selected_methods": [summarize(m) for m in selected],
        "limits": {
            "full_method_body": "NOT_EXPORTED",
            "nonselected_methods": "NOT_AUDITED",
            "runtime_behavior": "NOT_VERIFIED",
            "damage_amounts_targets_PvP": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "provider_universe_closed": False,
        },
    }
    return evidence



# The SHA-exact contract pins declared signatures and critical instruction anchors
# without pretending to reconstruct every instruction or prove runtime reachability.
SNAPSHOT_OFFSETS = {
    "onHitEntity": (6, 11, 31, 44, 71, 86, 97, 105, 113, 139, 144, 159, 174, 284, 290, 299, 308, 317, 326, 335, 346),
    "onHit": (2, 43, 54, 77, 94, 107, 168),
    "bounceFromDirection": (39, 46, 101, 167, 183, 189, 242, 287, 445, 458),
    "tick": (176, 183, 187, 197, 200, 207, 218, 237, 238, 239, 242, 247),
    "addAdditionalSaveData": (10, 13),
    "readAdditionalSaveData": (10, 13),
}


def strict_pairs(pairs):
    result = {}
    for key, val in pairs:
        if key in result:
            raise GumballEvidenceError("duplicate snapshot field: " + key)
        result[key] = val
    return result


def snapshot_view(evidence):
    """A bounded, exact method-hash and critical-anchored regression surface."""
    selected = evidence["selected_methods"]
    identities = [(m["name"], m["descriptor"]) for m in selected]
    if len(set(identities)) != len(identities):
        raise GumballEvidenceError("duplicated method identity")
    anchors = {}
    for name, requested in SNAPSHOT_OFFSETS.items():
        matches = [m for m in selected if m["name"] == name]
        if len(matches) != 1:
            raise GumballEvidenceError("missing or ambiguous anchored method: " + name)
        method = matches[0]
        available = method["symbolic_references"] + method["branches"] + method["constants"]
        anchors[name] = []
        for offset in requested:
            found = [i for i in available if i["offset"] == offset]
            if len(found) != 1:
                raise GumballEvidenceError("missing or ambiguous bytecode anchor: " + name + ":" + str(offset))
            anchors[name].append(found[0])
    return {
        "schema_version": 1,
        "scope": evidence["scope"],
        "artifact": evidence["artifact"],
        "class_path": evidence["class_path"],
        "class_sha256": evidence["class_sha256"],
        "declared_method_count": len(evidence["declared_methods"]),
        "selected_methods": [
            {k: m[k] for k in ("name", "descriptor", "instruction_count", "parsed_method_sha256")}
            for m in selected
        ],
        "selected_anchors": anchors,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--snapshot")
    args = p.parse_args()
    evidence = audit(args.jar, args.javap)
    if args.snapshot:
        expected = json.loads(Path(args.snapshot).read_text(encoding="utf8"), object_pairs_hook=strict_pairs)
        if snapshot_view(evidence) != expected:
            raise GumballEvidenceError("SHA-exact Gumball snapshot drift")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf8")
    print("GUMBALL_1010_BEGIN")
    print(json.dumps(evidence, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
    print("GUMBALL_1010_END")


if __name__ == "__main__":
    main()
