#!/usr/bin/env python3
"""Read-only 1.0.10 Raygun C2S receiver/UpdatesStackTags dispatch audit.

Version and code ownership are JAR-verified. This is not a security assessment
or physical gameplay certification: exported JVM references are bounded, and
branch-dataflow/authorization must not be inferred from a sender call.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file

ROOT = "com/github/alexmodguy/alexscaves/"
RAYGUN = ROOT + "server/item/RaygunItem.class"
PACKET = ROOT + "server/message/UpdateItemTagMessage.class"
UPDATES = ROOT + "server/item/UpdatesStackTags.class"
COMPAT = ROOT + "server/misc/ACCompat.class"
SET_TAG = "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V"
EXPECTED = {
    RAYGUN: "3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c",
    PACKET: "bda52d12e8cce7e010b3d4cd2db7d83000e78b35657c55773a8ba91a070478c8",
}
HANDLE = "(Lcom/github/alexmodguy/alexscaves/server/message/UpdateItemTagMessage;Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;)V"
C2S = "UpdateItemTagMessage"
RECEIVER_INTERFACE = "UpdatesStackTags.updateTagFromServer:"
ANCHORS = {
    "handle": {
        8: ("invokeinterface", "ACNetworkContext.getSender:"),
        15: ("invokeinterface", "ACNetworkContext.isClientSide:"),
        42: ("invokevirtual", "Level.getEntity:"),
        78: ("invokevirtual", "ItemStack.getItem:"),
        81: ("invokevirtual", "ItemStack.is:"),
        113: ("invokevirtual", "ItemStack.is:"),
        158: ("invokestatic", "ACCompat.getTag:"),
        171: ("invokestatic", "ACCompat.getTag:"),
        174: ("invokeinterface", RECEIVER_INTERFACE)
    },
    "onUseTick": {
        162: ("invokespecial", 'UpdateItemTagMessage."<init>":'),
        165: ("invokestatic", "AlexsCaves.sendMSGToServer:")
    },
    "releaseUsing": {
        25: ("invokespecial", 'UpdateItemTagMessage."<init>":'),
        28: ("invokestatic", "AlexsCaves.sendMSGToServer:")
    }
}
MAX_JSON_BYTES = 110000

class ReceiverProbeError(ValueError):
    pass

def method_name(m):
    return m["header"].split("(", 1)[0].split()[-1].rsplit(".", 1)[-1]

def method_hash(m):
    return hashlib.sha256(json.dumps(m, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def class_declaration(output, class_path):
    name = class_path[:-6].replace("/", ".")
    candidates = [line.strip() for line in output.splitlines()
                  if name in line and (line.strip().endswith("{") or line.strip().endswith(";"))
                  and (" class " in " " + line or " interface " in " " + line)]
    if len(candidates) != 1:
        raise ReceiverProbeError("ambiguous/missing javap type declaration for " + name)
    raw = candidates[0]
    if len(raw) > 3500:
        raise ReceiverProbeError("oversize type declaration")
    kind = "interface" if re.search(r"\binterface\b", raw) else "class"
    supers = re.search(r"\bextends\s+([\w.$]+)", raw)
    return {"kind": kind, "declaration": raw,
            "direct_superclass_or_interface": supers.group(1) if supers else None,
            "mentions_updates_interface": "UpdatesStackTags" in raw}

def method_by_sig(methods, name, descriptor):
    found = [m for m in methods if method_name(m) == name and m["descriptor"] == descriptor]
    if len(found) != 1:
        raise ReceiverProbeError("missing/ambiguous JVM method " + name)
    if len({r["offset"] for r in found[0]["instructions"]}) != len(found[0]["instructions"]):
        raise ReceiverProbeError("duplicate JVM offsets " + name)
    return found[0]

def anchor(method, off, opcode, symbol):
    hits = [x for x in method["instructions"] if x["offset"] == off]
    if len(hits) != 1 or hits[0]["opcode"] != opcode or symbol not in hits[0]["symbol"]:
        raise ReceiverProbeError("exact C2S/receiver callsite drift at " + str(off))
    return hits[0]

def bounded_method(method, offsets):
    ins = method["instructions"]
    if len(ins) > 7000:
        raise ReceiverProbeError("method size export budget")
    groups = [
        {"offset": x["offset"], "opcode": x["opcode"], "operand": x["operand"],
         "symbol": x["symbol"]}
        for x in ins if x["opcode"].startswith(("invoke", "if")) or x["opcode"]
        in {"getfield", "putfield", "getstatic", "putstatic", "instanceof",
            "checkcast", "goto", "ldc", "ldc_w", "bipush", "sipush"}
    ]
    if len(groups) > 450:
        raise ReceiverProbeError("bounded JVM references overflow")
    windows = []
    for off in offsets:
        pos = [i for i, x in enumerate(ins) if x["offset"] == off]
        if len(pos) != 1:
            raise ReceiverProbeError("window offset missing/duplicated")
        i = pos[0]
        windows.append({"at": off, "instructions": ins[max(0, i-6):i+8]})
    return {
        "name": method_name(method), "descriptor": method["descriptor"],
        "instruction_count": len(ins), "parsed_method_sha256": method_hash(method),
        "selected_references": groups, "selected_windows": windows
    }

def selected_class(jar, javap_bin, path, sha):
    with zipfile.ZipFile(jar) as z:
        if hashlib.sha256(z.read(path)).hexdigest() != sha:
            raise ReceiverProbeError("exact publisher class digest drift: " + path)
    raw = javap(javap_bin, jar, path[:-6].replace("/", "."))
    methods = parse_methods(raw)
    if len({(method_name(m), m["descriptor"]) for m in methods}) != len(methods):
        raise ReceiverProbeError("duplicate JVM signature")
    return class_declaration(raw, path), methods

def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise ReceiverProbeError("publisher JAR SHA/size drift")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            raise ReceiverProbeError("duplicated ZIP member")
        if UPDATES not in names:
            raise ReceiverProbeError("native UpdatesStackTags interface unavailable")
        updates_sha = hashlib.sha256(z.read(UPDATES)).hexdigest()
    ray_decl, ray_methods = selected_class(jar, javap_bin, RAYGUN, EXPECTED[RAYGUN])
    pkt_decl, pkt_methods = selected_class(jar, javap_bin, PACKET, EXPECTED[PACKET])
    iface_decl, iface_methods = selected_class(jar, javap_bin, UPDATES, updates_sha)
    with zipfile.ZipFile(jar) as z:
        compat_sha = hashlib.sha256(z.read(COMPAT)).hexdigest()
    compat_decl, compat_methods = selected_class(jar, javap_bin, COMPAT, compat_sha)
    setter = method_by_sig(compat_methods, "setTag", SET_TAG)
    if not setter["instructions"]:
        raise ReceiverProbeError("ACCompat.setTag has no observable implementation")
    sender_methods = [
        method_by_sig(ray_methods, "onUseTick",
            "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V"),
        method_by_sig(ray_methods, "releaseUsing",
            "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V")
    ]
    handler = method_by_sig(pkt_methods, "handle", HANDLE)
    validated = []
    for m in sender_methods + [handler]:
        entries = []
        for off, (opcode, sym) in ANCHORS[method_name(m)].items():
            x = anchor(m, off, opcode, sym)
            entries.append({"offset": off, "opcode": x["opcode"], "symbol": x["symbol"]})
        validated.append({"method": method_name(m), "descriptor": m["descriptor"],
                          "validated_callsites": entries,
                          **bounded_method(m, sorted(ANCHORS[method_name(m)]))})
    iface_member = [m for m in iface_methods if method_name(m) == "updateTagFromServer"]
    if not iface_member:
        raise ReceiverProbeError("no matching UpdatesStackTags method declared")
    report = {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_RAYGUN_C2S_RECEIVER_JVM_DISPATCH_ONLY",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "classes": [
            {"path": RAYGUN, "sha256": EXPECTED[RAYGUN],
             "declaration": ray_decl, "declared_method_count": len(ray_methods),
             "sender_methods": validated[:2]},
            {"path": PACKET, "sha256": EXPECTED[PACKET],
             "declaration": pkt_decl, "declared_method_count": len(pkt_methods),
             "receiver": validated[2]},
            {"path": UPDATES, "sha256": updates_sha,
             "declaration": iface_decl, "declared_method_count": len(iface_methods),
             "declared_update_methods": [
                 {"name": method_name(m), "descriptor": m["descriptor"],
                  "declaration": m["header"],
                  "implementation": bounded_method(m, [])}
                 for m in iface_member]},
            {"path": COMPAT, "sha256": compat_sha, "declaration": compat_decl,
             "declared_method_count": len(compat_methods),
             "selected_set_tag": bounded_method(setter, [])}
        ],
        "limits": {"type_declaration_is_direct_only": True,
                   "indirect_inheritance_verified": False,
                   "source_sender_same_as_receiver": "NOT_PROVEN",
                   "receiver_authorization_and_NBT_sanitization": "NOT_PROVEN",
                   "runtime_exploitability": "NOT_ASSESSED",
                   "physical_qa": "NOT_TESTED",
                   "mutating_hook": "NOT_VERIFIED"}
    }
    if len(json.dumps(report, ensure_ascii=False).encode()) > MAX_JSON_BYTES:
        raise ReceiverProbeError("bounded report too large")
    return report

def snapshot_projection(report):
    """Stable SHA-exact four-class boundary without raw full JVM code."""
    classes = report["classes"]
    if len(classes) != 4 or len({c["path"] for c in classes}) != 4:
        raise ReceiverProbeError("invalid four-class sealed roster")
    raygun, packet, interface, compat = classes
    if [c["path"] for c in classes] != [RAYGUN, PACKET, UPDATES, COMPAT]:
        raise ReceiverProbeError("receiver class ordering/identity drift")
    senders = raygun["sender_methods"]
    if [m["name"] for m in senders] != ["onUseTick", "releaseUsing"]:
        raise ReceiverProbeError("missing required sender methods")
    update_methods = interface["declared_update_methods"]
    if len(update_methods) != 1:
        raise ReceiverProbeError("ambiguous update method interface")
    def row(m):
        return {"name": m["name"], "descriptor": m["descriptor"],
                "parsed_method_sha256": m["parsed_method_sha256"],
                "instruction_count": m["instruction_count"]}
    return {
        "schema_version": report["schema_version"],
        "scope": report["scope"],
        "artifact": report["artifact"],
        "class_identities": [{"path": c["path"], "sha256": c["sha256"],
                              "declared_method_count": c["declared_method_count"]}
                             for c in classes],
        "direct_raygun_superclass": raygun["declaration"]["direct_superclass_or_interface"],
        "direct_raygun_updates_interface": raygun["declaration"]["mentions_updates_interface"],
        "sender_methods": [row(m) for m in senders],
        "packet_receiver": row(packet["receiver"]),
        "interface_update_method": {
            **row(update_methods[0]["implementation"]),
            "declaration": update_methods[0]["declaration"]
        },
        "compat_set_tag": row(compat["selected_set_tag"]),
        "anchors": [
            {"method": "handle", "offset": a, "opcode": op, "symbol": sym}
            for a, (op, sym) in sorted(ANCHORS["handle"].items())
        ] + [
            {"method": name, "offset": a, "opcode": op, "symbol": sym}
            for name in ("onUseTick", "releaseUsing")
            for a, (op, sym) in sorted(ANCHORS[name].items())
        ],
        "interface_default_call": {
            "offset": 2,
            "opcode": "invokestatic",
            "symbol_contains": "ACCompat.setTag:"
        },
        "compat_custom_data_calls": [
            {"offset": 5, "symbol_contains": "DataComponents.CUSTOM_DATA:"},
            {"offset": 8, "symbol_contains": "ItemStack.remove:"},
            {"offset": 20, "symbol_contains": "CustomData.of:"},
            {"offset": 23, "symbol_contains": "ItemStack.set:"}
        ]
    }


def verify_sealed_report(report, sealed):
    """Snapshot must match, and critical native writes must remain on exact offsets."""
    measured = snapshot_projection(report)
    if measured != sealed:
        raise ReceiverProbeError("sealed SHA-exact receiver manifest changed")
    classes = report["classes"]
    if not measured["direct_raygun_updates_interface"]:
        raise ReceiverProbeError("Raygun no longer directly implements UpdatesStackTags")
    member = classes[2]["declared_update_methods"][0]
    if not member["declaration"].startswith("public default void updateTagFromServer("):
        raise ReceiverProbeError("default interface implementation declaration changed")
    def require_reference(m, offset, symbol, opcode=None):
        hits = [i for i in m["selected_references"] if i["offset"] == offset]
        if (len(hits) != 1 or symbol not in hits[0]["symbol"]
                or opcode is not None and hits[0]["opcode"] != opcode):
            raise ReceiverProbeError("native receiver write/read path drift " + str(offset))
    require_reference(member["implementation"], 2, "ACCompat.setTag:", "invokestatic")
    setter = classes[3]["selected_set_tag"]
    for row in sealed["compat_custom_data_calls"]:
        require_reference(setter, row["offset"], row["symbol_contains"])
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--javap", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--snapshot", type=Path)
    args = parser.parse_args()
    report = audit(args.jar, args.javap)
    if args.snapshot is not None:
        sealed = json.loads(args.snapshot.read_text(encoding="utf8"))
        verify_sealed_report(report, sealed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True,
                                      ensure_ascii=False) + "\n", encoding="utf8")
    print("raygun_jvm_direct_receiver_boundary=OBSERVED_ONLY; physical_qa=NOT_TESTED")

if __name__ == "__main__":
    main()
