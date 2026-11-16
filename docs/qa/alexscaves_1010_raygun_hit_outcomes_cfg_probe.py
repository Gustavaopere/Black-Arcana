#!/usr/bin/env python3
"""Raygun 1.0.10: bounded, read-only normal-CFG reachability of hit outcomes.

This probe does not disassemble or redistribute the native implementation in
its report. A bounded normal CFG is not JVM symbolic execution, an exceptional
CFG, authoritative server validation, or evidence that a perk may mutate hits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from collections import deque
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_ferrous_haste_causal_audit import branches
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_all_method_seal import ARTIFACT, OWNER, CLASS_SHA256, SEAL_PATH, load
from alexscaves_1010_raygun_local_flow_probe import DESC, METHOD_SHA256, digest_method

SCOPE = "SHA_EXACT_1010_RAYGUN_HIT_OUTCOMES_BOUNDED_NORMAL_CFG_ONLY"
START, END = 953, 1157
GATES = (1044, 1088, 1122)
GOALS = (1119, 1154)
PINS = {
    1041: ("invokestatic", "ACCompat.hurt:"),
    1044: ("ifeq", "1051"),
    1088: ("ifne", "1157"),
    1119: ("invokevirtual", "LivingEntity.addEffect:"),
    1122: ("ifeq", "1157"),
    1154: ("invokestatic", "AlexsCaves.sendMSGToAll:"),
    1157: ("goto", "953"),
}
MAX_REPORT_BYTES = 16000

class FlowError(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise FlowError(message)

def normal_graph(method):
    """Construct a normal-edge graph; reject switches and unsupported transfers."""
    rows = method["instructions"]
    offsets = [r["offset"] for r in rows]
    require(offsets and offsets == sorted(set(offsets)), "invalid JVM offsets")
    direct, switches = branches(method)
    require(not switches, "switch normal CFG unsupported")
    branch_map = {src: dst for src, dst in direct}
    require(len(branch_map) == len(direct), "duplicate direct branch source")
    graph = {}
    for idx, row in enumerate(rows):
        op, offset = row["opcode"], row["offset"]
        following = rows[idx + 1]["offset"] if idx + 1 < len(rows) else None
        if op.startswith("if"):
            require(offset in branch_map and following is not None, "invalid conditional CFG")
            graph[offset] = (branch_map[offset], following)
        elif op in {"goto", "goto_w"}:
            require(offset in branch_map, "invalid jump CFG")
            graph[offset] = (branch_map[offset],)
        elif op in {"jsr", "jsr_w", "ret", "tableswitch", "lookupswitch"}:
            raise FlowError("unsupported control transfer " + op)
        elif op.endswith("return") or op == "athrow":
            graph[offset] = ()
        else:
            require(following is not None, "unrecognized terminal instruction")
            graph[offset] = (following,)
    require(len(graph) == len(rows), "incomplete normal graph")
    require(all(dst in graph for targets in graph.values() for dst in targets),
            "normal CFG contains missing destination")
    return graph, direct

def shortest_bounded(graph, origin, goal, *, low=START, high=END):
    """Return a path inside one hit-loop slice, stopping before loop back-edge."""
    if not low <= origin < high or not low <= goal < high:
        return None
    require(origin in graph and goal in graph, "missing bounded CFG node")
    queue = deque([origin])
    prior = {origin: None}
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = prior[node]
            return list(reversed(path))
        for nxt in graph[node]:
            if low <= nxt < high and nxt not in prior:
                prior[nxt] = node
                queue.append(nxt)
    return None

def assert_native_pins(method):
    by_offset = {r["offset"]: r for r in method["instructions"]}
    require(len(by_offset) == len(method["instructions"]), "duplicate pinned offset")
    for at, (opcode, token) in PINS.items():
        require(at in by_offset and by_offset[at]["opcode"] == opcode,
                "missing/different JVM opcode @" + str(at))
        row = by_offset[at]
        require(token in (row["symbol"] + " " + row["operand"]),
                "missing/different JVM anchor @" + str(at))

def bounded_projection(graph, instructions):
    """Report graph properties only; no native instructions or full path bodies."""
    offset_map = {row["offset"]: row for row in instructions}
    require(all(n in graph for n in (START, END, *GATES, *GOALS)),
            "missing Raygun bounded CFG anchor")
    results = []
    for gate in GATES:
        row = offset_map[gate]
        require(row["opcode"].startswith("if") and len(graph[gate]) == 2,
                "expected JVM conditional gate @" + str(gate))
        # The first edge is the JVM branch target; the second is fallthrough.
        outcomes = {}
        for label, successor in zip(("branch_taken", "fallthrough"), graph[gate]):
            destination = {}
            for goal in GOALS:
                path = shortest_bounded(graph, successor, goal)
                destination[str(goal)] = {
                    "reachable_in_same_bounded_iteration": path is not None,
                    "shortest_normal_edge_count": None if path is None else len(path) - 1,
                    "conditional_gate_offsets_on_one_shortest_path":
                        [] if path is None else [
                            p for p in path[:-1] if offset_map[p]["opcode"].startswith("if")
                        ],
                }
            outcomes[label] = {
                "successor_offset": successor,
                "downstream": destination,
            }
        results.append({
            "guard_offset": gate,
            "guard_opcode": row["opcode"],
            "outcomes": outcomes,
        })
    reach_from_head = {
        str(k): shortest_bounded(graph, START, k) is not None
        for k in (*GATES, *GOALS)
    }
    # A bounded slice may have externally entering edges; record this limitation.
    entering = sum(1 for a, targets in graph.items() if not START <= a < END
                   for b in targets if START <= b < END)
    exiting = sum(1 for a, targets in graph.items() if START <= a < END
                  for b in targets if not START <= b < END)
    return {
        "bounded_offsets": [START, END],
        "slice_instruction_count": sum(START <= n < END for n in graph),
        "normal_edges_entering_slice_from_outside": entering,
        "normal_edges_exiting_slice": exiting,
        "head_reachability": reach_from_head,
        "conditional_outcome_paths": results,
    }

def audit(jar: Path, javap_bin: str):
    require(sha_file(jar) == (SHA1, SHA256, SIZE), "publisher JAR identity drift")
    seal = load(SEAL_PATH)
    require(seal["artifact"] == ARTIFACT and seal["class_path"] == OWNER
            and seal["class_sha256"] == CLASS_SHA256 and len(seal["methods"]) == 26,
            "Raygun 26-method identity seal drift")
    with zipfile.ZipFile(jar) as archive:
        require(hashlib.sha256(archive.read(OWNER)).hexdigest() == CLASS_SHA256,
                "publisher Raygun class SHA drift")
    parsed = parse_methods(javap(javap_bin, jar, OWNER[:-6].replace("/", ".")))
    require(len(parsed) == 26, "Raygun class method population drift")
    found = {}
    for row in parsed:
        identity = name_of(row) + " " + row["descriptor"]
        require(identity not in found, "duplicate method identity")
        found[identity] = row
    for historical in seal["methods"]:
        key = historical["method"]
        require(key in found, "missing historical Raygun method")
        method = found[key]
        direct, switches = branches(method)
        require(historical["parsed_method_sha256"] == digest_method(method)
                and historical["instructions"] == len(method["instructions"])
                and historical["direct_branches"] == len(direct)
                and historical["switch_offsets"] == switches,
                "historical method body seal drift " + key)
    key = "onUseTick " + DESC
    require(key in found, "onUseTick descriptor absent")
    method = found[key]
    require(digest_method(method) == METHOD_SHA256
            and len(method["instructions"]) == 523,
            "onUseTick body SHA/count drift")
    graph, direct = normal_graph(method)
    require(len(direct) == 57, "onUseTick direct branch population drift")
    assert_native_pins(method)
    report = {
        "schema_version": 1,
        "scope": SCOPE,
        "artifact": ARTIFACT,
        "class_path": OWNER,
        "class_sha256": CLASS_SHA256,
        "method": key,
        "method_parsed_sha256": METHOD_SHA256,
        "method_instructions": 523,
        "method_direct_branches": 57,
        "graph_method_instructions": len(graph),
        "observations": bounded_projection(graph, method["instructions"]),
        "limits": {
            "graph": "NORMAL_EDGES_ONLY_NO_EXCEPTIONAL_OR_DYNAMIC_DISPATCH",
            "trace": "INTRA_ITERATION_REACHABILITY_NOT_EXECUTION_OR_EFFECT_ACCEPTANCE",
            "local_slots_and_reaching_definitions": "NOT_RECONSTRUCTED",
            "cross_iteration_consequences": "NOT_CERTIFIED",
            "server_authority_and_C2S": "NOT_VERIFIED",
            "world_protection_PvP_claims": "NOT_VERIFIED",
            "perk_static_contract": "NOT_CERTIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
        },
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf8")) < MAX_REPORT_BYTES,
            "bounded clean-room output budget exceeded")
    return report

def verify_snapshot(observed, snapshot):
    require(observed == snapshot, "Raygun bounded normal CFG seal drift")
    return observed

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--javap", default="javap")
    p.add_argument("--output", type=Path)
    p.add_argument("--snapshot", type=Path)
    p.add_argument("--print-candidate", action="store_true")
    args = p.parse_args()
    result = audit(args.jar, args.javap)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf8")
    if args.snapshot:
        verify_snapshot(result, load(args.snapshot))
    if args.print_candidate:
        print("RAYGUN_HIT_OUTCOMES_BEGIN")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("RAYGUN_HIT_OUTCOMES_END")
    print(json.dumps({
        "status": "SHA_EXACT_BOUND_CFG_SEALED" if args.snapshot
                  else "UNSEALED_DISCOVERY_ONLY",
        "graph_nodes": len(result["observations"]["head_reachability"]),
        "guard_cases": len(result["observations"]["conditional_outcome_paths"]),
        "mutation": result["limits"]["mutation"],
    }))

if __name__ == "__main__":
    main()
