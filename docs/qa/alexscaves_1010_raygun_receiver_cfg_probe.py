#!/usr/bin/env python3
"""Read-only bounded CFG and operand-source survey of exact Raygun C2S handler.

Purpose: determine whether direct callsites & branches support an interoperability
contract. This is not a proof of payload authorization, gameplay QA or an exploit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_raygun_receiver_probe import PACKET, HANDLE, method_by_sig, ANCHORS
from alexscaves_1010_raygun_receiver_identity_probe import digest_method

ANCHOR_OFFSETS = tuple(sorted(ANCHORS["handle"]))
BRANCH_OPCODE = re.compile(r"^(?:if[a-z0-9_]*|goto|goto_w)$")
REFERENCE_OPCODES = {"getfield", "putfield", "getstatic", "putstatic", "instanceof", "checkcast", "ldc", "ldc_w"}


class CfgProbeError(ValueError):
    pass


def require(x, why):
    if not x:
        raise CfgProbeError(why)


def successors(instructions):
    """Normal JVM branch successors only; excludes exception edges and dataflow."""
    offsets = [row["offset"] for row in instructions]
    require(len(offsets) == len(set(offsets)), "duplicate JVM instruction offsets")
    require(offsets == sorted(offsets), "JVM instruction offset order changed")
    idx = {offset: i for i, offset in enumerate(offsets)}
    edges = {}
    branches = []
    for i, row in enumerate(instructions):
        opcode, offset = row["opcode"], row["offset"]
        nextoff = offsets[i + 1] if i + 1 < len(offsets) else None
        if BRANCH_OPCODE.fullmatch(opcode):
            try:
                destination = int(row["operand"].split()[0])
            except (IndexError, ValueError):
                raise CfgProbeError("invalid JVM branch target")
            require(destination in idx, "branch target is not an instruction")
            edges[offset] = [destination]
            if opcode.startswith("if") and nextoff is not None:
                edges[offset].append(nextoff)
            branches.append({"offset": offset, "opcode": opcode,
                             "branch_target": destination,
                             "fallthrough": nextoff if opcode.startswith("if") else None})
        elif opcode in ("areturn", "ireturn", "return", "athrow", "lreturn", "dreturn", "freturn"):
            edges[offset] = []
        else:
            edges[offset] = [nextoff] if nextoff is not None else []
    require(1 <= len(branches) <= 32, "branch count unbounded/missing")
    return edges, branches


def reachable(edges, start):
    seen, stack = set(), [start]
    while stack:
        pos = stack.pop()
        if pos in seen:
            continue
        seen.add(pos)
        stack.extend(e for e in edges[pos] if e not in seen)
    return seen


def dominating_offsets(edges, start, sink):
    """Control-flow dominance, not a dataflow/ownership or safety assertion."""
    nodes = reachable(edges, start)
    require(sink in nodes, "native update dispatch unreachable from entry")
    predecessors = {n: set() for n in nodes}
    for n in nodes:
        for dest in edges[n]:
            if dest in nodes:
                predecessors[dest].add(n)
    dominators = {n: set(nodes) if n != start else {start} for n in nodes}
    for _ in range(len(nodes) + 1):
        changed = False
        for n in sorted(nodes - {start}):
            incoming = predecessors[n]
            updated = {n} | (set.intersection(*(dominators[p] for p in incoming))
                             if incoming else set())
            if updated != dominators[n]:
                dominators[n] = updated
                changed = True
        if not changed:
            return sorted(dominators[sink])
    raise CfgProbeError("normal-CFG dominance failed to converge")


def inspect_handler(method, sealed):
    require(method["descriptor"] == HANDLE, "Raygun handler JVM descriptor drift")
    require(digest_method(method) == sealed["packet_receiver"]["parsed_method_sha256"],
            "Raygun sealed handler digest changed")
    ins = method["instructions"]
    require(len(ins) == sealed["packet_receiver"]["instruction_count"] == 75,
            "Raygun handler instruction population changed")
    offsets = [x["offset"] for x in ins]
    for off, (opcode, symbol) in ANCHORS["handle"].items():
        actual = next((x for x in ins if x["offset"] == off), None)
        require(actual is not None and actual["opcode"] == opcode and
                symbol in actual["symbol"], "Raygun native callsite anchor drift")
    edges, branches = successors(ins)
    require(len(branches) == 9, "sealed nine-branch receiver layout changed")
    sink = 174
    dominate = dominating_offsets(edges, offsets[0], sink)
    selected = [x for x in ins if x["opcode"].startswith("invoke")
                or x["opcode"] in REFERENCE_OPCODES]
    require(len(selected) <= 60, "bounded selected references overflow")
    refs = [{"offset": x["offset"], "opcode": x["opcode"],
             "symbol": x["symbol"][:450]} for x in selected]
    fields = [r for r in refs if r["opcode"] in ("getfield", "putfield")]
    windows = []
    for off in ANCHOR_OFFSETS:
        i = offsets.index(off)
        # Bound each window: selected opcodes and local variable transfer,
        # without copying a full method or provider implementation.
        around = ins[max(0, i-3):i+4]
        window = [
            {"offset": x["offset"], "opcode": x["opcode"],
             "operand": x["operand"][:75], "symbol": x["symbol"][:350]}
            for x in around
        ]
        windows.append({"anchor": off, "local_jvm_window": window})
    require(len(json.dumps(windows, ensure_ascii=False).encode()) < 35000,
            "bounded context windows overflow")
    return {
        "name": "handle",
        "descriptor": method["descriptor"],
        "method_sha256": digest_method(method),
        "instruction_count": len(ins),
        "normal_cfg_branches": branches,
        "entry_offset": offsets[0],
        "update_dispatch_offset": sink,
        "normal_cfg_dominators_of_update_dispatch": dominate,
        "selected_call_and_field_refs": refs,
        "packet_field_accesses": [r for r in fields if
                                 "UpdateItemTagMessage" in r["symbol"]],
        "critical_anchor_windows": windows
    }


def audit(jar, javap_bin, receiver_seal, identity_seal):
    ident = {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE}
    require(sha_file(jar) == (SHA1, SHA256, SIZE), "physical publisher mismatch")
    require(receiver_seal["artifact"] == ident and identity_seal["artifact"] == ident,
            "receiver/identity artifact drift")
    pinned = next(x["sha256"] for x in receiver_seal["class_identities"]
                  if x["path"] == PACKET)
    with zipfile.ZipFile(jar) as f:
        require(len(set(f.namelist())) == len(f.namelist()), "duplicate JAR member")
        data = f.read(PACKET)
        digest = hashlib.sha256(data).hexdigest()
        require(digest == pinned, "Raygun receiver class digest drift")
        require(data[:4] == b"\xca\xfe\xba\xbe" and
                int.from_bytes(data[6:8], "big") == 65, "JVM class major drift")
    methods = parse_methods(javap(javap_bin, jar, PACKET[:-6].replace("/", ".")))
    handler = method_by_sig(methods, "handle", HANDLE)
    observed = inspect_handler(handler, receiver_seal)
    require(observed["method_sha256"] ==
            identity_seal["receiver"]["parsed_method_sha256"],
            "identity counterpart receiver digest mismatch")
    require(observed["normal_cfg_branches"] == [
        {"offset": r["offset"], "opcode": r["opcode"],
         "branch_target": int(r["operand"]), "fallthrough": (
             next((x["offset"] for x in handler["instructions"]
                   if x["offset"] > r["offset"]), None)
             if r["opcode"].startswith("if") else None)}
        for r in identity_seal["receiver"]["conditional_branches"]
    ], "identity counterpart receiver branch drift")
    return {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_RAYGUN_RECEIVER_NORMAL_CFG_AND_PACKET_FIELDS_ONLY",
        "artifact": ident,
        "receiver_class_path": PACKET,
        "receiver_class_sha256": digest,
        "handler": observed,
        "limits": {
            "exception_edges": "NOT_ANALYZED",
            "interprocedural_dataflow": "NOT_ANALYZED",
            "sender_entity_id_authorization": "NOT_VERIFIED",
            "packet_tag_sanitization": "NOT_VERIFIED",
            "packet_validation_security": "NOT_ASSESSED",
            "runtime_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "static_perk_contract": "NOT_CERTIFIED",
            "mutation": "NO_MUTATION"
        }
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", required=True)
    p.add_argument("--receiver-manifest", required=True, type=Path)
    p.add_argument("--identity-manifest", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    receiver = json.loads(args.receiver_manifest.read_text(encoding="utf8"))
    identity = json.loads(args.identity_manifest.read_text(encoding="utf8"))
    report = audit(args.jar, args.javap, receiver, identity)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False,
         indent=2, sort_keys=True) + "\n", encoding="utf8")
    h = report["handler"]
    print("RAYGUN_HANDLER_SHA256=" + h["method_sha256"])
    print("RAYGUN_NORMAL_CFG_BRANCHES=" + str(len(h["normal_cfg_branches"])))
    print("RAYGUN_DOMINATORS_OF_DISPATCH=" + str(h["normal_cfg_dominators_of_update_dispatch"]))
    for f in h["packet_field_accesses"]:
        print("RAYGUN_PACKET_FIELD=" + json.dumps(f, sort_keys=True))
    for ref in h["selected_call_and_field_refs"]:
        print("RAYGUN_SELECTED_REF=" + json.dumps(ref, sort_keys=True))
    for win in h["critical_anchor_windows"]:
        print("RAYGUN_LOCAL_WINDOW=" + json.dumps(win, sort_keys=True))
    print("RAYGUN_SECURITY_AUTHORITY=NOT_VERIFIED; NO_MUTATION; NOT_CERTIFIED")


if __name__ == "__main__":
    main()
