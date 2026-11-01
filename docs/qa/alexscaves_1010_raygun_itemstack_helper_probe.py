#!/usr/bin/env python3
"""Read-only SHA-exact 1.0.10 Citadel-shaded item-stack wire helper ABI.

Clean-room output is a bounded method ABI and JVM symbolic references only.
It does NOT prove NBT safety, network authorization or hook compatibility.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_raygun_receiver_probe import method_by_sig, method_name
from alexscaves_1010_raygun_receiver_identity_probe import digest_method

HELPER = "com/github/alexmodguy/alexscaves/citadel/server/message/PacketBufferUtils.class"
READ = "(Lio/netty/buffer/ByteBuf;)Lnet/minecraft/world/item/ItemStack;"
WRITE = "(Lio/netty/buffer/ByteBuf;Lnet/minecraft/world/item/ItemStack;)V"
TARGETS = (("readItemStack", READ), ("writeItemStack", WRITE))
MAX_METHOD_INSTRUCTIONS = 1800
MAX_SYMBOLS_PER_METHOD = 120
MAX_BRANCHES_PER_METHOD = 80
MAX_REPORT_BYTES = 70000
OPCODES = {
    "getstatic", "putstatic", "getfield", "putfield", "new", "checkcast",
    "instanceof", "ldc", "ldc_w", "bipush", "sipush", "anewarray", "newarray",
}


class HelperProbeError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise HelperProbeError(message)


def selected_abi(method):
    instructions = method["instructions"]
    require(0 < len(instructions) <= MAX_METHOD_INSTRUCTIONS, "bounded helper method length changed")
    offsets = [row["offset"] for row in instructions]
    require(len(offsets) == len(set(offsets)) and offsets == sorted(offsets),
            "helper JVM offsets duplicated/out of order")
    symbols = [{
        "offset": row["offset"], "opcode": row["opcode"],
        "symbol": row["symbol"][:440]
    } for row in instructions if row["opcode"].startswith("invoke") or
        row["opcode"] in OPCODES]
    branches = [{
        "offset": row["offset"], "opcode": row["opcode"],
        "operand": row["operand"][:65]
    } for row in instructions if row["opcode"].startswith(("if", "goto"))]
    require(len(symbols) <= MAX_SYMBOLS_PER_METHOD,
            "helper symbolic reference export is unbounded")
    require(len(branches) <= MAX_BRANCHES_PER_METHOD,
            "helper branch export is unbounded")
    return {
        "name": method_name(method),
        "descriptor": method["descriptor"],
        "method_sha256": digest_method(method),
        "instruction_count": len(instructions),
        "selected_symbolic_references": symbols,
        "conditional_and_jump_offsets": branches
    }


def audit(jar, javap_bin, message_codec):
    artifact = {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE}
    require(message_codec["artifact"] == artifact,
            "upstream Raygun packet codec artifact identity mismatch")
    require(message_codec["class_sha256"] ==
            "bda52d12e8cce7e010b3d4cd2db7d83000e78b35657c55773a8ba91a070478c8",
            "upstream packet codec class identity drift")
    require(sha_file(jar) == (SHA1, SHA256, SIZE),
            "physical 1.0.10 publisher identity mismatch")
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate publisher ZIP member")
        require(HELPER in names, "shaded Citadel helper absent in installed publisher")
        raw = archive.read(HELPER)
        require(len(raw) >= 8 and raw[:4] == b"\xca\xfe\xba\xbe"
                and int.from_bytes(raw[6:8], "big") == 65,
                "unexpected helper classfile version")
        helper_sha = hashlib.sha256(raw).hexdigest()
    dotted = HELPER[:-6].replace("/", ".")
    methods = parse_methods(javap(javap_bin, jar, dotted))
    signatures = [(method_name(m), m["descriptor"]) for m in methods]
    require(len(signatures) == len(set(signatures)), "duplicate helper method ABI")
    require(2 <= len(signatures) <= 80, "unbounded helper class method roster")
    selected = [selected_abi(method_by_sig(methods, name, descriptor))
                for name, descriptor in TARGETS]
    result = {
        "schema_version": 1,
        "scope": "SHA_EXACT_ALEXSCAVES_1010_SHADED_CITADEL_ITEMSTACK_WIRE_ABI_READONLY",
        "artifact": artifact,
        "helper_class_path": HELPER,
        "helper_class_sha256": helper_sha,
        "declared_method_count": len(methods),
        "selected_methods": selected,
        "limits": {
            "untrusted_wire_item_stack": True,
            "item_stack_max_bytes": "NOT_VERIFIED",
            "item_stack_max_components": "NOT_VERIFIED",
            "nbt_size_depth_and_fields": "NOT_VERIFIED",
            "server_authoritative_id_and_stack": "NOT_VERIFIED",
            "sanitized_raygun_charge_and_time": "NOT_VERIFIED",
            "runtime_exploitability": "NOT_ASSESSED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "static_perk_certification": "NOT_CERTIFIED",
            "mutation": "NO_MUTATION"
        }
    }
    require(len(json.dumps(result, ensure_ascii=False).encode("utf8")) <= MAX_REPORT_BYTES,
            "helper evidence report too large")
    return result



EXPECTED_CLASS_SHA256 = "3f203404344653e77167846c967635f930f84cad355f60b084358f826c7ae3db"
EXPECTED_HELPER_ABI = (
    ("readItemStack", 0, "getstatic", "ItemStack.OPTIONAL_STREAM_CODEC:"),
    ("readItemStack", 4, "checkcast", "RegistryFriendlyByteBuf"),
    ("readItemStack", 7, "invokeinterface", "StreamCodec.decode:"),
    ("readItemStack", 12, "checkcast", "net/minecraft/world/item/ItemStack"),
    ("writeItemStack", 0, "getstatic", "ItemStack.OPTIONAL_STREAM_CODEC:"),
    ("writeItemStack", 4, "checkcast", "RegistryFriendlyByteBuf"),
    ("writeItemStack", 8, "invokeinterface", "StreamCodec.encode:"),
)
EXPECTED_LIMITS = {
    "untrusted_wire_item_stack": True,
    "item_stack_max_bytes": "NOT_VERIFIED",
    "item_stack_max_components": "NOT_VERIFIED",
    "nbt_size_depth_and_fields": "NOT_VERIFIED",
    "server_authoritative_id_and_stack": "NOT_VERIFIED",
    "sanitized_raygun_charge_and_time": "NOT_VERIFIED",
    "runtime_exploitability": "NOT_ASSESSED",
    "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED",
    "static_perk_certification": "NOT_CERTIFIED",
    "mutation": "NO_MUTATION"
}


def snapshot_projection(report):
    """SHA-exact helper boundary, not a claim about vanilla codec internals."""
    require(report["helper_class_path"] == HELPER,
            "shaded Citadel helper path drift")
    require(report["helper_class_sha256"] == EXPECTED_CLASS_SHA256,
            "shaded Citadel helper class SHA drift")
    require(report["limits"] == EXPECTED_LIMITS,
            "helper boundaries or safety statuses changed")
    require(report["declared_method_count"] == 12,
            "helper native method population drift")
    methods = report["selected_methods"]
    require([(m["name"], m["descriptor"]) for m in methods] == list(TARGETS),
            "helper required methods/signatures drift")
    anchors = []
    for name, offset, opcode, symbol in EXPECTED_HELPER_ABI:
        method = next(x for x in methods if x["name"] == name)
        hits = [x for x in method["selected_symbolic_references"]
                if x["offset"] == offset]
        require(len(hits) == 1 and hits[0]["opcode"] == opcode
                and symbol in hits[0]["symbol"],
                "exact shaded helper codec callsite drift")
        anchors.append({"method": name, **hits[0]})
    require(all(not m["conditional_and_jump_offsets"] for m in methods),
            "native ItemStack helper now has branch logic")
    require(all(m["instruction_count"] == 6 for m in methods),
            "native ItemStack helper instruction count drift")
    return {
        **{k: report[k] for k in
           ("schema_version", "scope", "artifact", "helper_class_path",
            "helper_class_sha256", "declared_method_count")},
        "methods": [
            {k: m[k] for k in
             ("name", "descriptor", "method_sha256", "instruction_count")}
            for m in methods
        ],
        "stream_codec_abi_anchors": anchors,
        "limits": report["limits"]
    }


def verify_snapshot(report, snapshot):
    require(snapshot_projection(report) == snapshot,
            "exact shaded helper ABI snapshot mismatch")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", required=True)
    p.add_argument("--packet-codec-manifest", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--snapshot", required=True, type=Path)
    args = p.parse_args()
    upstream = json.loads(args.packet_codec_manifest.read_text(encoding="utf8"))
    report = audit(args.jar, args.javap, upstream)
    verify_snapshot(report, json.loads(args.snapshot.read_text(encoding="utf8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True,
                                      ensure_ascii=False) + "\n", encoding="utf8")
    print("ITEMSTACK_HELPER_CLASS_SHA256=" + report["helper_class_sha256"])
    print("ITEMSTACK_HELPER_METHOD_COUNT=" + str(report["declared_method_count"]))
    for item in report["selected_methods"]:
        print("ITEMSTACK_HELPER_METHOD=" + item["name"] + " " + item["descriptor"])
        print("ITEMSTACK_HELPER_METHOD_SHA256=" + item["method_sha256"])
        print("ITEMSTACK_HELPER_INSTRUCTION_COUNT=" + str(item["instruction_count"]))
        for row in item["selected_symbolic_references"]:
            print("ITEMSTACK_HELPER_REF=" + item["name"] + " " +
                  json.dumps(row, sort_keys=True, ensure_ascii=False))
        for row in item["conditional_and_jump_offsets"]:
            print("ITEMSTACK_HELPER_BRANCH=" + item["name"] + " " +
                  json.dumps(row, sort_keys=True, ensure_ascii=False))
    print("ITEMSTACK_HELPER_SECURITY=NOT_VERIFIED; NOT_CERTIFIED; NO_MUTATION")


if __name__ == "__main__":
    main()
