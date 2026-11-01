#!/usr/bin/env python3
"""Bounded SHA-exact observation of Raygun ammo and C2S item-tag message.

Produces method hashes, selected instructions and callsite anchors only.
Never copies full bytecode, JAR, or provider implementation. No runtime QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import (
    name_of, strict_pairs, summarize
)

ROOT = "com/github/alexmodguy/alexscaves/"
RAYGUN = ROOT + "server/item/RaygunItem.class"
PACKET = ROOT + "server/message/UpdateItemTagMessage.class"
RAYGUN_SHA = "3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c"
RAYGUN_METHODS = {
    "findAmmo", "use", "onUseTick", "releaseUsing", "getCharge",
    "setCharge", "hasCharge", "getUseDuration", "updateTagFromServer",
    "lambda$static$0", "lambda$static$1"
}
SENDERS = {
    "onUseTick": (162, 165),
    "releaseUsing": (25, 28),
}
MAX_REPORT_BYTES = 300_000


class PacketAmmoProbeError(ValueError):
    pass


def validate_sender(method, points):
    instr = method["instructions"]
    if len({i["offset"] for i in instr}) != len(instr):
        raise PacketAmmoProbeError("duplicate JVM bytecode offset")
    at = {i["offset"]: i for i in instr}
    constructor, dispatch = (at.get(k) for k in points)
    if (constructor is None or
        constructor["opcode"] != "invokespecial" or
        'UpdateItemTagMessage."<init>":(ILnet/minecraft/world/item/ItemStack;)V'
        not in constructor["symbol"]):
        raise PacketAmmoProbeError("missing exact C2S message constructor")
    if (dispatch is None or dispatch["opcode"] != "invokestatic" or
        "AlexsCaves.sendMSGToServer:(Ljava/lang/Object;)V"
        not in dispatch["symbol"]):
        raise PacketAmmoProbeError("missing exact C2S send dispatch")
    return {"constructor_offset": points[0], "sender_offset": points[1]}


def select(methods, chosen, *, raygun=False):
    names = [(name_of(m), m["descriptor"]) for m in methods]
    if len(names) != len(set(names)):
        raise PacketAmmoProbeError("duplicate declared JVM method")
    out = []
    for m in methods:
        name = name_of(m)
        if not m["instructions"] or (raygun and name not in chosen):
            continue
        if name == "onUseTick" and raygun:
            # Sender, charge/cost and target/damage traces are separate.
            points = [162, 165, 249, 1026]
        elif name == "releaseUsing" and raygun:
            points = [25, 28]
        else:
            points = []
        if name in SENDERS and raygun:
            validate_sender(m, SENDERS[name])
        out.append(summarize(m, points))
    if not 1 <= len(out) <= 45:
        raise PacketAmmoProbeError("selected JVM method population exceeds budget")
    if raygun and not {"onUseTick", "releaseUsing", "findAmmo", "use"}.issubset(
        {m["name"] for m in out}
    ):
        raise PacketAmmoProbeError("incomplete sender/ammo method coverage")
    return out


def snapshot_projection(report):
    return {
        "schema_version": report["schema_version"], "scope": report["scope"],
        "artifact": report["artifact"],
        "classes": [
            {"class_path": c["class_path"], "class_sha256": c["class_sha256"],
             "declared_method_count": c["declared_method_count"],
             "selected_methods": [
                 {"name": m["name"], "parsed_method_sha256": m["parsed_method_sha256"]}
                 for m in c["selected_methods"]
             ]}
            for c in report["classes"]
        ],
        "senders": report["senders"]
    }


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise PacketAmmoProbeError("publisher JAR version/hash/size mismatch")
    classes = []
    with zipfile.ZipFile(jar) as arc:
        members = arc.namelist()
        if len(members) != len(set(members)):
            raise PacketAmmoProbeError("duplicate ZIP member")
        for path in (RAYGUN, PACKET):
            data = arc.read(path)
            digest = hashlib.sha256(data).hexdigest()
            if path == RAYGUN and digest != RAYGUN_SHA:
                raise PacketAmmoProbeError("RaygunItem binary changed")
            disassembly = javap(javap_bin, jar, path[:-6].replace("/", "."))
            declaration = next((line.strip() for line in disassembly.splitlines()
                                if line.strip().endswith("{") and
                                ("class " in line or "interface " in line or "record " in line)), "")
            if not declaration or len(declaration) > 400:
                raise PacketAmmoProbeError("missing/bounded JVM class declaration")
            methods = parse_methods(disassembly)
            selected = select(methods, RAYGUN_METHODS, raygun=(path == RAYGUN))
            classes.append({
                "class_path": path, "class_sha256": digest,
                "class_declaration": declaration,
                "type_checks": [
                    {"name": name_of(m), "offset": i["offset"],
                     "opcode": i["opcode"], "symbol": i["symbol"]}
                    for m in methods for i in m["instructions"]
                    if path == PACKET and name_of(m) == "handle" and
                       i["opcode"] in {"instanceof", "checkcast"}
                ],
                "declared_method_count": len(methods),
                "declared_methods": [{"name": name_of(m), "descriptor": m["descriptor"]}
                                     for m in methods],
                "selected_methods": selected
            })
    return {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_RAYGUN_AMMO_AND_UPDATE_ITEM_TAG_C2S_SELECTED_BYTECODE",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "classes": classes,
        "senders": [{"method": k, **{"constructor_offset": v[0],
                    "sender_offset": v[1]}} for k,v in sorted(SENDERS.items())],
        "limits": {
            "dynamic_packet_authorization": "NOT_PROVEN",
            "C2S_does_not_establish_server_authority": True,
            "read_only_no_full_class_export": True,
            "complete_control_flow": "NOT_RECONSTRUCTED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED"
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--snapshot", type=Path)
    args = parser.parse_args()
    report = audit(args.jar, args.javap)
    if args.snapshot is not None:
        expected = json.loads(args.snapshot.read_text(encoding="utf8"),
                              object_pairs_hook=strict_pairs)
        if snapshot_projection(report) != expected:
            raise PacketAmmoProbeError("SHA-exact C2S/ammo manifest drift")
    raw = json.dumps(report, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    if len(raw.encode("utf8")) > MAX_REPORT_BYTES:
        raise PacketAmmoProbeError("bounded export exceeded size limit")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(raw, encoding="utf8")
    print("raygun_packet_and_ammo_static_evidence=" +
          str(sum(len(c["selected_methods"]) for c in report["classes"])) +
          " methods; NO_RUNTIME_OR_SECURITY_CERTIFICATION")


if __name__ == "__main__":
    main()
