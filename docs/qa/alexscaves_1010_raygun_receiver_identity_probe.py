#!/usr/bin/env python3
"""SHA-exact, read-only Raygun receiver identity/context-flow evidence.

Observes bounded JVM operands, branch offsets and wrapper method ABI only.
No provider code redistribution, no runtime authorization/security verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_raygun_receiver_probe import (
    PACKET, HANDLE, ANCHORS, method_by_sig, method_name
)

BASE = "com/github/alexmodguy/alexscaves/server/message/"
CONTEXT = BASE + "ACNetwork$NeoForgeContext.class"
ENTRY = BASE + "ACNetwork$Entry.class"
NETWORK = BASE + "ACNetwork.class"
CLASS_PATHS = (PACKET, CONTEXT, ENTRY, NETWORK)
MAX_REPORT_BYTES = 57000
MAX_METHOD_OPERANDS = 60
MAX_BRANCHES = 65


class IdentityProbeError(ValueError):
    pass


def require(predicate, message):
    if not predicate:
        raise IdentityProbeError(message)


def digest_method(m):
    return hashlib.sha256(json.dumps(m, sort_keys=True,
        ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def minimal(ins):
    return {"offset": ins["offset"], "opcode": ins["opcode"],
            "operand": ins["operand"][:100], "symbol": ins["symbol"][:500]}


def method_inventory(methods, selected_names):
    signatures = [(method_name(m), m["descriptor"]) for m in methods]
    require(len(signatures) == len(set(signatures)), "duplicate declared JVM signature")
    found = []
    for m in methods:
        if method_name(m) not in selected_names:
            continue
        ins = m["instructions"]
        require(0 < len(ins) < 4500, "empty/oversize selected context method")
        require(len({x["offset"] for x in ins}) == len(ins),
                "duplicate instruction offset")
        interesting = [minimal(x) for x in ins
                       if (x["opcode"].startswith(("invoke", "if")) or
                           x["opcode"] in ("areturn", "ireturn", "getfield", "getstatic", "instanceof", "checkcast")
                       )]
        require(len(interesting) <= MAX_METHOD_OPERANDS, "unbounded context method operands")
        found.append({"name": method_name(m), "descriptor": m["descriptor"],
                      "parsed_method_sha256": digest_method(m),
                      "selected_references": interesting})
    require(len(found) <= 12, "unbounded selected context method count")
    return found


def extract_receiver_guard(m, sealed):
    require(m["descriptor"] == HANDLE, "receiver JVM signature drift")
    require(digest_method(m) == sealed["packet_receiver"]["parsed_method_sha256"],
            "exact receiver method hash drift")
    require(len(m["instructions"]) == sealed["packet_receiver"]["instruction_count"],
            "receiver instruction count drift")
    instructions = m["instructions"]
    offsets = [x["offset"] for x in instructions]
    require(len(set(offsets)) == len(offsets), "receiver duplicate JVM offset")
    byoff = {x["offset"]: x for x in instructions}
    anchors = []
    for off, (opcode, symbol) in ANCHORS["handle"].items():
        x = byoff.get(off)
        require(x is not None and x["opcode"] == opcode and symbol in x["symbol"],
                "exact receiver anchor drift: " + str(off))
        anchors.append(minimal(x))
    branches = [minimal(x) for x in instructions if x["opcode"].startswith(("if", "goto"))]
    require(0 < len(branches) <= MAX_BRANCHES, "receiver branch budget/absence")
    local_windows = []
    for off in (8, 15, 42, 78, 81, 113, 158, 171, 174):
        ix = offsets.index(off)
        window = instructions[max(0,ix-3):ix+4]
        # Keep branch/field/target references; omit unneeded instruction sequence.
        chosen = [minimal(x) for x in window
                  if x["opcode"].startswith(("if", "invoke", "goto")) or
                  x["opcode"] in ("getfield", "getstatic", "instanceof", "checkcast")]
        local_windows.append({"at": off, "selected_guards_and_refs": chosen})
    return {"name": "handle", "descriptor": m["descriptor"],
            "parsed_method_sha256": digest_method(m),
            "instruction_count": len(instructions),
            "critical_anchors": anchors, "conditional_branches": branches,
            "bounded_guard_windows": local_windows}


def audit(jar, javap_bin, receiver_seal, network_seal):
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "publisher JAR identity drift")
    expected_artifact = {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE}
    require(receiver_seal["artifact"] == expected_artifact
            and network_seal["artifact"] == expected_artifact,
            "prior receiver/network seal artifact mismatch")
    require(network_seal["network_class_path"] == NETWORK,
            "native network class roster mismatch")
    pinned = {row["path"]: row["sha256"] for row in receiver_seal["class_identities"]}
    pinned[NETWORK] = network_seal["network_class_sha256"]
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate physical ZIP members")
        hashes = {}
        for path in CLASS_PATHS:
            data = archive.read(path)
            require(len(data) >= 8 and data[:4] == b"\xca\xfe\xba\xbe"
                    and int.from_bytes(data[6:8], "big") == 65,
                    "JVM class version drift: " + path)
            digest = hashlib.sha256(data).hexdigest()
            require(path not in pinned or digest == pinned[path],
                    "previously sealed class digest mismatch: " + path)
            hashes[path] = digest
    methods = {}
    for path in CLASS_PATHS:
        methods[path] = parse_methods(javap(javap_bin, jar,
                                           path[:-6].replace("/", ".")))
    handler = method_by_sig(methods[PACKET], "handle", HANDLE)
    packet = extract_receiver_guard(handler, receiver_seal)
    native_ctx = method_inventory(methods[CONTEXT], {
        "getSender", "isClientSide", "enqueueWork", "getDirection"
    })
    native_entry = method_inventory(methods[ENTRY], {
        "handle", "encoder", "decoder", "read", "write"
    })
    # Do not assert methods exist before seeing their real JVM ABI.
    require(native_ctx and native_entry, "native context/entry method roster absent")
    result = {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_RAYGUN_RECEIVER_IDENTITY_AND_ENVELOPE_CONTEXT_READONLY",
        "artifact": expected_artifact,
        "class_identities": [{"path": path, "sha256": hashes[path],
                             "declared_methods": len(methods[path])}
                            for path in CLASS_PATHS],
        "receiver": packet,
        "network_context_methods": native_ctx,
        "network_entry_methods": native_entry,
        "limits": {
            "packet_sender_entity_id_equality": "NOT_DEMONSTRATED_BY_THIS_PROBE",
            "client_to_server_authorization": "NOT_VERIFIED",
            "server_side_tag_validation": "NOT_VERIFIED",
            "network_threading": "NOT_VERIFIED",
            "replay_and_hand_swap": "NOT_TESTED",
            "native_security_vulnerability": "NOT_ASSESSED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "static_perk_certification": "NOT_CERTIFIED",
            "mutation": "NO_MUTATION"
        }
    }
    require(len(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            <= MAX_REPORT_BYTES, "bounded result size exceeded")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--receiver-manifest", required=True, type=Path)
    parser.add_argument("--network-manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    receiver = json.loads(args.receiver_manifest.read_text(encoding="utf-8"))
    network = json.loads(args.network_manifest.read_text(encoding="utf-8"))
    report = audit(args.jar, args.javap, receiver, network)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False,
        sort_keys=True, indent=2) + "\n", encoding="utf-8")
    for entry in report["class_identities"]:
        print("JVM_CLASS=" + entry["path"] + " SHA256=" + entry["sha256"])
    print("JVM_RECEIVER_BRANCH_COUNT=" + str(len(report["receiver"]["conditional_branches"])))
    for branch in report["receiver"]["conditional_branches"]:
        print("JVM_RECEIVER_BRANCH=" + json.dumps(branch, sort_keys=True))
    for name, rows in (("CONTEXT", report["network_context_methods"]),
                       ("ENTRY", report["network_entry_methods"])):
        for row in rows:
            print("JVM_" + name + "_METHOD=" + row["name"] + " " + row["descriptor"])
            print("JVM_" + name + "_METHOD_SHA256=" + row["parsed_method_sha256"])
            for ref in row["selected_references"]:
                print("JVM_" + name + "_REFERENCE=" + json.dumps(ref, sort_keys=True))
    print("SECURITY_REVIEW=REQUIRED; NOT_CERTIFIED; NO_MUTATION")


if __name__ == "__main__":
    main()
