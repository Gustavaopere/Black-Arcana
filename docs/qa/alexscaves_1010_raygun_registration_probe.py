#!/usr/bin/env python3
"""Bounded clean-room discovery: exact Raygun C2S native registration references.

Exploratory output is NOT a static certification or an authorization/exploit
finding. A later separately reviewed SHA-pinned manifest is required to seal it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_raygun_receiver_probe import method_name

PREFIX = "com/github/alexmodguy/alexscaves/"
RAYGUN = PREFIX + "server/item/RaygunItem.class"
PACKET = PREFIX + "server/message/UpdateItemTagMessage.class"
SEARCH = (b"UpdateItemTagMessage", b"ACNetworkContext")
REFERENCE = ("UpdateItemTagMessage", "ACNetworkContext")
MAX_CANDIDATES = 96
MAX_METHODS = 600
MAX_REFERENCES = 900
MAX_REPORT_BYTES = 250000


class RegistrationProbeError(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise RegistrationProbeError(reason)


def discover_candidates(archive):
    """Constant-pool search makes *candidates*, not proof of an executed call."""
    names = archive.namelist()
    require(len(names) == len(set(names)), "duplicate ZIP member")
    paths = sorted(name for name in names if name.startswith(PREFIX)
                   and name.endswith(".class"))
    require(0 < len(paths) <= 10000, "unbounded class population")
    found = []
    for path in paths:
        data = archive.read(path)
        if any(token in data for token in SEARCH):
            require(len(data) >= 8 and data[:4] == b"\xca\xfe\xba\xbe"
                    and int.from_bytes(data[6:8], "big") == 65,
                    "unexpected classfile major/version")
            found.append((path, hashlib.sha256(data).hexdigest()))
            require(len(found) <= MAX_CANDIDATES,
                    "unbounded candidate list; narrow scope explicitly")
    require(any(path == PACKET for path, _ in found), "packet class missing from scan")
    require(any(path == RAYGUN for path, _ in found), "sender class missing from scan")
    return found


def matching_method_refs(method):
    """Only exact javap symbolic operands; no inferred handler or direction."""
    name, desc = method_name(method), method["descriptor"]
    instructions = method["instructions"]
    offsets = [i["offset"] for i in instructions]
    require(len(offsets) == len(set(offsets)), "duplicate JVM offsets")
    refs = []
    for row in instructions:
        if any(term in row["symbol"] for term in REFERENCE):
            require(len(row["symbol"]) <= 1000, "symbol exceeds bounded export")
            refs.append({key: row[key] for key in ("offset", "opcode", "symbol")})
    if not refs:
        return None
    require(len(refs) <= 70, "unbounded per-method references")
    return {"name": name, "descriptor": desc,
            "instruction_count": len(instructions),
            "parsed_method_sha256": hashlib.sha256(
                json.dumps(method, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":")).encode("utf-8")).hexdigest(),
            "references": refs}


def audit(jar, javap_bin, sealed):
    jar = Path(jar)
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "installed publisher identity/version mismatch")
    require(sealed["artifact"] == {"sha1": SHA1, "sha256": SHA256,
                                   "size_bytes": SIZE},
            "existing exact receiver manifest identity drift")
    require(len(sealed["class_identities"]) == 4,
            "receiver class roster drift")
    pinned = {row["path"]: row["sha256"] for row in sealed["class_identities"]}
    with zipfile.ZipFile(jar) as archive:
        candidates = discover_candidates(archive)
    for path, digest in candidates:
        if path in pinned:
            require(pinned[path] == digest,
                    "previously sealed receiver class changed: " + path)
    result = []
    total_methods, total_refs = 0, 0
    for path, digest in candidates:
        methods = parse_methods(javap(javap_bin, jar, path[:-6].replace("/", ".")))
        signatures = [(method_name(m), m["descriptor"]) for m in methods]
        require(len(signatures) == len(set(signatures)), "duplicate JVM signature")
        hits = [record for m in methods
                if (record := matching_method_refs(m)) is not None]
        total_methods += len(hits)
        total_refs += sum(len(row["references"]) for row in hits)
        require(total_methods <= MAX_METHODS and total_refs <= MAX_REFERENCES,
                "bounded method/ref budget exceeded")
        result.append({"class_path": path, "class_sha256": digest,
                       "declared_method_count": len(methods),
                       "methods_with_direct_symbolic_references": hits})
    report = {
        "schema_version": 1,
        "scope": "ALEXSCAVES_1010_RAYGUN_C2S_REGISTRATION_REFERENCE_DISCOVERY_ONLY",
        "publisher": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "candidate_class_count": len(result),
        "direct_reference_method_count": total_methods,
        "direct_symbolic_reference_count": total_refs,
        "candidates": result,
        "limits": {
            "registration_direction_and_threading": "NOT_VERIFIED",
            "server_authorization": "NOT_VERIFIED",
            "sender_entity_id_binding": "NOT_VERIFIED",
            "custom_data_field_sanitization": "NOT_VERIFIED",
            "replay_and_hand_swap": "NOT_TESTED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "complete_perk_contract": "NOT_CERTIFIED",
            "runtime_mutation": "NO_MUTATION"
        }
    }
    require(len(json.dumps(report, ensure_ascii=False).encode("utf8"))
            <= MAX_REPORT_BYTES, "bounded JSON budget exceeded")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--javap", required=True)
    parser.add_argument("--existing-receiver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sealed = json.loads(args.existing_receiver.read_text(encoding="utf8"))
    report = audit(args.jar, args.javap, sealed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False,
        indent=2, sort_keys=True) + "\n", encoding="utf8")
    print("RAYGUN_C2S_CANDIDATES=" + str(report["candidate_class_count"]))
    print("RAYGUN_DIRECT_REFERENCE_METHODS=" + str(
        report["direct_reference_method_count"]))
    for entry in report["candidates"]:
        if entry["methods_with_direct_symbolic_references"]:
            print("JVM_REF_CLASS=" + entry["class_path"])
            for method in entry["methods_with_direct_symbolic_references"]:
                print("JVM_REF_METHOD=" + method["name"] + " " + method["descriptor"])
    print("NETWORK_AUTHORIZATION=NOT_VERIFIED; NO_MUTATION; NOT_CERTIFIED")


if __name__ == "__main__":
    main()
