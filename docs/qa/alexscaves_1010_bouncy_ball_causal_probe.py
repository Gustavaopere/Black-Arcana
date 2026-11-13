#!/usr/bin/env python3
"""Exact publisher 1.0.10 Bouncy Ball cross-manifest and JVM causal audit.

This is a read-only reconciliation of the already sealed Bouncy Ball and Gumball
state evidence against the actual publisher JAR. No third-party code is copied
or executed, and no mutating hook or physical QA is inferred.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_bouncy_ball_probe import (
    SHOT, BALL, GUMBEEPER, CLASSES, require, method as unique_method,
)
from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, sha_file, javap, parse_methods,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

OWNERS = (SHOT, BALL, GUMBEEPER)
EXPECTED_METHOD_COUNT = {SHOT: 25, BALL: 28, GUMBEEPER: 36}
EXPECTED_BRANCH_COUNT = {"acInventoryTick": 40,
                         "bounceFromDirection": 22,
                         "shootGumball": 12}
UNSUPPORTED = frozenset(("tableswitch", "lookupswitch", "jsr", "jsr_w", "ret"))
MAIN_METHODS = ("acInventoryTick", "bounceFromDirection", "shootGumball")
REQUIRED_PRODUCER = (
    (190, "BOUNCY_BALL"), (193, "enchantLevel"),
    (196, "iconst_2"), (197, "imul"), (198, "iadd"),
    (487, "setMaximumBounces"),
)
REQUIRED_CONSUMER = (
    (3, "getBounces"), (7, "getMaximumBounces"),
    (34, "setBounces"), (242, "discard"),
    (101, "getEntitiesOfClass"),
)
def pairs_unique(items):
    out = {}
    for key, value in items:
        require(key not in out, "duplicate manifest key " + key)
        out[key] = value
    return out

def digest(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()

def branch_edges(method):
    """Validate full direct bytecode conditional/goto destinations, fail closed."""
    rows = method["instructions"]
    positions = [r["offset"] for r in rows]
    require(1 <= len(rows) <= 2200 and positions == sorted(set(positions)),
            "non-canonical method offsets")
    valid = set(positions)
    edges = []
    for pos, row in enumerate(rows):
        op = row["opcode"]
        require(op not in UNSUPPORTED, "unsupported control-flow primitive")
        if not op.startswith(("if", "goto")):
            continue
        argument = row["operand"].split()[0] if row["operand"] else ""
        require(argument.lstrip("-").isdigit(), "branch without integer destination")
        target = int(argument)
        require(target in valid, "invalid JVM branch target")
        edge = {"offset": row["offset"], "opcode": op,
                "operand": row["operand"], "symbol": row["symbol"]}
        if op.startswith("if"):
            require(pos + 1 < len(rows), "conditional without fallthrough")
        edges.append(edge)
    require(len(edges) <= 180, "unexpected branch population")
    return edges

def pivots(method, anchors):
    by_offset = {row["offset"]: row for row in method["instructions"]}
    for offset, marker in anchors:
        row = by_offset.get(offset)
        require(row is not None, "missing exact causal offset " + str(offset))
        require(marker in (row["opcode"] + " " + row["symbol"]),
                "causal pivot changed: " + marker)

def check_nbt_color_only(methods):
    """Check Gumball's *own* NBT overrides, not inherited engine persistence."""
    outputs = {}
    for name in ("addAdditionalSaveData", "readAdditionalSaveData"):
        found = [m for m in methods if name_of(m) == name]
        require(len(found) == 1 and len(found[0]["instructions"]) == 9,
                "Gumball NBT override count changed")
        calls = " ".join(row["symbol"] for row in found[0]["instructions"])
        require("String Color" in calls, "Color serialization changed")
        required = "putInt" if name == "addAdditionalSaveData" else "setColor"
        require(required in calls, "Color save/load pivot changed")
        require(not any(kw in calls for kw in (
            "MAXIMUM_BOUNCES", "BOUNCES", "getMaximumBounces",
            "setMaximumBounces", "getBounces", "setBounces")),
            "Gumball own NBT override now handles bounce state")
        outputs[name] = digest_method(found[0])
    return outputs

def audit(jar: Path, parent_path: Path, state_path: Path, javap_bin: str):
    require(jar.is_file() and sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher JAR identity/size drift")
    parent_bytes = parent_path.read_bytes()
    parent = json.loads(parent_bytes, object_pairs_hook=pairs_unique)
    state = json.loads(state_path.read_bytes(), object_pairs_hook=pairs_unique)
    artifact = {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE}
    require(parent["artifact"] == state["artifact"] == artifact,
            "manifest artifact mismatch")
    require(parent["resources"]["bouncy_ball"]["json"]["max_level"] == 3,
            "Bouncy Ball maximum enchanting level drift")
    require(set(x["class"] for x in parent["owner_classes"]) == set(OWNERS),
            "owner class population drift")
    require({x["class"]: x["sha256"] for x in parent["owner_classes"]} == CLASSES,
            "parent owner identities drift")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate publisher archive entries")
        for owner, sha in CLASSES.items():
            require(digest(z.read(owner)) == sha, "publisher owner class drift")
    published = {c["class_path"]: c for c in state["classes"]}
    require(set(published) == set(OWNERS), "Gumball state owner mismatch")
    method_cache = {}
    for owner in OWNERS:
        rows = parse_methods(javap(javap_bin, jar, owner[:-6].replace("/", ".")))
        require(len(rows) == EXPECTED_METHOD_COUNT[owner] ==
                published[owner]["declared_method_count"],
                "declared class method census drift")
        keys = [(name_of(m), m["descriptor"]) for m in rows]
        require(len(keys) == len(set(keys)), "duplicate JVM method signature")
        for frozen in published[owner]["methods"]:
            original = unique_method(rows, frozen["name"], frozen["descriptor"])
            require(len(original["instructions"]) == frozen["instruction_count"] and
                    digest_method(original) == frozen["parsed_method_sha256"],
                    "prior Gumball state selected method digest drift")
        method_cache[owner] = rows
    consumers = []
    for frozen in parent["selected_consumers"]:
        owner = frozen["owner"]
        native = frozen["method"]
        current = unique_method(method_cache[owner], native["name"],
                                native["descriptor"])
        require(len(current["instructions"]) == native["instruction_count"] and
                digest_method(current) == native["parsed_method_sha256"],
                "Bouncy Ball selected method digest drift")
        actual_edges = branch_edges(current)
        require(actual_edges == native["selected_branches"],
                "sealed branch inventory does not match complete parsed method")
        if native["name"] in EXPECTED_BRANCH_COUNT:
            require(len(actual_edges) == EXPECTED_BRANCH_COUNT[native["name"]],
                    "principal consumer CFG population changed")
        if native["name"] == "acInventoryTick":
            pivots(current, REQUIRED_PRODUCER)
        if native["name"] == "bounceFromDirection":
            pivots(current, REQUIRED_CONSUMER)
        consumers.append({"owner": owner, "name": native["name"],
                          "descriptor": native["descriptor"],
                          "instructions": len(current["instructions"]),
                          "branches": len(actual_edges),
                          "parsed_method_sha256": digest_method(current)})
    require(len(consumers) == 7 and
            {m["name"] for m in consumers if m["name"] in MAIN_METHODS}
            == set(MAIN_METHODS), "incomplete native consumer set")
    own_nbt = check_nbt_color_only(method_cache[BALL])
    return {
        "schema_version": 1,
        "scope": "BOUNCY_BALL_FULL_DECLARED_METHOD_ROSTERS_AND_DIRECT_JVM_BRANCHES",
        "artifact": artifact,
        "parent_manifest_sha256": digest(parent_bytes),
        "state_manifest_sha256": digest(state_path.read_bytes()),
        "classes": [{"path": owner, "sha256": CLASSES[owner],
                     "declared_method_count": len(method_cache[owner])}
                    for owner in OWNERS],
        "selected_consumers": consumers,
        "gumball_own_nbt": {
            "write_method_sha256": own_nbt["addAdditionalSaveData"],
            "read_method_sha256": own_nbt["readAdditionalSaveData"],
            "bounce_state_in_own_overrides": False,
            "inherited_engine_persistence": "NOT_VERIFIED",
        },
        "limits": {
            "interprocedural_exception_flow": "NOT_RECONSTRUCTED",
            "effective_world_replay_and_reload": "NOT_VERIFIED",
            "external_mixins_and_other_jar_consumers": "NOT_VERIFIED",
            "unusual_enchant_levels_and_datapacks": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "certification": "STATIC_TECHNICAL_CATALOG_ONLY",
        }
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.jar, args.parent, args.state, args.javap)
    if args.snapshot is not None:
        old = json.loads(args.snapshot.read_bytes(), object_pairs_hook=pairs_unique)
        require(result == old, "Bouncy Ball causal snapshot mismatch")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
    print("BOUNCY_BALL_CAUSAL=" + json.dumps(result, ensure_ascii=False,
                                            separators=(",", ":")))

if __name__ == "__main__":
    main()
