#!/usr/bin/env python3
"""SHA-exact Raygun 1.0.10 post-hurt conditional guard discovery.

Read-only, bounded instruction-site windows and normal-graph reachability.
No native method bodies are redistributed. A syntactically reachable path
does not prove executable path predicates, status acceptance, or a safe perk.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import javap, parse_methods
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_all_method_seal import OWNER, ARTIFACT, CLASS_SHA256, load
from alexscaves_1010_raygun_local_flow_probe import DESC, METHOD_SHA256, digest_method
from alexscaves_1010_raygun_hit_outcomes_cfg_probe import (
    audit as baseline_audit, normal_graph, shortest_bounded,
    verify_snapshot as verify_baseline_snapshot, require,
)

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / ("wiki/modpack-catalog/providers/✅-alexs-caves-continued/"
                   "EXACT-RAYGUN-HIT-OUTCOMES-CFG-1.0.10.json")
SCOPE = "SHA_EXACT_1010_RAYGUN_POST_HURT_CONDITION_GUARD_WINDOWS_ONLY"
GUARDS = (1044, 1056, 1064, 1088)
GOALS = (1088, 1119, 1154)
WINDOW_START, WINDOW_END = 1013, 1091
MAX_REPORT_BYTES = 15000

def site(row):
    """A bounded JVM site; discard unused attributes and cap symbols."""
    return {
        "offset": row["offset"],
        "opcode": row["opcode"],
        "operand": row["operand"][:96],
        "symbol": row["symbol"][:240],
    }

def guard_projection(rows, graph):
    """Project only bounded native guard windows and reachability."""
    positions = {row["offset"]: i for i, row in enumerate(rows)}
    require(len(positions) == len(rows), "duplicate JVM offsets in guard projection")
    require(all(offset in positions for offset in GUARDS + GOALS),
            "missing post-hurt JVM sites")
    guard_rows = []
    for offset in GUARDS:
        idx = positions[offset]
        row = rows[idx]
        require(row["opcode"].startswith("if") and len(graph[offset]) == 2,
                "expected post-hurt conditional @" + str(offset))
        require(WINDOW_START <= offset < WINDOW_END, "guard outside audited window")
        # Deliberately short: context, not a third-party method listing.
        previous = rows[max(idx - 5, 0):idx]
        after = rows[idx + 1:idx + 3]
        edges = []
        for label, successor in zip(("taken", "fallthrough"), graph[offset]):
            reach = {}
            for goal in GOALS:
                path = shortest_bounded(graph, successor, goal)
                reach[str(goal)] = {
                    "reachable": path is not None,
                    "shortest_normal_edges": None if path is None else len(path) - 1,
                }
            edges.append({
                "outcome": label,
                "successor": successor,
                "downstream": reach,
            })
        guard_rows.append({
            "offset": offset,
            "opcode": row["opcode"],
            "destination": graph[offset][0],
            "fallthrough": graph[offset][1],
            "predecessor_window": [site(x) for x in previous],
            "following_window": [site(x) for x in after],
            "outcomes": edges,
        })
    calls = [site(row) for row in rows
             if WINDOW_START <= row["offset"] < WINDOW_END
             and row["opcode"].startswith(("invoke",))]
    require(len(calls) <= 24, "oversized post-hurt call population")
    summary = {
        "observed_window": [WINDOW_START, WINDOW_END],
        "window_instruction_count": sum(WINDOW_START <= row["offset"] < WINDOW_END for row in rows),
        "guard_count": len(guard_rows),
        "guard_observations": guard_rows,
        "invocation_sites_in_window": calls,
    }
    return summary

def analyze(method):
    graph, branches = normal_graph(method)
    require(len(method["instructions"]) == 523 and len(branches) == 57,
            "Raygun onUseTick method topology drift")
    return guard_projection(method["instructions"], graph)

def audit(jar: Path, javap_bin: str):
    # Re-run the entire publisher/JAR/class/26-method seal from PR #1102.
    observed = baseline_audit(jar, javap_bin)
    verify_baseline_snapshot(observed, load(BASELINE))
    parsed = parse_methods(javap(javap_bin, jar, OWNER[:-6].replace("/", ".")))
    require(len(parsed) == 26, "publisher Raygun method roster drift")
    hits = [row for row in parsed if name_of(row) == "onUseTick" and row["descriptor"] == DESC]
    require(len(hits) == 1, "ambiguous Raygun onUseTick overload")
    m = hits[0]
    require(digest_method(m) == METHOD_SHA256, "publisher onUseTick method digest drift")
    report = {
        "schema_version": 1,
        "scope": SCOPE,
        "artifact": ARTIFACT,
        "class_path": OWNER,
        "class_sha256": CLASS_SHA256,
        "method_descriptor": DESC,
        "method_parsed_sha256": METHOD_SHA256,
        "upstream_hit_outcomes_manifest": BASELINE.name,
        "observations": analyze(m),
        "limits": {
            "predicate_reaching_definitions": "NOT_RECONSTRUCTED",
            "stack_dataflow": "NOT_RECONSTRUCTED",
            "exception_edges_and_dynamic_dispatch": "NOT_RECONSTRUCTED",
            "normal_path_reachability": "POSSIBLE_NOT_EXECUTION_PROOF",
            "damage_success_versus_status_success": "NOT_VERIFIED_IN_GAME",
            "server_authority_and_c2s": "NOT_VERIFIED",
            "pvp_claims_and_effective_datapack": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "static_perk_contract": "NOT_CERTIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
        },
    }
    encoded = json.dumps(report, ensure_ascii=False)
    require(len(encoded.encode("utf8")) < MAX_REPORT_BYTES,
            "bounded clean-room report size exceeded")
    return report

def verify_snapshot(report, snapshot):
    require(report == snapshot, "Raygun post-hurt guard window snapshot drift")
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path)
    p.add_argument("--snapshot", type=Path)
    p.add_argument("--print-candidate", action="store_true")
    args = p.parse_args()
    result = audit(args.jar, args.javap)
    if args.snapshot:
        verify_snapshot(result, load(args.snapshot))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf8")
    if args.print_candidate:
        print("RAYGUN_POST_HURT_GUARDS_BEGIN")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("RAYGUN_POST_HURT_GUARDS_END")
    print(json.dumps({
        "result": "SHA_EXACT_POST_HURT_GUARDS_SEALED" if args.snapshot
                  else "UNSEALED_DISCOVERY_ONLY",
        "guards": result["observations"]["guard_count"],
        "window_instructions": result["observations"]["window_instruction_count"],
        "mutation": result["limits"]["mutation"],
    }))

if __name__ == "__main__":
    main()
