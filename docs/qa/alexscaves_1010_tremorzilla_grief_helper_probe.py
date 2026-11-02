#!/usr/bin/env python3
"""Read-only, bounded 1.0.10 publisher-native grief/compatibility helper seam.

Class identities, descriptors and method callsites are evidence, not proof
of modpack claims permission, world effect authorization or safe hooks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_tremorzilla_beam_probe import CLASS as TREMOR_CLASS, method_digest, method_name

BASE = "com/github/alexmodguy/alexscaves/server/"
CLASSES = {
    "ACPlatform": BASE + "misc/ACPlatform.class",
    "ACCompat": BASE + "misc/ACCompat.class",
    "TremorzillaEntity": TREMOR_CLASS,
}
SELECTION = {
    "ACPlatform": {
        "canEntityGrief": "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;)Z",
    },
    "ACCompat": {
        "onBlockExploded": "(Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/Explosion;)V",
        "createEntity": "(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/entity/Entity;",
    },
    "TremorzillaEntity": {
        "breakBlocksAround": "(Lnet/minecraft/world/phys/Vec3;FZZF)Z",
    },
}
ANCHORS = (
    (12, "invokestatic", "ACPlatform.canEntityGrief:"),
    (22, "invokevirtual", "Level.isClientSide:"),
    (249, "invokevirtual", "Level.destroyBlock:"),
    (268, "invokestatic", "ACCompat.onBlockExploded:"),
    (296, "invokestatic", "ACCompat.createEntity:"),
    (349, "invokevirtual", "Level.addFreshEntity:"),
)
MAX_REFS = 120
MAX_TRANSFERS = 100
MAX_WINDOWS = 24
MAX_EXPORT = 58000


class GriefHelperEvidenceError(ValueError):
    pass


def require(condition, problem):
    if not condition:
        raise GriefHelperEvidenceError(problem)


def selected(methods, owner, name, descriptor):
    hits = [m for m in methods
            if method_name(m) == name and m["descriptor"] == descriptor]
    require(len(hits) == 1, "exact 1.0.10 method missing/ambiguous: " + owner + "." + name)
    m = hits[0]
    insns = m["instructions"]
    require(1 <= len(insns) <= 2800, "invalid/empty publisher helper bytecode")
    offs = [i["offset"] for i in insns]
    require(offs == sorted(set(offs)), "duplicated/unordered helper bytecode offsets")
    return m


def window(instructions, offset, before=5, after=7):
    match = [i for i, op in enumerate(instructions) if op["offset"] == offset]
    require(len(match) == 1, "missing/duplicated JVM instruction window site")
    index = match[0]
    return {"site": offset,
            "nearby_instructions": instructions[max(0, index-before):index+after+1]}


def bounded(items, limit):
    require(len(items) <= 1100, "helper evidence rows exceed bounded maximum")
    return {"total": len(items), "truncated": len(items) > limit,
            "rows": items[:limit]}


def inspect(m, owner):
    instructions = m["instructions"]
    refs = [x for x in instructions if x["opcode"].startswith(("invoke", "getfield",
                    "getstatic", "putfield", "putstatic", "checkcast", "instanceof"))]
    flow = [x for x in instructions if x["opcode"].startswith(("if", "goto")) or
            x["opcode"] in ("ireturn", "areturn", "return", "athrow")]
    for sequence in (refs, flow):
        require(all(isinstance(x["offset"], int) and x["offset"] >= 0
                    for x in sequence), "invalid helper JVM offsets")
    sites = []
    if owner == "TremorzillaEntity":
        for offset, opcode, symbol_fragment in ANCHORS:
            matches = [i for i in instructions if i["offset"] == offset]
            require(len(matches) == 1 and
                    matches[0]["opcode"] == opcode and
                    symbol_fragment in matches[0]["symbol"],
                    "exact Tremorzilla grief/world ABI callsite drift: " + str(offset))
            if offset in (12, 22):
                sites.append(window(instructions, offset))
    else:
        for op in instructions:
            if op["opcode"].startswith(("invoke", "if")) or op["opcode"] in (
                    "ireturn", "areturn", "return"):
                sites.append(window(instructions, op["offset"], before=2, after=3))
                if len(sites) >= MAX_WINDOWS:
                    break
    return {
        "name": method_name(m), "descriptor": m["descriptor"],
        "method_sha256": method_digest(m),
        "instruction_count": len(instructions),
        "references": bounded(refs, MAX_REFS),
        "branches_and_returns": bounded(flow, MAX_TRANSFERS),
        "selected_windows": sites,
    }


def audit(jar, java):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "exact publisher jar checksum/size mismatch")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate publisher ZIP members")
        digest = {}
        for owner, name in CLASSES.items():
            require(name in names, "missing exact publisher class: " + owner)
            digest[owner] = hashlib.sha256(archive.read(name)).hexdigest()
    classes = []
    for owner, path in CLASSES.items():
        methods = parse_methods(javap(java, jar, path[:-6].replace("/", ".")))
        require(1 <= len(methods) <= 230, "unexpected compiled helper class method population")
        cls = {
            "owner": owner, "class_path": path, "class_sha256": digest[owner],
            "declared_method_count": len(methods),
            "selected_methods": [inspect(selected(methods, owner, n, d), owner)
                                 for n, d in SELECTION[owner].items()],
        }
        classes.append(cls)
    result = {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_NATIVE_GRIEF_AND_COMPAT_HELPER_SELECTED_ABI_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "classes": classes,
        "limits": {
            "full_interprocedural_cfg": "NOT_RECONSTRUCTED",
            "guard_return_semantics": "INSPECTION_REQUIRED",
            "loaded_modpack_claims": "NOT_VERIFIED",
            "world_effect_policy": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "perk_certification": "NOT_CERTIFIED",
        },
    }
    require(len(json.dumps(result, sort_keys=True).encode("utf-8")) <= MAX_EXPORT,
            "helper evidence export budget exceeded")
    return result



def verify_sealed_snapshot(report, seal):
    """Reject artifact/class/method/selected JVM branch and delegation drift."""
    for key in ("schema_version", "scope", "artifact"):
        require(report.get(key) == seal.get(key),
                "exact grief helper evidence identity drift: " + key)
    require(report.get("limits") == seal.get("limits") ==
            {"full_interprocedural_cfg": "NOT_RECONSTRUCTED",
             "guard_return_semantics": "INSPECTION_REQUIRED",
             "loaded_modpack_claims": "NOT_VERIFIED",
             "world_effect_policy": "NOT_VERIFIED",
             "mutating_hook": "NOT_VERIFIED",
             "physical_qa": "NOT_TESTED",
             "mutation": "NO_MUTATION",
             "perk_certification": "NOT_CERTIFIED"},
            "unsupported native helper security or QA promotion")
    require(seal.get("interpretation") ==
            "BYTECODE_DELEGATION_AND_EARLY_RETURN_ONLY_NOT_GLOBAL_CLAIMS_PERMISSION",
            "unsupported permission inference")

    required = seal.get("selected_methods")
    require(isinstance(required, list) and len(required) == 4,
            "invalid selected grievance method population")
    observed = {}
    for cls in report["classes"]:
        for m in cls["selected_methods"]:
            key = (cls["owner"], m["name"], m["descriptor"])
            require(key not in observed, "duplicate publisher helper method")
            observed[key] = (cls, m)
    require(len(observed) == 4, "unexpected publisher helper method universe")
    for target in required:
        key = (target["owner"], target["name"], target["descriptor"])
        require(key in observed, "missing sealed helper owner or method")
        cls, m = observed[key]
        for field in ("class_sha256", "class_path", "declared_method_count"):
            require(cls[field] == target[field],
                    "publisher class metadata drift: " + field)
        for field in ("method_sha256", "instruction_count"):
            require(m[field] == target[field],
                    "native helper descriptor or method hash drift: " + field)
    anchors = seal.get("selected_abi_anchors")
    require(isinstance(anchors, list) and 12 <= len(anchors) <= 60,
            "invalid world/grief selected anchor count")
    used = set()
    for item in anchors:
        key = (item["owner"], item["name"], item["offset"])
        require(key not in used, "duplicate exact grief helper anchor")
        used.add(key)
        matches = [record for (owner, name, descriptor), record in observed.items()
                   if owner == item["owner"] and name == item["name"]]
        require(len(matches) == 1, "missing or ambiguous sealed helper anchor owner")
        cls, m = matches[0]
        rows = []
        for group in ("references", "branches_and_returns"):
            evidence = m[group]
            require(not evidence["truncated"],
                    "truncated publisher helper anchor evidence")
            rows.extend(evidence["rows"])
        if item["owner"] == "TremorzillaEntity":
            for w in m["selected_windows"]:
                rows.extend(w["nearby_instructions"])
        found = [op for op in rows if op["offset"] == item["offset"]]
        require(bool(found) and all(
            op["opcode"] == item["opcode"] and
            item.get("symbol_contains", "") in op["symbol"] and
            ("operand_equals" not in item or op["operand"] == item["operand_equals"])
            for op in found),
            "publisher native helper callsite/branch drift: " + str(key))
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    args = p.parse_args()
    report = audit(args.jar, args.javap)
    verify_sealed_snapshot(report, json.loads(args.manifest.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False,
                                      sort_keys=True) + "\n", encoding="utf-8")
    for cls in report["classes"]:
        print("NATIVE_HELPER_CLASS=" + cls["owner"] + " class_sha256=" +
              cls["class_sha256"] + " declared=" + str(cls["declared_method_count"]))
        for m in cls["selected_methods"]:
            print("NATIVE_HELPER_METHOD=" + cls["owner"] + "." + m["name"] +
                  " sha256=" + m["method_sha256"] + " insns=" +
                  str(m["instruction_count"]))
            for row in m["references"]["rows"]:
                print("NATIVE_HELPER_REF=" + cls["owner"] + "." + m["name"] + " " +
                      json.dumps(row, sort_keys=True))
            for row in m["branches_and_returns"]["rows"]:
                print("NATIVE_HELPER_FLOW=" + cls["owner"] + "." + m["name"] + " " +
                      json.dumps(row, sort_keys=True))
            if cls["owner"] == "TremorzillaEntity":
                for win in m["selected_windows"]:
                    print("NATIVE_HELPER_GUARD_WINDOW=" + json.dumps(win, sort_keys=True))
    print("SHA_EXACT_STATIC_ONLY; NO_CLAIMS_AUTHORITY; NO_MUTATION; NO_PHYSICAL_QA")


if __name__ == "__main__":
    main()
