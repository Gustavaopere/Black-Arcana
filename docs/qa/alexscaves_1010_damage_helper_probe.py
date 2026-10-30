#!/usr/bin/env python3
"""Exact 1.0.10 selected damage helper ABI & bounded instruction evidence.

All observations originate from a hash-verified publisher JAR. This disassembly
probe is read-only interoperability research, NOT gameplay or hook homologation.
No full copied methods, no control flow solver, no decompiler, no runtime claims.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)

ROOT = BASE + "server/"
SPECS = (
    (ROOT + "misc/ACCompat.class", "hurt",
     "(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z"),
    (ROOT + "misc/ACCompat.class", "enchantLevel",
     "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/resources/ResourceKey;)I"),
    (ROOT + "entity/living/ForsakenEntity.class", "getSonicDamageAgainst",
     "(Lnet/minecraft/world/entity/LivingEntity;)F"),
    (ROOT + "entity/item/DarkArrowEntity.class", "getShadowArrowDamage", "()F"),
    (ROOT + "entity/item/DarkArrowEntity.class", "isPerfectShot", "()Z"),
)
EXPECTED_PRIOR = {
    "ForsakenAttackGoal.class": ("getSonicDamageAgainst",),
    "DarkArrowEntity.class": ("getShadowArrowDamage", "isPerfectShot",
                               "ACCompat.hurt"),
    "DesolateDaggerEntity.class": ("ACCompat.hurt", "ACCompat.enchantLevel"),
}
MAX_INSNS = 1900
MAX_ANCHORS = 450
RETURNS = {"ireturn", "lreturn", "freturn", "dreturn", "areturn", "return"}
ARITHMETIC = {
    "iadd", "isub", "imul", "idiv", "irem",
    "ladd", "lsub", "lmul", "ldiv",
    "fadd", "fsub", "fmul", "fdiv", "frem", "fneg",
    "dadd", "dsub", "dmul", "ddiv", "drem", "dneg",
    "i2f", "d2f", "f2d", "f2i", "i2d", "d2i",
}
CONSTANTS = re.compile(r"^(?:[ifld]const_|bipush$|sipush$|ldc(?:_w|2_w)?$)")
NAME_PATTERN = re.compile(r"(?<![\w$]){name}\(")


class EvidenceMismatch(ValueError):
    pass


def strict_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise EvidenceMismatch("duplicate JSON key: " + key)
        obj[key] = value
    return obj


def load_prior(path):
    obj = json.loads(Path(path).read_text(encoding="utf8"),
                     object_pairs_hook=strict_pairs)
    if obj.get("scope") != "SHA_EXACT_1010_SELECTED_DAMAGE_CALLSITE_INSTRUCTION_WINDOWS_ONLY":
        raise EvidenceMismatch("wrong preceding path-anchor scope")
    if obj.get("artifact") != {
        "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE
    }:
        raise EvidenceMismatch("prior hash pin differs from publisher artifact")
    previous = {}
    for item in obj.get("selected_classes", []):
        filename = item["class_path"].split("/")[-1]
        if filename in previous:
            raise EvidenceMismatch("duplicate prior class")
        previous[filename] = item
    for filename, helper_names in EXPECTED_PRIOR.items():
        item = previous.get(filename)
        if not item:
            raise EvidenceMismatch("missing prior " + filename)
        # Earlier SHA-exact evidence must actually mention each desired helper.
        # The preceding probe's filtered symbolic list intentionally omits
        # some helper names (e.g. isPerfectShot/enchantLevel). Its hash-pinned
        # factory instruction windows retain those exact method references.
        symbol_text = "\n".join(
            anchor["symbol"]
            for method in item["methods"]
            for anchor in (
                method["selected_symbolic_invocations"] +
                [inst for window in method["factory_windows"]
                 for inst in window["surrounding_instructions"]]
            )
        )
        for name in helper_names:
            if name not in symbol_text:
                raise EvidenceMismatch("unanchored helper " + filename + ":" + name)
    return previous


def method_named(method, name, descriptor):
    return (
        bool(re.search(NAME_PATTERN.pattern.format(name=re.escape(name)),
                       method["header"]))
        and method["descriptor"] == descriptor
    )


def select_method(methods, name, descriptor):
    candidates = [m for m in methods if method_named(m, name, descriptor)]
    if len(candidates) != 1:
        raise EvidenceMismatch("exact JVM method missing/ambiguous: " + name + descriptor)
    method = candidates[0]
    insns = method["instructions"]
    if not 1 <= len(insns) <= MAX_INSNS:
        raise EvidenceMismatch("method instruction budget exceeded: " + name)
    offsets = [i["offset"] for i in insns]
    if len(offsets) != len(set(offsets)):
        raise EvidenceMismatch("duplicate bytecode offsets")
    return method


def compact_instruction(item):
    return {k: item[k] for k in ("offset", "opcode", "operand", "symbol")}


def summarize_method(method):
    insns = method["instructions"]
    refs = []
    branches = []
    numeric = []
    math = []
    returns = []
    for idx, x in enumerate(insns):
        op = x["opcode"]
        if op.startswith("invoke") or op in ("getfield", "getstatic",
                                              "putfield", "putstatic"):
            refs.append(compact_instruction(x))
        if op.startswith("if") or op in ("goto", "goto_w", "tableswitch",
                                          "lookupswitch"):
            operand = x["operand"]
            branches.append({
                "offset": x["offset"], "opcode": op, "operand": operand,
                "simple_target": int(operand) if operand.isdecimal() else None
            })
        if CONSTANTS.match(op):
            numeric.append(compact_instruction(x))
        if op in ARITHMETIC:
            math.append(compact_instruction(x))
        if op in RETURNS:
            returns.append({
                "offset": x["offset"], "opcode": op,
                "local_instruction_window": [
                    compact_instruction(y) for y in insns[max(0, idx - 12):idx + 1]
                ],
            })
    if any(len(items) > MAX_ANCHORS for items in
           (refs, branches, numeric, math, returns)):
        raise EvidenceMismatch("method anchor budget exceeded")
    return {
        "header": method["header"],
        "descriptor": method["descriptor"],
        "instruction_count": len(insns),
        "parsed_method_sha256": hashlib.sha256(json.dumps(
            method, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode("utf8")).hexdigest(),
        "invoked_methods_and_fields": refs,
        "branch_opcodes": branches,
        "numeric_constants": numeric,
        "arithmetic_opcodes": math,
        "return_windows": returns,
        "semantics_and_effective_values": "NOT_CERTIFIED",
        "hook_mutation_contract": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
    }


def extract(jar, javap_bin, prior):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise EvidenceMismatch("publisher JAR hash/size mismatch")
    grouped = collections.defaultdict(list)
    for class_path, method_name, descriptor in SPECS:
        grouped[class_path].append((method_name, descriptor))
    output = []
    with zipfile.ZipFile(jar) as arc:
        names = arc.namelist()
        if len(names) != len(set(names)):
            raise EvidenceMismatch("duplicate ZIP entry")
        for path, targets in sorted(grouped.items()):
            member = arc.read(path)
            class_hash = hashlib.sha256(member).hexdigest()
            prior_class = prior.get(path.split("/")[-1])
            if prior_class and class_hash != prior_class["class_sha256"]:
                raise EvidenceMismatch("prior class hash mismatch")
            methods = parse_methods(javap(javap_bin, jar, path[:-6].replace("/", ".")))
            observed = []
            for name, descriptor in targets:
                method = select_method(methods, name, descriptor)
                observed.append({"name": name, **summarize_method(method)})
            output.append({
                "class_path": path,
                "class_sha256": class_hash,
                "methods": observed
            })
    return {
        "schema_version": 1,
        "scope": "EXACT_ALEXSCAVES_1010_SELECTED_DAMAGE_HELPER_ABI_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "upstream_anchor": "damage-types/EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json",
        "classes": output,
        "limitations": {
            "method_body_copied": False,
            "selected_methods_only": True,
            "control_flow_reachability": "NOT_PROVEN",
            "dynamic_damage_and_hit_count": "NOT_VERIFIED",
            "effective_targeting_and_PvP": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "complete_perk_ready": False,
            "provider_universe_closed": False,
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--prior", required=True)
    p.add_argument("--snapshot")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    result = extract(args.jar, args.javap, load_prior(args.prior))
    if args.snapshot:
        previous = json.loads(Path(args.snapshot).read_text(encoding="utf8"),
                              object_pairs_hook=strict_pairs)
        if previous != result:
            raise EvidenceMismatch("tracked exact helper ABI snapshot differs from JAR")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
                      + "\n", encoding="utf8")
    print("ALEXSCAVES_HELPERS_1010_BEGIN")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    print("ALEXSCAVES_HELPERS_1010_END")
    print("classes=" + str(len(result["classes"])) +
          " helper_methods=" + str(sum(len(c["methods"]) for c in result["classes"])) +
          " STATIC_ONLY_NO_HOOK_CERTIFICATION")


if __name__ == "__main__":
    main()
