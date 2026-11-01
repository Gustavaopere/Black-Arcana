#!/usr/bin/env python3
"""Read-only bounded ABI tracing of exact 1.0.10 ACNetwork registration paths.

No provider implementation is exported, no packets are sent, and this probe
does not establish server authority, register direction, or hook safety.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_raygun_receiver_probe import method_name
from alexscaves_1010_raygun_registration_probe import NETWORK, PACKET, RegistrationProbeError, require

TARGET_METHODS = ("registerMessages", "registerPayloads", "lambda$registerPayloads$0")
MAX_INSTRUCTIONS = 9000
MAX_SYMBOLS = 100
MAX_WINDOWS = 16
MAX_OUTPUT_BYTES = 52000
PINNED_PACKET_SHA = "bda52d12e8cce7e010b3d4cd2db7d83000e78b35657c55773a8ba91a070478c8"


def row_view(ins):
    return {"offset": ins["offset"], "opcode": ins["opcode"],
            "symbol": ins["symbol"][:400]}


def bounded_method(method):
    ins = method["instructions"]
    require(0 < len(ins) <= MAX_INSTRUCTIONS, "empty/oversize native registration method")
    offsets = [x["offset"] for x in ins]
    require(len(offsets) == len(set(offsets)), "duplicate JVM instruction offset")
    primary = [i for i, x in enumerate(ins) if "UpdateItemTagMessage" in x["symbol"]]
    require(len(primary) <= MAX_WINDOWS, "unbounded packet reference windows")
    windows = []
    for i in primary:
        windows.append({
            "packet_reference_at": ins[i]["offset"],
            "adjacent_selected_symbols": [
                row_view(x) for x in ins[max(0, i-4):i+5]
                if x["opcode"].startswith("invoke") or x["opcode"] in
                {"getstatic", "putstatic", "getfield", "putfield", "new", "ldc", "ldc_w", "checkcast"}
            ]
        })
    # Selected ABI references are a compact subset, not a reproduction of a method.
    matches = [
        row_view(x) for x in ins
        if x["opcode"].startswith("invoke") and (
            "register" in x["symbol"].lower() or
            "payload" in x["symbol"].lower() or
            "UpdateItemTagMessage" in x["symbol"] or
            "ACNetworkContext" in x["symbol"]
        )
    ]
    require(len(matches) <= MAX_SYMBOLS, "unbounded network symbolic refs")
    return {
        "name": method_name(method), "descriptor": method["descriptor"],
        "instruction_count": len(ins),
        "parsed_method_sha256": hashlib.sha256(json.dumps(
            method, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode("utf8")).hexdigest(),
        "packet_reference_offsets": [ins[i]["offset"] for i in primary],
        "bounded_abi_calls": matches,
        "packet_reference_windows": windows
    }


def select_network_methods(methods):
    signatures = [(method_name(m), m["descriptor"]) for m in methods]
    require(len(signatures) == len(set(signatures)), "ambiguous/duplicate JVM signature")
    selected = []
    for name in TARGET_METHODS:
        found = [m for m in methods if method_name(m) == name]
        require(len(found) == 1, "missing/ambiguous native network method: " + name)
        selected.append(bounded_method(found[0]))
    require(bool(selected[0]["packet_reference_offsets"]),
            "registerMessages lacks direct packet linkage")
    require(any("ACNetworkContext" in str(x) or "payload" in str(x).lower()
                for x in selected[2]["bounded_abi_calls"]),
            "payload callback boundary not observed")
    return selected


def audit(jar, javap_bin, receiver):
    expected = {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE}
    require(sha_file(jar) == (SHA1, SHA256, SIZE), "publisher JAR SHA drift")
    require(receiver.get("artifact") == expected, "receiver artifact identity drift")
    pinned = {row["path"]: row["sha256"] for row in receiver["class_identities"]}
    require(pinned.get(PACKET) == PINNED_PACKET_SHA, "exact receiver packet hash drift")
    with zipfile.ZipFile(jar) as archive:
        members = archive.namelist()
        require(len(set(members)) == len(members), "duplicate archive member")
        network_bytes = archive.read(NETWORK)
        packet_bytes = archive.read(PACKET)
        require(hashlib.sha256(packet_bytes).hexdigest() == PINNED_PACKET_SHA,
                "native packet class changed")
        require(len(network_bytes) >= 8 and network_bytes[:4] == b"\xca\xfe\xba\xbe"
                and int.from_bytes(network_bytes[6:8], "big") == 65,
                "network class JVM version drift")
    methods = parse_methods(javap(javap_bin, jar, NETWORK[:-6].replace("/", ".")))
    selected = select_network_methods(methods)
    report = {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_RAYGUN_NETWORK_REGISTRATION_SELECTED_ABI_ONLY",
        "artifact": expected,
        "network_class_path": NETWORK,
        "network_class_sha256": hashlib.sha256(network_bytes).hexdigest(),
        "declared_method_count": len(methods),
        "packet_class_path": PACKET,
        "packet_class_sha256": PINNED_PACKET_SHA,
        "selected_methods": selected,
        "limits": {
            "packet_register_direction": "UNRESOLVED_PENDING_REVIEW",
            "network_threading": "UNRESOLVED_PENDING_REVIEW",
            "sender_entity_id_binding": "NOT_VERIFIED",
            "custom_data_authorization": "NOT_VERIFIED",
            "no_full_method_export": True,
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "certification": "NOT_CERTIFIED",
            "mutation": "NO_MUTATION"
        }
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf8")) <= MAX_OUTPUT_BYTES,
            "bounded report JSON budget exceeded")
    return report


def verify_snapshot(report, snapshot):
    """A frozen manifest must match exact identities/selected method ABI."""
    require(report == snapshot, "sealed network ABI report drift")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", required=True)
    p.add_argument("--existing-receiver", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--snapshot", type=Path)
    args = p.parse_args()
    receiver = json.loads(args.existing_receiver.read_text(encoding="utf8"))
    report = audit(args.jar, args.javap, receiver)
    if args.snapshot:
        verify_snapshot(report, json.loads(args.snapshot.read_text(encoding="utf8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True,
                                      indent=2) + "\n", encoding="utf8")
    print("NETWORK_CLASS_SHA256=" + report["network_class_sha256"])
    print("NETWORK_DECLARED_METHODS=" + str(report["declared_method_count"]))
    for m in report["selected_methods"]:
        print("NETWORK_METHOD=" + m["name"] + " " + m["descriptor"])
        print("NETWORK_METHOD_HASH=" + m["parsed_method_sha256"])
        print("NETWORK_PACKET_OFFSETS=" + str(m["packet_reference_offsets"]))
        for window in m["packet_reference_windows"]:
            print("PACKET_WINDOW=" + json.dumps(window, ensure_ascii=False, sort_keys=True))
        if m["name"] != "registerMessages":
            for ref in m["bounded_abi_calls"][:24]:
                print("NETWORK_ABI_REF=" + json.dumps(ref, ensure_ascii=False, sort_keys=True))
    print("NETWORK_REGISTRATION_REVIEW=REQUIRED; NO_MUTATION; NOT_CERTIFIED")


if __name__ == "__main__":
    main()
