#!/usr/bin/env python3
"""Bounded, SHA-exact 1.0.10 Tremorzilla beam world/LOS bytecode evidence.

Read-only clean-room inspection. Symbol references and local CFG are not
provider authorization, protection compatibility, actual game QA or hooks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_tremorzilla_beam_probe import CLASS, CLASS_SHA, method_name, method_digest

METHODS = (
    "tickBreath", "canEntityBeHurtByBeam", "breakBlocksAround",
    "tickBeamTargeting", "getBeamShootFrom", "getMaxBeamBreakLength",
    "setMaxBeamBreakLength",
)
REQUIRED = ("tickBreath", "canEntityBeHurtByBeam", "breakBlocksAround")
MAX_JVM_INSNS = 2900
MAX_REFERENCES = 170
MAX_BRANCHES = 110
MAX_NUMBERS = 100
MAX_REPORT_BYTES = 118000
REF_OPS = (
    "invoke", "getfield", "putfield", "getstatic", "putstatic",
    "new", "instanceof", "checkcast",
)
HINTS = re.compile(
    r"(beam|hurtEntitiesAround|breakBlocksAround|block|clip|collider|fluid|"
    r"level|destroy|damage|grief|charge|target|ray|gameRule|setMaxBeam|"
    r"stun|firing|tick|entity|position|effect|blockPos|air|fluidState)",
    re.IGNORECASE,
)

class TremorzillaWorldEvidenceError(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise TremorzillaWorldEvidenceError(reason)


def extract(methods):
    require(100 <= len(methods) <= 160, "unexpected 1.0.10 class method population")
    names = [(method_name(m), m["descriptor"]) for m in methods]
    require(len(set(names)) == len(names), "duplicate method signature")
    grouped = {}
    for name in METHODS:
        candidates = [m for m in methods if method_name(m) == name]
        require(len(candidates) <= 2, "ambiguous native method overload population")
        if name in REQUIRED:
            require(len(candidates) == 1, "required beam/world method absent: " + name)
        grouped[name] = [compact_method(m) for m in candidates]
    breath = grouped["tickBreath"][0]
    for needle in ("breakBlocksAround:", "hurtEntitiesAround:"):
        require(any(needle in r["symbol"] for r in breath["references"]["rows"]),
                "native beam caller missing a required world/damage boundary: " + needle)
    los = grouped["canEntityBeHurtByBeam"][0]
    require(any("clip:" in r["symbol"] for r in los["references"]["rows"]),
            "native LOS raytrace boundary not demonstrated")
    return grouped


def select_rows(rows, limit):
    require(len(rows) <= 700, "JVM evidence export budget exceeded")
    return {"observed_count": len(rows), "truncated": len(rows) > limit,
            "rows": rows[:limit]}


def compact_method(m):
    instructions = m["instructions"]
    require(1 <= len(instructions) <= MAX_JVM_INSNS, "invalid bounded method body")
    offsets = [i["offset"] for i in instructions]
    require(len(set(offsets)) == len(offsets), "duplicate bytecode offset")
    refs = [{
        "offset": i["offset"], "opcode": i["opcode"],
        "symbol": i["symbol"][:250],
    } for i in instructions
        if i["opcode"].startswith(REF_OPS) and HINTS.search(i["symbol"])]
    branches = [{
        "offset": i["offset"], "opcode": i["opcode"], "operand": i["operand"][:45],
    } for i in instructions if i["opcode"].startswith("if") or
                              i["opcode"].startswith("goto")]
    constants = [{
        "offset": i["offset"], "opcode": i["opcode"],
        "operand": i["operand"][:50], "symbol": i["symbol"][:90],
    } for i in instructions if i["opcode"].startswith(
        ("iconst_", "lconst_", "fconst_", "dconst_", "bipush", "sipush", "ldc"))]
    return {
        "name": method_name(m), "descriptor": m["descriptor"],
        "method_sha256": method_digest(m),
        "instruction_count": len(instructions),
        "references": select_rows(refs, MAX_REFERENCES),
        "branches": select_rows(branches, MAX_BRANCHES),
        "constants": select_rows(constants, MAX_NUMBERS),
    }


def limitations():
    return {
        "loaded_modpack_runtime": "NOT_OBSERVED",
        "world_protection_and_claims": "NOT_VERIFIED",
        "destructive_effect_policy": "NOT_VERIFIED",
        "pvp_and_ownership": "NOT_VERIFIED",
        "raycast_semantics": "BYTECODE_REFERENCES_ONLY",
        "full_interprocedural_cfg": "NOT_RECONSTRUCTED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "static_perk_certification": "NOT_CERTIFIED",
        "mutation": "NO_MUTATION",
    }


def audit(jar, javap_bin):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "exact Alex's Caves publisher JAR checksum drift")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate JAR members")
        require(CLASS in names, "exact Tremorzilla class missing")
        blob = archive.read(CLASS)
        require(hashlib.sha256(blob).hexdigest() == CLASS_SHA,
                "Tremorzilla class checksum drift")
    methods = parse_methods(javap(javap_bin, jar, CLASS[:-6].replace("/", ".")))
    report = {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_TREMORZILLA_WORLD_AND_LOS_ABI_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "class_path": CLASS, "class_sha256": CLASS_SHA,
        "method_count": len(methods),
        "selected": extract(methods),
        "limits": limitations(),
    }
    require(len(json.dumps(report, sort_keys=True).encode("utf-8")) <= MAX_REPORT_BYTES,
            "bounded Tremorzilla world report exceeded")
    return report



def verify_sealed_snapshot(report, seal):
    """Reject method, opcode, literal, identity or status drift."""
    for key in ("schema_version", "scope", "artifact", "class_path",
                "class_sha256", "method_count"):
        require(report.get(key) == seal.get(key),
                "sealed 1.0.10 world/LOS identity drift: " + key)
    require(report.get("limits") == seal.get("limits") == limitations(),
            "unsupported gameplay, hook or QA promotion")
    require(seal.get("interpretation") ==
            "SELECTED_JVM_REFS_AND_LITERALS_ONLY_NO_INFERRED_AUTHORISATION_OR_FINAL_DAMAGE",
            "unverified runtime semantics promoted")
    methods = seal.get("method_signatures_and_digests")
    require(isinstance(methods, list) and len(methods) == 7,
            "wrong selected method seal size")
    signatures = [(m["name"], m["descriptor"]) for m in methods]
    require(len(set(signatures)) == len(signatures),
            "duplicate selected signature")
    observed = {}
    for items in report["selected"].values():
        for m in items:
            key = (m["name"], m["descriptor"])
            require(key not in observed, "duplicate selected method in report")
            observed[key] = m
    for m in methods:
        original = observed.get((m["name"], m["descriptor"]))
        require(original is not None and
                original["method_sha256"] == m["sha256"],
                "selected method descriptor/digest drift: " + m["name"])
    anchors = seal.get("selected_abi_anchors")
    require(isinstance(anchors, list) and 10 <= len(anchors) <= 70,
            "unbounded or empty world/LOS anchor seal")
    seen = set()
    for anchor in anchors:
        key = (anchor["method"], anchor["group"], anchor["offset"])
        require(key not in seen, "duplicate sealed world/LOS site")
        seen.add(key)
        item = next((m for (name, desc), m in observed.items()
                     if name == anchor["method"]), None)
        require(item is not None, "missing sealed method owner")
        group = item[anchor["group"]]
        require(not group["truncated"], "truncated world/LOS anchor group")
        hits = [x for x in group["rows"] if x["offset"] == anchor["offset"]]
        require(len(hits) == 1 and hits[0]["opcode"] == anchor["opcode"]
                and anchor.get("symbol_contains", "") in hits[0]["symbol"]
                and (not anchor.get("operand_equals") or
                     hits[0]["operand"] == anchor["operand_equals"]),
                "world/LOS JVM anchor mismatch: " + anchor["method"])
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.jar, args.javap)
    verify_sealed_snapshot(report, json.loads(args.manifest.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    for name, items in report["selected"].items():
        for item in items:
            print("WORLD_ABI_METHOD=" + name + " " + item["descriptor"]
                  + " SHA256=" + item["method_sha256"]
                  + " refs=" + str(item["references"]["observed_count"])
                  + " branches=" + str(item["branches"]["observed_count"]))
            for ref in item["references"]["rows"]:
                print("WORLD_ABI_REF=" + name + " " + json.dumps(ref, sort_keys=True))
            if name in ("tickBreath", "breakBlocksAround"):
                for row in item["constants"]["rows"]:
                    print("WORLD_ABI_CONST=" + name + " " + json.dumps(row, sort_keys=True))
    print("STATIC_ONLY; NOT_CERTIFIED; NO_MUTATION; PHYSICAL_QA_NOT_TESTED")


if __name__ == "__main__":
    main()
