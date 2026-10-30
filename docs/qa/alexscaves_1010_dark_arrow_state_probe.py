#!/usr/bin/env python3
"""Read-only SHA-exact audit of Dark Arrow state read/write references.

The publisher JAR 1.0.10 is verified by SHA-1, SHA-256 and size. This inventories
symbolic JVM references; it does not execute Minecraft, derive effective damage,
infer writers through reflection, or certify a mutating hook.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, BASE, sha_file, javap, parse_methods
)

ARROW = BASE + "server/entity/item/DarkArrowEntity.class"
ARROW_HASH = "089f0a65444078ca42fc1da2d5023384314ef5f5283ddf3fe8484bf31d4136ad"
TOKENS = (b"DarkArrowEntity", b"SHADOW_ARROW_DAMAGE", b"PERFECT_SHOT")
FIELDS = ("SHADOW_ARROW_DAMAGE", "PERFECT_SHOT")
ARROW_METHODS = ("getShadowArrowDamage", "isPerfectShot", "setShadowArrowDamage",
                 "setPerfectShot")
CANDIDATE_MAX = 100
SELECTED_MAX = 110
WINDOW_MAX = 140
PER_METHOD_MAX = 30
IMPORTANT = (
    "SHADOW_ARROW_DAMAGE", "PERFECT_SHOT", "DarkArrowEntity.",
    "SynchedEntityData.set:", "SynchedEntityData.get:",
    "SynchedEntityData$Builder.define:", "SynchedEntityData$Builder.",
    "setShadowArrowDamage", "setPerfectShot",
)


class ProbeError(ValueError):
    pass


def strict_pairs(pairs):
    doc = {}
    for key, val in pairs:
        if key in doc:
            raise ProbeError("duplicate JSON key: " + key)
        doc[key] = val
    return doc


def field_offsets(method):
    return [
        i for i, ins in enumerate(method["instructions"])
        if any(s in ins["symbol"] for s in FIELDS)
    ]


def relevant_offsets(method, is_arrow):
    insns = method["instructions"]
    found = []
    for i, ins in enumerate(insns):
        if any(symbol in ins["symbol"] for symbol in IMPORTANT):
            found.append(i)
    if not is_arrow and not any("DarkArrowEntity." in insns[i]["symbol"] for i in found):
        return []
    if is_arrow:
        own_decl = any(re.search(r"\b"+re.escape(name)+r"\(", method["header"])
                       for name in ARROW_METHODS)
        if not own_decl and not field_offsets(method):
            return []
        if own_decl and not found:
            found = [0]   # explicit method declaration: still no invented field access
    if len(found) > PER_METHOD_MAX:
        raise ProbeError("too many anchor sites in method")
    return found


def method_record(m, indices):
    ins = m["instructions"]
    if not ins or len(ins) > 5000:
        raise ProbeError("empty or oversized method")
    if len({x["offset"] for x in ins}) != len(ins):
        raise ProbeError("duplicate JVM offsets")
    windows = []
    for index in indices:
        item = ins[index]
        windows.append({
            "offset": item["offset"], "opcode": item["opcode"],
            "operand": item["operand"], "symbol": item["symbol"],
            "nearby": [
                {k: x[k] for k in ("offset", "opcode", "operand", "symbol")}
                for x in ins[max(0, index-5):min(len(ins), index+8)]
            ]
        })
    return {
        "method_header": m["header"],
        "descriptor": m["descriptor"],
        "parsed_instruction_count": len(ins),
        "parsed_method_sha256": hashlib.sha256(
            json.dumps(m, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "anchors": windows,
        "control_flow_reachability": "NOT_PROVEN",
    }


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise ProbeError("exact publisher JAR pin mismatch")
    with zipfile.ZipFile(jar) as arc:
        infos = arc.infolist()
        if len(infos) != len({entry.filename for entry in infos}):
            raise ProbeError("duplicate ZIP member")
        if hashlib.sha256(arc.read(ARROW)).hexdigest() != ARROW_HASH:
            raise ProbeError("prior SHA-exact DarkArrowEntity class pin mismatch")
        candidates = []
        for info in infos:
            if not (info.filename.startswith(BASE) and info.filename.endswith(".class")):
                continue
            # Classfile constant pool string presence is only a candidate filter.
            if info.file_size > 250_000:
                raise ProbeError("unexpected oversized provider class")
            data = arc.read(info)
            if any(token in data for token in TOKENS):
                candidates.append((info.filename, hashlib.sha256(data).hexdigest()))
        if len(candidates) > CANDIDATE_MAX or len(candidates) < 1:
            raise ProbeError("candidate class population not bounded")
        candidates.sort()
        selected = []
        anchors = 0
        for path, digest in candidates:
            methods = parse_methods(javap(javap_bin, jar, path[:-6].replace("/", ".")))
            group = []
            for method in methods:
                locations = relevant_offsets(method, path==ARROW)
                if locations:
                    row = method_record(method, locations)
                    group.append(row)
                    anchors += len(locations)
            if group:
                selected.append({"class": path, "sha256": digest, "methods": group})
        if len(selected) > SELECTED_MAX or anchors > WINDOW_MAX:
            raise ProbeError("selected class/anchor budget exceeded")
    if not any(x["class"]==ARROW for x in selected):
        raise ProbeError("no self-class field/getter anchor found")
    return {
        "schema_version": 1,
        "scope": "EXACT_ALEXSCAVES_1010_DARK_ARROW_SYMBOLIC_STATE_FLOW_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "dark_arrow_class_sha256": ARROW_HASH,
        "candidate_classes": len(candidates),
        "selected_classes": selected,
        "total_symbolic_anchors": anchors,
        "limits": {
            "candidate_filter": "CONSTANT_POOL_TOKEN_ONLY",
            "runtime_writers": "NOT_CERTIFIED",
            "dataflow_and_cfg": "NOT_RECONSTRUCTED",
            "inherited_dispatch_and_reflection": "NOT_COVERED",
            "final_damage_and_hit_counts": "NOT_VERIFIED",
            "owner_and_protections": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "complete_perk_ready": False,
            "provider_universe_closed": False
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--snapshot")
    parser.add_argument("--output", required=True)
    opts = parser.parse_args()
    result = audit(opts.jar, opts.javap)
    if opts.snapshot:
        snapshot = json.loads(Path(opts.snapshot).read_text(encoding="utf-8"),
                              object_pairs_hook=strict_pairs)
        if result != snapshot:
            raise ProbeError("tracked state-flow snapshot differs from SHA-exact JAR")
    output = Path(opts.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2,
                                 sort_keys=True)+"\n", encoding="utf-8")
    print("DARK_ARROW_1010_BEGIN")
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
    print("DARK_ARROW_1010_END")
    print("candidate_classes=" + str(result["candidate_classes"]) +
          " selected_classes=" + str(len(result["selected_classes"])) +
          " anchor_count=" + str(result["total_symbolic_anchors"]) +
          " STATIC_ONLY_NO_MUTATION")


if __name__ == "__main__":
    main()
