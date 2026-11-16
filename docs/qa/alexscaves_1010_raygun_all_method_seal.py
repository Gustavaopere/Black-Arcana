#!/usr/bin/env python3
"""SHA-exact Raygun 1.0.10 all-method fingerprint seal, read-only.

Input is the live JAR replay report from raygun_method_census_probe.py, not
source code or hand-entered opcodes. Produces bounded method identity/digest
metadata; no physical game or runtime mutation is certified.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from alexscaves_1010_raygun_method_census_probe import CensusError, unique_pairs

ROOT = Path(__file__).resolve().parents[2]
SEAL_PATH = (ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
             / "EXACT-RAYGUN-ALL-METHODS-1.0.10.json")
SCOPE = "SHA_EXACT_1010_RAYGUN_26_METHOD_BODY_FINGERPRINTS_ONLY"
PRIOR_SCOPE = "SHA_EXACT_1010_RAYGUN_ALL_26_DECLARED_METHODS_DISCOVERY_ONLY"
ARTIFACT = {
    "sha1": "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570",
    "sha256": "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c",
    "size_bytes": 75279314,
}
OWNER = "com/github/alexmodguy/alexscaves/server/item/RaygunItem.class"
CLASS_SHA256 = "3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c"
HEX = re.compile(r"[0-9a-f]{64}\Z")
LIMITS = {
    "claim_scope": "METHOD_FINGERPRINTS_NOT_COMPLETE_STATIC_PERK_CONTRACT",
    "method_roster": "JAR_1010_ONLY",
    "cross_method_reaching_definitions": "NOT_RECONSTRUCTED",
    "exception_cfg": "NOT_RECONSTRUCTED",
    "source_version_1_1_1": "NON_AUTHORITATIVE",
    "damage_and_status_acceptance": "NOT_CERTIFIED",
    "packet_sender_authorization": "NOT_VERIFIED",
    "pvp_los_claims": "NOT_VERIFIED",
    "provider_universe_closed": False,
    "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "mutation": "NO_MUTATION",
}

def require(value, reason):
    if not value:
        raise CensusError(reason)

def load(path):
    return json.loads(path.read_text(encoding="utf8"), object_pairs_hook=unique_pairs)

def projection(report):
    require(report.get("schema_version") == 1
            and report.get("scope") == PRIOR_SCOPE,
            "unrecognized unsealed JAR survey")
    require(report.get("artifact") == ARTIFACT
            and report.get("class_path") == OWNER
            and report.get("class_sha256") == CLASS_SHA256,
            "unrecognized publisher Raygun class")
    require((report.get("declared_methods"),
             report.get("historically_sealed_methods"),
             report.get("newly_surveyed_unsealed_methods"),
             report.get("instruction_total"),
             report.get("direct_branch_total")) == (26, 8, 18, 1111, 107),
            "unrecognized full method population/census")
    safety = report.get("safety")
    require(isinstance(safety, dict)
            and safety.get("discovery_only") is True
            and safety.get("static_perk_contract") == "NOT_CERTIFIED"
            and safety.get("full_method_roster_unsealed") is True
            and safety.get("packet_sender_binding") == "NOT_VERIFIED"
            and safety.get("mutating_hook") == "NOT_VERIFIED"
            and safety.get("physical_qa") == "NOT_TESTED"
            and safety.get("mutation") == "NO_MUTATION",
            "input improperly promoted runtime, hook or static contract")
    rows = report.get("methods")
    require(isinstance(rows, list) and len(rows) == 26,
            "incomplete method digest roster")
    seen = set()
    encoded = []
    for row in rows:
        require(isinstance(row, dict)
                and set(row) == {"method", "instructions", "direct_branches",
                                 "parsed_method_sha256", "switch_offsets"},
                "invalid method fingerprint record")
        method = row["method"]
        require(isinstance(method, str) and " " in method and method not in seen
                and len(method) <= 500,
                "empty, duplicated or unsafe method identity")
        seen.add(method)
        require(type(row["instructions"]) is int and row["instructions"] >= 1
                and type(row["direct_branches"]) is int
                and 0 <= row["direct_branches"] <= row["instructions"],
                "invalid method instruction or branch count")
        require(isinstance(row["parsed_method_sha256"], str)
                and HEX.fullmatch(row["parsed_method_sha256"]),
                "invalid full body fingerprint")
        offsets = row["switch_offsets"]
        require(isinstance(offsets, list)
                and len(offsets) <= row["instructions"]
                and all(type(i) is int and i >= 0 for i in offsets)
                and offsets == sorted(set(offsets)),
                "invalid JVM switch offsets")
        encoded.append(dict(row))
    require(sum(r["instructions"] for r in encoded) == 1111
            and sum(r["direct_branches"] for r in encoded) == 107,
            "method population totals inconsistent")
    onuse = [r for r in encoded if r["method"].startswith("onUseTick ")]
    require(len(onuse) == 1 and onuse[0]["instructions"] == 523,
            "onUseTick JAR signature/body drift")
    return {
        "schema_version": 1,
        "scope": SCOPE,
        "artifact": ARTIFACT,
        "class_path": OWNER,
        "class_sha256": CLASS_SHA256,
        "declared_methods": 26,
        "historically_pinned_method_digests": 8,
        "newly_pinned_method_digests": 18,
        "instruction_total": 1111,
        "direct_branch_total": 107,
        "methods": encoded,
        "limits": LIMITS,
    }

def verify(report, frozen):
    expected = projection(report)
    require(frozen == expected, "Raygun full-method fingerprint seal drift")
    return expected

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True, type=Path)
    ap.add_argument("--seal", type=Path)
    ap.add_argument("--print-candidate", action="store_true")
    args = ap.parse_args()
    report = load(args.report)
    candidate = projection(report)
    if args.seal:
        verify(report, load(args.seal))
    if args.print_candidate:
        print("RAYGUN_METHOD_SEAL_BEGIN")
        print(json.dumps(candidate, ensure_ascii=False, indent=2))
        print("RAYGUN_METHOD_SEAL_END")
    print(json.dumps({
        "status": "SEALED_SHA_EXACT_METHOD_ROSTER" if args.seal
                  else "CANDIDATE_ONLY_NOT_CERTIFIED",
        "methods": 26, "instructions": 1111, "branches": 107,
        "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
