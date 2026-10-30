#!/usr/bin/env python3
"""Read-only, hash-pinned JVM decision anchors in DreadbowItem 1.0.10.

This is a bounded interoperability audit, not disassembly redistribution,
execution-path proof, bytecode modification, or a verified perk hook.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, BASE, javap, parse_methods, sha_file
)

CLASS = BASE + "server/item/DreadbowItem.class"
CLASS_SHA256 = "b9cd6e843f923877775e38b89214e8649c10d4d5be704ed9dd377900439d44ae"
DESCRIPTORS = {
    "releaseUsing": "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V",
    "onUseTick": "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V",
}
PREVIOUS_HASHES = {
    "releaseUsing": "5d4e8c88df5b5c0442c67f6d7f81e0a674a223d87e6d7b1b75894e34fe4742aa",
    "onUseTick": "377ba9047604044c07dcffcc1ada989e83c4074b0140481588e958dc9fb5db18",
}
SITES = {
    "releaseUsing": (
        (383, "DarkArrowEntity", "<init>"),
        (402, "DarkArrowEntity", "setShadowArrowDamage"),
        (409, "DarkArrowEntity", "setPerfectShot"),
    ),
    "onUseTick": (
        (188, "DarkArrowEntity", "<init>"),
        (196, "DarkArrowEntity", "setShadowArrowDamage"),
    ),
}
BRANCHES = ("goto", "goto_w", "tableswitch", "lookupswitch")
CONSTANTS = re.compile(r"^(?:[difl]const_[0-9m]+|bipush|sipush|ldc(?:_w|2_w)?)$")
READ = re.compile(r"^(?:iload|istore)(?:_(\d+))?$")


class DecisionAuditError(ValueError):
    pass


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DecisionAuditError("duplicate JSON key: " + key)
        result[key] = value
    return result


def method_digest(m):
    return hashlib.sha256(json.dumps(m, sort_keys=True, ensure_ascii=False,
                    separators=(",", ":")).encode("utf8")).hexdigest()


def method_lookup(methods, name, descriptor):
    matches = [m for m in methods
               if re.search(r"\b" + name + r"\(", m["header"])
               and m["descriptor"] == descriptor]
    if len(matches) != 1:
        raise DecisionAuditError("exact declared method missing or ambiguous: " + name)
    return matches[0]


def local8_10(instruction):
    """Identify exact javap iload/istore local slots, not string substrings."""
    op = instruction["opcode"]
    m = READ.match(op)
    if not m:
        return None
    slot = int(m.group(1)) if m.group(1) is not None else (
        int(instruction["operand"]) if re.fullmatch(r"\d+", instruction["operand"]) else -1
    )
    return slot if slot in (8, 10) else None


def clipped_window(instructions, index, before=8, after=8):
    return [{key: ins[key] for key in ("offset", "opcode", "operand", "symbol")}
            for ins in instructions[max(0, index-before):min(len(instructions),index+after+1)]]


def matches_invocation_symbol(symbol, klass, name):
    """Normalize javap display quotes around <init> without changing ABI."""
    return klass + "." + name + ":" in symbol.replace('"', "")


def describe_method(method, label):
    insns = method["instructions"]
    if not 1 <= len(insns) <= 1800:
        raise DecisionAuditError("method instruction budget exceeded")
    if len({x["offset"] for x in insns}) != len(insns):
        raise DecisionAuditError("duplicate bytecode offsets")
    if method_digest(method) != PREVIOUS_HASHES[label]:
        raise DecisionAuditError("previous sealed method digest drift: " + label)
    at_offset = {item["offset"]: ix for ix, item in enumerate(insns)}
    sites = []
    for offset, klass, name in SITES[label]:
        if offset not in at_offset:
            raise DecisionAuditError("previous exact call offset missing")
        ix = at_offset[offset]
        inst = insns[ix]
        if not inst["opcode"].startswith("invoke") or (
            not matches_invocation_symbol(inst["symbol"], klass, name)):
            raise DecisionAuditError("exact invocation target drift: " + str(offset))
        sites.append({
            "offset": offset, "symbol": inst["symbol"],
            "window": clipped_window(insns, ix, 8, 8),
        })
    branch = [
        {"offset": i["offset"], "opcode": i["opcode"],
         "operand": i["operand"],
         "simple_target": (int(i["operand"]) if i["operand"].isdecimal() else None)}
        for i in insns if i["opcode"].startswith("if") or i["opcode"] in BRANCHES
    ]
    symbols = [
        {"offset": i["offset"], "opcode": i["opcode"], "symbol": i["symbol"]}
        for i in insns if i["opcode"].startswith("invoke") or
        i["opcode"] in ("getfield", "getstatic", "putfield", "putstatic")
    ]
    constants = [
        {"offset": i["offset"], "opcode": i["opcode"],
         "operand": i["operand"], "symbol": i["symbol"]}
        for i in insns if CONSTANTS.match(i["opcode"])
    ]
    locals_a = [
        {"offset": i["offset"], "opcode": i["opcode"], "slot": local8_10(i),
         "window": clipped_window(insns, idx, 10, 6)}
        for idx, i in enumerate(insns) if local8_10(i) is not None
    ] if label == "releaseUsing" else []
    if (len(branch) > 140 or len(symbols) > 200 or len(constants) > 200 or
            len(locals_a) > 40):
        raise DecisionAuditError("anchor budget exceeded")
    return {
        "method_header": method["header"], "descriptor": method["descriptor"],
        "parsed_method_sha256": method_digest(method),
        "instruction_count": len(insns),
        "direct_dark_arrow_sites": sites,
        "branch_opcode_anchors": branch,
        "symbolic_calls_and_fields": symbols,
        "constant_opcode_anchors": constants,
        "integer_slot_8_and_10_windows": locals_a,
        "dataflow_and_branch_reachability": "NOT_PROVEN",
    }


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise DecisionAuditError("publisher JAR SHA-1/SHA-256/size mismatch")
    with zipfile.ZipFile(jar) as arc:
        if len(arc.namelist()) != len(set(arc.namelist())):
            raise DecisionAuditError("duplicate JAR members")
        member = arc.read(CLASS)
        if hashlib.sha256(member).hexdigest() != CLASS_SHA256:
            raise DecisionAuditError("Dreadbow exact class SHA drift")
    parsed = parse_methods(javap(javap_bin, jar, CLASS[:-6].replace("/", ".")))
    result = {
        name: describe_method(method_lookup(parsed,name,descriptor),name)
        for name, descriptor in DESCRIPTORS.items()
    }
    return {
        "schema_version": 1,
        "scope": "EXACT_1010_DREADBOW_SELECTED_CONTROL_DECISION_ANCHORS_ONLY",
        "publisher_artifact": {
            "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "class_path": CLASS, "class_sha256": CLASS_SHA256,
        "methods": result,
        "limits": {
            "executed_paths_and_target_counts": "NOT_VERIFIED",
            "semantic_origin_of_int_slots": "NOT_CERTIFIED_FROM_ANCHORS",
            "full_cfg_exception_paths": "NOT_RECONSTRUCTED",
            "projectile_damage_applied": "NOT_VERIFIED",
            "multiplayer_pvp_and_permissions": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "complete_perk_ready": False,
            "provider_universe_closed": False,
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar",required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--snapshot")
    args=p.parse_args()
    output=audit(args.jar,args.javap)
    if args.snapshot:
        expected=json.loads(Path(args.snapshot).read_text(encoding="utf-8"),
                            object_pairs_hook=strict_pairs)
        if output != expected:
            raise DecisionAuditError("tracked exact JAR Dreadbow decision evidence drift")
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(output,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                    encoding="utf-8")
    print("DREADBOW_DECISIONS_1010_BEGIN")
    print(json.dumps(output,ensure_ascii=False,sort_keys=True,separators=(",",":")))
    print("DREADBOW_DECISIONS_1010_END")
    print("methods=2 direct_dark_arrow_sites=5 STATIC_ONLY_NO_MUTATION")

if __name__ == "__main__":
    main()
