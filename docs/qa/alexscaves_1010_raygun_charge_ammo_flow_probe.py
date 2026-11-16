#!/usr/bin/env python3
"""Read-only Raygun 1.0.10 charge/ammo/use flow: selected JVM call/branch evidence.

Replays the complete 26-method publisher class fingerprint seal first, then
extracts bounded facts for the 8 charging/ammo/activation-related methods.
No source or complete native bytecode is exported. No gameplay, security,
server authority, mutating perk hooks, or static perk-ready is certified.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_ferrous_haste_causal_audit import branches
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_all_method_seal import (
    ARTIFACT, CLASS_SHA256, OWNER, SEAL_PATH, load, require,
)
from alexscaves_1010_raygun_local_flow_probe import digest_method

SCOPE = "SHA_EXACT_1010_RAYGUN_CHARGE_AMMO_USE_SELECTED_CFG_DISCOVERY_ONLY"
METHODS = (
    "hasCharge", "use", "findAmmo", "getUseDuration",
    "getCharge", "setCharge", "releaseUsing", "lambda$static$0"
)
COUNTS = {
    "hasCharge": (8, 2), "use": (78, 4), "findAmmo": (27, 4),
    "getUseDuration": (2, 0), "getCharge": (11, 2),
    "setCharge": (11, 0), "releaseUsing": (20, 1),
    "lambda$static$0": (11, 2),
}
SELECTED_OPS = {
    "getstatic", "putstatic", "getfield", "putfield",
    "ldc", "ldc_w", "sipush", "bipush",
}
MAX_REPORT = 48000

def method_site(method):
    """Project a single method into fingerprints, CFG edges and bounded references."""
    ins = method["instructions"]
    require(ins, "empty method cannot be inventoried")
    offsets = [row["offset"] for row in ins]
    require(offsets == sorted(set(offsets)), "invalid method instruction order")
    edge_pairs, switches = branches(method)
    require(not switches, "unexpected JVM switch in charge/ammo subset")
    sites = []
    for row in ins:
        if row["opcode"].startswith("invoke") or row["opcode"] in SELECTED_OPS:
            sites.append({
                "offset": row["offset"], "opcode": row["opcode"],
                "operand": row["operand"][:100], "symbol": row["symbol"][:450],
            })
    require(len(sites) <= 85, "method symbolic evidence budget exceeded")
    return {
        "method": name_of(method) + " " + method["descriptor"],
        "instructions": len(ins),
        "parsed_method_sha256": digest_method(method),
        "direct_branch_edges": edge_pairs,
        "selected_references_and_constants": sites,
    }

def audit(jar: Path, javap_bin: str):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher physical JAR drift")
    seal = load(SEAL_PATH)
    require(seal["artifact"] == ARTIFACT and seal["class_path"] == OWNER
            and seal["class_sha256"] == CLASS_SHA256
            and seal["scope"] ==
            "SHA_EXACT_1010_RAYGUN_26_METHOD_BODY_FINGERPRINTS_ONLY",
            "upstream 26-method fingerprint seal identity drift")
    with zipfile.ZipFile(jar) as z:
        raw = z.read(OWNER)
        import hashlib
        require(hashlib.sha256(raw).hexdigest() == CLASS_SHA256,
                "physical Raygun class SHA drift")
    parsed = parse_methods(javap(javap_bin, jar, OWNER[:-6].replace("/", ".")))
    require(len(parsed) == len(seal["methods"]) == 26,
            "full native method population changed")
    native = {}
    for m in parsed:
        ident = name_of(m) + " " + m["descriptor"]
        require(ident not in native, "duplicate JVM method signature")
        native[ident] = m
    for old in seal["methods"]:
        ident = old["method"]
        require(ident in native, "26-method historical identity absent")
        m = native[ident]
        edges, switches = branches(m)
        require(old["parsed_method_sha256"] == digest_method(m)
                and old["instructions"] == len(m["instructions"])
                and old["direct_branches"] == len(edges)
                and old["switch_offsets"] == switches,
                "SHA-exact 26-method prior seal changed: " + ident)
    selected = []
    for name in METHODS:
        found = [(key, m) for key, m in native.items()
                 if key.split(" ", 1)[0] == name]
        require(len(found) == 1, "missing/overloaded charge-ammo method " + name)
        _key, method = found[0]
        item = method_site(method)
        instr, branches_count = COUNTS[name]
        require(item["instructions"] == instr
                and len(item["direct_branch_edges"]) == branches_count,
                "native branch topology changed for " + name)
        selected.append(item)
    require(sum(x["instructions"] for x in selected) == 168
            and sum(len(x["direct_branch_edges"]) for x in selected) == 15,
            "selected charge/ammo population arithmetic drift")
    report = {
        "schema_version": 1,
        "scope": SCOPE,
        "artifact": ARTIFACT,
        "class_path": OWNER,
        "class_sha256": CLASS_SHA256,
        "upstream_26_method_seal": SEAL_PATH.name,
        "selected_methods": selected,
        "selected_instruction_total": 168,
        "selected_branch_total": 15,
        "safety": {
            "static_perk_contract": "NOT_CERTIFIED",
            "source_implementation_redistributed": False,
            "server_charge_authority": "NOT_VERIFIED",
            "c2s_entity_authorization": "NOT_VERIFIED",
            "charge_used_bounds": "NOT_VERIFIED",
            "cross_method_dataflow": "NOT_RECONSTRUCTED",
            "native_damage_applied": "NOT_CERTIFIED",
            "physical_qa": "NOT_TESTED",
            "mutating_hook": "NOT_VERIFIED",
            "provider_universe_closed": False,
            "mutation": "NO_MUTATION",
        },
    }
    require(len(json.dumps(report,ensure_ascii=False).encode("utf8")) <= MAX_REPORT,
            "bounded evidence output budget")
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--print-candidate", action="store_true")
    args = parser.parse_args()
    report = audit(args.jar, args.javap)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",
                               encoding="utf8")
    if args.print_candidate:
        print("RAYGUN_CHARGE_AMMO_FLOW_BEGIN")
        print(json.dumps(report,indent=2,ensure_ascii=False))
        print("RAYGUN_CHARGE_AMMO_FLOW_END")
    print(json.dumps({
        "status": "DISCOVERY_PASS_NOT_CERTIFIED",
        "methods": len(report["selected_methods"]),
        "instructions": report["selected_instruction_total"],
        "direct_branches": report["selected_branch_total"],
        "safety": report["safety"],
    },ensure_ascii=False))

if __name__ == "__main__":
    main()
