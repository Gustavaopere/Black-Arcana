#!/usr/bin/env python3
"""Bounded exact-JAR bytecode anchors near Alex's Caves 1.0.10 damage factories.

Read-only interoperability research. Anchors, branch operands and symbol references
are not a proven control-flow graph, runtime effect, mutating hook, or damage formula.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file, callsites
)

PROVIDER = "com/github/alexmodguy/alexscaves/"
TARGETS = (
    PROVIDER + "server/entity/ai/ForsakenAttackGoal.class",
    PROVIDER + "server/entity/item/DarkArrowEntity.class",
    PROVIDER + "server/entity/item/DesolateDaggerEntity.class",
    PROVIDER + "server/entity/item/NuclearExplosionEntity.class",
)
# These are deliberately chosen from the previous SHA-exact 12-class audit.
ANCHOR_BEFORE = 14
ANCHOR_AFTER = 18
SYMBOL_HINT = re.compile(
    r"(?i)(?:hurt|damage|hit|target|owner|player|entity|collision|explode|"
    r"explosion|radius|discard|kill|block|knockback|fire|invulnerable)"
)


class ProbeError(ValueError):
    pass


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProbeError("duplicate JSON key: " + key)
        result[key] = value
    return result


def load_earlier(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"),
                     object_pairs_hook=strict_pairs)
    if (doc.get("scope") != "EXACT_1_0_10_BYTECODE_DIRECT_CALLSITES_ONLY"
            or doc.get("artifact") != {
                "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE
            }):
        raise ProbeError("earlier direct-callsite manifest is not the exact artifact")
    roster = {x["class"]: x for x in doc["direct_calling_classes"]}
    if len(roster) != len(doc["direct_calling_classes"]):
        raise ProbeError("duplicate prior class")
    if not set(TARGETS) <= set(roster):
        raise ProbeError("one or more selected classes missing from sealed prior manifest")
    return roster


def branch_anchors(insns):
    out = []
    for item in insns:
        opcode = item["opcode"]
        if opcode.startswith("if") or opcode in (
            "goto", "goto_w", "jsr", "jsr_w", "tableswitch", "lookupswitch"
        ):
            operand = item["operand"]
            # This is a textual destination only. Exception edges, switch rows
            # and stack/data-flow are NOT recovered by this probe.
            dest = int(operand) if re.fullmatch(r"\d+", operand) else None
            out.append({
                "offset": item["offset"], "opcode": opcode,
                "operand": operand, "simple_target": dest,
            })
    if len(out) > 600:
        raise ProbeError("branch anchor bound exceeded")
    return out


def risk_calls(insns):
    hits = [
        {"offset": item["offset"], "opcode": item["opcode"],
         "symbol": item["symbol"]}
        for item in insns
        if item["opcode"].startswith("invoke")
        and SYMBOL_HINT.search(item["symbol"])
    ]
    if len(hits) > 350:
        raise ProbeError("symbol anchor bound exceeded")
    return hits


def select_context(method, sites):
    insns = method["instructions"]
    if not 1 <= len(insns) <= 3500:
        raise ProbeError("method instruction size out of bounds")
    if len({x["offset"] for x in insns}) != len(insns):
        raise ProbeError("duplicate bytecode offset")
    offsets = {entry["offset"]: i for i, entry in enumerate(insns)}
    windows = []
    for site in sites:
        offset = site["bytecode_offset"]
        if offset not in offsets:
            raise ProbeError("missing pinned invocation offset " + str(offset))
        center = offsets[offset]
        observed = insns[center]
        if observed["opcode"] != site["opcode"]:
            raise ProbeError("pinned invocation opcode drift")
        target_symbol = "ACDamageTypes." + site["factory_name"] + ":" + site["factory_descriptor"]
        if target_symbol not in observed["symbol"]:
            raise ProbeError("pinned invocation target drift at " + str(offset))
        windows.append({
            "factory_name": site["factory_name"],
            "factory_descriptor": site["factory_descriptor"],
            "invocation_offset": offset,
            "surrounding_instructions": insns[
                max(0, center - ANCHOR_BEFORE):
                min(len(insns), center + ANCHOR_AFTER + 1)
            ],
        })
    method_hash = hashlib.sha256(
        json.dumps({
            "header": method["header"], "descriptor": method["descriptor"],
            "instructions": insns
        }, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return {
        "method_header": method["header"],
        "method_descriptor": method["descriptor"],
        "parsed_instruction_count": len(insns),
        "full_method_parsed_sha256": method_hash,
        "factory_windows": windows,
        "branch_opcode_anchors": branch_anchors(insns),
        "selected_symbolic_invocations": risk_calls(insns),
        "method_semantics": "NOT_PROVEN_FROM_ANCHORS",
    }


def extract(jar, javap_bin, previous):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise ProbeError("publisher JAR SHA-1/SHA-256/size mismatch")
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        if len(names) != len(set(names)):
            raise ProbeError("duplicate ZIP entries")
        out = []
        for cls in TARGETS:
            prior = previous[cls]
            member = arc.read(cls)
            observed_hash = hashlib.sha256(member).hexdigest()
            if observed_hash != prior["sha256"]:
                raise ProbeError("prior class hash drift: " + cls)
            dotted = cls[:-6].replace("/", ".")
            methods = parse_methods(javap(javap_bin, jar, dotted))
            actual_sites = callsites(methods, owner=cls[:-6])
            expected_sites = prior["direct_factory_calls"]
            if actual_sites != expected_sites:
                raise ProbeError("compiled direct calls differ from previous SHA-exact manifest: " + cls)
            selected = []
            keys = {(c["caller_header"], c["caller_descriptor"]) for c in expected_sites}
            for header, desc in sorted(keys):
                candidates = [
                    m for m in methods
                    if (m["header"], m["descriptor"]) == (header, desc)
                ]
                if len(candidates) != 1:
                    raise ProbeError("consumer method missing/ambiguous: " + cls + " " + header)
                method_sites = [
                    s for s in expected_sites
                    if (s["caller_header"], s["caller_descriptor"]) == (header, desc)
                ]
                selected.append(select_context(candidates[0], method_sites))
            out.append({
                "class_path": cls, "class_sha256": observed_hash,
                "methods": selected
            })
    return {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_SELECTED_DAMAGE_CALLSITE_INSTRUCTION_WINDOWS_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "parent_manifest": "damage-types/EXACT-CONSUMERS-1.0.10.json",
        "selected_classes": out,
        "limits": {
            "not_entire_provider": True,
            "exception_edges_and_switch_dispatch": "NOT_RECONSTRUCTED",
            "control_flow_reachability": "NOT_PROVEN",
            "dynamic_hit_counts": "NOT_VERIFIED",
            "runtime_damage_amounts": "NOT_VERIFIED",
            "target_filters_and_world_protection": "NOT_VERIFIED",
            "source_attribution_and_pvp": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "complete_perk_ready": False,
            "provider_universe_closed": False
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--earlier", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--snapshot")
    args = p.parse_args()
    evidence = extract(args.jar, args.javap, load_earlier(args.earlier))
    if args.snapshot:
        frozen = json.loads(Path(args.snapshot).read_text(encoding="utf-8"),
                            object_pairs_hook=strict_pairs)
        if frozen != evidence:
            raise ProbeError("exact-JAR instruction-anchor snapshot drift")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2,
                                 sort_keys=True) + "\n", encoding="utf-8")
    print("ALEXSCAVES_PATH_ANCHORS_BEGIN")
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")))
    print("ALEXSCAVES_PATH_ANCHORS_END")
    print("classes=" + str(len(evidence["selected_classes"]))
          + " windows=" + str(sum(len(m["factory_windows"])
             for c in evidence["selected_classes"] for m in c["methods"]))
          + " NO_RUNTIME_OR_HOOK_CERTIFICATION")


if __name__ == "__main__":
    main()
