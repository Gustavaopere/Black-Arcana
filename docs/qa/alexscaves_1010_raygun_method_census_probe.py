#!/usr/bin/env python3
"""Read-only RaygunItem 1.0.10 complete declared-method roster discovery.

Does NOT certify raygun static completeness, packet security, X-Ray behavior,
mutating hooks or physical gameplay. Emits method hashes and branch counts,
never the native code or full bytecode bodies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method
from alexscaves_1010_ferrous_haste_causal_audit import branches

ROOT = Path(__file__).resolve().parents[2]
CONTROL = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-CONTROL-1.0.10.json"
OWNER = "com/github/alexmodguy/alexscaves/server/item/RaygunItem.class"
CLASS_SHA256 = "3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c"
SCOPE = "SHA_EXACT_1010_RAYGUN_ALL_26_DECLARED_METHODS_DISCOVERY_ONLY"

class CensusError(ValueError):
    pass

def require(ok, reason):
    if not ok:
        raise CensusError(reason)

def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, "duplicate JSON key " + key)
        out[key] = value
    return out

def read_prior(path=CONTROL):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)

def census(methods, prior):
    require(prior["scope"] ==
            "SHA_EXACT_1010_RAYGUN_SELECTED_METHOD_REFERENCES_AND_NUMERIC_OPERANDS_ONLY",
            "wrong prior selected-method evidence")
    require(prior["declared_method_count"] == 26,
            "prior declared method count mismatch")
    require(len(methods) == 26, "Raygun declared method population changed")
    by_name = {}
    rows = []
    for method in methods:
        signature = name_of(method) + " " + method["descriptor"]
        require(method["descriptor"] and method["instructions"],
                "missing descriptor or bytecode for " + signature)
        require(signature not in by_name, "duplicate compiled method identity")
        by_name[signature] = method
        edges, switches = branches(method)
        rows.append({
            "method": signature,
            "instructions": len(method["instructions"]),
            "parsed_method_sha256": digest_method(method),
            "direct_branches": len(edges),
            "switch_offsets": switches,
        })
    old = prior["selected_method_digests"]
    require(len(old) == 8, "unexpected prior selected SHA roster")
    for key, digest in old.items():
        require(key in by_name, "selected historical method missing " + key)
        require(digest_method(by_name[key]) == digest,
                "selected historical full-body method drift " + key)
    onuse = next((m for m in rows if m["method"].startswith("onUseTick ")), None)
    require(onuse is not None and onuse["instructions"] == 523,
            "Raygun onUseTick method body drift")
    return {
        "declared_methods": len(rows),
        "historically_sealed_methods": len(old),
        "newly_surveyed_unsealed_methods": len(rows)-len(old),
        "instruction_total": sum(row["instructions"] for row in rows),
        "direct_branch_total": sum(row["direct_branches"] for row in rows),
        "methods": rows,
    }

def audit(jar, javap_binary):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher artifact SHA1/SHA256/size drift")
    prior = read_prior()
    require(prior["artifact"] ==
            {"sha1":SHA1, "sha256":SHA256, "size_bytes":SIZE},
            "prior publisher identity changed")
    require(prior["class_path"] == OWNER and
            prior["class_sha256"] == CLASS_SHA256,
            "prior Raygun class identity changed")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate publisher JAR member")
        native = z.read(OWNER)
        require(native[:4] == b"\xca\xfe\xba\xbe"
                and int.from_bytes(native[6:8], "big") == 65,
                "unexpected JVM major version")
        require(hashlib.sha256(native).hexdigest() == CLASS_SHA256,
                "physical Raygun class hash drift")
    methods = parse_methods(javap(javap_binary, jar, OWNER[:-6].replace("/", ".")))
    result = census(methods, prior)
    return {
        "schema_version":1, "scope":SCOPE,
        "artifact":prior["artifact"], "class_path":OWNER,
        "class_sha256":CLASS_SHA256,
        **result,
        "safety":{
            "discovery_only":True,
            "static_perk_contract":"NOT_CERTIFIED",
            "full_method_roster_unsealed":True,
            "cross_method_reaching_definitions":"NOT_RECONSTRUCTED",
            "exceptional_cfg":"NOT_RECONSTRUCTED",
            "damage_and_effect_acceptance":"NOT_CERTIFIED",
            "packet_sender_binding":"NOT_VERIFIED",
            "provider_universe_closed":False,
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
        }
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    parser.add_argument("--javap",default="javap")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    report=audit(args.jar,args.javap)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(
            json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":"DISCOVERY_PASS_NOT_CERTIFIED",
        "declared_methods":report["declared_methods"],
        "historically_sealed_methods":report["historically_sealed_methods"],
        "newly_surveyed_unsealed_methods":report["newly_surveyed_unsealed_methods"],
        "instructions":report["instruction_total"],
        "branches":report["direct_branch_total"],
        "safety":report["safety"]
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
