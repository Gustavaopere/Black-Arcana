#!/usr/bin/env python3
"""Exact 1.0.10 Raygun network message serialization ABI (read-only).

This bounds field operations, codec invocations and method digests. It does
not authorize untrusted data, infer a packet security flaw or mutate runtime.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_raygun_receiver_probe import PACKET, HANDLE, method_name
from alexscaves_1010_raygun_receiver_identity_probe import digest_method

MAX_CLASSES = 1
MAX_METHODS = 9
MAX_ROWS = 115
MAX_REPORT_BYTES = 39000
SELECTED_OPERATIONS = {
    "getfield", "putfield", "getstatic", "putstatic", "new", "checkcast",
    "instanceof", "ldc", "ldc_w", "bipush", "sipush",
}


class CodecProbeError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise CodecProbeError(message)


def include_ref(opcode, symbol):
    return opcode.startswith("invoke") or (
        opcode in SELECTED_OPERATIONS and (
            opcode in ("getfield", "putfield", "getstatic", "putstatic") or
            any(x in symbol for x in (
                "ItemStack", "UpdateItemTagMessage", "Codec", "ByteBuf",
                "ACNetwork", "CompoundTag", "entityId", "itemStackFrom"
            ))
        )
    )


def bounded_method(method):
    instructions = method["instructions"]
    require(len(instructions) <= 850, "unbounded packet method bytecode")
    require(len({x["offset"] for x in instructions}) == len(instructions),
            "duplicate packet JVM instruction offsets")
    rows = [
        {"offset": x["offset"], "opcode": x["opcode"],
         "symbol": x["symbol"][:480]}
        for x in instructions if include_ref(x["opcode"], x["symbol"])
    ]
    require(len(rows) <= MAX_ROWS, "unbounded packet ABI reference population")
    return {
        "name": method_name(method), "descriptor": method["descriptor"],
        "method_sha256": digest_method(method),
        "instruction_count": len(instructions),
        "abi_references": rows
    }


def audit(jar, javap_bin, receiver_seal, cfg_seal):
    ident = {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE}
    require(sha_file(jar) == (SHA1, SHA256, SIZE), "installed publisher identity drift")
    require(receiver_seal["artifact"] == ident and cfg_seal["artifact"] == ident,
            "prior Raygun manifests changed physical identity")
    pinned = next(row["sha256"] for row in receiver_seal["class_identities"]
                  if row["path"] == PACKET)
    require(cfg_seal["receiver_class_path"] == PACKET and
            cfg_seal["receiver_class_sha256"] == pinned,
            "prior exact packet class identity mismatch")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicated physical ZIP member")
        raw = archive.read(PACKET)
        require(len(raw) >= 8 and raw[:4] == b"\xca\xfe\xba\xbe" and
                int.from_bytes(raw[6:8], "big") == 65, "unexpected JVM class version")
        require(hashlib.sha256(raw).hexdigest() == pinned, "packet class digest drift")
    methods = parse_methods(javap(javap_bin, jar, PACKET[:-6].replace("/", ".")))
    require(1 < len(methods) <= MAX_METHODS, "unexpected Raygun message method count")
    identities = [(method_name(m), m["descriptor"]) for m in methods]
    require(len(set(identities)) == len(identities), "duplicate packet JVM signature")
    packet = [bounded_method(m) for m in methods]
    handlers = [m for m in packet if m["name"] == "handle" and m["descriptor"] == HANDLE]
    require(len(handlers) == 1, "packet receiver signature changed")
    require(handlers[0]["method_sha256"] ==
            cfg_seal["handler"]["method_sha256"], "receiver hash no longer matches CFG")
    require(len(json.dumps(packet, ensure_ascii=False).encode("utf8")) <= MAX_REPORT_BYTES,
            "bounded codec report budget exceeded")
    # Structural evidence only; packet codecs can still be unsafe semantically.
    return {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_RAYGUN_PACKET_SERIALIZATION_SELECTED_ABI_ONLY",
        "artifact": ident,
        "class_path": PACKET,
        "class_sha256": pinned,
        "declared_method_count": len(methods),
        "methods": packet,
        "limits": {
            "wire_data_trust": "UNTRUSTED_UNTIL_SERVER_VALIDATED",
            "sender_entity_id_binding": "NOT_VERIFIED",
            "stack_identity_binding": "NOT_VERIFIED",
            "tag_field_whitelist": "NOT_VERIFIED",
            "network_direction_and_threading": "REQUIRES_SEPARATE_CONTRACTS",
            "runtime_exploitability": "NOT_ASSESSED",
            "physical_qa": "NOT_TESTED",
            "mutating_hook": "NOT_VERIFIED",
            "perk_static_certification": "NOT_CERTIFIED",
            "mutation": "NO_MUTATION"
        }
    }


PACKET_ABI_NAMES = ("UpdateItemTagMessage", "read", "write", "handle")
PACKET_CODECS = (
    ("UpdateItemTagMessage", 6, "putfield", "Field entityId:I"),
    ("UpdateItemTagMessage", 11, "putfield", "Field itemStackFrom:"),
    ("read", 5, "invokevirtual", "FriendlyByteBuf.readInt:"),
    ("read", 9, "invokestatic", "PacketBufferUtils.readItemStack:"),
    ("read", 12, "invokespecial", "Method \"<init>\":"),
    ("write", 2, "getfield", "Field entityId:I"),
    ("write", 5, "invokevirtual", "FriendlyByteBuf.writeInt:"),
    ("write", 11, "getfield", "Field itemStackFrom:"),
    ("write", 14, "invokestatic", "PacketBufferUtils.writeItemStack:"),
)
SEALED_LIMITS = {
    "wire_data_trust": "UNTRUSTED_UNTIL_SERVER_VALIDATED",
    "sender_entity_id_binding": "NOT_VERIFIED",
    "stack_identity_binding": "NOT_VERIFIED",
    "tag_field_whitelist": "NOT_VERIFIED",
    "network_direction_and_threading": "REQUIRES_SEPARATE_CONTRACTS",
    "runtime_exploitability": "NOT_ASSESSED",
    "physical_qa": "NOT_TESTED",
    "mutating_hook": "NOT_VERIFIED",
    "perk_static_certification": "NOT_CERTIFIED",
    "mutation": "NO_MUTATION"
}


def snapshot_projection(report):
    """Seal the 4 exact method ABIs and 9 narrow wire codec callsites."""
    methods = report["methods"]
    require(len(methods) == 4, "exact packet method count drift")
    require(tuple(m["name"] for m in methods) == PACKET_ABI_NAMES,
            "exact packet method roster/order drift")
    require(len({(m["name"], m["descriptor"]) for m in methods}) == 4,
            "ambiguous packet methods")
    require(report["declared_method_count"] == 4, "declared method count drift")
    require(report["limits"] == SEALED_LIMITS,
            "unsafe/false Raygun packet status or limits drift")
    index = {m["name"]: m for m in methods}
    anchors = []
    for name, offset, opcode, symbol in PACKET_CODECS:
        hits = [x for x in index[name]["abi_references"] if x["offset"] == offset]
        require(len(hits) == 1 and hits[0]["opcode"] == opcode and
                symbol in hits[0]["symbol"],
                "exact packet codec opcode/field anchor drift")
        anchors.append({"method": name, **hits[0]})
    return {
        **{key: report[key] for key in (
            "schema_version", "scope", "artifact", "class_path",
            "class_sha256", "declared_method_count")},
        "methods": [
            {key: m[key] for key in (
                "name", "descriptor", "method_sha256")}
            for m in methods
        ],
        "codec_abi_anchors": anchors,
        "limits": report["limits"]
    }


def verify_snapshot(report, sealed):
    require(snapshot_projection(report) == sealed,
            "exact Raygun packet codec snapshot mismatch")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", required=True)
    p.add_argument("--receiver-manifest", required=True, type=Path)
    p.add_argument("--cfg-manifest", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--snapshot", type=Path)
    args = p.parse_args()
    old = json.loads(args.receiver_manifest.read_text(encoding="utf8"))
    cfg = json.loads(args.cfg_manifest.read_text(encoding="utf8"))
    report = audit(args.jar, args.javap, old, cfg)
    if args.snapshot:
        verify_snapshot(report, json.loads(args.snapshot.read_text(encoding="utf8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False,
                                      sort_keys=True) + "\n", encoding="utf8")
    print("RAYGUN_PACKET_CLASS_SHA256=" + report["class_sha256"])
    print("RAYGUN_PACKET_METHOD_COUNT=" + str(report["declared_method_count"]))
    for m in report["methods"]:
        print("RAYGUN_PACKET_METHOD=" + m["name"] + " " + m["descriptor"])
        print("RAYGUN_PACKET_METHOD_SHA256=" + m["method_sha256"])
        for x in m["abi_references"]:
            print("RAYGUN_PACKET_ABI_REF=" + m["name"] + " " +
                  json.dumps(x, ensure_ascii=False, sort_keys=True))
    print("RAYGUN_WIRE_DATA=UNTRUSTED; NOT_CERTIFIED; NO_MUTATION")


if __name__ == "__main__":
    main()
