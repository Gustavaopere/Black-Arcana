#!/usr/bin/env python3
"""Publisher-only ticket-controller ingress and caller census (read-only).

Classfile member references and direct JVM access sites are distinguished.
No transformed classes, engine ticket acceptance, quotas or gameplay tested.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

PREFIX = "com/github/alexmodguy/alexscaves/server/"
PLATFORM = PREFIX + "misc/ACPlatform"
DETONATOR = PREFIX + "item/RemoteDetonatorItem"
CONTROLLER = "net/neoforged/neoforge/common/world/chunk/TicketController"
REGISTER_EVENT = "net/neoforged/neoforge/common/world/chunk/RegisterTicketControllersEvent"
VALIDATION = "net/neoforged/neoforge/common/world/chunk/LoadingValidationCallback"
REGISTRATION_OWNER = "com/github/alexmodguy/alexscaves/AlexsCaves"
CHUNK_HELPER_OWNERS = {
    DETONATOR, PREFIX + "item/OccultGemItem", PREFIX + "entity/item/BeholderEyeEntity",
    PREFIX + "entity/item/NuclearExplosionEntity",
}
MEMBER_OPS = {"getstatic", "putstatic", "getfield", "putfield",
              "invokevirtual", "invokespecial", "invokestatic", "invokeinterface"}
LIMITS = {
    "effective_controller": "NOT_VERIFIED", "engine_ticket_acceptance": "NOT_VERIFIED",
    "ticket_lifetime": "NOT_VERIFIED", "effective_unforce": "NOT_VERIFIED",
    "modlauncher_loaded_classes": "NOT_OBSERVED", "world_safety": "BLOCKED",
    "static_contract": "NOT_CERTIFIED", "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
    "provider_universe_closed": False, "semantic_magic_roots_delta": 0,
}


def relevant(tag, owner, name):
    return ((tag == 9 and owner == PLATFORM and name == "ticketController")
            or (tag in (10, 11) and (
                (owner == PLATFORM and name in {"forceChunk", "setTicketController"})
                or (owner in CHUNK_HELPER_OWNERS and name == "loadChunksAround")
                or owner in {CONTROLLER, REGISTER_EVENT, VALIDATION})))


def selected_refs(reader):
    out = {}
    for i, entry in enumerate(reader.pool):
        if entry is None or entry[0] not in (9, 10, 11):
            continue
        tag, owner, signature = reader.resolve(i)
        _, name, descriptor = signature
        if relevant(tag, owner, name):
            out[i] = {"kind": tag, "owner": owner, "name": name, "descriptor": descriptor}
    return out


def registration_evidence(reader, parsed, archive, jar, javap):
    keys = [k for k in parsed if k[0] == "registerTicketControllers"]
    require(len(keys) == 1, "registration method not unique")
    key = keys[0]
    method = summarize(reader, key, parsed[key])
    bootstraps = []
    callback_keys = set()
    for offset, (opcode, operand, symbol) in sorted(parsed[key].items()):
        if opcode != "invokedynamic":
            continue
        match = re.match(r"#(\d+)(?:\s*,\s*\d+)?$", operand.strip())
        require(match is not None, "unparsed invokedynamic operand")
        tag, bootstrap_index, signature = reader.resolve(int(match.group(1)))
        require(tag == 18 and signature[0] == 12, "unexpected invokedynamic constant")
        if signature[1] != "validateTickets":
            continue
        bootstrap = reader.attributes["bootstrap_methods"][bootstrap_index]
        bootstraps.append({"offset": offset, "bootstrap_index": bootstrap_index,
                           "signature": signature, "bootstrap": bootstrap})
        for arg in bootstrap["arguments"]:
            ref = arg.get("reference") if isinstance(arg, dict) else None
            if isinstance(ref, list) and len(ref) == 3 and ref[0] in (10, 11):
                if ref[1].startswith("com/github/alexmodguy/alexscaves/"):
                    callback_keys.add((ref[1], ref[2][1], ref[2][2]))
    require(len(bootstraps) == 1 and len(callback_keys) == 1, "validation callback binding unresolved")
    owner, name, descriptor = next(iter(callback_keys))
    require(owner == PREFIX + "level/storage/ACWorldData" and name == "clearLoadedChunksCallback",
            "callback target differs from existing exact Occult Gem evidence")
    raw = archive.read(owner + ".class")
    callback_reader = ClassReader(raw)
    require(callback_reader.name == owner and callback_reader.major == 65, "callback class identity")
    callback_parsed = disassemble(jar, javap, owner)
    callback = (name, descriptor)
    require(callback in callback_parsed and bool(callback_parsed[callback]), "callback executable body missing")
    return {"registration": method, "bootstrap": bootstraps[0],
            "validation_callback_owner": owner, "validation_callback_class_sha256": digest(raw),
            "validation_callback": summarize(callback_reader, callback, callback_parsed[callback])}


def inspect(jar, javap, output):
    verify_artifact(jar)
    require(not output.exists(), "report must be write-once")
    candidates, site_count, registration = {}, 0, None
    with ZipFile(jar) as archive:
        paths = archive.namelist()
        require(len(paths) == len(set(paths)), "duplicate ZIP paths")
        classes = sorted(p for p in paths if p.endswith(".class"))
        require(len(classes) == 1555, "publisher class roster drift")
        for path in classes:
            raw = archive.read(path)
            reader = ClassReader(raw)
            require(path == reader.name + ".class" and reader.major == 65, "class identity drift")
            refs = selected_refs(reader)
            if not refs:
                continue
            parsed = disassemble(jar, javap, reader.name)
            if reader.name == REGISTRATION_OWNER:
                registration = registration_evidence(reader, parsed, archive, jar, javap)
            methods = []
            for key, body in sorted(parsed.items()):
                rows = sorted(body.items())
                sites = []
                for i, (offset, (opcode, operand, symbol)) in enumerate(rows):
                    if opcode not in MEMBER_OPS:
                        continue
                    match = re.match(r"#(\d+)(?:\s*,\s*\d+)?$", operand.strip())
                    require(match is not None, "unparsed member operand in " + reader.name)
                    index = int(match.group(1))
                    if index not in refs:
                        continue
                    sites.append({"offset": offset, "opcode": opcode, "member": refs[index],
                                  "previous": [
                                      {"offset": pos, "opcode": op, "operand": arg, "symbol": sym}
                                      for pos, (op, arg, sym) in rows[max(0, i-4):i]
                                  ]})
                if sites:
                    method = summarize(reader, key, body)
                    methods.append({"name": key[0], "descriptor": key[1],
                                    "code_sha256": method["declaration"]["code_sha256"],
                                    "instruction_sha256": method["instruction_sha256"],
                                    "instruction_count": method["instruction_count"], "sites": sites})
                    site_count += len(sites)
            candidates[reader.name] = {"class_sha256": digest(raw),
                                       "member_constants": [{"index": i, **ref} for i, ref in sorted(refs.items())],
                                       "methods": methods}
    require(PLATFORM in candidates and DETONATOR in candidates, "known publisher owner absent")
    require(0 < len(candidates) <= 100 and 0 < site_count <= 1000, "census budget")
    require(registration is not None, "registration evidence missing")
    report = {"schema_version": 2, "scope": "PUBLISHER_TICKET_REGISTRATION_AND_MEMBER_CENSUS_ONLY",
              "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
              "class_entries_scanned": len(classes), "candidate_owners": candidates,
              "direct_site_count": site_count, "registration": registration, "limits": LIMITS}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf8") as stream:
        stream.write(canonical(report))
    print("TICKET_REPORT_SHA256", digest(output.read_bytes()), "BYTES", output.stat().st_size)
    print("CENSUS", len(classes), "CANDIDATES", len(candidates), "DIRECT_SITES", site_count)
    for owner, entry in candidates.items():
        print("OWNER", owner, entry["class_sha256"], "CONSTANTS", len(entry["member_constants"]))
        for method in entry["methods"]:
            print("METHOD", method["name"], method["descriptor"], method["code_sha256"],
                  method["instruction_count"], method["instruction_sha256"])
            for site in method["sites"]:
                print("SITE", json.dumps(site, sort_keys=True, ensure_ascii=False))
    print("REGISTRATION", json.dumps(registration, sort_keys=True, ensure_ascii=False))
    print("NO_MUTATION NOT_CERTIFIED WORLD_SAFETY_BLOCKED")


def self_test():
    cases = [
        (9, PLATFORM, "ticketController", True),
        (10, PLATFORM, "forceChunk", True),
        (10, PLATFORM, "setTicketController", True),
        (10, REGISTER_EVENT, "register", True),
        (11, VALIDATION, "validateTickets", True),
        (10, PREFIX + "entity/item/NuclearExplosionEntity", "loadChunksAround", True),
        (10, PREFIX + "item/OccultGemItem", "loadChunksAround", True),
        (11, DETONATOR, "loadChunksAround", True),
        (10, CONTROLLER, "forceChunk", True),
        (9, PLATFORM, "other", False),
        (10, PLATFORM, "ticketController", False),
        (10, "fake/ACPlatform", "forceChunk", False),
        (9, CONTROLLER, "forceChunk", False),
        (10, DETONATOR, "other", False),
    ]
    for tag, owner, name, expected in cases:
        require(relevant(tag, owner, name) == expected, "typed member filter mismatch")
    print("PASS:", len(cases), "typed member filter cases")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--javap", default="javap")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        require(args.jar is not None and args.output is not None, "jar/output required")
        inspect(args.jar, args.javap, args.output)
