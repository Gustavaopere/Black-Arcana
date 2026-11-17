#!/usr/bin/env python3
"""SHA-exact, clean-room Alex's Mobs 2.1.13 Dimensional Carver portal lifecycle.

Inspects class ABI and bounded JVM operand windows. This is NOT runtime,
permission, claim protection, safe mutation or physical-teleport certification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import javap, parse_methods, sha_file

SHA1 = "50ddafdf3d12b33331e4eecb4ab514ae451baadd"
SHA256 = "eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8"
SIZE = 27452738
BASE = "com/github/alexthe666/alexsmobs/"
CARVER = BASE + "item/ItemDimensionalCarver.class"
PORTAL = BASE + "entity/EntityVoidPortal.class"
NAMES = {
    CARVER: ("onUseTick", "use", "onPortalOpen", "releaseUsingImpl",
             "rayTracePortal", "getUseDuration"),
}
PORTAL_NAME = re.compile(
    r"(?:tick|portal|teleport|lifespan|life|destination|attach|"
    r"save|load|interact|touch|remove|discard|synched|data|entity|player)",
    re.I,
)
REFERENCE = re.compile(
    r"(?:lifespan|destination|attach|teleport|dimension|"
    r"discard|addFreshEntity|hurtAndBreak|isClientSide|"
    r"distanceToSqr|getRespawn|getSleepingPos|"
    r"cooldown|defineId|entityData|synched|setLifespan|"
    r"EntityVoidPortal)",
    re.I,
)
SCHEMA = "SHA_EXACT_ALEXSMOBS_213_CARVER_PORTAL_LIFECYCLE_JVM_BOUNDARY_READONLY"
MAX_METHODS = 45
MAX_REFS_METHOD = 54
MAX_TOTAL_REFERENCES = 265
MAX_REPORT_BYTES = 105000


class PortalProbeError(ValueError):
    pass


def require(predicate, message):
    if not predicate:
        raise PortalProbeError(message)


def name_of(method):
    return method["header"].split("(", 1)[0].split()[-1].rsplit(".", 1)[-1]


def method_hash(method):
    return hashlib.sha256(json.dumps(method, sort_keys=True, ensure_ascii=False,
        separators=(",", ":")).encode("utf8")).hexdigest()


def small(row):
    return {
        "offset": row["offset"], "opcode": row["opcode"],
        "operand": row["operand"][:48], "symbol": row["symbol"][:240],
    }


def bounded_operator_window(method, start, end):
    """Keep selected branch/operand facts, not a method body or source."""
    require(start < end and end - start <= 100, "unbounded lifecycle operator window")
    allowed = {
        "bipush", "sipush", "ldc", "ldc_w", "ldc2_w",
        "iadd", "isub", "imul", "idiv", "irem",
        "iconst_0", "iconst_1", "iconst_2", "aconst_null",
        "dup", "pop", "checkcast", "instanceof",
    }
    items = [
        small(ins) for ins in method["instructions"]
        if start <= ins["offset"] < end and
        (ins["opcode"].startswith(("if", "goto", "invoke", "iload", "istore",
                                  "aload", "astore")) or
         ins["opcode"] in allowed or
         ins["opcode"].startswith(("getfield", "putfield", "getstatic", "putstatic")))
    ]
    require(len(items) <= 64, "too many selected lifecycle operators")
    return items


def selected_method(method):
    ins = method["instructions"]
    require(0 < len(ins) <= 3000, "empty/oversize selected JVM method")
    offsets = [x["offset"] for x in ins]
    require(offsets == sorted(set(offsets)), "duplicated/reordered JVM offsets")
    sites = [
        (j, x) for j, x in enumerate(ins)
        if (REFERENCE.search(x["symbol"]) or REFERENCE.search(x["operand"])
            and x["opcode"] in {"ldc", "ldc_w"})
        and (x["opcode"].startswith("invoke") or x["opcode"] in {
            "getfield", "putfield", "getstatic", "putstatic", "new",
            "instanceof", "checkcast", "ldc", "ldc_w",
        })
    ]
    require(len(sites) <= MAX_REFS_METHOD,
            "unbounded native portal references in method " + name_of(method) +
            " (" + str(len(sites)) + ")")
    branches = []
    for x in ins:
        if not x["opcode"].startswith(("if", "goto")):
            continue
        parts = x["operand"].split()
        require(parts and parts[0].lstrip("-").isdigit(),
                "unparseable native JVM conditional destination")
        branches.append({"offset": x["offset"], "opcode": x["opcode"],
                         "branch_target": int(parts[0])})
    require(len(branches) <= 85, "unbounded JVM branch count")
    return {
        "name": name_of(method), "descriptor": method["descriptor"],
        "method_sha256": method_hash(method),
        "instruction_count": len(ins),
        "branch_count": len(branches), "branches": branches,
        "references": [
            {"site": small(x), "predecessor": small(ins[j-1]) if j > 0 else None,
             "successor": small(ins[j+1]) if j+1 < len(ins) else None}
            for j, x in sites
        ],
    }


def projection(class_methods):
    result = []
    total_refs = 0
    for path in (CARVER, PORTAL):
        methods = class_methods[path]
        require(1 <= len(methods) <= 85, "unknown portal/carver method population")
        all_signatures = [(name_of(m), m["descriptor"]) for m in methods]
        require(len(all_signatures) == len(set(all_signatures)),
                "duplicated native JVM method descriptor")
        if path == CARVER:
            chosen = [m for m in methods if name_of(m) in NAMES[path]]
            require(set(NAMES[path]) == {name_of(m) for m in chosen},
                    "previously documented Carver method missing")
        else:
            chosen = [m for m in methods if PORTAL_NAME.search(name_of(m))
                      and m["instructions"]]
            require(chosen, "portal lifecycle method discovery empty")
        require(len(chosen) <= MAX_METHODS, "unbounded selected native methods")
        items = [selected_method(m) for m in chosen]
        total_refs += sum(len(m["references"]) for m in items)
        windows = []
        if path == PORTAL:
            tick = [m for m in chosen if name_of(m) == "tick"]
            require(len(tick) == 1, "portal tick JVM identity absent or ambiguous")
            for start, end in ((0, 35), (530, 576), (675, 718), (850, 942)):
                windows.append({"start": start, "end": end,
                                "selected_operators":
                                    bounded_operator_window(tick[0], start, end)})
        result.append({
            "class_path": path, "declared_method_count": len(methods),
            "selected_method_count": len(items),
            "tick_operator_windows": windows,
            "selected_methods": items,
            "method_roster": [{
                "name": name_of(m), "descriptor": m["descriptor"],
                "instruction_count": len(m["instructions"])
            } for m in methods],
        })
    require(total_refs <= MAX_TOTAL_REFERENCES,
            "unbounded two-class portal reference export")
    carver = result[0]["selected_methods"]
    required = {"onUseTick", "onPortalOpen", "releaseUsingImpl", "rayTracePortal"}
    require(required.issubset({m["name"] for m in carver}), "Carver surface incomplete")
    require(any("EntityVoidPortal" in r["site"]["symbol"]
                for m in carver for r in m["references"]),
            "Carver portal reference not visible")
    return {"classes": result, "bounded_reference_sites": total_refs}


def audit(jar, javap_bin):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "physical publisher 2.1.13 hash/size mismatch")
    fingerprints = {}
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate publisher ZIP members")
        for path in (CARVER, PORTAL):
            require(path in names, "missing exact provider class "+path)
            raw = archive.read(path)
            require(raw[:4] == b"\xca\xfe\xba\xbe"
                    and int.from_bytes(raw[6:8], "big") == 65,
                    "unsupported provider classfile version "+path)
            fingerprints[path] = hashlib.sha256(raw).hexdigest()
    methods = {path: parse_methods(javap(
        javap_bin, jar, path[:-6].replace("/", ".")))
        for path in (CARVER, PORTAL)}
    output = projection(methods)
    for row in output["classes"]:
        row["class_sha256"] = fingerprints[row["class_path"]]
    result = {
        "schema_version": 1, "scope": SCHEMA,
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "observations": output,
        "limits": {
            "static_bytecode_only": True,
            "effective_teleport_and_claims": "NOT_VERIFIED",
            "runtime_dimension_destination": "NOT_OBSERVED",
            "portal_spawn_accepted": "NOT_TESTED",
            "portal_save_load_and_reconnect": "NOT_TESTED",
            "multi_client_owner_authorization": "NOT_VERIFIED",
            "exception_edges_interprocedural_cfg": "NOT_ANALYZED",
            "mutating_hook": "NOT_VERIFIED",
            "static_perk_contract": "NOT_CERTIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "publisher_universe_closed": False,
        }
    }
    require(len(json.dumps(result, ensure_ascii=False).encode("utf8")) <= MAX_REPORT_BYTES,
            "clean-room report byte budget exceeded")
    return result


def verify_snapshot(result, expected):
    require(result == expected, "SHA-exact portal/carver snapshot drift")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--print-candidate", action="store_true")
    args = parser.parse_args()
    result = audit(args.jar, args.javap)
    if args.snapshot:
        verify_snapshot(result, json.loads(args.snapshot.read_text(encoding="utf8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n",
                           encoding="utf8")
    if args.print_candidate:
        print("CARVER_PORTAL_EVIDENCE_BEGIN")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("CARVER_PORTAL_EVIDENCE_END")
    print(json.dumps({
        "result": ("SHA_EXACT_PORTAL_LIFECYCLE_SEALED" if args.snapshot else
                   "UNSEALED_PORTAL_LIFECYCLE_DISCOVERY"),
        "classes": len(result["observations"]["classes"]),
        "refs": result["observations"]["bounded_reference_sites"],
        "mutation": "NO_MUTATION",
    }))


if __name__ == "__main__":
    main()
