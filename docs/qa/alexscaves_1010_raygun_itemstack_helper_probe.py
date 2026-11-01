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


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--javap", required=True)
    p.add_argument("--packet-codec-manifest", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    upstream = json.loads(args.packet_codec_manifest.read_text(encoding="utf8"))
    report = audit(args.jar, args.javap, upstream)
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
